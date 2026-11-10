def identifySentence(sentence):
    
    return

def englishWords():
    f = open("documents/englishWordsFormatted.txt", "r", encoding="utf-8").read()
    f = f.split("\n")
    englishWords = {}
    for line in f:
        s = line.split("(")
        englishWords[s[0][:-1]] = s[1][:s[1].index(")")]
    return englishWords

words = englishWords()

def unconjugate(verb):
    irregularPastSimple = {}
    irregularPastParticiple = {}
    f = open("documents/irregularPastVerbs.txt", "r", encoding="utf-8").read()
    f = f.split("\n")
    for line in f:
        s = line.split("\t")
        if "/" in s[1]:
            s1s = s[1].split("/")
            for v in s1s:
                irregularPastSimple[v] = s[0]
        else:
            irregularPastSimple[s[1]] = s[0]
        if "/" in s[2]:
            s2s = s[2].split("/")
            for v in s2s:
                irregularPastParticiple[v] = s[0]
        else:
            irregularPastParticiple[s[2]] = s[0]
    modal = ["will", "may", "can", "shall", "must", "ought", "do", "need", "dare", "had better", "used"]
    # [I, you/we/they, he/she, infinative]
    irregularPresent = {
        "am": ["be", "1st sing", "Present"],
        "are": ["be", "", "Present"],
        "is": ["be", "3rd sing", "Present"],
        "do": ["do", "", "Present"],
        "does": ["do", "3rd sing", "Present"],
        "have": ["have", "", "Present"],
        "has": ["have", "3rd sing", "Present"]
    }

    if verb in modal:
        return [verb, "", ""]
    if verb in irregularPresent:
        return irregularPresent[verb]
    if verb in irregularPastSimple and verb in irregularPastParticiple:
        return [irregularPastSimple[verb], "", "Past"]
    if verb in irregularPastSimple:
        return [irregularPastSimple[verb], "", "Past Simple"]
    if verb in irregularPastParticiple:
        return [irregularPastParticiple[verb], "", "Past Participle"]
    if verb in words or "to " + verb in words:
        return [verb, "", "Present Simple"]
    if verb[-1] == "s" and verb[:-1] in words or "to " + verb[:-1] in words:
        return [verb[:-1], "3rd sing", "Present Simple"]
    if verb[-2:] == "ed" and verb[:-2] in words or "to " + verb[:-2] in words:
        return [verb[:-2], "", "Past Simple"]

    return ["", "", ""]

    
    contractable = {
        "m": ["am"],
        "re": ["are"],
        "ve":["have"],
        "d": ["did", "would"],
        "ll": ["will", "shall"]
    }