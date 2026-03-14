from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class SegmentoAtuacao(str, Enum):
    tecnologia = "Tecnologia"
    comercio = "Comércio"
    industria = "Indústria"
    servicos = "Serviços"
    agronegocio = "Agronegócio"


class EmpreendimentoBase(BaseModel):
    nome_empreendimento: str = Field(min_length=2, max_length=120)
    nome_empreendedor: str = Field(min_length=2, max_length=120)
    municipio_sc: str = Field(min_length=2, max_length=120, description="Município em Santa Catarina")
    segmento_atuacao: SegmentoAtuacao
    contato: str = Field(
        min_length=3,
        max_length=160,
        description="E-mail ou outro meio de contato",
        examples=["contato@empresa.com", "(48) 99999-9999", "@empresa_no_instagram"],
    )
    status_ativo: bool = True
    descricao: str | None = Field(default=None, max_length=500)


class EmpreendimentoCreate(EmpreendimentoBase):
    pass


class EmpreendimentoUpdate(BaseModel):
    nome_empreendimento: str | None = Field(default=None, min_length=2, max_length=120)
    nome_empreendedor: str | None = Field(default=None, min_length=2, max_length=120)
    municipio_sc: str | None = Field(default=None, min_length=2, max_length=120)
    segmento_atuacao: SegmentoAtuacao | None = None
    contato: str | None = Field(default=None, min_length=3, max_length=160)
    status_ativo: bool | None = None
    descricao: str | None = Field(default=None, max_length=500)


class EmpreendimentoOut(EmpreendimentoBase):
    id: int

    class Config:
        from_attributes = True

