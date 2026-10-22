-- Ativa a extensão espacial
CREATE EXTENSION IF NOT EXISTS postgis;

-- Tabela de Propriedades Rurais (SICAR)
CREATE TABLE IF NOT EXISTS public.propriedades_sicar (
    id SERIAL PRIMARY KEY,
    codigo_car VARCHAR(100) UNIQUE NOT NULL,
    nome_imovel VARCHAR(255),
    municipio VARCHAR(100),
    gleba_ha NUMERIC(12, 2),
    geometry geometry(MultiPolygon, 4674),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Alertas (PRODES / MapBiomas)
CREATE TABLE IF NOT EXISTS public.alertas_desmatamento (
    id SERIAL PRIMARY KEY,
    id_alerta VARCHAR(100) UNIQUE NOT NULL,
    fonte VARCHAR(50) NOT NULL,
    data_alerta DATE,
    area_alerta_ha NUMERIC(12, 2),
    geometry geometry(MultiPolygon, 4674),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices Espaciais de Performance (GIST)
CREATE INDEX IF NOT EXISTS idx_propriedades_sicar_geom ON public.propriedades_sicar USING GIST(geometry);
CREATE INDEX IF NOT EXISTS idx_alertas_desmatamento_geom ON public.alertas_desmatamento USING GIST(geometry);

