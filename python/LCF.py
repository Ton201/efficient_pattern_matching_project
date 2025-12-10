from SAM import SuffixAutomaton

def LCF(x, y):
    """
    Longest Common Factors between strings x and y.

    Returns:
        (positions_in_x, length)
        positions_in_x: list of starting indices in x where the LCF occurs
        length: length of the LCFs
    """
    SAM = SuffixAutomaton().build(x)
    best_length = 0
    best_states = []
    cur_length = 0
    # scan y with SAM for x
    state_id = 0 # start from SAM root
    for letter in y:
        # follow matching transitions
        if letter in SAM.states[state_id].next.keys():
            cur_length += 1
            state_id = SAM.states[state_id].next[letter]
        else:
            # try to find substring with extisting transition ... follow suffix links
            while state_id != 0 and letter not in SAM.states[state_id].next.keys():
                state_id = SAM.states[state_id].suffix_link
                cur_length = SAM.states[state_id].length # reset to the depth of coresponding SAM state
            # check if there is a transition for y[i]
            if letter in SAM.states[state_id].next.keys():
                state_id = SAM.states[state_id].next[letter]
                cur_length += 1
            else:
                # reset to root
                cur_length = 0
                # best_states = []
        # update the best length
        if cur_length > best_length:
            best_length = cur_length
            # reset the best states list
            best_states = [state_id]
        # append another match
        elif cur_length == best_length:
            best_states.append(state_id)
    # hits = [SAM.states[state].length - best_length + 1 for state in best_states]
    # check for case where is no matching pattern - no hits
    if best_length == 0:
        return [], 0
    # best_states is suffix link forrest
    hits = []
    l = best_length
    for state_id in best_states:
        t_in = SAM.tin[state_id]
        t_out = SAM.tout[state_id]
        # search suffix link tree
        for i, st in enumerate(SAM.state_at_pos):
            if t_in <= SAM.tin[st] <= t_out:
                hits.append(i - l + 1)
    # remove duplicates
    hits = sorted(set(hits))
    return hits, best_length
    raise NotImplementedError("TODO: implement LCF()")
