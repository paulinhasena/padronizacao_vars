from app.models.schemas import NormalizedVariable


def to_table(results: list[NormalizedVariable]) -> list[dict]:
    """Converte os resultados para tabela.

    O frontend usa esse formato para montar a grade visual.
    """
    return [item.model_dump() for item in results]


def to_tfvars(results: list[NormalizedVariable]) -> str:
    """Gera saída no formato terraform.tfvars.

    Esse formato pode ser útil em fluxos declarativos ou parametrizados.
    """
    lines = ["variables = {"]

    for item in results:
        lines.append(f'  "{item.physical_name}" = {{')
        lines.append(f'    logical_name  = "{escape(item.logical_name)}"')
        lines.append(f'    physical_name = "{escape(item.physical_name)}"')
        lines.append(f'    description   = "{escape(item.description)}"')
        lines.append(f'    nature        = "{escape(item.nature)}"')
        lines.append(f'    qualifiers    = {format_list(item.qualifiers)}')
        lines.append(f'    confidence    = {item.confidence}')
        lines.append("  }")

    lines.append("}")
    return "\n".join(lines)


def to_noscript(results: list[NormalizedVariable]) -> str:
    """Gera saída textual para NoScript/NoCode.

    Este formato é mais simples de copiar e colar em outros fluxos.
    """
    lines = []

    for item in results:
        lines.append(f"CAMPO: {item.physical_name}")
        lines.append(f"NOME_LOGICO: {item.logical_name}")
        lines.append(f"DESCRICAO: {item.description}")
        lines.append(f"NATUREZA: {item.nature}")
        lines.append(f"QUALIFICADORES: {', '.join(item.qualifiers) if item.qualifiers else 'NAO_INFERIDO'}")
        lines.append(f"CONFIANCA: {item.confidence}")
        lines.append("---")

    return "\n".join(lines)


def escape(value: str) -> str:
    """Escapa aspas para não quebrar o texto gerado."""
    return value.replace('"', '\\"')


def format_list(values: list[str]) -> str:
    """Formata lista em sintaxe parecida com tfvars."""
    if not values:
        return "[]"

    return "[" + ", ".join(f'"{escape(value)}"' for value in values) + "]"
