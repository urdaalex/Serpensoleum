import re

def trim_whitespace(s):
    '''
    Trims the white space from a string.
    
    Attributes:
        s (str): Input String to be trimmed.
    '''
    return re.sub('\s+', ' ', s)

def remove_quotes(s):
    '''
    Removes all quotation marks from a string.
    
    Attributes:
        s (str): Input String to get all quotes removed.
    '''
    return s.replace('"', '')

def remove_garbage(s):
    '''
    Applies the two functions above
    
    Attributes:
        s (str): Input String to be cleaned.
    '''
    s = trim_whitespace(s)
    s = remove_quotes(s)

    return s
