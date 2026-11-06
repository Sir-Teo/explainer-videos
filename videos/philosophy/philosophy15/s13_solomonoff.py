from __future__ import annotations

from videos.philosophy.philosophy15.common import *  # noqa: F403


class Solomonoff(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"The universal prior", r"Can one prior learn every computable world?",
                            lit=(1964,), part=PART)
        with self.voiceover("Chapter twelve. The universal prior."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.idea()
        self.toy()
        self.catch()

    def idea(self):
        hc = history_card(1964, r"Ray Solomonoff", r"`A Formal Theory of Inductive Inference'", width=6.4,
                          color=HIST).to_corner(UL, buff=0.35)
        steps = VGroup(
            label(r"every hypothesis is a program \ for a universal machine $U$", font_size=23, color=WHITE),
            label(r"its prior weight: \ $2^{-\text{length}}$: \ short programs count for more", font_size=23,
                  color=PAST),
            MathTex(r"M(x) = \sum_{p\,:\ U(p) \text{ begins with } x} 2^{-|p|}", font_size=36, color=FUT),
            MathTex(r"M(1 \mid x) = \frac{M(x1)}{M(x)}", font_size=34, color=FUT),
        ).arrange(DOWN, buff=0.3).next_to(hc, DOWN, buff=0.4).set_x(0)
        thm = VGroup(label(r"if the data come from \textit{any} computable source $\mu$, \ with Kolmogorov complexity "
                           r"$K(\mu)$ \ (its shortest program's length):", font_size=21, color=GREY_A),
                     MathTex(r"\sum_{n} \mathbb{E}_\mu\big[(M(1\mid x_{<n}) - \mu(1 \mid x_{<n}))^2\big] \le "
                             r"\tfrac{\ln 2}{2}\, K(\mu)", font_size=30, color=OK)).arrange(DOWN, buff=0.15).to_edge(
            DOWN, buff=0.3)
        with self.voiceover(
            "Ray Solomonoff, in 1964, proposed a single prior for all of science. <bookmark mark='a'/>Treat every "
            "hypothesis as a program for a universal computer. <bookmark mark='b'/>Give each program prior weight "
            "two to the minus its length, so shorter programs count for more: Ockham, in bits. "
            "<bookmark mark='c'/>The universal prior of a data string x adds up the weights of every program whose "
            "output begins with x. <bookmark mark='d'/>To predict, condition: the probability that the next bit is "
            "one is M of x one over M of x. <bookmark mark='e'/>Solomonoff's theorem: if the data come from any "
            "computable source whatever, the total expected squared error of these predictions, summed over all "
            "time, is bounded by a constant times the Kolmogorov complexity of the source: the length of the shortest "
            "program that computes it. The errors must die out. One "
            "prior learns every computable world."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, s in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s) if mk in "ab" else Write(s))
            vo.wait_until("e")
            self.play(FadeIn(thm))
        self.clear_scene()

    def toy(self):
        d = load("solomonoff")
        run = d["run"]
        head = label(r"A toy universal prior", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        lang = stack([(r"programs: \ a bit pattern, \ printed over and over; \ weight $2^{-2|p|}$", WHITE),
                      (str(d["count"]) + r" programs up to length 8; \ the data: \ 011011011\dots", GREY_A)],
                     font_size=21).next_to(head, DOWN, buff=0.25)
        n = len(run)
        cw = 0.62
        x0 = -cw * (n - 1) / 2
        base_y = -1.6
        hmax = 2.4
        frame = DashedLine([x0 - 0.4, base_y + hmax, 0], [-x0 + 0.4, base_y + hmax, 0], color=GREY_D,
                           stroke_width=1)
        bars, bits, errs = VGroup(), VGroup(), VGroup()
        for k, r in enumerate(run):
            # the probability given to the bit that actually came
            p_true = r["p_one"] if r["next"] == "1" else 1 - r["p_one"]
            b = Rectangle(width=cw - 0.14, height=max(p_true * hmax, 0.03), stroke_width=0,
                          fill_color=OK if p_true > 0.5 else BAD, fill_opacity=0.85)
            b.move_to([x0 + k * cw, base_y + b.height / 2, 0])
            bars.add(b)
            bits.add(MathTex(r["next"], font_size=26).move_to([x0 + k * cw, base_y - 0.3, 0]))
        bl = label(r"probability given to the bit that came", font_size=18, color=GREY_B).next_to(frame, UP,
                                                                                                buff=0.08)
        lock = next(k for k, r in enumerate(run) if r["best"] == "011" and all(q["best"] == "011" for q in run[k:]))
        first_sure = next(k for k, r in enumerate(run) if min(r["p_one"], 1 - r["p_one"]) < 0.01)
        mark_ = Brace(VGroup(*bars[lock:]), DOWN, buff=0.45, color=FUT)
        ml = label(r"leading hypothesis from here: \ `011'", font_size=19, color=FUT).next_to(mark_, DOWN, buff=0.1)
        foot = label(r"after " + str(first_sure) + r" bits it is 99\% sure; \ after 9, \ certain: \ the other "
                     r"programs are refuted", font_size=21, color=GOAL).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "The real universal prior cannot be computed, but the Reasoner can run a toy version. "
            "<bookmark mark='a'/>In the toy language a program is a bit pattern, printed over and over, with "
            "weight two to the minus twice its length. There are five hundred and ten programs up to length eight. "
            "The data are zero one one, repeated. <bookmark mark='b'/>Each bar shows the probability the mixture "
            "gave to the bit that actually came. <bookmark mark='c'/>At first it is guessing: shorter patterns "
            "predict wrongly, and are refuted. <bookmark mark='d'/>From the fourth bit on, the leading hypothesis is "
            "zero one one, and the bars climb. <bookmark mark='e'/>By the seventh bit the mixture is ninety nine "
            "percent sure, and after the ninth it is certain, because every program that disagrees has been "
            "refuted. This is induction by elimination, weighted by simplicity."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lang))
            vo.wait_until("b")
            self.play(Create(frame), FadeIn(bl))
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(bars[k], DOWN), FadeIn(bits[k])) for k in
                                    range(lock)], lag_ratio=0.4))
            vo.wait_until("d")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(bars[k], DOWN), FadeIn(bits[k])) for k in
                                    range(lock, n)], lag_ratio=0.15), run_time=3)
            self.play(FadeIn(mark_), FadeIn(ml))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def catch(self):
        head = label(r"The catch", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"incomputable", r"to sum over all programs, \ you must know which halt: \ Part 7", BAD),
            (r"so Putnam's diagonal", r"does not apply: \ $M$ escapes it by being incomputable", GOAL),
            (r"machine-relative", r"another universal machine $V$: \ $K_U(x) \le K_V(x) + c_{UV}$", PAST),
            (r"", r"the constant is fixed, \ but it can be huge: \ grue returns, \ as a choice of machine", PAST),
            (r"approximations", r"MDL \ (next chapter); \ Levin search; \ AIXI \ (Hutter, \ 2005)", FUT),
            (r"", r"`language modelling is compression' \ (Delétang et al., \ 2024)", FUT),
        ]
        g = VGroup()
        for i, (a, b, c) in enumerate(rows):
            x = label(a, font_size=22, color=c)
            y = label(b, font_size=21)
            x.move_to([-6.2 + x.width / 2, 1.6 - i * 0.78, 0])
            y.move_to([-2.4 + y.width / 2, 1.6 - i * 0.78, 0])
            g.add(VGroup(x, y))
        with self.voiceover(
            "There is a catch, in three parts. <bookmark mark='a'/>The universal prior is incomputable. To add up "
            "the weights of all programs whose output begins with x, you would have to know which programs halt, "
            "and Part 7 showed that no machine can. <bookmark mark='b'/>That is how it escapes Putnam's diagonal: "
            "the diagonal defeats only computable predictors. <bookmark mark='c'/>Second, the prior depends on the "
            "choice of universal machine. Switching machines changes every complexity by at most a constant. "
            "<bookmark mark='d'/>But the constant can be enormous, and over any finite stretch of data it can make "
            "grue simpler than green. Goodman's riddle comes back as the choice of a machine. "
            "<bookmark mark='e'/>Third, all practical use is by approximation: minimum description length, Levin's "
            "search, Marcus Hutter's AIXI agent. <bookmark mark='f'/>And today's language models, trained to "
            "predict the next token, are compressors in exactly this sense."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
