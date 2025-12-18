import os # доступ к работе с операционной системой

def read_text_file(filepath):
    """
    Читает содержимое текстового файла.

    Args:
        filepath (str): Путь к файлу

    Returns:
        str: Содержимое файла или сообщение об ошибке
    """
    try: # попытка кода, в котором может возникнуть ошибка
        with open(filepath, 'r', encoding='utf-8') as f:   # - as f: создание файлового объекта с именем f; with гарантирует закрытие файла при ошибке
            content = f.read()  
        return content
    except FileNotFoundError:
        return "Ошибка: Файл не найден"
    except UnicodeDecodeError:
        return "Ошибка: Неверная кодировка файла"
    
def read_csv_file(filepath):
    """
    Читает содержимое CSV-файла и возвращает список словарей.

    Args:
        filepath (str): Путь к CSV-файлу

    Returns:
        list: Список словарей с данными
    """
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines() # Возвращает список строк, где каждая строка — элемент списка
            if not lines:
                return data
            headers = lines[0].strip().split(',')
            for line in lines[1:]:
                values = line.strip().split(',')
                row = {}
                for i in range(len(values)):
                    row[headers[i]] = values[i] 
                data.append(row)
                   # - headers[i] берет i-й элемент из списка заголовков (ключ для словаря)
    # - values[i] берет i-й элемент из списка значений (значение для словаря)
    # - Результат: создается пара ключ-значение в словаре row
        return data
    except FileNotFoundError:
        print(f"Ошибка: файл {filepath} не найден")
        return data
    except Exception as e:
        print(f"Ошибка при чтении {filepath}: {e}")
        return data
    
def write_csv_file(filepath, headers, data):
    """
    Записывает данные в CSV-файл.

    Args:
        filepath (str): Путь к результатному CSV-файлу
        headers (list): Список заголовков столбцов
        data (list): Список строк данных
    """
    folder = os.path.dirname(filepath)
    # Извлекает путь к директории (папке) из полного пути к файлу
# и сохраняет его в переменную 'folder'
    os.makedirs(folder, exist_ok=True)  # Создаём папку, если её нет; Если True: не вызывает ошибку, если директория уже существует
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(','.join(headers) + '\n') # Записывает заголовки в файл в формате CSV (значения, разделенные запятыми)
            for row in data:
                file.write(','.join(str(v) for v in row) + '\n') # Для каждого элемента v в текущей строке row преобразует его в строку
        return True
    except Exception as e:
        print(f"Ошибка при записи {filepath}: {e}")
        return False
    
def get_files_in_folder(folder_path, extension):
    """
    Возвращает список файлов с указанным расширением из папки.

    Args:
        folder_path (str): Путь к папке
        extension (str): Например, '.txt'

    Returns:
        list: Список имён файлов
    """
    files = []
    for filename in os.listdir(folder_path): # os.listdir возвращает список имен всех файлов и поддиректорий в этой директории
        if filename.endswith(extension) and os.path.isfile(os.path.join(folder_path, filename)): # Объединяет путь к папке и имя файла в полный путь; # Функция проверяет, существует ли путь и является ли он обычным файлом
            files.append(filename)
    return files

def write_text_file(filepath, text):
    """
    Создаёт текстовый файл и записывает в него строку или несколько строк.

    Args:
        filepath (str): Путь и имя файла для записи.
        text (str): Текст для записи. 

    Returns:
        bool: True, если запись прошла успешно, иначе False.
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            if isinstance(text, list): # Проверяет, является ли переменная 'text' списком (list); список - ["hello", "world"]
                for line in text: # для строки в тексте 
                    file.write(line + '\n')
            else: # если текст строка
                file.write(text)
        return True # завершает выполнение функции и возвращает управление вызывающему коду, возвращает значение True —  индикатор успешного выполнения
    except Exception as e:
        print(f"Ошибка при записи файла {filepath}: {e}")
        return False
    
def count_texts(filepath):
    """
    Считает количество файлов формата .txt в заданной папке

    Args:
        filepath (str): путь к папке.

    Returns: 
        int: количество файлов в заданной папке.
        
    """
    count = 0
    for filename in os.listdir(filepath):
        # Полный путь к файлу
        filepath = os.path.join(filepath, filename)
        # Проверяем, что это файл и имеет расширение .txt
        if os.path.isfile(filepath) and filename.lower().endswith('.txt'):
            count += 1
    
    return count



