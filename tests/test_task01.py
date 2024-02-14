import project.task01
import filecmp
import os
import tempfile

dir_path = os.path.dirname(os.path.realpath(__file__))


def test_get_graph_info():
    (n, m, e) = project.task01.get_graph_info("people")
    assert n == 337
    assert m == 640


def test_labeled_two_cycles_graph_to_dot():
    with tempfile.NamedTemporaryFile() as tmp:
        path = tmp.name
    project.task01.labeled_two_cycles_graph_to_dot(10, 8, None, path)
    assert filecmp.cmp(f"{dir_path}/test_task01_data/10_8_graph.dot", path)
