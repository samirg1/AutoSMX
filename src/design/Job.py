class Job:
    def __init__(self, department: str, contact_name: str, comment: str):
        self.department = department
        self.contact_name = contact_name
        self.comment = comment.strip()
        self.test_comment = self.comment
        self.part_quantity = 0
        self.part_number = ""

        lines = self.comment.split("\n")
        match lines[-1].split(" "):
            case [quantity, "X" | "x", part_number] if quantity.isdigit():
                self.part_quantity = int(quantity)
                self.part_number = part_number
                self.test_comment = "\n".join(lines[:-1])
            case _:
                pass

    def __str__(self) -> str:
        return f"{self.comment}"
