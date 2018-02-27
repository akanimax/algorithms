""" This module containing the implementation of the Aho-Corasick algorithm which is used for
    matching a set of substrings within a given matchstring. This is an advanced algorithm mainly
    used for doing dna sequences analysis. The algorithm works by first generating a Finite Automaton
    and then using the FA for performing the substring matching.

    The algorithm works in O(m + k + n);
    where m: length of the match string
          k: number of pattern substrings
          n: average length of each pattern substring

    for more info, refer the wiki page -> https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm
"""


def create_fsm(pattern_strings):
    """
    The function for creating the finite state machine for the given pattern strings
    :param pattern_strings: the list of pattern strings
    :return: goto, failure and output structures
    """
    # obtain the vocabulary elements
    vocab_elems = sorted(set(''.join(pattern_strings)))

    # create the empty structures for the goto, failure and output
    print(vocab_elems)


if __name__ == '__main__':
    create_fsm(["animesh", "karnewar", "is", "here"])