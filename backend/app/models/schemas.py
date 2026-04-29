from enum import Enum
from pydantic import BaseModel, Field


class OutputFormat(str, Enum):
    """Formatos de saída aceitos pela API."""

    table = "table"
    tfvars = "tfvars"
    noscript = "noscript"
    all = "all"


class VariableInput(BaseModel):
    """Representa uma variável de entrada."""

    raw_name: str = Field(..., description="Nome original informado pelo usuário")
    description: str | None = Field(None, description="Descrição funcional/técnica opcional")


class NormalizeRequest(BaseModel):
    """Contrato para normalização via JSON."""

    variables: list[VariableInput]
    output_format: OutputFormat = OutputFormat.all
    use_ai: bool = False


class NormalizedVariable(BaseModel):
    """Resultado padronizado de uma variável."""

    original_name: str
    logical_name: str
    physical_name: str
    description: str
    confidence: float
    nature: str
    qualifiers: list[str]
    explanation: str


class NormalizeResponse(BaseModel):
    """Resposta consolidada da API."""

    results: list[NormalizedVariable]
    table: list[dict] | None = None
    tfvars: str | None = None
    noscript: str | None = None
