class TestJob:
    def __init__(self, department: str, contact_name: str | None):
        self.department = department
        self.contact_name = contact_name or input("Enter contact name: ")
        self.description = input("Enter job description: ")