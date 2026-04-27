import re
import unicodedata
from pathlib import Path

import pandas as pd


DICTIONARY_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_dictionary.csv"


def remove_accents(value: str) -> str:
    """Remove acentos para comparação robusta entre termos."""
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(char for char in normalized if not unicodedata.combining(char))


def clean_text(value: str) -> str:
    """Normaliza texto para comparação e geração de nomes físicos."""
    value = remove_accents(value.lower().strip())
    value = re.sub(r"[^a-z0-9\s_/-]", " ", value)
    value = re.sub(r"[\s_/-]+", " ", value)
    return value.strip()


def load_dictionary() -> pd.DataFrame:
    """Carrega dicionário de termos.

    Em produção, esse ponto pode ser trocado por uma tabela governada,
    API interna ou catálogo corporativo.
    """
    return pd.read_csv(DICTIONARY_PATH, sep=";")


def build_term_map() -> dict[str, dict]:
    """Cria mapa de consulta termo -> metadados."""
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
    """Gera sugestão de nome lógico/físico com regras + dicionário.

    A estratégia é híbrida:
    1. tenta casar termos compostos do dicionário;
    2. tenta casar palavras individuais;
    3. usa fallback controlado para termos não mapeados;
    4. calcula confiança baseada na cobertura do dicionário.
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

    # Termos compostos primeiro: "identificacao pessoa", "data nascimento", etc.
    for term, meta in sorted(term_map.items(), key=lambda item: len(item[0]), reverse=True):
        if term and term in remaining_text:
            physical_parts.append(meta["physical"])
            logical_parts.append(meta["logical"])
            qualifiers.append(meta["qualifier"])
            natures.append(meta["nature"])
            matched_words += len(term.split())
            remaining_text = re.sub(rf"\b{re.escape(term)}\b", " ", remaining_text)

    # Palavras restantes.
    for word in remaining_text.split():
        if word in term_map:
            meta = term_map[word]
            physical_parts.append(meta["physical"])
            logical_parts.append(meta["logical"])
            qualifiers.append(meta["qualifier"])
            natures.append(meta["nature"])
            matched_words += 1
        else:
            physical_parts.append(word[:8])
            logical_parts.append(word)

    physical_name = "_".join(part for part in physical_parts if part)
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
    """Retorna o valor mais frequente de uma lista."""
    if not values:
        return None

    return max(set(values), key=values.count)


def build_explanation(confidence: float) -> str:
    """Explica o score em linguagem simples."""
    if confidence >= 0.8:
        return "Alta aderência ao dicionário de termos e às regras de nomenclatura."
    if confidence >= 0.5:
        return "Aderência parcial. Recomenda-se revisão funcional antes de uso produtivo."
    return "Baixa aderência. Termos não encontrados integralmente no dicionário base."
