from app.models.schemas import VariableInput
from app.services.naming_rules import infer_standard_name


async def normalize_variable(variable: VariableInput, use_ai: bool = False) -> dict:
    """Normaliza uma variável usando motor híbrido.

    MVP atual:
    - regra determinística
    - dicionário de termos
    - saída estruturada

    Evolução:
    - conectar LLM autorizada;
    - passar o resultado do motor de regras como contexto;
    - exigir JSON estrito;
    - validar retorno com Pydantic;
    - manter rastreabilidade da decisão.
    """
    base_result = infer_standard_name(
        raw_name=variable.raw_name,
        description=variable.description,
    )

    if use_ai:
        # Placeholder intencional:
        # evita dependência de chave externa e mantém o MVP rodando.
        base_result["explanation"] = (
            base_result["explanation"]
            + " Camada preparada para refinamento por IA generativa autorizada."
        )

    return base_result
