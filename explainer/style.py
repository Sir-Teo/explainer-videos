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
    GOLD,
    GOLD_A,
    GREEN,
    GREEN_A,
    GREY_A,
    GREY_B,
    GREY_D,
    MAROON,
    ORANGE,
    LIGHT_BROWN,
    PINK,
    PURPLE,
    PURPLE_A,
    PURPLE_B,
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
    # Language models (videos/llm)
    TOKEN=GREY_A,  # token boxes, raw text
    EMBED=BLUE,  # token vectors, the residual stream
    POSITION=PINK,  # positional information
    QUERY=YELLOW,  # q = W_Q x, "what am I looking for?"
    KEY=TEAL,  # k = W_K x, "what do I contain?"
    VALUE=RED,  # v = W_V x, the information that gets moved
    ATTN=ORANGE,  # attention scores, weights, patterns
    MLP=PURPLE_B,  # feed-forward layers, neurons
    PROB=GREEN,  # logits, probabilities, predictions
    LOSS=MAROON,  # training loss, -log p
    NORM=GREY_B,  # layer norm
    # Markets and macro (videos/opposing_forces)
    EARNINGS=GREEN,  # E, earnings per share, profit growth, margins
    MULTIPLE=ORANGE,  # P/E, earnings yield, valuation
    PRICE=BLUE,  # index level P = E x P/E; the cap-weighted S&P 500
    EQUAL_WEIGHT=GOLD_A,  # the equal-weighted S&P 500, "the average stock", breadth
    RATE=RED,  # nominal Treasury yields, the discount rate r, the cost of capital
    REAL_RATE=PINK,  # real (TIPS) yields
    INFLATION=GREY_B,  # breakeven inflation
    TERM_PREMIUM=PURPLE_A,  # extra yield for lending long
    POLICY=TEAL,  # the Fed's policy rate and its expected path
    DEBT=LIGHT_BROWN,  # government debt, deficits, interest costs
    GROWTH=GREEN_A,  # GDP growth g, potential growth
    MORTGAGE=GOLD,  # mortgage rates, MBS
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
\DeclareMathOperator{\softmax}{softmax}
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
