name = "dccSocketServer"

version = "0.0.0"


description = \
    """
    dcc socket server python
    """

requires = [
    # ONLY PY2 library
]


tools = [
    "doc_md",
    "doc_html",
]


build_command = False
timestamp = 0


def commands():
    env.PATH.append("{root}/src")
    env.PATH.append("{root}")
    env.PYTHONPATH.append('C:/Maya2019/Python/Lib/site-packages')
    env.MAYA_SCRIPT_PATH.append("{root}/src")


vcs = "git"
# ------------------------ TESTS -----------------------


def pre_test_commands():
    if test.name == "unit":
        env.IS_UNIT_TEST = 1
        env.PYTHONPATH.append("{root}/src/tests")


tests = {
    "unit": {
        "command": "python -m unittest discover -s {root}/src/tests"
    }
}