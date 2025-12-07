class State:
    """
    A node (state) of the suffix automaton.
    """
  
  
    def __init__(self):
        self.suffix_link = None
        self.next = {} # dictionary: keys = characters, values = states you transition to on that character
        self.length = 0
        self.final = False
        self.occurence = 0
    def goto(self, c):
        """Return destination state id on character `c`, or None if absent."""
        return self.next.get(c, None)
  


class SuffixAutomaton:
    """
    Suffix Automaton for a single text T.
    Implement the following public methods:
      build(T) -> None
        Build the automaton from text T. Should reset previous content.
      count(P) -> int
        Return number of occurrences of `pattern` in the built text.
      match_first(P) -> int
        Starting index of the first (leftmost) occurrence, or -1 if absent.
      match_last(P) -> int
        Starting index of the last (rightmost) occurrence, or -1 if absent.
      match_all(P) -> list[int]
        Return all starting indices where `pattern` occurs in the text.
    """
    
  
    def __init__(self):
        self.states = [State()]
        self._alphabet = set()
        self.last = 0
  
  
    def n_states(self):
        """
        Get number of states in M.
        """
        return len(self.states)
        raise NotImplementedError("TODO: implement n_states()")
  
  
    def n_transitions(self):
        """
        Get number of transitions in M.
        """
        trans = 0
        for state in self.states:
                trans += len(state.next.keys())
        return trans
        raise NotImplementedError("TODO: implement n_transitions()")
  
  
    def build(self, T):
        """
        Build the automaton from text T.
        """
        self._alphabet = set(T)
        # reset automaton
        self.states = [State()]
        # set the last pointer to the innitial state
        # length 0 and sl = None set when initialiying the SAM
        self.last = 0
        # EXTEND:
        # itterate thought the text T and extend the SAM
        # 
        for letter in T:
            self._extend(letter)
        # end of extension
        # mark final states
        p = self.last
        while p != 0:
            self.states[p].final = True
            p = self.states[p].suffix_link
        # propagate occurence counts
        # get order of states sorted by length decreasing
        order = sorted(range(len(self.states)),
               key=lambda i: self.states[i].length,
               reverse=True)
        # add up the occurences followinf sl
        for state_index in order:
            link = self.states[state_index].suffix_link
            if link is not None:
                self.states[link].occurence += self.states[state_index].occurence
        return self
        # raise NotImplementedError("TODO: implement build()")
    

    def _extend(self, letter):
        # create a new state
        # firstly pointer in SAM states list
        new = len(self.states)
        # secondly to said state
        self.states.append(State())
        # set the depth of the state
        self.states[new].length = self.states[self.last].length + 1
        self.states[new].occurence = 1
        # set pointer to the last added state
        p = self.last
        while p is not None and letter not in self.states[p].next.keys():
            self.states[p].next[letter] = new # new is not an index but a node!
            p = self.states[p].suffix_link
        # if p is initial state suffix link of the first node is an initial state
        if p is None:
                self.states[new].suffix_link = 0
        else:
            q = self.states[p].next[letter]
            # if q is the next node
            if self.states[p].length + 1 == self.states[q].length:
                self.states[new].suffix_link = q # q is an index
            # else need a clone
            else:
                clone = len(self.states)
                self.states.append(State())
                self.states[clone].length = self.states[p].length + 1
                # occurence is 0 in State().__init__ by default
                # copy transitions from OG node q
                self.states[clone].next = self.states[q].next.copy()
                self.states[new].suffix_link = clone
                self.states[clone].suffix_link = self.states[q].suffix_link # clone inherits suffix links from OG node
                self.states[q].suffix_link = clone
                # redirect transitions to point to clone
                while p is not None and self.states[p].next[letter] == q:
                    self.states[p].next[letter] = clone # clone is not an index but a node!
                    p = self.states[p].suffix_link
        # update 'last' pointer
        self.last = new
  
    def count(self, P) -> int:
        """
        Number of occurrences of pattern P in the built text.
        """
        # start from the innitial state and propagate though pattern P
        v = 0
        for letter in P:
            if letter not in self.states[v].next.keys():
                return 0
            v = self.states[v].next[letter]
        return self.states[v].occurence
        raise NotImplementedError("TODO: implement count()")
    
  
    def match_first(self, P) -> int:
        """
        Starting index of the first (leftmost) occurrence, or -1 if absent.
        """
        raise NotImplementedError("TODO: implement match_first()")
    
  
    def match_last(self, P) -> int:
        """
        Starting index of the last (rightmost) occurrence, or -1 if absent.
        """
        raise NotImplementedError("TODO: implement match_last()")
    
  
    def match_all(self, P) -> list:
        """
        Return all starting positions of pattern P in the text.
        """
        raise NotImplementedError("TODO: implement match_all()")
  
