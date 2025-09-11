from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import requests
import re
import json
import os
import validators

app = FastAPI(title="CPTED Image Analysis API")

# ==============================
# 🔑 Configurações da API
# ==============================
API_URL = "https://api.hyperbolic.xyz/v1/chat/completions"
API_KEY = os.getenv("CPTED_API_KEY", "")
if not API_KEY:
    raise RuntimeError("API Key não definida. Configure a variável de ambiente CPTED_API_KEY.")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}

PROMPT = """Quero que você atue como um especialista em CPTED (Crime Prevention Through Environmental Design).  
Vou enviar uma imagem de uma rua e você deve analisá-la segundo os seis princípios do CPTED:

1. **Vigilância Natural (V)** – Há iluminação adequada? A rua é visível? Janelas e fachadas contribuem para a observação?
2. **Controle Natural de Acesso (A)** – Existem barreiras, entradas definidas, portões ou elementos que limitem acessos indesejados?
3. **Reforço Territorial (T)** – Há sinais claros de propriedade e pertencimento (jardins cuidados, muros, sinalização, pintura)?
4. **Manutenção (M)** – O espaço está limpo, conservado, sem pichações ou sinais de abandono?
5. **Atividades Legítimas (AL)** – O espaço é usado para atividades positivas (comércio, lazer, convivência)?
6. **Suporte para Atividades Sociais (S)** – Existem estruturas que favoreçam interação comunitária (praças, bancos, quadras)?

Sua resposta deve seguir **estritamente este formato de saída**:

### Análise CPTED

**1. Vigilância Natural (V)**
- Nota: X/10
- Comentário: [descreva sua avaliação]

**2. Controle Natural de Acesso (A)**
- Nota: X/10
- Comentário: [descreva sua avaliação]

**3. Reforço Territorial (T)**
- Nota: X/10
- Comentário: [descreva sua avaliação]

**4. Manutenção (M)**
- Nota: X/10
- Comentário: [descreva sua avaliação]

**5. Atividades Legítimas (AL)**
- Nota: X/10
- Comentário: [descreva sua avaliação]

**6. Suporte para Atividades Sociais (S)**
- Nota: X/10
- Comentário: [descreva sua avaliação]
"""

# ==============================
# Funções auxiliares
# ==============================
def get_cpted_analysis(image_url: str) -> str:
    """
    Envia a imagem para a API externa e retorna o texto de análise CPTED.
    Lança HTTPException em caso de erro.
    """
    payload = {
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": PROMPT},
                {"type": "image_url", "image_url": {"url": image_url}},
            ],
        }],
        "model": "Qwen/Qwen2.5-VL-7B-Instruct",
        "max_tokens": 512,
        "temperature": 0.1,
        "top_p": 0.001,
    }
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Erro de conexão com API externa: {str(e)}")
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=500, detail=f"Resposta inesperada da API: {str(e)}")


def parse_cpted_analysis(text: str) -> list:
    """
    Faz o parsing do texto de análise CPTED e retorna lista de critérios.
    """
    pattern = re.compile(
        r"\*\*(\d+)\.\s*(.*?)\*\*\s*"
        r"- Nota:\s*(\d+)/10\s*"
        r"- Comentário:\s*(.*?)(?=\n\*\*|\Z)",
        re.DOTALL
    )
    result = []
    for _, criterion, score, comment in pattern.findall(text):
        result.append({
            "criterio": criterion.strip(),
            "nota": int(score),
            "comentario": comment.strip().replace("\n", " ")
        })
    return result

# ==============================
# Endpoint
# ==============================
@app.get("/api/image-extract/{image_url:path}")
async def extract_cpted(image_url: str):
    """
    Recebe a URL de uma imagem e retorna a análise CPTED estruturada em JSON.
    Valida a URL, verifica tamanho da imagem e trata erros detalhadamente.
    """
    # Validação da URL
    if not validators.url(image_url):
        raise HTTPException(status_code=400, detail="URL da imagem inválida.")

    # Verificação básica de tamanho da imagem (HEAD request)
    try:
        head = requests.head(image_url, timeout=10)
        if head.status_code != 200:
            raise HTTPException(status_code=404, detail="Imagem não encontrada.")
        content_length = head.headers.get("Content-Length")
        if content_length and int(content_length) > 5_000_000:  # 5MB
            raise HTTPException(status_code=413, detail="Imagem muito grande. Limite: 5MB.")
    except requests.RequestException:
        raise HTTPException(status_code=400, detail="Não foi possível acessar a imagem.")

    try:
        raw_text = get_cpted_analysis(image_url)
        analysis = parse_cpted_analysis(raw_text)
        return JSONResponse(content=analysis)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
