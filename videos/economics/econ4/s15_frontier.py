from __future__ import annotations

from videos.economics.econ4.common import *  # noqa: F403

TREATED = "#7BD88F"
UNTREATED = "#9AA5B8"


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 13, r"Frontier: \ when treatments spill over", r"What does a trial miss when the treated and the "
             r"untreated share a market?", "Chapter thirteen. Frontier: when treatments spill over.",
             lit=("households", "firms"), scale=("person", "city", "nation"), horizon=("a year",))
        self.villages()
        self.evidence()
        self.open()

    def villages(self):
        v = load("villages")
        ax = axes([0, 1], [1.88, 2.14], x_length=6.0, y_length=4.4, xticks=[0, 0.25, 0.5, 0.75, 1],
                  yticks=[1.9, 2.0, 2.1], xfmt=lambda x: f"{100 * x:.0f}\\%",
                  xlabel=r"share of the village offered a place", ylabel=r"mean log earnings", font_size=19,
                  center=LEFT * 2.9 + DOWN * 0.3)
        a = ax.ax
        sats = v["saturations"]
        tr = [(q, v["means"][f"{q:g}"]["treated"]) for q in sats if v["means"][f"{q:g}"]["treated"] is not None]
        un = [(q, v["means"][f"{q:g}"]["untreated"]) for q in sats if v["means"][f"{q:g}"]["untreated"] is not None]
        td = VGroup(*[Dot(a.c2p(q, m), radius=0.09, color=TREATED) for q, m in tr])
        ud = VGroup(*[Dot(a.c2p(q, m), radius=0.09, color=UNTREATED) for q, m in un])
        base = un[0][1]
        tline = DashedLine(a.c2p(0, base + v["direct"]), a.c2p(1, base + v["direct"] + v["spill"]), color=TREATED,
                           stroke_width=2.5, stroke_opacity=0.8)
        uline = DashedLine(a.c2p(0, base), a.c2p(1, base + v["spill"]), color=UNTREATED, stroke_width=2.5,
                           stroke_opacity=0.8)
        key = VGroup(Dot(radius=0.08, color=TREATED), label(r"offered a place", font_size=19, color=TREATED),
                     Dot(radius=0.08, color=UNTREATED), label(r"not offered", font_size=19, color=UNTREATED)
                     ).arrange(RIGHT, buff=0.12).next_to(ax, UP, buff=0.05).shift(RIGHT * 1.2)
        key[2].shift(RIGHT * 0.25)
        key[3].shift(RIGHT * 0.25)
        gap = Arrow(a.c2p(0.5, v["means"]["0.5"]["untreated"]), a.c2p(0.5, v["means"]["0.5"]["treated"]), buff=0.08,
                    color=E.ACCENT, stroke_width=4, max_tip_length_to_length_ratio=0.25)
        total = DoubleArrow(a.c2p(1.0, v["means"]["0"]["untreated"]), a.c2p(1.0, v["means"]["1"]["treated"]),
                            buff=0.05, color=E.MISS, stroke_width=3, tip_length=0.15)
        ref = DashedLine(a.c2p(0, v["means"]["0"]["untreated"]), a.c2p(1, v["means"]["0"]["untreated"]),
                         color=GREY_C, stroke_width=1.5)
        rows = VGroup(
            label(rf"{v['villages']} villages; \ the share offered a place \\ drawn from 0, 25, 50, 75 or 100\%",
                  font_size=23, color=GREY_A),
            label(rf"within villages: \ ${v['within']:+.3f}$ \ (s.e.\ {v['within_se']:.3f}); \\ planted direct "
                  rf"effect ${v['direct']:+.2f}$", font_size=23, color=E.ACCENT),
            label(rf"the not-offered lose as the share rises: \\ slope ${v['spill_hat']:+.3f}$, \ planted "
                  rf"${v['spill']:+.2f}$", font_size=23, color=UNTREATED),
            label(rf"everyone against no one: \ ${v['total']:+.3f}$; \\ planted ${v['truth_total']:+.2f}$",
                  font_size=23, color=E.MISS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(UP * 0.2)
        tag = island_tag(rf"simulated: the Island, {v['villages']} villages of {v['per_village']}; a place takes "
                         r"some work from the neighbours", corner=DR, font_size=13)
        with self.voiceover(
            "Every design in this part rests on an assumption so natural that it's easy to miss: one person's "
            "treatment doesn't change anyone else's outcome. In a market it often fails. Take the Island's "
            "apprenticeship again, and suppose every apprentice takes a little of the boatwrights' work from the "
            f"other young islanders in the same village. <bookmark mark='a'/> Run the trial in {v['villages']} "
            "villages, and let a lottery decide not just who gets a place, but what share of each village does: "
            "none, a quarter, a half, three quarters or all. <bookmark mark='b'/> Inside each village, those "
            "offered a place earn about ten percent more than their neighbours. That's what an ordinary trial "
            "would report. <bookmark mark='c'/> But look across villages. The more of a village is offered a "
            "place, the less everyone in it earns, including those who weren't. <bookmark mark='d'/> So the effect "
            "of the policy, a place for everyone against a place for no one, is a small fraction of what the "
            "trial said. The gain was partly taken from the neighbours."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in td], lag_ratio=0.15),
                      LaggedStart(*[FadeIn(d, scale=0.5) for d in ud], lag_ratio=0.15), run_time=1.6)
            self.play(GrowArrow(gap), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(tline), Create(uline), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(ref), GrowFromCenter(total), FadeIn(rows[3]))
        self.clear_scene()

    def evidence(self):
        cards = VGroup(
            history_card(r"2013", r"Cr\'epon, Duflo, Gurgand, Rathelot and Zamora: \ job counselling in France",
                         r"235 labour markets, each with 0 to 100\% of young job seekers offered help; the gains "
                         r"were partly at the expense of those not offered, and little was left overall",
                         color="#F28C6F", width=4.15, font_size=20),
            history_card(r"2022", r"Egger, Haushofer, Miguel, Niehaus and Walker: \ cash in rural Kenya",
                         r"about \$1{,}000 each to over 10{,}500 households in 653 villages; each dollar raised "
                         r"local spending and income by about 2.5, with little inflation", color=TREATED,
                         width=4.15, font_size=20),
            history_card(r"2023", r"Muralidharan, Niehaus and Sukhtankar: \ a better-run job guarantee in India",
                         r"earnings rose about 14\%, mostly not from the programme but from higher private wages: "
                         r"the spillover was the larger part", color="#C9A0FF", width=4.15, font_size=20),
        ).arrange(RIGHT, buff=0.25, aligned_edge=UP).move_to(UP * 0.35)
        head = label(r"Trials that randomize the share treated", font_size=32).to_edge(UP, buff=0.45)
        foot = label(r"the spillover can shrink the effect, \ multiply it, \ or be most of it", font_size=26,
                     color=E.ACCENT).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"QJE 128(2) (2013); Econometrica 90(6) (2022); Econometrica 91(4) (2023)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "The best evidence now comes from trials that randomize the share treated, as we just did. "
            "<bookmark mark='a'/> In France, Bruno Crépon, Esther Duflo and their coauthors offered job counselling "
            "to young job seekers, with the share offered drawn at random across two hundred and thirty-five labour "
            "markets. Those offered help found stable jobs sooner, but partly at the expense of those who weren't, "
            "and the net gain was small. <bookmark mark='b'/> In Kenya, Dennis Egger and his coauthors followed "
            "cash transfers of about a thousand dollars to more than ten thousand households in 653 villages. Each "
            "dollar raised local spending and income by about two and a half, with little inflation. "
            "<bookmark mark='c'/> In India, Karthik Muralidharan, Paul Niehaus and Sandip Sukhtankar found that a "
            "better-run job guarantee raised the earnings of poor households by about fourteen percent, mostly "
            "through higher wages in private jobs, not through the programme itself. <bookmark mark='d'/> So the "
            "spillover can shrink an effect, multiply it, or be most of it. A trial that can't see it can't tell "
            "you which."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(head))
            for mk, c_ in zip("abc", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c_, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def open(self):
        items = point_cards([
            (r"not known", r"when a trial's effect survives being scaled up \\ to a whole market, \ and how to "
                           r"tell in advance", E.MISS),
            (r"the tools", r"two-stage designs \ (Hudgens and Halloran, 2008); \\ exposure mappings \ (Aronow and "
                           r"Samii, 2017)", E.ACCENT),
            (r"the platforms", r"in two-sided markets, \ buyers and sellers share a market: \\ randomize whole "
                               r"markets, \ or correct the bias", "#7BD88F"),
            (r"$\bigstar$ \ research problem", r"design the Island's next trial: \ how many villages, \\ at what "
                                               r"shares, \ to see a spillover of $-0.04$?", E.TRUTH),
        ], width=12.6, cols=2, font_size=21).move_to(UP * 0.2)
        head = label(r"What is not known", font_size=34).to_edge(UP, buff=0.4)
        tag = published_tag(r"Hudgens and Halloran, JASA (2008); Aronow and Samii, Ann.\ Appl.\ Stat.\ (2017); "
                            r"\emph{Statistics, Built} Parts 35, 62, 64", corner=DR, font_size=12)
        with self.voiceover(
            "What is not known? <bookmark mark='a'/> Above all, when the effect a trial finds will survive being "
            "scaled to a whole market, and how to tell before spending the money. <bookmark mark='b'/> The "
            "statistics are being built: designs that randomize at two levels, as in Michael Hudgens and Elizabeth "
            "Halloran's work, and Peter Aronow and Cyrus Samii's exposure mappings, which say exactly which "
            "neighbours' treatments can reach you. <bookmark mark='c'/> The same problem now costs online "
            "platforms money every day: when buyers and sellers share a market, a test on some of them changes the "
            "market for the rest. <bookmark mark='d'/> And here is the research problem for this part. Design the "
            "Island's next trial: how many villages, at what shares, to detect a spillover half the size of this "
            "one? The problem set has the place to start."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c_ in zip("abcd", items.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c_, shift=UP * 0.1))
        self.clear_scene()
