"""Helpers shared by the scenes of Part 4 ("Change")."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import BOWL_P0, bowl, bowl_grad, lag_f, load  # noqa: F401

PART = 4
MONO = "DejaVu Sans Mono"
HIST = C.HUMAN  # history cards
VALUE, GRAD = "#58A6FF", "#FF9F45"  # values flow forward (blue), gradients flow back (orange)
