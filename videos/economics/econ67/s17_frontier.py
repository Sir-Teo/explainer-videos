from __future__ import annotations

from videos.economics.econ67.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ a cumulative record", r"What would it take for economics to know what it "
             r"knows?", "Chapter fifteen. Frontier: a cumulative record.", scale=("world",), horizon=("a decade",))
        self.record()
        self.dials_per_part()

    def record(self):
        cards = point_cards([
            (r"living meta-analyses", r"each new estimate added as it is published, \ with its design and its "
             r"standard error, \ corrected for selection", TRUE),
            (r"replication as routine", r"institutes and journals that reproduce papers at scale, \ and publish "
             r"what fails", FIRST),
            (r"machine-readable results", r"estimates stored as data, \ not only as prose: \ ready to be "
             r"pooled, \ checked and reused", PUB),
            (r"forecasts on file", r"predictions written down before results, \ scored after them", STATE),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"a cumulative record", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "The frontier is less a new method than a new habit: keeping the record. <bookmark mark='a'/> Living "
            "meta-analyses add each estimate as it is published, with its design and its standard error, and "
            "correct the whole for selection. <bookmark mark='b'/> Replication becomes routine, done at scale by "
            "institutes and journals, with the failures published too. <bookmark mark='c'/> Results are stored as "
            "data, not only as prose, so they can be pooled and checked by machines as well as people. <bookmark "
            "mark='d'/> And forecasts are filed before results arrive, and scored after."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def dials_per_part(self):
        A = load("audit")
        pp = {int(k): v for k, v in A["per_part"].items()}
        ax = plane([0, 69], [0, 7], center=DOWN * 0.3 + LEFT * 0.6, x_length=11.0, y_length=4.2,
                   xticks=[1, 10, 20, 30, 40, 50, 60, 67], yticks=[0, 2, 4, 6], xlabel=r"part",
                   ylabel=r"Dials the part entered or reopened", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        b = bars(ax, list(pp), list(pp.values()), [TRUE if p == 67 else FIRST for p in pp], width=0.7)
        head = label(rf"the series' own record: \ {A['n_dials']} Dials, \ {A['n_estimates']} estimates, \ each "
                     r"with its source, \ design and date checked", font_size=21, color=E.ACCENT).to_edge(UP,
                                                                                                         buff=0.45)
        foot = label(r"a public good: \ anyone can add a row, \ and every row can be checked", font_size=21,
                     color=PUB).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"explainer/economics/dials.py", corner=DR, font_size=12)
        with self.voiceover(
            "This series has kept a small version of that record. <bookmark mark='a'/> Every part entered or "
            "reopened its Dials, each estimate stored as data with its source, its design and the date it was "
            "checked. <bookmark mark='b'/> "
            f"{A['n_dials']} Dials and {A['n_estimates']} estimates across sixty-seven parts. <bookmark mark='c'/> "
            "It is a public good in the sense of Part fifteen: once kept, anyone can use it, add a row, or check "
            "one. The next economics will be built less by any single study than by records like this, kept by "
            "many hands."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(bb, DOWN) for bb in b], lag_ratio=0.03), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(head))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
