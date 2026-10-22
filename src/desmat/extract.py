import geopandas as gpd
import requests

from .config import RAW_DIR


def baixar_wfs(url: str, camada: str, destino: str) -> gpd.GeoDataFrame:
    """Baixa uma camada via WFS (GeoJSON) e salva em data/raw."""
    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "typeName": camada,
        "outputFormat": "application/json",
    }
    resp = requests.get(url, params=params, timeout=300)
    resp.raise_for_status()
    caminho = RAW_DIR / destino
    caminho.write_bytes(resp.content)
    return gpd.read_file(caminho)


def ler_arquivo(caminho) -> gpd.GeoDataFrame:
    """Lê shapefile/GeoPackage/GeoJSON já baixado manualmente."""
    return gpd.read_file(caminho)
