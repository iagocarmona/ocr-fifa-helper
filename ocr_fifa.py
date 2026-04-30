import re
import sys
import pytesseract
from PIL import Image

def extract_fifa_codes(image_path):
    """
    Extrai códigos de figurinhas da Copa do Mundo de uma imagem usando Tesseract OCR.
    Os códigos seguem o formato: AAA 1, BRA 12, etc.
    """
    # Abrir a imagem
    image = Image.open(image_path)
    
    # Executar OCR na imagem
    text = pytesseract.image_to_string(image)
    
    # Procurar por padrões de códigos: três letras maiúsculas seguidas de espaço e número
    pattern = r'\b[A-Z]{3} \d+\b'
    codes = re.findall(pattern, text)
    
    return codes

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python ocr_fifa.py <caminho_da_imagem>")
        print("Exemplo: python ocr_fifa.py imagem.jpg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    try:
        codes = extract_fifa_codes(image_path)
        if codes:
            print("Códigos encontrados:")
            for code in codes:
                print(code)
        else:
            print("Nenhum código encontrado na imagem.")
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")