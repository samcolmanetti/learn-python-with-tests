from .hello_pytest import hello


def test_says_hello_world():
    assert hello() == "Hello, world"
