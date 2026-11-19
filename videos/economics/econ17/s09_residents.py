from __future__ import annotations

from videos.economics.econ17.common import *  # noqa: F403


class Residents(VoiceoverScene):
    def construct(self):
        card(self, 7, r"The residents' match", r"Why did the doctors' clearinghouse survive, \ when so many others "
             r"failed?", "Chapter seven. The residents' match.",
             lit={1952: r"the clearinghouse", 1984: r"Roth", 1991: r"the British test", 1998: r"the redesign"},
             scale=("market", "nation"), horizon=("a decade",))
        self.britain()
        self.called()
        self.couples()

    def britain(self):
        r = load("roth")
        rows = [c for c in r["clearinghouses"] if c[0] not in ("osteopaths before 1994", "osteopaths from 1994",
                                                                 "pharmacists")]
        head = label(r"Britain's natural experiment: \ a different clearinghouse in each region", font_size=26,
                     color=E.ACCENT).to_edge(UP, buff=0.35)
        hdr = VGroup(label(r"market", font_size=20, color=GREY_B).move_to([-3.4, 2.5, 0]),
                     label(r"stable?", font_size=20, color=GREY_B).move_to([0.6, 2.5, 0]),
                     label(r"still in use?", font_size=20, color=GREY_B).move_to([3.2, 2.5, 0]))
        grid = VGroup()
        for i, (name, stable, used) in enumerate(rows):
            y = 1.9 - 0.52 * i
            grid.add(VGroup(label(name, font_size=21, color=WHITE if i else STABLE).move_to([-3.4, y, 0]),
                            label("yes" if stable else "no", font_size=22,
                                  color=STABLE if stable else REJECT).move_to([0.6, y, 0]),
                            label("yes" if used else "no", font_size=22,
                                  color=STABLE if used else REJECT).move_to([3.2, y, 0])))
        foot = label(r"the two unstable survivors each matched one medical school to one hospital", font_size=21,
                     color=GREY_A).to_edge(DOWN, buff=0.8)
        tag = published_tag(r"Roth, AER 81(3) (1991); \ Roth, Nobel lecture (2012)", corner=DR, font_size=13)
        with self.voiceover(
            "In 1984 Roth showed that the doctors' clearinghouse produced stable matches, and argued that this was "
            "why it had survived: a match that a doctor and a hospital could both profitably walk away from would "
            "not last. <bookmark mark='a'/> Britain offered a test. In the 1960s its market for new doctors "
            "unravelled as the American one had, and a Royal Commission said, in effect, do what the Americans do. "
            "But nobody had published how the American clearinghouse worked, so each region of the health service "
            "built its own. <bookmark mark='b'/> Edinburgh's of 1969 and Cardiff's produced stable matches, and both "
            "were still in use. <bookmark mark='c'/> Birmingham's, Edinburgh's of 1967, Newcastle's and Sheffield's "
            "did not, and all four were abandoned. <bookmark mark='d'/> Two unstable ones survived, at Cambridge and "
            "at the London Hospital, but each matched the students of one medical school to the jobs of one "
            "hospital, where it was hard to act on an instability."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr), FadeIn(grid[0]), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(grid[1]), FadeIn(grid[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(g) for g in grid[3:7]], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(grid[7]), FadeIn(grid[8]), FadeIn(foot))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["roth_stability"]
        cc = call_card(r"Alvin Roth, \ on the doctors' match", c.when,
                       r"a clearinghouse survives if its matches are stable; \ one whose matches can be blocked will be "
                       r"abandoned",
                       r"Britain: \ both stable clearinghouses still in use; \ four of six unstable ones abandoned; \ the "
                       r"two survivors each served a single school and hospital", c.verdict, width=12.4,
                       font_size=23).move_to(UP * 0.5)
        q = label(r"in the laboratory too, \ stable clearinghouses kept a market from unravelling, \ and unstable "
                  r"ones did not \ (Kagel and Roth, \ 2000)", font_size=21, color=E.ACCENT).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Roth, JPE 92(6) (1984); \ AER 81(3) (1991); \ Kagel and Roth, QJE 115(1) (2000)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In 1984 Roth said that a clearinghouse survives if its matches are "
            "stable, and that one whose matches can be blocked will be abandoned. <bookmark mark='b'/> In Britain, "
            "both stable clearinghouses were still in use, four of the six unstable ones had been abandoned, and "
            "the two survivors were the special cases of one school and one hospital. <bookmark mark='c'/> Right. "
            "And when John Kagel and Roth ran the same comparison in the laboratory in 2000, the stable "
            "clearinghouse stopped the market unravelling, and the unstable one did not."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3), FadeIn(q))
        self.clear_scene()

    def couples(self):
        r = load("roth")
        w = r["women_students"]
        rows = VGroup(
            label(rf"1950s: \ almost no women in American medical schools; \ 1970s: \ about "
                  rf"{w['1970s'] * 100:.0f}\%; \ now about half", font_size=23),
            label(r"married couples got jobs far apart, \ and began to arrange jobs outside the match", font_size=23,
                  color=REJECT),
            label(r"a couple wants a pair of jobs: \ with couples, \ a stable matching may not even exist",
                  font_size=23, color=HELD),
            label(r"1995: \ Roth and Elliott Peranson are asked to redesign the match", font_size=23, color=PROPOSE),
            label(r"1998: \ applicants ask, \ couples rank pairs of jobs, \ and the algorithm searches for stability",
                  font_size=23, color=STABLE),
            label(rf"about {r['nrmp_positions']:,} positions a year by 2012; \ the design now runs dozens of medical "
                  r"markets".replace(",", "{,}", 1), font_size=23, color=E.ACCENT),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Roth and Peranson, AER 89(4) (1999); \ Roth, Nobel lecture (2012)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "The American match met its own crisis. <bookmark mark='a'/> In the 1950s there were almost no women "
            "in American medical schools; by the 1970s about a tenth of students were women, and today about half. "
            "<bookmark mark='b'/> Married couples, treated by the clearinghouse as two strangers, were given jobs "
            "far apart, and began to arrange jobs outside the match. <bookmark mark='c'/> A couple wants a pair of "
            "jobs, and with couples in the market a stable matching may not even exist. "
            "<bookmark mark='d'/> In 1995 Roth was asked, with Elliott Peranson, to redesign the match. "
            "<bookmark mark='e'/> From 1998 applicants did the asking, couples ranked pairs of jobs, and the "
            "algorithm searched for a stable outcome. "
            "<bookmark mark='f'/> By 2012 the match placed about twenty-five thousand doctors a year, and the same "
            "design runs dozens of other medical markets."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, rr in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(rr, shift=UP * 0.1))
        self.clear_scene()
