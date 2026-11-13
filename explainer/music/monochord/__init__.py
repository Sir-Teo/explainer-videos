"""Monochord: the instrument *Music, Built* builds, one layer per part (videos/music/SYLLABUS.md, 2.1).

It starts as one simulated string and grows into an orchestra, a studio and a set of listening machines.  Nothing here
imports manim: the labs and the tests use it directly, and the films only draw what it computes.

* :mod:`.audio`: the :class:`Clip` (samples at 48 kHz with named events), mixing, fades, WAV files, the clip store;
* :mod:`.loudness`: ITU-R BS.1770 loudness and a true-peak estimate, used to set and to check levels (the meter is
  derived on screen in Part 57; the films need it from Part 1 to keep their own levels honest);
* :mod:`.pitch`: frequencies, ratios, cents and note names;
* :mod:`.dsp`: spectra, partial tracking, a fundamental-frequency estimate (Part 3 derives them);
* :mod:`.physics.string`: the string of Part 1 by finite differences and by modes.

Every layer is checked against something that does not share its code (``tests/music/``).
"""

from .audio import SR, Clip, ClipStore, concat, mix, silence  # noqa: F401
