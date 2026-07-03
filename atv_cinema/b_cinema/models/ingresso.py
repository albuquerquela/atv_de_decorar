from . import db
from .base import ModeloBase


class Ingresso(ModeloBase):
    """Opcional — vale ponto extra se implementar compra de ingresso."""

    __tablename__ = "ingressos"

    
    sessoes_id = db.Column(db.String(15), primary_key=True)
    assento = db.Column(db.String(10), nullable=False)
    nome_comprador = db.Column(db.String(120), nullable=False)

    
    sessoes = db.relationship("Sessão", back_populates = "ingressos")
