import re
import sys
import cv2
import easyocr

reader = None

def get_reader():
    global reader
    if reader is None:
        reader = easyocr.Reader(['en'], gpu=False)
    return reader

def preprocess(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, None, fx=2, fy=2)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return gray


def extract_fifa_code(image_path):
    processed = preprocess(image_path)
    reader = get_reader()
    
    results = reader.readtext(processed)

    print("\n🧠 RAW OCR:")
    for (bbox, text, prob) in results:
        print(f"{text} ({prob:.2f})")

    best_match = None
    highest_conf = 0

    for (_, text, prob) in results:
        cleaned = text.upper().replace(" ", "")

        # correções comuns OCR
        cleaned = cleaned.replace("I", "1").replace("O", "0")

        match = re.search(r'^([A-Z]{3})(\d{1,2})$', cleaned)

        if match and prob > highest_conf:
            code = match.group(1)
            number = int(match.group(2))

            best_match = {
                "code": code,
                "number": number,
                "fullCode": f"{code}{number}",
                "confidence": float(prob)
            }

            highest_conf = prob

    return best_match

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python ocr_fifa.py <imagem>")
        sys.exit(1)

    result = extract_fifa_code(sys.argv[1])

    if result:
        print("\n✅ Resultado:")
        print(result)
    else:
        print("\n❌ Nenhum código encontrado")