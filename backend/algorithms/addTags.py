def addTag(word, tag):
    return f"<{tag}>{word}</{tag}>"


s = 'Here are some words'
indices = [0, 5, 8, ]
tag = "mark"
l = 2

output = []
prev = 0
for i in indices:
    output.append(s[prev:i])
    output.append(addTag(s[i:i+l], tag))
    prev = i+l
output.append(s[prev:])

print(s)
print(''.join(output))
