def task_run_test():
    from test import tests

    return {
        'actions': [tests, "coverage run test.py", "coverage xml"]
    }

def task_lint_modules():
    return {
        'actions': ["pylint modules"]
    }

def task_bazel_build():
    return {
        'actions': ["bazel build //:Skat"]
    }

def task_create_html():
    return {
        'actions': ["make html"]
    }

def task_create_pdf():
    return {
        'actions': ["make pdf"]
    }