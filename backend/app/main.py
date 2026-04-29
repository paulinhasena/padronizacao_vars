from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

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


# ----------------------------------------------------------------------
# CRIAÇÃO DA API
# ----------------------------------------------------------------------
# FastAPI é o framework Python usado para criar o backend.
# O backend é a parte que recebe os dados, aplica regras e devolve resultado.
#
# O projeto funciona em dois modos:
#
# 1. Desenvolvimento:
#    - frontend separado com npm run dev;
#    - backend separado com uvicorn;
#    - usado por quem desenvolve a tela.
#
# 2. Corporativo / usuário final:
#    - frontend já compilado em frontend/dist;
#    - backend Python serve a tela pronta;
#    - não precisa Node/npm na máquina da pessoa usuária.
app = FastAPI(
    title=settings.app_name,
    description="API para padronização de nomes lógicos e físicos com regras de dados e IA generativa.",
    version="0.1.0",
)


# ----------------------------------------------------------------------
# CORS
# ----------------------------------------------------------------------
# CORS permite que a tela React chame o backend.
#
# Quando o frontend roda em modo desenvolvimento, ele costuma abrir em:
# http://localhost:5173
#
# O backend abre em:
# http://localhost:8000
#
# Como são portas diferentes, precisamos liberar essa comunicação.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict:
    """Valida se o backend está ativo.

    Se acessar /health e retornar status ok, significa que a API subiu.
    """
    return {"status": "ok", "app": settings.app_name}


@app.post("/normalize", response_model=NormalizeResponse)
async def normalize(request: NormalizeRequest) -> NormalizeResponse:
    """Normaliza variáveis recebidas via JSON.

    Este endpoint é mais técnico.
    Ele permite que no futuro outro sistema chame esta API diretamente.
    """
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
    """Normaliza variáveis coladas na tela.

    Exemplo de entrada:
        codigo identificacao pessoa | Formato criptografado do id do cliente.

    O parser separa:
    - nome da variável;
    - descrição, quando existir.
    """
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
    """Normaliza variáveis a partir de CSV ou Excel.

    A tela envia o arquivo para este endpoint.
    O backend lê o arquivo, transforma cada linha em variável
    e aplica a mesma regra usada no texto colado.
    """
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
    """Mostra um resumo do dicionário CSV carregado.

    Isso ajuda no diagnóstico.
    Se esse endpoint retornar quantidade de termos, o backend achou o CSV.
    """
    from app.services.naming_rules import load_dictionary

    df = load_dictionary()
    return {
        "terms": int(len(df)),
        "columns": list(df.columns),
        "source": "local_csv",
    }


def build_response(results: list[NormalizedVariable], output_format: OutputFormat) -> NormalizeResponse:
    """Monta a resposta no formato escolhido pela pessoa usuária.

    A pessoa pode escolher:
    - tabela;
    - terraform.tfvars;
    - NoScript/NoCode;
    - tudo junto.
    """
    response = NormalizeResponse(results=results)

    if output_format in [OutputFormat.table, OutputFormat.all]:
        response.table = to_table(results)

    if output_format in [OutputFormat.tfvars, OutputFormat.all]:
        response.tfvars = to_tfvars(results)

    if output_format in [OutputFormat.noscript, OutputFormat.all]:
        response.noscript = to_noscript(results)

    return response


# ----------------------------------------------------------------------
# FRONTEND COMPILADO
# ----------------------------------------------------------------------
# Esta parte é o que permite manter o front bonito SEM Node/npm no corporativo.
#
# A pasta frontend/dist é gerada na máquina pessoal com:
#
#   GERAR_FRONTEND_PESSOAL.bat
#
# Depois essa pasta vai para o repositório.
# No corporativo, o FastAPI serve esses arquivos como se fosse um site.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIST = PROJECT_ROOT / "frontend" / "dist"

if FRONTEND_DIST.exists():
    assets_path = FRONTEND_DIST / "assets"

    # A pasta assets guarda JavaScript, CSS e outros arquivos gerados pelo React/Vite.
    if assets_path.exists():
        app.mount(
            "/assets",
            StaticFiles(directory=assets_path),
            name="assets",
        )

    @app.get("/")
    def serve_frontend_index():
        """Abre a interface principal em http://localhost:8000."""
        return FileResponse(FRONTEND_DIST / "index.html")

    @app.get("/{full_path:path}")
    def serve_frontend_routes(full_path: str):
        """Serve arquivos do frontend ou devolve index.html.

        Isso é útil para aplicações React, porque algumas rotas são controladas
        pelo próprio frontend.
        """
        requested_file = FRONTEND_DIST / full_path

        if requested_file.exists() and requested_file.is_file():
            return FileResponse(requested_file)

        return FileResponse(FRONTEND_DIST / "index.html")
