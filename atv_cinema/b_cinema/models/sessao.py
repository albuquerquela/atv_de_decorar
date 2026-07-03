from . import db
from .base import ModeloBase


class Sessao(ModeloBase):
    __tablename__ = "sessoes"

    filme_id = db.Column(db.Integer, primary_key=True)
    sala_id = db.Column(db.String, primary_key=True)
    data_hora = db.Column(db.DateTime, nullable=False)
    preco = db.Column(db.Float, nullable=False)

    filme = db.relationship("Filmes", back_populates = "sessão")
    ingressos = db.relationship("Ingresso", back_populates = "sessão")
    sala = db.relationship("Sala", back_populates = "sessão")
    @classmethod
    def listar_com_detalhes(cls):
        return cls.query.order_by(cls.data_hora.desc()).all()
