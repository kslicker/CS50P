from project import distance, generate_random_coords, generate_random_coords_top_pipes


def test_distance():
    assert distance(5, 5, 10, 10) == 7.0710678118654755

def test_generate_random_coords():
    result = generate_random_coords(800)
    assert  600 <= result[0] <= 800, 275 <= result[1] <= 350

def test_generate_random_coords_top_pipes():
    result = generate_random_coords_top_pipes(800)
    assert  600 <= result[0] <= 800, -300 <= result[1] <= -175