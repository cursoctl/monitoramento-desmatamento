import logging
import folium
import geopandas as gpd
from sqlalchemy import create_engine
from desmat.config import Config

logger = logging.getLogger(__name__)

def gerar_mapa_auditoria():
    logger.info("Conectando ao PostGIS para extrair dados da auditoria...")
    engine = create_engine(Config.get_db_url())
    
    # Busca a view materializada convertendo a coluna geométrica para o GeoPandas
    query = "SELECT codigo_car, nome_imovel, municipio, hectares_desmatados, geom_interseccao as geometry FROM public.mv_auditoria_desmatamento;"
    gdf_auditoria = gpd.read_postgis(query, con=engine, geom_col="geometry", crs="EPSG:4674")
    
    if gdf_auditoria.empty:
        logger.warning("Nenhuma intersecção espacial encontrada para mapear.")
        return
    
    # Centraliza o mapa em Pelotas (-31.76, -52.33)
    mapa = folium.Map(location=[-31.7654, -52.3376], zoom_start=11, tiles="OpenStreetMap")
    
    # Adiciona camada de Satélite para dar o visual do Agro
    folium.TileLayer(
        tiles="https://google.com{x}&y={y}&z={z}",
        attr="Google Satellite",
        name="Satélite (Google)",
        overlay=False,
        control=True
    ).add_to(mapa)
    
    logger.info("Plotando polígonos de desmatamento no mapa interativo...")
    
    # Converte para GeoJSON para o Folium renderizar
    for _, row in gdf_auditoria.iterrows():
        # Cria a máscara vermelha do desmatamento (Estilo Cyber/Alerta)
        geojson_data = folium.GeoJson(
            row["geometry"].__geo_interface__,
            style_function=lambda x: {
                "fillColor": "#d62728",
                "color": "#d62728",
                "weight": 2,
                "fillOpacity": 0.6
            }
        )
        
        # Pop-up dinâmico ao clicar no polígono
        popup_html = f"""
        <div style="font-family: Arial, sans-serif; width: 220px; font-size: 12px;">
            <h4 style="margin: 0 0 5px 0; color: #d62728;">🚨 ALERTA DE COMPLIANCE</h4>
            <b>Imóvel:</b> {row['nome_imovel']}<br>
            <b>CAR:</b> {row['codigo_car']}<br>
            <b>Município:</b> {row['municipio']}<br>
            <hr style="border: 0; border-top: 1px solid #ccc; margin: 5px 0;">
            <span style="color: red; font-weight: bold;">Sobreposição: {row['hectares_desmatados']:.2f} ha</span>
        </div>
        """
        folium.Popup(popup_html, max_width=250).add_to(geojson_data)
        geojson_data.add_to(mapa)
        
    folium.LayerControl().add_to(mapa)
    
    # Salva o arquivo HTML final pronto para o portfólio
    caminho_mapa = "docs/mapa_interativo.html"
    mapa.save(caminho_mapa)
    logger.info(f"🏆 Mapa interativo HTML gerado com sucesso em: {caminho_mapa}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    gerar_mapa_auditoria()

