from SAM import SuffixAutomaton

sam = SuffixAutomaton()
sam.build("ababa")

print(sam.match_all("a"))     # ?
print(sam.match_all("aba"))   # ?
print(sam.match_all("baba"))  # ?
print(sam.match_all("c"))     # ?
print(sam.match_all(""))
