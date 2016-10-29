import re

URL_PATTERN = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
PHONE_NUMBER_PATTERN = u'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
COPYRIGHT_PATTERN = r"""copyright|rights"""
PARAGRAPH_SPLITTING_PATTERN = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s'
PUNCTUATION_PATTERN = r'[^\?|\.|\!][\?|\.|\!]{1}$'


GARBAGE = [PHONE_NUMBER_PATTERN, COPYRIGHT_PATTERN]

def check_text_for_garbage(text, patterns=[]):
    for pattern in patterns:
        pattern = re.compile(pattern, re.IGNORECASE)
        if pattern.search(text) != None:
            # print text
            return True

    return False

def check_ends_with_punctuation(text):
    pattern = re.compile(PUNCTUATION_PATTERN)

    if pattern.search(text) != None:
        return True

    return False

def get_links(text):
    pattern = re.compile(URL_PATTERN)
