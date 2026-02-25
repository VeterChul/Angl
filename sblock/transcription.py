import fitz  # PyMuPDF
import re

def extract_bold_from_pdf(pdf_path):
    """
    Извлекает жирный текст из PDF, используя информацию о шрифтах
    """
    doc = fitz.open(pdf_path)
    bold_texts = []
    
    # Шаблоны для определения жирного текста
    bold_patterns = [
        r'bold', 'bd', 'black', 'heavy', 'semibold', 'demibold',
        '700', '800', '900', 'жирный', 'boldmt', 'calibrib', 'calibri-b'
    ]
    
    # Шрифты, которые считаем жирными (Calibri без Light)
    bold_fonts = [
        'calibri',  # стандартный Calibri (не Light)
        'calibrib',  # Calibri Bold
        'calibri-b',  # Calibri Bold
        'calibri-bold'  # Calibri Bold
    ]
    
    # Шрифты, которые считаем НЕжирными
    non_bold_fonts = [
        'calibril',  # Calibri Light
        'calibri-light',  # Calibri Light
        'calibri-l'  # Calibri Light
    ]
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Получаем все текстовые блоки
        blocks = page.get_text("dict")["blocks"]
        
        for block in blocks:
            if "lines" not in block:
                continue
                
            for line in block["lines"]:
                line_bold_parts = []
                
                for span in line["spans"]:
                    font_name = span["font"].lower() if span.get("font") else ""
                    flags = span.get("flags", 0)
                    
                    # Проверяем различные способы определения жирности
                    is_bold = False
                    
                    # 1. Проверяем флаг жирности в PDF
                    if flags & 2**4:  # 16 - bold flag
                        is_bold = True
                    
                    # 2. Проверяем по названию шрифта (Calibri без Light)
                    elif font_name:
                        # Ищем шрифты Calibri без Light
                        if 'calibri' in font_name:
                            # Если это Calibri, но не Light
                            if any(pattern in font_name for pattern in bold_fonts):
                                is_bold = True
                            elif 'light' not in font_name and 'l' not in font_name[-2:]:
                                # Calibri без Light - вероятно, жирный
                                is_bold = True
                    
                    # 3. Проверяем по другим признакам жирности
                    if not is_bold and font_name:
                        # Ищем любые признаки жирности в названии шрифта
                        for pattern in bold_patterns:
                            if pattern in font_name:
                                is_bold = True
                                break
                    
                    # Если текст жирный, добавляем его
                    if is_bold:
                        text = span["text"].strip()
                        if text:
                            line_bold_parts.append(text)
                
                # Если в строке есть жирные части, объединяем их
                if line_bold_parts:
                    bold_line = " ".join(line_bold_parts)
                    bold_texts.append({
                        'page': page_num + 1,
                        'text': bold_line,
                        'raw_text': line_bold_parts
                    })
    
    doc.close()
    return bold_texts

def extract_english_words_and_transcriptions(bold_items):
    """
    Фильтрует английские слова и их транскрипции из жирного текста
    """
    english_items = []
    
    # Паттерны для английских слов (с дефисами и апострофами)
    english_word_pattern = re.compile(r'^[A-Za-z\-\'\s]+$')
    
    # Паттерны для транскрипций
    transcription_patterns = [
        r'^\[.*\]$',    # [trænˈskrɪpʃən]
        r'^/.*/$',      # /trænˈskrɪpʃən/
        r'^⟨.*⟩$',      # ⟨trænˈskrɪpʃən⟩
        r'^\/.*\/$',    # \/trænˈskrɪpʃən\/
    ]
    
    for item in bold_items:
        text = item['text'].strip()
        
        # Пропускаем слишком короткий текст
        if len(text) < 2:
            continue
        
        # Проверяем, является ли текст английским словом
        if english_word_pattern.match(text):
            english_items.append({
                'page': item['page'],
                'type': 'english_word',
                'text': text,
                'raw': item
            })
        
        # Проверяем, является ли текст транскрипцией
        else:
            for pattern in transcription_patterns:
                if re.match(pattern, text):
                    english_items.append({
                        'page': item['page'],
                        'type': 'transcription',
                        'text': text,
                        'raw': item
                    })
                    break
    
    return english_items

def main(pdf_path):
    """
    Основная функция обработки PDF
    """
    
    bold_texts = extract_bold_from_pdf(pdf_path)
    
    if not bold_texts:
        print("Жирный текст не найден!")
        return
        
    # 3. Фильтруем английские слова и транскрипции
    english_items = extract_english_words_and_transcriptions(bold_texts)
    
    if english_items:
        # Разделяем слова и транскрипции
        transcriptions = [item["text"] for item in english_items if item['type'] == 'transcription']
        
    else:
        print("\nАнглийские слова и транскрипции не найдены")
    
    
    return transcriptions


# Запуск скрипта
# if __name__ == "__main__":
#     # Укажите путь к вашему PDF файлу
#     pdf_file = "fold/03/pdf/ans.pdf"  # Замените на путь к вашему файлу
    
#     try:
#         transcriptions = main(pdf_file)
#         print(transcriptions)
        
#     except FileNotFoundError:
#         print(f"ОШИБКА: Файл '{pdf_file}' не найден.")
#         print("Пожалуйста, укажите правильный путь к PDF файлу.")
#     except Exception as e:
#         print(f"ОШИБКА: {e}")
#         print("Убедитесь, что у вас установлены необходимые библиотеки:")
#         print("  pip install PyMuPDF")