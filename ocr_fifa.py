import re
import sys
from paddleocr import PaddleOCR

def extract_fifa_codes(image_path):
    """
    Extrai códigos de figurinhas da Copa do Mundo de uma imagem usando PaddleOCR.
    Os códigos seguem o formato: AAA 1, BRA 12, etc.
    """
    # Inicializar o modelo OCR
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    
    # Executar OCR na imagem
    result = ocr.ocr(image_path, cls=True)
    
    # Extrair texto das linhas detectadas
    text = ''
    for line in result[0]:  # result[0] contém as linhas
        text += line[1][0] + ' '  # line[1][0] é o texto reconhecido
    
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