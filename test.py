import json

s = '''
{
    "words": [
        {
            "english": "convention",
            "russian": "договорённость, традиция",
            "part_of_speech": "noun",
            "transcription": "kənˈvɛnʃən",
            "examples": ["conventions of essay writing", "conventional expression"],
            "context": "Установленные обычаи или договорённость. Синоним к слову традиции.",
            "lesson_part": "основная лексика"
        },
        {
            "english": "conventional",
            "russian": "обычный, традиционный",
            "part_of_speech": "adjective",
            "transcription": "kənˈvɛnʃənl",
            "examples": ["the conventional phrasing", "conventional expression"],
            "context": "The adjective is conventional, which is a synonym for traditional. The adverb is conventionally.",
            "lesson_part": "основная лексика"
        },
        {
            "english": "expression",
            "russian": "выражение",
            "part_of_speech": "noun",
            "transcription": "ɪkˈspres̩ʃn",
            "examples": ["a conventional expression"],
            "context": "A conventional expression. This is a fixed phrase or a set phrase that is traditionally used in a given context.",
            "lesson_part": "основная лексика"
        },
        {
            "english": "introductory",
            "russian": "вводный, вступительный",
            "part_of_speech": "adjective",
            "transcription": "ɪnˈtrədʌktəri',
            "examples": ["the introductory paragraph"],
            "context": "The introductory paragraph is the opening paragraph of your essay.",
            "lesson_part": "основная лексика"
        },
        {
            "english": "paragraph",
            "russian": "параграф, абзац",
            "part_of_speech": "noun",
            "transcription": "ˈpærəɡræf",
            "examples": ["the introductory paragraph"],
            "context": "The introductory paragraph is the opening paragraph of your essay.",
            "lesson_part": "основная лексика"
        },
        {
            "english": "hook",
            "russian": "заковыристая фраза, цепляющая предложение",
            "part_of_speech": "noun",
            "transcription": "hʊk",
            "examples": ["the hook is optional"],
            "context": "The hook is the first sentence of the essay, which introduces the main topic.",
            "lesson_part": "основная лексика"
        }
    ]
}
'''

print(json.loads(s))