from SAM import SuffixAutomaton

text = 'abcbabaabc'

sa = SuffixAutomaton()
# should terutn the text alphabet
print(sa.build(text))
