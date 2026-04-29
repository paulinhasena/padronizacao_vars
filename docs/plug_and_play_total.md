# Plug-and-play total

## Objetivo

Facilitar o uso local da ferramenta por pessoas que não são desenvolvedoras.

## Modo atual recomendado

Arquivo principal:

```text
INICIAR_DATA_NAMING_AI.bat
```

Ele faz:

1. valida se `frontend/dist` existe;
2. valida se Python existe;
3. cria `.venv` se necessário;
4. instala dependências Python;
5. inicia FastAPI;
6. abre navegador em `http://localhost:8000`.

## O que o usuário precisa ter?

Apenas:

```text
Python
```

Não precisa:

```text
Node
npm
npm install
npm run dev
node_modules
Vite
```

## O que mantém o front bonito?

A pasta:

```text
frontend/dist
```

Ela é o frontend React já compilado.

## Se o pip install for bloqueado

Aí existem duas alternativas:

### Alternativa 1 — pacote com `.venv` pronto

Gerar o `.venv` em uma máquina Windows compatível e entregar junto no pacote.

Ponto de atenção:
- `.venv` pode não ser 100% portátil entre máquinas diferentes.
- É melhor quando as máquinas usam mesma versão de Windows e Python.

### Alternativa 2 — gerar `.exe`

Usar PyInstaller em uma máquina Windows para empacotar o backend Python.

Ponto de atenção:
- O `.exe` precisa ser gerado em Windows.
- Pode precisar passar por validação de segurança corporativa.
