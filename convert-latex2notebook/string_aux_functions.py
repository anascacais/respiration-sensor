import re

def try_search(regex, test_string):
    try:
        return re.search(regex, test_string).group(1)
    except:
        print(f'not found: {regex}')
        return ''
    

def find_str_in_list(test_string, list):
    '''
     Returns
     -------
     idx: list
        List where each element is the line number where the test_string is found
     '''

    return [i for i, st in enumerate(list) if test_string in st]