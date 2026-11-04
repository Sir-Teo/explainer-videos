"""Helpers shared by the scenes of Part 3 ("Logic from Switches")."""

from __future__ import annotations

from explainer.cs import *  # noqa: F403
from explainer.cs.gates import (GATE_FILL, GATE_STROKE, ONE, WIRE, ZERO, Relay, Switch, gate, ground, lamp,  # noqa: F401
                                light, live, nmos, pmos, rail, switch, wire)

from .compute import load  # noqa: F401

PART = 3

DATA = C.CS_DATA  # input signals
CTRL = C.CS_CONTROL  # gates, control
HEAD = C.CS_HEAD  # the current signal, the focus
CODE = C.CS_CODE  # expressions as written
FUNC = C.CS_FUNC  # functions
COST = C.CS_COST  # gate counts, delays, power
YES = C.CS_TRUE  # 1, high, conducting
NO = C.CS_FALSE  # 0 where it matters, a glitch, a failure
LIMIT = C.CS_LIMIT
INF = C.CS_INF
CLOCK = C.CS_CLOCK
HIST = C.HUMAN
VDD_COLOR = "#E5484D"


def fmt(n) -> str:
    return f"{int(n):,}".replace(",", "{,}")


def say(n) -> str:
    return f"{int(n):,}"


def bit_tex(v, font_size=34) -> MathTex:
    return MathTex(str(int(v)), font_size=font_size, color=YES if v else GREY_B)
