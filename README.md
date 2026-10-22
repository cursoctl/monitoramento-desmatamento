# Monitoramento de Desmatamento

Análise de supressão de vegetação nativa com dados **PRODES/DETER (INPE)** e **MapBiomas**, armazenados em **PostGIS** e consumidos por um dashboard **Power BI**.

> Recorte inicial: bioma **Pampa** (ajustável em `src/desmat/config.py`).

## Pergunta de negócio

Quanto da supressão detectada por ano e por município se sobrepõe a imóveis rurais (CAR) e a áreas protegidas, e onde PRODES e MapBiomas divergem?

## Arquitetura

Fontes públicas -> ETL em Python -> PostGIS -> Power BI / mapa web / GitHub

(inserir aqui a imagem em `docs/arquitetura.png`)

## Stack

Python (geopandas, requests, SQLAlchemy) · PostGIS · Power BI · Docker

## Como rodar

```bash
# 1. ambiente
conda env create -f environment.yml
conda activate desmat
pip install -e .

# 2. banco
cp .env.example .env
docker compose up -d

# 3. pipeline
python -m desmat.pipeline --fonte municipios
python -m desmat.pipeline --fonte prodes
```

## Estrutura

```
src/desmat/   extração, transformação e carga
sql/          schema e views para o Power BI
powerbi/      arquivo .pbix e instruções de conexão
data/         dados brutos e processados (ignorados pelo Git)
docs/         diagrama, dicionário de dados, metodologia
tests/        testes automatizados
```

## Fontes e limitações

- PRODES é anual; para alertas recentes use o DETER.
- PRODES e MapBiomas têm metodologias e áreas mínimas de mapeamento diferentes; as diferenças são parte da análise.
- Confirmar versão e data de cada base baixada (registrar em `docs/fontes.md`).

## Roadmap

- [ ] MVP: PRODES + municípios IBGE no PostGIS
- [ ] Integrar MapBiomas
- [ ] Dashboard Power BI com 3 páginas
- [ ] Camada DETER e agendamento (GitHub Actions)
- [ ] Cruzamento com CAR e unidades de conservação

## Autor

Marcos Leal · [LinkedIn](https://linkedin.com/in/marcosleal-cyber) · [GitHub](https://github.com/cursoctl)
