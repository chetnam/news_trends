import pytest
from news_trends import utils
# utils = news_trends.utils

class TestClass:
    
    def test_mean_pass(self):
        lst = [1, 2, 3, 4, 5]
        mean_correct = sum(lst) / len(lst)
        
        assert mean_correct == utils.mean(lst)

    def test_mean_exception(self):
        lst = [1, 2, 3, 'a', 5]
        with pytest.raises(Exception):
            utils.mean(lst)