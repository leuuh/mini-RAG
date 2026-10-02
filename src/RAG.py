from spec import especificacao, chunks_por_secao   
from sentence_transformers import SentenceTransformer, util
import numpy as np

modelo = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

frases = [
    "solicitar estorno da compra",
    "chargeback no cartão de crédito",
    "erro ao fazer login",
]

vetores = modelo.encode(frases)
print("tamanho de cada vetor: ", len(vetores[0]))
print(util.cos_sim(vetores, vetores))

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

contexto = ""
for r in resultado[0]:
    if r["score"] >= limiar:
        contexto += chunks[r["corpus_id"]]["texto"] + "\n"

prompt = f"""Responda usando APENAS o contexto abaixo.
Se a resposta não estiver no contexto, diga que não sabe.

Contexto:
{contexto}  
Pergunta: {pergunta}"""

print(prompt)