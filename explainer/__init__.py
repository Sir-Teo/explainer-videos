"""Shared toolkit for 3Blue1Brown-style explainer videos.

    from explainer import *          # manim + style + VoiceoverScene
"""

from manim import *  # noqa: F401,F403

from .style import C, BACKGROUND, TEX_TEMPLATE  # noqa: F401
from .voiceover import VoiceoverScene  # noqa: F401
