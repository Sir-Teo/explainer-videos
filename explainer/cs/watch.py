"""The watch standard's scene kit (videos/cs/SYLLABUS.md, section 1.2): what makes a fifty-minute lecture a film.

    from explainer.cs import *

    class Pipeline(WatchScene):
        def construct(self):
            card = self.predict("Which loop finishes first?", ["the random array", "the sorted array", "a tie"],
                                narration="Same loop, same numbers. Which finishes first?")
            ...                                    # the run that answers it
            self.reveal(card, 1, narration="The sorted one, by a factor of five.")

* :class:`WatchScene`: a narrated ``MovingCameraScene``.  :meth:`~WatchScene.zoom` and :meth:`~WatchScene.home`
  move the camera, and :meth:`~WatchScene.clear_scene` brings it home as it clears;
* :meth:`~WatchScene.predict` / :meth:`~WatchScene.reveal`: the viewer commits to an answer before the run (a
  question, two to four options, a three-second countdown);
* :meth:`~WatchScene.checkpoint`: two questions about every ten minutes, a pause, and the answers;
* :meth:`~WatchScene.wrong_idea`: the part's misconception, stated, struck through, and replaced;
* :meth:`~WatchScene.title`: the part's title and the series' place, after the cold open;
* :func:`tag`: the small chip that says where a number comes from (``measured``, ``simulated``, ``assumed``,
  ``schematic``, ``cited``, ``illustrative``), so the narration doesn't have to.

Everything a card shows is placed relative to the camera's frame, so it works while the camera is zoomed in.
``tools/check_watch.py`` counts the calls (``predict``, ``checkpoint``, ``wrong_idea``) and the motion.
"""

from __future__ import annotations

import os

import numpy as np
from manim import *  # noqa: F403

from explainer.style import C
from explainer.voiceover import VoiceoverScene

FRAME_W = 14.222222222222221
CARD_BG = "#0E131D"
PREDICT = C.CS_HEAD
LETTERS = "ABCD"
NUMBER_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
                "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty",
                "twenty-one", "twenty-two", "twenty-three", "twenty-four", "twenty-five"]

# where a number comes from: the label the screen carries instead of a spoken caveat
TAGS = {
    "measured": (r"measured on this machine", C.CS_CLOCK),
    "simulated": (r"simulated", C.CS_DATA),
    "computed": (r"computed", C.CS_DATA),
    "assumed": (r"assumed", C.CS_COST),
    "schematic": (r"schematic", GREY_B),
    "illustrative": (r"illustrative", GREY_B),
    "cited": (r"cited", C.HUMAN),
    "projected": (r"projected", C.CS_INF),
}


def _label(text, **kw):
    from explainer.analysis import label

    return label(text, **kw)


def tag(kind: str, detail: str = "", font_size=19) -> VGroup:
    """A small rounded chip naming the source of what it sits next to: ``tag("measured")``,
    ``tag("cited", "Smith 1981")``, ``tag("assumed", "1 ns per memory access")``."""
    text, color = TAGS.get(kind, (kind, GREY_B))
    if detail:
        text = text + r": \ " + detail
    t = _label(text, font_size=font_size, color=color)
    dot = Dot(radius=0.045, color=color)
    body = VGroup(dot, t).arrange(RIGHT, buff=0.1)
    box = RoundedRectangle(width=body.width + 0.28, height=max(0.3, body.height + 0.14), corner_radius=0.12,
                           stroke_color=color, stroke_width=1.2, fill_color=color, fill_opacity=0.08)
    g = VGroup(box, body.move_to(box))
    g.box, g.text = box, t
    return g


def _option(letter: str, text: str, font_size=26, width=None) -> VGroup:
    disc = Circle(radius=0.22, stroke_color=PREDICT, stroke_width=2, fill_color=PREDICT, fill_opacity=0.12)
    lt = Text(letter, font="DejaVu Sans", font_size=20, weight=BOLD, color=PREDICT).move_to(disc)
    body = _label(text, font_size=font_size, color=WHITE)
    row = VGroup(VGroup(disc, lt), body).arrange(RIGHT, buff=0.22)
    w = width or row.width + 0.4
    box = RoundedRectangle(width=w, height=row.height + 0.24, corner_radius=0.14, stroke_color=GREY_D,
                           stroke_width=1.2, fill_color=WHITE, fill_opacity=0.03)
    row.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.18)
    g = VGroup(box, row)
    g.box, g.disc, g.body = box, VGroup(disc, lt), body
    return g


def predict_card(question: str, options, font_size=26, width=None) -> VGroup:
    """The prediction: a "Predict" chip, the question, and lettered options.  ``card.options[k]`` is option k."""
    chipt = Text("PREDICT", font="DejaVu Sans", font_size=16, weight=BOLD, color=CARD_BG)
    chipb = RoundedRectangle(width=chipt.width + 0.3, height=0.32, corner_radius=0.1, stroke_width=0,
                             fill_color=PREDICT, fill_opacity=1)
    head = VGroup(chipb, chipt.move_to(chipb))
    q = _label(question, font_size=font_size + 4, color=WHITE)
    opts = VGroup(*[_option(LETTERS[k], o, font_size=font_size) for k, o in enumerate(options)])
    ow = max(o.width for o in opts)
    opts = VGroup(*[_option(LETTERS[k], o, font_size=font_size, width=ow) for k, o in enumerate(options)])
    opts.arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    body = VGroup(head, q, opts).arrange(DOWN, buff=0.26, aligned_edge=LEFT)
    w = width or body.width + 0.6
    panel = RoundedRectangle(width=w, height=body.height + 0.5, corner_radius=0.2, stroke_color=PREDICT,
                             stroke_width=2, fill_color=CARD_BG, fill_opacity=0.94)
    body.move_to(panel).align_to(panel, LEFT).shift(RIGHT * 0.3)
    card = VGroup(panel, body)
    card.panel, card.head, card.question, card.options = panel, head, q, opts
    return card


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


def series_strip(part: int, width=11.0, font_size=20) -> VGroup:
    """The sixty-one parts as a row of dots grouped by act: those before ``part`` filled, ``part`` lit and larger,
    its act's name beneath."""
    from explainer.cs import ACTS

    dots, acts = VGroup(), VGroup()
    for name, (a, b) in ACTS:
        grp = VGroup()
        for n in range(a, b + 1):
            if n == part:
                d = Dot(radius=0.11, color=C.CS_HEAD)
            elif n < part:
                d = Dot(radius=0.055, color=GREY_B)
            else:
                d = Circle(radius=0.055, stroke_color=GREY_D, stroke_width=1.5)
            grp.add(d)
        grp.arrange(RIGHT, buff=0.075)
        acts.add(grp)
        if a <= part <= b:
            here = (name, grp)
    acts.arrange(RIGHT, buff=0.3)
    if acts.width > width:
        acts.width = width
    name, grp = here
    lab = _label(name, font_size=font_size, color=C.CS_HEAD).next_to(grp, DOWN, buff=0.18)
    brace = Line(grp.get_left(), grp.get_right(), color=C.CS_HEAD, stroke_width=2).next_to(grp, DOWN, buff=0.08)
    return VGroup(acts, brace, lab)


SHORT_TEX = 44  # characters of TeX source a label may have and still be written stroke by stroke


def lively(anim, top=True):
    """A plain ``FadeIn``, given the entrance its content suggests (videos/cs/SYLLABUS.md 1.2, picture and motion):
    an arrow grows from its tail; a line, arc or plotted curve is drawn along its length; a short one-line label or
    formula is written; a group of a few parts arrives part by part, each with its own entrance. The end state is the
    same, so layouts are untouched; anything else keeps its fade. ``EXPLAINER_PLAIN_FADES=1`` turns this off."""
    if os.environ.get("EXPLAINER_PLAIN_FADES") or type(anim) is not FadeIn:
        return anim
    m = anim.mobject
    if top and os.environ.get("EXPLAINER_LIVELY_LOG"):  # which kinds of things fade in (the motion audit)
        with open(os.environ["EXPLAINER_LIVELY_LOG"], "a") as f:
            f.write(type(m).__name__ + "\n")
    kw = {"run_time": anim.run_time, "rate_func": anim.rate_func}
    if isinstance(m, Arrow):
        return GrowArrow(m, **kw)
    if isinstance(m, (Line, Arc, ParametricFunction)):
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


class WatchScene(VoiceoverScene, MovingCameraScene):
    """A narrated scene with a camera, and the watch standard's set pieces."""

    def play(self, *anims, **kw):
        return super().play(*[lively(a) for a in anims], **kw)

    # ------------------------------------------------------------------ the camera
    def frame_center(self):
        return self.camera.frame.get_center()

    def frame_scale(self) -> float:
        return self.camera.frame.width / FRAME_W

    def _fit(self, mob, where="right", buff=0.35):
        """Scale ``mob`` to the camera's zoom and put it ``where`` in the current frame."""
        s = self.frame_scale()
        mob.scale(s)
        f = self.camera.frame
        c = f.get_center()
        w, h = f.width, f.height
        pos = {"right": c + RIGHT * (w / 2 - mob.width / 2 - buff * s),
               "left": c + LEFT * (w / 2 - mob.width / 2 - buff * s),
               "bottom": c + DOWN * (h / 2 - mob.height / 2 - buff * s),
               "top": c + UP * (h / 2 - mob.height / 2 - buff * s),
               "center": c}[where]
        return mob.move_to(pos)

    def pin(self, mob):
        """Keep ``mob`` fixed on the screen while the camera moves (cards, readouts, tags): it follows the frame's
        centre and scales with its zoom."""
        f = self.camera.frame
        s0 = f.width / FRAME_W
        mob._pin = (mob.get_center() - f.get_center()) / s0, s0

        def follow(m):
            off, s_prev = m._pin
            s_now = f.width / FRAME_W
            if abs(s_now - s_prev) > 1e-9:
                m.scale(s_now / s_prev)
            m.move_to(f.get_center() + off * s_now)
            m._pin = off, s_now

        mob.add_updater(follow)
        return mob

    def unpin(self, mob):
        mob.clear_updaters()
        return mob

    def make_room(self, mob, beside, side=LEFT, buff=0.4, run_time=0.8):
        """Slide and shrink ``mob`` into the part of the frame ``beside`` (a card) leaves free; :meth:`give_back`
        puts it back.  (A scale and a position are recorded, not a copy: a live instrument changes shape as it
        runs.)"""
        s = self.frame_scale()
        f = self.camera.frame
        free_w = f.width - beside.width - 3 * buff * s
        k = min(1.0, free_w / max(mob.width, 1e-6), (f.height - 2 * buff * s) / max(mob.height, 1e-6))
        center = mob.get_center().copy()
        new_w = mob.width * k
        x = f.get_left()[0] + buff * s + new_w / 2 if np.allclose(side, LEFT) else \
            f.get_right()[0] - buff * s - new_w / 2
        mob._room = (center, k)
        self.play(mob.animate.scale(k).move_to([x, center[1], 0]), run_time=run_time)
        return mob

    def give_back_anim(self, mob):
        center, k = mob._room
        del mob._room
        return mob.animate.scale(1 / k).move_to(center)

    def give_back(self, mob, run_time=0.8):
        self.play(self.give_back_anim(mob), run_time=run_time)

    def zoom(self, target, margin=1.3, width=None, run_time=1.6, **kw):
        """Move the camera onto ``target`` (a mobject or point)."""
        from explainer.ai.viz import frame_to

        self.play(frame_to(self, target, width=width, margin=margin), run_time=run_time, **kw)

    def home(self, run_time=1.2):
        from explainer.ai.viz import frame_home

        self.play(frame_home(self), run_time=run_time)

    def rewrite(self, terms, focus=None, counter: str | None = None, run_time: float = 0.9, hold: float = 0.25,
                first=None):
        """A chain of terms (a derivation, a reduction, a proof's lines) played in one place: each term morphs into
        the next with its shared symbols flying to their new places (``TransformMatchingShapes``), instead of a
        stack of lines fading in.

        ``terms`` are mobjects; each is moved to where the first stands.  ``focus(k)`` may return the submobject of
        ``terms[k]`` rewritten next (a redex, the rule's left side): it is boxed before the step.  ``counter`` labels
        a step count shown under the chain (``"step"`` gives "step 3"); ``first`` is the first term's entrance
        (``Write`` for a short formula, else a fade).  Returns the last term, on screen."""
        terms = list(terms)
        place = terms[0].get_center()
        for t in terms[1:]:
            t.move_to(place)
        cur = terms[0]
        self.play(first(cur) if first else lively(FadeIn(cur)), run_time=0.8)
        count = None
        if counter:
            n = ValueTracker(0)
            count = always_redraw(lambda: Text(f"{counter} {int(round(n.get_value()))}", font="DejaVu Sans",
                                               font_size=18, color=GREY_B).next_to(cur, DOWN, buff=0.3))
            self.add(count)
        for k, nxt in enumerate(terms[1:]):
            part = focus(k) if focus else None
            if part is not None:
                box = SurroundingRectangle(part, color=PREDICT, buff=0.06, stroke_width=3)
                self.play(Create(box), run_time=0.35)
                self.play(FadeOut(box), run_time=0.2)
            anims = [TransformMatchingShapes(cur, nxt, path_arc=0.6)]
            if count is not None:
                anims.append(n.animate.set_value(k + 1))
            self.play(*anims, run_time=run_time)
            cur = nxt
            if hold:
                self.wait(hold)
        if count is not None:
            count.clear_updaters()  # the final count stays until the section clears
        return cur

    def ask(self, question: str, options, answer: int, say: str | None = None, reveal: str | None = None,
            room=None, where: str = "right"):
        """The retrofit's prediction in one call: ask (``say`` aloud), count down, park the card in a corner, and
        answer it (``reveal`` aloud) when the section clears, after the section's own run has shown the result."""
        card = self.predict(question, options, narration=say, room=room, where=where)
        self.park(card)
        self.expect(card, answer, narration=reveal)
        return card

    def expect(self, card, answer: int, narration: str | None = None):
        """Answer ``card`` when this section clears: the run between the prediction and the reveal is the section's
        own (``predict``, ``park``, ``expect``, then the section as it was)."""
        self._pending = (card, answer, narration)

    def clear_scene(self, *keep, extra=(), run_time: float = 1.0, home: bool = True):
        """Fade everything but ``keep`` (and never the camera's frame); bring the camera home at the same time.  A
        prediction left open with :meth:`expect` is revealed first."""
        from explainer.ai.viz import frame_home

        pending = getattr(self, "_pending", None)
        if pending is not None:
            self._pending = None
            card, answer, narration = pending
            self.reveal(card, answer, narration=narration, keep=True)

        f = self.camera.frame
        if f in self.mobjects:
            self.remove(f)
        moved = abs(f.width - FRAME_W) > 1e-3 or np.linalg.norm(f.get_center()) > 1e-3
        extra = list(extra) + ([frame_home(self)] if home and moved else [])
        super().clear_scene(*keep, extra=extra, run_time=run_time)

    # ------------------------------------------------------------------ chapter cards
    def chapter(self, number, title: str, question: str = "", lit=(), extra=(), part=None, said: str | None = None,
                **card_kw):
        """The chapter card (the tower, the timeline), spoken, then sent off to the left.  ``said`` is the line the
        narration speaks; by default "Chapter seven. Predicting branches."."""
        from explainer.cs import chapter_card

        card = chapter_card(number, title, question, lit=lit, extra=extra, part=part, **card_kw)
        if said is None:
            plain = " ".join(title.replace("\\\\", " ").replace("\\ ", " ").replace("$", "").split())
            said = f"Chapter {NUMBER_WORDS[number] if number < len(NUMBER_WORDS) else number}. {plain}."
        self.mark("card")
        with self.voiceover(said):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card, shift=LEFT * 0.6), run_time=0.6)

    # ------------------------------------------------------------------ predictions
    def predict(self, question: str, options, narration: str | None = None, seconds: float = 3.0,
                where: str = "right", font_size=26, room=None):
        """Ask, count down, and return the card; answer it with :meth:`reveal` after the run.  The narration asks
        the question aloud (it should name the options); the countdown runs in silence.  ``room``: a mobject to
        slide aside while the card is up (it comes back at the reveal)."""
        card = self._fit(predict_card(question, options, font_size=font_size), where)
        card.room = room
        if room is not None:
            self.make_room(room, card, side=LEFT if where == "right" else RIGHT)
        ring, t = countdown_ring(seconds)
        ring.scale(self.frame_scale()).next_to(card.head, RIGHT, buff=0.3 * self.frame_scale())
        if narration:
            with self.voiceover(narration):
                self.play(FadeIn(card, shift=LEFT * 0.3 * self.frame_scale()), run_time=0.8)
        else:
            self.play(FadeIn(card, shift=LEFT * 0.3 * self.frame_scale()), run_time=0.8)
        self.add(ring)
        self.mark("countdown")
        self.play(t.animate.set_value(1.0), run_time=seconds, rate_func=linear)
        ring.clear_updaters()
        for m in ring.get_family():
            m.clear_updaters()
        self.remove(ring)
        card.ring = ring
        return self.pin(card)

    def park(self, card, corner=UR, scale=0.5, run_time=0.8):
        """After the countdown: shrink the card into a corner and give the instrument its room back, so the run
        that answers it plays full size.  :meth:`reveal` answers it there."""
        self.unpin(card)
        anims = [card.animate.scale(scale).to_corner(corner, buff=0.25)]
        room = getattr(card, "room", None)
        if room is not None and hasattr(room, "_room"):
            anims.append(self.give_back_anim(room))
        card.room = None
        f = self.camera.frame
        if abs(f.width - FRAME_W) > 1e-3 or np.linalg.norm(f.get_center()) > 1e-3:
            self.unpin(card)  # placed in the frame as it is
        self.play(*anims, run_time=run_time)
        return self.pin(card)

    def reveal(self, card, answer: int, narration: str | None = None, keep: bool = False):
        """Light the right option, dim the others, then (unless ``keep``) send the card away."""
        self.unpin(card)
        good = card.options[answer]
        anims = [good.box.animate.set_stroke(C.CS_TRUE, width=3).set_fill(C.CS_TRUE, opacity=0.18),
                 good.disc[0].animate.set_fill(C.CS_TRUE, opacity=1).set_stroke(C.CS_TRUE),
                 good.disc[1].animate.set_color(CARD_BG)]
        anims += [o.animate.set_opacity(0.3) for k, o in enumerate(card.options) if k != answer]
        if narration:
            with self.voiceover(narration):
                self.play(*anims, run_time=0.8)
                self.play(Indicate(good, color=C.CS_TRUE, scale_factor=1.04))
        else:
            self.play(*anims, run_time=0.8)
        if not keep:
            room = getattr(card, "room", None)
            anims = [FadeOut(card, shift=RIGHT * 0.3 * self.frame_scale())]
            if room is not None and hasattr(room, "_room"):
                anims.append(self.give_back_anim(room))
            self.play(*anims, run_time=0.8)

    # ------------------------------------------------------------------ checkpoints
    def checkpoint(self, items, narration: str | None = None, answers_narration: str | None = None,
                   seconds: float = 4.0, font_size=28):
        """Two (or three) short questions, a pause to answer, then the answers.  ``items`` are (question, answer)
        pairs of on-screen text."""
        s = self.frame_scale()
        chipt = Text("CHECKPOINT", font="DejaVu Sans", font_size=18, weight=BOLD, color=CARD_BG)
        chipb = RoundedRectangle(width=chipt.width + 0.34, height=0.36, corner_radius=0.1, stroke_width=0,
                                 fill_color=C.CS_CLOCK, fill_opacity=1)
        head = VGroup(chipb, chipt.move_to(chipb))
        qs, ans = VGroup(), VGroup()
        for k, (q, a) in enumerate(items):
            n = Text(f"{k + 1}", font="DejaVu Sans", font_size=24, weight=BOLD, color=C.CS_CLOCK)
            qt = _label(q, font_size=font_size, color=WHITE)
            row = VGroup(n, qt).arrange(RIGHT, buff=0.3, aligned_edge=UP)
            at = _label(a, font_size=font_size - 4, color=C.CS_TRUE).next_to(qt, DOWN, buff=0.16, aligned_edge=LEFT)
            qs.add(row)
            ans.add(at)
        block = VGroup(*[VGroup(q, a) for q, a in zip(qs, ans)]).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        body = VGroup(head, block).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        panel = RoundedRectangle(width=max(9.5, body.width + 1.0), height=body.height + 0.8, corner_radius=0.22,
                                 stroke_color=C.CS_CLOCK, stroke_width=2, fill_color=CARD_BG, fill_opacity=0.97)
        body.move_to(panel)
        card = VGroup(panel, body).scale(s).move_to(self.frame_center())
        ring, t = countdown_ring(int(seconds), color=C.CS_CLOCK)
        ring.scale(s).next_to(head, RIGHT, buff=0.35 * s)
        shown = VGroup(panel, head, *qs)
        if narration:
            with self.voiceover(narration):
                self.play(FadeIn(panel, scale=0.96), FadeIn(head), run_time=0.6)
                self.play(LaggedStart(*[FadeIn(q, shift=UP * 0.1 * s) for q in qs], lag_ratio=0.5), run_time=1.2)
        else:
            self.play(FadeIn(panel, scale=0.96), FadeIn(head), LaggedStart(*[FadeIn(q) for q in qs], lag_ratio=0.4))
        self.add(ring)
        self.mark("countdown")
        self.play(t.animate.set_value(1.0), run_time=seconds, rate_func=linear)
        for m in ring.get_family():
            m.clear_updaters()
        self.remove(ring)
        if answers_narration:
            with self.voiceover(answers_narration):
                self.play(LaggedStart(*[Write(a) for a in ans], lag_ratio=0.6), run_time=2.0)
        else:
            self.play(LaggedStart(*[Write(a) for a in ans], lag_ratio=0.6), run_time=2.0)
        self.wait(0.6)
        self.play(FadeOut(VGroup(shown, ans), scale=0.97), run_time=0.6)

    # ------------------------------------------------------------------ the misconception
    def wrong_idea(self, wrong: str, right: str, narration: str | None = None, right_narration: str | None = None,
                   font_size=34):
        """State the misconception, strike it through, and turn it into the right idea."""
        s = self.frame_scale()
        chipt = Text("WRONG IDEA", font="DejaVu Sans", font_size=18, weight=BOLD, color=CARD_BG)
        chipb = RoundedRectangle(width=chipt.width + 0.34, height=0.36, corner_radius=0.1, stroke_width=0,
                                 fill_color=C.CS_FALSE, fill_opacity=1)
        head = VGroup(chipb, chipt.move_to(chipb))
        w = _label(wrong, font_size=font_size, color=WHITE)
        r = _label(right, font_size=font_size, color=C.CS_TRUE)
        g = VGroup(head, w).arrange(DOWN, buff=0.35).scale(s).move_to(self.frame_center() + UP * 0.6 * s)
        r.scale(s).move_to(w)
        panel = RoundedRectangle(width=max(w.width, r.width) + 1.4 * s, height=g.height + 1.9 * s,
                                 corner_radius=0.2 * s, stroke_color=GREY_D, stroke_width=1.5, fill_color=CARD_BG,
                                 fill_opacity=0.96).move_to(g.get_center() + DOWN * 0.35 * s)
        self.play(FadeIn(panel, scale=0.97), run_time=0.4)
        strike = Line(w.get_left() + LEFT * 0.1 * s, w.get_right() + RIGHT * 0.1 * s, color=C.CS_FALSE,
                      stroke_width=5 * s)
        if narration:
            with self.voiceover(narration):
                self.play(FadeIn(head, shift=DOWN * 0.1 * s), Write(w), run_time=1.2)
        else:
            self.play(FadeIn(head), Write(w))
        new_chipb = chipb.copy().set_fill(C.CS_TRUE)
        new_chipt = Text("RIGHT IDEA", font="DejaVu Sans", font_size=18, weight=BOLD, color=CARD_BG)
        new_chipt.scale(s).move_to(chipb)
        # the end state: the chip, the struck wrong idea (small, dim), the right idea in the old place
        w_end = w.copy().scale(0.7).set_opacity(0.4).next_to(r, UP, buff=0.3 * s)
        k_end = strike.copy().scale(0.7).move_to(w_end)
        h_end = VGroup(chipb.copy(), chipt.copy()).next_to(w_end, UP, buff=0.25 * s)
        new_chipb.move_to(h_end[0])
        new_chipt.move_to(h_end[0])
        if right_narration:
            with self.voiceover(right_narration):
                self.play(Create(strike), w.animate.set_opacity(0.4), run_time=0.6)
                self.play(Transform(w, w_end), Transform(strike, k_end), Transform(chipb, new_chipb),
                          Transform(chipt, new_chipt), FadeIn(r, shift=UP * 0.3 * s), run_time=1.0)
        else:
            self.play(Create(strike), w.animate.set_opacity(0.4))
            self.play(FadeIn(r, shift=UP * 0.3 * s))
        return VGroup(panel, head, w, strike, r)

    # ------------------------------------------------------------------ the title, after the cold open
    def title(self, part: int, subtitle: str = "", hold: float = 1.6):
        """The part's title, the series, and its act on the series map, drawn small; about seven seconds."""
        from explainer.ai import zh
        from explainer.cs import PARTS, SERIES_EN, SERIES_ZH

        series = SERIES_ZH if zh() else SERIES_EN
        top = _label(series, font_size=26, color=GREY_B)
        name = _label(PARTS[part], font_size=64, color=WHITE)
        num = _label((rf"第{part}部分" if zh() else rf"Part {part}"), font_size=30, color=C.CS_HEAD)
        g = VGroup(top, num, name).arrange(DOWN, buff=0.22)
        if subtitle:
            g.add(_label(subtitle, font_size=28, color=GREY_A).next_to(name, DOWN, buff=0.3))
        smap = series_strip(part)
        g.move_to(UP * 0.9)
        smap.next_to(g, DOWN, buff=0.45)
        whole = VGroup(g, smap).scale(self.frame_scale()).move_to(self.frame_center())
        self.mark("title")
        self.play(LaggedStart(FadeIn(top, shift=DOWN * 0.15), FadeIn(num, shift=DOWN * 0.15),
                              Write(name), lag_ratio=0.35), run_time=2.0)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in smap[0].family_members_with_points()], lag_ratio=0.01),
                  GrowFromCenter(smap[1]), FadeIn(smap[2]), run_time=1.6)
        self.wait(hold)
        self.play(FadeOut(whole, shift=UP * 0.3), run_time=0.8)
