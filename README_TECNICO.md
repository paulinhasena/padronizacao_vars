# Data Naming AI — README Técnico

## Propósito

MVP local para padronização de variáveis, com foco em:

- experiência simples para usuário final;
- motor baseado em dicionário estático;
- regras determinísticas auditáveis;
- arquitetura preparada para plugar IA generativa;
- validação de valor antes de qualquer custo de infraestrutura.

## Decisão arquitetural

Nesta versão, a aplicação roda localmente:

```text
Navegador → React Frontend → FastAPI Backend → CSV estático → Resultado
```

Essa decisão evita:

- custo de cloud;
- dependência de infraestrutura;
- exposição desnecessária de dados;
- necessidade de esteira corporativa antes da validação do MVP.

## Componentes

### Backend

Tecnologias:

- Python
- FastAPI
- Pydantic
- Pandas

Responsabilidades:

- receber texto ou arquivo;
- ler CSV/Excel;
- aplicar regras de padronização;
- consultar dicionário de termos;
- gerar saída estruturada.

### Frontend

Tecnologias:

- React
- Vite
- CSS puro
- lucide-react

Responsabilidades:

- interface de uso;
- upload de arquivo;
- input por texto;
- escolha de formato de saída;
- visualização de tabela e blocos estruturados.

## Fonte de verdade

O dicionário está em:

```text
backend/app/data/sample_dictionary.csv
```

Colunas:

```text
termo;nome_logico_padrao;abreviacao_fisica;natureza;qualificador
```

## Como evoluir

### Evolução 1 — Dicionário real

Substituir `sample_dictionary.csv` por uma base validada de termos.

### Evolução 2 — IA generativa

Implementar refinamento em:

```text
backend/app/services/ai_service.py
```

Estratégia recomendada:

1. aplicar regra/dicionário primeiro;
2. enviar contexto resumido para LLM aprovada;
3. exigir retorno JSON;
4. validar retorno com Pydantic;
5. exibir confiança e justificativa.

### Evolução 3 — Publicação

Somente após validação de valor:

- Copilot Studio;
- portal interno;
- container corporativo;
- API interna;
- S3/CloudFront + API Gateway/Lambda;
- outro padrão aprovado pela arquitetura.

## Como rodar manualmente

Backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Acesso:

```text
http://localhost:5173
```

## Como rodar via scripts

Primeira vez:

```text
setup.bat
```

Uso diário:

```text
start.bat
```
