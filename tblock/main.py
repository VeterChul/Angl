import ollama

def main(word):

    EXTRACTION_PROMPT = f"""
    You are an AI that writes essays strictly following a template. 
    Your output must start exactly with the chosen first line and contain no other text before it.
    Do not add any introductory phrases, comments, or extra lines.

    Rules:
    - If the input is a single word (like "creativity" or "hello"), use "Word" in the first two lines.
    - If the input is a phrase or collocation (like "break a leg" or "once in a blue moon"), use "Expression" in the first two lines.
    - The rest of the template is the same regardless of the choice.

    Examples:

    Single word: creativity
    /Favorite Word:/ creativity
    /The word that I like most from this set is/ creativity
    creativity/ is a/ noun
    /How do you say it in Russian?/
    /It translates into Russian as/ творчество, креативность
    /What does it mean?/
    /It meanS/ the ability to use imagination to make new things or solve problems.
    /A good synonym for/ 'creativity' /is/ inventiveness
    /The opposite/ of 'creativity' /is/ stereotype
    /I find this word/ inspiring
    /because it reminds me of / the art studio where I used to take painting classes. The studio had tall windows, so we often enjoyed watching beautiful sunsets, which really inspired me and sparked my imagination.

    Single word: hello
    /Favorite Word:/ hello
    /The word that I like most from this set is/ hello
    hello/ is a/ interjection
    /How do you say it in Russian?/
    /It translates into Russian as/ здравствуйте
    /What does it mean?/
    /It meanS/ a greeting used to acknowledge someone's presence or to initiate communication.
    /A good synonym for/ 'hello' /is/ greetings
    /The opposite/ of 'hello' /is/ goodbye
    /I find this word/ engaging
    /because it reminds me of / the morning when I wake up and say hello to my family.

    Phrase example: break a leg
    /Favorite Expression:/ break a leg
    /The expression that I like most from this set is/ break a leg
    break a leg/ is a/ phrase
    /How do you say it in Russian?/
    /It translates into Russian as/ ни пуха ни пера
    /What does it mean?/
    /It meanS/ a way of wishing someone good luck, especially before a performance.
    /A good synonym for/ 'break a leg' /is/ good luck
    /The opposite/ of 'break a leg' /is/ bad luck
    /I find this expression/ encouraging
    /because it reminds me of / my school play when my teacher said it to me right before I went on stage. It made me smile and feel more confident.

    Now write the essay for the input: "{word}". 
    First, decide if it is a single word or a phrase. Then produce the template accordingly.
    Follow these rules exactly:
    - For a single word, first line: /Favorite Word:/ {word}
    - For a phrase, first line: /Favorite Expression:/ {word}
    - Second line: match the choice.
    - Part of speech: choose from [noun, adjective, verb, adverb, phrase, collocation, interjection]. Use the most accurate one.
    - /I find this word/expression/: choose from [inspiring, encouraging, engaging, fascinating]. (Use "word" or "expression" consistently.)
    - Use correct Russian translation.
    - Definition ends with a period.
    - Personal story (2-3 sentences) ends with a period.
    - No other punctuation at line ends.
    - Do not include any extra text before, after, or between lines.

    Output only the filled template.
    """
    
    response = ollama.chat(
        model='llama3:8b',
        messages=[
            {'role': 'system', 'content': 'You are a precise template filler. Output only the filled template with no extra text.'},
            {'role': 'user', 'content': EXTRACTION_PROMPT}
        ],
        options={'temperature': 0.0}
    )

    essay_text = response['message']['content'].replace("/","")

    return essay_text