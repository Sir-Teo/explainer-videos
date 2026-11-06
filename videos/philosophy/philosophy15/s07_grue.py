from __future__ import annotations

from videos.philosophy.philosophy15.common import *  # noqa: F403

SEED_C = ["#5FD38D", "#F28EC2", "#6FB7FF", "#FFD166", "#F2A65A", "#B08CFF", "#5EE6D0", "#E8E8E8"]


class Grue(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Grue", r"Which regularities should we project?", lit=(1955,), part=PART)
        with self.voiceover("Chapter six. Grue."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.goodman()
        self.symmetry()
        self.network()
        self.entrench()

    def goodman(self):
        hc = history_card(1955, r"Nelson Goodman", r"\textit{Fact, Fiction, and Forecast}: \ the new riddle",
                          width=6.4, color=HIST).to_corner(UL, buff=0.35)
        defn = MathTex(r"\text{grue}(x) \iff (\text{examined before } T \wedge \text{green}) \vee "
                       r"(\lnot\,\text{examined before } T \wedge \text{blue})", font_size=30,
                       color=FUT).next_to(hc, DOWN, buff=0.35).set_x(0)
        y0 = -0.4
        tline = Line([-6.0, y0, 0], [6.0, y0, 0], color=GREY_C, stroke_width=2)
        tT = DashedLine([0.6, y0 + 1.6, 0], [0.6, y0 - 2.2, 0], color=GOAL, stroke_width=2)
        tl = label(r"$T$: \ now", font_size=20, color=GOAL).next_to(tT, UP, buff=0.08)
        past = VGroup(*[emerald(GREENC, 0.22).move_to([-5.6 + i * 0.62, y0 + 0.5, 0]) for i in range(10)])
        fut_g = VGroup(*[emerald(GREENC, 0.22).move_to([1.2 + i * 0.62, y0 + 0.5, 0]) for i in range(8)])
        fut_b = VGroup(*[emerald(BLUEC, 0.22).move_to([1.2 + i * 0.62, y0 - 1.0, 0]) for i in range(8)])
        lg = label(r"`all emeralds are green' \ predicts", font_size=19, color=GREENC).move_to(
            [fut_g.get_x(), y0 - 0.3, 0])
        lb = label(r"`all emeralds are grue' \ predicts", font_size=19, color=BLUEC).next_to(fut_b, DOWN,
                                                                                         buff=0.15)
        pl = label(r"every emerald examined: \ green, \ \textit{and} grue", font_size=19, color=PAST).move_to(
            [past.get_x(), y0 - 0.3, 0])
        foot = label(r"the same evidence, \ equally `instances', \ opposite predictions", font_size=24,
                     color=BAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Hume asked why we should project past regularities at all. In 1955 Nelson Goodman asked a harder "
            "question: which ones? <bookmark mark='a'/>Define a new predicate, grue. Something is grue if it is "
            "examined before a time T and green, or not examined before T and blue. <bookmark mark='b'/>Every emerald "
            "we have ever examined is green. Each of them was examined before T, so each one is also grue. "
            "<bookmark mark='c'/>The hypothesis that all emeralds are green predicts that the emeralds examined "
            "after T will be green. <bookmark mark='d'/>The hypothesis that all emeralds are grue predicts that they "
            "will be blue. <bookmark mark='e'/>The two hypotheses have exactly the same instances so far, and they "
            "make opposite predictions. Instance confirmation cannot tell them apart."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(defn))
            vo.wait_until("b")
            self.play(Create(tline), Create(tT), FadeIn(tl),
                      LaggedStart(*[FadeIn(e, scale=1.4) for e in past], lag_ratio=0.1), run_time=2)
            self.play(FadeIn(pl))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(e) for e in fut_g], lag_ratio=0.08), FadeIn(lg))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(e) for e in fut_b], lag_ratio=0.08), FadeIn(lb))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def symmetry(self):
        d = load("grue")["basic"]
        head = label(r"`But grue is gerrymandered'", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        left = VGroup(label(r"our language", font_size=24, color=GREENC),
                      MathTex(r"\text{grue} = \text{green before } T, \text{ blue after}", font_size=28),
                      MathTex(r"\text{bleen} = \text{blue before } T, \text{ green after}", font_size=28)).arrange(
            DOWN, buff=0.2)
        right = VGroup(label(r"the grue speaker's language", font_size=24, color=BLUEC),
                       MathTex(r"\text{green} = \text{grue before } T, \text{ bleen after}", font_size=28),
                       MathTex(r"\text{blue} = \text{bleen before } T, \text{ grue after}", font_size=28)).arrange(
            DOWN, buff=0.2)
        lr = VGroup(left, right).arrange(RIGHT, buff=1.0).next_to(head, DOWN, buff=0.4)
        lrn = stack([
            (r"one learner \ (logistic regression on time), \ the same ten observations, \ two encodings", WHITE),
            (r"encoded green/blue: \ predicts \textit{green} after $T$ \ with probability " +
             f"{d['green_encoding_says_green']:.4f}", GREENC),
            (r"encoded grue/bleen: \ predicts \textit{grue}, \ that is \textit{blue}, \ after $T$ \ with probability "
             + f"{d['grue_encoding_says_blue']:.4f}", BLUEC),
            (r"`more of the same' is relative to the vocabulary", GOAL),
        ], font_size=22).next_to(lr, DOWN, buff=0.5)
        with self.voiceover(
            "The obvious reply is that grue is gerrymandered: it mentions a time, and green does not. "
            "<bookmark mark='a'/>But the symmetry is exact. In our language, grue is green before T and blue after. "
            "<bookmark mark='b'/>In the language of someone who speaks of grue and bleen, green is grue before T and "
            "bleen after. Whose predicate mentions time depends on where you stand. <bookmark mark='c'/>The Reasoner "
            "makes this concrete. One learner, logistic regression on time, gets the same ten observations, "
            "encoded two ways. <bookmark mark='d'/>Encoded as green or blue, it predicts green after T, with "
            "probability point nine nine nine five. <bookmark mark='e'/>Encoded as grue or bleen, it predicts grue, "
            "which is to say blue, with exactly the same confidence. <bookmark mark='f'/>The learner projects more "
            "of the same, and more of the same is relative to the vocabulary it is given."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            for mk, r in zip("cdef", lrn):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def network(self):
        d = load("grue")
        T, H = d["T"], d["H"]
        head = label(r"Grue in a neural network", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        setup = stack([(r"input: \ the time, \ and a feature `after $T$?' \ that is 0 on every training example",
                        WHITE),
                       (r"eight networks, \ eight random initializations, \ the same data", GREY_A)],
                      font_size=21).next_to(head, DOWN, buff=0.25)
        ax = Axes(x_range=[0, H - 1, 5], y_range=[0, 1, 0.5], x_length=7.6, y_length=3.6, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 18}).move_to([-2.2, -1.4, 0])
        yl = label(r"P(green)", font_size=19, color=GREENC).next_to(ax.y_axis, UP, buff=0.1)
        xl = label(r"time", font_size=19, color=GREY_B).next_to(ax.x_axis, DOWN, buff=0.35)
        tT = DashedLine(ax.c2p(T - 0.5, 0), ax.c2p(T - 0.5, 1.05), color=GOAL, stroke_width=2)
        tl = label(r"$T$", font_size=20, color=GOAL).next_to(tT, UP, buff=0.05)
        obs = VGroup(*[Dot(ax.c2p(i, 1.0), radius=0.06, color=GREENC) for i in range(T)])
        curves = VGroup(*[series_plot(ax, r, SEED_C[k], width=2.5) for k, r in enumerate(d["stepped"])])
        bars = VGroup()
        for k, (fit, aft) in enumerate(zip(d["train_fit"], d["after_T_green"])):
            b = Rectangle(width=0.32, height=max(aft * 2.6, 0.03), stroke_width=0, fill_color=SEED_C[k],
                          fill_opacity=0.85)
            b.move_to([3.2 + k * 0.42, -2.9 + b.height / 2, 0])
            bars.add(b)
        bt = label(r"after $T$: \ P(green)", font_size=19, color=GREY_A).next_to(bars, UP, buff=0.2).shift(UP * 0.0)
        bars_t = label(r"training fit: \ all " + f"{min(d['train_fit']):.3f}" + r"+", font_size=19,
                       color=PAST).next_to(bt, UP, buff=0.15)
        base = Line([3.0, -2.9, 0], [6.3, -2.9, 0], color=GREY_C, stroke_width=2)
        foot = stack([(r"the data fix the training fit;", GOAL), (r"only the inductive bias fixes the rest", GOAL)],
                     font_size=20).next_to(base, DOWN, buff=0.2)
        with self.voiceover(
            "Grue is not a philosopher's toy. It is the central fact about machine learning. "
            "<bookmark mark='a'/>Give a small neural network two inputs: the time, and a feature that says whether "
            "we are past T. On every training example that feature is zero, so the data say nothing about its "
            "weight. <bookmark mark='b'/>Train eight networks from eight random starting points on the same ten "
            "green emeralds. <bookmark mark='c'/>All eight fit the training data perfectly. <bookmark mark='d'/>After "
            "T they disagree. Most project green. One projects grue, confidently. Others hedge. "
            "<bookmark mark='e'/>The data fix behaviour on the data and nowhere else. What a network does off its "
            "training distribution is settled by its inductive bias: the architecture, the initialization, the "
            "training procedure. That is distribution shift, and it is Goodman's riddle."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(setup[0]))
            vo.wait_until("b")
            self.play(FadeIn(setup[1]), FadeIn(ax), FadeIn(yl), FadeIn(xl), Create(tT), FadeIn(tl), FadeIn(obs))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.15), run_time=3)
            self.play(FadeIn(bars_t))
            vo.wait_until("d")
            self.play(FadeIn(base), FadeIn(bt), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def entrench(self):
        head = label(r"What makes a predicate projectible?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Goodman", r"entrenchment: \ predicates with a history of successful projection", PAST),
            (r"Quine \ (1969)", r"natural kinds: \ a similarity space shaped by evolution, \ then by science", GREENC),
            (r"Bayesians", r"the prior: \ it simply weights `green' above `grue'", FUT),
            (r"learning theory", r"inductive bias: \ every learner has one; \ no data can supply it", GOAL),
        ]
        g = VGroup()
        for i, (a, b, c) in enumerate(rows):
            x = label(a, font_size=23, color=c)
            y = label(b, font_size=21)
            x.move_to([-6.2 + x.width / 2, 1.5 - i * 0.95, 0])
            y.move_to([-3.3 + y.width / 2, 1.5 - i * 0.95, 0])
            g.add(VGroup(x, y))
        foot = label(r"every answer names something the evidence itself does not contain", font_size=23,
                     color=BAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "So what makes green projectible and grue not? <bookmark mark='a'/>Goodman's answer was entrenchment: "
            "green has a long history of successful projections, grue has none. <bookmark mark='b'/>Quine appealed "
            "to natural kinds, and to a sense of similarity that evolution gave us and science refines. "
            "<bookmark mark='c'/>For a Bayesian the answer is the prior, which weights green above grue. "
            "<bookmark mark='d'/>In learning theory the name is inductive bias, and every learner has one. "
            "<bookmark mark='e'/>Each answer names something that the evidence itself does not contain."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
