from db.get_connection import get_connection
from design.Script import Script, ScriptLine


def get_script(script_number: int) -> Script:
    with get_connection("SCMLookup") as connection:
        script_name = connection.execute(
            """
            SELECT script_name
            FROM SCMOBILESCRIPTSM1
            WHERE script_no = ?
        """,
            (script_number,),
        ).fetchone()[0]

        script_line_fields: list[tuple[int, str, str, str]] = connection.execute(
            """
            SELECT z_rv, script_line_text, answer_type, answer_id
            FROM SCMobileScriptLinesm1
            WHERE script_no = ?
            ORDER BY win32_page, win32_order
            """,
            (script_number,),
        ).fetchall()

        lines: list[ScriptLine] = []
        for z_rv, text, answer_type, answer_id in script_line_fields:
            if "header" in (answer_type, answer_id):
                continue

            if z_rv == 8236:
                answer_id = script_line_fields[0][-1]
                answer_type = script_line_fields[0][-1]

            raw: list[tuple[str]] = []
            for possible_id in (answer_id, answer_type):
                if raw := connection.execute(
                    """
                    SELECT answer_text
                    FROM SCMobileAnswers
                    WHERE answer_id == ?
                    ORDER BY z_rv
                    """,
                    (possible_id,),
                ).fetchall():
                    break

            lines.append(ScriptLine(text, *(text[0] for text in raw)))

    return Script(script_name, script_name, script_number, tuple(lines))
