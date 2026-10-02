# Boas práticas de segurança e integridade de dados (aplicadas a este RAG)

## 1. Segredos e credenciais
- **Nunca** colocar `GEMINI_API_KEY` no código ou em commits; usar variável de ambiente
  (`llm.py` já faz isso) ou Secrets do Colab. `.env` está no `.gitignore`.
- Usar chave com menor privilégio e cota limitada; rotacionar se vazar.
- Não logar a chave nem o prompt completo se houver dados sensíveis.

## 2. Prompt injection (específico de RAG)
- O conteúdo recuperado (`contexto`) é **dado não confiável**: um documento pode conter
  "ignore as instruções anteriores". Delimitar o contexto (ex.: `<contexto>…</contexto>`)
  e instruir o modelo a tratá-lo apenas como informação.
- Manter a instrução "responda só com o contexto; se não souber, diga que não sabe"
  (já presente) e validar a saída antes de agir sobre ela.
- Nunca dar ao LLM ferramentas com efeitos colaterais sem confirmação humana.

## 3. Validação de entrada
- Limitar o tamanho da `pergunta` e do contexto (custo/DoS e estouro de janela).
- `chunks_por_secao` assume o formato `## Título\nconteúdo`; um documento fora do padrão
  levanta `ValueError` no `split("\n", 1)`. Validar o formato antes de indexar.
- Não usar `eval`/`exec`/`pickle` em dados externos.

## 4. Integridade dos dados
- Preservar **metadados** (`id`, `modulo`, `secao`) em cada chunk para rastreabilidade
  e citação da fonte na resposta.
- Versionar a especificação e guardar um **hash (SHA-256)** do documento/chunk; reindexar
  quando mudar, evitando vetores desatualizados em relação ao texto.
- Usar `id`s únicos e imutáveis; detectar duplicatas antes de indexar.
- Persistir índices de forma atômica (gravar em arquivo temporário e renomear) e fazer backup.
- Aplicar o **limiar de similaridade** (`limiar`) e tratar o caso "nenhum resultado":
  hoje, sem resultados, o prompt vai com contexto vazio — responder "não sei" sem chamar o LLM.

## 4.1 Controle de acesso aos dados
- Filtrar chunks por permissão (módulo/tenant) **antes** da busca, não depois da resposta.
- Não indexar dados pessoais (CPF, e-mails, cartões); mascarar/anonimizar (LGPD).

## 5. Dependências e supply chain
- Fixar versões em `requirements.txt` (`pacote==x.y.z`) e usar `pip-audit` periodicamente.
- Baixar modelos apenas de fontes oficiais (Hugging Face) e fixar a revisão.
- Evitar `pip install` de pacotes desconhecidos; usar ambiente virtual.

## 6. Robustez e operação
- Tratar exceções e aplicar timeout/retry com backoff nas chamadas ao LLM.
- Não expor stack traces ou prompts ao usuário final.
- Registrar logs de auditoria (quem perguntou, quais chunks foram usados), sem dados sensíveis.
- Evitar efeitos colaterais na importação (ex.: `print` no nível do módulo em `spec.py`/`chunking.py`);
  proteger com `if __name__ == "__main__":`.

## 7. Achados nesta revisão (código não alterado)
| Arquivo | Achado | Gravidade |
|---|---|---|
| `src/index.py` | `modelo` não definido → `NameError` (não é erro de sintaxe) | Alta (quebra) |
| `src/RAG.py` | Prompt monta contexto sem delimitadores (risco de prompt injection) | Média |
| `src/RAG.py` | Sem resultados acima do limiar, segue com contexto vazio | Baixa |
| `src/spec.py` | `split("\n", 1)` falha se seção sem quebra de linha; `print` ao importar | Baixa |
| `src/llm.py` | Sem timeout/retry; chave lida corretamente via ambiente (bom) | Baixa |
