#!/usr/bin/env python2.7
#encoding=utf-8

"""
Code about implementing calculate min edit distance using Dynamic Programming. Although the method is used for compare similariy of two strings,it can also be used to compare two vectors
Code from http://blog.csdn.net/kongying168/article/details/6909959
"""

class EditDistance():
    def __init__(self):
        pass
    def levenshtein(self,first,second):
        """
        Compute the least steps numver to convert first to second by insert,delete,replace(like comparing first with second)

        In information theory and computer science, the Levenshtein distance is a string metric for measuring the difference between two sequences. Informally, the Levenshtein distance between two words is the minimum number of single-character edits (insertion, deletion, substitution) required to change one word into the other. The phrase edit distance is often used to refer specifically to Levenshtein distance.

        (str/list of int, str/list of int) -> int
        return the mininum distance number

        >>> ed = EditDistance()
        >>> ed.levenshtein("abc","abec")
        1
        >>> ed.levenshtein("ababec","abc")
        3

        In Chinese, distance of each word is 3 times than English
        """
    
        if len(first) > len(second):
            first,second = second,first
        if len(first) == 0:
            return len(second)
        if len(second) == 0:
            return len(first)
        first_length = len(first)+1
        second_length = len(second)+1
        distance_matrix = [range(second_length)for x in range(first_length)]
        for i in range(1,first_length):
            for j in range(1,second_length):
                deletion = distance_matrix[i-1][j]+1
                insertion = distance_matrix[i][j-1]+1
                substitution = distance_matrix[i-1][j-1]
                if first[i-1]!=second[j-1]:
                    substitution+=1
                distance_matrix[i][j]=min(insertion,deletion,substitution)
        #print distance_matrix
        return distance_matrix[-1][-1]

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    ed = EditDistance()
    print ed.levenshtein('可能是灯光的原因','因为有光的原因')
