from os import listdir, mkdir
import whisper

from fblock.mp4_to_txt import mp4_to_txt
from fblock.txt_to_json import txt_for_json

def main(path, path_save, i):

    r = {}

    model = whisper.load_model("medium", device="cuda")
            
    #Создаем директорию для данных, если её ещзё нет
    try:
        mkdir(f"{path_save}/{i}")
    except FileExistsError:
        print("Директория для сохраненых файлов уже есть")

    #расспознаем аудио в текст, если не сделали этого раньше
    if not("res.txt" in listdir(f"{path_save}/{i}")):     
        if not(mp4_to_txt(f"{path}/{i}/", f"{path_save}/{i}/", model)):
            return False
    
    #Доставание слов из расшифровки 
    if not(f"list_slov.txt" in listdir(f"{path_save}/{i}")):
        print("Запущена неиросеть для доставания слов из расшифровки")
        list_json, flag = txt_for_json(f"{path_save}/{i}/")
        if not(flag):
            return False
        with open(f"{path_save}/{i}/list_slov.txt", "w", encoding="utf-8") as file:
            file.write(list_json)
    else:            
        print("Использование раньше расспознаных слов")
        try:
            with open(f"{path_save}/{i}/list_slov.txt", 'r', encoding='utf-8') as f:
                exec(f"list_json = {f.read()}")
            
        except FileNotFoundError:
            print(f"❌ Файл {path_save}/{i}/slov.json не найден")
        except  Exception as e:
            print(f"Ошибка при доставании слов {e}")
    
    r[f"{path}/{i}/"] = list_json

    return r
    
        
    

