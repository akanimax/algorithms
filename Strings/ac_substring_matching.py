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


def create_fsm(match_string, pattern_strings):
    """
    The function for creating the finite state machine for the given pattern strings
    :param match_string: the string which is to be matched against
    :param pattern_strings: the list of pattern strings
    :return: (goto, failure, output) structures and the num_states
    """
    # obtain the vocabulary elements and max_states
    vocab_elems = sorted(set(match_string))
    max_states = sum([len(x) for x in pattern_strings])

    # create the empty structures for the goto, failure and output
    goto = {k: [-1 for _ in range(max_states)] for k in vocab_elems}
    fail = [0 for _ in range(max_states)]
    out = [set() for _ in range(max_states)]

    num_states = 1  # at the beginning, there is only one state (0)

    # build the trie which is represented by the goto and the out
    for pat_no in range(len(pattern_strings)):
        current_state = 0
        pattern = pattern_strings[pat_no]

        for ch in pattern:
            if goto[ch][current_state] == -1:
                # insert a new state
                goto[ch][current_state] = num_states
                num_states += 1

            current_state = goto[ch][current_state]

        # add the output to the output state
        out[current_state].add(pat_no)  # this pattern is detected here

    # add self connections to the root state
    for ch in vocab_elems:
        if goto[ch][0] == -1:
            goto[ch][0] = 0

    # readjust the goto, out and fail according to num_states now.
    red_states = max_states - num_states  # stands for redundant states

    goto = {k: v[:-red_states] for (k, v) in goto.items()}
    out = out[:-red_states]
    fail = fail[:-red_states]

    # build the failure cases: This
    # is done in a breadth first manner.

    queue = []  # initially empty list

    # add failure to root for all depth 1 nodes:
    for ch in vocab_elems:
        node = goto[ch][0]
        if node != -1 and node != 0:
            queue.append(node)

    # perform dfs
    while len(queue):
        state = queue.pop(0)  # obtain the front state
        failure = fail[state]  # obtain the failure of current state

        for ch in vocab_elems:
            child = goto[ch][state]
            if child != -1:
                # obtain the failure link for this child starting from the failure
                while goto[ch][failure] == -1:
                    failure = fail[failure]

                fail[child] = goto[ch][failure]
                out[child] = out[child].union(out[goto[ch][failure]])

                # finally add the child to the queue
                queue.append(child)

    # return the required
    return goto, fail, out, num_states


def next_state(goto, fail, current_state, next_char):
    """
    The function that gives you the next state based on the current state and occurring character
    :param goto: the goto function
    :param fail: the fail function
    :param current_state: current state
    :param next_char: char under occurence
    :return: next_state
    """
    nst = current_state  # initialize this to current state

    while goto[next_char][nst] == -1:
        nst = fail[nst]

    return goto[next_char][nst]


def ac_match_substrings(match_string, patterns):
    """
    The main function for this algorithm which performs the substring matching
        Note => This function returns the number of occurrences of the patterns
        in order to keep the mem consumption in check. But, this can be modified
        to obtain the places where a match occurs

    :param match_string: the string to be searched
    :param patterns: the list of search patterns
    :return: no_of occurrences of each pattern in the match_string
    """
    # create the result data structure
    result = {pat: 0 for pat in patterns}

    # obtain the fsm for the patterns
    goto, fail, out, num_states = create_fsm(match_string, patterns)

    # traverse the match string and move over the generated fsm
    state = 0  # start from root
    for ch in match_string:
        state = next_state(goto, fail, state, ch)
        if len(out[state]):
            for match in out[state]:
                result[patterns[match]] += 1

    # return the result
    return result


if __name__ == '__main__':
    res = ac_match_substrings(match_string="cdababaabbaaaabbababbacd",
                              patterns=["abab", "aabb", "aaab", "abba"])

    for (b, d) in res.items():
        print(b, ":", d)
