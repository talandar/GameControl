linkMap = {}


def format(text):
    initLinks()
    lines = text.splitlines()
    length = len(lines)
    formatted = []
    i = 0
    while i < length:
        # for i in range(length):
        thisLine = lines[i]
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
    for key in linkMap:
        if line.find(key) >= 0:
            line = line.replace(key, "@["+key+"]"+linkMap[key], 1)
    return line


def indent(indentLevel):
    # what's the efficient way to do this?
    txt = ''
    for i in range(indentLevel):
        txt = txt+"\t"
    return txt


def addLinkEntry(tag, *args):
    thisMap = {}
    name = tag[2:tag.index(']')]
    linkIndex = tag.index(']')+1
    link = tag[linkIndex:]
    thisMap[name] = link
    for otherName in args:
        thisMap[otherName] = link
    return thisMap


def initLinks():
    linkMap.clear()
    linkMap.update(addLinkEntry(
        "@[Graham](person:7fda6bf6-7a78-40e6-934f-43c4f06d1540)", "Graham Hayward"))
    linkMap.update(addLinkEntry(
        "@[Celduin](person:6da69324-d324-41a1-8931-d6b72e0c73c4)"))
    linkMap.update(addLinkEntry(
        "@[Ardr](person:7d7f9110-e15d-458d-af8e-d21f0ad3982b)"))
    linkMap.update(addLinkEntry(
        "@[Gilda](person:8a644e93-53f1-4d05-a661-407ca703b19c)", "Gilda Gonne"))
    linkMap.update(addLinkEntry(
        "@[Fedaria](person:eb7b59b3-81a8-42f5-b628-151da32436b8)", "Fedaria Quinn"))
    linkMap.update(addLinkEntry("@[Rosie](person:08dee44c-a760-4308-9011-35af77cf5dba)",
                                "Rosie of the Glittering Coast"))
    linkMap.update(addLinkEntry(
        "@[Daermir](person:be55dabc-1761-4ff5-93f2-8d7239deb0ed)"))
    linkMap.update(addLinkEntry(
        "@[Lysivia](person:f9b4be98-bbd2-4cbf-a2e0-c13f1d0796a7)"))
    linkMap.update(addLinkEntry(
        "@[Tobias](person:c06484d7-b27e-41d2-9ba0-dabdaec502c3)", "Toby"))
    linkMap.update(addLinkEntry(
        "@[Dotmoul Smeltspine](person:5ce1a9ba-63da-41d9-a22e-ca4cd90981e4)"))
    linkMap.update(addLinkEntry("@[Breaker](person:62f309c5-a5fd-4489-a1d8-be40337da877)",
                                "Breaker of the Seventh Star"))
    linkMap.update(addLinkEntry(
        "@[Esta](person:1523c000-9148-4d7e-add1-d2825aecdd5b)", "Esta Damsev"))
    linkMap.update(addLinkEntry(
        "@[Arthund](person:c0116e17-6382-44ab-b089-9696041902a6)"))
    linkMap.update(addLinkEntry(
        "@[Blue](person:a44d91c7-cf06-458a-a2ea-d00c9263b68a)"))
    linkMap.update(addLinkEntry(
        "@[Gareholm](settlement:c572cfb7-9024-401e-834c-73284278093b)"))
    linkMap.update(addLinkEntry(
        "@[Volantis](settlement:8688cefc-ba76-46ac-9dce-fc29e48b14e2)"))
    linkMap.update(addLinkEntry(
        "@[Gods' Watch](settlement:dcddce0a-0056-484b-9fc2-6cb171704a98)"))
    linkMap.update(addLinkEntry(
        "@[Highmount](location:40d004e4-5e73-4a90-984d-e60fadc0b8f6)"))
    linkMap.update(addLinkEntry(
        "@[Shard Armament](article:957e1458-ed13-48fe-bc14-0e17f9360f7a)"))
    linkMap.update(addLinkEntry(
        "@[Thousand Eyes](organization:999ac77a-34ea-4344-8b36-97cf930f6ef3)"))
    linkMap.update(addLinkEntry(
        "@[Adlem's Quay](settlement:454ed8ea-0866-479e-8b13-b911e6378d34)"))
    linkMap.update(addLinkEntry(
        "@[Eadwic Vyncis](person:c71659fd-022d-49dd-99b1-5bf9c6c6d445)"))
    linkMap.update(addLinkEntry(
        "@[Lindor's Rest](location:8718d1b5-d602-4101-9ad9-6c2f6521614b)"))
    linkMap.update(addLinkEntry(
        "@[Silvius](organization:7a39665c-d367-4df1-8866-eb3e6a44f7c5)"))
    linkMap.update(addLinkEntry(
        "@[Brunhild](organization:f02499fc-8ddb-443d-b5ac-dc34b1bbd119)"))
    linkMap.update(addLinkEntry(
        "@[Pyrrhus](organization:e5539076-3535-4110-8ba4-3d4d59537969)"))
    linkMap.update(addLinkEntry(
        "@[Acid Wastes](location:ebe447ec-88f3-4ebb-b196-78a5913c7a36)"))
    linkMap.update(addLinkEntry(
        "@[The Fly By Night](vehicle:25646caa-f0a8-4eba-9b49-ca15b7fd09e5)"))
    linkMap.update(addLinkEntry(
        "@[Gregory](person:4570f0d0-6a2e-402e-a8b6-9e48b91dbdc6)", "Big Greg"))
    linkMap.update(addLinkEntry(
        "@[Yrrasil](person:2f490b36-728e-4746-a002-950877d81295)"))
    linkMap.update(addLinkEntry(
        "@[Red Gulch](settlement:50d2162c-2178-4819-a102-668327846ff9)"))
    linkMap.update(addLinkEntry(
        "@[Brightseeker Bolviar](person:dcc56c5d-b347-4eee-bd10-a1e260ebba55)", "Bolviar"))
    linkMap.update(addLinkEntry(
        "@[Imera](person:5ed14923-fb04-4368-8a60-f13c6267d51b)"))
