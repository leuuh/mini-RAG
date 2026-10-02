especificacao = {
    "id": "REQ-PAG", "modulo": "pagamentos",
    "texto": "## Estorno\nO cliente pode solicitar estorno em até 7 dias.\n"
             "## Parcelamento\nCompras acima de R$100 podem ser parceladas em até 12x.\n"
             "## Boleto\nO boleto vence em 3 dias úteis.",
}


def chunks_por_secao(doc):
    chunks = []
    partes = doc["texto"].split("##")
    for parte in partes:
        if parte == "":   
            continue
        titulo, conteudo = parte.split("\n", 1)
        chunks.append({
            "texto": conteudo.strip(),
            "metadados": {"id": doc["id"], "modulo": doc["modulo"], "secao": titulo.strip()},
        })
        
    return chunks
        
    
for c in chunks_por_secao(especificacao):
    print(c)