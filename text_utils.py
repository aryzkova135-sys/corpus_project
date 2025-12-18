import os
def count_words(text):
    """
    Подсчитывает количество слов в тексте.

    Args:
        text (str): Текст для анализа

    Returns:
        int: Количество слов
    """
    words = text.split()
    return len(words) 

def count_unique_words (text):
    """
    Ищет в тексте уникальные слова

    Args:
        text(str): Текст для анализа

    Returns:
        int: Количество слов
    """
    words = text.split()
    unique_words= set(words) # Удаляет все дубликаты, оставляя только уникальные элементы
    return len(unique_words) 

def calculate_ttr(text):
    """
    Функция вычисляет отношение уникальных слов ко всем в тексте

    Args:
        text(str):текст для анализа
    Returns:
        float: Числовой коэффициент уникальных слов
    """
    numberofu_words = count_unique_words(text)
    words_count = count_words(text)
    ttr_number = numberofu_words/words_count
    return round(ttr_number, 3)

def count_lines(text):
    """
    Подсчитывает количество строк в тексте 

    Args:
        text(str): Текст для анализа
    
    Returns:
        int: Количество строк
    """
    lines = text.split('\n')
    return (len(lines))

from collections import Counter

from collections import Counter
import re

# Список русских стоп-слов (предлоги, союзы, частицы и т.д.)
STOP_WORDS_RU = {
    'в', 'во', 'на', 'над', 'под', 'к', 'ко', 'от', 'до', 'из', 'со', 'о', 'об', 'обо',
    'у', 'по', 'за', 'про', 'с', 'при', 'между', 'перед', 'через', 'сквозь',
    'без', 'для', 'ради', 'около', 'вокруг', 'после', 'вместо', 'ввиду',
    'благодаря', 'вследствие', 'насчет', 'вроде', 'включая', 'исключая',
    'и', 'а', 'но', 'да', 'или', 'либо', 'то', 'как', 'что', 'чтобы', 'потому',
    'так', 'если', 'хотя', 'когда', 'пока', 'будто', 'словно', 'точно',
    'ли', 'бы', 'же', 'не', 'ни', 'ведь', 'вот', 'мол', 'дескать',
    'я', 'ты', 'он', 'она', 'оно', 'мы', 'вы', 'они', 'себя',
    'мой', 'твой', 'его', 'её', 'наш', 'ваш', 'их',
    'этот', 'тот', 'такой', 'какой', 'чей', 'который',
    'ах', 'ох', 'эй', 'увы', 'вот', 'вон', 'ну'
}

def clean_text_for_analysis(text, remove_punctuation=True, remove_stopwords=True):
    """
    Очищает текст для анализа.
    
    Args:
        text (str): Исходный текст
        remove_punctuation (bool): Удалять знаки препинания
        remove_stopwords (bool): Удалять стоп-слова
    
    Returns:
        str: Очищенный текст
    """
    if remove_punctuation:
        # Удаляем знаки препинания, оставляя буквы, цифры, пробелы и дефис
        text = re.sub(r'[^\w\s-]', ' ', text)
        # Заменяем множественные пробелы на один
        text = re.sub(r'\s+', ' ', text)
    
    words = text.split()
    
    if remove_stopwords:
        # Фильтруем стоп-слова и короткие слова (меньше 2 букв)
        filtered_words = []
        for word in words:
            word_lower = word.lower()
            # Проверяем, не является ли слово стоп-словом и имеет ли достаточную длину
            if (word_lower not in STOP_WORDS_RU and 
                len(word) > 1 and 
                not word.isdigit()):  # Исключаем чисто числовые значения
                filtered_words.append(word)
        words = filtered_words
    
    return ' '.join(words).strip()

def get_most_common_words(text, n=5, cleaned=True, remove_punctuation=True, remove_stopwords=True):
    """
    Функция выводит топ наиболее частых слов с опцией очистки текста.
    
    Args:
        text (str): Текст для анализа
        n (int): Количество слов в топе (по умолчанию 5)
        cleaned (bool): Очищать ли текст перед анализом (по умолчанию True)
        remove_punctuation (bool): Удалять знаки препинания (по умолчанию True)
        remove_stopwords (bool): Удалять стоп-слова (по умолчанию True)
    
    Returns:
        list: Самые популярные слова в употреблении (слово, количество)
    """
    if cleaned:
        text = clean_text_for_analysis(text, remove_punctuation, remove_stopwords)
    
    # Разделяем на слова и приводим к нижнему регистру для корректного подсчета
    words = text.split()
    
    # Дополнительная фильтрация (на случай если cleaned=False)
    if remove_stopwords:
        words = [word.lower() for word in words 
                if word.lower() not in STOP_WORDS_RU and len(word) > 1]
    else:
        words = [word.lower() for word in words if word.strip()]
    
    # Подсчитываем частоту
    text_freq = Counter(words)
    
    return text_freq.most_common(n)

