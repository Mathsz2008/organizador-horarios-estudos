from datetime import date

from pydantic import BaseModel


class AtividadeSchema(BaseModel):
    titulo: str
    descricao: str | None = None
    disciplina: str
    data_entrega: date
    concluida: bool = False


class AtividadePublic(AtividadeSchema):
    id: int


class AtividadeList(BaseModel):
    atividades: list[AtividadePublic]


class Message(BaseModel):
    message: str
