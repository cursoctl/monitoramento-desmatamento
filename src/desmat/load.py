import logging
import geopandas as gpd
from sqlalchemy import create_engine, text
from desmat.config import Config

logger = logging.getLogger(__name__)

def carregar_dados_espaciais(gdf: gpd.GeoDataFrame, tabela_destino: str, chave_conflito: str):
    """Carrega dados no PostGIS usando técnica de staging para garantir Upsert."""
    engine = create_engine(Config.get_db_url())
    stg_tabela = f"stg_{tabela_destino}"
    
    try:
        with engine.begin() as conn:
            # 1. Envia para staging (Aqui o replace é seguro pois a tabela cai no final)
            gdf.to_postgis(
                name=stg_tabela,
                con=conn,
                if_exists="replace",
                index=False,
                schema="public"
            )
            
            # Obtém colunas para estruturar a query dinâmica
            colunas = [col for col in gdf.columns if col != 'geometry']
            colunas_str = ", ".join(colunas) + ", geometry"
            select_str = ", ".join([f"s.{col}" for col in colunas]) + ", s.geometry"
            update_str = ", ".join([f"{col} = EXCLUDED.{col}" for col in colunas if col != chave_conflito])
            
            # 2. Executa o SQL de UPSERT nativo salvando tipos do PostGIS
            upsert_query = text(f"""
                INSERT INTO public.{tabela_destino} ({colunas_str})
                SELECT {select_str} FROM public.{stg_tabela} s
                ON CONFLICT ({chave_conflito})
                DO UPDATE SET {update_str}, geometry = EXCLUDED.geometry;
            """)
            
            conn.execute(upsert_query)
            conn.execute(text(f"DROP TABLE IF EXISTS public.{stg_tabela};"))
            logger.info(f"Carga via UPSERT finalizada com sucesso na tabela: {tabela_destino}")
            
    except Exception as e:
        logger.error(f"Erro crítico durante a carga na tabela {tabela_destino}: {str(e)}")
        raise e

