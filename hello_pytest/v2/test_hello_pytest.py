from .hello_pytest import hello


def test_greets_a_person_by_name():
    assert hello("Chris") == "Hello, Chris"


def test_defaults_to_world_when_no_name_given():
    assert hello() == "Hello, world"
