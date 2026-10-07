"""Shared visual language for every video in this repo.

The single most important 3Blue1Brown-style habit is *consistent color coding*:
once a concept gets a color, it keeps that color for the whole video (and
ideally across videos).  Scenes should import semantic names from here
(``C.VELOCITY``) instead of hard-coding hex values, so the palette can be
tuned in one place.
"""

from __future__ import annotations

from types import SimpleNamespace

from manim import (
    BLUE,
    GREEN,
    GREY_A,
    GREY_B,
    GREY_D,
    ORANGE,
    PURPLE,
    RED,
    TEAL,
    WHITE,
    YELLOW,
    Tex,
    TexTemplate,
    MathTex,
    config,
)

BACKGROUND = "#0E1117"

# ---------------------------------------------------------------------------
# Semantic palette
# ---------------------------------------------------------------------------
C = SimpleNamespace(
    # Fields / quantities
    VELOCITY=BLUE,  # u, velocity arrows, streamlines
    PRESSURE=RED,  # p, -grad p, pressure forces
    DENSITY=GREY_A,  # rho
    VISCOUS=GREEN,  # mu, nu, Laplacian term
    TIME=TEAL,  # partial u / partial t
    ADVECT=YELLOW,  # (u . grad) u, the nonlinear term
    FORCE=PURPLE,  # external body force f
    DIVERGENCE=ORANGE,  # div u, incompressibility
    VORTICITY=ORANGE,  # omega (shares the "spin" family color)
    REYNOLDS=YELLOW,
    # UI
    TEXT=WHITE,
    DIM=GREY_B,
    FAINT=GREY_D,
    HIGHLIGHT=YELLOW,
)

# Colormap anchor colors (used by explainer.fluids.colormaps)
PRESSURE_LOW = "#1B2A6B"
PRESSURE_HIGH = "#E8533F"
VORT_NEG = "#3BA7E0"
VORT_POS = "#F08A3C"

# ---------------------------------------------------------------------------
# LaTeX
# ---------------------------------------------------------------------------
TEX_TEMPLATE = TexTemplate()
TEX_TEMPLATE.add_to_preamble(
    r"""
\usepackage{amsmath,amssymb,bm}
\newcommand{\vu}{\mathbf{u}}
\newcommand{\vx}{\mathbf{x}}
\newcommand{\vf}{\mathbf{f}}
\newcommand{\dd}{\partial}
"""
)
MathTex.set_default(tex_template=TEX_TEMPLATE)
Tex.set_default(tex_template=TEX_TEMPLATE)

# ---------------------------------------------------------------------------
# Typography helpers
# ---------------------------------------------------------------------------
TITLE_SIZE = 56
HEADER_SIZE = 44
BODY_SIZE = 36
LABEL_SIZE = 30
SMALL_SIZE = 24


def apply_global_config() -> None:
    config.background_color = BACKGROUND


apply_global_config()
