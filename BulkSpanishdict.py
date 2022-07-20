import requests

# Set the class name in the HTML
# neodictTranslation--YR6epHeU
# as of 7/18/22
f = open("className.txt", "r")
SPANISHDICT_TRANSLATED_WORD_CLASS = f.read()
f.close()

#.encode('iso-8859-1').decode('utf-8') for strings

class Word:
    def __init__(self, sp = '', en = ''):
        self.en = en.encode('iso-8859-1').decode('utf-8')
        self.sp = sp.encode('iso-8859-1').decode('utf-8')

    def translate(self):
        if (self.en == '' and self.sp == '') or (self.en != '' and self.sp != ''):
            return False
        
        if self.en != '':
            orig = self.en
        elif self.sp != '':
            orig = self.sp
        
        initial = requests.get('https://www.spanishdict.com/translate/'+orig)
        url = initial.url #in case of redirect
        r = requests.get(url)
        r.encoding = r.content
        html = str(r.text.encode('utf-8', 'ignore').decode('utf-8'))
        # print(html)

        translations = []

        cursor = 0
        while len(translations) < 5:
            cursor = html.find(SPANISHDICT_TRANSLATED_WORD_CLASS, cursor)
            if cursor > 0:
                bad_start = html.find('{', cursor) # this will be a css class definition
                start = html.find('>', cursor) # this will be an actual word
                if bad_start < start: # exclude the css
                    cursor = cursor + len(SPANISHDICT_TRANSLATED_WORD_CLASS)
                    continue
                end = html.find('<', cursor)
                translation = html[start+1:end]
                translations.append(translation)
                cursor = end
            else:
                break
        
        if self.en == '':
            self.en = translations
        elif self.sp == '':
            self.sp = translations
    
    def toStrings(self):
        if isinstance(self.en, list):
            self.en = ', '.join(list(set(self.en)))
        if isinstance(self.sp, list):
            self.sp = ', '.join(list(set(self.sp)))
        if self.en == '':
            self.en == '???'
        if self.sp == '':
            self.sp == '???'

    def __str__(self):
        self.toStrings()
        #return self.sp.encode('iso-8859-1').decode('utf-8') + ' - ' + self.en.encode('iso-8859-1').decode('utf-8')
        return self.sp + ' - ' + self.en

class Dictionary:
    def __init__(self, words = []):
        self.words = words
    
    def add(self, word = ''):
        if isinstance(word, Word):
            self.words.append(word)

    def complete(self):
        for word in self.words:
            word = word.translate()

    def __str__(self):
        return '\n\n'.join([str(word) for word in self.words])

def translateList(inText):
    dictionary = Dictionary(words = [])

    for enword in inText.split('\n'):
        word = Word(enword, '')
        word.translate()
        word.toStrings()
        dictionary.add(word)

    return str(dictionary)

def setClassName(name):
    f = open('className.txt', 'w')
    f.write(name)
    f.close()