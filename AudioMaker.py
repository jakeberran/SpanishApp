#make the example fetcher from wiktionary work right...
#find what all the word types in that xml are, pick which ones to throw out

import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import os
import csv
from pydub import AudioSegment
AudioSegment.converter = "C:/ffmpeg"

parent_folder = ''

def num_in_string(strg):
    num = ""
    for c in strg:
        if c.isdigit():
            num = num + c
    if num=='':
        return 99999999
    return int(num)

def proxy():
    url = 'https://httpbin.org/ip'
    proxies = {
    "http": 'http://209.50.52.162:9050', 
    "https": 'http://209.50.52.162:9050'
    }
    response = requests.get(url,proxies=proxies)
    print(response.json())

def lingolex():
    URL = "https://lingolex.com/sp/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser") #.content is the raw bytes

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

def xmlread(spen):
    tree = ET.parse(spen)
    root = tree.getroot()
    #print(root.tag, root.attrib)
    dict_table = [['ES', 'EN', 'DIF', 'EJEMPLO']] #this probably shouldn't be here, idk if it totally matters how fast the program runs
    remove_strings = ['<i>', '</i>', '"']
    replace_with_space = ['  ', '\n']
    for letter in root:
        #print(letter.tag, letter.attrib)
        for word in letter:
            spword = word.find('c').text
            enword = word.find('d').text
            if spword == dict_table[-1][0]:
                dict_table[-1][1].append(enword)
            else:
                dict_table.append([spword, [enword]]) #examples in last
                    
            #if len(dict_table) > 3:
                #print(dict_table)
                #quit()
    return dict_table

    #print(dict_table)

def wikixmlread(filename):
    f = open(filename, 'r')
    text = f.read()
    f.close()
    text2 = text[text.find('<title>aarónico</title>'):]
    return text2

def csvread(filename):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        return list(reader)

def tts(text="", language="es", filename="play"):
    filename = filename.replace('/', '\\')
    if language=="es":
        cfg = '"Microsoft Helena" -v 100 -p 10'
    else:
        cfg = '"Microsoft Zira" -v 90 -s 0 -p 5 -se 3000'
    if filename=="play":
        command = 'cmd /c "balcon -n '+cfg+' -t "'+text+'"'
    else:
        command = 'cmd /c "balcon -n '+cfg+' -t "'+text+'" -w "'+filename+'"'
    os.system(command)
    #print(command)

#working on this 9/12
def concatenate(folder, target, delete=False):
    try:
        os.remove(folder+'/filelist.txt')
    except:
        pass
    filelist = os.listdir(folder) #puts in number order
    filelist.sort(key = lambda x: num_in_string(x))
    #print(filelist)
    textfile = folder+'/filelist.txt'
    textfileb = '"'+textfile.replace("/","\\")+'"' #need backslash for win commands
    targetb = '"'+target.replace('/', '\\')+'"'
    folder = folder.replace('/', '\\')
    strg = ''
    for file in filelist:
        strg += "file '" + folder + '\\' +  file + "'\n"
    print(strg)
    t = open(textfile, 'w+')
    t.write(strg)
    t.close()
    #os.system('cmd /k cd '+folder)
    print(folder+'\\filelist.txt')
    os.system('cmd /c ffmpeg -y -f concat -safe 0 -i '+textfileb+' -c copy '+targetb[:-4]+'wav"')
    if targetb[-4:]=='mp3"':
        os.system('cmd /c ffmpeg -y -i '+targetb[:-4]+'wav"'+' -vn -ar 44100 -ac 2 -b:a 128k '+targetb)
        os.remove(target[:-3]+'wav') #just leave the mp3
    os.remove(textfile)
    if delete:
        for filename in filelist:
            os.remove(folder+'/'+filename)

def shorten():
    f = open(parent_folder + "eswiktionary-20210901-pages-meta-current.xml", "r")
    n = ''
    count = 0
    badwords = ['Plantilla:', 'Apéndice:', 'MediaWiki:', 'iscusiÃ³n:', "Usuario:", "CategorÃ­a:", 'Wikcionario discusión:']
    transdict = {91: None, 93: None}
    while f:
        try:
            l = f.readline()
            if count % 100000 == 0:
                print(count, l)
            count += 1
            
            badline = False
            if len(l) > 500:
                badline = True
                #print('Too long')
                continue #next line
            for word in badwords:
                if word in l:
                    badline = True
                    #print("Bad word")
                    break
            
            if not badline:
                if "<title>" in l:
                    n += l
                    #print(count, l)
                elif "Ejemplos" in l: #cleanup for all of these
                    l2 = f.readline()
                    start = l2.find('&quot;')+6
                    end = l2[start:].find('.')
                    n += l2[start:end]
                    count += 1
                elif "Ejemplo:" in l:
                    start = l.find("Ejemplo:")+8
                    end = l[start:].find('.')
                    n += l[start:end].strip("' ").translate(transdict)
                elif "ejemplo|" in l:
                    start = l.find('ejemplo|')+8
                    end = l[start:].find('.')
                    n += l[start:end].strip("' ").translate(transdict)
            
            
            if count > 30000000:
                break
        except UnicodeDecodeError:
            pass
    f.close()

    f2 = open(parent_folder + "short_wiktionary2.txt", "w")
    f2.write(n)
    f2.close()

def alphabetize():
    f = open(parent_folder + "short_wiktionary2.txt", "r")

    #get into a list
    wiki_pages = [[]]
    index = 0
    while index < 790000:
        if index % 10000 == 0:
            print(index, wiki_pages[index])
        l = f.readline().strip(' \n')
        if l.startswith('<title>'):
            #print(l.strip(' \n')[7:-8])
            wiki_pages.append([l[7:-8]])
            #print(wiki_pages[index])
            index += 1
        else:
            wiki_pages[index].append(l)
    
    totalindex=0
    for index in range(len(wiki_pages)):
        totalindex+=1
        #print("Here now")
        print('2 - '+str(totalindex))
        try:
            while len(wiki_pages[index]) == 1: #remove last one if no example
                del wiki_pages[index]
                totalindex += 1
            while len(wiki_pages[index]) > 2: #ensures there is only one example line
                del wiki_pages[index][2]
        except:
            break

    
    #sort the list
    wiki_pages.sort(key = lambda x: x[0])
    print(wiki_pages[:200])
    return wiki_pages

def winFormat(f):
    return '"'+f+'"'.replace('/', '\\')

def construct_dictionary():
    table = xmlread(parent_folder + "es-en.xml")
    freq_table = csvread(parent_folder + "word_info.csv")
    freq_words = [row[0] for row in freq_table]
    for i in range(1, len(table)):
        word = table[i][0]
        try:
            idx = freq_words.index(word)
        except: #not in the freq table
            continue #stop trying with this word, go to next i
        del freq_table[:idx]
        del freq_words[:idx]
        table[i].append(100 - float(freq_table[0][2]))
        #print(table[i])
    
    i = 0
    for j in range(len(table)): #do j times regardless, if no difficulty then take out
        if len(table[i]) < 3:
            del table[i]
        else:
            i += 1

    #now do the wiktionary
    with open(parent_folder + 'wiki_table.csv', 'r', newline='\n') as f:
        reader = csv.reader(f, lineterminator='\n')

        ex_table = list(reader)
        ex_words = [row[0] for row in ex_table]
    for i in range(1, len(table)):
        word = table[i][0]
        try:
            idx = ex_words.index(word)
        except: #not in the freq table
            continue #stop trying with this word, go to next i
        del ex_table[:idx]
        del ex_words[:idx]
        if i % 100 == 0:
            print(i)
        table[i].append(ex_table[0][1])
        #print(table[i])
        
    print(table[:200])

    del table[0]
    table.sort(key = lambda x: x[2]) #sort by difficulty, i should have definitely used a word class instead of a list
    table.insert(0, ['ES', 'EN', 'DIF', 'EJEMPLO'])
    return table



with open(parent_folder + 'Complete dictionary.csv', 'r', newline='\n') as f:

    reader = csv.reader(f, lineterminator='\n')
    dictionary = list(reader)
    dictionary_length = len(dictionary)
    for i in range(dictionary_length):
        dictionary[i][1] = dictionary[i][1].strip('[]').split(',')
        if len(dictionary[i]) < 4:
            dictionary[i].append('')
    #
    # print(dictionary_length)

def inv_cdf(fraction_below): #enter a percent, it will find the difficulty level where that percent of words are below it
    index = int(fraction_below*dictionary_length)
    return index, dictionary[index]

def train(num_of_words):
    print('Enter if you know, type something and enter if you dont')
    score = 0
    for i in range(num_of_words):
        index = random.randrange(1, dictionary_length)
        word = dictionary[index]
        print(word[0], ":", word[1])
        x = input()
        if x == '':
            score += 1
    score_adjusted = score/num_of_words
    min_index = inv_cdf(score_adjusted)
    print('You should start on #', inv_cdf(score_adjusted))
    return min_index 

#train(50)

def unaccent(sptext):
    changes = 'áéíóúÁÉÍÓÚaeiouAEIOU'
    for i in range(10):
        sptext = sptext.replace(changes[i], changes[i+10])
    return sptext


def make_audio(min_index, num_of_words, filename):
    tts(filename+', empezando con palabra número '+str(min_index)+'. ', 'es', parent_folder + 'Audio/temp/0header.wav')
    #make a table of lines
    for i in range(min_index, min_index+num_of_words):
        sptext = dictionary[i][0] + '. '
        tts(sptext, "es", parent_folder + 'Audio/sub_temp/temp1.wav')
        entext = dictionary[i][1][0] #first definition
        for j in range(1, len(dictionary[i][1])):
            entext += ', or ' + dictionary[i][1][j]
        #print(entext)
        tts(entext, "en", parent_folder + 'Audio/sub_temp/temp2.wav')
        if dictionary[i][3] != '':
            extext = unaccent(dictionary[i][3]) + '. '
            tts(extext, "es", parent_folder + 'Audio/sub_temp/temp3.wav')
        tts(sptext, "es", parent_folder + 'Audio/sub_temp/temp4.wav')

        concatenate(parent_folder + 'Audio/sub_temp', parent_folder + 'Audio/temp/'+str(i)+'.wav', True)
    tts('Fin del archivo, '+filename+'. ', "es", parent_folder + 'Audio/temp/zfooter.wav')
    
    speechaudio = parent_folder + 'Audio/'+filename+'0.mp3'
    concatenate(parent_folder + 'Audio/temp', speechaudio, True)
    background = winFormat(parent_folder + 'Audio/background.mp3')
    output = winFormat(parent_folder + 'Audio/'+filename+'.mp3')
    os.system('cmd /c ffmpeg -y -i '+winFormat(speechaudio)+' -i '+background+' -filter_complex amix=inputs=2:duration=shortest '+output)
    os.remove(speechaudio)

def make_personal_dictionary():
    table = csvread(parent_folder + 'Complete dictionary.csv')
    table2 = []
    for line in table:
        print(line)
        if input() != '':
            table2.append(line)
    writer = csv.writer(parent_folder + 'Personal dictionary.csv')
    writer.writerows(table2)


num_of_files = 10
words_per_file = 50
starting_word_idx = 4952

for i in range(num_of_files):
    make_audio(words_per_file * i + starting_word_idx, words_per_file, 'Práctica '+str(i+1))