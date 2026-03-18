from random import randint
from os import listdir, mkdir
from faster_whisper import WhisperModel
from fblock.main import main as getting_words_out
from sblock.main import main as transcription
from tblock.main import main as essay_f

seed = ["111","0","1"]

def main(path, path_save, seed):
    
    #Создаем директорию для данных, если её ещзё нет
    try:
        mkdir(f"{path_save}")
    except FileExistsError:
        print("Директория для сохраненых файлов уже есть")

    if not(seed[0] in 'g'):
        model = WhisperModel(
                        "large-v3",
                        device="cuda",
                        compute_type="int8_float16",  # экономия VRAM
                        cpu_threads=4,                 # опционально, для декодирования на CPU
                        num_workers=1                  # сколько потоков загрузки данных
                        )
                    
    for i in sorted(listdir(path)):
        
        if seed[0] != "0":
            if seed[0] == "g":
                fblock = ["Hello", "my", "beloved", "world"]
            else:
                
                seed1 = [int(i) for i in seed[0]]
                
                
                fblock = getting_words_out(f"{path}/{i}", f"{path_save}/{i}", model, seed1)
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
            print(transcriptions)

        if seed[2] != 0:
            i = randint(0, len(fblock))
            essay = essay_f(fblock[i])
            print(essay)
        
        

main("fold", "fold_save", seed)