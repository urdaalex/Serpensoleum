import re

def trim_whitespace(s):
    return re.sub('\s+', ' ', s)

def remove_quotes(s):
    return s.replace('"', '')

def remove_garbage(s):
    s = trim_whitespace(s)
    s = remove_quotes(s)

    return s