import json

emoji_dataset = {}

f = open("emoji_dataset.txt", 'r')
while True:
    line = f.readline()
    if not line: break
    title, emoji = line.split(': ')
    emoji_dataset[emoji[:-1]] = title
f.close()

with open('emoji_dataset.json', 'w', encoding='utf-8') as make_json:
    json.dump(emoji_dataset, make_json, ensure_ascii=False, indent='\t')