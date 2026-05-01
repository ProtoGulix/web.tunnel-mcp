# tunnel-mcp

Serveur MCP (Model Context Protocol) **read-only** qui expose les données de l'API Tunnel GMAO à des clients MCP (Claude.ai, Claude Code, etc.). Il agit comme une passerelle légère : il ne contient aucune logique métier et ne touche jamais la base de données — il relaie les requêtes vers `tunnel-backend` via HTTP avec un token Bearer CONSULTANT.

## Prérequis

- Python 3.12+
- Un compte CONSULTANT actif sur l'instance Tunnel cible (ex: `mcp-consultant@frezille.fr`)
- `tunnel-backend` accessible (local ou Docker)

## Setup dev (stdio)

```bash
cp .env.example .env
# Éditer TUNNEL_API_TOKEN avec le token du compte CONSULTANT
pip install -e .
python server.py
```

Le serveur démarre en mode `stdio`, prêt à être utilisé par Claude Code.

## Tools exposés

| Tool | Domaine | Description |
|------|---------|-------------|
| `get_interventions` | Interventions | Liste avec filtres (status, priorité, équipement) |
| `get_intervention_detail` | Interventions | Détail complet d'une intervention |
| `get_actions` | Actions | Liste des actions d'intervention |
| `get_data_quality` | Actions | Anomalies de qualité de données |
| `get_equipements` | Équipements | Liste avec recherche textuelle |
| `get_equipement_detail` | Équipements | Détail et stats d'un équipement |
| `get_dashboard_summary` | KPIs | Compteurs globaux du tableau de bord |
| `get_stats_anomalies_summary` | KPIs | Résumé agrégé des anomalies |

## Intégration docker-compose.yml

Ajouter dans le `docker-compose.yml` de `tunnel-backend` :

```yaml
tunnel-mcp:
  build: ../tunnel-mcp
  container_name: tunnel-mcp
  env_file:
    - ../tunnel-mcp/.env
  environment:
    - TUNNEL_API_BASE_URL=http://tunnel-api:8000
    - MCP_TRANSPORT=sse
  ports:
    - "8001:8001"
  depends_on:
    - api
  restart: unless-stopped
```

## Licence

AGPL-3.0
