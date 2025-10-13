// SAM.cpp
#include "SAM.hpp"

#include <stdexcept>

// ---------------- State ----------------

State* State::gotoNext(char c) {
    auto it = next.find(c);
    return (it == next.end()) ? NULL : it->second;
}

// ---------------- SuffixAutomaton ----------------

SuffixAutomaton::SuffixAutomaton() = default;
SuffixAutomaton::~SuffixAutomaton() = default;

size_t SuffixAutomaton::size() const {
    throw std::logic_error("TODO: implement size()");
}

void SuffixAutomaton::build(const std::string& T) {
    throw std::logic_error("TODO: implement build()");
}

int SuffixAutomaton::count(const std::string& P) const {
    throw std::logic_error("TODO: implement count()");
}

int SuffixAutomaton::match_first(const std::string& P) const {
    throw std::logic_error("TODO: implement match_first()");
}

int SuffixAutomaton::match_last(const std::string& P) const {
    throw std::logic_error("TODO: implement match_last()");
}

std::vector<int> SuffixAutomaton::match_all(const std::string& P) const {
    throw std::logic_error("TODO: implement match_all()");
}

