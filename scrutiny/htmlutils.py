from dominate import tags


def note(text: str) -> None:
    tags.p(text)
