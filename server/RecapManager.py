def format(text):
    lines = text.splitlines()
    print lines
    length = len(lines)
    formatted = '''
'''
    for i in range(length):
        thisLine = lines[i]
        try:
            nextLine = lines[i+1]
        except:
            nextLine = None
        print(thisLine)
        print indentLevel(thisLine)
    formatted.join(lines)
    return formatted.join(lines)


def indentLevel(line):
    if line is None:
        return 0
    return line.count('''   ''')
