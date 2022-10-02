# Highlight words starting at specific indices. 

def addTag(word, tag):
    return f"<{tag}>{word}</{tag}>"


s = 'Here are some words, but again. Please'
indices = [s.find(word) for word in ('are', 'words', 'again', 'Please')]
tag = "mark"
l = 2

output = []
prev = 0
for i in indices:
    output.append(s[prev: i])
    nextD = i
    while nextD < len(s) and s[nextD].isalnum():
        nextD += 1
    output.append(addTag(s[i: nextD], tag))
    prev = nextD
output.append(s[prev:])

print(s)
result = ''.join(output)
print(result)


