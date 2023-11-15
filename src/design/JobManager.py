from design.Item import Item
from design.Job import Job
from design.Problem import Problem


class JobManager:
    def __init__(self) -> None:
        self.problem_to_jobs: dict[Problem, list[Job]] = {}
        self.job_to_item: dict[Job, Item] = {}

    def add_job(self, item: Item, problem: Problem, job: Job) -> None:
        self.problem_to_jobs.setdefault(problem, []).append(job)
        self.job_to_item[job] = item

    def delete_job(self, problem: Problem, job: Job) -> None:
        self.problem_to_jobs[problem].pop()
        del self.job_to_item[job]

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, JobManager):
            return self.__dict__ == __value.__dict__
        return NotImplemented
