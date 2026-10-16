from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import load, surprise_color, surprise_legend

TOKEN_FONT = "DejaVu Sans"


def token_paragraph(tokens, bits, width=13.0, font_size=19, line_gap=0.42) -> VGroup:
    """The tokens of a paragraph, laid out in lines no wider than ``width``, each on a tile colored by its surprise.
    A token's leading space becomes a gap.  Returns a VGroup of tiles (each a VGroup(rect, text)), in order."""
    tiles, x, y = VGroup(), 0.0, 0.0
    gap = 0.11
    for tok, b in zip(tokens, bits):
        space = tok.startswith(" ")
        t = Text(tok.strip() or "·", font=TOKEN_FONT, font_size=font_size, color=BLACK if b > 5.0 else WHITE)
        w = t.width + 0.08
        if space and x > 0:
            x += gap
        if x + w > width:
            x, y = 0.0, y - line_gap
        r = Rectangle(width=w, height=0.34, stroke_width=0, fill_color=surprise_color(b), fill_opacity=1)
        r.move_to([x + w / 2, y, 0])
        t.move_to(r.get_center())
        tile = VGroup(r, t)
        tile.bits, tile.tok = b, tok
        tiles.add(tile)
        x += w
    return tiles.move_to(ORIGIN)


class Knowledge(VoiceoverScene):
    def construct(self):
        self.card()
        self.landscape()
        self.facts()
        self.memory()
        self.ladder_of_knowledge()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(10, r"What it takes to guess well", r"What must a model know, to drive the bits down?",
                            part=1)
        with self.voiceover("Chapter ten. What does a model have to know, to guess well?") as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def landscape(self):
        d = load("lms")
        para = d["paragraph"]
        A, B = d["surprise"]["GPT-2 small"], d["surprise"]["Qwen3-4B"]
        ta, tb = sum(A["bits"]), sum(B["bits"])
        assert abs(ta - 446.1) < 0.1 and abs(tb - 349.5) < 0.1
        assert para.startswith("A switch clicked") and "Bull Durham tobacco" in para
        pa = token_paragraph(A["tokens"], A["bits"]).move_to(UP * 1.25)
        pb = token_paragraph(B["tokens"], B["bits"]).move_to(DOWN * 1.75)
        la = label(rf"GPT-2 small (2019): \ ${ta:.0f}$ bits, \ ${ta / len(para):.2f}$ per character", font_size=26,
                   color=C.NEURAL).next_to(pa, UP, buff=0.25)
        lb = label(rf"Qwen3-4B (2025): \ ${tb:.0f}$ bits, \ ${tb / len(para):.2f}$ per character", font_size=26,
                   color=C.NEURAL).next_to(pb, UP, buff=0.25)
        head = label(r"Each token's surprise, under two models", font_size=32).to_edge(UP, buff=0.25)
        leg = surprise_legend(width=3.2).to_corner(DR, buff=0.3)
        tag = note(r"computed: \ the Falcon passage, chapter 2, third paragraph").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Let's look at what a strong model knows that a weaker one doesn't. Here is one paragraph of the "
            "Falcon passage, broken into tokens, <bookmark mark='a'/> each colored by how surprised GPT-2, from "
            "2019, was by it: dark when expected, bright when not. <bookmark mark='b'/> And the same paragraph under "
            "Qwen3, from 2025. Its tiles are darker almost everywhere: 350 bits instead of 446."
        ) as vo:
            self.play(FadeIn(head), FadeIn(leg), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(la), LaggedStart(*[FadeIn(t) for t in pa], lag_ratio=0.03), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(lb), LaggedStart(*[FadeIn(t) for t in pb], lag_ratio=0.03), run_time=2.5)
        # where they differ
        def find(tiles, word):
            return next(t for t in tiles if t.tok.strip() == word)

        pairs = [("Durham", 7.4, 2.9), ("tobacco", 9.4, 2.4), ("telephone", 11.0, 3.4)]
        for w, x, y in pairs:
            assert abs(find(pa, w).bits - x) < 0.05 and abs(find(pb, w).bits - y) < 0.05, w
        boxes = VGroup(*[SurroundingRectangle(find(g, w), color=WHITE, buff=0.05, stroke_width=2.5)
                         for w, _, _ in pairs[:2] for g in (pa, pb)])
        tel = VGroup(*[SurroundingRectangle(find(g, "telephone"), color=C.BITS, buff=0.05, stroke_width=2.5)
                       for g in (pa, pb)])
        cx = load("context")
        alone, with_ = cx["Qwen3-4B"]["alone"], cx["Qwen3-4B"]["with context"]
        assert abs(alone - 12.8) < 0.05 and abs(with_ - 3.4) < 0.05
        mem = label(rf"Qwen3-4B on this paragraph alone: \ \texttt{{telephone}} costs ${alone:.1f}$ bits", font_size=22,
                    color=C.BITS).to_edge(DOWN, buff=0.75)
        with self.voiceover(
            "Look where they differ. <bookmark mark='a'/> After Bull, GPT-2 doesn't expect Durham, or tobacco. "
            "Qwen3 does: Bull Durham was a real brand of tobacco, and somewhere in its training it learned that. "
            "<bookmark mark='b'/> And the telephone: GPT-2 is surprised by it, eleven bits; Qwen3 isn't, three "
            "bits, because two paragraphs earlier, a telephone bell rang. <bookmark mark='c'/> Show Qwen3 this "
            "paragraph on its own, and the telephone costs it almost thirteen bits. It remembers."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(boxes))
            vo.wait_until("b")
            self.play(FadeOut(boxes), Create(tel))
            vo.wait_until("c")
            self.play(FadeIn(mem))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def facts(self):
        pr = load("probes")

        def p_of(model, prompt, token):
            r = next(r for r in pr[model] if r["prompt"] == prompt)
            return dict(zip(r["tokens"], r["probs"])).get(token)

        items = [
            ("The Eiffel Tower is located in the city of", " Paris", r"\texttt{Paris}"),
            ("The author of Pride and Prejudice is Jane", " Aust", r"\texttt{Aust}(en)"),
            ("The chemical symbol for gold is", " Au", r"\texttt{Au}"),
            ("Two plus two equals", " four", r"\texttt{four}"),
        ]
        head = label(r"Knowing things lowers the surprise", font_size=34).to_edge(UP, buff=0.35)
        rows = VGroup()
        for prompt, tok, name in items:
            a, b = p_of("GPT-2 small", prompt, tok), p_of("Qwen3-4B", prompt, tok)
            ptxt = Text(prompt + " …", font=TOKEN_FONT, font_size=22, color=C.TOKEN)
            ans = label(name, font_size=24, color=WHITE)
            bars = VGroup()
            for k, (v, col) in enumerate(((a, C.MODEL_Q), (b, C.NEURAL))):
                w = 4.0 * (v if v is not None else 0.004)
                r = Rectangle(width=max(w, 0.02), height=0.22, stroke_width=0, fill_color=col, fill_opacity=0.9)
                t = MathTex(f"{v:.3f}" if v is not None else r"< 0.01", font_size=22, color=col)
                bars.add(VGroup(r, t))
            rows.add(VGroup(ptxt, ans, bars))
        y = 1.9
        for r in rows:
            r[0].move_to([-6.6, y, 0], aligned_edge=LEFT)
            r[1].move_to([-6.6, y - 0.45, 0], aligned_edge=LEFT).shift(RIGHT * 0.3)
            for k, b in enumerate(r[2]):
                b[0].move_to([1.2, y - 0.1 - 0.32 * k, 0], aligned_edge=LEFT)
                b[1].next_to(b[0], RIGHT, buff=0.15)
            y -= 1.25
        leg = VGroup(label(r"GPT-2 small (2019)", font_size=22, color=C.MODEL_Q),
                     label(r"Qwen3-4B (2025)", font_size=22, color=C.NEURAL)).arrange(RIGHT, buff=0.6)
        leg.next_to(head, DOWN, buff=0.25)
        assert p_of("GPT-2 small", items[2][0], " Au") is None
        assert abs(p_of("Qwen3-4B", items[3][0], " four") - 0.276) < 0.001
        assert abs(p_of("Qwen3-4B", items[3][0], " five") - 0.243) < 0.001
        cap = note(r"probability of the right next token; \ computed").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Facts work the same way. Ask for the city of the Eiffel Tower, <bookmark mark='a'/> the author of Pride "
            "and Prejudice, <bookmark mark='b'/> or the chemical symbol for gold, and the model that knows the "
            "answer pays far fewer bits when the answer comes. <bookmark mark='c'/> Arithmetic is harder: the 2025 "
            "model gives four 28 percent, but five 24."
        ) as vo:
            self.play(FadeIn(head), FadeIn(leg), FadeIn(cap))
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def memory(self):
        d = load("mi")
        ds, mi = np.asarray(d["d"], float), np.asarray(d["mi"])
        slope = float(d["slope"])
        assert abs(mi[0] - 0.753) < 0.001 and -0.6 < slope < -0.45
        head = label(r"How far back does the past tell you about the future?", font_size=32).to_edge(UP, buff=0.3)
        defn = mtex(r"I(X_t; X_{t+d}) = D_{\mathrm{KL}}\big(p(x, y) \,\|\, p(x)\,p(y)\big)", font_size=32,
                    color=GREY_A).next_to(head, DOWN, buff=0.2)
        # log-log axes: x = log10 d, y = log10 I + 6 (so the axes meet at the bottom left)
        ax = Axes(x_range=[0, 3, 1], y_range=[0, 6, 1], x_length=8.6, y_length=4.3, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).shift(DOWN * 0.75 + LEFT * 0.8)
        xl = VGroup(*[MathTex(t, font_size=24, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.15)
                      for t, v in (("1", 0), ("10", 1), ("100", 2), ("1000", 3))])
        yl = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=22, color=GREY_B).next_to(ax.c2p(0, v + 6), LEFT, buff=0.12)
                      for v in (0, -2, -4, -6)])
        axl = VGroup(label(r"distance $d$, in letters", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.5),
                     label(r"mutual information, bits", font_size=22, color=GREY_A).next_to(ax.c2p(0, 6), UP, buff=0.12))
        ok = mi > 0
        pts = [ax.c2p(math.log10(x), math.log10(y) + 6) for x, y in zip(ds[ok], mi[ok])]
        curve = VMobject(stroke_color=C.CONTEXT, stroke_width=4).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p_, radius=0.045, color=C.CONTEXT) for p_ in pts])
        fit_x = np.array([math.log10(20), 3])
        fit = DashedLine(ax.c2p(fit_x[0], d["intercept"] + slope * fit_x[0] + 6),
                         ax.c2p(fit_x[1], d["intercept"] + slope * fit_x[1] + 6), color=C.BITS, stroke_width=2.5)
        fit_l = label(rf"a power law: \ $\propto d^{{{slope:.2f}}}$", font_size=24, color=C.BITS).next_to(fit, UP, buff=0.15)
        fit_l.shift(RIGHT * 0.6)
        a1 = label(r"inside a word: \ $0.75$ bits at $d = 1$, \ falling fast", font_size=22, color=WHITE)
        a1.next_to(ax.c2p(0.12, math.log10(mi[0]) + 6), RIGHT, buff=0.25)
        side = VGroup(
            label(r"a counting model with $k$ letters of context:", font_size=22, color=GREY_A),
            label(r"its dependence dies off \textit{exponentially}", font_size=22, color=GREY_A),
            label(r"real text: \ a long, slow tail", font_size=22, color=C.BITS),
            label(r"(Lin \& Tegmark, 2017)", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.9, 0.9, 0])
        tag = computed_tag(r"computed: $22.8$ million letters of the $30$ books")
        with self.voiceover(
            "And the telephone points to something deep. How much does one letter tell you about a letter d places "
            "later? That's the mutual information from chapter five, measured here over all thirty books. "
            "<bookmark mark='a'/> Neighbors share three quarters of a bit. Inside a word, it falls fast. "
            "<bookmark mark='b'/> But then it doesn't vanish. It decays slowly, like a power of the distance, out to a "
            "thousand letters and beyond."
        ) as vo:
            self.play(FadeIn(head), FadeIn(defn), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(axl), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(curve), FadeIn(dots), run_time=2.5)
            self.play(FadeIn(a1))
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(fit_l))
        with self.voiceover(
            "A counting model can't produce a tail like that: the influence of anything outside its few letters of "
            "context is cut off, and the dependence it models dies away exponentially. <bookmark mark='a'/> Real "
            "text keeps paying back what you remember, at every distance. To guess well, a model needs a long "
            "memory, and a way to find the parts of the past that matter. That's what attention is for, in part "
            "eleven."
        ) as vo:
            self.play(FadeIn(side[:2]))
            vo.wait_until("a")
            self.play(FadeIn(side[2:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ladder_of_knowledge(self):
        steps = [
            (r"letter frequencies", r"$4.1$", C.COUNTING),
            (r"spelling: \ a few letters of context", r"$2.0$", C.COUNTING),
            (r"words and grammar", r"", GREY_A),
            (r"facts about the world", r"", GREY_A),
            (r"the story so far: \ long memory", r"", GREY_A),
            (r"people (Shannon, 1951)", r"$0.6$--$1.3$", C.HUMAN),
        ]
        head = label(r"To drive the bits down, a model must learn\ldots", font_size=34).to_edge(UP, buff=0.4)
        rows = VGroup()
        for k, (t, v, col) in enumerate(steps):
            r = VGroup(label(t, font_size=28, color=col), label(v + (r" \ bits per letter" if v else ""), font_size=24,
                                                                   color=col))
            r[1].next_to(r[0], RIGHT, buff=0.5)
            rows.add(r)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(head, DOWN, buff=0.5)
        rows.shift(RIGHT * 1.3)
        # the same descent on a scale of bits per letter
        def yb(b):
            return -3.1 + 1.12 * b
        x0 = -5.6
        scale = NumberLine(x_range=[0, 5, 1], length=1.12 * 5, rotation=PI / 2, color=GREY_C, include_numbers=False)
        scale.move_to([x0, yb(2.5), 0])
        nums = VGroup(*[MathTex(str(v), font_size=26, color=GREY_B).next_to([x0, yb(v), 0], LEFT, buff=0.18)
                        for v in range(6)])
        unit = label(r"bits per letter", font_size=22, color=GREY_B).next_to(scale, UP, buff=0.15)
        band = Rectangle(width=0.7, height=1.12 * 0.7, stroke_width=0, fill_color=C.HUMAN, fill_opacity=0.35)
        band.move_to([x0, yb(0.95), 0])
        ball = glow_dot([x0, yb(4.75), 0], color=C.BITS, radius=0.1)
        ticks = VGroup(*[Line([x0 - 0.25, yb(v), 0], [x0 + 0.25, yb(v), 0], color=C.COUNTING, stroke_width=4)
                         for v in (4.1, 2.0)])
        fall = DashedLine([x0, yb(2.0), 0], [x0, yb(1.0), 0], color=GREY_A, stroke_width=3, dash_length=0.08)
        thesis = label(r"predicting the text means modeling the world that wrote it", font_size=30, color=C.BITS)
        thesis.to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "So here's the ladder. <bookmark mark='a'/> Letter frequencies get you four bits. Spelling, a few "
            "letters of context, gets you two. <bookmark mark='b'/> Below that, a model has to learn words and "
            "grammar, facts about the world, and what has happened so far in the story, <bookmark mark='c'/> down "
            "toward the one bit or so that people need. <bookmark mark='d'/> Nobody tells the model to learn any of "
            "this. It is pushed there by one number: the bits it pays for each guess. To predict the text, it has "
            "to model the world that wrote it."
        ) as vo:
            self.play(FadeIn(head), Create(scale), FadeIn(nums), FadeIn(unit), FadeIn(ball, scale=0.5))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), ball.animate.move_to([x0, yb(4.1), 0]), Create(ticks[0]))
            self.play(FadeIn(rows[1]), ball.animate.move_to([x0, yb(2.0), 0]), Create(ticks[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[2:5]], lag_ratio=0.5), Create(fall),
                      ball.animate.move_to([x0, yb(1.3), 0]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[5]), FadeIn(band), ball.animate.move_to([x0, yb(1.0), 0]))
            vo.wait_until("d")
            self.play(FadeIn(thesis, shift=UP * 0.1))
        self.wait(0.5)
        self.clear_scene()
