from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from random import randint


def main(wolds, transcriptions, text, path_save):
    
    font_size = 20
    font = 'font.ttf'
    
    x = 40
    y = 800

    #Создаем pdf
    pdfmetrics.registerFont(TTFont('MyFont', font))
    c = canvas.Canvas(path_save)

    c.setFont('MyFont', font_size)

    for i in wolds:
        if y<=20:
            c.showPage()
            c.setFont('MyFont', font_size)
            y = 800
        c.drawString(x+randint(0, 10), y, i)
        y -= 25

    if y<=20:    
            c.showPage()
            c.setFont('MyFont', font_size)
            y = 800
        
    c.drawString(x+randint(0, 10), y, "Words in transcription")
    y -= 25

    for i in  transcriptions:
        if y<=20:    
            c.showPage()
            c.setFont('MyFont', font_size)
            y = 800
            
        c.drawString(x+randint(0, 10), y, f"{i["t"]} - {i["w"]}")
        y -= 25

    if y<=20:    
            c.showPage()
            c.setFont('MyFont', font_size)
            y = 800
        
    page_width, page_height = A4
    left_margin = 40
    right_margin = 40
    top_margin = 50
    bottom_margin = 50
    text_width = page_width - left_margin - right_margin


    current_y = y + 25
    style = ParagraphStyle('MyStyle', fontName='MyFont', fontSize=font_size, leading=font_size+5)
    p = Paragraph(text.replace('\n', '<br/>'), style)
    available_height = current_y - bottom_margin
    parts = p.split(text_width, available_height)
    if parts:
        first = parts[0]
        # Подготавливаем first к рисованию на canvas c
        first.wrapOn(c, text_width, available_height)
        # Рисуем так, чтобы верхняя граница текста совпадала с current_y
        # Для этого нижний левый угол ставим в (left_margin, current_y - first.height)
        first.drawOn(c, left_margin, current_y - first.height)
        # Обновляем current_y, если дальше ещё что-то будете писать вручную
        current_y -= first.height

    # Остальные части размещаем на новых страницах
    for part in parts[1:]:
        c.showPage()  # новая страница
        # На новой странице нужно сбросить шрифт? Нет, шрифт сохраняется в flowable.
        # Но если вы потом планируете снова рисовать вручную, лучше установить нужный шрифт.
        c.setFont('MyFont', 12)

        # Доступная высота на новой странице (от верхнего поля до нижнего)
        new_page_available_height = page_height - top_margin - bottom_margin

        # Подготавливаем part
        part.wrapOn(c, text_width, new_page_available_height)
        # Рисуем вверху новой страницы (отступ сверху = top_margin)
        part.drawOn(c, left_margin, page_height - top_margin - part.height)
    # Сохраняем PDF
    c.save()

words = [
    "apple", "house", "car", "sun", "forest", "water", "fire", "earth", "sky", "sea",
    "city", "street", "square", "bridge", "river", "lake", "mountain", "wind", "snow", "rain",
    "morning", "afternoon", "evening", "night", "winter", "spring", "summer", "autumn", "time", "minute",
    "person", "woman", "man", "child", "family", "friend", "brother", "sister", "mother", "father",
    "work", "rest", "study", "school", "university", "teacher", "doctor", "engineer", "artist", "musician",
    ]

transcriptions = [{'w': 'hook,', 't': '/hʊk/'}, {'w': 'survey', 't': '/ˈsɜː(r).veɪ/'}, {'w': 'thesis', 't': '/ˈθiː.sɪs/'}]

text = '''
Favorite Word: beloved
The word that I like most from this set is beloved
beloved is an adjective
How do you say it in Russian?
It translates into Russian as любимый, любимая
What does it mean?
It means deeply loved or cherished.
A good synonym for 'beloved' is dear
The opposite of 'beloved' is hated
I find this word inspiring
because it reminds me of  my grandmother who was always a beloved figure in our family. She had a warm smile and a kind heart, which made everyone feel loved and valued.
'''


main(words, transcriptions, text, "test.pdf")