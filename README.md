# Data Naming AI

MVP profissional para padronização de nomes lógicos e físicos usando regras de nomenclatura, dicionário de termos e camada opcional de IA generativa.

## O que esse MVP faz

Entrada:
- texto colado no front
- CSV
- Excel

Saída:
- nome original
- nome lógico padronizado
- nome físico padronizado
- descrição
- natureza
- qualificadores
- confiança
- justificativa
- tabela
- `terraform.tfvars`
- formato NoScript/NoCode
- pacote completo com todas as opções

## Arquitetura

```text
data-naming-ai/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── data/
│   │   │   └── sample_dictionary.csv
│   │   ├── models/
│   │   │   └── schemas.py
│   │   └── services/
│   │       ├── ai_service.py
│   │       ├── formatter_service.py
│   │       ├── naming_rules.py
│   │       └── parser_service.py
│   ├── .env.example
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── api.js
    │   ├── index.css
    │   ├── main.jsx
    │   └── components/
    │       ├── Header.jsx
    │       ├── InputPanel.jsx
    │       ├── ResultPanel.jsx
    │       └── ResultTable.jsx
    ├── index.html
    ├── package.json
    └── vite.config.js
```

## Como rodar o backend

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env

uvicorn app.main:app --reload --port 8000
```

Abra:

```text
http://localhost:8000/docs
```

## Como rodar o frontend

Em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

Abra:

```text
http://localhost:5173
```

## Exemplo para colar no front

```text
codigo identificacao - pessoa | Formato criptografado do id do cliente.
data nascimento cliente | Data de nascimento do cliente.
valor contrato credito | Valor total do contrato de crédito.
codigo matricula beneficio | Código da matrícula do benefício INSS.
```

## Como preparar CSV ou Excel

O arquivo pode ter colunas como:

```text
nome_logico,descricao
codigo identificacao - pessoa,Formato criptografado do id do cliente.
data nascimento cliente,Data de nascimento do cliente.
```

Também aceita colunas com nomes como:

- `nome`
- `variavel`
- `campo`
- `raw_name`
- `descricao`
- `descrição`
- `description`

## Como conectar IA depois

Hoje o MVP roda com motor determinístico para estudo e demonstração.  
A camada de IA já está isolada em:

```text
backend/app/services/ai_service.py
```

E preparada para receber uma LLM corporativa, Claude, OpenAI ou outro provedor aprovado.

Importante: não envie dados internos, sensíveis ou proprietários para IA externa sem validação de segurança/compliance.


## Versão local profissional

Esta distribuição inclui:

- `setup.bat`: instala dependências;
- `start.bat`: inicia backend, frontend e abre navegador;
- `README_USUARIO.txt`: guia simples para usuário;
- `README_TECNICO.md`: visão técnica e evolução;
- `docs/roteiro_piloto.md`: roteiro para validar com usuários.

Fluxo recomendado:

1. rode `setup.bat` uma vez;
2. depois use `start.bat`;
3. valide com poucas pessoas;
4. ajuste o dicionário;
5. só depois discuta publicação corporativa.
