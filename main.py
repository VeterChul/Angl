from os import listdir, mkdir
#from fblock.main import main as getting_words_out
from sblock.main import main as transcription

seed = "01"

def main(path, path_save, seed):
    
    #Создаем директорию для данных, если её ещзё нет
    try:
        mkdir(f"{path_save}")
    except FileExistsError:
        print("Директория для сохраненых файлов уже есть")


    for i in sorted(listdir(path)):
        
        if seed[0] != "0":
            pass
            #fblock = getting_words_out(path, path_save, i)
            #if not(fblock):
            #    continue

        if seed[1] != "0":
            for j in listdir(f"{path}/{i}/pdf/"):
                if ".pdf" in j:
                    pdf_file = f"{path}/{i}/pdf/{j}"
                    pdf_save = f"{path_save}/{i}/pdf/{j}".replace(".pdf", ".docx")
                    break
                        
            #Создаем директорию для данных, если её ещзё нет
            try:
                mkdir(f"{path_save}/{i}/pdf/")
            except FileExistsError:
                print("Директория для сохраненых файлов уже есть")

            transcriptions = transcription(pdf_file, pdf_save)
            print(transcriptions)

main("fold", "fold_save", seed)