class TestJob:
    def __init__(self, department: str, contact_name: str, comment: str):
        self.department = department
        self.contact_name = contact_name
        self.comment = comment

    def __str__(self) -> str:
        return f"{self.comment}"
