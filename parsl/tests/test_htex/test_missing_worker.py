import pytest

import parsl
from parsl.app.app import python_app
from parsl.tests.configs.htex_local import fresh_config


def local_config():
    config = fresh_config()
    config.executors[0].poll_period = 1
    config.executors[0].max_workers_per_node = 1
    config.executors[0].launch_cmd = "executable_that_hopefully_does_not_exist_1030509.py"
    return config


@python_app
def dummy():
    pass


@pytest.mark.local
def test_that_it_fails():
    x = dummy()
    failed = False
    try:
        x.result()
    except Exception as ex:
        print(ex)
        failed = True
    if not failed:
        raise Exception("The app somehow ran without a valid worker")

    assert parsl.dfk().config.executors[0]._executor_bad_state.is_set()
