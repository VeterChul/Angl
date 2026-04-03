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
        EXTRACTION_PROMPT = f"""
        Ты — ассистент, который обрабатывает расшифровку аудио лекции. В тексте смешаны русский и английский языки.

        ПРАВИЛА ИНСТРУКЦИИ:
        1. Ты должен найти в тексте все команды, означающие необходимость что-то записать. Это фразы, такие как: "запишите", "запиши", "пишите", "write down", "note", "record", "и так далее".
        2. Сразу после такой команды (или через небольшое пояснение) лектор произносит слово или короткую фразу для записи.
        3. Твоя задача — извлечь ЭТО СЛОВО/ФРАЗУ (которое нужно записать), игнорируя саму команду и все пояснения до следующей команды.
        4. Собери все такие слова/фразы в СПИСОК в точной последовательности, в которой они встречаются в тексте.
        
        ФОРМАТ ВЫВОДА (это важно):
        извлеченная_фраза_1; извлеченная_фраза_2; извлеченная_фраза_3

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
            words = ob.split("; ")
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
