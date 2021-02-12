import demjson
with open('pokedex.ts') as f:
    file_text = f.read()

file_text = file_text[file_text.find("=")+2:-2]
print(file_text)
parsed_text = demjson.decode(file_text)


with open('ability_lookup.py', 'w') as f:
    for key in parsed_text.keys():
        f.write(key.capitalize() + " = " + str(parsed_text[key]) + "\n")
