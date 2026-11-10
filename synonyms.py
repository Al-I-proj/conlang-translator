def findSynonyms(word, part_of_speech):
    # If  this word is recorded in the thesarus, return the list of synonyms
    f = open("documents/thesarus_dictionary.txt", "r").read()
    f.split("\n")

def multiSplit(text, splitters):
    t = text
    for splitter in splitters:
        t = t.replace(splitter, "[{[*[SPLITTER]*]}]")
    return t.split("[{[*[SPLITTER]*]}]")

def sortOxford():
    f = open("documents/OxfordThesarus.txt", "r", encoding="utf-8").read()
    current_section = "A"
    # starting line = 753
    f = f.split("\n")[753:]

    newText = ""
    for line in f:
        newText += line
        newText += "\n"
    newText = removeTabs(newText)
    labels = ["Colloq", "Slang", "Taboo", "Archaic", "Old-fashioned", "Technical", "Literary"
              "Brit", "US", "Australian", "Canadian", "New Zealand"]
    for label in labels:
        newText = newText.replace(" " + label + " ", " ")
    newText = oneLineEntries(newText)
    # starting line = 116
    #newText = removeExamples(newText)
    newText = removeExamples2(newText)
    newText = removeDividers(newText)
    newText = removeFrontSpace(newText)
    newText = polish(newText)
    f2 = open("documents/newThesarus.txt", "w", encoding="utf-8")
    f2.write(newText)
    print("DONE")

def removeTabs(text):
    newText = ""
    t = text.split("\n")
    for line in t:
        newLine = ""
        if len(line) > 0:
            if line[0] == " ":
                i = 0
                while line[i] == " " and i < len(line):
                    i += 1
                newLine = line[i-1:]
            else:
                newLine = line
        newText += newLine
        newText += "\n"
    return newText[:-1]
                
def oneLineEntries(text):
    newText = ""
    t = text.split("\n")
    for line in t:
        if len(line) == 0:
            newText += "\n"
        else:
            newText += line
    return newText

def removeExamples(text):
    newText = ""
    t = text.split("\n") 
    for line in t:
        num = 1
        defs = multiSplit(line, ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"])
        if type(defs) is str:
            if ":" in defs:
                print(defs)
                newText += "1 " + defs[:defs.index(":")]
            else:
                newText += "1 " + defs
        else:
            newText += defs[0]
            for a in range(len(defs) - 1):
                i = a + 1
                if ":" in defs[i]:
                    newText += str(num) + " " + defs[i][:defs[i].index(":")] + " "
                else:
                    newText += str(num) + " " + defs[i] + " "
                num += 1
        newText += "\n"
        
    return newText[:-1]

def removeExamples2(text):
    newText = ""
    t = text.split("\n") 
    for line in t:
        if ":" in line:
            l = line.split(":")
            newText += l[0]
            for sec in l[1:]:
                i = 0
                while i < len(sec) - 2 and (sec[i] != "." or sec[i+2] not in "123456789"):
                    i += 1
                newText += sec[i + 1:]
        newText += "\n"
    return newText[:-1]

def removeDividers(text):
    newText = ""
    t = text.split("\n")
    for line in t:
        if ".=-=-" not in line:
            if "=-=-" in line:
                newText += line[:line.index("=-=-")]
            else:
                newText += line
            newText += "\n"
        
    return newText[:-1]

def removeFrontSpace(text):
    newText = ""
    t = text.split("\n")
    for line in t:
        if len(line) > 0:
            newText += line.strip()
        newText += "\n"
    return newText[:-1]

def polish(text):
    # - remove blank lines 
    # - standardize format of letters to ***letter
    # - remove multi space gaps

    newText = ""
    t = text.split("\n")
    for line in t:
        if len(line) > 0:
            if line[0] in "1234567890":
                newText += "***" + line[-1]
            else:
                l = line
                for s in ["      ", "     ", "    ", "   ", "  "]:
                    if s in l:
                        l = l.replace(s, " ")
                newText += l
            newText += "\n"
    return newText[:-1]

def newThesarusAsDict():
    f = open("documents/newThesarus.txt", "r", encoding="utf-8").read()
    t = f.split("\n")
    d = {}
    # d[firstLetter][secondLetter][word type][Word] = synonyms
    letter1 = "a"
    letter2 = "a"
    wt = ""
    word = ""
    for line in t:
        if line[0] != "-":
            if len(line) > 3:
                if line[:3] == "***":
                    letter1 = line[-1].lower()
            if len(line) > 1:
                letter2 = line[1]
            if line[0] != "*":
                #Find word type based on the items between the first and second space
                space1 = line.index(" ")
                space2 = line[space1:].index(" ") + space1
                wt = line[space1:space2]
                #Identify the word based on first space
                word = line[:space1]
        else:
            # TODO: Make a system to find word type based on the items immediately following the dashes
            # up to the first space
            ""
            space1 = line.index(" ")
            space2 = line[space1:].index(" ") + space1
            wt = line[2:space1]

        #TODO: Make system to identify different definitions
        
        #TODO: Make system to split up the list of synonyms
        
sortOxford()