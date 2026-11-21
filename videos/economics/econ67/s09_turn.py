from __future__ import annotations

from videos.economics.econ67.common import *  # noqa: F403


class Turn(VoiceoverScene):
    def construct(self):
        card(self, 7, r"The empirical turn", r"How did economics change from a field of theory to a field of data?",
             "Chapter seven. The empirical turn.", lit={1983: "Leamer", 2010: "Angrist and Pischke",
                                                        2013: "Hamermesh"}, scale=("world",), horizon=("a century",))
        self.methods()
        self.revolution()

    def methods(self):
        H = load("turn")
        years, shares, names = H["years"], H["shares"], H["methods"]
        ax = plane([0, 6], [0, 100], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.6, y_length=4.8, xticks=[],
                   yticks=[0, 25, 50, 75, 100], ylabel=r"share of articles, \ \%", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        cols = VGroup()
        for k, (y, sh) in enumerate(zip(years, shares)):
            tot = sum(sh)
            base = 0.0
            g = VGroup()
            for j, v in enumerate(sh):
                v = 100 * v / tot
                if v > 0:
                    p0, p1 = ax.ax.c2p(k + 0.15, base), ax.ax.c2p(k + 0.85, base + v)
                    g.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=METHOD_COL[j],
                                    fill_opacity=0.85, stroke_width=0.6, stroke_color=BACKGROUND)
                          .move_to((p0 + p1) / 2))
                base += v
            cols.add(g)
        xl = VGroup(*[label(str(y), font_size=15, color=GREY_A).next_to(ax.ax.c2p(k + 0.5, 0), DOWN, buff=0.12)
                      for k, y in enumerate(years)])
        key = legend_rows([(METHOD_COL[j], names[j]) for j in range(5)][::-1], font_size=15).next_to(
            ax.ax, RIGHT, buff=0.5).shift(UP * 0.8)
        side = VGroup(
            label(rf"theory: \ {shares[2][0]:.0f}\% in 1983, \ {shares[5][0]:.0f}\% in 2011", font_size=18,
                  color=METHOD_COL[0]),
            label(rf"own data: \ {shares[2][3]:.1f}\% to {shares[5][3]:.0f}\%", font_size=18, color=METHOD_COL[3]),
            label(rf"experiments: \ 0 to {shares[5][4]:.1f}\%", font_size=18, color=METHOD_COL[4]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(key, DOWN, buff=0.5).align_to(key, LEFT)
        tag = published_tag(r"Hamermesh, \ \emph{JEL} 51(1) (2013), \ Table 4: \ full-length articles in the AER, \ "
                            r"JPE and QJE", corner=DL, font_size=12)
        with self.voiceover(
            "Step back from single results to the field. <bookmark mark='a'/> Daniel Hamermesh classified every "
            "full-length article in the three leading American general journals in one year of each decade from "
            "1963 to 2011. <bookmark mark='b'/> In 1963 half were pure theory and most of the rest used data "
            "borrowed from someone else, typically a government. <bookmark mark='c'/> Theory peaked at "
            f"{shares[2][0]:.0f} percent in 1983. By 2011 it was down to {shares[5][0]:.0f} percent. <bookmark "
            "mark='d'/> What replaced it: studies whose authors built their own data, up from two percent to a "
            f"third, and experiments, from nothing to {shares[5][4]:.0f} percent. The field had turned from "
            "proving what must happen to measuring what does."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(xl), FadeIn(key), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cols[0]), FadeIn(cols[1]))
            vo.wait_until("b")
            self.play(Indicate(cols[0], scale_factor=1.03))
            vo.wait_until("c")
            self.play(FadeIn(cols[2]), FadeIn(cols[3]), FadeIn(cols[4]), FadeIn(cols[5]), FadeIn(side[0]))
            vo.wait_until("d")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.clear_scene()

    def revolution(self):
        cards = point_cards([
            (r"the complaint", r"Leamer, \ 1983: \ results hung on assumptions nobody believed and specifications "
             r"nobody reported", FAIL),
            (r"the credibility revolution", r"Angrist and Pischke, \ 2010: \ better designs, \ experiments and "
             r"natural experiments, \ took the con out", TRUE),
            (r"the data", r"administrative records, \ taxes, \ schools, \ hospitals, \ firms: \ millions of people, "
             r"\ not thousands", FIRST),
            (r"who can get them", r"access is negotiated, \ often by insiders; \ results that cannot be checked by "
             r"others are harder to replicate", PUB),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"the credibility revolution", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Leamer, \ \emph{AER} 73(1) (1983); \ Angrist and Pischke, \ \emph{JEP} 24(2) (2010)",
                            corner=DL, font_size=12)
        with self.voiceover(
            "Why the turn? <bookmark mark='a'/> Partly a complaint. Leamer's 1983 paper argued that econometric "
            "results hung on assumptions nobody believed and specifications nobody reported. <bookmark mark='b'/> "
            "In 2010 Joshua Angrist and Jörn-Steffen Pischke answered that better research design had taken the "
            "con out: randomized trials, and natural experiments like the draft lotteries and minimum-wage borders "
            "of Parts four and thirty-eight. <bookmark mark='c'/> Partly the data. Administrative records of taxes, "
            "schools, hospitals and firms now cover millions of people rather than the thousands in a survey. "
            "<bookmark mark='d'/> That brings a new problem: access to such records is negotiated, often by "
            "insiders, and a result that outsiders cannot check is harder to replicate. Chapter three's first rung "
            "is hardest to climb where the data are most valuable."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
