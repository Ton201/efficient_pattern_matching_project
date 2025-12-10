from SAM import SuffixAutomaton

sam = SuffixAutomaton()
sam.build("ababa")
print(sam.count("a"))   # expect 3
print(sam.count("aba")) # expect 2
print(sam.count("baba"))# expect 1
print(sam.count("c"))   # expect 0
print(sam.count(""))   # expect 0
