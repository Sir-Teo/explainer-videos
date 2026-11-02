"""Exercise actual Hook path interpolation with synthetic, uneven step lengths."""
import ast
from pathlib import Path
import unittest

import numpy as np

PART = Path(__file__).resolve().parents[1] / 'videos/ai/ai11'


class HookStepReplay(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        node = next(n for n in ast.parse((PART / 's01_hook.py').read_text()).body
                    if isinstance(n, ast.FunctionDef) and n.name == 'step_path')
        scope = {'np': np}
        exec(compile(ast.Module(body=[node], type_ignores=[]), '<actual-step-prefix>', 'exec'), scope)
        cls.prefix = staticmethod(scope['step_path'])

    def test_optimization_steps_are_independent_of_segment_lengths(self):
        points = np.array([[0., 0., 0.], [100., 0., 0.], [101., 1., 0.], [103., 1., 0.]])
        np.testing.assert_array_equal(self.prefix(points, 1), points[:2])
        np.testing.assert_allclose(self.prefix(points, 1.5)[-1], [100.5, .5, 0.])
        np.testing.assert_array_equal(self.prefix(points, 2), points[:3])
        np.testing.assert_array_equal(self.prefix(points, 3), points)

    def test_zero_and_clamped_endpoints_never_reveal_a_future_update(self):
        points = np.array([[3., 4., 5.], [8., 9., 10.], [30., 40., 50.]])
        for step in (-10, 0):
            np.testing.assert_array_equal(self.prefix(points, step), np.repeat(points[:1], 2, axis=0))
        np.testing.assert_array_equal(self.prefix(points, 900), points)
        original = points.copy()
        self.prefix(points, .25)
        np.testing.assert_array_equal(points, original)

    def test_scene_uses_one_six_second_clock_for_every_optimizer(self):
        fn = next(n for n in ast.walk(ast.parse((PART / 's01_hook.py').read_text()))
                  if isinstance(n, ast.FunctionDef) and n.name == 'race')
        calls = [n for n in ast.walk(fn) if isinstance(n, ast.Call)]
        self.assertFalse(any(isinstance(n.func, ast.Name) and n.func.id == 'MoveAlongPath' for n in calls))
        clock = [n for n in calls if isinstance(n.func, ast.Attribute) and n.func.attr == 'play'
                 and any(isinstance(k, ast.keyword) and k.arg == 'run_time' and isinstance(k.value, ast.Constant)
                         and k.value.value == 6.0 for k in n.keywords)]
        self.assertEqual(len(clock), 1)
        self.assertEqual(ast.unparse(clock[0].args[0]), 'step.animate.set_value(steps)')

    def test_counter_registers_replacement_glyphs_with_three_d_camera(self):
        node = next(n for n in ast.walk(ast.parse((PART / 's01_hook.py').read_text()))
                    if isinstance(n, ast.FunctionDef) and n.name == 'update_counter')

        class Camera:
            fixed = set()
            def add_fixed_in_frame_mobjects(self, mob):
                self.fixed.update(mob.glyphs)
            def remove_fixed_in_frame_mobjects(self, mob):
                self.fixed.difference_update(mob.glyphs)

        class Number:
            glyphs = [object()]
            def set_value(self, value):
                self.value = value
                self.glyphs = [object(), object()]
            def set_z_index(self, value):
                self.z_index = value
                return self

        class Scene:
            camera = Camera()

        class Clock:
            def get_value(self):
                return 41

        scene, number = Scene(), Number()
        previous = set(number.glyphs)
        scene.camera.add_fixed_in_frame_mobjects(number)
        scope = dict(self=scene, step=Clock())
        exec(compile(ast.Module(body=[node], type_ignores=[]), '<actual-counter-updater>', 'exec'), scope)
        scope['update_counter'](number)
        self.assertEqual(number.value, 41)
        self.assertEqual(number.z_index, 21)
        self.assertEqual(scene.camera.fixed, set(number.glyphs))
        self.assertTrue(scene.camera.fixed.isdisjoint(previous))

    def test_first_hit_cue_uses_inclusive_cached_step_and_handles_no_hit(self):
        fn = next(n for n in ast.walk(ast.parse((PART / 's01_hook.py').read_text()))
                  if isinstance(n, ast.FunctionDef) and n.name == 'race')
        cue = next(n for n in ast.walk(fn) if isinstance(n, ast.Lambda)
                   and isinstance(n.body, ast.Call) and isinstance(n.body.func, ast.Attribute)
                   and n.body.func.attr == 'set_opacity')

        class Clock:
            current = 0
            def get_value(self):
                return self.current

        class Badge:
            def set_opacity(self, value):
                return value

        step = Clock()
        env = dict(step=step, reach={'adam':30, 'never':-1}, n='adam')
        badge = eval(compile(ast.Expression(cue), '<actual-first-hit-cue>', 'eval'), env)
        for current, expected in [(0,0),(29.99,0),(30,1),(30.01,1),(150,1)]:
            step.current = current
            self.assertEqual(badge(Badge()), expected)
        self.assertEqual(badge(Badge(), n='never'), 0)

    def test_final_transition_does_not_fade_reached_counts_back_in(self):
        fn = next(n for n in ast.walk(ast.parse((PART / 's01_hook.py').read_text()))
                  if isinstance(n, ast.FunctionDef) and n.name == 'race')
        calls = [n for n in ast.walk(fn) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                 and n.func.attr == 'play']
        final = next(n for n in calls if any(isinstance(a, ast.Call) and isinstance(a.func, ast.Name)
                                            and a.func.id == 'FadeOut' for a in n.args))
        scope = dict(counter='clock', tally=['hit-count','not-yet'], names=['hit','never'],
                     reach={'hit':30,'never':-1}, FadeIn=lambda m:('in',m), FadeOut=lambda m:('out',m))
        actions = eval(compile(ast.fix_missing_locations(ast.Expression(ast.Tuple(elts=final.args,ctx=ast.Load()))),
                               '<actual-final-transition>', 'eval'),scope)
        self.assertEqual(actions,(('out','clock'),('in','not-yet')))


if __name__ == '__main__':
    unittest.main()
