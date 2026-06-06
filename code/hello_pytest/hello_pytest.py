ENGLISH_HELLO_PREFIX = "Hello, "
SPANISH = "Spanish"
SPANISH_HELLO_PREFIX = "Hola, "
FRENCH = "French"
FRENCH_HELLO_PREFIX = "Bonjour, "

DEFAULT_NAME = "world"


def hello(name="", language=""):
    if name == "":
        name = DEFAULT_NAME
    return greeting_prefix(language) + name


def greeting_prefix(language):
    if language == SPANISH:
        return SPANISH_HELLO_PREFIX
    if language == FRENCH:
        return FRENCH_HELLO_PREFIX
    return ENGLISH_HELLO_PREFIX
