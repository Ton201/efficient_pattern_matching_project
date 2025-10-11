
# Semester Project for Course NI-EVY, Semester B251 - Suffix Automata for Solving LCF

The goal of the semester project is to implement and use a suffix automaton and the required methods. The implementation, unless otherwise permitted, will be written in C++, or exceptionally in Python. Interfaces for both languages are prepared in the `cpp` and `python` folders. The semester project can be awarded up to 20 points. 20 points from the semester project is not a sufficient condition for obtaining credit — the student must successfully pass the credit test with a required minimum score of 10 p...

## Assignment

**Suffix automaton** is a deterministic finite automaton $M = (Q,\Sigma,\delta,q_0,F)$, where:
- $Q$ is a non-empty set of states of the automaton
- $\Sigma$ is a non-empty set of input symbols (alphabet)
- $\delta$ is the transition function $Q \times \Sigma \rightarrow Q$
- $q_0$ is the initial state of the automaton
- $F$ is the set of final states

and it holds that for text $T$, $L(M_T) = \{T[i\ldots|T|-1] \mid 0\leq i \leq |T|-1\}$

1. Create a data structure of a suffix automaton $M_T$ for text $T$, which will have the following methods implemented:

|Method Name       |Description     |
|------------      |-----     |
|$build(T)$        | Creates a data structure over the text $T$ |
|$count(P)$        | Returns the number of occurrences of pattern $P$ in text $T$| 
|$match\_all(P)$  | Returns all positions $i$ in text $T$, where $T[i\ldots i+\|P\|-1]=P$ | 
|$match\_first(P)$| Returns the first position $i$ in text $T$, where $T[i\ldots i+\|P\|-1]=P$, -1 if the position is not found | 
|$match\_last(P)$ | Returns the last position $i$ in text $T$, where $T[i\ldots i+\|P\|-1]=P$, -1 if the position is not found | 

Additionally, each state of the automaton $p$ stores a **suffix_link** $sl(p)$:

| | |
|-           |-     |
|$label(q)$ | is the longest word $w$ such that $(q_0,w)\vdash^*(q,\varepsilon)$ -> not required to implement |
|$suffix\_linkl(p)$ | $q$ such that $label(p) = u, label(q) = v$ and $v$ is the longest proper suffix of $u$ |
|           |     |

**!!If part 1 of the assignment is not fulfilled, the following parts cannot be evaluated (it is not allowed to use a suffix automaton implementation from external libraries)!!**

2. Use your suffix automaton for the following problem:

Two words $x$ and $y$ are given over the same alphabet $\Sigma$, and it holds that $|x| \leq |y|$.
Let $LCF(x,y)$ denote the longest substrings that occur in both word $x$ and word $y$.
Design and implement an algorithm for $LCF(x,y)$ using the suffix automaton $M$ only for word $x$.
Return the result as a pair $(I,l)$, where $I$ is the set of positions in text $x$ and $l$ is the length. Analyze the time and memory complexity of your algorithm.

3. Run experiments

For each dataset, create a suffix automaton, measure the construction time and the size of the automaton given by $|Q|+|\delta|$. Also, for a set of patterns for each dataset, measure the search time and normalize it by the number of occurrences. Record the results in a graph and compare them with naive pattern matching without any preprocessing (measured values in *datasets/naive.csv*).

You may also perform additional experiments as you see fit.

4. Fill out the report on your semester project

In the `README.md` file, write and describe all your steps in the implementation and algorithm design.
The report can be written in Czech, Slovak, or English. Implementation and graphs should remain in English.

5. Submit your project in your GitLab repository, create an issue and assign it to your reviewer (J. Holub).

How to do it? In your pushed repository on GitLab, click *Issues* in the left panel. Create a *new issue* and in the *Assignees* field, select Jan Holub. Optionally, add a comment and click *Create issue*.

**!!Submit the semester project by 14.12.2025 23:59:59. Late submission will result in a penalty (see the evaluation section)!!**

## Project Evaluation

The project evaluation takes place in 4 phases.
1. The implementation undergoes automated tests, which are available in the $test$ folder.
To run the tests:

- **Python tests**

   For Python, tests are available for pytest. If you don't have it installed:

   ```shell
   pip install pytest
   ```
   
   All tests can be run at once from the python folder:

   ```shell
   PYTHONPATH=. pytest
   ```

   Or individually:

   ```shell
   PYTHONPATH=. pytest text/<test_name>
   ```

- **Cpp tests**
    
   Clean the environment and compile:

   ```shell
   make clean && make
   ```

   Run the tests:

   ```shell
   make test
   ```

   The tests check the output values of the functions from parts 1 and 2 of the assignment.
   This part is worth 8 points.

-------------------------------
2. Run experiments and process the resulting data into graphs.

   This part is worth 6 points.

3. Evaluation of results and description of the implementation in the project report.

   This part is worth up to 6 points.

4. In case of evaluator questions, an oral defense of the semester project may be required.

**Penalties**
1. Code readability  
It is important that your code is well-readable and well-commented. If not, the evaluator reserves the right to reduce the total score by up to 3 points.
2. Late submission  
If the project is submitted late without prior excuse, the total score may be reduced by up to 2 points for each starting week of delay.

## Final Notes
Yes, AI is powerful enough today to complete all tasks on its own, and the internet is full of ready-made and explained implementations. The purpose of the semester project is for you to try the data structure yourself. Therefore, we expect that you will not excessively use or abuse AI or implementations from the internet.

If you find any errors that you think everyone should know about, write to the shared email conversation (it will be created no later than with the automated repository creation).

Good luck!
