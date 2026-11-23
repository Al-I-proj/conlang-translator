import requests

def findWord(word):
    url = "https://www.thesaurus.com/browse/" + word
    data = '''{selections:[]
    }'''
    response = requests.post(url, data)
    if len(response.text) > 0:
        t = ""
        l = response.text.split(">")
        for i in range(len(l)):
            entry = l[i][:l[i].find("<")].strip()
            if len(entry) > 0:
                t += entry
                t += "\n"
        if "Jump To" in t:
            t = t[t.find("Jump To:") + 9:]
        else:
            t = t[t.find("Definitions") + 12:]

        open("documents/onlineWord.txt", "w", encoding="utf-8").write(t)
        return t
    return ""

def findWordTypes(wordEntry):
    l = wordEntry.split("\n")
    types = []
    for line in l:
        if line == "n." or line == "NOUN":
            if "nouns" not in types:
                types += ["nouns"]
        elif line == "v." or line == "VERB":
            if "verbs" not in types:
                types += ["verbs"]
        elif line == "adj." or line == "ADJECTIVE":
            if "adjectives" not in types:
                types += ["adjectives"]
        elif line == "adv." or line == "ADVERB":
            if "adverbs" not in types:
                types += ["adverbs"]
        elif line == "CONJUNCTION":
            if "conjunctions" not in types:
                types += ["conjunctions"]
        elif line == "INTERJECTION":
            if "interjections" not in types:
                types += ["interjections"]
        elif line == "ARTICLE":
            if "determiners" not in types:
                types += ["determiners"]
    return types

