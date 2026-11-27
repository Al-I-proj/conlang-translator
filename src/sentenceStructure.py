import baseFunctions

class wordInfo:
    def __init__(self, base, wt = [], agreement = {}, wt_variant = {}):
        self.base = base
        self.wt = wt
        self.agreement = agreement
        self.wt_variant = wt_variant

    def __eq__(self, other):
        same = True
        if type(other) != wordInfo:
            return False
        
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
            s += ")}>"
        return s

    def __repr__(self):
        return str(self)

    def addWT(self, wt):
        self.wt += [wt]

    def addAgreement(self, wt, agreement):
        if wt in self.agreement:
            self.agreement[wt] += [agreement]
        else:
            self.agreement[wt] = [agreement]

    def addWTVariant(self, wt, wtVariant):
        if wt in self.wt_variant:
            self.wt_variant[wt] += [wtVariant]
        else:
            self.wt_variant[wt] = [wtVariant]

    def addWordVariant(self, wt, agreement, wtVariant):
        if wt not in self.wt:
            self.wt += [wt]
        self.addAgreement(wt, agreement)
        self.addWTVariant(wt, wtVariant)


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
    "am": wordInfo("be", ["verbs"], {"verbs":["1st sing"]}, {"verbs":["Present"]}),
    "are": wordInfo("be", ["verbs"], {"verbs":["2nd sing", "1st plur", "2nd plur", "3rd plur"]}, {"verbs":["Present"]}),
    "is": wordInfo("be", ["verbs"], {"verbs":["3rd sing"]}, {"verbs":["Present"]}),
    "do": wordInfo("do", ["verbs"], {"verbs":["1st sing", "2nd sing", "1st plur", "2nd plur", "3rd plur"]}, {"verbs":["Present"]}),
    "does": wordInfo("be", ["verbs"], {"verbs":["3rd sing"]}, {"verbs":["Present"]}),
    "have": wordInfo("do", ["verbs"], {"verbs":["1st sing", "2nd sing", "1st plur", "2nd plur", "3rd plur"]}, {"verbs":["Present"]}),
    "has": wordInfo("have", ["verbs"], {"verbs":["3rd sing"]}, {"verbs":["Present"]}),
}
auxilaryVerbs = ["be", "can", "could", "dare", "do", "have", "may",
                 "might", "mote", "must", "need", "ought", "shall",
                 "should", "will", "would"]

irregularPlurals = {"people":"person", "dice":"die", "pence":"penny"}
singIsPlurWords = []

f = open("documents/singIsPlurNouns.txt", "r", encoding = "utf-8").read().split("\n")
for line in f:
    nouns = line.split("\t")
    for noun in nouns:
        singIsPlurWords += [noun.strip()]

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
    for a in range(len(breakdown) - 1):
        i = a + 1
        word = breakdown[i].base
        if word[0] == word[0].upper() and word[-1] != word[-1].upper():
            breakdown[i] = wordInfo(word, ["proper noun"])
    return 

def findBaseWords(breakdown):

    for i in range(len(breakdown)):
        word = breakdown[i].base
        if word not in words[word[0]]:
            nextCheck = True
            if nextCheck:
                if word[:-1] in words[word[0]] and word[-1] == "s":
                    if "nouns" in words[word[0]] or "verbs" in words[word[0]]:
                        breakdown[i].base = word[:-1] 
                        if "nouns" in words[word[0]][word[:-1]]:
                            breakdown[i].wt += "nouns"
                            breakdown[i].agreement["nouns"] = ["plur"]
                        if "verbs" in words[word[0]][word[:-1]]:
                            breakdown[i].wt += "verbs"
                            breakdown[i].agreement["verbs"] = ["3rd sing"]
                        nextCheck = False
            if nextCheck:
                if (word[:-2] in words[word[0]] and 
                    word[-2:] == "es" and (
                    word[-3] in ["s", "z", "x", "o"] or
                    word[-4:-3] in ["ch", "dg", "sh"])):
                    if "nouns" in words[word[0]] or "verbs" in words[word[0]]:
                        breakdown[i].base = word[:-2] 
                        if "nouns" in words[word[0]][word[:-2]]:
                            breakdown[i].wt += "nouns"
                            breakdown[i].agreement["nouns"] = ["plur"]
                        if "verbs" in words[word[0]][word[:-2]]:
                            breakdown[i].wt += "verbs"
                            breakdown[i].agreement["verbs"] = ["3rd sing"]
                        nextCheck = False
            if nextCheck:
                if word[:-3] + "y" in words[word[0]] and word[-3:] == "ies":
                    if "nouns" in words[word[0]][word[:-3] + "y"] or "verbs" in words[word[0]][word[:-3] + "y"]:
                        breakdown[i].base = word[:-1] + "y"
                        if "nouns" in words[word[0]][word[:-3] + "y"] :
                            breakdown[i].wt += "nouns"
                            breakdown[i].agreement["nouns"] = ["plur"]
                        if "verbs" in words[word[0]][word[:-3] + "y"] :
                            breakdown[i].wt += "verbs"
                            breakdown[i].agreement["verbs"] = ["3rd sing"]
                        nextCheck = False


                
                    
    return


def identifySentence(sentence):
    breakdown = contractionsBreakdown(sentence)
    markProperNouns(breakdown)
    
     
    return 

def checkVariations(word):
    s = []
    if word[0] in words:
        letterSection = words[word[0]]
        if word in letterSection:
            if "nouns" in letterSection[word]:
                s += wordInfo(word, ["nouns"])
            for wt in ["verbs", "adverbs", "prepositions", "adjectives", "conjugations", "interjections"]:
                if wt in letterSection[word]:
                    s[-1].wt += [wt]
        if word[-1] == "s" and word[:-1] in letterSection:
            if "n" in letterSection[word[:-1]]:
                if "v" in letterSection[word[:-1]]:
                    s += [wordInfo(word[:-1], ["nouns", "verbs"], {"nouns":["plur"], "verbs":["3rd sing"]}, {"verbs":["present"]})]
                else:
                    s += [wordInfo(word[:-1], ["nouns"], {"nouns":["plur"]})]
            elif "v" in letterSection[word[:-1]]:
                s += [wordInfo(word[:-1], ["verbs"], {"verbs":["3rd sing"]}, {"verbs":["present"]})]
        if len(word) > 2:
            if word[-2:] == "es":
                if word[:-2] in letterSection:
                    s += [wordInfo(word[:-2])]
                    if "n" in letterSection[word[:-2]]:
                        s[-1].wt += ["nouns"]
                        s[-1].agreement["nouns"] = ["plur"]
                    if "v" in letterSection[word[:-2]]:
                        s[-1].wt += ["verbs"]
                        s[-1].agreement["verbs"] = ["3rd sing"]
                        s[-1].wt_variant["verbs"] = ["present"]
                if word[-3] == "i" and word[:-3] + "y" in letterSection:
                    s[0] = word[:-3] + "y"
                    s += wordInfo(word[:-3] + "y")
                    if "n" in letterSection[word]:
                        s[-1].wt += ["nouns"]
                        s[-1].agreement["nouns"] = ["plur"]
                    if "v" in letterSection[word]:
                        s[-1].wt += ["verbs"]
                        s[-1].agreement = ["3rd sing"]
                        s[-1].wt_variant = ["present"]
            s += unconjugate(word)
    return s

def nounVariants(noun):
    if noun[0] not in words:
        return []
    letterSection = words[noun[0]]
    s = []
    if noun in letterSection:
        singIsPlurEndings = ["craft", "fish"]
        singIsPlur = False
        for ending in singIsPlurEndings:
            if len(noun) > len(ending):
                if noun[-len(ending):] == ending:
                    singIsPlur = True
        if noun in singIsPlurWords:
            singIsPlur = True
        if singIsPlur:
            s += [wordInfo(noun, ["nouns"], {"nouns":["sing", "plur"]})]
        elif "nouns" in letterSection[noun]:
            s += [wordInfo(noun, ["nouns"], {"nouns":["sing"]})]
    if noun[-1] == "s":
        if len(noun) > 1:
            if noun[:-1] in letterSection:
                if "nouns" in letterSection[noun[:-1]]:
                    s += [wordInfo(noun[:-1], ["nouns"], {"nouns":"plur"})]
        if len(noun) > 2:
            if noun[-2] == "e":
                if noun[:-2] in letterSection:
                    if "nouns" in letterSection[noun[:-2]]:
                        s += [wordInfo(noun[:-2], ["nouns"], {"nouns":"plur"})]
                if noun[:-2] + "is" in letterSection:
                    if "nouns" in letterSection[noun[:-2] + "is"]:
                        s += [wordInfo(noun[:-2] + "is", ["nouns"], {"nouns":"plur"})]
        if len(noun) > 3:
            if noun[-3:] == "ies":
                if noun[:-3] + "y" in letterSection:
                    if "nouns" in letterSection[noun]:
                        s += [wordInfo(noun[:-3] + "y", ["nouns"], {"nouns":"plur"})]
    if len(noun) > 1:
        if noun[-1] == "i":
            if noun[:-1] + "us" in letterSection:
                if "nouns" in letterSection[noun[:-1] + "us"]:
                    s += [wordInfo(noun[:-1] + "us", ["nouns"], {"nouns":"plur"})]
        if noun[-1] == "a":
            if noun[:-1] + "on" in letterSection:
                if "nouns" in letterSection[noun[:-1] + "on"]:
                    s += [wordInfo(noun[:-1] + "on", ["nouns"], {"nouns":"plur"})]
        if noun[-1] == "i":
            if noun[:-1] + "o" in letterSection:
                if "nouns" in letterSection[noun[:-1] + "o"]:
                    s += [wordInfo(noun[:-1] + "o", ["nouns"], {"nouns":"plur"})]

    if len(noun) > 2:
        if noun[-2:] == "en":
            if noun[:-2] in letterSection:
                if "nouns" in letterSection[noun[:-2]]:
                    s += [wordInfo(noun[:-2], ["nouns"], {"nouns":"plur"})]
            if noun[:-2] + "an" in letterSection:
                if "nouns" in letterSection[noun[:-2] + "an"]:
                    s += [wordInfo(noun[:-2] + "an", ["nouns"], {"nouns":"plur"})]
        if noun[-2:] == "ae":
            if noun[:-1] in letterSection:
                if "nouns" in letterSection[noun[:-1]]:
                    s += [wordInfo(noun[:-1], ["nouns"], {"nouns":"plur"})]
        if noun[-2:] == "im":
            if noun[:-2] in letterSection:
                if "nouns" in letterSection[noun[:-2]]:
                    s += [wordInfo(noun[:-2], ["nouns"], {"nouns":"plur"})]
    if len(noun) > 3:
        if noun[-3:] == "ren":
            if noun[:-3] in letterSection:
                if "nouns" in letterSection[noun]:
                    s += [wordInfo(noun[:-2], ["nouns"], {"nouns":"plur"})]
        if noun[-3:-1] == "ee" and noun[:-3] + "oo" + noun[-1] in letterSection:
            if "nouns" in letterSection[noun[:-3] + "oo" + noun[-1]]:
                s += [wordInfo(noun[:-3] + "oo" + noun[-1], ["nouns"], {"nouns":"plur"})]
        if noun[-3:] == "ice" and noun[:-3] + "ouse" in letterSection:
            if "nouns" in letterSection[noun[:-3] + "ouse"]:
                s += [wordInfo(noun[:-3] + "ouse", ["nouns"], {"nouns":["plur"]})]
        if noun[-3:] == "ata" and noun[:-2] in letterSection:
            if "nouns" in letterSection[noun[:-2]]:
                s += [wordInfo(noun[:-2], ["nouns"], {"nouns":["plur"]})]
        
    if len(noun) > 4:
        if noun[-4:-2] == "ee" and noun[:-4] + "oo" + noun[-2:] in letterSection:
            if "nouns" in letterSection[noun[:-4] + "oo" + noun[-2:]]:
                s += [wordInfo(noun[:-4] + "oo" + noun[-2:], ["nouns"], {"nouns":"plur"})]
        if noun[-4:] == "ices":
            if noun[-3:] + "x" in letterSection:
                if "nouns" in letterSection[noun[:-3] + "x"]:
                    s += [wordInfo(noun[:-3] + "x", ["nouns"], {"nouns":["plur"]})]
            if noun[-4:] + "ex" in letterSection:
                if "nouns" in letterSection[noun[:-4] + "ex"]:
                    s += [wordInfo(noun[:-4] + "ex", ["nouns"], {"nouns":["plur"]})]
        if noun[-4:] == "eaux":
            if noun[:-1] in letterSection:
                if "nouns" in letterSection[noun[:-1]]:
                    s += [wordInfo(noun[:-1], ["nouns"], {"nouns":["plur"]})]

    return s

def unconjugate(verb):
    s = []
    letterSection = words[verb[0]]
    if verb in modal:
        s += [wordInfo(verb, ["verbs"], 
                       {"verbs":["1st sing", "2nd sing", "3rd sing", "1st plur", "2nd plur", "3rd plur"]},
                       {"verbs":["Present"]})]
    if verb in irregularPresent:
        s += [irregularPresent[verb]]
    if verb in irregularPastSimple and verb in irregularPastParticiple:
        s += [wordInfo(verb, ["verbs"], {},
                       {"verbs":["Past Simple", "Past Participle"]})]
    if verb in irregularPastSimple:
        s += [wordInfo(verb, ["verbs"], {},
                       {"verbs":["Past Simple"]})]
    if verb in irregularPastParticiple:
        s += [wordInfo(verb, ["verbs"], {}, 
                       {"verbs":["Past Participle"]})]
    if verb in words or "to " + verb in words:
        if verb not in modal:
            s += [wordInfo(verb, ["verbs"], {}, 
                           {"verbs":["Present Simple"]})]
    if len(verb) > 1:
        if verb[-1] == "s" and verb[:-1] in letterSection:
            s += [wordInfo(verb[:-1], ["verbs"], {"verbs":["3rd sing"]}, {"verbs":["Present"]})]

    if len(verb) > 2:
        if verb[-2:] == "ed" and verb[:-2] in letterSection:
            s += [wordInfo(verb[:-2], ["verbs"], {}, {"verbs":["Past Simple"]})]
    if len(verb) > 3:
        if verb[-3:] == "ies" and verb[:-3] + "y" in letterSection or  "to " + verb[:-3] + "y" in letterSection:
            s += [wordInfo(verb[:-3] + "y", ["verbs"], {"verbs":["3rd sing"]}, {"verbs":["Present"]})]


    return s

def checkWord(word):
    if word[0] not in words:
        print("invalid letters")
    if word in words[word[0]]:
        print(words[word[0]][word])
    else:
        print(word + " is not in words")

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

def testUnconjugate():
    testPhrases = ["am", "looks", "looked"]
    answers = {"am": [wordInfo("be", ["verbs"], {"verbs":["1st sing"]}, {"verbs":["Present"]})],
               "looks": [wordInfo("look", ["verbs"], {"verbs":["3rd sing"]}, {"verbs":["Present"]})],
               "looked": [wordInfo("look", ["verbs"], {}, {"verbs":["Past Simple"]})],
    }
    passed = 0
    failed = 0
    for i in range(len(testPhrases)):
        t = unconjugate(testPhrases[i])
        if t == answers[testPhrases[i]]:
            passed += 1
        else:
            failed += 1
            print("\tTEST: " + testPhrases[i])
            print("\tRESULT: " + str(t))
            print("\tEXPECTED: " + str(answers[testPhrases[i]]))
            print()
    print("PASSED: " + str(passed) + " / " + str(len(testPhrases)))

testUnconjugate()
