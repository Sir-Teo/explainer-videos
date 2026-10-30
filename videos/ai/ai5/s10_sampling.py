from __future__ import annotations


import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import DATA, MODEL, MONO, load, printable

ALPHA27 = " abcdefghijklmnopqrstuvwxyz"
TEMP = "#FF6B8B"  # the temperature dial


def softmax_T(z, T):
    a = (z - z.max()) / T
    p = np.exp(a)
    return p / p.sum()


class Sampling(VoiceoverScene):
    def construct(self):
        self.card()
        self.stick()
        self.temperature()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(4, r"Rolling loaded dice", r"How does a model actually choose?", part=5)
        with self.voiceover("Chapter four. Rolling loaded dice."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def stick(self):
        freq = np.asarray(load("markov")["freq"])
        assert abs(freq.sum() - 1) < 1e-9
        W, y0, h = 12.4, 0.9, 0.7
        edges = np.concatenate([[0], np.cumsum(freq)])
        palette = [ManimColor(DATA), ManimColor("#7C7FE0"), ManimColor(C.INTERVAL), ManimColor(MODEL)]
        segs, labs = VGroup(), VGroup()
        for i, ch in enumerate(ALPHA27):
            a, b = edges[i], edges[i + 1]
            r = Rectangle(width=W * (b - a), height=h, stroke_width=1, stroke_color=BACKGROUND,
                          fill_color=palette[i % 4], fill_opacity=0.55).move_to([-W / 2 + W * (a + b) / 2, y0, 0])
            segs.add(r)
            if W * (b - a) > 0.3:
                labs.add(Text("␣" if ch == " " else ch, font=MONO, font_size=22).move_to(r))
        # the same probabilities first as bars, standing up
        bw = 0.34
        stand = VGroup(*[Rectangle(width=bw, height=max(9.0 * f, 0.02), stroke_width=0, fill_color=palette[i % 4],
                                   fill_opacity=0.55) for i, f in enumerate(freq)])
        for i, r in enumerate(stand):
            r.move_to([-(27 * (bw + 0.08)) / 2 + i * (bw + 0.08) + bw / 2, -2.2 + r.height / 2, 0])
        stand_l = VGroup(*[Text("␣" if c == " " else c, font=MONO, font_size=18, color=GREY_A)
                           .next_to(stand[i], DOWN, buff=0.1).set_y(-2.45) for i, c in enumerate(ALPHA27)])
        dist_l = label(r"a model's output: \ a probability for every letter", font_size=28, color=GREY_A)
        dist_l.next_to(stand, UP, buff=0.4)
        z0 = MathTex("0", font_size=28, color=GREY_B).next_to(segs, LEFT, buff=0.15)
        z1 = MathTex("1", font_size=28, color=GREY_B).next_to(segs, RIGHT, buff=0.15)
        head = label(r"Every letter gets a stretch of $[0, 1)$ as long as its probability", font_size=30)
        head.to_edge(UP, buff=0.5)
        u = ValueTracker(0.5)
        needle = always_redraw(lambda: VGroup(
            Line([-W / 2 + W * u.get_value(), y0 + h / 2 + 0.55, 0], [-W / 2 + W * u.get_value(), y0 - h / 2 - 0.05, 0],
                 color=WHITE, stroke_width=3),
            Triangle(color=WHITE, fill_opacity=1, stroke_width=0).scale(0.09).rotate(PI)
            .move_to([-W / 2 + W * u.get_value(), y0 + h / 2 + 0.6, 0])))
        uv = DecimalNumber(0.5, num_decimal_places=3, font_size=30)
        uv.add_updater(lambda m: m.set_value(u.get_value()).next_to([-W / 2 + W * u.get_value(), y0 + h / 2 + 0.85, 0],
                                                                       UP, buff=0.0))
        g = np.random.default_rng(4)
        draws = g.random(16)
        out_l = label(r"drawn:", font_size=30, color=GREY_A).move_to([-5.4, -1.0, 0])
        out = VGroup()
        rule = label(r"a uniform random number $u$; \ the letter whose stretch contains it", font_size=28, color=C.BITS)
        rule.to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "A model never hands us a letter or a word. It hands us a distribution, and to write anything we have to "
            "roll the dice. <bookmark mark='a'/> Here's how a computer rolls loaded dice. Lay the probabilities end "
            "to end, from zero to one, so each letter owns a stretch exactly as long as its probability. "
            "<bookmark mark='b'/> Pick a uniformly random point, and take the letter it lands in. Each letter wins "
            "exactly as often as its probability says. <bookmark mark='c'/> These letters are drawn from part one's "
            "letter frequencies."
        ) as vo:
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in stand], lag_ratio=0.03), FadeIn(stand_l),
                      FadeIn(dist_l), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeOut(dist_l), FadeOut(stand_l), FadeIn(head),
                      LaggedStart(*[ReplacementTransform(r, sg) for r, sg in zip(stand, segs)], lag_ratio=0.03),
                      run_time=2.2)
            self.play(FadeIn(labs), FadeIn(z0), FadeIn(z1))
            vo.wait_until("b")
            self.play(FadeIn(needle), FadeIn(uv), FadeIn(rule))
            vo.wait_until("c")
            self.play(FadeIn(out_l))
            for j, r in enumerate(draws):
                i = int(np.searchsorted(edges, r, side="right") - 1)
                ch = ALPHA27[i]
                t = Text("␣" if ch == " " else ch, font=MONO, font_size=30, color=palette[i % 4])
                t.move_to([-4.6 + 0.42 * j, -1.0, 0])
                self.play(u.animate.set_value(r), run_time=0.45 if j < 4 else 0.25)
                self.play(Indicate(segs[i], color=WHITE, scale_factor=1.0), TransformFromCopy(segs[i], t),
                          run_time=0.45 if j < 4 else 0.25)
                out.add(t)
        needle.clear_updaters()
        uv.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def temperature(self):
        d = load("temperature")
        z = np.asarray(d["logits"], float)
        top = [int(i) for i in d["top"]]
        toks = [t.strip() for t in d["top_tokens"]]
        for T in (0.5, 1.0, 2.0):
            assert np.allclose(softmax_T(z, T)[top], np.asarray(d[f"p{T}"]), atol=1e-6)
        n_vocab = len(z)
        Tt = ValueTracker(1.0)
        p1 = softmax_T(z, 1.0)[top]
        bars = LiveBars(p1, max_value=0.24, height=3.4, bar_width=0.62, gap=0.22, colors=MODEL,
                        label_mobs=[Text(t, font=MONO, font_size=22, color=GREY_A) for t in toks])
        bars.place(-1.9, x=-2.4)
        for i, lab in enumerate(bars.labels):  # every other word one line lower, so long ones don't collide
            if i % 2:
                lab.shift(DOWN * 0.32)
        for i, tr in enumerate(bars.trackers):
            tr.add_updater(lambda m, i=i: m.set_value(float(softmax_T(z, Tt.get_value())[top[i]])))
        prompt = Text(d["prompt"] + " …", font="DejaVu Serif", font_size=26, color=WHITE).to_edge(UP, buff=0.4)
        prompt.set_x(-2.0)
        sub = label(r"GPT-2's ten favourite next words, \ out of $50{,}257$", font_size=24, color=GREY_A)
        sub.next_to(prompt, DOWN, buff=0.2).align_to(prompt, LEFT)
        colors = {r"T": TEMP, r"z_i": MODEL, r"z_j": MODEL}
        f = cmath(r"q_i \;\propto\; \exp\!\big(", r"z_i", r"\,/\,", r"T", r"\big)", colors=colors, font_size=44)
        f.move_to([4.4, 1.6, 0])
        tv = DecimalNumber(1.0, num_decimal_places=2, font_size=40, color=TEMP)
        tv.add_updater(lambda m: m.set_value(Tt.get_value()))
        trd = VGroup(MathTex(r"T =", font_size=40, color=TEMP), tv).arrange(RIGHT, buff=0.15).next_to(f, DOWN, buff=0.45)

        def ent():
            q = softmax_T(z, Tt.get_value())
            q = q[q > 0]
            return float(-(q * np.log2(q)).sum())

        hv = DecimalNumber(ent(), num_decimal_places=1, font_size=34, color=C.SURPRISE)
        hv.add_updater(lambda m: m.set_value(ent()))
        hrd = VGroup(label(r"entropy:", font_size=30), hv, label(r"bits", font_size=30)).arrange(RIGHT, buff=0.15)
        hrd.next_to(trd, DOWN, buff=0.3)
        rv = DecimalNumber(100 * (1 - p1.sum()), num_decimal_places=0, font_size=30, color=GREY_A, unit=r"\%")
        rv.add_updater(lambda m: m.set_value(100 * (1 - softmax_T(z, Tt.get_value())[top].sum())))
        rest = VGroup(label(rf"the other ${n_vocab - 10:,}$:".replace(",", "{,}"), font_size=26, color=GREY_A), rv)
        rest.arrange(RIGHT, buff=0.15).next_to(hrd, DOWN, buff=0.3)
        with self.voiceover(
            "Language models do the same with words, with one dial added. <bookmark mark='a'/> Here's GPT-2's "
            "distribution for the word after: Spade sat down in the armchair, and. Its favourite, I, gets only four "
            "percent; the other fifty thousand words share the rest. <bookmark mark='b'/> The dial is the "
            "temperature: divide the scores by T before the softmax, the exponentiate-and-rescale of part one."
        ) as vo:
            self.play(FadeIn(prompt), FadeIn(sub))
            vo.wait_until("a")
            self.add(*bars.trackers)  # their updaters follow the temperature
            self.play(FadeIn(bars), FadeIn(rest))
            vo.wait_until("b")
            self.play(Write(f), FadeIn(trd), FadeIn(hrd))
        with self.voiceover(
            "Turn it down, below one, and the distribution sharpens toward the favourites. <bookmark mark='a'/> Turn "
            "it up, and it flattens, until any word at all might come next. <bookmark mark='b'/> The entropy, part "
            "one's measure of uncertainty, follows the dial: under five bits at a half, nine at one, thirteen and a half "
            "at two."
        ) as vo:
            self.play(Tt.animate.set_value(0.5), run_time=2.5)
            vo.wait_until("a")
            self.play(Tt.animate.set_value(2.0), run_time=3.0)
            vo.wait_until("b")
            self.play(Tt.animate.set_value(1.0), run_time=1.5)
        for tr in bars.trackers:
            tr.clear_updaters()
        for m in (tv, hv, rv):
            m.clear_updaters()
        bars.freeze()
        self.wait(0.2)
        self.clear_scene()
        # what comes out
        samples = d["samples"]
        rows = VGroup()
        for T, name in (("0.0", r"$T \to 0$: \ always the favourite"), ("0.5", r"$T = 0.5$"), ("1.0", r"$T = 1$"),
                        ("2.0", r"$T = 2$")):
            tag = label(name, font_size=28, color=TEMP)
            words = ("… " + printable(samples[T])).split()
            lines, cur = [], ""
            for w in words:  # wrap at 12.6 units
                trial = (cur + " " + w).strip()
                if cur and Text(trial, font="DejaVu Serif", font_size=22).width > 12.6:
                    lines.append(cur)
                    cur = w
                else:
                    cur = trial
            lines.append(cur)
            txt = VGroup(*[Text(l_, font="DejaVu Serif", font_size=22, color=WHITE) for l_ in lines])
            txt.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            rows.add(VGroup(tag, txt).arrange(DOWN, aligned_edge=LEFT, buff=0.12))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.36).move_to(DOWN * 0.3)
        ph = Text(d["prompt"], font="DejaVu Serif", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here's what comes out, twenty-four words at a time. <bookmark mark='a'/> Always taking the favourite is "
            "safe and flat. <bookmark mark='b'/> At a half, still sensible. <bookmark mark='c'/> At one, sampling the "
            "model's own distribution, it's stranger and more varied. <bookmark mark='d'/> At two, it falls apart. "
            "Choosing how to sample is a real design decision, and we'll come back to it."
        ) as vo:
            self.play(FadeIn(ph))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k], shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
