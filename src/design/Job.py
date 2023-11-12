from design.Part import Part


class Job:
    def __init__(self, department: str, contact_name: str, comment: str, parts: list[tuple[Part, int]]):
        self.department = department
        self.contact_name = contact_name
        self.comment = comment.strip()
        self.test_comment = self.comment
        self.part_quantities = parts
        self.synced = False

        for part, quantity in parts:
            self.comment += f"\n{part.number} X {quantity}"

    def __repr__(self) -> str:
        return f"{self.comment}"
