def format(text):
    lines = text.splitlines()
    print lines
    length = len(lines)
    formatted = []
    i = 0
    while i < length:
        # for i in range(length):
        thisLine = lines[i]
        print(thisLine)
        if i == 0:
            # assume first line is date
            formatted.extend(makeDateLine(thisLine))
            formatted.append("[ul]")
            i = i+1
            continue
        try:
            nextLine = lines[i+1]
        except:
            nextLine = None
        thisLineIndentLevel = indentLevel(thisLine)
        nextLineIndentLevel = indentLevel(nextLine)

        if thisLine.isspace():  # empty line - get ready for a date
            formatted.append("[/ul]")
            while(lines[i].isspace()):
                i = i+1
            # line should be date
            formatted.extend(makeDateLine(lines[i]))
            formatted.append("[ul]")
            i = i+1
            continue

        thisLine = makeLinks(thisLine)
        thisLine = thisLine.strip()
        thisLine = indent(thisLineIndentLevel)+"[li]"+thisLine
        if thisLineIndentLevel == nextLineIndentLevel:  # same list level
            thisLine = thisLine+"[/li]"
            formatted.append(thisLine)
        elif thisLineIndentLevel < nextLineIndentLevel:  # start of deeper list
            formatted.append(thisLine)
            formatted.append(indent(nextLineIndentLevel)+"[ul]")
        else:  # thisLineIndentLevel>nextLineIndentLevel - end of nested list
            thisLine = thisLine+"[/li]"
            formatted.append(thisLine)
            currentNestLevel = thisLineIndentLevel
            while currentNestLevel > nextLineIndentLevel:
                formatted.append(indent(currentNestLevel)+"[/ul]")
                formatted.append(indent(currentNestLevel-1)+"[/li]")
                currentNestLevel = currentNestLevel-1
        i = i+1
    formatted.append("[/ul]")
    lineSep = "\n"
    return lineSep.join(formatted)
    # return {"lines": formatted, "rawText": nlSep.join(formatted)}
    # return formatted


def indentLevel(line):
    if line is None:
        return 0
    if line.isspace():
        return 0
    return line.count('\t')


# assumption: already at zero-indent
# makeDateLine returns a list
def makeDateLine(line):
    formatted = [
        '[b]' + line + '[/b]',
        '[hr]'
    ]
    return formatted


def makeLinks(line):
    return line  # TODO


def indent(indentLevel):
    # what's the efficient way to do this?
    txt = ''
    for i in range(indentLevel):
        txt = txt+"\t"
    return txt
