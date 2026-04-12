import ollama

def txt_for_json(path_save):
    try:
        with open(f"{path_save}/res.txt", "r", encoding='utf-8') as file:
            list_text = file.read().splitlines()
    except Exception as e:
        print(f"Ошибка {e}, при открытии файла в {path}")
        return [], False
    list_ans = []
    i = 0
    for text_chunk in list_text:
        i+=1
        EXTRACTION_PROMPT =  f"""
        Ты — эксперт по анализу лекций. Входной текст — транскрипция лекции на русском и английском языке.

        Твоя задача: найти все случаи, когда лектор ПРЯМО или КОСВЕННО просит студентов что-то записать. Извлеки именно ту фразу (слово, термин, короткое выражение), которую нужно записать.

        Правила:
        1. Командами считай любые фразы из списка (и их грамматические вариации):
        - русские: "запишите", "запиши", "пишите", "запомните", "выпишите", "возьмите на заметку", "обратите внимание на", "важный термин", "повторите", "это нужно записать", "зафиксируйте", "выделите", "ключевое слово", "обратите внимание на слово", "давайте запишем", "прошу записать".
        - английские: "write down", "note", "record", "copy", "remember the word", "important term", "listen and repeat", "take note", "jot down", "please write", "let's write", "note down".

        2. Сразу после команды (иногда через 1–3 пояснительных слова) идёт целевая фраза. Извлеки только её.
        Пример: "запишите слово convention" → "convention"
        Пример: "обратите внимание на термин 'conventional expression'" → "conventional expression"
        Пример: "важно запомнить речевое клише" → "речевое клише"

        3. Если команда повторяется для одной и той же фразы подряд (из-за сбоя транскрипции), верни фразу один раз. Если та же фраза встречается позже снова (через минуту), верни её снова — это отдельное требование.

        4. Если лектор говорит: "запишите" и затем называет несколько слов через паузу, каждое слово считай отдельной фразой для записи. Пример: "запишите first, second, third" → "first; second; third"

        5. Игнорируй длинные повторяющиеся блоки, не содержащие новых команд.

        Формат вывода (строгий):
        - Только одна строка, слова/фразы разделены символом ";" (точка с запятой)
        - Никаких пробелов до и после ";"
        - Никаких кавычек, скобок, пояснений, номеров
        - Если ничего не найдено — пустая строка

        Примеры правильного вывода:
        convention;conventional expression;речевое клише
        write down;take note
        first term;second term

        Текст для анализа:
        {text_chunk}
        """
        response = ollama.chat(
            model='qwen2.5:7b',
            messages=[{'role': 'user', 'content': EXTRACTION_PROMPT}],
            options={'temperature': 0.1}  # Меньше "креатива", больше точности
        )
        
        try:
            ob = response['message']['content']
            words = ob.split(";")
            print(words)
            for word in words:
                list_ans.append(word)
            
            
        except Exception as e:
            print(path_save)
            print(i)
            print(f"Ошибка {e}")
            return [], False
        #    exit
        
    return list_ans, True
