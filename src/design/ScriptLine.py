class ScriptLine:
    def __init__(self, text: str, number: int, z_rv: int, *options: str, required: bool = False, use_saved: bool = True) -> None:
        self.text = text
        self.number = number
        self.default = options[0] if options else ""
        self.options = options
        self.result = ""
        self.required = required
        self.use_saved = use_saved
        self.z_rv = z_rv

    def __repr__(self) -> str:
        return f"{self.text} -> {self.options}"
