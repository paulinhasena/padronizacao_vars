# Evolução — IA e Conversão Bidirecional

## Problema

Nem sempre o usuário informa um nome dentro do padrão esperado.

Exemplo:

```text
dtda
```

Pode significar:

```text
data admissão colaborador
```

Esse tipo de entrada é difícil para regra pura, porque `dtda` não necessariamente existe no glossário como termo ou mnemônico.

## Estratégia recomendada

A IA não deve inventar nomes físicos.

Ela deve atuar como camada de interpretação.

Fluxo ideal:

```text
Entrada do usuário
  ↓
Normalização básica
  ↓
Busca exata no glossário
  ↓
Busca aproximada / similaridade
  ↓
IA sugere interpretação
  ↓
Validação contra glossário
  ↓
Resposta com confiança
```

## Regras de segurança

1. Se o mnemônico não existir no glossário, não usar como definitivo.
2. Se o termo não existir, marcar como revisão necessária.
3. A IA pode sugerir, mas o glossário valida.
4. A resposta precisa mostrar confiança e justificativa.

## Exemplo esperado

Entrada:

```text
dtda
```

Resposta possível:

| Entrada | Interpretação sugerida | Nome físico | Confiança | Observação |
|---|---|---|---|---|
| dtda | data admissão colaborador | dt_adms_colab | Média | Sugestão inferida. Validar termos no glossário. |

## Próximo passo técnico

Criar uma função nova:

```python
def infer_with_similarity(raw_name: str) -> dict:
    ...
```

Essa função pode usar:

- comparação por texto;
- sinônimos;
- dicionário auxiliar de exceções;
- IA generativa aprovada;
- embeddings, em fase futura.
```
