from typing import Tuple

import fileflow


class IntFile(fileflow.File):
    ...


class CustomFiletype(fileflow.File):
    ...


class CustomDatatype(fileflow.Saveable):
    def get_filetype():
        return CustomFiletype


my_workflow = fileflow.Workflow(fileflow.Config())
my_workflow.register_filetype(int, IntFile)
dummy_task = fileflow.Task(lambda: 42, (), {})


def test_futurize():
    from fileflow import Future

    out = my_workflow._futurize_type(
        Tuple[int, Tuple[CustomDatatype, int]], dummy_task
    )
    assert type(out) == tuple
    assert len(out) == 2
    assert out[0] == Future(IntFile, dummy_task, (0,))
    assert len(out[1]) == 2
    assert out[1][0] == Future(CustomFiletype, dummy_task, (1, 0))
    assert out[1][1] == Future(IntFile, dummy_task, (1, 1))

    out_2 = my_workflow._futurize_type(int, dummy_task)
    assert type(out_2) != tuple
    assert out_2 == Future(IntFile, dummy_task, ())


def test_task_decorator():
    
    @my_workflow.task
    def f(a, b) -> CustomDatatype:
        ...

    from fileflow import Future

    out = f(1, 2)
    task = my_workflow._tasks[0]
    # assert t.function == f
    assert task.args == (1, 2)
    assert out == Future(CustomFiletype, task, ())
