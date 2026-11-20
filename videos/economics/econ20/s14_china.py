from __future__ import annotations

from videos.economics.econ20.common import *  # noqa: F403


class China(VoiceoverScene):
    def construct(self):
        card(self, 12, r"China's growth in the model", r"Can the Solow model account for four decades of Chinese "
             r"growth, \ and what does it say about the next?", "Chapter twelve. China's growth in the model.",
             lit={1978: r"reform begins", 2011: r"Growing Like China"}, scale=("nation",), horizon=("decades",))
        self.series()
        self.accounting()
        self.ssz()
        self.ahead()

    def series(self):
        c = load("china")
        a1 = plane([1958, 2025], [0, 0.55], center=UP * 1.45 + LEFT * 3.4, x_length=5.8, y_length=2.4,
                   xticks=[1960, 1980, 2000, 2020], yticks=[0, 0.2, 0.4], ylabel=r"investment, \ share of GDP",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        a2 = plane([1958, 2025], [0, 6], center=UP * 1.45 + RIGHT * 3.3, x_length=5.8, y_length=2.4,
                   xticks=[1960, 1980, 2000, 2020], yticks=[0, 2, 4, 6], ylabel=r"capital $\div$ output",
                   xfmt=lambda v: f"{v:.0f}", font_size=14)
        a3 = plane([1958, 2025], [0, 0.2], center=DOWN * 1.9 + LEFT * 3.4, x_length=5.8, y_length=2.4,
                   xticks=[1960, 1980, 2000, 2020], yticks=[0, 0.05, 0.1, 0.15, 0.2],
                   ylabel=r"return on capital \ (PWT)", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        l1 = path(a1, c["years"], c["inv"], color=SAVE, width=3, smooth=False)
        l2 = path(a2, c["years"], c["ky"], color=CAPITAL, width=3, smooth=False)
        l3 = path(a3, c["irr_years"], c["irr"], color=RATE, width=3, smooth=False)
        rows = VGroup(
            label(rf"investment: \ {pc(c['inv_1978'], 0)} in 1978, \ {pc(c['inv_peak'], 0)} at its peak \ "
                  rf"({c['inv_peak_year']})", font_size=19, color=SAVE),
            label(rf"capital: \ {c['ky_1978']:.1f} years of output $\to$ {c['ky_last']:.1f} \ ({c['last']})",
                  font_size=19, color=CAPITAL),
            label(r"the return rose in the 1980s and early 1990s, \ then fell", font_size=19, color=RATE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.3 + DOWN * 1.9)
        src = data_tag(r"Penn World Table 11.0 \ (csh\_i, rnna, rgdpna, irr)", corner=DR, font_size=11)
        with self.voiceover(
            "No economy has tested the model harder than China's since its reforms began in 1978. "
            f"<bookmark mark='a'/> It invested about {100 * c['inv_1978']:.0f} percent of its output in 1978, and "
            f"at the peak, in {c['inv_peak_year']}, about {100 * c['inv_peak']:.0f} percent, measured at "
            "international prices. <bookmark mark='b'/> So its capital grew faster than its output: from about "
            f"{c['ky_1978']:.1f} years of output to {c['ky_last']:.1f}. <bookmark mark='c'/> Diminishing returns "
            "say that so much accumulation should drive the return on capital down. For fifteen years it did the "
            "opposite: the return rose, through the 1980s and into the 1990s. Only later did it fall."
        ) as vo:
            self.play(FadeIn(a1), FadeIn(a2), FadeIn(a3), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(l1), FadeIn(rows[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(l2), FadeIn(rows[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(l3), FadeIn(rows[2]), run_time=2)
        self.clear_scene()

    def accounting(self):
        c = load("china")
        per = c["periods"]
        rows = VGroup()
        head = VGroup(*[label(t, font_size=21, color=col) for t, col in (
            (r"China", COUNTRY["CHN"][1]), (r"output per hour", OUTPUT), (r"capital deepening", CAPITAL),
            (r"schooling", HUMAN), (r"residual", TFP))])
        xs = [-4.6, -1.8, 0.8, 3.0, 5.0]
        for m, x in zip(head, xs):
            m.move_to([x, 1.9, 0])
        for i, (k, v) in enumerate(per.items()):
            y = 1.0 - i * 0.75
            rows.add(VGroup(label(k.replace("-", "--"), font_size=23, color=GREY_A).move_to([xs[0], y, 0]),
                            *[label(pc(v[key]), font_size=23, color=col).move_to([x, y, 0])
                              for key, col, x in (("per_hour", OUTPUT, xs[1]), ("deepening", CAPITAL, xs[2]),
                                                  ("human_capital", HUMAN, xs[3]), ("tfp", TFP, xs[4]))]))
        note_ = label(r"after 2008: \ more of the growth from capital, \ less from the residual", font_size=23,
                      color=HOLD).to_edge(DOWN, buff=0.8)
        src = data_tag(r"Penn World Table 11.0", corner=DR, font_size=11)
        p1, p3 = per["1980-1995"], per["2008-2019"]
        with self.voiceover(
            "Take China's growth apart, period by period. <bookmark mark='a'/> From 1980 to 1995, output per hour "
            f"grew {100 * p1['per_hour']:.1f} percent a year, and more than half of it was the residual, "
            f"{100 * p1['tfp']:.1f} percent: farms freed from collectives, workers moving from fields to factories, "
            "firms allowed to compete. <bookmark mark='b'/> From 1995 to 2008, output per hour grew faster still, and "
            "capital deepening took a larger share. "
            "<bookmark mark='c'/> After 2008, output per hour still grew fast, but capital deepening now did most of "
            f"the work, and the residual fell to {100 * p3['tfp']:.1f} percent. That is what growth that runs into "
            "diminishing returns looks like."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            self.play(FadeIn(note_))
        self.clear_scene()

    def ssz(self):
        sc = study_card(r"Growing Like China", r"Zheng Song, \ Kjetil Storesletten \ and Fabrizio Zilibotti, \ 2011",
                        [(r"the firms", r"state firms with poor productivity but easy credit; \ private firms, \ more "
                                        r"productive, \ that must finance themselves"),
                         (r"the mechanism", r"workers move from state to private firms, \ so measured productivity "
                                            r"rises and the return to capital stays high"),
                         (r"the saving", r"private entrepreneurs save to grow; \ the banks' deposits, \ with no "
                                         r"private borrowers, \ flow abroad"),
                         (r"explains", r"high growth, \ a high return and a growing trade surplus, \ all at once")],
                        design="structural", width=12.2, font_size=22).move_to(UP * 0.1)
        tag = published_tag(r"Song, Storesletten and Zilibotti, AER 101(1) (2011): \ 196--233", corner=DR,
                            font_size=12)
        with self.voiceover(
            "How can capital pile up without its return falling? <bookmark mark='a'/> Zheng Song, Kjetil "
            "Storesletten and Fabrizio Zilibotti built a model of China with two kinds of firm. State firms have "
            "poor productivity but easy access to the banks. Private firms are more productive, but must finance "
            "themselves. <bookmark mark='b'/> As workers move from state firms to private ones, measured productivity "
            "rises, and capital keeps earning a high return even as it accumulates. "
            "<bookmark mark='c'/> Private entrepreneurs save hard to grow, and the deposits the banks collect, with "
            "few private borrowers to lend to, flow abroad. <bookmark mark='d'/> One mechanism, reallocation, "
            "accounts for high growth, a high return and a growing trade surplus at the same time. It is the residual "
            "of chapter seven, given a cause."
        ) as vo:
            rest = [m for m in sc if m is not sc[1]]
            self.play(*[FadeIn(m) for m in rest], FadeIn(sc.head), FadeIn(tag))
            for mk, r in zip("abcd", sc.body):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.clear_scene()

    def ahead(self):
        rows = VGroup(
            label(r"what the model says about the next decades", font_size=28, color=E.ACCENT),
            label(r"reallocation ends when the state firms have shed their workers", font_size=23, color=GREY_A),
            label(r"investment near half of output is far above the golden rule's third", font_size=23, color=SAVE),
            label(r"so growth must come from the residual, \ or slow", font_size=23, color=TFP),
            label(r"the misallocation dial \ (Parts 9 and 21) \ measures how much is left to gain", font_size=22,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        with self.voiceover(
            "What does the model say about China's future? <bookmark mark='a'/> Reallocation runs out once the "
            "state firms have shed their workers. <bookmark mark='b'/> An investment rate near half of output is far "
            "above the golden rule's third: more capital now adds little to consumption. <bookmark mark='c'/> So "
            "growth must come from the residual, or it will slow, as Korea's did and the Soviet Union's did. "
            "<bookmark mark='d'/> How much productivity is still to be gained by moving capital and workers to "
            "better uses is a dial this series opened in part nine, and returns to in part twenty-one."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
