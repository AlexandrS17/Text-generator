import sys
import re
import random
import pymorphy2

KNOWLEDGE = {}


class WordsFill:
    def __init__(self, *text):
        '''
        Инициализируем txt-файл;
        splitим текст на предложения для работы с ними (т.к. в каждом предложении свой смысл);
        также заводим словарь для "обучения"
        '''
        self.morph = pymorphy2.MorphAnalyzer()

        self.text0 = text[0]
        self.knowledge = {}
        self.fit()

    def fit(self):
        global KNOWLEDGE
        '''в строчке значение всегда хранит слова, разделённые Уникальным символом (которого нет в тексте).
        так удобнее'''
        for sentence in self.text0:
            for i, symbol in enumerate(sentence[:-1]):
                self.knowledge[symbol] = self.knowledge.get(symbol, '') + (sentence[i+1] + '|')\
                    if sentence[i+1] not in self.knowledge.get(symbol, '') else self.knowledge.get(symbol)

        KNOWLEDGE = self.knowledge
        return self.knowledge


class WordsGenerate:
    '''подключаем известную из ЯндексЛицея (: библиотеку Pymorphy2 для работы со словами;
       pymorphy пока бесполезна, но с её помощью можно будет(потооом) сделать 
    '''
    def __init__(self, l):
        self.len_sen = l
        self.knowledge = KNOWLEDGE
        super().__init__()

        self.generate()

    def generate(self):
        word = random.choice(list(self.knowledge.keys()))
        line = word[0].upper() + word[1:] + ' '
        
        for _ in range(self.len_sen-1):
            try:
                word = random.choice(self.knowledge[word][:-1].split('|'))
            except KeyError:
                line = line.rstrip() + '. '
                word = random.choice(list(self.knowledge.keys()))
                line += (word[0].upper() + word[1:] + ' ')
            else:
                line += (word + ' ')
        print(line.rstrip() + '.')


file1 = open('Mon1', encoding="utf-8")
file2 = open('Mon2', encoding="utf-8")
file3 = open('AnnaK', encoding="utf-8")


def produce_txt(*f):
    data = []
    for every_f in f:
        txt = every_f.read().strip().split('\n')
        txt = list(map(lambda x: x.lower(), txt))
        txt = [re.findall('\w+', sentence) for sentence in txt]
        data += txt
    return data

# можно убрать из строчки ниже некоторые файлы, можно загрузить и добавить
all_files = WordsFill(produce_txt(file1, file2, file3))

for _ in range(5):
    print("После ввода длины строки Вы увидите гениальное предложение!!")
    print(f'Осталось {5 - _} предложений..\n')
    length = int(input())
    new_sen = WordsGenerate(length)



