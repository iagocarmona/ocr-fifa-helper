from fastapi import FastAPI, UploadFile, File
import tempfile
import os
from ocr_fifa import extract_fifa_codes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="OCR FIFA Codes API",
    description="API para reconhecimento de códigos de figurinhas da Copa via OCR"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    print("\n📥 Nova requisição recebida")

    if not file:
        print("❌ Nenhum arquivo enviado")
        return {"error": "No file"}

    print(f"📄 Nome do arquivo: {file.filename}")
    print(f"📄 Tipo: {file.content_type}")

    # Salvar temporário
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_path = temp_file.name

    print(f"💾 Arquivo salvo em: {temp_path}")
    print(f"📦 Tamanho: {len(content)} bytes")

    try:
        print("🔍 Iniciando OCR...")
        codes = extract_fifa_codes(temp_path)

        print(f"✅ OCR finalizado")
        print(f"🔢 Códigos encontrados: {codes}")

        return {"codes": codes}

    except Exception as e:
        print("❌ Erro no OCR:", str(e))
        return {"error": str(e)}

    finally:
        print("🧹 Removendo arquivo temporário")
        os.unlink(temp_path)
        print("🧹 Arquivo removido")


@app.get("/")
async def root():
    print("🌐 Health check acessado")
    return {"message": "API OCR FIFA Codes está rodando. Use POST /ocr para enviar uma imagem."}