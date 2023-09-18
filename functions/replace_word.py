#This function replaces the the old word with the new word in a file
#old = the word we want to be replaced
#new = the new word we want to put where the old word is
#fl = the file we want to modify

def replace_word(old, new, fl):
    with open(fl, "r") as file:
        content = file.read()
        modified_content = content.replace(old, new)
    with open(fl, 'w') as file:
        file.write(modified_content)
