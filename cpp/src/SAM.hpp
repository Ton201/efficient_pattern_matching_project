// SAM.hpp
// Suffix Automaton

#pragma once

#include <unordered_map>
#include <vector>
#include <string>
#include <limits>

class State {
    // A node (state) of the suffix automaton.
    public:

    State* suffix_link; 
    std::unordered_map<char, State*> next; // transitions

    State() = default;
    ~State() = default;

    // Return destination state id on character `c`, or null if absent.
    State* gotoNext(char c);
};

class SuffixAutomaton {
private: 
    std::vector<State> states; 
    std::unordered_map<char, bool> alphabet;

  // Suffix Automaton class.
public:
    SuffixAutomaton();
    ~SuffixAutomaton();

    // Build the automaton from text T. Should reset previous content.
    void build(const std::string& T);
    
    // Number of occurrences of P in the built text.
    int  count(const std::string& P) const;
    
    // Starting index of the first (leftmost) occurrence, or -1 if absent.
    int  match_first(const std::string& P) const;
    
    // Starting index of the last (rightmost) occurrence, or -1 if absent.
    int  match_last (const std::string& P) const;

    // Return all starting indices where P occurs in the text.
    std::vector<int> match_all(const std::string& P) const;
};
