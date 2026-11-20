from __future__ import annotations

from videos.economics.econ24.common import *  # noqa: F403


class Hosios(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Efficiency: \ the Hosios condition", r"Does the market create the right number of jobs?",
             "Chapter eight. Efficiency: the Hosios condition.", lit={1982: r"Diamond", 1990: r"Hosios"},
             scale=("market",), horizon=("years",))
        self.externalities()
        self.curve()
        self.thick()

    def externalities(self):
        rows = VGroup(
            label(r"a firm that opens one more vacancy:", font_size=24, color=JOB),
            label(r"makes it easier for the unemployed to find work \ (good for them)", font_size=22, color=MATCH),
            label(r"makes it harder for other firms to fill theirs \ (bad for them)", font_size=22, color=SEP),
            label(r"the firm counts neither: \ it counts only its own share of the surplus", font_size=23,
                  color=GREY_A),
            label(r"too little worker share: \ firms keep too much, \ open too many vacancies", font_size=22,
                  color=JOB),
            label(r"too much worker share: \ too few vacancies, \ too much unemployment", font_size=22,
                  color=WORKER),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        with self.voiceover(
            "Does this market create the right number of jobs? Think about one more vacancy. "
            "<bookmark mark='a'/> When a firm opens it, two things happen to other people. "
            "<bookmark mark='b'/> The unemployed find work a little faster. <bookmark mark='c'/> And other firms "
            "fill their own vacancies a little more slowly: congestion. <bookmark mark='d'/> The firm counts "
            "neither. It counts only the share of the match surplus it will keep, one minus beta. "
            "<bookmark mark='e'/> If workers' share is small, firms keep a lot, and they open too many vacancies "
            "that get in each other's way. <bookmark mark='f'/> If workers' share is large, firms open too few, "
            "and too many people wait unemployed. Somewhere between, the two effects cancel."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def curve(self):
        h = load("hosios")
        d = load("dmp")
        ax = plane([0, 1], [0.90, 0.965], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.2, y_length=5.0,
                   xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0.90, 0.92, 0.94, 0.96],
                   xlabel=r"the worker's bargaining share $\beta$", ylabel=r"net output a month \ (per member of the "
                   r"labour force)", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.2f}", font_size=16)
        line_ = path(ax, h["beta"], h["net"], color=MATCH, width=4)
        k = int(np.argmax(h["net"]))
        peak = dot(ax, h["beta"][k], h["net"][k], color=E.ACCENT, r=0.1)
        drop = seg(ax, d["eta"], 0.90, d["eta"], h["net"][k], color=E.ACCENT, width=2, dashed=True)
        side = VGroup(
            label(r"net output: \\ $(1-u)\,p + u\,b - c\,v$", font_size=21, color=MATCH),
            label(rf"best at $\beta = {h['best']:.2f}$", font_size=24, color=E.ACCENT),
            label(rf"the matching elasticity \\ $\eta = {d['eta']:g}$", font_size=21, color=TIGHT),
            label(r"Hosios, \ 1990: \\ efficient if and only if $\beta = \eta$", font_size=22, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Hosios, RES 57(2) (1990): \ 279--298", corner=DR, font_size=12)
        with self.voiceover(
            "Score the Island's market by what it produces, net of what it spends on searching: output from "
            "everyone employed, plus what the unemployed produce at home, which the benefit stands for, minus the "
            "cost of all the open vacancies. <bookmark mark='a'/> Now vary the worker's bargaining share, and "
            "solve the model again for each. <bookmark mark='b'/> Net output is highest when the share is "
            f"{h['best']:.2f}. <bookmark mark='c'/> That is exactly the elasticity of matches with respect to "
            "unemployment, eta, in the Island's matching function. <bookmark mark='d'/> Arthur Hosios proved in "
            "1990 that this is no coincidence: with constant returns in matching, the decentralized market is "
            "efficient exactly when workers' share of the surplus equals their share in producing matches. "
            "Nothing guarantees that bargaining delivers it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), Create(line_), run_time=2)
            vo.wait_until("a")
            self.play(Indicate(line_, color=WHITE))
            vo.wait_until("b")
            self.play(GrowFromCenter(peak), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(drop), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def thick(self):
        dm = load("diamond")
        rows = VGroup(
            label(r"Hosios needs constant returns in matching", font_size=24, color=GREY_A),
            label(r"Diamond's island has increasing returns: \ the more who search, \ the easier each finds a partner",
                  font_size=22, color=JOB),
            label(rf"so it has several equilibria \ (0, \ {dm['equilibria'][1]:.2f}, \ {dm['equilibria'][2]:.2f}), \ "
                  r"and the low one is a coordination failure", font_size=22, color=SEP),
            label(r"a slump that nobody chose, \ which everyone's pessimism sustains", font_size=24, color=E.ACCENT),
            label(r"the estimates of chapter 5 find roughly constant returns, \ so most economists think of this as "
                  r"a possibility, \ not the normal case", font_size=20, color=HOLD),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Diamond, JPE 90(5) (1982); \ Cooper and John, QJE 103(3) (1988)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Hosios's result needs constant returns in matching. <bookmark mark='a'/> Diamond's island does not "
            "have them. There, the more people climb, the easier each one finds a trading partner: a thick-market "
            "externality, with increasing returns. <bookmark mark='b'/> That is why it has several equilibria, "
            "and why the one where nobody climbs is a coordination failure. <bookmark mark='c'/> A slump that "
            "nobody chose, and that everyone's pessimism sustains: Russell Cooper and Andrew John showed in 1988 "
            "how many macroeconomic models share this structure. <bookmark mark='d'/> The estimates in chapter five "
            "find roughly constant returns in real labour markets, so most economists treat Diamond's slump as a "
            "possibility to keep in mind, not as the ordinary state of things."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
