import json

def stopwords(additional: list = None) -> list:

    with open('./utils/stop_words_english.json', 'rb') as words:
        words = json.load(words)

    if additional:
        words.extend(additional)

    return words