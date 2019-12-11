"""
Houses common multipurpose helper methods
Currently contains: sentiment, mean, median, string builder for query parameters
"""

import textblob as tb
import json

def get_textual_sentiment_and_objectivity(content):
    """
    Given string content, returns a tuple of (polarity, objectivity)
    According to textblob docs:
    - polarity is in range of [-1.0, 1.0]
    - subjectivity is in range of [0.0, 1.0] where 0.0 is very objective
    """
    if len(content)==0:
        return (0,0)

    text = tb.TextBlob(content)
    polarity = text.sentiment.polarity
    subjectivity = text.sentiment.subjectivity

    return (polarity, subjectivity)

def isListNumeric(lst:[]):
    """
    Returns True if given parameter is a list and only has numeric elements.
    False otherwise.
    """

    # check if list
    if not isinstance(lst, list):
        return False

    # check if each element is numeric
    if False in [isinstance(num, int) or isinstance(num, float) for num in lst]:
        return False

    return True

def mean(lst):
    """
    Expects a numeric list.
    Throws Exception if parameter is not a list or has non-numeric elements.
    """

    # return error if any element is not a number
    if not isListNumeric(lst):
        return Exception('Given argument is either not a list or has non-numeric elements')

    if len(lst)==0:
        return 0

    sum = 0
    for num in lst:
        sum += num

    return sum/len(lst)

def median(lst):
    """
    Sorts list before getting median.
    Expects a numeric list.
    Throws Exception if parameter is not a list or has non-numeric elements.
    """

    if not isListNumeric(lst):
        return Exception('Given list has non-numeric elements')
    
    lst.sort()

    mid = len(lst) // 2
    
    if len(lst)>0 and len(lst)%2 == 0: # if even
        return (lst[mid-1] + lst[mid]) / 2
    else: # if odd
        return lst[mid]

# included here because it might be useful if adding more data sources
def build_part_of_query_string(param_name, param_value, query_string):
    """
    Given a string param_name, a param_value (can be None), and a string query_string,
    this function returns query_string 
    with the query parameter param_name is param_value is not None
    """
    if param_value:
        if query_string:
            query_string += '&'
        query_string += f'{param_name}{"=" if param_name else ""}{param_value}'

    return query_string
    
