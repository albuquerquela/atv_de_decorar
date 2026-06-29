from flask import Blueprint, render_template

from models import Jogador

__all__ = Blueprint


@dashboard_bp.route("/")
def index():
    return render_template(
        "index.html",
        total_jogadores=Jogador.query.count(),
    )
