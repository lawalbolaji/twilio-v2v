class Model:
    """represents any model that can execute completions"""

    def complete(self, query) -> str | None:
        pass
