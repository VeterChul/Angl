import torch
import gc
from os import listdir

def mp4_to_txt(path, path_save, model):
    try:
        list_mp3 = []

        for j in listdir(path):
            if "mp3" in j:
                list_mp3.append(j)
        list_mp3 = sorted(list_mp3)
        print(list_mp3)
        for j in list_mp3:
            print(f"Начало обработки {f"{path}{j}"}")
            
            res = model.transcribe(
                f"{path}{j}",
                fp16=True,  # Используем половинную точность
                word_timestamps=False,  # Отключаем временные метки слов
                best_of=2,  # Уменьшаем
                beam_size=2,  # Уменьшаем
                temperature=0.0
            )
            
            #res = j
            
            with open(f"{path_save}res.txt", "a", encoding='utf-8') as file:
                file.write(res["text"] + "\n")
            
            torch.cuda.empty_cache()
            gc.collect()

            print(f"Конец обработки {path}{j}")
    except Exception as e:
        print(f"Ошибка на этапе расспознования аудио:\n{e}\n")
        print(path)
        return False
    return True