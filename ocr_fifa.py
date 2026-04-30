import cv2
import pytesseract
import re
from difflib import get_close_matches

VALID_CODES = [
    # Grupo A
    "MEX", "RSA", "KOR", "CZE",

    # Grupo B
    "CAN", "BIH", "QAT", "SUI",

    # Grupo C
    "BRA", "MAR", "HAI", "SCO",

    # Grupo D
    "USA", "PAR", "AUS", "TUR",

    # Grupo E
    "GER", "CUW", "CIV", "ECU",

    # Grupo F
    "NED", "JPN", "SWE", "TUN",

    # Grupo G
    "BEL", "EGY", "IRN", "NZL",

    # Grupo H
    "ESP", "CPV", "KSA", "URU",

    # Grupo I
    "FRA", "SEN", "IRQ", "NOR",

    # Grupo J
    "ARG", "ALG", "AUT", "JOR",

    # Grupo K
    "POR", "COD", "UZB", "COL",

    # Grupo L
    "ENG", "CRO", "GHA", "PAN"
]

def fix_code(code):
    match = get_close_matches(code, VALID_CODES, n=1, cutoff=0.6)
    return match[0] if match else None


def preprocess(img):
    img = cv2.resize(img, None, fx=2.5, fy=2.5)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 🔥 inverter (CRÍTICO)
    gray = cv2.bitwise_not(gray)

    # 🔥 threshold adaptativo
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return thresh


def normalize_text(text):
    text = text.upper()
    text = text.replace(" ", "").replace("\n", "")

    # remove lixo
    text = re.sub(r'[^A-Z0-9]', '', text)

    # correções OCR
    replacements = {
        "I": "1",
        "L": "1",
        "|": "1",
        "!": "1",
        "O": "0",
        "Q": "0",
        "G": "6",
        "B": "8",
        "S": "5"
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text


def extract_fifa_code(image_path):
    img = cv2.imread(image_path)

    if img is None:
        print("❌ erro ao carregar imagem")
        return None

    processed = preprocess(img)
    cv2.imwrite("debug.png", processed)

    text = pytesseract.image_to_string(
        processed,
        config=r'--oem 3 --psm 6'
    )

    print("\n🧠 OCR RAW:", repr(text))

    cleaned = normalize_text(text)

    print("🧼 CLEANED:", cleaned)

    # 🔥 pega candidatos dentro do texto
    candidates = re.findall(r'[A-Z0-9]{4,6}', cleaned)

    print("🔎 CANDIDATES:", candidates)

    for c in candidates:
        # 🔥 tenta todos os offsets possíveis
        for i in range(len(c) - 3):
            sub = c[i:i+5]  # tenta pegar algo tipo GER16

            match = re.match(r'([A-Z0-9]{3})([0-9]{1,2})', sub)
            if not match:
                continue

            raw_code = match.group(1)
            number_part = match.group(2)

            # 🔥 normaliza código
            fixed_code = fix_code(raw_code)

            if fixed_code:
                return {
                    "code": fixed_code,
                    "number": int(number_part),
                    "fullCode": f"{fixed_code}{number_part}",
                    "confidence": 1.0
                }

    return None


if __name__ == "__main__":
    import sys

    result = extract_fifa_code(sys.argv[1])
    print("\n🎯 RESULT:", result)