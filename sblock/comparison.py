import eng_to_ipa as ipa
import editdistance

def clean_text(s: str) -> str:
    """Оставляет только буквы (Unicode isalpha), убирая знаки ударения, длины и т.п."""
    return ''.join(c for c in s if c.isalpha())

def match_words_to_transcriptions(words, provided_transcriptions):
    """
    Сопоставляет слова с предоставленными транскрипциями, используя
    сгенерированные IPA и расстояние Левенштейна.
    
    Параметры:
        words (list[str]) – список английских слов.
        provided_transcriptions (list[str]) – список транскрипций (в любом порядке).
        
    Возвращает:
        list[str | None] – для каждого слова наилучшую подходящую транскрипцию
                           из provided_transcriptions или None, если подходящей не нашлось.
    """
    # Предварительно очистим предоставленные транскрипции
    prov_clean = [clean_text(t) for t in provided_transcriptions]
    
    # Список всех возможных назначений (расстояние, индекс слова, индекс предоставленной,
    # оригинал IPA варианта, оригинал предоставленной транскрипции)
    candidates = []
    
    for i, word in enumerate(words):
        # Получаем все варианты IPA для слова
        try:
            ipa_str = ipa.convert(word, keep_punct=False, stress_marks='both')
        except Exception:
            ipa_str = ""  # если библиотека выдаёт ошибку
        
        if not ipa_str:
            # Если транскрипция не получена, попробуем использовать само слово как вариант
            variants = [word]
        else:
            # Разделяем варианты, если их несколько (через запятую)
            variants = [v.strip() for v in ipa_str.split(',') if v.strip()]
        
        # Для каждого варианта IPA
        for variant in variants:
            clean_variant = clean_text(variant)
            # Сравниваем со всеми предоставленными транскрипциями
            for j, prov_orig in enumerate(provided_transcriptions):
                clean_prov = prov_clean[j]
                # Вычисляем расстояние Левенштейна
                dist = editdistance.eval(clean_variant, clean_prov)
                candidates.append((dist, i, j, variant, prov_orig))
    
    # Сортируем кандидатов по расстоянию (от наименьшего)
    candidates.sort(key=lambda x: x[0])
    
    # Жадное назначение
    used_word = [False] * len(words)
    used_prov = [False] * len(provided_transcriptions)
    result = [None] * len(words)
    
    for dist, i, j, _, prov_orig in candidates:
        if not used_word[i] and not used_prov[j]:
            result[i] = prov_orig
            used_word[i] = True
            used_prov[j] = True
    
    res = []
    for w, t in zip(words, result):
        res.append({"w" : w, "t" : t})

    
    return res


# Пример использования
# if __name__ == "__main__":
#     # Исходные данные (слова и транскрипции перемешаны)
#     words = ["hello", "world", "python", "apple", "read"]
#     transcriptions_given = [
#         "wɜːld",
#         "ˈpaɪθɑn",
#         "həˈloʊ",
#         "rid",           # для read (наст. время)
#         "rɛd"            # для read (прош. время) – лишняя, но пусть будет
#     ]
    
#     matched = match_words_to_transcriptions(words, transcriptions_given)
    
#     print(matched)