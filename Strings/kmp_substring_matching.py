""" The Module containing the Knuth-Morris-Pratt (KMP) algorithm
    used to find occurrences of matching substrings
"""


# There are two parts of this algorithm:
# 1.) A function for generating the prefix tables for the given pattern to match
# 2.) The function performing the main matching

def get_prefix_suffix(pattern):
    """
    The function for generating the prefix-suffix table for the given pattern string
    :param pattern: The string pattern to be located in the main string
    :return: The list (table) generated for the pattern
    """
    tmp = [0]  # initialize the tmp to a list containing just 0
    # initialize the i and j pointers
    i = 1
    j = 0

    while i < len(pattern):
        if pattern[i] == pattern[j]:
            tmp.append(j + 1)
            i = i + 1
            j = j + 1

        else:
            if j == 0:
                tmp.append(tmp[j])
                i = i + 1  # increment only i

            else:
                j = tmp[j - 1]

    return tmp  # return the tmp so created


def kmp_match_substrings(match_string, pattern):
    """
    The function for computing the match occurrences of the substring in the string
    :param match_string: The main string for finding the occurrences
    :param pattern: The substring for finding the occurrence matches
    :return: The array (python list) containing a 1 for the start position where there is a match
    """
    # compute the prefix table for the search pattern
    pre_su_tab = get_prefix_suffix(pattern)

    matches = [0 for _ in range(len(match_string))]  # initialize the match list
    pat_len = len(pattern)

    # initialize the pointers for the algorithm
    i = 0
    j = 0

    while i < len(match_string):
        if match_string[i] == pattern[j]:
            # This is a part of a potential match
            if j == (pat_len - 1):
                # the patterns have matched
                matches[i - pat_len + 1] = 1  # set the place of match
                j = pre_su_tab[j]
                i = i + 1
            else:
                i = i + 1
                j = j + 1
        else:
            # This is not a match or a partial match
            if j == 0:
                i = i + 1
            else:
                j = pre_su_tab[j - 1]

    # return the matches so created
    return matches


# naive tester
if __name__ == '__main__':
    # Test the get_prefix_suffix function
    string = "ababa"
    pat_pre = get_prefix_suffix(string)
    print(pat_pre)

    string = "ababcacababc"
    pat_pre = get_prefix_suffix(string)
    print(pat_pre)

    # Test the kmp_match_substrings function
    string = "ababaccabababa"
    pat = "ababa"
    print(kmp_match_substrings(string, pat))
