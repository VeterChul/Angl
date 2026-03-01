from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

# Регистрация шрифта (если ещё не сделано)
pdfmetrics.registerFont(TTFont('MyFont', 'font.ttf'))

# Параметры страницы
page_width, page_height = A4
left_margin = 50
right_margin = 50
top_margin = 50
bottom_margin = 50
text_width = page_width - left_margin - right_margin

# Создаём canvas (предположим, вы уже что-то писали на нём)
c = canvas.Canvas("output.pdf", pagesize=A4)

# ... тут ваш код, который уже что-то записал на нескольких страницах ...
# Допустим, после всей работы вы находитесь на последней странице
# и знаете текущую координату Y (от верхнего края), с которой хотите начать длинный текст.
current_y = page_height - top_margin - 200  # например, через 200 pt от верхнего поля

# Длинный текст
long_text = "Очень длинный текст... (ваш текст, возможно с \\n)"

# Стиль
style = ParagraphStyle('MyStyle', fontName='MyFont', fontSize=12, leading=14)

# Создаём параграф
p = Paragraph(long_text, style)

# Доступная высота на текущей странице (от current_y до нижнего поля)
available_height = current_y - bottom_margin

# Разбиваем параграф на части, помещающиеся в эту область
parts = p.split(text_width, available_height)

# Рисуем первую часть на текущей странице
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

# Завершаем документ
c.save()