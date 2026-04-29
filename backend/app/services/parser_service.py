from io import BytesIO

import pandas as pd

from app.models.schemas import VariableInput


def parse_text_input(text: str) -> list[VariableInput]:
    """Transforma texto colado na tela em lista de variáveis.

    Aceita formatos simples:
        nome
        nome | descrição
        nome ; descrição
        nome, descrição

    Exemplo:
        codigo identificacao pessoa | id criptografado do cliente
    """
    variables: list[VariableInput] = []

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        separator = detect_separator(line)

        if separator:
            raw_name, description = line.split(separator, 1)
        else:
            raw_name, description = line, None

        variables.append(
            VariableInput(
                raw_name=raw_name.strip(),
                description=description.strip() if description else None,
            )
        )

    return variables


def detect_separator(line: str) -> str | None:
    """Detecta qual separador foi usado entre nome e descrição."""
    for sep in ["|", ";", ","]:
        if sep in line:
            return sep
    return None


def parse_file(content: bytes, filename: str) -> list[VariableInput]:
    """Lê CSV ou Excel e transforma linhas em variáveis.

    A função tenta identificar automaticamente a coluna principal.

    Nomes aceitos para coluna de variável:
    - nome_logico
    - nome lógico
    - nome
    - variavel
    - variável
    - campo
    - raw_name

    Nomes aceitos para descrição:
    - descricao
    - descrição
    - description
    """
    file_bytes = BytesIO(content)
    filename = filename.lower()

    if filename.endswith(".csv"):
        df = pd.read_csv(file_bytes, sep=None, engine="python")
    elif filename.endswith((".xlsx", ".xls")):
        df = pd.read_excel(file_bytes)
    else:
        raise ValueError("Formato não suportado. Envie CSV, XLSX ou XLS.")

    if df.empty:
        return []

    columns = {str(col).lower().strip(): col for col in df.columns}

    name_column = (
        columns.get("nome_logico")
        or columns.get("nome lógico")
        or columns.get("nome")
        or columns.get("variavel")
        or columns.get("variável")
        or columns.get("campo")
        or columns.get("raw_name")
        or df.columns[0]
    )

    description_column = (
        columns.get("descricao")
        or columns.get("descrição")
        or columns.get("description")
    )

    variables: list[VariableInput] = []

    for _, row in df.iterrows():
        raw_name = str(row[name_column]).strip()

        if not raw_name or raw_name.lower() == "nan":
            continue

        description = None
        if description_column and pd.notna(row[description_column]):
            description = str(row[description_column]).strip()

        variables.append(VariableInput(raw_name=raw_name, description=description))

    return variables
