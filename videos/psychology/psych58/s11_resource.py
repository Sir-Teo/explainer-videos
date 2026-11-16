from __future__ import annotations

from videos.psychology.psych58.common import *  # noqa: F403


class Resource(VoiceoverScene):
    def construct(self):
        card_section(self, 10, r"Resource rationality", r"Are heuristics optimal after all?")
        self.one()
        self.idea()

    def one(self):
        d = load("samples")
        head = heading(r"One and done")
        k = np.asarray(d["k"])
        A = axes([-0.1, 1.85], [0, 1.0], x_length=5.6, y_length=3.2, xticks=None, yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{v:g}", center=[-3.3, 0.2, 0], font_size=12)
        x = np.log10(k)
        ca = curve(A.ax, x, d["accuracy"], MODEL, stroke_width=4)
        rr = np.asarray(d["reward_rate"]) / np.max(d["reward_rate"])
        cr = curve(A.ax, x, rr, GOOD, stroke_width=4)
        ticks = VGroup(*[label(f"{int(v)}", font_size=12, color=GREY_A).next_to(A.ax.c2p(np.log10(v), 0), DOWN,
                                                                              buff=0.1) for v in (1, 2, 5, 10, 20, 50)])
        xl = label(r"samples drawn before deciding", font_size=13, color=GREY_A).next_to(ticks, DOWN, buff=0.1)
        key = VGroup(label(r"accuracy", font_size=13, color=MODEL),
                     label(r"reward per unit time (scaled)", font_size=13, color=GOOD)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.2)
        rows = rows_of([
            (r"Vul, \ Goodman, \ Griffiths and Tenenbaum, \ 2014: \ decide by drawing a few samples from your "
             r"posterior and taking the majority", WHITE),
            (r"more samples, \ more accuracy: \ from 0.65 with one to 0.98 with fifty", MODEL),
            (r"but if each sample costs time, \ reward per unit time peaks at one sample: \ your fourth number", GOOD),
            (r"probability matching, \ often called irrational, \ is what one-sample deciders do", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{efficient.samples\_value}")
        tag2 = published_tag(r"Vul et al.\ (2014)").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Are heuristics optimal after all? <bookmark mark='a'/> In 2014 Edward Vul, Noah Goodman, Thomas "
            "Griffiths and Joshua Tenenbaum modelled decisions made by drawing a few samples from the posterior and "
            "taking the majority. <bookmark mark='b'/> More samples give more accuracy: from zero point six five with "
            "one, to zero point nine eight with fifty. <bookmark mark='c'/> But if each sample costs time, reward "
            "per unit time peaks at a single sample. That's your fourth number. <bookmark mark='d'/> Probability "
            "matching, often called irrational, is just what one-sample deciders do."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), FadeIn(A), FadeIn(ticks), FadeIn(xl), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(ca))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(cr))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def idea(self):
        chips_section(self, r"Optimal use of limited computation", [
            (r"the idea", r"Lieder and Griffiths, \ 2020: \ the best strategy given the cost of thinking, \ not the "
                          r"best answer given unlimited time", MODEL),
            (r"heuristics", r"anchoring and adjusting, \ or taking the best cue (Part 26), \ can be rational when "
                            r"thinking is costly", PERSON),
            (r"a test", r"people shift strategies when costs and stakes change, \ in the direction the analysis "
                        r"predicts", GOOD),
            (r"the risk", r"with costs chosen freely, \ any behaviour is resource-rational: \ the costs must be "
                          r"measured too", AUTH),
        ], "Resource rationality makes this general. <bookmark mark='a'/> Falk Lieder and Thomas Griffiths define it "
           "as the best strategy given the cost of thinking, not the best answer given unlimited time. "
           "<bookmark mark='b'/> Heuristics such as anchoring and adjusting, or taking the best cue from Part 26, can "
           "be rational when thinking is costly. <bookmark mark='c'/> A test: people shift strategies when costs and "
           "stakes change, in the direction the analysis predicts. <bookmark mark='d'/> And the risk is the same as "
           "before: with costs chosen freely, any behaviour is resource-rational, so the costs must be measured too.",
           tag=published_tag(r"Lieder \& Griffiths (2020)"))
