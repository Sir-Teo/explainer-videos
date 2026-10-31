"""The constant-power VJP must not evaluate zero times a reciprocal at zero."""
import unittest

import numpy as np

from explainer.ai.autodiff import Tensor


class ConstantPowerTests(unittest.TestCase):
    def test_zero_input_and_scalar_exponent_types(self):
        for exponent in (0, 0.0, np.int64(0), np.float64(0)):
            with self.subTest(exponent=type(exponent).__name__), np.errstate(all="raise"):
                x = Tensor(0.0, requires_grad=True)
                y = x ** exponent
                y.backward()
                self.assertEqual(float(y.data), 1.0)
                self.assertEqual(float(x.grad), 0.0)

    def test_array_zero_power_with_nonuniform_incoming_gradient(self):
        with np.errstate(all="raise"):
            x = Tensor(np.array([[0., -2., 3.], [4., 0., -5.]]), requires_grad=True)
            weights = np.array([[1., 2., -3.], [7., -11., 13.]])
            y = x ** 0
            (y * weights).sum().backward()
            np.testing.assert_array_equal(y.data, np.ones_like(x.data))
            np.testing.assert_array_equal(x.grad, np.zeros_like(x.data))

    def test_constant_branch_composes_and_fan_in_keeps_other_gradient(self):
        with np.errstate(all="raise"):
            x = Tensor(np.array([0., -2., 3.]), requires_grad=True)
            shared = x * 2
            ((shared ** 0) * 17 + x ** 2 + 3 * x).sum().backward()
            np.testing.assert_array_equal(x.grad, 2 * x.data + 3)

    def test_constant_operation_keeps_requested_graph_path(self):
        x = Tensor([0., 2.], requires_grad=True)
        y = x ** 0
        self.assertTrue(y.requires_grad)
        self.assertEqual(len(y.parents), 1)
        y.sum().backward()
        np.testing.assert_array_equal(x.grad, [0., 0.])

    def test_nonzero_powers_and_numpy_scalar_exponents_are_unchanged(self):
        for exponent in (1, 2, np.int64(3), np.float64(0.5), -1.0):
            with self.subTest(exponent=exponent), np.errstate(all="raise"):
                x = Tensor([0.5, 2., 4.], requires_grad=True)
                y = x ** exponent
                y.sum().backward()
                np.testing.assert_allclose(y.data, x.data ** exponent)
                np.testing.assert_allclose(x.grad, exponent * x.data ** (exponent - 1))

    def test_array_exponent_existing_behavior_is_preserved(self):
        x = Tensor([1., 2., 3.], requires_grad=True)
        exponent = np.array([1., 2., 3.])
        (x ** exponent).sum().backward()
        np.testing.assert_allclose(x.grad, exponent * x.data ** (exponent - 1))

    def test_negative_power_at_zero_remains_undefined(self):
        # The repair handles the constant polynomial only. It must not silently
        # replace a pole with a finite value or derivative.
        with np.errstate(divide="ignore", invalid="ignore"):
            x = Tensor(0., requires_grad=True)
            y = x ** -1
            y.backward()
        self.assertTrue(np.isinf(y.data))
        self.assertTrue(np.isneginf(x.grad))


if __name__ == "__main__":
    unittest.main()
