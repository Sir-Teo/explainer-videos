from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from explainer.fluids import colormaps as cm
from videos.llm.common import Mono, Plot, data, label, load, show_chapter_card, token_row


def sample_block(text: str, max_lines=7, width=62, font_size=22) -> VGroup:
    """A text sample with its own line breaks kept (blank lines dropped)."""
    lines = [ln[:width] for ln in text.split("\n") if ln.strip()][:max_lines]
    return VGroup(*[Mono(ln, font_size=font_size) for ln in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)


class Training(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 10, "How it learns")
        self.d = data()
        self.tiny = load("tiny_shakespeare")
        self.random_start()
        self.loss()
        self.every_position()
        self.descent()
        self.tiny_model()

    # ------------------------------------------------------------------
    def random_start(self):
        n = 40
        rng = np.random.default_rng(0)
        bars = VGroup(*[Rectangle(width=0.18, height=0.25 + 0.03 * rng.normal(), stroke_width=0, fill_color=C.PROB,
                                  fill_opacity=0.8) for _ in range(n)]).arrange(RIGHT, buff=0.08, aligned_edge=DOWN)
        bars.move_to(DOWN * 0.6)
        base = Line(bars.get_corner(DL) + LEFT * 0.2, bars.get_corner(DR) + RIGHT * 0.2, color=GREY_B)
        dots = MathTex(r"\cdots", font_size=40).next_to(bars, RIGHT, buff=0.3)
        lab = MathTex(r"\text{every token: about } \tfrac{1}{50{,}257}", font_size=40).next_to(bars, UP, buff=0.6)
        title = label(r"a freshly initialized model", font_size=36).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Every number we've seen so far, the embeddings, the attention matrices, the MLP weights, all 124 million of "
            "them, starts out random. <bookmark mark='u'/> A freshly initialized model has no idea what comes next: its "
            "predictions are spread almost evenly, about one in fifty thousand for every token."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("u")
            self.play(Create(base), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02), FadeIn(dots))
            self.play(Write(lab))
        self.clear_scene()

    # ------------------------------------------------------------------
    def loss(self):
        pl = Plot((0, 1), (0, 11.5), width=6.2, height=4.8, x_ticks=[0, 0.5, 1], y_ticks=[0, 2, 4, 6, 8, 10],
                  x_fmt=lambda v: f"{v:g}").move_to(LEFT * 2.6 + DOWN * 0.3)
        ps = np.concatenate([np.geomspace(1 / 50257, 0.05, 60), np.linspace(0.05, 1, 60)])
        curve = pl.line(ps, -np.log(ps), C.LOSS, 4)
        xl = label(r"probability given to the right answer", font_size=28, color=GREY_A).next_to(pl, DOWN, buff=0.5)
        yl = MathTex(r"-\log p", font_size=40, color=C.LOSS).next_to(pl, UP, buff=0.2).align_to(pl, LEFT)
        title = label(r"the loss", font_size=40, color=C.LOSS).to_corner(UR, buff=0.5)
        p_paris = self.d["final"]["probs"][0]
        pts = [(1.0, r"certain and right: 0"), (p_paris, rf"Paris at {100 * p_paris:.1f}\%: {-math.log(p_paris):.2f}"),
               (1 / 50257, r"uniform guess: 10.8")]
        assert abs(math.log(50257) - 10.82) < 0.01
        marks = VGroup()
        for p, t in pts:
            d = Dot(pl.c2p(p, -math.log(p)), color=YELLOW, radius=0.08)
            lab = label(t, font_size=28, color=YELLOW).next_to(d, RIGHT, buff=0.2)
            if p > 0.9:
                lab.next_to(d, UP, buff=0.2).shift(LEFT * 1.0)
            marks.add(VGroup(d, lab))
        with self.voiceover(
            "To improve, the model needs a score. Take any text, and at each position, look at the probability the model "
            "gave to the token that actually came next. <bookmark mark='l'/> The loss is minus the logarithm of that "
            "probability. <bookmark mark='a'/> If the model was certain and right, the loss is zero. "
            "<bookmark mark='b'/> For our Paris, at six percent, it's 2.75. <bookmark mark='c'/> A model that guesses "
            "uniformly scores about 10.8. Averaged over lots of text, this one number is what training tries to make small."
        ) as vo:
            self.play(FadeIn(title), Create(pl), FadeIn(xl))
            vo.wait_until("l")
            self.play(Write(yl), Create(curve))
            for m, mk in zip(marks, "abc"):
                vo.wait_until(mk)
                self.play(FadeIn(m, scale=1.2), run_time=0.7)
        self.clear_scene()

    # ------------------------------------------------------------------
    def every_position(self):
        tl = self.d["token_losses"]
        pieces, losses = tl["pieces"], tl["losses"]
        assert pieces[3] == "el" and losses[2] < 0.05 and losses[3] < 0.1 and 2.5 < losses[10] < 3.0
        row = token_row(pieces, font_size=28, buff=0.12).to_edge(DOWN, buff=1.0)
        if row.width > 13.4:
            row.scale_to_fit_width(13.4)
        scale = 0.42
        bars, vals = VGroup(), VGroup()
        for t, l in zip(row[1:], losses):
            b = Rectangle(width=t.width * 0.7, height=max(0.02, scale * l), stroke_width=0, fill_color=C.LOSS, fill_opacity=0.85)
            b.next_to(t, UP, buff=0.15)
            bars.add(b)
            vals.add(DecimalNumber(l, num_decimal_places=2, font_size=24, color=GREY_A).next_to(b, UP, buff=0.08))
        title = label(r"GPT-2's real loss at every position of one sentence", font_size=32).to_edge(UP, buff=0.4)
        first = label(r"(the first token has nothing to predict it from)", font_size=24, color=GREY_B)
        first.next_to(row[0], DOWN, buff=0.25).align_to(row, LEFT)
        with self.voiceover(
            "And one piece of text gives a prediction at every position at once. <bookmark mark='r'/> Here are GPT-2's real "
            "losses on our sentence. <bookmark mark='e'/> After 'The', the token E was a big surprise. <bookmark mark='i'/> "
            "But once it has seen E and iff, the model is certain that el comes next, <bookmark mark='t'/> and then Tower. "
            "<bookmark mark='p'/> Paris costs 2.75."
        ) as vo:
            self.play(FadeIn(title), FadeIn(row), FadeIn(first))
            vo.wait_until("r")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.06), FadeIn(vals, lag_ratio=0.06),
                      run_time=2)
            for mk, i in zip("eitp", (0, 2, 3, 10)):
                vo.wait_until(mk)
                self.play(Indicate(VGroup(bars[i], vals[i], row[i + 1]), color=YELLOW), run_time=0.8)

        mask = label(r"each prediction may only use the tokens before it, so all of them\\can be trained at once without any of them seeing its own answer",
                     font_size=28, color=YELLOW).next_to(title, DOWN, buff=0.3)
        with self.voiceover(
            "This is why the causal mask matters. Each position's prediction may only use the tokens before it, so all of "
            "these predictions can be trained at the same time, in parallel, without any of them getting to see its own "
            "answer."
        ) as vo:
            self.play(FadeIn(mask, shift=DOWN * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def descent(self):
        def f(x, y):
            return 0.35 * (x - 1.2) ** 2 + 1.1 * (y + 0.6) ** 2 + 0.25 * np.sin(2.2 * x) * np.cos(1.7 * y) + 0.15 * x * y

        def grad(x, y, h=1e-4):
            return np.array([(f(x + h, y) - f(x - h, y)) / (2 * h), (f(x, y + h) - f(x, y - h)) / (2 * h)])

        x0, x1, y0, y1 = -4.0, 4.0, -2.6, 2.6
        res = 220
        X, Y = np.meshgrid(np.linspace(x0, x1, int(res * 8 / 5.2)), np.linspace(y1, y0, res))
        Z = f(X, Y)
        rgb = cm.sequential(np.log1p(Z - Z.min()), 0, np.log1p(Z - Z.min()).max(), low="#120F18", mid="#4A1F35", high="#C55F73")
        img = ImageMobject(cm.to_uint8(rgb))
        img.stretch_to_fit_width(7.0).stretch_to_fit_height(5.2 * 7.0 / 8.0).move_to(LEFT * 3.0 + DOWN * 0.4)
        sc = 7.0 / 8.0
        to_scene = lambda p: img.get_center() + sc * np.array([p[0], p[1], 0])  # noqa: E731
        p = np.array([-3.3, 2.0])
        path = [p.copy()]
        for _ in range(40):
            p = p - 0.35 * grad(*p)
            path.append(p.copy())
        dots = VGroup(*[Dot(to_scene(q), radius=0.06, color=YELLOW) for q in path])
        lines = VGroup(*[Line(to_scene(a), to_scene(b), color=YELLOW, stroke_width=2.5) for a, b in zip(path, path[1:])])
        tag = label(r"schematic: a loss landscape over just 2 of 124 million parameters", font_size=24, color=GREY_B)
        tag.next_to(img, DOWN, buff=0.2)
        legend = VGroup(label(r"brighter: higher loss", font_size=26, color=GREY_A)).next_to(img, UP, buff=0.2)
        text = VGroup(
            label(r"1.\ measure the loss on a batch of text", font_size=30),
            label(r"2.\ compute the gradient: how each\\\ \ \ parameter nudges the loss", font_size=30),
            label(r"3.\ step every parameter downhill", font_size=30),
            label(r"4.\ repeat, millions of times", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 3.95 + DOWN * 0.2)
        with self.voiceover(
            "So how do you improve 124 million numbers at once? <bookmark mark='m'/> Measure the loss on a batch of text. "
            "<bookmark mark='g'/> For every parameter, calculus tells you how the loss would change if you nudged it "
            "slightly; together, these slopes make up the gradient. <bookmark mark='s'/> Move every parameter a small step "
            "downhill, <bookmark mark='r'/> and repeat, on fresh text, millions of times. This is gradient descent."
        ) as vo:
            self.play(FadeIn(img), FadeIn(tag), FadeIn(legend))
            self.play(FadeIn(dots[0], scale=2))
            vo.wait_until("m")
            self.play(FadeIn(text[0]))
            vo.wait_until("g")
            self.play(FadeIn(text[1]))
            g0 = -grad(*path[0])
            arrow = Arrow(to_scene(path[0]), to_scene(path[0] + 0.6 * g0 / np.linalg.norm(g0)), buff=0, color=WHITE)
            self.play(GrowArrow(arrow))
            vo.wait_until("s")
            self.play(FadeIn(text[2]), FadeOut(arrow))
            vo.wait_until("r")
            self.play(FadeIn(text[3]), LaggedStart(*[AnimationGroup(Create(ln), FadeIn(d)) for ln, d in zip(lines, dots[1:])],
                                                    lag_ratio=0.3), run_time=4)
        bp = label(r"\emph{backpropagation}: all 124 million slopes at once,\\via the chain rule, working backwards through the layers",
                   font_size=28, color=YELLOW).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Computing 124 million slopes sounds expensive, but there's a trick: apply the chain rule backwards through the "
            "layers, reusing work as you go, and you get all of them for roughly the cost of a couple more forward passes. "
            "That algorithm is called backpropagation."
        ) as vo:
            self.play(FadeOut(legend), FadeIn(bp))
        self.clear_scene()

    # ------------------------------------------------------------------
    def tiny_model(self):
        t = self.tiny
        assert 0.7e6 < t["n_params"] < 0.9e6 and abs(t["uniform_loss"] - math.log(len(t["chars"]))) < 1e-6
        steps = sorted(int(k) for k in t["samples"])
        assert steps == [0, 100, 300, 1000, 2000, 4000]
        tr = np.array(t["train_loss"])
        k = 25
        smooth = np.convolve(tr, np.ones(k) / k, mode="valid")
        xs = np.arange(len(smooth)) + k // 2
        val = np.array(t["val_loss"])
        pl = Plot((0, 4000), (1.0, 4.5), width=5.6, height=4.2, x_ticks=[0, 1000, 2000, 3000, 4000],
                  y_ticks=[1, 2, 3, 4], x_fmt=lambda v: f"{v:,}".replace(",", "{,}")).move_to(LEFT * 3.5 + DOWN * 0.1)
        curve = pl.line(xs[::5], smooth[::5], C.LOSS, 3)
        vdots = pl.dots(val[:, 0], val[:, 1], WHITE, radius=0.04)
        yl = label(r"loss", font_size=28, color=C.LOSS).next_to(pl, UP, buff=0.15).align_to(pl, LEFT)
        xl = label(r"training step", font_size=26, color=GREY_A).next_to(pl, DOWN, buff=0.5)
        uni = DashedLine(pl.c2p(0, t["uniform_loss"]), pl.c2p(4000, t["uniform_loss"]), color=GREY_B, stroke_width=1.5)
        uni_l = label(r"random guessing", font_size=22, color=GREY_B).next_to(uni, UP, buff=0.05).align_to(uni, RIGHT)
        spec = label(r"a tiny GPT trained from scratch on Shakespeare: 0.8 million parameters, 4 layers,"
                     r" 65 single characters as tokens", font_size=24, color=GREY_A).to_edge(UP, buff=0.3)

        with self.voiceover(
            "To see learning happen, I trained a tiny transformer from scratch. It's the same design as GPT-2, but with "
            "just 0.8 million parameters, four layers, and single characters as tokens, trained on about a million "
            "characters of Shakespeare. <bookmark mark='c'/> Here's its real loss curve. It starts at the loss of random "
            "guessing, and falls fast."
        ) as vo:
            self.play(FadeIn(spec), Create(pl), FadeIn(yl), FadeIn(xl))
            vo.wait_until("c")
            self.play(Create(uni), FadeIn(uni_l))
            self.play(Create(curve), FadeIn(vdots), run_time=3, rate_func=linear)

        box_pos = RIGHT * 3.25 + DOWN * 0.3
        frame = RoundedRectangle(width=7.1, height=5.0, corner_radius=0.15, stroke_color=GREY_B, stroke_width=1.5)
        frame.move_to(box_pos)
        marker = Dot(pl.c2p(0, t["val_loss"][0][1]), radius=0.11, color=YELLOW)
        step_lab = label(r"step 0", font_size=30, color=YELLOW).next_to(frame, UP, buff=0.12).align_to(frame, LEFT)
        current = sample_block(t["samples"]["0"]).move_to(box_pos)
        if current.width > 6.8:
            current.scale_to_fit_width(6.8)
        vl = {int(st): v for st, v in t["val_loss"]}
        state = {"current": current}

        def show(st):
            new = sample_block(t["samples"][str(st)]).move_to(box_pos)
            if new.width > 6.8:
                new.scale_to_fit_width(6.8)
            new_lab = label(rf"step {st:,}".replace(",", "{,}"), font_size=30, color=YELLOW).move_to(step_lab, aligned_edge=LEFT)
            self.play(marker.animate.move_to(pl.c2p(st, vl[st])), Transform(step_lab, new_lab),
                      FadeOut(state["current"], shift=UP * 0.2), FadeIn(new, shift=UP * 0.2), run_time=1.2)
            state["current"] = new

        with self.voiceover("At step zero, it produces random characters.") as vo:
            self.play(Create(frame), FadeIn(marker), FadeIn(step_lab), FadeIn(current))
        with self.voiceover(
            "After a hundred steps, it has learned which letters are common, and that text comes in chunks separated by "
            "spaces."
        ) as vo:
            show(100)
        with self.voiceover(
            "By step 300, there are short real words, line breaks, and made-up names in capitals, followed by a colon, "
            "just like the speaker names in a play."
        ) as vo:
            show(300)
        with self.voiceover("By step 1,000: real words, real names, like Gloucester, and the rhythm of dialogue.") as vo:
            show(1000)
        with self.voiceover(
            "And after 4,000 steps, about a quarter of an hour on four ordinary processor cores, it writes this. It's not "
            "great Shakespeare, but nobody told it about spelling, words, names, or line breaks. All of it came from "
            "predicting the next character."
        ) as vo:
            show(4000)

        gpt2 = label(r"GPT-2 learned exactly this way, from about 40 GB of text from the web", font_size=30, color=GREY_A)
        gpt2.to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "GPT-2 learned in exactly the same way, just bigger: predicting the next token across about 40 gigabytes of text "
            "from the web."
        ) as vo:
            self.play(FadeIn(gpt2, shift=UP * 0.2))
        self.clear_scene()

