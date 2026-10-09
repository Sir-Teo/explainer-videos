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
    BLUE_B,
    GOLD,
    GOLD_A,
    GREEN,
    GREEN_A,
    GREEN_B,
    GREY_A,
    GREY_B,
    GREY_D,
    LIGHT_BROWN,
    LIGHT_PINK,
    MAROON,
    ORANGE,
    PINK,
    PURPLE,
    PURPLE_A,
    PURPLE_B,
    RED,
    RED_B,
    TEAL,
    TEAL_B,
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
    # The Riemann hypothesis (videos/riemann)
    PRIME=BLUE,  # primes, prime staircases pi(x) and psi(x), Eisenstein primes
    SMOOTH=GREEN,  # the smooth prediction: li(x), x, R(x)
    ZERO=YELLOW,  # nontrivial zeros, the critical line, the waves they create
    ZERO_FREE=TEAL,  # proven zero-free regions (incl. the 7/8 half-plane)
    DANGER=RED,  # hypothetical zeros off the line, Landau-Siegel zeros
    MOBIUS=PURPLE_B,  # mu(n), Mertens' M(x), Möbius sums A_u(D)
    CHARACTER=ORANGE,  # Dirichlet characters, residue symbols chi_n(u)
    GAUSS=LIGHT_PINK,  # Gauss sums
    THETA=GOLD,  # theta functions, automorphy, the "reflection"
    SIEVE=GREEN_A,  # the large sieve, near-orthogonality
    # Open frontier models (videos/open_models).  Reuses the LLM colors above for
    # tokens, the residual stream, q/k/v, attention weights and FFNs.
    MIMO="#FF9F5A",  # Xiaomi MiMo-V2.6-Pro (model identity: tags, chart series)
    GLM="#6EA8FE",  # Z.ai GLM-5.3
    KIMI="#D4A5FF",  # Moonshot Kimi K3
    EXPERT=PURPLE_B,  # routed experts (an FFN, so the MLP color)
    SHARED_EXPERT=PURPLE_A,  # always-on shared experts
    ROUTER=GOLD,  # router scores, expert selection
    BALANCE=LIGHT_BROWN,  # load-balancing biases, expert load
    LOCAL=TEAL_B,  # sliding-window (local) attention layers and windows
    GLOBAL=ORANGE,  # global (full) attention layers
    SINK="#B39C8E",  # attention-sink logits, attention that goes "nowhere"
    LATENT=GREEN_B,  # MLA's compressed latent KV
    INDEXER=PINK,  # DSA's lightning indexer, selected tokens
    MEMORY=GREEN,  # linear-attention / KDA recurrent state S
    DEPTH=ORANGE,  # attention over depth (attention residuals): it is attention
    QUANT=GREY_A,  # low-precision number formats
    # Training frontier models (videos/frontier)
    PAGE=GREY_B,  # raw web pages, HTML, Common Crawl
    KEPT=TEAL,  # text that survives filtering, the clean corpus
    REMOVED=RED,  # pages or text dropped by a filter
    DUP=ORANGE,  # near-duplicates, MinHash
    EDU=GOLD,  # quality / educational-value scores
    PARAMS=BLUE,  # model size N
    DATA=GREEN,  # training tokens D
    COMPUTE=YELLOW,  # FLOPs C
    LR=GOLD_A,  # learning rate, schedules
    ADAMW=BLUE_B,  # AdamW
    MUON=PINK,  # Muon, orthogonalized updates
    # EXPERT (PURPLE_B) is defined above, shared with videos/open_models
    SIGN_BIT=RED_B,  # floating-point layouts: sign
    EXP_BIT=GREEN_B,  # exponent
    MAN_BIT=BLUE_B,  # mantissa
    GPU=TEAL_B,  # accelerators
    WEIGHTS=BLUE,  # memory: parameters
    GRADS=ORANGE,  # memory: gradients; the backward pass
    OPT_STATE=PURPLE_B,  # memory: optimizer state (master weights, Adam moments)
    ACTS=GREEN,  # memory: activations; the forward pass
    COMM=YELLOW,  # communication between GPUs
    BUBBLE=GREY_D,  # idle time in a pipeline schedule
    REWARD=GREEN,  # correct answers, positive reward / advantage
    PENALTY=RED,  # wrong answers, negative advantage
    RL_POLICY=BLUE,  # the model being trained by RL
    REFERENCE=GREY_B,  # the frozen reference model, KL anchor
    USER=BLUE_B,  # chat: user turns
    ASSISTANT=GREEN_B,  # chat: assistant turns (the trained tokens)
    # Reinforcement learning, derived (videos/rl).  Reuses RL_POLICY (pi_theta), REFERENCE (pi_ref),
    # REWARD (R, correct) and PENALTY (wrong, negative) from above.
    OLD_POLICY=TEAL,  # pi_old: the policy that sampled the batch; the inference engine
    ADVANTAGE=YELLOW,  # A, advantages (individual signs use REWARD / PENALTY)
    SCORE=ORANGE,  # the score function grad log pi, gradient arrows
    BASELINE=PURPLE_A,  # baselines b, values V(s), the critic
    RATIO=PINK,  # importance ratios rho = pi_theta / pi_old
    KL=GOLD,  # KL divergence, beta: the leash to the reference
    ENTROPY=LIGHT_PINK,  # entropy H
    LENGTH=LIGHT_BROWN,  # answer length |o|, token counts
    PROMPT_TOK=GREY_A,  # prompt tokens
    WORK_TOK="#9DD6F0",  # "showing the work" tokens (the scratchpad)
    # Stochastic calculus (videos/stochastic)
    BROWNIAN=BLUE,  # W_t, Brownian paths, dW, the noise term sigma dW
    CLOCK=TEAL,  # time t, dt, Delta t
    QV=YELLOW,  # (dW)^2, quadratic variation, Ito's correction 1/2 f'' dt, the "missing half"
    DRIFT=GREEN,  # mu, drift, mu dt
    STAKE=PURPLE_B,  # the integrand H: a stake, a position, a hedge ratio
    GAINS=GOLD,  # the Ito integral, accumulated gains
    LEFT_PT=GREEN_B,  # left-endpoint (Ito) sums
    RIGHT_PT=RED_B,  # right-endpoint sums (they peek at the future)
    MID_PT=PINK,  # midpoint / trapezoid sums (Stratonovich)
    PDF=ORANGE,  # probability densities, histograms, Fokker-Planck solutions
    MEAN=WHITE,  # expectations, the mean path
    MEDIAN=TEAL_B,  # the median / typical path
    LANDSCAPE=GREY_B,  # potentials V(x), domains, boundaries
    OPTION=PURPLE_A,  # option value V(t, S), payoffs
    HEDGE=LIGHT_BROWN,  # the hedge portfolio
    WEIGHT="#FF7EB6",  # Girsanov likelihood ratios, path weights
    HOT="#F2A541",  # boundary temperature 1 (Dirichlet problem)
    COLD="#3D5A98",  # boundary temperature 0
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
\DeclareMathOperator{\li}{li}
\DeclareMathOperator{\Real}{Re}
\DeclareMathOperator{\Imag}{Im}
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
