// test/test_SAM.cpp

#include <cassert>
#include <vector>
#include <string>
#include <algorithm>
#include <iostream>

#include "../src/SAM.hpp"

// Utility to assert exact vector equality (for readability)
static void expect_eq(const std::vector<int>& a, const std::vector<int>& b) {
    assert(a.size() == b.size());
    for (size_t i = 0; i < a.size(); ++i) assert(a[i] == b[i]);
}

// --- Basic: build + simple queries ------------------------------------

static void test_build_and_basic_counts_abracadabra() {
    SuffixAutomaton sa;
    sa.build("abracadabra");

    // P in T
    assert(sa.count("abra") == 2);
    assert(sa.count("ra")   == 2);
    assert(sa.count("cad")  == 1);
    assert(sa.count("adab") == 1);

    // P not in T
    for (const std::string& p : {"xyz", "abba", "aaab"}) {
        assert(sa.count(p) == 0);
    }
}

static void test_match_positions_abracadabra() {
    SuffixAutomaton sa;
    sa.build("abracadabra");

    assert(sa.match_first("abra") == 0);
    assert(sa.match_last ("abra") == 7);
    expect_eq(sa.match_all("abra"), std::vector<int>({0, 7}));

    assert(sa.match_first("ra") == 2);
    assert(sa.match_last ("ra") == 9);
    expect_eq(sa.match_all("ra"), std::vector<int>({2, 9}));

    assert(sa.match_first("cad") == 4);
    assert(sa.match_last ("cad") == 4);
    expect_eq(sa.match_all("cad"), std::vector<int>({4}));
}

// --- Overlaps ----------------------------------------------

static void test_overlaps_multiple_occurrences() {
    const std::string T = "aaaaa";
    SuffixAutomaton sa;
    sa.build(T);

    assert(sa.count("a") == 5);
    assert(sa.match_first("a") == 0);
    assert(sa.match_last ("a") == 4);
    expect_eq(sa.match_all("a"), std::vector<int>({0, 1, 2, 3, 4}));

    assert(sa.count("aa") == 4);
    expect_eq(sa.match_all("aa"), std::vector<int>({0, 1, 2, 3}));

    assert(sa.count("aaa") == 3);
    expect_eq(sa.match_all("aaa"), std::vector<int>({0, 1, 2}));
    assert(sa.match_first("aaa") == 0);
    assert(sa.match_last ("aaa") == 2);
}

// --- Empty ------------------------------------------

static void test_empty_text_behavior() {
    SuffixAutomaton sa;
    sa.build("");

    std::string p = "aa";
    assert(sa.count(p) == 0);
    assert(sa.match_first(p) == -1);
    assert(sa.match_last (p) == -1);
    expect_eq(sa.match_all(p), std::vector<int>{});
}

static void test_empty_pattern_convention() {
    SuffixAutomaton sa;
    sa.build("abcde");

    assert(sa.count("") == 0);
    assert(sa.match_first("") == -1);
    assert(sa.match_last ("") == -1);
    expect_eq(sa.match_all(""), std::vector<int>{});
}

// --- Rebuild (reset) -------------------------------------------------------

static void test_rebuild_resets_state() {
    SuffixAutomaton sa;
    sa.build("abcabc");
    int c1  = sa.count("abc");
    int mf1 = sa.match_first("abc");
    int ml1 = sa.match_last ("abc");

    sa.build("zzzz");
    assert(sa.count("abc") == 0);
    assert(sa.match_first("abc") == -1);
    assert(sa.match_last ("abc") == -1);

    assert(sa.count("zz") == 3);
    expect_eq(sa.match_all("zz"), std::vector<int>({0, 1, 2}));
    assert(sa.match_first("zz") == 0);
    assert(sa.match_last ("zz") == 2);

    assert( (sa.count("abc") != c1) ||
            (sa.match_first("abc") != mf1) ||
            (sa.match_last ("abc") != ml1) );
}

// --- Other ----------------------------------------------

static void test_sentence_varied_alphabet() {
    const std::string T = "the quick brown fox jumps over the lazy dog";
    SuffixAutomaton sa;
    sa.build(T);

    assert(sa.count("the") == 2);
    expect_eq(sa.match_all("the"), std::vector<int>({0, 31}));
    assert(sa.match_first("the") == 0);
    assert(sa.match_last ("the") == 31);

    assert(sa.count("fox") == 1);
    size_t pos = T.find("fox");
    assert(pos != std::string::npos);
    assert(sa.match_first("fox") == static_cast<int>(pos));
    assert(sa.match_last ("fox") == static_cast<int>(pos));

    assert(sa.count("doge") == 0);
    expect_eq(sa.match_all("doge"), std::vector<int>{});
    assert(sa.match_first("doge") == -1);
    assert(sa.match_last ("doge") == -1);
}

static void test_size_measurement() {
    {
        SuffixAutomaton sa;
        sa.build("abracadabra");
        size_t sz = sa.size();
        std::cout << "[abracadabra] SAM size (states + transitions): " << sz << "\n";

        // Rough invariant: #states <= 2 * n, and #transitions < 3 * n
        size_t n = 11; // length of "abracadabra"
        assert(sa.size() > 0);
        assert(sa.size() <= 5 * n);  // generous upper bound
    }

    {
        SuffixAutomaton sa;
        sa.build("aaaaa");
        size_t sz = sa.size();
        std::cout << "[aaaaa] SAM size: " << sz << "\n";

        // Exact: 6 states (2 * n - 1), transitions = 5 (chain)
        // But clones may reduce transitions slightly. We just check range.
        assert(sz > 0);
        assert(sz <= 5 * 5);
    }

    {
        SuffixAutomaton sa;
        sa.build("");
        size_t sz = sa.size();
        std::cout << "[empty] SAM size: " << sz << "\n";
        // empty string should produce 1 state (root) and 0 transitions
        assert(sz == 1);
    }
}

int main() {
    std::cout << "Running C++ SAM tests...\n";

    test_build_and_basic_counts_abracadabra();
    test_match_positions_abracadabra();
    test_overlaps_multiple_occurrences();
    test_empty_text_behavior();
    test_empty_pattern_convention();
    test_rebuild_resets_state();
    test_sentence_varied_alphabet();
    test_size_measurement();

    std::cout << "All tests passed successfully.\n";
    return 0;
}
