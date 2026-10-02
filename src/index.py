from sentence_transformers import SentenceTransformer, util
from spec import especificacao, chunks_por_secao   

chunks = chunks_por_secao(especificacao)
textos = [c["texto"] for c in chunks]
vetores_chunks = modelo.encode(textos)

pergunta = "em quantos dias posso pedir meu dinheiro de volta?"
vetor_pergunta = modelo.encode(pergunta)

resultado = util.semantic_search(vetor_pergunta, vetores_chunks, top_k=2)
limiar = 0.5    
for r in resultado[0]:
    if r["score"] >= limiar:
        print(round(r["score"], 2), chunks[r["corpus_id"]]["metadados"]["secao"])