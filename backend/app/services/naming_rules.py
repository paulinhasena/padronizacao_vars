import re
import unicodedata
from pathlib import Path

import pandas as pd


# Caminho do dicionário usado pelo MVP.
# Este arquivo é a "fonte de verdade" para o motor de padronização.
DICTIONARY_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_dictionary.csv"


def remove_accents(value: str) -> str:
    """Remove acentos de um texto.

    Exemplo:
        "identificação" -> "identificacao"

    Por que isso é importante?
    Porque a pessoa pode digitar com acento, sem acento, maiúsculo ou minúsculo.
    Para comparar corretamente com o dicionário, normalizamos o texto.
    """
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(char for char in normalized if not unicodedata.combining(char))


def clean_text(value: str) -> str:
    """Padroniza o texto para comparação.

    Esta função:
    - coloca em minúsculo;
    - remove acentos;
    - remove caracteres especiais;
    - transforma hífen, underline e barra em espaço;
    - remove espaços duplicados.

    Exemplo:
        "Código-Identificação_Pessoa" -> "codigo identificacao pessoa"
    """
    value = remove_accents(value.lower().strip())
    value = re.sub(r"[^a-z0-9\s_/-]", " ", value)
    value = re.sub(r"[\s_/-]+", " ", value)
    return value.strip()


def load_dictionary() -> pd.DataFrame:
    """Carrega o dicionário CSV.

    Formato esperado:
        termo;nome_logico_padrao;abreviacao_fisica;natureza;qualificador

    Exemplo:
        codigo;Código;cod;IDENTIFICADOR;TECNICO

    Em uma evolução futura, este CSV pode ser substituído por:
    - glossário oficial;
    - tabela governada;
    - API interna;
    - base exportada do catálogo corporativo.
    """
    return pd.read_csv(DICTIONARY_PATH, sep=";")


def build_term_map() -> dict[str, dict]:
    """Cria um dicionário Python para consulta rápida.

    O CSV é uma tabela.
    Para buscar rápido, transformamos a tabela em um mapa.

    Exemplo:
        "codigo" -> {
            "physical": "cod",
            "logical": "Código",
            "nature": "IDENTIFICADOR",
            "qualifier": "TECNICO"
        }

    Isso facilita gerar o nome físico e o nome lógico.
    """
    df = load_dictionary()
    term_map: dict[str, dict] = {}

    for _, row in df.iterrows():
        term = clean_text(str(row["termo"]))
        term_map[term] = {
            "physical": str(row["abreviacao_fisica"]).strip(),
            "logical": str(row["nome_logico_padrao"]).strip(),
            "nature": str(row["natureza"]).strip(),
            "qualifier": str(row["qualificador"]).strip(),
        }

    return term_map


def infer_standard_name(raw_name: str, description: str | None = None) -> dict:
    """Gera uma sugestão padronizada para uma variável.

    Entrada exemplo:
        codigo identificacao pessoa

    Saída física:
        cod_idef_pess

    Saída lógica:
        Código - Identificação - Pessoa

    Como funciona:
    1. limpa a entrada;
    2. procura cada termo no dicionário;
    3. junta as abreviações com underscore;
    4. junta os nomes lógicos com separador;
    5. calcula confiança conforme termos encontrados.

    Importante:
    A versão atual funciona melhor para "termo por extenso -> nome físico".
    A próxima evolução é suportar também "nome físico -> termo por extenso".
    """
    term_map = build_term_map()
    normalized = clean_text(raw_name)
    words = normalized.split()

    physical_parts: list[str] = []
    logical_parts: list[str] = []
    qualifiers: list[str] = []
    natures: list[str] = []
    matched_words = 0
    remaining_text = normalized

    # Primeiro tentamos casar termos compostos.
    # Exemplo futuro: "data admissao" pode ser um termo composto.
    for term, meta in sorted(term_map.items(), key=lambda item: len(item[0]), reverse=True):
        if term and term in remaining_text:
            physical_parts.append(meta["physical"])
            logical_parts.append(meta["logical"])
            qualifiers.append(meta["qualifier"])
            natures.append(meta["nature"])
            matched_words += len(term.split())
            remaining_text = re.sub(rf"\b{re.escape(term)}\b", " ", remaining_text)

    # Depois tratamos palavra por palavra.
    for word in remaining_text.split():
        if word in term_map:
            meta = term_map[word]
            physical_parts.append(meta["physical"])
            logical_parts.append(meta["logical"])
            qualifiers.append(meta["qualifier"])
            natures.append(meta["nature"])
            matched_words += 1
        else:
            # Hoje mantemos um fallback simples para não quebrar o fluxo.
            # Em uma versão mais madura, este ponto deve marcar "revisão necessária"
            # ou chamar uma camada de IA/similaridade.
            physical_parts.append(word[:8])
            logical_parts.append(word)

    physical_name = "_".join(part.lower() for part in physical_parts if part)
    physical_name = re.sub(r"_+", "_", physical_name).strip("_")

    logical_name = " - ".join(part for part in logical_parts if part)
    logical_name = re.sub(r"\s+", " ", logical_name).strip()

    total_words = max(len(words), 1)
    confidence = min(round(matched_words / total_words, 2), 1.0)

    return {
        "original_name": raw_name,
        "logical_name": logical_name or raw_name,
        "physical_name": physical_name or clean_text(raw_name).replace(" ", "_"),
        "description": description or f"Campo derivado de: {raw_name}",
        "confidence": confidence,
        "nature": most_common(natures) or "NAO_INFERIDA",
        "qualifiers": sorted(set(q for q in qualifiers if q and q.lower() != "nan")),
        "explanation": build_explanation(confidence),
    }


def most_common(values: list[str]) -> str | None:
    """Retorna o valor mais comum em uma lista.

    Usado para escolher uma natureza predominante quando vários termos aparecem.
    """
    if not values:
        return None

    return max(set(values), key=values.count)


def build_explanation(confidence: float) -> str:
    """Transforma o score de confiança em uma explicação simples."""
    if confidence >= 0.8:
        return "Alta aderência ao dicionário de termos e às regras de nomenclatura."
    if confidence >= 0.5:
        return "Aderência parcial. Recomenda-se revisão funcional antes de uso produtivo."
    return "Baixa aderência. Termos não encontrados integralmente no dicionário base."
