def multiSplit(text, splitters):
    t = text
    for splitter in splitters:
        t = t.replace(splitter, "[{[*[SPLITTER]*]}]")
    return t.split("[{[*[SPLITTER]*]}]")