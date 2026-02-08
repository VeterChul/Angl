import fitz  # PyMuPDF
import re

def extract_bold_text(pdf_path):
    """
    Извлекает жирный текст из PDF с помощью PyMuPDF
    """
    bold_texts = []
    
    # Открываем PDF
    doc = fitz.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Получаем текст со свойствами
        blocks = page.get_text("dict")["blocks"]
        
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        # Проверяем, является ли текст жирным
                        # Жирный текст обычно имеет флаг 16 или содержит "Bold" в названии шрифта
                        is_bold = span["flags"] & 2**4  # 16 - bold flag
                        font_name = span["font"].lower()
                        
                        if is_bold or "bold" in font_name:
                            text = span["text"].strip()
                            if text:  # Игнорируем пустые строки
                                bold_texts.append(text)
    
    doc.close()
    return bold_texts

# Использование
pdf_path = "ваш_файл.pdf"
bold_text = extract_bold_text(pdf_path)

print("Жирный текст в документе:")
for i, text in enumerate(bold_text, 1):
    print(f"{i}. {text}")