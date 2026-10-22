import os
from pathlib import Path
import geopandas as gpd
from shapely.geometry import Polygon

def gerar_arquivos_teste():
    base_dir = Path(__file__).resolve().parent / "data" / "raw"
    os.makedirs(base_dir, exist_ok=True)
    
    print("Gerando dados espaciais fictícios para a região de Pelotas...")
    
    # 1. Cria duas fazendas (CAR) no padrão SIRGAS 2000 (EPSG:4674)
    dados_car = {
        'num_car': ['RS-4314407-0001', 'RS-4314407-0002'],
        'nm_imovel': ['Fazenda Pampa Seguro', 'Estância das Missões'],
        'municipio': ['Pelotas', 'Pelotas'],
        'area_ha': [250.50, 180.20],
        'geometry': [
            Polygon([(-52.34, -31.76), (-52.32, -31.76), (-52.32, -31.78), (-52.34, -31.78)]),
            Polygon([(-52.30, -31.74), (-52.28, -31.74), (-52.28, -31.76), (-52.30, -31.76)])
        ]
    }
    gdf_car = gpd.GeoDataFrame(dados_car, crs="EPSG:4674")
    gdf_car.to_file(base_dir / "sicar_teste.gpkg", driver="GPKG")
    
    # 2. Cria um alerta de desmatamento (PRODES) invadindo a Fazenda 0001
    dados_prodes = {
        'id': ['PRODES_2026_001'],
        'data': ['2026-10-22'],
        'hectares': [15.40],
        'geometry': [
            Polygon([(-52.33, -31.77), (-52.31, -31.77), (-52.31, -31.79), (-52.33, -31.79)])
        ]
    }
    gdf_prodes = gpd.GeoDataFrame(dados_prodes, crs="EPSG:4674")
    gdf_prodes.to_file(base_dir / "alertas_prodes_teste.shp")
    
    print(f"Arquivos gerados com sucesso em: {base_dir}")

if __name__ == "__main__":
    gerar_arquivos_teste()

