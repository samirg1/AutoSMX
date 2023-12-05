from typeguard import check_type

from db.get_connection import get_connection
from design.Script import Script
from design.ScriptInfo import ScriptInfo
from design.ScriptLine import ScriptLine
from utils.constants import DatabaseFilenames


def get_script(script_info: ScriptInfo) -> Script:
    with get_connection(DatabaseFilenames.LOOKUP) as connection:
        res = check_type(
            connection.execute(
                """
                SELECT script_name, service_type
                FROM SCMOBILESCRIPTSM1
                WHERE script_no = ?;
                """,
                (script_info.number,),
            ).fetchone(),
            tuple[str, str] | None,
        )

        if res is None:
            raise ValueError

        script_name, service_type = res

        script_line_fields = check_type(
            connection.execute(
                """
                SELECT z_rv, script_line_text, line_no, answer_type, answer_id
                FROM SCMobileScriptLinesm1
                WHERE script_no = ?
                ORDER BY win32_page, win32_order;
                """,
                (script_info.number,),
            ).fetchall(),
            list[tuple[int, str, float, str | None, str | None]],
        )

        lines: list[ScriptLine] = []
        header_lines: list[ScriptLine] = []
        for z_rv, text, line_no, answer_type, answer_id in script_line_fields:
            if "header" in (answer_type, answer_id):
                header_lines.append(ScriptLine(text, int(line_no), z_rv))
                continue

            if z_rv == 8236:
                answer_id = script_line_fields[0][-1]
                answer_type = script_line_fields[0][-1]

            raw: list[tuple[str]] = []
            for possible_id in (answer_id, answer_type):
                if raw := check_type(
                    connection.execute(
                        """
                        SELECT answer_text
                        FROM SCMobileAnswers
                        WHERE answer_id == ?
                        ORDER BY z_rv;
                        """,
                        (possible_id,),
                    ).fetchall(),
                    list[tuple[str]],
                ):
                    break

            line = ScriptLine(text, int(line_no), z_rv, *(text[0] for text in raw), required=(z_rv in script_info.required_fields), use_saved=(z_rv not in script_info.non_persistent_fields))
            if script_info.condition_line is not None and z_rv == script_info.condition_line:
                line.default = "1"
                line.required = True
                line.use_saved = False
            else:
                line.default = script_info.line_defaults.get(z_rv, line.default)

            lines.append(line)

    return Script(
        script_info.nickname,
        script_name,
        script_info.number,
        script_info.tester_number,
        service_type,
        tuple(lines),
        tuple(header_lines),
        search_terms=script_info.search_terms,
        exact_matches=script_info.exact_matches,
    )
