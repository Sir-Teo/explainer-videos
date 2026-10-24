from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai27.common import ASSIST, GOLD, PART, PENALTY, PROXY, REWARD, USER, bubble, load, said


class Rewards(VoiceoverScene):
    def construct(self):
        self.card()
        self.compare()
        self.bradley_terry()
        self.ours()
        self.accuracy()

    def card(self):
        card = chapter_card(4, r"Learning what people prefer", r"How do you turn people's judgments into a number?",
                            lit=(2017, 2022), part=PART)
        with self.voiceover("Chapter four. Learning what people prefer."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def compare(self):
        q = bubble(r"Explain the moon to a six-year-old.", "user").move_to([0, 2.6, 0])
        a = bubble(r"The moon is a big ball of rock that goes \\ around the Earth. \ The sun lights it up.",
                   "assistant", width=5.6, font_size=22).move_to([-3.3, 0.6, 0])
        b = bubble(r"The Moon is Earth's sole natural satellite, \\ with a mean radius of 1,737 km.", "assistant",
                   width=5.6, font_size=22).move_to([3.3, 0.6, 0])
        score = VGroup(label(r"score it from $1$ to $10$: \ a $7$? \ an $8$?", font_size=26, color=GREY_A),
                       label(r"different people, \ different scales", font_size=22, color=GREY_B))
        score.arrange(DOWN, buff=0.15).move_to(DOWN * 1.5)
        pick = SurroundingRectangle(a, color=REWARD, buff=0.12, stroke_width=4)
        better = label(r"which is better? \ easy, \ and people mostly agree", font_size=26, color=REWARD)
        better.move_to(DOWN * 1.5)
        agree = note(r"InstructGPT's labellers agreed with each other on $73\%$ of comparisons (Ouyang et al., 2022)")
        agree.to_edge(DOWN, buff=0.35)
        tag = note(r"illustrative").to_corner(UR, buff=0.25)
        with self.voiceover(
            "Suppose you want a number that says how good an answer is. You could ask people to score answers from "
            "one to ten. <bookmark mark='a'/> But scores drift: one person's seven is another's eight, and the same "
            "person's scale moves during a day. <bookmark mark='b'/> Comparisons are much more reliable. Show two "
            "answers to the same question, and ask which is better. <bookmark mark='c'/> People still disagree, but "
            "less: InstructGPT's labellers agreed with each other on about seventy-three percent of comparisons. "
            "Comparisons are what the reward model learns from."
        ) as vo:
            self.play(FadeIn(q), FadeIn(a), FadeIn(b), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(score))
            vo.wait_until("b")
            self.play(FadeOut(score), Create(pick), FadeIn(better))
            vo.wait_until("c")
            self.play(FadeIn(agree))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bradley_terry(self):
        rows = [
            cmath(r"P(a \succ b)", r"=", r"\sigma\big(r(a) - r(b)\big)", r"=", r"\frac{1}{1 + e^{-(r(a) - r(b))}}",
                  font_size=36),
            cmath(r"P(a \succ b)", r"=", r"\frac{1}{1 + 10^{(R_b - R_a)/400}}", font_size=36),
            cmath(r"\mathcal L(\phi)", r"=", r"-\,\mathbb E_{(x,\, y_w,\, y_l)}\Big[\log \sigma\big(r_\phi(x, y_w) - "
                  r"r_\phi(x, y_l)\big)\Big]", font_size=36),
            cmath(r"r_\phi(x, y)", r"\to", r"r_\phi(x, y) + c(x)", font_size=36),
        ]
        rows[0][2].set_color(PROXY)
        rows[2][0].set_color(PROXY)
        whys = [why(r"Bradley \& Terry (1952): \ a score per answer"),
                why(r"the same model as Elo ratings, \ Part 26"),
                why(r"the winner $y_w$ should outscore the loser $y_l$: \ logistic regression on differences"),
                why(r"only differences are learned: \ any shift per question fits as well")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-2.2, buff=0.55, edge=6.9)
        with self.voiceover(
            "The standard model of comparisons is Bradley and Terry's, from 1952. Give every answer a hidden score, "
            "r. The chance that a beats b is the logistic sigmoid of the difference in their scores. "
            "<bookmark mark='a'/> If that looks familiar, it should: it is exactly the Elo model that rated "
            "AlphaZero's generations in Part 26, with a different scale. <bookmark mark='b'/> A reward model is a "
            "network, usually the fine-tuned language model with its last layer swapped for a single number, trained "
            "by maximum likelihood on the comparisons: make the winner's score exceed the loser's. It's logistic "
            "regression on differences, Part 6's loss in a new place. <bookmark mark='c'/> One consequence matters "
            "later. Only differences are ever seen, so the scores are only defined up to a shift for each question. "
            "A reward model says which answer is better, not how good an answer is on any absolute scale."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ours(self):
        pr = load("prefs")
        rm = load("rm")
        ex = [p for p in pr["test"] if len(p["chosen"]) < 90 and len(p["rejected"]) < 90][:2]
        q = bubble(rf"Write a line about the {ex[0]['topic']}.", "user", font_size=22).move_to([0, 2.7, 0])
        cw = said(ex[0]["chosen"], chars=36).move_to([-3.4, 1.0, 0])
        cl = said(ex[0]["rejected"], chars=36).move_to([3.4, 1.0, 0])
        mark = VGroup(label(r"preferred", font_size=22, color=REWARD).next_to(cw, DOWN, buff=0.15),
                      label(r"rejected", font_size=22, color=PENALTY).next_to(cl, DOWN, buff=0.15))
        gold = VGroup(
            label(r"our stand-in for human taste, \ \textit{gold}:", font_size=24, color=GOLD),
            label(r"cheerful words \ $+$, \ gloomy words \ $-$, \ past a dozen words \ $-$, \ repetition and "
                  r"empty answers \ $--$", font_size=22, color=GREY_A),
            label(r"simulated people: \ $P(a \succ b) = \sigma\big((\mathrm{gold}(a) - \mathrm{gold}(b)) / 0.25\big)$",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([0, -1.6, 0])
        n = len(pr["train"]) + len(pr["test"])
        tag = note(rf"computed: \ ${n:,}$ comparisons of our fine-tuned model's lines".replace(",", "{,}"))
        tag.to_corner(DR, buff=0.2)
        with self.voiceover(
            "Now we do it ourselves. Our fine-tuned model from chapter two writes lines on request: a line about the "
            "sea, a line about the night. <bookmark mark='a'/> We have no crowd of labellers, so we simulate one. "
            "Hidden from every model is a stand-in for human taste we'll call gold: it likes cheerful words, dislikes "
            "gloomy ones, prefers a line of about a dozen words to a paragraph, and strongly dislikes repetition and "
            "empty answers. <bookmark mark='b'/> Our simulated "
            "people compare two lines and prefer the one gold likes more, but not always: the closer the call, the "
            f"more often they pick the other one. <bookmark mark='c'/> That gives us {n:,} comparisons. From here on, "
            "everything that learns what people prefer sees only these comparisons, never gold itself, just as a "
            "real lab never sees inside its labellers' heads."
        ) as vo:
            self.play(FadeIn(q), FadeIn(cw), FadeIn(cl), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(gold[0]), FadeIn(gold[1]))
            vo.wait_until("b")
            self.play(FadeIn(gold[2]), FadeIn(mark))
            vo.wait_until("c")
            self.play(Indicate(tag))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def accuracy(self):
        rm = load("rm")
        sizes, acc = np.asarray(rm["sizes"], float), np.asarray(rm["acc"])
        ceil = float(rm["people_agree_gold"])
        lx = np.log10(sizes)
        x0, x1 = 1.8, float(np.ceil(lx.max() * 2) / 2)  # log10 of the comparisons (CornerAxes keeps its own shifted range)
        g = axes([x0, x1], [0.5, 1.0], x_length=7.0, y_length=4.0,
                 xlabel=r"comparisons it learned from (log scale)", ylabel=r"held-out comparisons it gets right",
                 xticks=[2, 3], yticks=[0.5, 0.75, 1.0], log_x=True, yfmt=lambda v: rf"{int(100 * v)}\%",
                 center=[-1.0, -0.3, 0])
        line = VGroup(*[Line(g.ax.c2p(a, b), g.ax.c2p(c, d_), color=PROXY, stroke_width=4)
                        for (a, b), (c, d_) in zip(zip(lx, acc), zip(lx[1:], acc[1:]))])
        dots = VGroup(*[Dot(g.ax.c2p(x, y), radius=0.07, color=PROXY) for x, y in zip(lx, acc)])
        cl = DashedLine(g.ax.c2p(x0, ceil), g.ax.c2p(x1, ceil), color=GOLD, dash_length=0.08)
        cll = label(rf"how often the simulated people agree with gold: \ ${100 * ceil:.0f}\%$", font_size=20,
                    color=GOLD).next_to(cl, UP, buff=0.08).align_to(cl, RIGHT)
        chance = DashedLine(g.ax.c2p(x0, 0.5), g.ax.c2p(x1, 0.5), color=GREY_C,
                            dash_length=0.06)
        tag = note(rf"computed: \ reward models on our fine-tuned model, \ ${rm['n_test']}$ held-out comparisons")
        tag.to_corner(DR, buff=0.2)
        cite_ = note(r"InstructGPT's reward model: \\ $69.6\%$ on held-out labellers \\ (Ouyang et al., 2022)",
                     font_size=20).move_to([4.7, 0.9, 0])
        with self.voiceover(
            "Train reward models on more and more of the comparisons, and test each on comparisons it has never seen. "
            f"<bookmark mark='a'/> With {int(sizes[0])} comparisons it gets {100 * acc[0]:.0f} percent right; with "
            f"{int(sizes[-1]):,}, {100 * acc[-1]:.0f} percent. <bookmark mark='b'/> It can't reach a hundred: the "
            f"people it learns from agree with gold only {100 * ceil:.0f} percent of the time, so that's the ceiling. "
            "<bookmark mark='c'/> Real reward models live in the same range. InstructGPT's predicted held-out "
            "labellers' choices about seventy percent of the time, close to how often the labellers agreed with "
            "each other. A reward model is an imperfect copy of an imperfect judge. Next we open ours up, and "
            "then see what happens when you optimize against it."
        ) as vo:
            self.play(FadeIn(g), Create(chance), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in dots], lag_ratio=0.2), Create(line), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(cl), FadeIn(cll))
            vo.wait_until("c")
            self.play(FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()
