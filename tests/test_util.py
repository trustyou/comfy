from comfy.util import camel_case_to_lower


def test_camel_case_to_lower():

    assert camel_case_to_lower("Word") == "word"
    assert camel_case_to_lower("CamelCase") == "camel_case"
    assert camel_case_to_lower("ALLUPPER") == "allupper"
    assert camel_case_to_lower("Python3000Options") == "python3000_options"
