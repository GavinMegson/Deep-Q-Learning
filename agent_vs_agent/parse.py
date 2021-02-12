import demjson
with open('moves.ts') as f:
    file_text = f.read()

file_text = file_text[file_text.find("=")+2:-2]
print(file_text)
parsed_text = demjson.decode(file_text)


with open('moves.py', 'w') as f:
    for key in parsed_text.keys():
        f.write(parsed_text[key]['name'] + " = auto()\n")
