from __future__ import annotations

from videos.economics.econ53.common import *  # noqa: F403


def matrix_card(M, title: str, color, rows=(r"good", r"bad"), cols=(r"$s_1$", r"$s_2$")):
    head = label(title, font_size=21, color=color)
    cells = VGroup(label(r"", font_size=16), *[label(c, font_size=17, color=GREY_A) for c in cols])
    for r, row in zip(rows, M):
        cells.add(label(r, font_size=17, color=GREY_A), *[label(f"{v:.2f}", font_size=19, color=WHITE) for v in row])
    cells.arrange_in_grid(rows=len(rows) + 1, cols=len(cols) + 1, buff=(0.4, 0.2))
    box = SurroundingRectangle(cells, buff=0.2, color=color, stroke_width=1.6, corner_radius=0.1)
    return VGroup(head, VGroup(cells, box)).arrange(DOWN, buff=0.2)


class Blackwell(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Blackwell's order", r"When is one source of information better for everyone?",
             "Chapter seven. Blackwell's order.", lit={1953: r"Blackwell"}, scale=("person",), horizon=("a day",))
        self.garble()
        self.values()

    def garble(self):
        B = load("blackwell")
        Pm = matrix_card(B["P"], r"experiment P", RECEIVER)
        Mg = matrix_card(B["garble"], r"a garbling", SIGNAL, rows=(r"$s_1$", r"$s_2$"), cols=(r"$t_1$", r"$t_2$"))
        Q = matrix_card(B["Q"], r"experiment Q = P, \ garbled", BELIEF, cols=(r"$t_1$", r"$t_2$"))
        R = matrix_card(B["R"], r"experiment R", SENDER)
        top = VGroup(Pm, MathTex(r"\times", font_size=40), Mg, MathTex(r"=", font_size=40), Q).arrange(
            RIGHT, buff=0.35).move_to(UP * 1.4)
        R.next_to(top, DOWN, buff=0.7)
        rows = VGroup(
            label(r"rows: \ the chance of each signal, \ given the state", font_size=19, color=GREY_A),
            label(r"Q is P with noise added: \ everyone weakly prefers P", font_size=21, color=BELIEF),
            label(r"P and R: \ neither is a garbling of the other", font_size=21, color=SENDER),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        tag = published_tag(r"Blackwell, \ Annals of Mathematical Statistics 24 (1953)", corner=DR, font_size=12)
        hc = history_card(1953, r"David Blackwell", r"``Equivalent comparisons of experiments'': \ when one source "
                          r"of information is better for every decision maker", color=RECEIVER, width=10.0,
                          font_size=24).move_to(UP * 0.4)
        with self.voiceover(
            "Information is worth something because it changes decisions, and different decision makers want "
            "different things. Is there ever a sense in which one source of information is simply better? In 1953 "
            "David Blackwell answered. <bookmark mark='a'/> An experiment is a table: in each state of the world, "
            "the chance of each signal. Experiment P is right ninety percent of the time when the state is good "
            "and eighty when it is bad. <bookmark mark='b'/> Now pass its signal through a garbling, a second "
            "table that scrambles it at random, and you get experiment Q. <bookmark mark='c'/> Blackwell's "
            "theorem: every decision maker, with any prior and any payoffs, weakly prefers P to Q if and only if Q "
            "is a garbling of P. <bookmark mark='d'/> But here is experiment R. When the state is good it almost "
            "never sends its second signal, so that signal is a near-certain warning; when the state is bad it "
            "sends the warning less than half the time. Neither P nor R is a garbling of the other: Agora's "
            "linear programme finds no garbling either way."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeOut(hc))
            self.play(FadeIn(Pm), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(top[1]), FadeIn(Mg), FadeIn(top[3]), FadeIn(Q))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(R), FadeIn(rows[2]))
        self.clear_scene()

    def values(self):
        B = load("blackwell")
        th = np.array(B["thresholds"])
        ax = plane([0, 1], [0, 0.3], center=LEFT * 1.8 + DOWN * 0.3, x_length=7.4, y_length=4.6,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 0.1, 0.2, 0.3],
                   xlabel=r"how sure of ``good'' you must be to act", ylabel=r"value of the experiment",
                   xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        cP = path(ax, th, B["values"]["P"], RECEIVER, 3.0, smooth=False)
        cQ = path(ax, th, B["values"]["Q"], BELIEF, 3.0, smooth=False)
        cR = path(ax, th, B["values"]["R"], SENDER, 3.0, smooth=False)
        side = VGroup(
            label(r"each point: \ a decision maker \\ who acts only if the chance \\ of ``good'' passes a threshold",
                  font_size=18, color=WHITE),
            label(r"blue P \ is above purple Q \\ everywhere", font_size=19, color=RECEIVER),
            label(r"gold R \ beats P for the \\ bold, \ loses for the cautious", font_size=19, color=SENDER),
            label(r"no garbling, \ no ranking: \\ who is better informed \\ depends on who is asking", font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "See it in decisions. <bookmark mark='a'/> Each point along the bottom is a decision maker who acts only "
            "if the chance that the state is good passes some threshold: a cautious one on the right, a bold one "
            "on the left. The height is what each experiment is worth to them. <bookmark mark='b'/> P is worth "
            "more than its garbling Q to every one of them, as Blackwell's theorem says. <bookmark mark='c'/> But R "
            "is worth more than P to the bold, who would act anyway and need only a reliable warning, and less to "
            "the cautious, who need reassurance R cannot give. <bookmark mark='d'/> When neither "
            "experiment is a garbling of the other, there is no answer to which is better, only to which is better "
            "for whom. The prosecutor's investigation was a garbling of the truth, chosen for the one decision "
            "maker she cared about."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(cP), run_time=1.4)
            vo.wait_until("b")
            self.play(Create(cQ), FadeIn(side[1]), run_time=1.4)
            vo.wait_until("c")
            self.play(Create(cR), FadeIn(side[2]), run_time=1.4)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
