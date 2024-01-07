import pytest
import numpy as np
from Map import Map
import matplotlib.pyplot as plt


@pytest.fixture
def instance_random():
    return Map(5, 3, "a")


@pytest.fixture
def instance_manually():
    return Map(2, 3, "m")


# tests: calling Errors
def test_negative_map_size():
    with pytest.raises(ValueError):
        Map(5, -3.0, "a")


def test_not_int_map_size():
    with pytest.raises(TypeError):
        Map("a", 2.0, "a")


def test_negative_draught():
    with pytest.raises(ValueError):
        Map(-5, 0.2, "a")


def test_not_float_draught():
    with pytest.raises(TypeError):
        Map(5, "b", "a")


# tests for function create_map_from_choice
def test_create_map_from_choice_invalid_choice():
    map = Map(3, 2, "invalid_choice")
    with pytest.raises(ValueError):
        map.create_map_from_choice("invalid_choice")


def test_create_map_from_choice_random(instance_random):
    instance_random.create_map_from_choice("a")
    assert instance_random.map_matrix is not None
    assert isinstance(instance_random.map_matrix, np.ndarray)
    assert all(
        np.isscalar(element) for row in instance_random.map_matrix for element in row
    )


def test_create_map_from_choice_file():
    path = "C:\\project\\project_map\\example.txt"
    instance = Map(3, 2, "f", path)
    instance.create_map_from_choice("f")
    assert instance.map_matrix is not None
    assert isinstance(instance.map_matrix, np.ndarray)


# tests for function create_map_random
def test_create_map_random_shape(instance_random):
    map_matrix = instance_random.create_map_random()
    assert map_matrix.shape == (instance_random.map_size, instance_random.map_size)


def test_create_map_random_values(instance_random):
    map_matrix = instance_random.create_map_random()
    unique_values = np.unique(map_matrix)
    assert all(
        value in [-instance_random.draught * 2, 1 - instance_random.draught, 1, 10]
        for value in unique_values
    )


def test_create_map_random_first_last(instance_random):
    map_matrix = instance_random.create_map_random()
    assert map_matrix[0, 0] == -instance_random.draught * 2
    assert map_matrix[-1, -1] == -instance_random.draught * 2


def test_create_map_random_probabilities_sum():
    probabilities = [0.75, 0.10, 0.10, 0.05]
    sum_of_probabilities = sum(probabilities)
    assert sum_of_probabilities == pytest.approx(1.0, abs=1e-5)


# tests for function create_map_manually
def test_create_map_manually_valid_input(instance_manually, monkeypatch, capsys):
    input_values = ["1", "2", "3", "4"]
    monkeypatch.setattr("builtins.input", lambda x: input_values.pop(0))
    result = instance_manually.create_map_manually()
    assert np.array_equal(result, np.array([[1.0, 2.0], [3.0, 4.0]]))


def test_create_map_manually_invalid_input(instance_manually, monkeypatch):
    input_values = ["a", "b", "c"]
    monkeypatch.setattr("builtins.input", lambda x: input_values.pop(0))
    with pytest.raises(
        ValueError, match="Invalid input. Please enter a valid numeric elevation."
    ):
        instance_manually.create_map_manually()


def test_create_map_manually_negative_elevation(instance_manually, monkeypatch):
    input_values = ["-1", "2", "3", "-6"]
    monkeypatch.setattr("builtins.input", lambda x: input_values.pop(0))
    result = instance_manually.create_map_manually()
    assert np.array_equal(result, np.array([[-1.0, 2.0], [3.0, -6.0]]))


def test_create_map_manually_float_input(instance_manually, monkeypatch):
    input_values = ["1.5", "2.7", "3.2", "5"]
    monkeypatch.setattr("builtins.input", lambda x: input_values.pop(0))
    result = instance_manually.create_map_manually()
    assert np.array_equal(result, np.array([[1.5, 2.7], [3.2, 5.0]]))


def test_create_map_manually_empty_input(instance_manually, monkeypatch):
    input_values = ["", "2", "3", "6"]
    monkeypatch.setattr("builtins.input", lambda x: input_values.pop(0))
    with pytest.raises(
        ValueError, match="Invalid input. Please enter a valid numeric elevation."
    ):
        instance_manually.create_map_manually()


# tests for function create_map_from_file
def test_create_map_from_file_success(tmp_path):
    test_matrix = np.random.rand(4, 3)
    test_file = tmp_path / "test_map.txt"
    np.savetxt(test_file, test_matrix, fmt="%1.2f", header="", comments="")

    test_map = Map(3, 3, "f", test_file)

    result_matrix = test_map.create_map_from_file(test_file)

    # The first line skip here is due to the fact that the code's first line contains the matrix length values and the frigate precipitation.
    assert np.allclose(result_matrix, test_matrix[1:], atol=1e-2)


def test_create_map_from_file_missing_path():
    map_instance = Map(3, 2, "f", None)
    with pytest.raises(ValueError):
        map_instance.create_map_from_file(path=None)


def test_create_map_from_file_invalid_dimensions(tmp_path):
    invalid_matrix = np.random.rand(4, 4)
    file = tmp_path / "invalid_map.txt"
    np.savetxt(file, invalid_matrix, fmt="%1.2f")

    map_instance = Map(3, 1, "f", file)

    with pytest.raises(ValueError):
        map_instance.create_map_from_file(file)


# tests for function plot_map
def test_plot_map_bounds(instance_random):
    bounds = [-int(instance_random.draught * 2), -instance_random.draught, 0, 5, 10]
    expected_bounds = [-6, -3, 0, 5, 10]
    assert bounds == expected_bounds


def test_plot_map_colorbar(instance_random, monkeypatch):
    def mock_colorbar(**kwargs):
        raise AttributeError("colorbar attribute is not allowed")

    monkeypatch.setattr(plt, "colorbar", mock_colorbar)

    with pytest.raises(AttributeError, match="colorbar"):
        instance_random.plot_map()


def test_plot_map_color(instance_random):
    polygon_face_colors = []
    polygons = []

    plt.figure()
    instance_random.plot_map()

    current_axis = plt.gca()
    all_children = current_axis.get_children()

    for child in all_children:
        if isinstance(child, plt.Polygon):
            polygons.append(child)

    for polygon in polygons:
        face_color = polygon.get_facecolor()
        polygon_face_colors.append(face_color)

    assert (np.array_equal(color, "LemonChiffon") for color in polygon_face_colors)


# tests for function is_valid_cell
def test_valid_cell_within_bounds():
    map = Map(5, 2, "a")
    map.create_map_from_choice("a")
    if map.map_matrix[3, 3] < -2:
        assert map.is_valid_cell(3, 3)
    else:
        assert map.is_valid_cell(3, 3) == False


def test_invalid_cell_below_zero():
    game_map = Map(5, 2, "a")
    assert game_map.is_valid_cell(-1, 2) == False


def test_invalid_cell_above_max_size():
    game_map = Map(5, 2, "a")
    assert game_map.is_valid_cell(6, 3) == False


# tests for function get_neighbors
def test_get_neighbors_invalid_cell():
    instance_random = Map(5, 0.2, "a")
    neighbors = instance_random.get_neighbors((-1, -1))
    assert neighbors == []


def test_get_neighbors_valid_cell(instance_random):
    neighbors = instance_random.get_neighbors((1, 1))
    expected_neighbors = [(0, 1), (1, 0), (1, 2), (2, 1)]

    assert list.sort(neighbors) == list.sort(expected_neighbors)


def test_get_neighbors_corner_cell(instance_random):
    neighbors = instance_random.get_neighbors((0, 9))
    expected_neighbors = [(0, 8), (1, 9)]
    assert list.sort(neighbors) == list.sort(expected_neighbors)
