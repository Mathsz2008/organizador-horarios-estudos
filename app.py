from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from schemas import AtividadeList, AtividadePublic, AtividadeSchema, Message

app = FastAPI(title='Agenda Acadêmica')

# Lista temporária usada como banco de dados durante esta etapa.
database: list[AtividadePublic] = []


@app.get('/')
def read_root():
    return {'message': 'Hello World'}


@app.post(
    '/atividades/',
    status_code=HTTPStatus.CREATED,
    response_model=AtividadePublic,
)
def create_atividade(atividade: AtividadeSchema):
    novo_id = max((item.id for item in database), default=0) + 1
    atividade_criada = AtividadePublic(
        id=novo_id,
        **atividade.model_dump(),
    )
    database.append(atividade_criada)
    return atividade_criada


@app.get('/atividades/', response_model=AtividadeList)
def read_atividades():
    return {'atividades': database}


@app.get('/atividades/{atividade_id}', response_model=AtividadePublic)
def read_atividade(atividade_id: int):
    for atividade in database:
        if atividade.id == atividade_id:
            return atividade

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail='Atividade não encontrada',
    )


@app.put('/atividades/{atividade_id}', response_model=AtividadePublic)
def update_atividade(atividade_id: int, atividade: AtividadeSchema):
    for indice, atividade_existente in enumerate(database):
        if atividade_existente.id == atividade_id:
            atividade_atualizada = AtividadePublic(
                id=atividade_id,
                **atividade.model_dump(),
            )
            database[indice] = atividade_atualizada
            return atividade_atualizada

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail='Atividade não encontrada',
    )


@app.delete('/atividades/{atividade_id}', response_model=Message)
def delete_atividade(atividade_id: int):
    for indice, atividade in enumerate(database):
        if atividade.id == atividade_id:
            database.pop(indice)
            return {'message': 'Atividade removida'}

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail='Atividade não encontrada',
    )
