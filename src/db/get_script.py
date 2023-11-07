from db.get_connection import DatabaseFilenames, get_connection
from design.Script import Script, ScriptLine
from design.ScriptInfo import ScriptInfo


def get_script(script_info: ScriptInfo, line_defaults: dict[int, str], condition_lines: set[int], required_lines: set[int]) -> Script:
    with get_connection(DatabaseFilenames.LOOKUP) as connection:
        script_name, service_type = connection.execute(
            """
            SELECT script_name, service_type
            FROM SCMOBILESCRIPTSM1
            WHERE script_no = ?;
            """,
            (script_info.number,),
        ).fetchone()

        script_line_fields: list[tuple[int, str, float, str, str]] = connection.execute(
            """
            SELECT z_rv, script_line_text, line_no, answer_type, answer_id
            FROM SCMobileScriptLinesm1
            WHERE script_no = ?
            ORDER BY win32_page, win32_order;
            """,
            (script_info.number,),
        ).fetchall()

        lines: list[ScriptLine] = []
        for z_rv, text, line_no, answer_type, answer_id in script_line_fields:
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
                    ORDER BY z_rv;
                    """,
                    (possible_id,),
                ).fetchall():
                    break
            
            line = ScriptLine(text, int(line_no), *(text[0] for text in raw), required=(z_rv in required_lines))
            if z_rv in condition_lines:
                line.default = "1"
            else:
                line.default = line_defaults.get(z_rv, line.default)

            lines.append(line)

    return Script(
        script_info.nickname, script_name, script_info.number, script_info.tester_number, service_type, tuple(lines), search_terms=script_info.search_terms, exact_matches=script_info.exact_matches
    )
