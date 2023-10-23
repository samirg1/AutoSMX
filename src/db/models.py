from abc import ABC, abstractmethod
from sqlite3 import Connection
from random import randrange

from design.Test import Test
from design.Problem import Problem
from design.Script import ScriptLine
from design.Job import Job


def rand_hex(n: int) -> str:
    return f"{randrange(16**n):0{n}x}".upper()


class Model(ABC):
    @property
    @abstractmethod
    def table_name(self) -> str:
        ...

    def insert(self, connection: Connection) -> None:
        connection.execute(
            f"""
            INSERT INTO {self.table_name} {f"({', '.join(self.__dict__.keys())})"}
            VALUES (?{', ?'*(len(self.__dict__)-1)});
            """,
            tuple(self.__dict__.values()),
        )


class TestModel(Model):
    @property
    def table_name(self) -> str:
        return "SCMobileTestsm1"

    def __init__(self, test: Test, problem: Problem):
        self.test_id = test.id
        self.logical_name = test.item.number
        self.customer_barcode = test.item.customer_barcode
        self.test_date = test.date
        self.sysmoduser = test.user
        self.problem_number = problem.number
        self.user_name = test.user
        self.comments = test.comments
        self.customer_id = problem.customer_number
        self.company_name = problem.company
        self.location = problem.campus
        self.dept = problem.department
        self.pointsync_id = None
        self.overall = test.result
        self.building = ""
        self.floor = ""
        self.room = test.item.room
        self.model = test.item.model
        self.manufacturer = test.item.manufacturer
        self.description = test.item.description
        self.serial_no_ = test.item.serial
        self.pointsync_time = None
        self.sysmodtime = test.date
        self.interfaced = None


class ScriptTesterModel(Model):
    @property
    def table_name(self) -> str:
        return "SCMobileTesterNumbersm1"

    def __init__(self, test: Test):
        self.test_id = test.id
        self.script_number = test.script.number
        self.tester_number = test.script.tester_number


class ScriptLineModel(Model):
    @property
    def table_name(self) -> str:
        return "SCMobileTestLinesm1"

    def __init__(self, test: Test, line: ScriptLine):
        self.test_id = test.id
        self.script_number = test.script.number
        self.script_line = line.number
        self.result = line.result
        self.comments = None
        self.date_performed = None
        self.performed_by = test.user
        self.script_line_text = line.text
        self.set_point = 200 if (test.script.number == 1287 and line.number == 5) else None
        self.page = None
        self.orderprgn = None


class JobModel(Model):
    @property
    def table_name(self) -> str:
        return "SCMProbsUploadm1"

    def __init__(self, test: Test, problem: Problem, job: Job) -> None:
        self.pointsync_id = "{" + f"{rand_hex(8)}-{rand_hex(4)}-{rand_hex(4)}-{rand_hex(4)}-{rand_hex(12)}" + "}"
        self.customer_no_ = problem.customer_number
        self.location = problem.campus
        self.building = None
        self.floor = None
        self.room = test.item.room
        self.category = None
        self.subcategory = None
        self.logical_name = test.item.number
        self.customer_barcode = test.item.customer_barcode
        self.actionprgn = job.comment
        self.assignment = None
        self.dept = job.department
        self.contact_name = job.contact_name
        self.contact_phone = None
        self.contact_email = None
        self.assignee_name = test.user
        self.asset_description = test.item.description
        self.opened_by = test.user
        self.link_to_problem = problem.number
        self.test_id = test.id
