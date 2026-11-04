"""The TankFactory picture (Part 9): captured serials are lit in the right cells."""

import numpy as np

from explainer.stats import TankFactory


def test_captured_marks_sit_on_their_serials():
    f = TankFactory(60, [3, 17, 60], cols=10, cell=0.2)
    assert len(f.tanks) == 60 and len(f.marks) == 3 and len(f.numbers) == 3
    for m, s_ in zip(f.marks, [3, 17, 60]):
        assert np.allclose(m.get_center(), f.tanks[s_ - 1].get_center())
    # serial 17 is row 1, column 6: one cell below and to the right of serial 6
    assert np.isclose(f.tanks[16].get_y(), f.tanks[5].get_y() - 0.2)


def test_capture_without_numbers_still_animates():
    f = TankFactory(40, [5, 9], show_numbers=False)
    anim = f.capture_anims()
    assert len(f.numbers) == 0 and anim.run_time > 0
