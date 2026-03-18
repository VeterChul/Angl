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
        for j in list_mp3:
            print(f"Начало обработки {f"{path}/{j}"}")
            
            # Транскрибируем файл (fp16 больше не передаём)
            segments, info = model.transcribe(
                f"{path}/{j}",
                beam_size=2,
                temperature=0.0,
                word_timestamps=False  # этот параметр, кстати, работает
            )

            full_text = " ".join(segment.text for segment in segments)
            print(full_text)
            with open(f"{path_save}/res.txt", "a", encoding='utf-8') as file:
                file.write(full_text + "\n")
            
            torch.cuda.empty_cache()
            gc.collect()
            
            print(f"Конец обработки {path}{j}")
    except Exception as e:
        print(f"Ошибка на этапе расспознования аудио:\n{e}\n")
        print(path)
        return False
    return True