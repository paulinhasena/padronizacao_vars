from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.models.schemas import (
    NormalizedVariable,
    NormalizeRequest,
    NormalizeResponse,
    OutputFormat,
)
from app.services.ai_service import normalize_variable
from app.services.formatter_service import to_noscript, to_table, to_tfvars
from app.services.parser_service import parse_file, parse_text_input


app = FastAPI(
    title=settings.app_name,
    description="API para padronização de nomes lógicos e físicos com regras de dados e IA generativa.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict:
    """Valida se a API está funcionando."""
    return {"status": "ok", "app": settings.app_name}


@app.post("/normalize", response_model=NormalizeResponse)
async def normalize(request: NormalizeRequest) -> NormalizeResponse:
    """Normaliza variáveis recebidas via JSON."""
    results = [
        NormalizedVariable(**await normalize_variable(variable, request.use_ai))
        for variable in request.variables
    ]

    return build_response(results, request.output_format)


@app.post("/normalize/text", response_model=NormalizeResponse)
async def normalize_text(
    text: str = Form(...),
    output_format: OutputFormat = Form(OutputFormat.all),
    use_ai: bool = Form(False),
) -> NormalizeResponse:
    """Normaliza variáveis a partir de texto colado."""
    variables = parse_text_input(text)

    if not variables:
        raise HTTPException(status_code=400, detail="Nenhuma variável válida encontrada no texto.")

    results = [
        NormalizedVariable(**await normalize_variable(variable, use_ai))
        for variable in variables
    ]

    return build_response(results, output_format)


@app.post("/normalize/file", response_model=NormalizeResponse)
async def normalize_file(
    file: UploadFile = File(...),
    output_format: OutputFormat = Form(OutputFormat.all),
    use_ai: bool = Form(False),
) -> NormalizeResponse:
    """Normaliza variáveis a partir de arquivo CSV/Excel."""
    content = await file.read()

    try:
        variables = parse_file(content, file.filename or "")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if not variables:
        raise HTTPException(status_code=400, detail="Arquivo sem variáveis válidas.")

    results = [
        NormalizedVariable(**await normalize_variable(variable, use_ai))
        for variable in variables
    ]

    return build_response(results, output_format)


@app.get("/dictionary/summary")
def dictionary_summary() -> dict:
    """Retorna resumo simples do dicionário carregado."""
    from app.services.naming_rules import load_dictionary

    df = load_dictionary()
    return {
        "terms": int(len(df)),
        "columns": list(df.columns),
        "source": "local_csv",
    }


def build_response(results: list[NormalizedVariable], output_format: OutputFormat) -> NormalizeResponse:
    """Monta resposta conforme o formato solicitado."""
    response = NormalizeResponse(results=results)

    if output_format in [OutputFormat.table, OutputFormat.all]:
        response.table = to_table(results)

    if output_format in [OutputFormat.tfvars, OutputFormat.all]:
        response.tfvars = to_tfvars(results)

    if output_format in [OutputFormat.noscript, OutputFormat.all]:
        response.noscript = to_noscript(results)

    return response
