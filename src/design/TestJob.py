class TestJob:
    def __init__(self, department: str, contact_name: str, description: str):
        self.department = department
        self.contact_name = contact_name
        self.description = description

    def __str__(self) -> str:
        return f"{self.description}"