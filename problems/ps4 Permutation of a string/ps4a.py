# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx




def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    list = []
    if len(sequence) == 1:
        return [sequence]

    else:
        char = sequence[0]
        premuted_list = get_permutations(sequence[1:])
        for element in premuted_list :
            for index in range(len(element)+1):
                list.append(element[:index] + char + element[index:])

        for mutation in list[:]:
            for counter in range(list.count(mutation)-1):
                list.remove(mutation)


    return sorted(list)

if __name__ == '__main__':
   #EXAMPLE
    example_input1 = 'abc'
    example_input2 = 'kaki'
    example_input3 = 'loda'
    print('Input:', example_input1)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input1))

#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)
