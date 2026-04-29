# Padronizador de Variáveis — MVP Local

MVP local para padronização de nomes de variáveis usando dicionário de termos, regras de nomenclatura e uma camada preparada para IA/similaridade.

## 1. Objetivo

A ideia é reduzir esforço manual na consulta de termos e mnemônicos, melhorar consistência de nomes e oferecer uma experiência simples para pessoas que precisam padronizar variáveis.

O sistema permite:

- colar variáveis na tela;
- enviar CSV ou Excel;
- retornar nome lógico;
- retornar nome físico;
- gerar descrição;
- indicar confiança;
- gerar saída em tabela;
- gerar saída em `terraform.tfvars`;
- gerar saída em formato NoScript/NoCode.

## 2. Como usar — modo mais simples

Use o arquivo:

```text
INICIAR_PADRONIZADOR.bat
```

Esse modo:

- não usa Node;
- não usa npm;
- não usa Vite;
- não precisa de `node_modules`;
- usa o frontend pronto em `frontend/dist`;
- sobe o backend Python;
- abre o navegador automaticamente.

### Requisito único

A máquina precisa ter:

```text
Python
```

### Passo a passo

1. Baixe o projeto.
2. Extraia a pasta.
3. Clique duas vezes em `INICIAR_PADRONIZADOR.bat`.
4. Use no navegador.

A aplicação abre em:

```text
http://localhost:8000
```

## 3. Como gerar o frontend bonito

A interface bonita é gerada uma vez em uma máquina que tenha Node/npm liberado.

Rode:

```text
GERAR_FRONTEND_PESSOAL.bat
```

Esse script cria:

```text
frontend/dist
```

Depois suba essa pasta no repositório.

No computador corporativo, a pessoa usuária não precisa de Node/npm.

## 4. Arquitetura

```text
Usuário
  ↓
Frontend React já compilado
  ↓
Backend Python/FastAPI
  ↓
Dicionário CSV + regras
  ↓
Resposta estruturada
```

## 5. Estrutura do projeto

```text
backend/                         -> backend Python/FastAPI
frontend/                        -> frontend React
frontend/dist/                   -> frontend já compilado
docs/                            -> documentação complementar
exemplos/                        -> arquivos de exemplo
INICIAR_PADRONIZADOR.bat         -> script principal para usuário final
GERAR_FRONTEND_PESSOAL.bat       -> gera frontend/dist na máquina pessoal
LEIA_ME_PRIMEIRO.txt             -> instrução rápida para usuário
GUIA_DESENVOLVEDORA.md           -> explicação técnica para manutenção
README.md                        -> documentação principal
```

## 6. O que ficou em português e o que ficou em inglês

Ficou em português:

- scripts `.bat`;
- documentação;
- textos de orientação;
- comentários explicativos.

Foi mantido em inglês quando é padrão técnico:

- `backend`;
- `frontend`;
- `requirements.txt`;
- `package.json`;
- `src`;
- `components`;
- `App.jsx`;
- `api.js`.

Isso evita quebrar ferramentas e mantém padrão de mercado.

## 7. Exemplo de uso

Entrada:

```text
codigo identificacao pessoa | Formato criptografado do id do cliente.
data nascimento cliente | Data de nascimento do cliente.
valor contrato credito | Valor total do contrato.
```

Saída esperada:

- nome original;
- nome lógico;
- nome físico;
- descrição;
- confiança;
- justificativa.

## 8. Sobre o dicionário

O dicionário fica em:

```text
backend/app/data/sample_dictionary.csv
```

Formato esperado:

```text
termo;nome_logico_padrao;abreviacao_fisica;natureza;qualificador
```

Exemplo:

```text
codigo;Código;cod;IDENTIFICADOR;TECNICO
identificacao;Identificação;idef;IDENTIFICADOR;TECNICO
pessoa;Pessoa;pess;ENTIDADE;NEGOCIO
```

## 9. Evolução com IA/similaridade

Nem sempre a entrada do usuário vem no padrão.

Exemplo:

```text
dtda = data admissão colaborador
```

Nesse caso, regra pura pode não ser suficiente.

A camada de IA/similaridade deve ajudar a interpretar a intenção, mas sem inventar mnemônicos fora do glossário.

Regra de ouro:

```text
IA sugere, glossário valida.
```

## 10. Como apresentar

Sugestão de fala:

> Construí um MVP local para validar uma solução de padronização de variáveis. A ideia é reduzir esforço manual na consulta de termos e mnemônicos, melhorar consistência e oferecer uma experiência simples para uso. Para evitar dependência de Node no ambiente corporativo, o frontend é gerado previamente e servido pelo backend Python. A arquitetura separa frontend, backend, dicionário e uma camada preparada para IA/similaridade.

## 11. Troubleshooting

### Frontend não abre

Verifique se existe:

```text
frontend/dist/index.html
```

Se não existir, rode na máquina pessoal:

```text
GERAR_FRONTEND_PESSOAL.bat
```

### Python não encontrado

Instale ou solicite Python conforme padrão da máquina.

### pip install bloqueado

Possíveis soluções futuras:

- pacote com `.venv` pronto;
- `.exe` com PyInstaller;
- uso de repositório interno de pacotes.

## 12. Próximos passos

- adicionar conversão bidirecional;
- trocar dicionário exemplo pelo glossário real;
- melhorar score de confiança;
- adicionar IA/similaridade para casos fora do padrão;
- validar com usuários piloto.
