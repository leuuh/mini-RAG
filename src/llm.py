import os

try:
    from google.colab import userdata
except ImportError:
    userdata = None

from google import genai


def _get_client():
    api_key = None

    if userdata is not None:
        api_key = userdata.get("GEMINI_API_KEY")
    else:
        api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("Defina GEMINI_API_KEY no ambiente ou no Google Colab.")

    return genai.Client(api_key=api_key)


def perguntar_ao_llm(texto):
    cliente = _get_client()
    resposta = cliente.models.generate_content(
        model="gemini-2.5-flash",
        contents=texto,
    )
    return resposta.text


if __name__ == "__main__":
    prompt = "Responda de forma curta: o que é RAG?"
    print(perguntar_ao_llm(prompt))