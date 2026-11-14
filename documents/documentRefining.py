def refineVerbs():
    f = open("documents/top-1000-verbs.txt", "r", encoding="utf-8").read()
    s = ""
    f = f.split("\n")
    count = 10
    for line in f:
        l = line.split("\t")
        if count > 0:
            count -=1
            print(l)
        s += l[-1].lower()
        s += "\n"
    t = open("documents/top-1000-verbs2.txt", "w")
    t.write(s)
def refineAdverbs():
    l = []
    f = open("documents/adverbs1.txt", "r", encoding="utf-8").read()
    spl = f.split("\n")
    for line in spl:
        l += [line]
    f = open("documents/adverbs2.txt", "r", encoding="utf-8").read()
    spl = f.split("\n")
    for line in spl:
        spl2 = line.split("\t")
        for adv in spl2:
            a = adv.strip()
            if adv not in l:
                l += [adv]
    f = open("documents/adverbs3.txt", "r", encoding="utf-8").read()
    spl = f.split("\n")
    for line in spl:
        if line not in l:
            l += [line]
    s = ""
    for adv in l:
        s += adv
        s += "\n"
    f2 = open("documents/adverbs.txt", "w").write(s[:-1])
    
def refineAdjectives():
    l = []
    f = open("documents/top-500-adjectives.txt","r",encoding="utf-8").read()
    spl = f.split("\n")
    for line in spl:
        l += [line]
    f = open("documents/adjectives2.txt","r",encoding="utf-8").read()
    spl = f.split("\n")
    for line in spl:
        if line not in l:
            l += [line]
    s = ""
    for adj in l:
        s += adj
        s += "\n"
    w = open("documents/adjectives.txt","w").write(s[:-1])

def refineNouns():
    f = open("documents/nouns2.txt","r",encoding="utf-8").read()
    spl = f.split("\n")
    l = []
    for line in spl:
        l += [line]
    f = open("documents/top-1000-nouns.txt","r",encoding="utf-8").read()
    spl = f.split("\n")
    for line in spl:
        if line not in l:
            l += [line]
    s = ""
    for noun in l:
        for letter in noun:
            if letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-":
                s += letter
        s += "\n"
    s.replace("﻿","")
    open("documents/nouns.txt", "w").write(s[:-1])

refineNouns()