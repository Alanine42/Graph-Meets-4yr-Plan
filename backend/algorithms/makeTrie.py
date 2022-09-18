# Read in index words. 
# Build a Trie as a nested dictionary  ('#' means end of word)
# Write the Trie as JSON to trie.json

from indexing import *
from collections import deque
import json

index = generateIndex(index, commonWords)
trie = {}

def insert(trie, word):
    node = trie
    for char in word:
        if char not in node:
            node[char] = {}
        node = node[char]
    node['#'] = word    # end of word
    
def contains(trie, word):
    node = trie
    for char in word.lower():
        if char not in node:
            return False
        node = node[char]
    return '#' in node

def hasPrefix(trie, prefix):
    node = trie
    for char in prefix.lower():
        if char not in node:
            return False
        node = node[char]
    return True

def prefixDfs(trie, prefix, limit=float('inf')):
    output = []
    node = trie
    for char in prefix.lower():
        if char not in node:
            return output
        node = node[char]
    
    stack = deque([node])
    while stack:
        node = stack.pop()
        for child in node:
            if child == '#':
                output.append(node['#'])
                if len(output) > limit:
                    return output
            else:
                stack.append(node[child])

    return output

# Main program
for word in index:
    insert(trie, word)
    
print(list( prefixDfs(trie, 's', limit=6)))

print(json.loads(json.dumps(trie)))

outputFile = "trie.json"
with open(outputFile, 'w') as f:
    f.write(json.dumps(trie))
    


# Future Improvements:
# Enable fuzzy search by Levenshtein automata!


