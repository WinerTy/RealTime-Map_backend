import pytest

from utils import camel_case_to_snake_case


class TestUtils:

    @pytest.mark.parametrize(
        "string, result",
        [
            pytest.param("ClassName", "class_name", id="default_word"),
            pytest.param("VeryLongClassName", "very_long_class_name", id="long_word"),
            pytest.param("Class", "class", id="single_word"),
        ],
    )
    def test_camel_case_to_snake_case(self, string, result):
        result_string = camel_case_to_snake_case(string)
        assert result == result_string
