from __future__ import annotations

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class Empreendimento(Base):
    __tablename__ = "empreendimentos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome_empreendimento: Mapped[str] = mapped_column(String(120), nullable=False)
    nome_empreendedor: Mapped[str] = mapped_column(String(120), nullable=False)
    municipio_sc: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    segmento_atuacao: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    contato: Mapped[str] = mapped_column(String(160), nullable=False)
    status_ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    descricao: Mapped[str | None] = mapped_column(String(500), nullable=True)

