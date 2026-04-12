from random import randint
from os import listdir, mkdir
from fblock.main import main as getting_words_out
from sblock.main import main as transcription
from tblock.main import main as essay_f
from importer.main import main as importer

seed = ["010","1","1"]

def main(path, path_save, seed):
    
    #Создаем директорию для данных, если её ещзё нет
    try:
        mkdir(f"{path_save}")
    except FileExistsError:
        print("Директория для сохраненых файлов уже есть")

    for i in sorted(listdir(path)):
        
        if seed[0] != "0":
            if seed[0] == "g":
                fblock = ["Hello", "my", "beloved", "wogit rld"]
            else:
                
                seed1 = [int(i) for i in seed[0]]
                
                
                fblock = getting_words_out(f"{path}/{i}", f"{path_save}/{i}", seed1)
                if not(fblock):
                   continue

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
            

        if seed[2] != "0":
            j = randint(0, len(fblock))
            print(fblock)
            essay = essay_f(fblock[j])
            print(essay)
    
        importer(fblock, transcriptions, essay, f"{path_save}/{i}/ans.pdf")
    
        break

    # print("fbloc")
    # print(fblock)
    # print("transcriptions")
    # print(transcriptions)
    # print("essay")
    # print(essay)
    
        
        

main("fold", "fold_save", seed)