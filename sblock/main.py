from sblock.transcription import main as transcription
from sblock.words import convert_pdf_to_docx, find_underlined_text
from sblock.comparison import match_words_to_transcriptions

def main(pdf_file, path_save):
    
    docx_file = convert_pdf_to_docx(pdf_file, path_save)
    words = find_underlined_text(docx_file)

    transcriptions = transcription(pdf_file)

    matched = match_words_to_transcriptions(words, transcriptions)

    return matched
    
        
