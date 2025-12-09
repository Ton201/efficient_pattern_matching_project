class State:
    """
    A node (state) of the suffix automaton.
    """
  
  
    def __init__(self):
        self.suffix_link = None
        self.next = {} # dictionary: keys = characters, values = states you transition to on that character
        self.length = 0
        self.final = False
        # sttributes for count(), match_first(), match_last()
        self.occurence = 0
        self.first_pos = None
        self.last_pos = None
        # atributes for match_all()
        self.state_at_pos = [] # for each i: state after reading T[:i+1]
        self.children = [] # suffix-link tree adjacency list
        # DFS intervals of suffix-link tree
        self.tin = []            
        self.tout = []
        # DFS time counter
        self._time = 0           


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
        self.state_at_pos = []
        # set the last pointer to the innitial state
        # length 0 and sl = None set when initialiying the SAM
        self.last = 0
        # EXTEND:
        # itterate thought the text T and extend the SAM
        # 
        for i, letter in enumerate(T):
            self._extend(letter, pos=i)
            self.state_at_pos.append(self.last)
        # end of extension
        # mark final states
        p = self.last
        while p != 0:
            self.states[p].final = True
            p = self.states[p].suffix_link
        # propagate occurence counts
        # Core idea: every occurrence of a string in v gives an occurrence of 
        # its suffix in link, ending at the same index, so min/max end positions
        # propagate the same way as counts.
        # 
        # get order of states sorted by length decreasing
        order = sorted(range(len(self.states)),
               key=lambda i: self.states[i].length,
               reverse=True)
        # follow suffix links
        for state_index in order:
            link = self.states[state_index].suffix_link
            if link is not None:
                # add up the occurences
                self.states[link].occurence += self.states[state_index].occurence
                # first position
                if self.states[link].first_pos is None:
                    self.states[link].first_pos = self.states[state_index].first_pos
                else:
                    self.states[link].first_pos = min(self.states[link].first_pos,
                                                      self.states[state_index].first_pos)
                # last position
                if self.states[link].last_pos is None:
                    self.states[link].last_pos = self.states[state_index].last_pos
                else:
                    self.states[link].last_pos = max(self.states[link].last_pos,
                                                     self.states[state_index].last_pos)
        self._build_suffix_tree_info()
        return self
        # raise NotImplementedError("TODO: implement build()")
    

    def _extend(self, letter, pos):
        # create a new state
        # firstly pointer in SAM states list
        new = len(self.states)
        # secondly to said state
        self.states.append(State())
        # set the depth of the state
        self.states[new].length = self.states[self.last].length + 1
        self.states[new].occurence = 1
        self.states[new].first_pos = pos
        self.states[new].last_pos = pos
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
                #
                # clone does not add an end posstion
                # occurence is 0 in State().__init__ by default
                #
                # clone inherits possitions from q
                self.states[clone].first_pos = self.states[q].first_pos
                self.states[clone].last_pos  = self.states[q].last_pos
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
        state_id = 0
        for letter in P:
            if letter not in self.states[state_id].next.keys():
                return 0
            state_id = self.states[state_id].next[letter]
        return self.states[state_id].occurence
        raise NotImplementedError("TODO: implement count()")
    
  
    def match_first(self, P) -> int:
        """
        Starting index of the first (leftmost) occurrence, or -1 if absent.
        """
        # start from the innitial state and propagate though pattern P
        state_id = 0
        for letter in P:
            if letter not in self.states[state_id].next.keys():
                return -1
            state_id = self.states[state_id].next[letter]
        end = self.states[state_id].first_pos
        if end is None:
            return -1
        return end - len(P) + 1
        raiseNotImplementedError("TODO: implement match_first()")
    
  
    def match_last(self, P) -> int:
        """
        Starting index of the last (rightmost) occurrence, or -1 if absent.
        """
        # start from the innitial state and propagate though pattern P
        state_id = 0
        for letter in P:
            if letter not in self.states[state_id].next.keys():
                return -1
            state_id = self.states[state_id].next[letter]
        end = self.states[state_id].last_pos
        if end is None:
            return -1
        return end - len(P) + 1
        raise NotImplementedError("TODO: implement match_last()")
    
  
    def match_all(self, P) -> list:
        """
        Return all starting positions of pattern P in the text.
        """
        # simple SAM-based approach would crush on 'mono' dataset ~ O(n^2) time and memory
        # let's reverse the idea of suffix link
        #   suffix links lead to longest propper suffixes of the string
        #   there for in the opposite dirrection, we can all strings containing siad string in suffix
        # 
        # efficient way to navigate suffix links in opposite direction = tree structure + depth-first-search
        state_id = 0
        for letter in P:
            if letter not in self.states[state_id].next.keys():
                return -1
            state_id = self.states[state_id].next[letter]

        result = []
        l = len(P)
        t_in = self.tin[state_id]
        t_out = self.tout[state_id]
        # search suffix link tree
        for i, st in enumerate(self.states[state_id].state_at_pos):
            if t_in <= tin[st] <= t_out:
                result.append(i - m + 1)
        return result.sort()
        NotImplementedError("TODO: implement match_all()")
        
    def _build_suffix_tree_info(self):
        '''
        Builds suffix link tree and runs DFS on in
        '''
        n_states = len(self.states)
        # children list: parent = suffix_link, child = state
        self.children = [[] for _ in range(n_states)]
        for state_id in range(1, n_states):     # skip 0 because its suffix_link is None
            link = self.states[state_id].suffix_link
            if link is not None:
                self.children[link].append(state_id)
        # prepare tin/tout arrays
        self.tin = [0] * n_states
        self.tout = [0] * n_states
        self._time = 0

        # run DFS from root
        self._dfs_suffix_tree(0)


    def _dfs_suffix_tree(self, state_id):
        self._time += 1
        self.tin[state_id]
        for branch in self.children[state_id]:
            self._dfs_suffix_tree(branch)
        self._time += 1
        self.tout[state_id] = self._time





