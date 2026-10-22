# Dicionário de dados

## municipios
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| cd_mun | text | Código IBGE do município |
| nm_mun | text | Nome |
| sigla_uf | text | UF |
| geom | MultiPolygon 4674 | Limite municipal |

## prodes_desmatamento
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| ano | integer | Ano de detecção |
| bioma | text | Bioma |
| area_ha | numeric | Área em hectares |
| geom | MultiPolygon 4674 | Polígono de supressão |
