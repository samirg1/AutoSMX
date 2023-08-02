from typing import Callable

TRESOLVE = Callable[..., str]
RESOLVES: dict[str, TRESOLVE] = {
    "PASS": lambda: "PASS",
    "FAIL": lambda: "FAIL",
    "N/A": lambda: "N/A",
    "SKIP": lambda: "SKIP",
    "OPTION": lambda msg, pass_opt: "PASS" if bool(input(msg)) == pass_opt else "N/A",
    "1": lambda: "1",
    "N": lambda: "N",
    "NUMBER": lambda msg: input(msg),
}

TSCRIPT = tuple[TRESOLVE, ...]
SCRIPTS: dict[str, TSCRIPT] = {
    "BATTERY": (RESOLVES["PASS"], RESOLVES["PASS"], RESOLVES["PASS"]),
    "CHARGER": (RESOLVES["N/A"], RESOLVES["PASS"], RESOLVES["PASS"], RESOLVES["N/A"]),
}
