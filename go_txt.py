from os import listdir
import os
import json 
import re
import random
from typing import List, Dict, Optional, Union, Tuple
from pathlib import Path



ffmpeg_path = "C:\\Users\\vchul\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-8.0.1-full_build\\bin"  # Измените на свой путь
os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ["PATH"]


list_folder = [f"fold\\{i}\\" for i in listdir("fold")]

def txt_for_json(path):
    import ollama

    def fix_json_quotes(json_text):
        if json_text[0] == "`":
            new_js = json_text[8:-3]
        else:
            new_js = json_text
        pattern1 = r'''("(?:transcription|russian|english|context|examples)":\s*")([^"]*?)\','''
        fixed = re.sub(pattern1, r'\1\2",', new_js)
        return fixed
    list_ans = []
    with open(f"{path}res.txt", "r", encoding='utf-8') as file:
        list_text = file.read().splitlines()
    
    for text_chunk in list_text:
        EXTRACTION_PROMPT = f"""Ты — специалист по извлечению учебной лексики из транскрипций уроков английского.

        ЗАДАЧА:
        Извлеки ВСЕ английские слова/фразы с их русскими переводами и дополнительной информацией.

        ВХОДНЫЕ ДАННЫЕ:
        Текст транскрипции урока, где учитель:
        1. Даёт английское слово
        2. Объясняет значение на русском/английском
        3. Даёт перевод
        4. Может указывать часть речи, примеры, произношение

        ТРЕБОВАНИЯ К ВЫВОДУ:
        1. ВЕРНИ ТОЛЬКО JSON, без пояснений
        2. Формат:
        {{
        "words": [
            {{
            "english": "convention",
            "russian": "договорённость, традиция",
            "context": "оригинальная фраза из текста",
            }}
        ]
        }}

        ПРАВИЛА ИЗВЛЕЧЕНИЯ:
        1. Извлекай ТОЛЬКО слова, которые явно даются для запоминания
        2. Если слово повторяется — объедини информацию
        3. Части речи определяй: noun, verb, adjective, adverb, phrase
        4. Если есть варианты перевода — укажи через запятую
        5. Примеры бери из контекста урока
        6. Внимательно следи за ковычками в транскрипциях. ВНУТРИ ИПОЛЬЗУЙ ТОЛЬКО ' А СНАРУЖИ ДЛЯ УПАКОВКИ В СТРОКУ ТОЛЬКО "

        ОБРАБОТКА БОЛЬШИХ ТЕКСТОВ:
        Это ЧАСТЬ большого текста. Обработай только предоставленный фрагмент.
        Если встречаешь "Write down..." — это точно слово для извлечения.

        ВОТ ТЕКСТ ДЛЯ АНАЛИЗА:
        {text_chunk}
        """

        response = ollama.chat(
            model='qwen2.5:7b',
            messages=[{'role': 'user', 'content': EXTRACTION_PROMPT}],
            options={'temperature': 0.1}  # Меньше "креатива", больше точности
        )
        
        try:
            ob = response['message']['content']
            ob = fix_json_quotes(ob)
            list_ans.append(json.loads(ob))
            #list_ans.append(response['message']['content'])
        except Exception as e:
            print(ob)
            print(path)
            print(f"Ошибка {e}")
        #    exit
        
    return list_ans

def json_to_list(json):
    list_r = []
    for i in json:
        for j in i["words"]:
            list_r.append((j['english'], str(j['russian'].split()[0]), j["context"]))
    return list_r

def create_vocabulary_pdf_advanced(word_pairs, output_filename="vocabulary_two_columns_compact.pdf", font_file="frift.ttf", font_size=25):
    def filter_text_for_font(text):
        """
        Удаляет из текста все символы, которых нет в шрифте.
        Оставляет только разрешенные символы.
        """
        # Разрешенные символы (латиница, кириллица, цифры, знаки препинания)
        allowed_chars = set(
            'abcdefghijklmnopqrstuvwxyz'
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
            'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
            '0123456789'
            '.,-:;!?()[]{}"\''  # Апостроф добавлен в кавычках
            ' '  # пробел
        )
    
        # Добавляем транскрипционные символы, которые могут быть в английских словах
        transcription_chars = set("ˈˌː")
        allowed_chars.update(transcription_chars)
        
        # Фильтруем текст, оставляя только разрешенные символы
        filtered_text = ''.join(char for char in text if char in allowed_chars)
        
        return filtered_text
    
    """
    Две колонки с автоматическим переносом текста.
    1 слово-перевод-транскрипция
    2 слово-перевод-транскрипция
    С эффектом рукописного текста
    """
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.pagesizes import A4
    import random
    
    # Загружаем шрифт
    try:
        pdfmetrics.registerFont(TTFont('Frift', font_file))
        FONT_NAME = 'Frift'
        print(f"✅ Шрифт зарегистрирован: {font_file}")
    except:
        FONT_NAME = 'Helvetica'
        print("⚠️ Шрифт frift.ttf не найден, использую Helvetica")
    
    # Создаем PDF
    c = canvas.Canvas(output_filename, pagesize=A4)
    width, height = A4
    
    # Настройки страницы
    margin_left = 20
    margin_right = 25
    margin_top = height - 60
    margin_bottom = 60
    
    # Рассчитываем колонки
    total_width = width - margin_left - margin_right
    column_width = total_width
    
    # Используем только левую колонку
    left_column_x = margin_left
    
    current_y = margin_top
    base_font_size = font_size

    # Функция для переноса текста
    def wrap_text(text, font_name, font_size, max_width):
        """Разбивает текст на строки, чтобы поместиться в max_width."""
        lines = []
        current_line = []
        current_width = 0
        
        words = text.split()
        space_width = c.stringWidth(' ', font_name, font_size)
        
        for word in words:
            word_width = c.stringWidth(word, font_name, font_size)
            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width + space_width
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width + space_width
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines

    # Обрабатываем слова
    for i in range(len(word_pairs)):
        # Проверяем, не вышли ли за нижний край
        if current_y < margin_bottom + 50:  # Оставляем запас
            c.showPage()
            current_y = margin_top
        
        english1, russian1, rash1 = word_pairs[i]
        
        # Формируем полный текст с транскрипцией
        full_text = filter_text_for_font(f"{i+1}. {english1} - {russian1}{" "*20}{rash1}")
        
        # Случайные параметры для этого элемента
        font_size1 = base_font_size + random.randint(-3, 3)
        x_offset1 = random.randint(-6, 6)
        y_offset1 = random.randint(-4, 5)
        
        # Разбиваем текст на строки
        lines = wrap_text(full_text, FONT_NAME, font_size1, column_width)
        
        # Выводим каждую строку
        line_height = 25 + random.randint(-4, 4)
        
        # Проверяем, хватит ли места для всех строк
        needed_height = len(lines) * line_height
        if current_y - needed_height < margin_bottom:
            c.showPage()
            current_y = margin_top
        
        for j, line in enumerate(lines):
            # Рисуем строку
            c.setFont(FONT_NAME, font_size1)
            left_x = left_column_x + x_offset1
            left_y = current_y + y_offset1
            
            # Эффект дрожания (только для первой строки элемента)
            if j == 0 and random.random() < 0.25:
                c.setFillGray(0.9)
                c.drawString(left_x + 1, left_y - 1, line)
                c.setFillGray(0)
            
            c.drawString(left_x, left_y, line)
            
            # Кляксы (редко, только для последней строки элемента)
            if j == len(lines) - 1 and random.random() < 0.03:
                blot_x = left_x + random.randint(-5, 5)
                blot_y = left_y + random.randint(-12, -8)
                c.setFillGray(0.7)
                c.circle(blot_x, blot_y, 0.6, fill=1)
                c.setFillGray(0)
            
            # Переход к следующей строке
            current_y -= line_height
    
    # Сохраняем PDF
    c.save()
    
    print(f"✅ PDF создан: {output_filename}")
    print(f"   Формат: одна колонка с переносами")
    print(f"   Размер шрифта: ~{base_font_size}pt")
    print(f"   Всего слов: {len(word_pairs)}")
    
    return output_filename



for i in list_folder:
    try:
        if not("res.txt" in listdir(i)):     
            for j in listdir(i):
                print(f"Начало обработки {f"{i}{j}"}")
                import whisper
                model = whisper.load_model("medium")
                res = model.transcribe(f"{i}{j}",task="transcribe")["text"]
                #res = j
                with open(f"{i}res.txt", "a", encoding='utf-8') as file:
                    file.write(res + "\n")

                print(f"Конец обработки {i}{j}")
    except Exception as e:
        print(f"Ошибка на этапе расспознования аудио:{e}")
        print({i})
    
    print(f"Достование слов и переводов для {i}")
    
    try:
        if not(f"slov.json" in listdir(i)):
            list_json = txt_for_json(i)
            with open(f"{i}slov.json", "w", encoding="utf-8") as file:
                json.dump({"list":list_json}, file)
        else:
            print("Испрользование готовых данных")
            try:
                with open(f"{i}slov.json", 'r', encoding='utf-8') as f:
                    list_json = json.load(f)["list"]
                
            except FileNotFoundError:
                print(f"❌ Файл {i}slov.json не найден")
            except json.JSONDecodeError as e:
                print(f"❌ Ошибка в JSON файле: {e}")
    except Exception as e:
        print(f"Ошибка на этапе доставания слов:{e}")
        print({i})

    

    print("Слова на собирание в pdf")

    try:
        list_slov = json_to_list(list_json)
    except Exception as e:
        print(f"Ошибка на этапе :{e}")
        print({i})

    print("Создание pdf")

    try:
        create_vocabulary_pdf_advanced(list_slov, output_filename=f'{i}ans.pdf')
    except Exception as e:
        print(f"Ошибка на этапе :{e}")
        print({i})
    
    print("Создание фото")

    try:
        from pdf_to_image import pdf_to_photos
        pdf_to_photos(f"{i}ans.pdf", output_folder=f"{i}img")
    except Exception as e:
        print(f"Ошибка при создании фото {e}")

    print(f"С {i} закончено")

    
    
