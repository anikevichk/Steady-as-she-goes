import pytest
import matplotlib
import numpy as np
from classes import Map, Path
import matplotlib.pyplot as plt

@pytest.fixture
def map_instance():
    return Map(10, 2.0)

@pytest.fixture
def path_instance(map_instance):
    return Path(map_instance, 10)

"""tests: calling Errors"""
def test_invalid_n():
    with pytest.raises(TypeError):
        map_instance = Map(5, -3.0)

def test_invalid_draught():
    with pytest.raises(TypeError):
        map_instance = Map(-5, 0.2)

"""tests for function create_map_random"""
def test_create_map_random_shape(map_instance):
    map_matrix = map_instance.create_map_random()
    assert map_matrix.shape == (10, 10)

def test_create_map_random_values(map_instance):
    map_matrix = map_instance.create_map_random()
    assert all(value in [-4, -1, 1, 10] for value in map_matrix.flatten())

"""tests for function plot_map"""
def test_plot_map_output(map_instance):
    plt.figure()
    map_instance.plot_map()
    assert True

def test_plot_map_color(map_instance):
    polygon_face_colors = []
    polygons = []

    plt.figure()
    map_instance.plot_map()

    current_axis = plt.gca()
    all_children = current_axis.get_children()

    for child in all_children:
        if isinstance(child, plt.Polygon):
            polygons.append(child)

    for polygon in polygons:
        face_color = polygon.get_facecolor()
        polygon_face_colors.append(face_color)

    assert (np.array_equal(color, "LemonChiffon") for color in polygon_face_colors)

"""tests for function is_valid_cell"""
def test_is_valid_cell_valid(map_instance):
    if map_instance.map_matrix[3, 3] == -4:
        assert map_instance.is_valid_cell(3, 3)
    else:
       assert map_instance.is_valid_cell(3, 3) == False 

def test_is_valid_cell_valid_with_zero(map_instance):
    assert map_instance.is_valid_cell(0, 0)

def test_is_valid_cell_out_of_bounds(map_instance):
    assert map_instance.is_valid_cell(10, 10) is False

"""tests for function get_neighbors"""
def test_get_neighbors_invalid_cell():
    map_instance = Map(5, 0.2)
    neighbors = map_instance.get_neighbors((-1, -1))
    assert neighbors == []

def test_get_neighbors_valid_cell(map_instance):
    neighbors = map_instance.get_neighbors((1, 1))
    expected_neighbors = [(0, 1), (1, 0), (1, 2), (2, 1)]

    assert  list.sort(neighbors) == list.sort(expected_neighbors)

def test_get_neighbors_corner_cell(map_instance):
    neighbors = map_instance.get_neighbors((0, 9))
    expected_neighbors = [(0, 8), (1, 9)]
    assert list.sort(neighbors) == list.sort(expected_neighbors)


