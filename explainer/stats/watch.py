"""The watch kit of *Statistics, Built* (videos/stats/SYLLABUS.md, section 1.2): what turns an hour of lecture into a
film you want to keep watching.

    from explainer.stats import *

    class Principle(StatsScene):
        def construct(self):
            self.chapter(1, r"The principle", r"Minimize the sum of squared misses", lit=(1805,), part=PART)
            self.ask(r"Which line do the squares choose?", [r"through the median", r"through the means",
                     r"through the extremes"], 1, say="Before we start: where must the best line pass?",
                     reveal="Through the means: the first normal equation says the residuals sum to zero.")
            self.squares()          # the chapter, as it was
            ...
            self.answer()           # the prediction, answered once the chapter has shown it

* :class:`StatsScene`: a narrated ``MovingCameraScene`` whose every plain ``FadeIn`` is given the entrance its content
  suggests (:func:`lively`: arrows grow, lines and curves draw, short formulas write themselves, small groups arrive
  part by part); :meth:`~StatsScene.zoom` and :meth:`~StatsScene.home` move the camera;
* :meth:`~StatsScene.chapter`: the chapter card, animated: the title writes itself, the timeline strip draws from
  1650 to 2030 and the chapter's years flash; the score's sting plays under it;
* :meth:`~StatsScene.title`: after the cold open, the part's name and its place in the degree (sixty-five dots in
  five stages, the milestones as diamonds), in silence under the series' theme;
* :meth:`~StatsScene.ask` / :meth:`~StatsScene.answer`: the chapter's prediction. The viewer commits to an answer
  (two to four options, a three-second countdown) before the chapter shows it, and the card comes back at the end of
  the chapter with the right option lit;
* :meth:`~StatsScene.checkpoint`: two short questions about every fifteen minutes, a pause, and the answers;
* :meth:`~StatsScene.wrong_idea`: a misconception, stated, struck through, and replaced by the right idea;
* :meth:`~StatsScene.rewrite`: a derivation played in one place, each line morphing into the next.

The set pieces record marks (``card``, ``title``, ``countdown:N``, ``reveal``, ``strike``) in each scene's
``.narration.json``; the score (:mod:`explainer.stats.score`) places its cues on them.  ``EXPLAINER_PLAIN_FADES=1``
turns :func:`lively` off.  ``tools/check_watch.py statsN`` counts the set pieces from the source.
"""

from __future__ import annotations

import os

import numpy as np
from manim import *  # noqa: F403

from explainer.stats.style import S
from explainer.voiceover import VoiceoverScene

FRAME_W = 14.222222222222221
CARD_BG = "#0B0F17"
PREDICT = S.ACCENT      # the question: the series' gold
GOOD = S.KEPT           # the right answer: the Board's "kept"
BAD = S.BROKEN          # the wrong idea: the Board's "broken"
CHECK = S.EST           # the checkpoint: theta-hat's blue (you, estimating what you know)
LETTERS = "ABCD"
NUMBER_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
                "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty",
                "twenty-one", "twenty-two", "twenty-three", "twenty-four", "twenty-five"]
SHORT_TEX = 44  # characters of TeX source a label may have and still be written stroke by stroke


def _label(text, **kw):
    from explainer.analysis import label

    return label(text, **kw)


def _wrapped(text, width, **kw):
    from explainer.analysis import wrapped_label

    return wrapped_label(text, width, **kw)


def _lines(text, width, font_size=30, color=WHITE) -> VGroup:
    """``text`` broken at word boundaries (outside math) into lines no wider than ``width``, each its own label, so a
    strike-through can cross each line."""
    from explainer.analysis import _tex_words, _wrapped_lines, label

    one = label(text, font_size=font_size, color=color)
    if one.width <= width:
        return VGroup(one)
    lines = _wrapped_lines(_tex_words(text), width, lambda s: label(s, font_size=font_size).width)
    g = VGroup(*[label(ln, font_size=font_size, color=color) for ln in lines]).arrange(DOWN, buff=0.16,
                                                                                         aligned_edge=LEFT)
    if g.width > width:
        g.width = width
    return g


def _chip(text: str, color, font_size=16) -> VGroup:
    t = Text(text, font="DejaVu Sans", font_size=font_size, weight=BOLD, color=CARD_BG)
    b = RoundedRectangle(width=t.width + 0.32, height=0.34, corner_radius=0.1, stroke_width=0, fill_color=color,
                         fill_opacity=1)
    g = VGroup(b, t.move_to(b))
    g.box, g.text = b, t
    return g


# ---------------------------------------------------------------------------- entrances
def lively(anim, top=True):
    """A plain ``FadeIn``, given the entrance its content suggests: an arrow grows from its tail; a line, arc or
    plotted curve is drawn along its length; a short one-line label or formula is written; a group of a few parts
    arrives part by part, each with its own entrance.  The end state is the same, so layouts are untouched; anything
    else keeps its fade.  ``EXPLAINER_PLAIN_FADES=1`` turns this off."""
    if os.environ.get("EXPLAINER_PLAIN_FADES") or type(anim) is not FadeIn:
        return anim
    m = anim.mobject
    kw = {"run_time": anim.run_time, "rate_func": anim.rate_func}
    if isinstance(m, Arrow):
        return GrowArrow(m, **kw)
    if isinstance(m, (Line, Arc, ParametricFunction)) and not isinstance(m, (Dot, Circle)):
        return Create(m, **kw)
    if isinstance(m, MathTex):
        src = m.tex_string
        if len(src) <= SHORT_TEX and "\\\\" not in src and any(
                g.get_fill_opacity() > 0 for g in m.family_members_with_points()):
            return Write(m, **kw)
        return anim
    if top and type(m) is VGroup and 2 <= len(m.submobjects) <= 40:
        parts = [lively(FadeIn(c, shift=0.08 * UP), top=False) for c in m.submobjects]
        return LaggedStart(*parts, lag_ratio=0.25, run_time=anim.run_time)
    return anim


def countdown_ring(seconds=3, radius=0.34, color=PREDICT):
    """A ring that empties over ``seconds`` with the whole seconds left inside it.  Returns ``(ring, tracker)``:
    animate ``tracker`` from 0 to 1."""
    t = ValueTracker(0.0)
    base = Circle(radius=radius, stroke_color=GREY_D, stroke_width=3)
    ring = always_redraw(lambda: Arc(radius=base.width / 2, start_angle=PI / 2,
                                     angle=-TAU * max(1e-4, 1 - t.get_value()), arc_center=base.get_center(),
                                     stroke_color=color, stroke_width=5 * base.width / (2 * radius)))
    num = Integer(seconds, font_size=26, color=color)
    num.add_updater(lambda m: m.set_value(int(np.ceil(seconds * (1 - t.get_value()) - 1e-6))).move_to(base))
    return VGroup(base, ring, num), t


# ---------------------------------------------------------------------------- cards
def _option(letter: str, text: str, font_size=26, width=None) -> VGroup:
    disc = Circle(radius=0.22, stroke_color=PREDICT, stroke_width=2, fill_color=PREDICT, fill_opacity=0.12)
    lt = Text(letter, font="DejaVu Sans", font_size=20, weight=BOLD, color=PREDICT).move_to(disc)
    body = _label(text, font_size=font_size, color=WHITE)
    if body.width > 10.4:
        body.width = 10.4
    row = VGroup(VGroup(disc, lt), body).arrange(RIGHT, buff=0.22)
    w = width or row.width + 0.4
    box = RoundedRectangle(width=w, height=row.height + 0.24, corner_radius=0.14, stroke_color=GREY_D,
                           stroke_width=1.2, fill_color=WHITE, fill_opacity=0.03)
    row.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.18)
    g = VGroup(box, row)
    g.box, g.disc, g.body = box, VGroup(disc, lt), body
    return g


def predict_card(question: str, options, font_size=26, max_width=12.6) -> VGroup:
    """The prediction: a "Predict" chip, the question, and lettered options.  ``card.options[k]`` is option k."""
    head = _chip("PREDICT", PREDICT)
    q = _wrapped(question, 11.2, font_size=font_size + 4, color=WHITE)
    probe = [_option(LETTERS[k], o, font_size=font_size) for k, o in enumerate(options)]
    ow = max(o.width for o in probe)
    opts = VGroup(*[_option(LETTERS[k], o, font_size=font_size, width=ow) for k, o in enumerate(options)])
    opts.arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    body = VGroup(head, q, opts).arrange(DOWN, buff=0.26, aligned_edge=LEFT)
    panel = RoundedRectangle(width=body.width + 0.6, height=body.height + 0.5, corner_radius=0.2, stroke_color=PREDICT,
                             stroke_width=2, fill_color=CARD_BG, fill_opacity=0.95)
    body.move_to(panel).align_to(panel, LEFT).shift(RIGHT * 0.3)
    card = VGroup(panel, body)
    if card.width > max_width:
        card.width = max_width
    if card.height > 7.2:
        card.height = 7.2
    card.panel, card.head, card.question, card.options = panel, head, q, opts
    return card


def degree_strip(part: int, width=12.4, font_size=20) -> VGroup:
    """The sixty-five parts as dots in five stage groups: parts before ``part`` filled, ``part`` lit and larger,
    the four milestones (BSc, MSc, candidacy, PhD) as diamonds, and the current stage named beneath its group."""
    from explainer.stats import MILESTONES, STAGES

    groups = VGroup()
    here = None
    for name, (a, b) in STAGES:
        grp = VGroup()
        for n in range(a, b + 1):
            if n in MILESTONES:
                d = Square(0.13, stroke_width=1.5).rotate(PI / 4)
                d.set_stroke(S.ACCENT if n <= part else GREY_C)
                d.set_fill(S.ACCENT if n == part else (GREY_B if n < part else CARD_BG), opacity=1)
                if n == part:
                    d.scale(1.6)
            elif n == part:
                d = Dot(radius=0.11, color=S.ACCENT)
            elif n < part:
                d = Dot(radius=0.055, color=GREY_B)
            else:
                d = Circle(radius=0.055, stroke_color=GREY_D, stroke_width=1.5)
            grp.add(d)
        grp.arrange(RIGHT, buff=0.07)
        groups.add(grp)
        if a <= part <= b:
            here = (name, grp, part - a)
    groups.arrange(RIGHT, buff=0.3)
    if groups.width > width:
        groups.width = width
    name, grp, k = here
    text = name.split(r".\ ", 1)[-1]
    lab = _label(text, font_size=font_size, color=S.ACCENT)
    rule = Line(grp.get_left(), grp.get_right(), color=S.ACCENT, stroke_width=2).next_to(grp, DOWN, buff=0.1)
    lab.next_to(rule, DOWN, buff=0.14)
    if lab.get_left()[0] < groups.get_left()[0]:  # the first and last stages: keep the name under the strip
        lab.align_to(groups, LEFT)
    if lab.get_right()[0] > groups.get_right()[0]:
        lab.align_to(groups, RIGHT)
    out = VGroup(groups, rule, lab)
    out.groups, out.rule, out.stage_label, out.current = groups, rule, lab, grp[k]
    return out


# ---------------------------------------------------------------------------- the scene
class StatsScene(VoiceoverScene, MovingCameraScene):
    """A narrated scene with a camera, livelier entrances, and the watch kit's set pieces."""

    def play(self, *anims, **kw):
        return super().play(*[lively(a) for a in anims], **kw)

    # ------------------------------------------------------------------ the camera
    def frame_center(self):
        return self.camera.frame.get_center()

    def frame_scale(self) -> float:
        return self.camera.frame.width / FRAME_W

    def zoom(self, target, margin=1.3, width=None, run_time=1.6, **kw):
        """Move the camera onto ``target`` (a mobject or point); :meth:`home` brings it back."""
        from explainer.ai.viz import frame_to

        self.play(frame_to(self, target, width=width, margin=margin), run_time=run_time, **kw)

    def home(self, run_time=1.2):
        from explainer.ai.viz import frame_home

        self.play(frame_home(self), run_time=run_time)

    def _fit(self, mob):
        """Scale ``mob`` to the camera's zoom and centre it in the current frame."""
        return mob.scale(self.frame_scale()).move_to(self.frame_center())

    def clear_scene(self, *keep, extra=(), run_time: float = 1.0, home: bool = True):
        """Fade everything but ``keep`` (never the camera's frame), bringing the camera home at the same time."""
        from explainer.ai.viz import frame_home

        f = self.camera.frame
        if f in self.mobjects:
            self.remove(f)
        moved = abs(f.width - FRAME_W) > 1e-3 or np.linalg.norm(f.get_center()) > 1e-3
        extra = list(extra) + ([frame_home(self)] if home and moved else [])
        super().clear_scene(*keep, extra=extra, run_time=run_time)

    def _on_screen(self) -> list:
        return [m for m in self.mobjects if m is not self.camera.frame and m.get_family()]

    # ------------------------------------------------------------------ chapter cards
    def chapter(self, number, title: str, question: str = "", lit=(), part=None, said: str | None = None):
        """The chapter card, animated, spoken, then sent off to the left: the heading drops in, the title writes
        itself, the question rises, the timeline strip draws from 1650 to 2030 and the chapter's years flash.
        ``said`` is the line the narration speaks; by default "Chapter seven. The bootstrap."."""
        from explainer.stats import chapter_card

        card = chapter_card(number, title, question, lit=lit, part=part)
        text, strip = card
        if said is None:
            plain = " ".join(title.replace("\\\\", " ").replace("\\ ", " ").replace("$", "").split())
            said = f"Chapter {NUMBER_WORDS[number] if number < len(NUMBER_WORDS) else number}. {plain}."
        lit_dots = [m for m in strip.submobjects if isinstance(m, Dot) and m.radius > 0.05]
        rest = [m for m in strip.submobjects if m is not strip[0]]
        self.mark("card")
        with self.voiceover(said):
            entr = [FadeIn(text[0], shift=DOWN * 0.15), Write(text[1], run_time=1.1)]
            if len(text) > 2:
                entr.append(FadeIn(text[2], shift=UP * 0.15))
            self.play(LaggedStart(*entr, lag_ratio=0.3), Create(strip[0], run_time=1.2),
                      LaggedStart(*[FadeIn(m) for m in rest], lag_ratio=0.02, run_time=1.4), run_time=1.6)
            if lit_dots:
                self.play(*[Flash(d, color=S.ACCENT, line_length=0.14, flash_radius=0.16, run_time=0.6)
                            for d in lit_dots])
        self.play(FadeOut(card, shift=LEFT * 0.6), run_time=0.6)

    # ------------------------------------------------------------------ the title, after the cold open
    def title(self, part: int, subtitle: str = "", hold: float = 1.6):
        """The part's name and its place in the degree, about seven seconds, in silence: the series' theme plays."""
        from explainer.ai import zh
        from explainer.stats import PARTS, SERIES_EN, SERIES_ZH

        if self._on_screen():
            self.clear_scene()
        top = _label(SERIES_ZH if zh() else SERIES_EN, font_size=26, color=GREY_B)
        num = _label(rf"第{part}部分" if zh() else rf"Part {part}", font_size=30, color=S.ACCENT)
        name = _label(PARTS[part], font_size=64, color=WHITE)
        if name.width > 12.8:
            name.width = 12.8
        g = VGroup(top, num, name).arrange(DOWN, buff=0.22)
        if subtitle:
            g.add(_label(subtitle, font_size=28, color=GREY_A).next_to(name, DOWN, buff=0.3))
        strip = degree_strip(part)
        g.move_to(UP * 0.9)
        strip.next_to(g, DOWN, buff=0.55)
        whole = self._fit(VGroup(g, strip))
        self.mark("title")
        self.play(LaggedStart(FadeIn(top, shift=DOWN * 0.15), FadeIn(num, shift=DOWN * 0.15), Write(name),
                              lag_ratio=0.35), run_time=2.0)
        dots = [d for grp in strip.groups for d in grp]
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.015), Create(strip.rule),
                  FadeIn(strip.stage_label, shift=UP * 0.1), run_time=1.8)
        self.play(Flash(strip.current, color=S.ACCENT, line_length=0.18, flash_radius=0.24), run_time=0.8)
        self.wait(hold)
        self.play(FadeOut(whole, shift=UP * 0.3), run_time=0.8)

    # ------------------------------------------------------------------ predictions
    def predict(self, question: str, options, narration: str | None = None, seconds: float = 3.0, font_size=26):
        """Ask, count down, and return the card (still on screen); answer it with :meth:`reveal`.  The narration
        asks the question aloud; the countdown runs in silence, over the score's clicks."""
        card = self._fit(predict_card(question, options, font_size=font_size))
        ring, t = countdown_ring(int(seconds))
        ring.scale(self.frame_scale()).next_to(card.head, RIGHT, buff=0.3 * self.frame_scale())
        s = self.frame_scale()
        anims = [FadeIn(card.panel, scale=0.96), FadeIn(card.head, shift=DOWN * 0.1 * s),
                 FadeIn(card.question, shift=UP * 0.1 * s),
                 LaggedStart(*[FadeIn(o, shift=LEFT * 0.2 * s) for o in card.options], lag_ratio=0.25)]
        if narration:
            with self.voiceover(narration):
                self.play(LaggedStart(*anims, lag_ratio=0.2), run_time=1.4)
        else:
            self.play(LaggedStart(*anims, lag_ratio=0.2), run_time=1.4)
        self.add(ring)
        self.mark(f"countdown:{int(seconds)}")
        self.play(t.animate.set_value(1.0), run_time=seconds, rate_func=linear)
        for m in ring.get_family():
            m.clear_updaters()
        self.remove(ring)
        return card

    def reveal(self, card, answer: int, narration: str | None = None, keep: bool = False):
        """Light the right option, dim the others (the score's chime), then (unless ``keep``) send the card away."""
        good = card.options[answer]
        anims = [good.box.animate.set_stroke(GOOD, width=3).set_fill(GOOD, opacity=0.18),
                 good.disc[0].animate.set_fill(GOOD, opacity=1).set_stroke(GOOD),
                 good.disc[1].animate.set_color(CARD_BG)]
        for k, o in enumerate(card.options):
            if k != answer:
                anims += [o.box.animate.set_stroke(opacity=0.35), o.body.animate.set_opacity(0.3),
                          o.disc.animate.set_opacity(0.3)]
        if narration:
            with self.voiceover(narration):
                self.mark("reveal")
                self.play(*anims, run_time=0.8)
                self.play(Indicate(good, color=GOOD, scale_factor=1.04))
        else:
            self.mark("reveal")
            self.play(*anims, run_time=0.8)
        if not keep:
            self.play(FadeOut(card, shift=RIGHT * 0.3 * self.frame_scale()), run_time=0.7)

    def ask(self, question: str, options, answer: int, say: str | None = None, reveal: str | None = None,
            seconds: float = 3.0):
        """The chapter's prediction: ask it (``say`` aloud), count down, and put the card away; :meth:`answer`
        brings it back at the end of the chapter, after the chapter has shown the result, and reveals it (``reveal``
        aloud)."""
        if self._on_screen():
            self.clear_scene()
        card = self.predict(question, options, narration=say, seconds=seconds)
        card.save_state()
        self.play(card.animate.scale(0.3).move_to(self.frame_center() + np.array([6.2, 3.2, 0]) * self.frame_scale())
                  .set_opacity(0), run_time=0.7)
        self.remove(card)
        self._asked = (card, answer, reveal)
        return card

    def answer(self):
        """Bring back the chapter's prediction and answer it: the screen clears, the card returns, the right option
        lights up."""
        asked = getattr(self, "_asked", None)
        if asked is None:
            return
        self._asked = None
        card, answer, narration = asked
        if self._on_screen():
            self.clear_scene()
        self.add(card)
        self.play(Restore(card), run_time=0.7)
        self.reveal(card, answer, narration=narration)

    # ------------------------------------------------------------------ checkpoints
    def checkpoint(self, items, narration: str | None = None, answers_narration: str | None = None,
                   seconds: float = 4.0, font_size=28):
        """Two (or three) short questions, a pause to answer, then the answers.  ``items`` are (question, answer)
        pairs of on-screen text."""
        if self._on_screen():
            self.clear_scene()
        s = self.frame_scale()
        head = _chip("CHECKPOINT", CHECK, font_size=18)
        qs, ans = VGroup(), VGroup()
        for k, (q, a) in enumerate(items):
            n = Text(f"{k + 1}", font="DejaVu Sans", font_size=24, weight=BOLD, color=CHECK)
            qt = _wrapped(q, 10.6, font_size=font_size, color=WHITE)
            row = VGroup(n, qt).arrange(RIGHT, buff=0.3, aligned_edge=UP)
            at = _wrapped(a, 10.6, font_size=font_size - 4, color=GOOD).next_to(qt, DOWN, buff=0.16,
                                                                                  aligned_edge=LEFT)
            qs.add(row)
            ans.add(at)
        block = VGroup(*[VGroup(q, a) for q, a in zip(qs, ans)]).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        body = VGroup(head, block).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        panel = RoundedRectangle(width=max(9.5, body.width + 1.0), height=body.height + 0.8, corner_radius=0.22,
                                 stroke_color=CHECK, stroke_width=2, fill_color=CARD_BG, fill_opacity=0.97)
        body.move_to(panel)
        card = VGroup(panel, body)
        if card.width > 13.4:
            card.width = 13.4
        if card.height > 7.4:
            card.height = 7.4
        self._fit(card)
        ring, t = countdown_ring(int(seconds), color=CHECK)
        ring.scale(s).next_to(head, RIGHT, buff=0.35 * s)
        shown = VGroup(panel, head, *qs)
        if narration:
            with self.voiceover(narration):
                self.play(FadeIn(panel, scale=0.96), FadeIn(head), run_time=0.6)
                self.play(LaggedStart(*[FadeIn(q, shift=UP * 0.1 * s) for q in qs], lag_ratio=0.5), run_time=1.2)
        else:
            self.play(FadeIn(panel, scale=0.96), FadeIn(head), LaggedStart(*[FadeIn(q) for q in qs], lag_ratio=0.4))
        self.add(ring)
        self.mark(f"countdown:{int(seconds)}")
        self.play(t.animate.set_value(1.0), run_time=seconds, rate_func=linear)
        for m in ring.get_family():
            m.clear_updaters()
        self.remove(ring)
        self.mark("reveal")
        if answers_narration:
            with self.voiceover(answers_narration):
                self.play(LaggedStart(*[Write(a) for a in ans], lag_ratio=0.6), run_time=2.0)
        else:
            self.play(LaggedStart(*[Write(a) for a in ans], lag_ratio=0.6), run_time=2.0)
        self.wait(0.6)
        self.play(FadeOut(VGroup(shown, ans), scale=0.97), run_time=0.6)

    # ------------------------------------------------------------------ the misconception
    def wrong_idea(self, wrong: str, right: str, narration: str | None = None, right_narration: str | None = None,
                   font_size=32, hold: float = 1.0, keep: bool = False):
        """State the misconception, strike it through (the score's thud), and turn it into the right idea; then
        clear it away unless ``keep``."""
        if self._on_screen():
            self.clear_scene()
        s = self.frame_scale()
        chip = _chip("WRONG IDEA", BAD, font_size=18)
        w = _lines(wrong, 11.0, font_size=font_size, color=WHITE)
        r = _lines(right, 11.0, font_size=font_size, color=GOOD)
        VGroup(chip, w).arrange(DOWN, buff=0.35).scale(s).move_to(self.frame_center())
        r.scale(s).move_to(w)
        new_chip = _chip("RIGHT IDEA", GOOD, font_size=18).scale(s)
        w_end = w.copy().scale(0.62).set_opacity(0.4).next_to(r, UP, buff=0.3 * s)
        new_chip.next_to(w_end, UP, buff=0.25 * s)
        whole = VGroup(chip, w, r, w_end, new_chip)
        whole.shift(self.frame_center() - whole.get_center())
        panel = RoundedRectangle(width=whole.width + 1.2 * s, height=whole.height + 0.8 * s, corner_radius=0.2 * s,
                                 stroke_color=GREY_D, stroke_width=1.5, fill_color=CARD_BG,
                                 fill_opacity=0.96).move_to(whole)
        self.play(FadeIn(panel, scale=0.97), run_time=0.4)
        strike = VGroup(*[Line(ln.get_left() + LEFT * 0.08 * s, ln.get_right() + RIGHT * 0.08 * s, color=BAD,
                               stroke_width=4 * s) for ln in w])
        if narration:
            with self.voiceover(narration):
                self.play(FadeIn(chip, shift=DOWN * 0.1 * s), FadeIn(w), run_time=1.0)
        else:
            self.play(FadeIn(chip), FadeIn(w))
        k_end = strike.copy().scale(0.62).move_to(w_end)
        if right_narration:
            with self.voiceover(right_narration):
                self.mark("strike")
                self.play(Create(strike), w.animate.set_opacity(0.4), run_time=0.6)
                self.play(Transform(w, w_end), Transform(strike, k_end), Transform(chip, new_chip),
                          FadeIn(r, shift=UP * 0.3 * s), run_time=1.0)
        else:
            self.mark("strike")
            self.play(Create(strike), w.animate.set_opacity(0.4))
            self.play(Transform(w, w_end), Transform(strike, k_end), Transform(chip, new_chip),
                      FadeIn(r, shift=UP * 0.3 * s))
        group = VGroup(panel, chip, w, strike, r)
        if keep:
            return group
        self.wait(hold)
        self.play(FadeOut(group, scale=0.97), run_time=0.6)
        return group

    # ------------------------------------------------------------------ derivations in place
    def rewrite(self, terms, focus=None, run_time: float = 0.9, hold: float = 0.25, first=None):
        """A chain of terms (a derivation's lines) played in one place: each morphs into the next, its shared
        symbols flying to their new places, instead of a stack of lines fading in.  ``focus(k)`` may return the
        submobject of ``terms[k]`` rewritten next: it is boxed before the step.  Returns the last term, on screen."""
        terms = list(terms)
        place = terms[0].get_center()
        for t in terms[1:]:
            t.move_to(place)
        cur = terms[0]
        self.play(first(cur) if first else lively(FadeIn(cur)), run_time=0.8)
        for k, nxt in enumerate(terms[1:]):
            part = focus(k) if focus else None
            if part is not None:
                box = SurroundingRectangle(part, color=PREDICT, buff=0.06, stroke_width=3)
                self.play(Create(box), run_time=0.35)
                self.play(FadeOut(box), run_time=0.2)
            self.play(TransformMatchingShapes(cur, nxt, path_arc=0.6), run_time=run_time)
            cur = nxt
            if hold:
                self.wait(hold)
        return cur
