casos_de_teste = [
    {"id": "CT-101", "modulo": "pagamentos",
     "texto": "Pré-condição: compra aprovada há menos de 7 dias. Passos: acessar a fatura "
              "e solicitar estorno. Resultado esperado: valor creditado em até 2 dias úteis."},
    {"id": "CT-102", "modulo": "autenticacao",
     "texto": "Pré-condição: senha expirada. Passos: tentar login. "
              "Resultado esperado: sistema exige troca de senha."},
]

def criar_chunk(documento, tipo):
    chunks = []
    for doc in documento:
        chunks.append({
            "texto": doc["texto"],
            "metadados": {"id": doc["id"], "modulo": doc["modulo"], "tipo": tipo}
         })
    return chunks

chunks = criar_chunk(casos_de_teste, "caso_de_teste")
print(len(chunks), chunks[0]["metadados"])
