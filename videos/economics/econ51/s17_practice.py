from __future__ import annotations

from videos.economics.econ51.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 15, r"In practice: \ model teams and estimation", r"Who solves economies, \ and how often?",
             "Chapter fifteen. In practice: model teams and estimation.", lit={1965: r"Moore", 1987: r"Rust",
                                                                              1996: r"FRB/US"},
             scale=("nation", "world"), horizon=("a decade",))
        self.people()
        self.estimation()
        self.called()

    def people(self):
        rows = VGroup(
            label(r"central banks: \ model teams; \ the Federal Reserve's FRB/US, \ in use since 1996", font_size=22,
                  color=VFI),
            label(r"perturbation by free software: \ Dynare, \ developed since the 1990s", font_size=22,
                  color=PERT),
            label(r"structural estimation: \ the model solved inside every evaluation of the likelihood",
                  font_size=22, color=PROJ),
            label(r"heterogeneous agents: \ a household like chapter five's, \ for every candidate price \ "
                  r"(Part 52)", font_size=22, color=EGM),
            label(r"industry: \ pricing, \ inventories, \ fleets, \ by the same dynamic programming", font_size=22,
                  color=POLICY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.2)
        head = label(r"who solves economies", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Who uses these methods? <bookmark mark='a'/> Central banks keep model teams; the Federal Reserve's "
            "large model, FRB/US, has been in use since 1996. <bookmark mark='b'/> Many of their smaller models are "
            "solved by perturbation, often with Dynare, free software developed since the 1990s. <bookmark "
            "mark='c'/> Academic economists estimate models structurally, which means solving the model again "
            "inside every evaluation of the likelihood. <bookmark mark='d'/> Models with many different "
            "households, the subject of the next part, solve a household like chapter five's for every candidate "
            "interest rate. <bookmark mark='e'/> And firms use the same dynamic programming to price seats and "
            "rooms, manage inventories and replace equipment."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.1))
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=WHITE, scale_factor=1.03))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def estimation(self):
        G = load("growth")
        chain = flow_chain([(r"guess the \\ parameters", POLICY), (r"solve the \\ model", VALUE),
                            (r"simulate or \\ compute moments", EGM), (r"compare with \\ the data", PROJ),
                            (r"a better \\ guess", POLICY)],
                           box_w=2.2, box_h=1.05, buff=0.42, font_size=19,
                           notes=[r"", rf"{1000 * G['howard_seconds']:.0f} ms here", r"", r"likelihood \\ or moments",
                                  r"thousands of \\ times over"], note_size=15)
        chain.move_to(UP * 0.8)
        foot = VGroup(
            label(r"Rust's nested fixed point \ (Part 44): \ the bus engine problem solved inside each step",
                  font_size=21, color=WHITE),
            label(r"a solver a thousand times too slow makes an estimation a thousand times too slow", font_size=21,
                  color=ERR),
        ).arrange(DOWN, buff=0.3).next_to(chain, DOWN, buff=0.8)
        with self.voiceover(
            "Why speed matters so much there. <bookmark mark='a'/> An estimation guesses the parameters, <bookmark "
            "mark='b'/> solves the model, <bookmark mark='c'/> computes what the model says about the data, "
            "<bookmark mark='d'/> compares, <bookmark mark='e'/> and guesses again, thousands of times over. "
            "<bookmark mark='f'/> John Rust's nested fixed point of Part forty-four works exactly so, solving the "
            "bus engine problem inside each step. A solver a thousand times too slow makes the estimation a "
            "thousand times too slow, and a solver that is not accurate makes the estimates wrong."
        ) as vo:
            for i, mk in enumerate("abcde"):
                vo.wait_until(mk)
                if i == 0:
                    self.play(FadeIn(chain.boxes[0]), FadeIn(chain.notes[0]))
                else:
                    self.play(GrowArrow(chain.arrows[i - 1]), FadeIn(chain.boxes[i]), FadeIn(chain.notes[i]),
                              run_time=0.9)
            vo.wait_until("f")
            self.play(FadeIn(foot[0]), FadeIn(foot[1]))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["moore_1965"]
        F = load("film")
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said).replace("65,000", "65{,}000"),
                       tex_safe(c.outcome).replace("2,300", "2{,}300"), c.verdict, width=12.6, font_size=17)
        cc.move_to(UP * 1.5)
        ax = plane([1969, 2023], [3, 11], center=DOWN * 2.1 + LEFT * 0.8, x_length=7.6, y_length=2.6,
                   xticks=[1970, 1990, 2010], yticks=[3, 7, 11], xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"10^{{{y:.0f}}}", font_size=12)
        t = np.array(F["t"])
        v = np.array(F["log10"])
        line = path(ax, t, v, VALUE, 2.4, smooth=False)
        rate = path(ax, [t[0], t[-1]], [v[0], v[0] + (t[-1] - t[0]) * np.log10(2) / 2], GREY_B, 1.4)
        rate = DashedVMobject(rate, num_dashes=30)
        cap = label(rf"transistors per \\ microprocessor; \\ dashed: \ doubling \\ every two years \\ (measured: "
                    rf"{F['doubling_years']:.1f})", font_size=12, color=GREY_A).next_to(ax, RIGHT, buff=0.35)
        tag = published_tag(r"Moore (1965, 1975); \ Rupp (2022), \ via Our World in Data", corner=DL, font_size=11)
        with self.voiceover(
            "Called it? A forecast about the machines themselves. <bookmark mark='a'/> In April 1965 Gordon Moore, "
            "then director of research at Fairchild Semiconductor, plotted a handful of points and predicted in "
            "the magazine Electronics that by 1975 the cheapest chips would carry about sixty-five thousand "
            "components, the number doubling every year. <bookmark mark='b'/> In 1975 he reported that the "
            "projection had been met, and revised the pace to a doubling every two years. <bookmark mark='c'/> That "
            "pace held for half a century: the largest microprocessor grew from about two thousand three hundred "
            f"transistors in 1971 to {F['last'] / 1e9:.0f} billion in 2021, doubling about every "
            f"{F['doubling_years']:.1f} years. <bookmark mark='d'/> The verdict: right, with one revision, and the "
            "revision was made in the open. Every method in this part rides on that curve."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1][0]), FadeIn(cc.left), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(ax), run_time=0.8)
            vo.wait_until("b")
            self.play(FadeIn(cc.right))
            vo.wait_until("c")
            self.play(Create(line), Create(rate), FadeIn(cap), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()
