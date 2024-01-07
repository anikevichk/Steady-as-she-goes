import pytest
from Path import Path
from Map import Map
import numpy as np
from PathNotFound import PathNotFound


@pytest.fixture
def map_instance():
    return Map(5, 1.5, "m")


# tests for function find_path


def test_find_path_single_path():
    start = (0, 0)
    end = (2, 2)

    map = Map(2, 2.0, "a")
    path = Path(map, 2)
    path.find_path(start, end)
    if path.first_path is None:
        assert "There is no valid path"
    else:
        assert path.path_of_matrix is not None


def test_find_path_no_path(map_instance):
    start = (0, 0)
    end = (4, 4)
    map_instance.map_matrix[1][1] = 1.0
    path_instance = Path(map_instance, map_instance.map_size)
    path = path_instance.find_path(start, end)
    assert path is None


def test_find_path_same_start_and_end(map_instance):
    start = (0, 0)
    end = (0, 0)
    path_instance = Path(map_instance, map_instance.map_size)
    path = path_instance.find_path(start, end)
    assert path == [(0, 0)]


# tests for function find_paths


def test_find_paths_no_paths(map_instance):
    map_instance.map_matrix = np.array(
        [
            [0, 0, 0, 0, 0],
            [0, -2, -2, -2, 0],
            [0, -2, -2, -2, 0],
            [0, -2, -2, -2, 0],
            [0, 0, 0, 0, 0],
        ]
    )

    path_instance = Path(map_instance, map_instance.map_size)
    with pytest.raises(PathNotFound):
        path_instance.find_paths()


def test_find_paths_different_paths(map_instance):
    map_instance.map_matrix = np.array(
        [
            [-5, -5, -5, -5, -5],
            [-5, 0, 0, 0, -5],
            [-5, 0, 0, 0, -5],
            [-5, 0, 0, 0, -5],
            [-5, -5, -5, -5, -5],
        ]
    )

    path_instance = Path(map_instance, map_instance.map_size)
    result_path = path_instance.find_paths()

    assert type(result_path) is tuple
    assert set(path_instance.first_path) != set(path_instance.second_path)


def test_find_paths_same_paths(map_instance):
    map_instance.map_matrix = np.array(
        [
            [-5, 0, -5, -5, -5],
            [-5, 0, 0, 0, -5],
            [-5, 0, 0, 0, -5],
            [-5, 0, 0, 0, -5],
            [-5, -5, -5, -5, -5],
        ]
    )
    path_instance = Path(map_instance, map_instance.map_size)
    result_path = path_instance.find_paths()

    assert type(result_path) is not tuple


# tests for function reconstruct_path
def test_reconstruct_path_none():
    path_instance = Path(None, 5)
    visited = {(0, 0): None, (0, 1): (0, 0), (1, 1): (0, 1)}
    end = (2, 2)
    assert path_instance.reconstruct_path(visited, end) is None


def test_reconstruct_path_valid():
    path_instance = Path(None, 3)
    visited = {(0, 0): None, (0, 1): (0, 0), (1, 1): (0, 1), (2, 2): (1, 1)}
    end = (2, 2)
    expected_path = [(2, 2), (1, 1), (0, 1), (0, 0)]
    assert path_instance.reconstruct_path(visited, end) == expected_path


def test_reconstruct_path_same_start_and_end():
    path_instance = Path(None, 3)
    visited = {(0, 0): None, (0, 1): (0, 0), (1, 1): (0, 1)}
    end = (0, 0)
    expected_path = [(0, 0)]
    assert path_instance.reconstruct_path(visited, end) == expected_path


def test_reconstruct_path_empty_visited():
    path_instance = Path(None, 3)
    visited = {}
    end = (2, 2)
    assert path_instance.reconstruct_path(visited, end) is None
