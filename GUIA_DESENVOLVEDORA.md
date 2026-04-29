# Guia da Desenvolvedora — Padronizador de Variáveis

Este documento explica o projeto em linguagem simples, para você conseguir entender, manter e apresentar.

## 1. Visão geral

O projeto tem duas partes principais:

```text
frontend/  -> tela bonita em React
backend/   -> API em Python/FastAPI com as regras
```

No modo corporativo, a pessoa usuária não precisa rodar Node/npm.  
O frontend é gerado antes, na pasta:

```text
frontend/dist
```

Depois o backend Python abre a interface no navegador.

## 2. Fluxo do sistema

```text
Usuário cola variáveis ou envia arquivo
        ↓
Frontend envia para o backend
        ↓
Backend lê entrada
        ↓
Backend consulta o dicionário CSV
        ↓
Backend aplica regras
        ↓
Backend devolve resultado estruturado
        ↓
Frontend mostra tabela / tfvars / NoScript
```

## 3. Arquivos mais importantes

### Backend

```text
backend/app/main.py
```

É o coração da API. Define as rotas como:

- `/normalize/text`
- `/normalize/file`
- `/dictionary/summary`

```text
backend/app/services/naming_rules.py
```

Contém a regra de padronização.  
É onde o sistema transforma:

```text
codigo identificacao pessoa
```

em:

```text
cod_idef_pess
```

```text
backend/app/services/parser_service.py
```

Lê texto, CSV e Excel.

```text
backend/app/services/formatter_service.py
```

Monta os formatos de saída:

- tabela
- terraform.tfvars
- NoScript/NoCode

```text
backend/app/services/ai_service.py
```

Camada preparada para evolução com IA/similaridade.

### Frontend

```text
frontend/src/App.jsx
```

Componente principal da tela.

```text
frontend/src/api.js
```

Responsável por chamar a API Python.

```text
frontend/src/components/
```

Componentes visuais da tela.

```text
frontend/src/index.css
```

Estilo visual.

## 4. O que fica em português e o que fica em inglês

Mantivemos em português:

- documentação;
- nomes dos scripts `.bat`;
- textos de orientação;
- explicações e comentários.

Mantivemos em inglês quando é padrão técnico:

- `backend`
- `frontend`
- `requirements.txt`
- `package.json`
- `src`
- `components`
- `App.jsx`
- `api.js`
- nomes de bibliotecas/frameworks.

Isso é bom porque evita quebrar ferramentas e mantém padrão de mercado.

## 5. Como apresentar tecnicamente

Você pode explicar assim:

> Eu construí um MVP local com front em React e backend em FastAPI. Para evitar dependência de Node no ambiente corporativo, gerei uma versão compilada do front em `frontend/dist`, e o próprio backend Python serve a interface. A regra atual usa um dicionário CSV e está preparada para evoluir com IA/similaridade quando o nome informado não estiver no padrão.

## 6. Próxima evolução técnica

Adicionar conversão bidirecional:

```text
codigo-identificacao-pessoa -> cod_idef_pess
cod_idef_pess -> codigo-identificacao-pessoa
```

Adicionar inteligência para casos como:

```text
dtda = data admissão colaborador
```

A IA/similaridade deve sugerir interpretação, mas o glossário oficial deve validar.
