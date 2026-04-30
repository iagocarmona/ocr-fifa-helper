# OCR para Códigos de Figurinhas da Copa

Este projeto fornece tanto um script standalone quanto uma API para reconhecer códigos de figurinhas da Copa do Mundo em imagens usando PaddleOCR. Os códigos seguem o formato de três letras maiúsculas seguidas de um número, como "BRA 12" ou "AAA 1".

## Instalação

1. Instale Python 3 se não estiver instalado (no Linux: `sudo apt install python3 python3-pip`).
2. Instale as dependências:

   ```
   pip install -r requirements.txt
   ```

   Nota: PaddleOCR requer PaddlePaddle, que pode precisar de instalação específica dependendo do seu sistema. Consulte a documentação oficial se houver problemas.

## Uso como Script Standalone

Execute o script passando o caminho para a imagem como argumento:

```
python ocr_fifa.py caminho/para/imagem.jpg
```

O script irá imprimir os códigos encontrados na imagem.

### Exemplo

Supondo que você tenha uma imagem `figurinha.jpg` com o código "BRA 12":

```
python ocr_fifa.py figurinha.jpg
```

Saída esperada:

```
Códigos encontrados:
BRA 12
```

## Uso como API

A API permite que outros serviços enviem imagens via HTTP POST e recebam os códigos extraídos.

### Executar a API

```
uvicorn app:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`.

### Endpoint

- **POST /ocr**: Envie uma imagem como multipart/form-data.

  Parâmetro: `file` (arquivo de imagem, e.g., JPG, PNG).

  Resposta: JSON com `codes` (lista de códigos encontrados) ou `error` (em caso de falha).

### Exemplo de Requisição

Usando curl:

```
curl -X POST "http://127.0.0.1:8000/ocr" -F "file=@figurinha.jpg"
```

Resposta de sucesso:

```json
{
  "codes": ["BRA 12", "AAA 1"]
}
```

### Documentação Interativa

Acesse `http://127.0.0.1:8000/docs` para a documentação interativa do FastAPI.

## Deploy no Render

Para hospedar a API na nuvem usando Render:

1. **Envie o código para o GitHub**: Crie um repositório no GitHub e faça push dos arquivos (`app.py`, `ocr_fifa.py`, `requirements.txt`, `runtime.txt`, `README.md`).

2. **Conecte ao Render**:
   - Acesse [render.com](https://render.com) e faça login.
   - Clique em "New" > "Web Service".
   - Conecte seu repositório do GitHub.

3. **Configure o serviço**:
   - **Name**: Escolha um nome para o serviço (e.g., `ocr-fifa-api`).
   - **Environment**: Selecione `Python`.
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Escolha um plano gratuito ou pago conforme necessário.

4. **Deploy**: Clique em "Create Web Service". O Render irá construir e implantar automaticamente.

5. **Acesse a API**: Após o deploy, você receberá uma URL (e.g., `https://ocr-fifa-api.onrender.com`). Use essa URL para fazer requisições POST para `/ocr`.

### Exemplo de Requisição no Deploy

```
curl -X POST "https://seu-servico.onrender.com/ocr" -F "file=@figurinha.jpg"
```

Nota: O plano gratuito do Render pode ter limitações de uso; considere um plano pago para produção.

## Notas

- Certifique-se de que a imagem esteja clara e o texto legível para melhores resultados.
- O script/API usa o modelo de idioma inglês, adequado para códigos alfanuméricos.
- Se nenhum código for encontrado, verifique a qualidade da imagem ou ajuste o padrão regex se necessário.
# ocr-fifa-helper
