"""Physical models: objects that vibrate, stepped forward by Newton's law.  Part 1: the string."""

from .string import (Run, String, dalembert, exact_rate, grid_for, modal, modal_bridge_force,  # noqa: F401
                     pluck_modes, pluck_shape, simulate, sine_coefficients)
