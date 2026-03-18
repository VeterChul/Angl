from os import listdir, mkdir, remove

from fblock.mp4_to_txt import mp4_to_txt
from fblock.txt_to_json import txt_for_json

def main(path, path_save, model, seed):

    r = {}
            
    #Создаем директорию для данных, если её ещзё нет
    try:
        mkdir(path_save)
    except FileExistsError:
        print("Директория для сохраненых файлов уже есть")

    if seed[0]:     
        if seed[2]:
            remove(f"{path_save}/res.txt")
        if not(mp4_to_txt(path, path_save, model)):
            return False      

    #Доставание слов из расшифровки 
    if seed[1]:
        print("Запущена неиросеть для доставания слов из расшифровки")
        list_json, flag = txt_for_json(path_save)
        if not(flag):
            return False
        with open(f"{path_save}/list_slov.txt", "w", encoding="utf-8") as file:
            file.write(list_json)
    else:            
        print("Использование раньше расспознаных слов")
        try:
            with open(f"{path_save}/list_slov.txt", 'r', encoding='utf-8') as f:
                exec(f"list_json = {f.read()}")
            
        except FileNotFoundError:
            print(f"❌ Файл {path_save}/slov.json не найден")
        except  Exception as e:
            print(f"Ошибка при доставании слов {e}")
    
    for i in list_json:
        r.append(i)

    return r
    
        
    

