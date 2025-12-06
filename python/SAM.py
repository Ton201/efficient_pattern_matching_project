class State:
    """
    A node (state) of the suffix automaton.
    """
  
  
    def __init__(self):
        self.suffix_link = None
        self.next = {} # dictionary: keys = characters, values = states you transition to on that character
        self.length = 0
        self.initial = False 
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
  
  
    def n_states(self):
        """
        Get number of states in M.
        """
        raise NotImplementedError("TODO: implement n_states()")
  
  
    def n_transitions(self):
        """
        Get number of transitions in M.
        """
        raise NotImplementedError("TODO: implement n_transitions()")
  
  
    def build(self, T):
        """
        Build the automaton from text T.
        """
        self._alphabet = set(T)
        n = len(T)
        # set the last pointer to the innitial state
        # length 0 and sl = None set when initialiying the SAM
        last = None
        # itterate thought the text T and extend the SAM
        for letter in T:
            # create a new state
            new = State()
            # set the depth of the state
            len = self.states[last].length + 1
            # set pointer to the last added state
            p = last
            while not (p is None and letter not in self.states[p].next.keys)
                self.states[p].next[letter] = new # new is not an index but a node!
                p = self.states[p].suffix_link
            # if p is initial state suffix link of the first node is an initial state
            if p is None:
                new.suffix_link = 0
            else:
                q = self.states[p].next[c]
                # if q is the next node
                if self.states[p].length + 1 == self.states[p].length:
                    new.suffix_link = q # q is not an index but a node!
                # else need a clone
                else:
                    clone = State()
                    clone.length = q.length + 1
                    # copy transitions from OG node q
                    for b in self._alphabet:
                        clone.next[b] = q.next[b]
                    new.suffix_link = clone
                    clone.suffix_link = q.suffix_link # clone inherits suffix links from OG node
                    q.suffix_link = clone
                    while (p is None and letter not in self.states[p].next.keys):
                        self.states[p].next[letter] = clone # clone is not an index but a node!
                        p = self.states[p].suffix_link
            self.states.append(current)
            last = new
        # end of extension
        p = last
        while p is not None:
            self.states[p].final = True
            p = self.states[p].suffix_link
        return self
        # raise NotImplementedError("TODO: implement build()")
    
  
    def count(self, P) -> int:
        """
        Number of occurrences of pattern P in the built text.
        """
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
  
