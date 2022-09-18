from collections import defaultdict, Counter
import string
import json
import os.path
# index in course's cName and cDescription


file = os.path.dirname(__file__)+'/../../mongodb_crawler/courseObjects.json'
index = defaultdict(lambda: defaultdict(lambda: [[],[]]))
# index = {
    # 'data': { 
    #           'CSE 12': [[matches in cName],[matches in cDescription]], 
    #           'DSC 10': [[start_idx],[start_idx1, start_idx2, ..]]
    # }
# }

def cleaned(word: str):
    """Lower all chars and remove all punctuations in the word"""
    return word.translate(str.maketrans('','',string.punctuation)).lower()

# [!] Exclude too common words.  (Inverse frequency?) => Counter of all words => exclude top xx frequent ones? 
commonWords = {'and','of','the','in','to','for','a','with','this','an','may','be','on','as','is','not','by'}

def checkWordFreq():
    wordCounter = Counter()
    with open(file, 'r') as f:
        for line in f:
            courseObject = json.loads(line)
            cName = courseObject['cName'].split()
            cDes = courseObject['cDescription'].split()
            
            wordCounter += Counter((cleaned(word) for word in cName)) + Counter((cleaned(word) for word in cDes))
          
    print(wordCounter.most_common(60)[40:])
    
# checkWordFreq()


def generateIndex(index, commonWords):
    """
    Get each word's occur indices in its cName or cDescription. 
    Clean punctuation in each word before storing it in the index(hashmap)
    """
    with open(file, 'r') as f:
        for line in f:
            courseObject = json.loads(line)
            cID = courseObject['cID']
            
            cName = courseObject['cName']
            prevI = 0
            for word in cName.split():
                i = cName.find(word, prevI)
                index[cleaned(word)][cID][0].append(i)
                prevI = i
            
            cDescription = courseObject['cDescription']
            prevI = 0
            for word in cDescription.split():
                i = cDescription.find(word, prevI)
                if word not in commonWords:
                    index[cleaned(word)][cID][1].append(i)
                prevI = i
    return index

print(os.path.dirname(__file__))
index = generateIndex(index, commonWords)

# filtered = {key:index[key] for key in index if len(index[key]) < 4}
# # print(filtered)
# print('filtered length',len(filtered))
# print(filtered.keys())
# print(sorted(filtered, key=lambda word: len(filtered[word]))[:30])

'''
TODO
[*] Export the index in json
[.] Add weights in courses (in terms of occuring frequency) / let the user decide
whether to sort by frequency, course name, their major, ...

'''

outputFile = "index.json"
with open(outputFile, 'w') as f:
    f.write(json.dumps(index))
    