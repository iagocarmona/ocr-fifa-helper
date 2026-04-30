from fastapi import FastAPI, UploadFile, File
import tempfile
import os
from ocr_fifa import extract_fifa_codes

app = FastAPI(title="OCR FIFA Codes API", description="API para reconhecimento de códigos de figurinhas da Copa via OCR")

@app.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    """
    Recebe uma imagem e retorna os códigos de figurinhas detectados.
    """
    # Salvar o arquivo temporariamente
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_path = temp_file.name

    try:
        # Executar OCR
        codes = extract_fifa_codes(temp_path)
        return {"codes": codes}
    except Exception as e:
        return {"error": str(e)}
    finally:
        # Limpar arquivo temporário
        os.unlink(temp_path)

@app.get("/")
async def root():
    return {"message": "API OCR FIFA Codes está rodando. Use POST /ocr para enviar uma imagem."}