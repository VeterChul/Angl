import whisper

def mp4_to_txt(i):
    try:
        for j in listdir(i):
            print(f"Начало обработки {f"{i}{j}"}")
            model = whisper.load_model("medium")
            res = model.transcribe(f"{i}{j}",task="transcribe")["text"]
            #res = j
            with open(f"{i}res.txt", "a", encoding='utf-8') as file:
                file.write(res + "\n")

            print(f"Конец обработки {i}{j}")
            return True
    except Exception as e:
        print(f"Ошибка на этапе расспознования аудио:{e}")
        print({i})
        return False