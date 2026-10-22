import logging
from pathlib import Path
import geopandas as gpd
from desmat.config import Config
from desmat.transform import transformar_sicar, transformar_alertas
from desmat.load import carregar_dados_espaciais

# Configuração de Logging profissional para o terminal WSL
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("pipeline_desmat")

def rodar_pipeline_completo(caminho_sicar: str, caminho_alertas: str, fonte_alertas: str):
    """
    Executa o ciclo completo de ETL Geo-Cyber:
    1. Extract: Lê as geometrias brutas locais (.gpkg e .shp)
    2. Transform: Trata nomes de colunas, tipagens e reprojeta para SIRGAS 2000
    3. Load: Executa o UPSERT incremental mantendo restrições e índices GIST
    """
    logger.info("--- INICIANDO PIPELINE DE MONITORAMENTO TERRITORIAL ---")
    
    # -------------------------------------------------------------------------
    # 1. ETAPA: EXTRACT
    # -------------------------------------------------------------------------
    try:
        logger.info("Extraindo dados dos arquivos espaciais locais...")
        gdf_sicar_bruto = gpd.read_file(caminho_sicar)
        gdf_alertas_bruto = gpd.read_file(caminho_alertas)
        logger.info(f"Extract Concluído! SICAR: {len(gdf_sicar_bruto)} registros | Alertas: {len(gdf_alertas_bruto)}")
    except Exception as e:
        logger.error(f"Falha crítica na extração dos arquivos de dados: {str(e)}")
        return False

    # -------------------------------------------------------------------------
    # 2. ETAPA: TRANSFORM (Evitando desvios de CRS e tipos)
    # -------------------------------------------------------------------------
    try:
        logger.info("Executando limpeza de atributos e reprojeção de CRS para EPSG:4674...")
        gdf_sicar_processado = transformar_sicar(gdf_sicar_bruto)
        gdf_alertas_processado = transformar_alertas(gdf_alertas_bruto, fonte=fonte_alertas)
        logger.info("Geometrias e colunas padronizadas com sucesso.")
    except Exception as e:
        logger.error(f"Falha crítica na transformação de dados: {str(e)}")
        return False

    # -------------------------------------------------------------------------
    # 3. ETAPA: LOAD (Upsert Seguro)
    # -------------------------------------------------------------------------
    try:
        logger.info(f"Conectando ao banco PostGIS e iniciando UPSERT...")
        
        # Envia propriedades rurais
        carregar_dados_espaciais(
            gdf=gdf_sicar_processado,
            tabela_destino="propriedades_sicar",
            chave_conflito="codigo_car"
        )
        
        # Envia alertas de desmatamento
        carregar_dados_espaciais(
            gdf=gdf_alertas_processado,
            tabela_destino="alertas_desmatamento",
            chave_conflito="id_alerta"
        )
        
        logger.info("--- PIPELINE GEO-CYBER EXECUTADO COM SUCESSO DE PONTA A PONTA ---")
        return True
    except Exception as e:
        logger.error(f"Falha crítica ao persistir dados no banco de dados: {str(e)}")
        return False

if __name__ == "__main__":
    # Define o caminho absoluto da pasta raiz independente de onde o terminal chame o script
    RAIZ_PROJETO = Path(__file__).resolve().parent.parent.parent
    PASTA_RAW = RAIZ_PROJETO / "data" / "raw"
    
    rodar_pipeline_completo(
        caminho_sicar=str(PASTA_RAW / "sicar_teste.gpkg"),
        caminho_alertas=str(PASTA_RAW / "alertas_prodes_teste.shp"),
        fonte_alertas="PRODES"
    )

