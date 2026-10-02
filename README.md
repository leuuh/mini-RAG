# RAG — busca semântica sobre especificações e casos de teste

## Estrutura
```
rag/
├── src/
│   ├── spec.py       # especificação de exemplo + chunking por seção
│   ├── chunking.py   # chunking de casos de teste
│   ├── RAG.py        # embeddings, busca semântica e montagem do prompt
│   ├── index.py      # indexação/consulta (ver nota abaixo)
│   └── llm.py        # cliente Gemini (chave via ambiente/Colab)
├── docs/SEGURANCA.md # boas práticas de segurança e integridade de dados
├── requirements.txt
├── .env.example
└── .gitignore
```

## Uso
```
pip install -r requirements.txt
set GEMINI_API_KEY=sua_chave      # Windows (cmd)
python src/RAG.py
python src/llm.py
```

## Pendência conhecida
`src/index.py` usa `modelo` sem defini-lo (NameError em execução). Não é erro de
sintaxe, então não foi alterado; a correção é importar/criar o `SentenceTransformer`
como em `RAG.py`.
