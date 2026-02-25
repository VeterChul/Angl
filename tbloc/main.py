import ollama

def main(word):
    EXTRACTION_PROMPT = f"""
        You are a helpful assistant that writes short essays following a strict template. 
        I will give you a word, and you must produce an essay exactly in the format below.

        Template:
        /Favorite Word/Expression:/ {word}
        /The word/expression that I like most from this set is/ {word}
        {word}/ is a/ [choose one: noun / adjective / verb / adverb / phrase / collocation]
        /How do you say it in Russian?/
        /It translates into Russian as/ [Russian translation]
        /What does it mean?/
        /It meanS/ [clear definition of the word]
        /A good synonym for/ '{word}' /is/ [one synonym]
        /The opposite/ of '{word}' /is/ [one antonym]
        /I find this word/ [choose one: inspiring / encouraging / engaging / fascinating]
        /because it reminds me of / [a short personal story (2-3 sentences) related to the word]

        Now write the essay for the word: "{word}"       
    """
    response = ollama.chat(
        model='llama3:8b',          # заменено с qwen2.5:7b на llama3:8b
        messages=[{'role': 'user', 'content': EXTRACTION_PROMPT}],
        options={'temperature': 0.3} # теперь 0.3 для баланса точности и вариативности
    )
    essay_text = response['message']['content']

    return essay_text