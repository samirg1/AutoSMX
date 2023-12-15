from design.Part import Part


class Job:
    def __init__(self, department: str, contact_name: str, comment: str, parts: list[tuple[Part, int]]) -> None:
        self.department = department
        self.contact_name = contact_name
        self.comment = comment.strip()
        self.part_quantities = parts
        self.synced = False

    def finalise(self, room: str):
        for part, quantity in self.part_quantities:
            self.comment += f"\n{quantity} X {part.number}"

        lines = self.comment.split("\n")
        lines[0] += f" (ROOM: {room})"
        self.comment = "\n".join(lines)

    def __repr__(self) -> str:
        return f"{self.comment}"
