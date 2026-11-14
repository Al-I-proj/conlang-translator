import baseFunctions

class wordInfo:
    def __init__(self, base, wt = [], agreement = {}, wt_variant = {}):
        self.base = base
        self.wt = wt
        self.agreement = agreement
        self.wt_variant = wt_variant

    def __eq__(self, other):
        same = True
        
        return self.base == other.base and self.wt == other.wt and self.agreement == other.agreement and self.wt_variant == other.wt_variant
    def __str__(self):
        s = "<" + self.base + " : "
        for w in self.wt:
            s += "{" + w + " : (" 
            if w in self.agreement:
                s += str(self.agreement[w]) + ", " 
            else:
                s += "NULL, "
            if w in self.wt_variant:
                s += str(self.wt_variant[w])
            else:
                s += "NULL"
            s += ")}"
        return s
auxVerbs = {
    "will" : "will",

}
irregularPastSimple = {}
irregularPastParticiple = {}
f = open("documents/irregularPastVerbs.txt", "r", encoding="utf-8").read()
f = f.split("\n")
for line in f:
    s = line.split("\t")
    if len(s) == 3:
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
auxilaryVerbs = ["be", "can", "could", "dare", "do", "have", "may",
                 "might", "mote", "must", "need", "ought", "shall",
                 "should", "will", "would"]

def englishWords():
    englishWords = {}
    # "e":{"example": ["noun"]}
    word_types = ["nouns", "verbs", "adjectives", "adverbs"] 
        # + conjugations, prepositions, interjections
    for wt in word_types:
        f = open("documents/" + wt + ".txt", "r", encoding = "utf-8").read()
        l = f.split("\n")
        for line in l:
            if len(line) > 0:
                if line[0] in englishWords:
                    if line in englishWords[line[0]]:
                        englishWords[line[0]][line] += [wt]
                    else:
                        englishWords[line[0]][line] = [wt]
                else:
                    englishWords[line[0]] = {}
                    englishWords[line[0]][line] = [wt]
    return englishWords

words = englishWords()
words["I"] = {"I":"nouns"}

def contractionsBreakdown(sentence):
    s = sentence.split(" ")
    breakdown = [wordInfo("")] * len(s)
    bi = 0
    basicWordInfo = wordInfo("")
    for i in range(len(s)):
        if breakdown[bi] == basicWordInfo:
            if "'" in s[i]:
                if s[i] == "I'm":
                    breakdown[bi] = wordInfo("I", ["nouns"], {"nouns":["sing"]})
                    bi += 1
                    breakdown += [wordInfo("")]
                    breakdown[bi] = wordInfo("be", ["verbs"], {"verbs": ["1st sing"]}, {"verbs":["present simple"]})
                elif s[i][-3:] == "'re":
                    breakdown[bi] = wordInfo(s[i][:-3])
                    bi += 1
                    breakdown += [wordInfo("")]
                    breakdown[bi] = wordInfo("be", ["verbs"],
                                            {"verbs" : ["2nd sing", "1st plur", "2nd plur", "3rd plur"]},
                                            {"verbs" : ["present simple"]})
                elif s[i][-3:] == "'ve":
                    breakdown[bi] = wordInfo(s[i][:-3])
                    bi += 1
                    breakdown += [wordInfo("")]
                    breakdown[bi] = wordInfo("have", ["verbs"], 
                                            {"verbs": ["1st sing", "3rd sing", "1st plur", "2nd plur", "3rd plur"]}, 
                                            {"verbs":["present"]})
                elif s[i][-3:] == "n't":
                    if s[i] == "won't":
                        breakdown[bi] += wordInfo("will", ["verbs"], 
                                                {"verbs":["1st sing", "2nd sing", "3rd sing", "1st plur", "2nd plur", "3rd plur"]}, 
                                                {"verbs":["present"]})
                        bi += 1
                        breakdown += [wordInfo("")]
                        breakdown[bi] = wordInfo("not", ["adverbs"])
                    elif s[i][:-2] in words[s[i][0]]:
                        breakdown[bi] = wordInfo(s[i][:-2])
                        bi += 1
                        breakdown += [wordInfo("")]
                        breakdown[bi] = wordInfo("not", ["adverbs"])

                    else:
                        breakdown[bi] = wordInfo(s[i][:-3])
                        bi += 1
                        breakdown += [wordInfo("")]
                        breakdown[bi] = wordInfo("not", ["adverbs"])
                elif s[i][-3:] == "'ll":
                    breakdown[bi] = wordInfo(s[i][:-3])
                    bi += 1
                    breakdown += [wordInfo("")]
                    breakdown[bi] = wordInfo("will", ["verbs"], 
                                            {"verbs": ["1st sing", "3rd sing", "1st plur", "2nd plur", "3rd plur"]}, 
                                            {"verbs":["present"]})
                elif s[i][-2:] == "'d":
                    if i < len(s) - 1:
                        # would, did, or had
                        nextCheck = True
                        if nextCheck:
                            if s[i + 1] in irregularPastParticiple:
                                    breakdown[bi] = wordInfo(s[i][:-2], ["nouns"], {}, {})
                                    bi += 1
                                    breakdown += [wordInfo("")]
                                    breakdown[bi] = wordInfo("had", ["verbs"], 
                                                            {"verbs":["1st sing", "3rd sing", "1st plur", "2nd plur", "3rd plur"]},
                                                            {"verbs":["past simple"]})
                                    breakdown[bi + 1] = wordInfo(irregularPastParticiple[s[i + 1]], ["verbs"], {}, {"verbs": "past participle"})
                                    nextCheck = False

                        if nextCheck:
                            if s[i + 1][:-1] in words[s[i][0]] and s[i + 1][-1] == "d":
                                if ["verbs"] in words[s[i][0]][s[i + 1][:-3]]:
                                    breakdown[bi] = wordInfo(s[i][:-2], ["nouns"], {}, {})
                                    bi += 1
                                    breakdown += [wordInfo("")]
                                    breakdown[bi] = wordInfo("had", ["verbs"], 
                                                            {"verbs":["1st sing", "3rd sing", "1st plur", "2nd plur", "3rd plur"]},
                                                            {"verbs":["past simple"]})
                                    breakdown[bi + 1] = wordInfo(s[i + 1][:-1], ["verbs"], {}, {"verbs": "past participle"})
                                    nextCheck = False
                                
                        if nextCheck:
                            if s[i + 1][:-4] in words and s[i + 1][-4:-2] == "ed":
                                if "verbs" in words[s[i][0]][s[i + 1][:-4]]:
                                    breakdown[bi] = wordInfo(s[i][:-2], ["nouns"], {}, {})
                                    bi += 1
                                    breakdown += [wordInfo("")]
                                    breakdown[bi] = wordInfo("had", ["verbs"], 
                                                            {"verbs":["1st sing", "3rd sing", "1st plur", "2nd plur", "3rd plur"]},
                                                            {"verbs":["past simple"]})
                                    breakdown[bi + 1] = wordInfo(s[i + 1][:-2], ["verbs"], {}, {"verbs": "past participle"})
                                    nextCheck = False
                        if nextCheck:
                            breakdown[bi] = wordInfo(s[i][:-2])
                            bi += 1
                            breakdown += [wordInfo("")]
                            breakdown[bi] = wordInfo("'d")

                elif s[i][-2:] == "'s" or s[i][-2:] == "s'":
                    # TODO: check 's for possessive vs 's for is
                    breakdown[bi] = wordInfo(s[i][:-2])
                    bi += 1
                    breakdown += [wordInfo("")]
                    breakdown[bi] += wordInfo("'s")
                    
                else:
                    breakdown[bi] = wordInfo(s[i])
            else:
                breakdown[bi] = wordInfo(s[i])
        
        bi += 1
    return breakdown

def markProperNouns(breakdown):
    for i in range(len(breakdown)):
        word = breakdown[i].base
        if word[0] == word[0].upper() and word[-1] != word[-1].upper():
            breakdown[i] = wordInfo(word, ["proper noun"])
    return 



def identifySentence(sentence):
    breakdown = contractionsBreakdown(sentence)
    markProperNouns(breakdown)
    
     
    return 

def checkVariations(word):
    s = [wordInfo("", "", "", "")] 
    if word[0] in words:
        letterSection = words[word[0]]
        if word in letterSection:
            if "nouns" in letterSection:
                s = [word, ["sing"], ["nouns"]]
            for wt in ["verbs", "adverbs", "prepositions", "adjectives", "conjugations", "interjections"]:
                s[1] += [""]
                s[2] += [wt]
        elif word[-1] == "s" and word[:-1] in letterSection:
            if "n" in letterSection:
                if "v" in letterSection:
                    return wordInfo(word[:-2], ["plur", "3rd sing"], ["nouns", "verbs"], ["", "present"])
                else:
                    return wordInfo(word[:-2], ["plur"], ["nouns"], [""])
        elif len(word) > 2:
            if word[-2:] == "es":
                if word[:-2] in letterSection:
                    return [word[:-2], ["plur"], ["n"]]
                if word[-3] == "i" and word[:-3] + "y" in letterSection:
                    s[0] = word[:-3] + "y"
                    if "n" in words[word]:
                        s[1] += ["plur"]
                        s[2] += ["nouns"]
                    if "v" in words[word]:
                        s[1] += ["3rd sing"]
                        s[2] += ["verbs"]
    return s
    

        
    


def unconjugate(verb):
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

def testContrationsBreakdown():
    testPhrases = ["test with no contractions", "can't", "they're", "don't", "I'm", "I'd go", "I'd gone"]
    answers = {"test with no contractions": ["test", "with", "no", "contractions"],
               "can't": ["can", "not"],
        "they're": ["they", "be"],
        "don't":["do", "not"],
        "I'm":["I", "be"],
        "I'd go":["I", "'d", "go"],
        "I'd gone":["I", "had", "go"]
    }
    passed = 0
    failed = 0
    for i in range(len(testPhrases)):
        t = contractionsBreakdown(testPhrases[i])
        result = []
        for j in range(len(answers[testPhrases[i]])):
            if j < len(t):
                result += [t[j].base]
        if result == answers[testPhrases[i]]:
            passed += 1
        else:
            failed += 1
            print("\tTEST: " + testPhrases[i])
            print("\tRESULT: " + str(result))
            print("\tEXPECTED: " + str(answers[testPhrases[i]]))
            print()
    print("PASSED: " + str(passed) + " / " + str(len(testPhrases)))
