#   Semestral work report B251
-   Implementation Language: **python/cpp**

##  Implementation and data structure design
-   What construction algorithm did you choose and why?

I used Suffix-Automaton-Online algorithm as described in provided lecture materials. The extension function was implemented also according to the lecture materials  - function Extension(a ∈ Σ). 

-   Did you need any additional computation to answer all of the queries for matching? If yes, what and how did you integrate it? 

	- for **count()** I had to implement occurrence counter. Every new state has one occurrence upon initialization. However since the pattern can be just the suffix of the state. States representing shorter stings have more occurrences. After the extension phase in build function I ordered states from longest to shortest and added up their occurrences following their suffix links.

	- for **match_first()** and **match_last()** I applied similar idea to implementation of count(). Only difference is that it does not make sense to add up first or last occurrence. The minimum and maximum of first and last occurrence respectively are calculated between state and its suffix link.  

	- **match_all()** method was more challenging to implement. Applying the same logic as in previous methods would work. However, the time and memory complexity would be $O(n^2)$ which would be exploited later on by _mono dataset_. The chose approach was _suffix link tree_ + _depth first search (DFS)_ to navigate it efficiently.(link)[https://cp-algorithms.com/string/suffix-automaton.html#all-occurrence-positions] 

-   Did you have any troubles you want to share with your implementation?

Get the understanding for suffixlink tree and DFS took some time and effort.

##  LCF Algorithm design
-   Describe and write pseudocode of your algorithm
-   Analyse time and memory consumption
-   Please, keep your variable name same as in implementation

##  Experiment results
-   Import your graphs from the experiments
-   How the pattern length and the number of occurences in the text inflict the query time?
-   Did you have any troubles you want to share with experiment running and evaluation?

##  Conclusion
-   For what kind of queries and data would you recommend Suffix Automaton data structure?
-   Can you just by your words compare SAM with other suffix data structures (Trie, Tree, Array?)