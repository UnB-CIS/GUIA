# API CPTED Image Analysis

Esta API utiliza FastAPI para analisar imagens de ruas segundo os princípios do CPTED (Crime Prevention Through Environmental Design).

## Endpoints

### `GET /api/image-extract/{image_url}`
Recebe uma URL de imagem e retorna uma análise CPTED estruturada em JSON.

- **Parâmetro:**
  - `image_url`: URL da imagem pública (JPEG, PNG, etc)
- **Resposta:**
  - Lista de critérios CPTED, cada um com nota (0-10) e comentário.

#### Exemplo de resposta
```json
[
  {
    "criterio": "Vigilância Natural (V)",
    "nota": 8,
    "comentario": "A rua possui boa iluminação e visibilidade."
  },
  // ... demais critérios ...
]
```

## Como iniciar o servidor

1. **Instale as dependências:**
   ```bash
   pip install fastapi uvicorn validators requests
   ```

2. **Configure a variável de ambiente da API Key:**
   ```bash
   export CPTED_API_KEY="<sua_api_key>"
   ```

3. **Inicie o servidor FastAPI:**
   ```bash
   uvicorn app:app --reload
   ```
   (Execute o comando na pasta `services/VLM`)

## Como usar

- Acesse: `http://localhost:8000/docs` para a documentação interativa (Swagger UI).
- Faça requisições GET para `/api/image-extract/{image_url}` usando ferramentas como curl, Postman ou diretamente pelo navegador.

#### Exemplo com curl
```bash
curl "http://localhost:8000/api/image-extract/https://m.extra.globo.com/incoming/15973700-86a-b53/w640h360-PROP/2010-320088734-2010030436218_20100304.jpg"
```

## Observações
- A API valida a URL e o tamanho da imagem (máx. 5MB).
- A chave da API deve ser obtida junto ao serviço externo utilizado.
- Em caso de erro, será retornado um código HTTP apropriado e mensagem explicativa.
