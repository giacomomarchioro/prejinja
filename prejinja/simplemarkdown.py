import re

markdownPatterns = [
    (re.compile(r"\*\*\*(.+?)\*\*\*"),r"<em><strong>\1</strong></em>"),
    (re.compile(r"\*\*(.+?)\*\*"),r"<strong>\1</strong>"),
    (re.compile(r"\*(.+?)\*"),r"<em>\1</em>"),
    (re.compile(r"\'(.+?)\'"),r"<code>\1</code>"),
    (re.compile(r'\[([^\]]+)\]\(([^)]+)\)'),r'<a href="\2">\1</a>')
]

def simpleMarkdown(text):
    for i in markdownPatterns:
        text = re.sub(i[0],i[1],text)
    return text