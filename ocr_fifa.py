import re
import sys
import easyocr

def extract_fifa_codes(image_path):
    """
    Extrai códigos de figurinhas da Copa do Mundo de uma imagem usando EasyOCR.
    Os códigos seguem o formato: AAA 1, BRA 12, etc.
    """
    # Inicializar o modelo OCR
    reader = easyocr.Reader(['en'])
    
    # Executar OCR na imagem
    result = reader.readtext(image_path)
    
    # Extrair texto das linhas detectadas
    text = ''
    for detection in result:
        text += detection[1] + ' '  # detection[1] é o texto reconhecido
    
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