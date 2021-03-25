name = "DccSocketServer"

version = "0.0.0"


description = \
    """
    dcc socket server python
    """

requires = [
    "python-3.7.7",
    "PyYAML-5.4.1",
    "os",
    "Sphinx",
    "sphinx_rtd_theme",
    "sphinx_markdown_builder",
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
    env.PYTHONPATH.append("{root}/src")


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