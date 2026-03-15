from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas


def create_empreendimento(db: Session, payload: schemas.EmpreendimentoCreate) -> models.Empreendimento:
    print(f"-> [CRUD] Criando empreendimento: {payload.nome_empreendimento}")
    obj = models.Empreendimento(
        nome_empreendimento=payload.nome_empreendimento,
        nome_empreendedor=payload.nome_empreendedor,
        municipio_sc=payload.municipio_sc,
        segmento_atuacao=payload.segmento_atuacao.value,
        contato=payload.contato,
        status_ativo=payload.status_ativo,
        descricao=payload.descricao,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_empreendimento(db: Session, empreendimento_id: int) -> models.Empreendimento | None:
    return db.get(models.Empreendimento, empreendimento_id)


def list_empreendimentos(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 50,
    municipio_sc: str | None = None,
    segmento_atuacao: schemas.SegmentoAtuacao | None = None,
    status_ativo: bool | None = None,
) -> list[models.Empreendimento]:
    stmt = select(models.Empreendimento)

    if municipio_sc:
        stmt = stmt.where(models.Empreendimento.municipio_sc.ilike(f"%{municipio_sc}%"))

    if segmento_atuacao:
        stmt = stmt.where(models.Empreendimento.segmento_atuacao == segmento_atuacao.value)

    if status_ativo is not None:
        stmt = stmt.where(models.Empreendimento.status_ativo == status_ativo)

    stmt = stmt.order_by(models.Empreendimento.id.desc()).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def update_empreendimento(
    db: Session,
    empreendimento_id: int,
    payload: schemas.EmpreendimentoUpdate,
) -> models.Empreendimento | None:
    obj = get_empreendimento(db, empreendimento_id)
    if not obj:
        print(f"!! [CRUD] Falha ao atualizar: ID {empreendimento_id} não encontrado")
        return None

    print(f"-> [CRUD] Atualizando empreendimento: {obj.nome_empreendimento} (ID: {empreendimento_id})")
    data = payload.model_dump(exclude_unset=True)
    if "segmento_atuacao" in data and data["segmento_atuacao"] is not None:
        data["segmento_atuacao"] = data["segmento_atuacao"].value

    for key, value in data.items():
        setattr(obj, key, value)

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def delete_empreendimento(db: Session, empreendimento_id: int) -> bool:
    obj = get_empreendimento(db, empreendimento_id)
    if not obj:
        print(f"!! [CRUD] Falha ao remover: ID {empreendimento_id} não encontrado")
        return False
    
    print(f"-> [CRUD] Removendo empreendimento: {obj.nome_empreendimento}")
    db.delete(obj)
    db.commit()
    return True

