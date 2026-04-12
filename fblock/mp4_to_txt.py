import torch
import gc
from os import listdir
from faster_whisper import WhisperModel

def mp4_to_txt(path, path_save):
    try:
        list_mp3 = []

        for j in listdir(path):
            if "mp3" in j:
                list_mp3.append(j)
        list_mp3 = sorted(list_mp3)

        model = WhisperModel(
                "large-v2,
                device="cuda",
                compute_type="int8_float16",  # экономия VRAM
                cpu_threads=4,                 # опционально, для декодирования на CPU
                num_workers=1                  # сколько потоков загрузки данных
                )

        for j in list_mp3:
            print(f"Начало обработки {f"{path}/{j}"}")
            
            
            segments, info = model.transcribe(
                f"{path}/{j}",
                beam_size=5,                        # чуть выше для качества (было 2)
                temperature=0.0,
                temperature_increment_on_fallback=0.2,
                best_of=5,
                vad_filter=True,
                vad_parameters={
                    "min_silence_duration_ms": 500,
                    "threshold": 0.5,
                    "speech_pad_ms": 400,
                },
                compression_ratio_threshold=2.0,
                log_prob_threshold=-1.0,
                no_speech_threshold=0.6,
                initial_prompt="Conversation in English and Russian. Разговор на русском и английском.",
                word_timestamps=False,
            )

            # # Транскрибируем файл (fp16 больше не передаём)
            # segments, info = model.transcribe(
            #     f"{path}/{j}",
            #     beam_size=2,
            #     temperature=0.0,
            #     word_timestamps=False  # этот параметр, кстати, работает
            # )

            full_text = " ".join(segment.text for segment in segments)
            print(full_text)
            with open(f"{path_save}/res.txt", "a", encoding='utf-8') as file:
                file.write(full_text + "\n")

            # 3. Принудительная очистка GPU (обязательно!)

            print(f"Конец обработки {path}{j}")

        del model                     # удаляем объект модели
        gc.collect()                  # собираем мусор Python
        torch.cuda.empty_cache()      # очищаем кэш аллокатора PyTorch

    except Exception as e:
        print(f"Ошибка на этапе расспознования аудио:\n{e}\n")
        print(path)
        return False
    return True