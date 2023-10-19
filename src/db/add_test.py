from datetime import datetime

from db.get_connection import get_connection, DatabaseFilenames
from db.test_models import TestModel, ScriptLineModel, ScriptTesterModel
from db.get_user import get_user
from design.Test import Test
from design.Job import Job
from design.Item import Item


class NoTestIDsError(RuntimeError):
    ...


def _get_new_test_id() -> str:
    with get_connection(DatabaseFilenames.SETTINGS) as connection:
        res: tuple[str, int, int] | None = connection.execute("""
            SELECT TABLENAME, LASTUSED, LASTRESERVED
            FROM SCMIDTABLE
            WHERE TABLENAME == 'SCMobileTestsm1' AND LASTUSED <> LASTRESERVED;
        """).fetchone()

    if res is None:
        raise NoTestIDsError
    
    _, current, end = res

    with get_connection(DatabaseFilenames.SETTINGS, mode="rw") as connection:
        # with connection:
        connection.execute("""
        UPDATE SCMIDTABLE
        SET LASTUSED = ?
        WHERE TABLENAME == 'SCMobileTestsm1' AND LASTRESERVED = ?;
        """, (current+1, end))
    
    return f"SMX{str(current+1).zfill(10)}"


def add_test(test: Test, job: Job) -> None:
    user = get_user()
    test_id = _get_new_test_id()
    time = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S.%f")[:-3]

    test_model = TestModel(
        test_id=test_id,
        logical_name=test.item.number,
        customer_barcode=test.item.number,
        test_date=time,
        sysmoduser=user,
        problem_number=job.number,
        user_name=user,
        comments=test.comment,
        customer_id=str(job.customer_number),
        company_name=job.company,
        location=job.campus,
        dept=job.department,
        overall=test.final_result,
        room=test.item.room,
        model=test.item.model,
        manufacturer=test.item.manufacturer,
        description=test.item.description,
        serial_no_=test.item.serial,
        sysmodtime=time,
    )

    script_model = ScriptTesterModel(
        test_id=test_id,
        script_number=test.script.number,
        tester_number=test.script.tester_number,
    )

    with get_connection(DatabaseFilenames.TESTS, mode="rw") as connection:
        # with connection:
        connection.execute(
            f"""
            INSERT INTO SCMobileTestsm1 {test_model.fields()}
            VALUES (?{', ?'*(len(test_model.__annotations__)-1)});
            """, 
            test_model.values()
        )

        connection.execute(
            f"""
            INSERT INTO SCMobileTesterNumbersm1 {script_model.fields()}
            VALUES (?{', ?'*(len(script_model.__annotations__)-1)});
            """, 
            script_model.values()
        )

        for line, result in zip(test.script.lines, test.script_answers):
            set_point = 200 if test.script.number == 1287 and line.number == 5 else None
            script_line_model = ScriptLineModel(
                test_id=test_id,
                script_number=test.script.number,
                script_line=line.number,
                result=result,
                performed_by=user,
                script_line_text=line.text,
                set_point=set_point
            )

            connection.execute(
                f"""
                INSERT INTO SCMobileTestLinesm1 {script_line_model.fields()}
                VALUES (?{', ?'*(len(script_line_model.__annotations__)-1)});
                """,
                script_line_model.values()
            )

        # test_id = 'SMX0001391907'


        res = connection.execute(f"""
            SELECT * from SCMobileTestsm1 WHERE test_id == '{test_id}'
        """)

        print(list(zip((d[0] for d in res.description), res.fetchone())))
        print()

        res = connection.execute(f"""
            SELECT * from SCMobileTesterNumbersm1 WHERE test_id == '{test_id}'
        """)

        print(list(zip((d[0] for d in res.description), res.fetchone())))
        print()
        
        res = connection.execute(f"""
            SELECT * from SCMobileTestLinesm1 WHERE test_id == '{test_id}'
        """)
        descs = [d[0] for d in res.description]

        for r in res.fetchall():
            print(list(zip(descs, r)))

if __name__ == "__main__":
    t = Test(item=Item("123456", "BED", "model", "manu", "serial", "room", None))
    t.script = t.determine_script()
    t.complete("comment", "final_res", ["pass"] * len(t.script.lines))


    add_test(t, Job("company", "campus", "dept", "pm12345", 1))
        