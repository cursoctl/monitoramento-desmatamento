import geopandas as gpd
import pytest
from shapely.geometry import Polygon, box

from desmat.transform import padronizar


def test_reprojeta_para_sirgas2000():
    gdf = gpd.GeoDataFrame(geometry=[box(-53, -31, -52, -30)], crs="EPSG:4326")
    assert padronizar(gdf).crs.to_epsg() == 4674


def test_corrige_geometria_invalida():
    laco = Polygon([(0, 0), (1, 1), (1, 0), (0, 1)])
    gdf = gpd.GeoDataFrame(geometry=[laco], crs="EPSG:4674")
    assert padronizar(gdf).geometry.is_valid.all()


def test_exige_crs():
    gdf = gpd.GeoDataFrame(geometry=[box(0, 0, 1, 1)])
    with pytest.raises(ValueError):
        padronizar(gdf)


def test_sempre_multipolygon():
    gdf = gpd.GeoDataFrame(geometry=[box(0, 0, 1, 1)], crs="EPSG:4674")
    assert padronizar(gdf).geometry.geom_type.eq("MultiPolygon").all()
