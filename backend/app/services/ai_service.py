from app.models.schemas import VariableInput
from app.services.naming_rules import infer_standard_name


async def normalize_variable(variable: VariableInput, use_ai: bool = False) -> dict:
    """Normaliza uma variável.

    Esta função existe para centralizar o fluxo de padronização.

    Hoje:
    - chama o motor de regras;
    - consulta o dicionário CSV;
    - devolve nome lógico, nome físico, descrição e confiança.

    Futuro:
    - pode chamar uma IA generativa;
    - pode chamar algoritmo de similaridade;
    - pode tratar abreviações livres.

    Exemplo de caso futuro:
        dtda = data admissão colaborador

    A IA/similaridade ajudaria a interpretar "dtda".
    Mas a resposta final ainda precisa respeitar o glossário oficial.
    """

    # Primeiro sempre usamos regra determinística.
    # Isso reduz risco de a IA inventar mnemônico.
    base_result = infer_standard_name(
        raw_name=variable.raw_name,
        description=variable.description,
    )

    if use_ai:
        # Ainda não chamamos IA externa nesta versão.
        # Esta marcação mostra que a arquitetura está preparada para evolução.
        base_result["explanation"] = (
            base_result["explanation"]
            + " Camada preparada para refinamento por IA generativa autorizada."
        )

    return base_result
