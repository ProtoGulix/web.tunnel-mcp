from typing import Optional
from mcp.server.fastmcp import FastMCP
from client import tunnel_client


def register(app: FastMCP):
    @app.tool()
    async def get_actions(
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        tech_id: Optional[str] = None,
    ) -> list:
        """Liste les actions groupées par date, du plus récent au plus ancien.
        Sans paramètre : actions du jour uniquement.
        start_date / end_date au format YYYY-MM-DD.
        tech_id : UUID du technicien pour filtrer ses actions."""
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if tech_id:
            params["tech_id"] = tech_id
        return await tunnel_client.get("/intervention-actions", params=params)

    @app.tool()
    async def get_action_detail(action_id: str) -> dict:
        """Détail complet d'une action : sous-catégorie, technicien, tâches liées,
        demandes d'achat, et contexte complet de l'intervention parente."""
        return await tunnel_client.get(f"/intervention-actions/{action_id}")

    @app.tool()
    async def create_action(
        intervention_id: str,
        action_subcategory: int,
        tech: str,
        complexity_score: int,
        time_spent: Optional[float] = None,
        action_start: Optional[str] = None,
        action_end: Optional[str] = None,
        description: Optional[str] = None,
        complexity_factor: Optional[str] = None,
        created_at: Optional[str] = None,
        tasks: Optional[list] = None,
    ) -> dict:
        """Ajoute une action à une intervention.

        Deux modes exclusifs pour le temps :
        - Mode bornes  : fournir action_start + action_end (format HH:MM:SS)
        - Mode direct  : fournir time_spent (multiple de 0.25h : 0.25, 0.5, 0.75…)

        complexity_factor est obligatoire si complexity_score > 5.

        tasks (optionnel) : liste de dicts pour tagger des tâches simultanément.
          Chaque dict : { task_id, close_task?, skip?, skip_reason? }
          skip et close_task sont mutuellement exclusifs.
          skip_reason est obligatoire si skip=true."""
        body: dict = {
            "intervention_id": intervention_id,
            "action_subcategory": action_subcategory,
            "tech": tech,
            "complexity_score": complexity_score,
        }
        if time_spent is not None:
            body["time_spent"] = time_spent
        if action_start:
            body["action_start"] = action_start
        if action_end:
            body["action_end"] = action_end
        if description:
            body["description"] = description
        if complexity_factor:
            body["complexity_factor"] = complexity_factor
        if created_at:
            body["created_at"] = created_at
        if tasks:
            body["tasks"] = tasks
        return await tunnel_client.post("/intervention-actions", body)

    @app.tool()
    async def update_action(
        action_id: str,
        description: Optional[str] = None,
        time_spent: Optional[float] = None,
        action_start: Optional[str] = None,
        action_end: Optional[str] = None,
        action_subcategory: Optional[int] = None,
        tech: Optional[str] = None,
        complexity_score: Optional[int] = None,
        complexity_factor: Optional[str] = None,
        created_at: Optional[str] = None,
    ) -> dict:
        """Met à jour partiellement une action existante. Seuls les champs fournis sont modifiés.

        Modes de temps mutuellement exclusifs : time_spent OU action_start+action_end.
        complexity_factor obligatoire si le score résultant > 5.
        created_at modifiable pour corriger une erreur de saisie (backdating)."""
        body: dict = {}
        if description is not None:
            body["description"] = description
        if time_spent is not None:
            body["time_spent"] = time_spent
        if action_start:
            body["action_start"] = action_start
        if action_end:
            body["action_end"] = action_end
        if action_subcategory is not None:
            body["action_subcategory"] = action_subcategory
        if tech:
            body["tech"] = tech
        if complexity_score is not None:
            body["complexity_score"] = complexity_score
        if complexity_factor:
            body["complexity_factor"] = complexity_factor
        if created_at:
            body["created_at"] = created_at
        return await tunnel_client.patch(f"/intervention-actions/{action_id}", body)
