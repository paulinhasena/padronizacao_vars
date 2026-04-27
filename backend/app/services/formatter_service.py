from app.models.schemas import NormalizedVariable


def to_table(results: list[NormalizedVariable]) -> list[dict]:
    """Prepara tabela para exibição no frontend."""
    return [item.model_dump() for item in results]


def to_tfvars(results: list[NormalizedVariable]) -> str:
    """Gera formato terraform.tfvars."""
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
    """Gera formato textual genérico para NoScript/NoCode."""
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
    """Escapa aspas para evitar quebra em texto gerado."""
    return value.replace('"', '\\"')


def format_list(values: list[str]) -> str:
    """Formata lista em sintaxe compatível com tfvars."""
    if not values:
        return "[]"

    return "[" + ", ".join(f'"{escape(value)}"' for value in values) + "]"
