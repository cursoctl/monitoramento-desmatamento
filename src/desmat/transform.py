import logging
import geopandas as gpd

logger = logging.getLogger(__name__)

def transformar_sicar(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Padroniza e valida o GeoDataFrame do SICAR."""
    logger.info("Iniciando transformação dos dados do SICAR.")
    
    # Resolve TODO: Renomeação dinâmica para o padrão do banco
    mapeamento = {
        'cod_imovel': 'codigo_car',
        'num_car': 'codigo_car',
        'nome': 'nome_imovel',
        'nm_imovel': 'nome_imovel',
        'municipio': 'municipio',
        'area_ha': 'gleba_ha'
    }
    gdf = gdf.rename(columns={k: v for k, v in mapeamento.items() if k in gdf.columns})
    
    # Mantém apenas colunas necessárias
    colunas_validas = ['codigo_car', 'nome_imovel', 'municipio', 'gleba_ha', 'geometry']
    gdf = gdf[[col for col in colunas_validas if col in gdf.columns]]
    
    # Padronização de Sistema de Coordenadas (CRS)
    if gdf.crs != "EPSG:4674":
        gdf = gdf.to_crs("EPSG:4674")
        
    return gdf

def transformar_alertas(gdf: gpd.GeoDataFrame, fonte: str) -> gpd.GeoDataFrame:
    """Padroniza e valida os alertas de desmatamento."""
    logger.info(f"Iniciando transformação de alertas da fonte: {fonte}.")
    
    # Força a marcação da origem do dado
    gdf['fonte'] = fonte
    
    mapeamento = {
        'id': 'id_alerta',
        'alert_id': 'id_alerta',
        'data': 'data_alerta',
        'dt_alerta': 'data_alerta',
        'area': 'area_alerta_ha',
        'hectares': 'area_alerta_ha'
    }
    gdf = gdf.rename(columns={k: v for k, v in mapeamento.items() if k in gdf.columns})
    
    # Garante tipagem de data
    if 'data_alerta' in gdf.columns:
        gdf['data_alerta'] = gpd.pd.to_datetime(gdf['data_alerta']).dt.date
        
    if gdf.crs != "EPSG:4674":
        gdf = gdf.to_crs("EPSG:4674")
        
    return gdf

