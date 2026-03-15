from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from . import crud, schemas
from .db import get_db
from .init_db import init_db


app = FastAPI(
    title="CRUD Empreendimentos - Santa Catarina",
    version="1.0.0",
    description="API REST para gerenciamento de empreendimentos em Santa Catarina (desafio CRUD).",
)


@app.on_event("startup")
def _startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/empreendimentos",
    response_model=schemas.EmpreendimentoOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Empreendimentos"],
    summary="Cadastrar um novo empreendimento",
    description="Cria um novo registro de empreendimento no banco de dados de Santa Catarina.",
)
def criar_empreendimento(
    payload: schemas.EmpreendimentoCreate,
    db: Session = Depends(get_db),
) -> schemas.EmpreendimentoOut:
    return crud.create_empreendimento(db, payload)


@app.get(
    "/empreendimentos", 
    response_model=list[schemas.EmpreendimentoOut],
    tags=["Empreendimentos"],
    summary="Listar empreendimentos",
    description="Retorna uma lista de empreendimentos cadastrados, permitindo filtros por município, segmento e status.",
)
def listar_empreendimentos(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    municipio_sc: str | None = Query(default=None),
    segmento_atuacao: schemas.SegmentoAtuacao | None = Query(default=None),
    status_ativo: bool | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[schemas.EmpreendimentoOut]:
    return crud.list_empreendimentos(
        db,
        skip=skip,
        limit=limit,
        municipio_sc=municipio_sc,
        segmento_atuacao=segmento_atuacao,
        status_ativo=status_ativo,
    )


@app.get(
    "/empreendimentos/{empreendimento_id}", 
    response_model=schemas.EmpreendimentoOut,
    tags=["Empreendimentos"],
    summary="Obter detalhes de um empreendimento",
    description="Busca um empreendimento específico pelo seu ID único.",
)
def obter_empreendimento(
    empreendimento_id: int,
    db: Session = Depends(get_db),
) -> schemas.EmpreendimentoOut:
    obj = crud.get_empreendimento(db, empreendimento_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Empreendimento não encontrado")
    return obj


@app.put(
    "/empreendimentos/{empreendimento_id}", 
    response_model=schemas.EmpreendimentoOut,
    tags=["Empreendimentos"],
    summary="Atualizar um empreendimento",
    description="Atualiza os dados de um empreendimento existente. Apenas os campos enviados no JSON serão alterados.",
)
def atualizar_empreendimento(
    empreendimento_id: int,
    payload: schemas.EmpreendimentoUpdate,
    db: Session = Depends(get_db),
) -> schemas.EmpreendimentoOut:
    obj = crud.update_empreendimento(db, empreendimento_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Empreendimento não encontrado")
    return obj


@app.delete(
    "/empreendimentos/{empreendimento_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Empreendimentos"],
    summary="Remover um empreendimento",
    description="Exclui permanentemente um empreendimento do banco de dados.",
)
def remover_empreendimento(
    empreendimento_id: int,
    db: Session = Depends(get_db),
) -> Response:
    ok = crud.delete_empreendimento(db, empreendimento_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Empreendimento não encontrado")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

