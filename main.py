import os
import csv
from file_utils import get_files_in_folder, read_text_file, write_csv_file, read_csv_file
from text_utils import count_words, count_unique_words, count_lines, get_most_common_words, calculate_ttr

def analyze_text_file(filepath):
    """
    Анализирует один текстовый файл и выводит статистику.

    Args:
        filepath (str): Путь к текстовому файлу 
    """
    print("=" * 70)
    print(f"📊 Анализ файла: {os.path.basename(filepath)}") 
    print("=" * 70)
    text = read_text_file(filepath)

    word_count = count_words(text)
    words_ucount = count_unique_words(text)
    lines_count = count_lines(text)
    ttr_count = calculate_ttr(text)

    print(f"Количество слов: {word_count}")
    print(f"Количество уникальных слов: {words_ucount}")
    print(f"Количество строк: {lines_count}")
    print(f"Коэффициент тип-токен (TTR): {round(ttr_count, 3)}")

    top_words = get_most_common_words(text)
    print(f"\nНаиболее употребляемые слова: {top_words}")

def analyze_corpus(corpus_folder):
    """
    Анализирует все тексты в папке, сохраняет результаты и выводит статистику.

    Args:
        corpus_folder (str): Путь к папке с текстами 
    """
    print("=" * 70)
    print("📊 Анализ корпуса текстов")
    print("=" * 70)

    # 1. Получаем список всех текстовых файлов из папки
    files = get_files_in_folder(corpus_folder, '.txt')
    
    # Создаём пустой список для результата анализа
    data = []
    all_text = ""

    # 2. Проходим по каждому файлу из списка
    for filename in files:
        # Строим полный путь к файлу
        filepath = os.path.join(corpus_folder, filename)
        # Читаем текст из файла
        text = read_text_file(filepath)
        all_text += text + " "     # Добавляем к общему тексту с разделителем
        # Считаем сколько слов в тексте
        word_count = count_words(text)
        words_ucount = count_unique_words(text)
        lines_count = count_lines(text)
        ttr_count = calculate_ttr(text)
        data.append([filename, word_count, words_ucount, lines_count, ttr_count])
    
    # 3. Сохраняем результаты в CSV файл
    results_folder = 'results'
    # Создаём папку results, если её нет
    os.makedirs(results_folder, exist_ok=True)
    
    csv_file_path = os.path.join(results_folder, 'statistics.csv')
    write_csv_file(csv_file_path, 
                   ['filename', 'word_count', 'words_ucount', 'lines_count', 'ttr_count'], 
                   data)

    print(f"\n✓ Проанализировано файлов: {len(data)}")
    print(f"✓ Результаты сохранены в {csv_file_path}")

    # 4. Загружаем результаты из CSV файла
    stats = read_csv_file(csv_file_path)

    print("\n📖 Статистика по файлам:\n")

    # 5. Выводим имя каждого файла и количество слов
    total_words = 0  # переменная для хранения суммы всех слов
    for i, row in enumerate(stats, start=1):
        # Получаем имя файла и количество слов (строка → число)
        filename = row['filename']
        word_count = int(row['word_count'])
        words_ucount = int(row['words_ucount'])
        lines_count = int(row['lines_count'])
        ttr_count = round(float(row['ttr_count']), 3)
        print(f"{i}. {filename}: {word_count}, {words_ucount}, {lines_count}, {ttr_count}")
        total_words += word_count

    # 6. Выводим общую статистику: всего слов и среднее на файл
    print("\n📈 Общая статистика:")
    print(f"   Всего текстов в корпусе: {len(files)}")
    print(f"   Всего слов в корпусе: {total_words}")
    # Чтобы найти среднее количество слов — делим на число файлов
    if len(stats) > 0:
        average = total_words // len(stats)
    else:
        average = 0
    print(f"   Среднее количество слов: {average}")
    top_words = get_most_common_words(all_text)
    print(f"\nНаиболее употребляемые слова во всём корпусе: {top_words}")
    
    return csv_file_path  # Возвращаем путь к CSV файлу

def load_csv_data(filepath):
    """
    Загружает данные из CSV файла.
    
    Args:
        filepath (str): Путь к CSV файлу
        
    Returns:
        list: Список словарей с данными
    """
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data
    except FileNotFoundError:
        print(f"✗ Файл не найден: {filepath}")
        return []
    except Exception as e:
        print(f"✗ Ошибка при загрузке {filepath}: {e}")
        return []

def prepare_results_for_report(csv_filepath):
    """
    Преобразует данные из statistics.csv в формат для generate_report.
    
    Args:
        csv_filepath (str): Путь к statistics.csv
        
    Returns:
        list: Данные в правильном формате
    """
    raw_data = load_csv_data(csv_filepath)
    if not raw_data:
        return []
    
    results = []
    for row in raw_data:
        # Преобразуем данные из CSV в формат для отчета
        result = {
            'filename': row.get('filename', ''),
            'word_count': int(row.get('word_count', 0)),
            'words_ucount': int(row.get('words_ucount', 0)),  # Оставляем как есть
            'ttr_count': float(row.get('ttr_count', 0.0)),    # Оставляем как есть
            'lines_count': int(row.get('lines_count', 0))     # Добавляем если нужно
        }
        results.append(result)
    
    return results

def generate_report(results, metadata):
    """
    Генерирует текстовый отчёт с объединением данных анализа и метаданных.

    Args:
        results (list): Список словарей с результатами анализа
                       (должен содержать ключи: filename, word_count, words_ucount, ttr_count)
        metadata (list): Список словарей с метаданными о текстах

    Returns:
        str: Текстовый отчёт
    """
    # Проверяем, есть ли данные
    if not results:
        return "Ошибка: Нет данных для генерации отчета."
    
    # Создаём словарь метаданных для быстрого поиска по имени файла
    metadata_map = {}
    if metadata:
        try:
            for item in metadata:
                if 'filename' in item:
                    metadata_map[item['filename']] = item
        except Exception as e:
            print(f"Внимание: Ошибка при обработке метаданных: {e}")

    # Начинаем составлять отчёт
    report_lines = []
    report_lines.append("=" * 70)
    report_lines.append("📊 ОТЧЁТ ПО АНАЛИЗУ КОРПУСА ТЕКСТОВ")
    report_lines.append("=" * 70)

    # ========== ОБЩАЯ СТАТИСТИКА ==========
    report_lines.append("\n📈 ОБЩАЯ СТАТИСТИКА:")
    report_lines.append("-" * 70)

    # Считаем общие метрики
    total_files = len(results)
    total_words = sum(r.get('word_count', 0) for r in results)
    total_unique = sum(r.get('words_ucount', 0) for r in results)  # Используем words_ucount
    avg_ttr = sum(r.get('ttr_count', 0) for r in results) / len(results) if results else 0  # Используем ttr_count

    report_lines.append(f"  Всего текстов в корпусе: {total_files}")
    report_lines.append(f"  Всего слов: {total_words}")
    report_lines.append(f"  Всего уникальных слов: {total_unique}")
    report_lines.append(f"  Средний Type-Token Ratio (TTR): {round(avg_ttr, 3)}")

    # ========== ДЕТАЛЬНАЯ СТАТИСТИКА ==========
    report_lines.append("\n📄 ДЕТАЛЬНАЯ СТАТИСТИКА ПО ФАЙЛАМ:")
    report_lines.append("-" * 70)

    for i, result in enumerate(results, start=1):
        filename = result.get('filename', f'Файл_{i}')
        meta = metadata_map.get(filename, {})

        report_lines.append(f"\n{i}. {filename}")
        report_lines.append(f"   Название: {meta.get('title', 'Неизвестно')}")
        report_lines.append(f"   Автор: {meta.get('author', 'Неизвестен')}")
        report_lines.append(f"   Год: {meta.get('year', 'N/A')}")
        report_lines.append(f"   Слов: {result.get('word_count', 'N/A')}")
        report_lines.append(f"   Уникальных слов: {result.get('words_ucount', 'N/A')}")  # Используем words_ucount
        report_lines.append(f"   TTR: {result.get('ttr_count', 0):.3f}")  # Используем ttr_count и форматируем

    # ========== ВЫВОДЫ ==========
    report_lines.append("\n" + "=" * 70)
    report_lines.append("📌 ВЫВОДЫ И ИНТЕРПРЕТАЦИЯ:")
    report_lines.append("=" * 70)

    if results:
        # Находим текст с максимальным TTR (лексическое разнообразие)
        max_ttr_result = max(results, key=lambda x: x.get('ttr_count', 0))  # Используем ttr_count
        min_ttr_result = min(results, key=lambda x: x.get('ttr_count', 0))  # Используем ttr_count

        report_lines.append(f"\n1. Лексическое разнообразие:")
        report_lines.append(
            f"   • Максимальное разнообразие: {max_ttr_result.get('filename', 'N/A')} "
            f"(TTR = {max_ttr_result.get('ttr_count', 0):.3f})"  # Используем ttr_count
        )
        report_lines.append(
            f"   • Минимальное разнообразие: {min_ttr_result.get('filename', 'N/A')} "
            f"(TTR = {min_ttr_result.get('ttr_count', 0):.3f})"  # Используем ttr_count
        )

    report_lines.append(f"\n2. Общие наблюдения:")
    report_lines.append(
        f"   • Средний TTR всего корпуса составляет {round(avg_ttr, 3)}, "
        f"что указывает на {'высокое' if avg_ttr > 0.6 else 'среднее' if avg_ttr > 0.4 else 'низкое'} "
        f"лексическое разнообразие текстов."
    )
    report_lines.append(
        f"   • Всего в корпусе проанализировано {total_words} слов "
        f"и найдено {total_unique} уникальных слов."
    )

    # Объединяем всё в один текст
    return "\n".join(report_lines)

def get_report():
    """
    Основная функция для генерации и сохранения отчета.
    Загружает данные из файлов и сохраняет отчет в results/report.txt
    """
    
    # 1. Подготавливаем данные для отчета
    results_data = prepare_results_for_report('results/statistics.csv')
    
    if not results_data:
        print("✗ Не удалось загрузить данные статистики")
        return
    
    # 2. Загружаем метаданные
    metadata_path = 'data/metadata.csv'
    metadata_data = load_csv_data(metadata_path)
    
    if not metadata_data:
        print("⚠ Метаданные не загружены, отчет будет без дополнительной информации")
    
    # 3. Генерируем отчет
    report_text = generate_report(results_data, metadata_data)
    
    # 4. Сохраняем отчет в файл
    report_path = 'results/report.txt'
    try:
        # Убедимся, что папка results существует
        os.makedirs('results', exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_text)   
        print(f"✅ Отчет сохранен в {report_path}")
        
    except Exception as e:
        print(f"✗ Ошибка при сохранении отчета: {e}")

if __name__ == '__main__':
    # Пример использования:
    
    # 1. Анализ одного файла (опционально)
    # filepath = "corpus/poem_01.txt"  
    # analyze_text_file(filepath)
    # print("\n" + "=" * 70 + "\n")
    
    # 2. Анализ всего корпуса
    stats_file = analyze_corpus('corpus')
    
    print("\n" + "=" * 70 + "\n")
    
    # 3. Генерация отчета
    get_report()