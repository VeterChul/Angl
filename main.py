from os import listdir

from mp4_to_txt import mp4_to_txt
from txt_to_json import txt_for_json

list_folder = [f"fold/{i}/" for i in listdir("fold")]

for i in list_folder:
    #расспознаем аудио в текст, если не сделали этого раньше
    if not("res.txt" in listdir(i)):     
        if not(mp4_to_txt(i)):
            continue
    
    #Доставание слов из расшифровки 
    if not(f"list_slov.txt" in listdir(i)):
        print("Запущена неиросеть для доставания слов из расшифровки")
        list_json, flag = txt_for_json(i)
        if not(flag):
            continue
        with open(f"{i}list_slov.txt", "w", encoding="utf-8") as file:
            file.write(list_json)
    else:            
        print("Использование раньше расспознаных слов")
        try:
            with open(f"{i}list_slov.txt", 'r', encoding='utf-8') as f:
                exec(f"list_json = {f.read()}")
            
        except FileNotFoundError:
            print(f"❌ Файл {i}slov.json не найден")
        except  Exception as e:
            print(f"Ошибка при доставании слов {e}")
    

