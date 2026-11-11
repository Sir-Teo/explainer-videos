"""Exercise the scene's real redraw constructors through the sample-size animation."""
import ast
from pathlib import Path

import numpy as np
from manim import Axes, GREY_B, ValueTracker, always_redraw

from videos.quant.quant6.common import ALT, EST, ellipse_curve


def test_all_three_confidence_regions_contract_about_the_estimate():
    source = Path('videos/quant/quant6/s08_mle.py').read_text()
    tree = ast.parse(source)
    method = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == 'ellipses')
    names = {'e_naive', 'e_opg', 'e_hac'}
    constructors = [n for n in method.body if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id in names for t in n.targets)]
    ax = Axes(x_range=[1.9, 3.0], y_range=[0.53, 0.62], tips=False)
    ctr = np.array([2.45, 0.575])
    covariance = np.array([[0.000001, 0.000003], [0.000003, 0.0001]])
    tracker = ValueTracker(1)
    scope = dict(ax=ax, ctr=ctr, sw=lambda v: np.asarray(v)[::-1, ::-1],
                 m={key: covariance * scale for key, scale in
                    [('V_naive', 1), ('V_sandwich', 1.4), ('V_hac', 4)]},
                 Tf=tracker, clip=((1.9, 3.0), (0.53, 0.62)),
                 always_redraw=always_redraw, ellipse_curve=ellipse_curve,
                 EST=EST, ALT=ALT, GREY_B=GREY_B)
    exec(compile(ast.Module(body=constructors, type_ignores=[]), '<scene constructors>', 'exec'), scope)
    assert all(name in scope for name in names)
    origin = ax.c2p(*ctr)
    reference = {name: scope[name].points.copy() for name in names}
    # Includes intermediate frames, the doubled sample, and the quadrupled sample.
    for multiplier in sorted(set(np.linspace(1, 4, 25)) | {2.0}):
        tracker.set_value(multiplier)
        for name in names:
            region = scope[name]
            region.update(0)
            np.testing.assert_allclose(region.points - origin,
                                       (reference[name] - origin) / np.sqrt(multiplier), atol=1e-12)
