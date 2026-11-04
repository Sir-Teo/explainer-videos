"""The field plot paints, tags and frames its plots."""

import numpy as np

from explainer.stats import FieldPlot


def test_field_plot():
    f = FieldPlot(4, 6, cell=0.4)
    assert len(f.cells) == 4 and len(f.cells[0]) == 6
    assert f.cells[0][0].get_x() < f.cells[0][5].get_x() and f.cells[0][0].get_y() > f.cells[3][0].get_y()
    v = np.arange(24.0).reshape(4, 6)
    f.painted(v)
    assert f.cells[0][0].get_fill_color().to_hex().lower() == FieldPlot.SOIL.lower()
    alloc = np.zeros((4, 6), int)
    alloc[0, 0] = -1
    assert len(f.tags(alloc)) == 23
    box = f.outline(0, 3, 0, 1)
    assert abs(box.get_center()[0] - (f.cells[0][0].get_x() + f.cells[0][1].get_x()) / 2) < 1e-6
    f.paint(v)
