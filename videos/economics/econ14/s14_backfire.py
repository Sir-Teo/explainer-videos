from __future__ import annotations

from videos.economics.econ14.common import *  # noqa: F403

FINE = "#F2788F"
CTRL = "#9FB8F2"


class Backfire(VoiceoverScene):
    def construct(self):
        card(self, 12, r"When incentives backfire", r"Can paying for something get you less of it?",
             "Chapter twelve. When incentives backfire.",
             lit={1997: r"Frey and Oberholzer-Gee", 2000: r"Gneezy and Rustichini", 2003: r"Bénabou and Tirole"},
             scale=("person", "community"), horizon=("a season",))
        self.daycare()
        self.cases()
        self.why()

    def daycare(self):
        d = load("daycare")
        wk = np.array(d["weeks"])
        ax = plane([0.5, 20.5], [0, 22], center=LEFT * 2.6 + DOWN * 0.3, x_length=6.8, y_length=4.4,
                   xticks=[1, 5, 10, 16, 20], yticks=[0, 5, 10, 15, 20], xlabel=r"week",
                   ylabel=r"late pick-ups per centre", font_size=16, xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        shade = Rectangle(width=a.c2p(16.5, 0)[0] - a.c2p(4.5, 0)[0], height=a.c2p(0, 22)[1] - a.c2p(0, 0)[1],
                          stroke_width=0, fill_color=FINE, fill_opacity=0.08).move_to(
            (a.c2p(4.5, 0) + a.c2p(16.5, 22)) / 2)
        sl = label(r"the fine", font_size=15, color=FINE).move_to(a.c2p(10.5, 21))
        ct = path(ax, wk, d["control"], color=CTRL, width=3, smooth=False)
        tt = path(ax, wk, d["test"], color=FINE, width=3.5, smooth=False)
        lt = label(r"6 fined centres", font_size=15, color=FINE).move_to(a.c2p(3.0, 5.0))
        lc = label(r"4 others", font_size=15, color=CTRL).move_to(a.c2p(18.5, 6.3))
        side = VGroup(
            label(rf"before the fine: \ {d['before']:.1f} a week", font_size=21, color=GREY_A),
            label(rf"with it: \ {d['during']:.1f}", font_size=21, color=FINE),
            label(rf"after it was removed: \ {d['after']:.1f}", font_size=21, color=FINE),
            label(r"the guilt was gone, \\ and did not come back", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"Gneezy and Rustichini (2000), Table 1, transcribed", corner=DR, font_size=13)
        with self.voiceover(
            "Part one began with a fine. <bookmark mark='a'/> Ten day-care centres in Haifa, and parents who came late "
            "to collect their children. In six of them, chosen at random, a small fine for lateness was introduced; "
            f"before it, they had about {d['before']:.0f} late pick-ups a week. <bookmark mark='b'/> With the fine, "
            "late pick-ups doubled. <bookmark mark='c'/> And when the fine was taken away, they stayed high, and if "
            "anything rose. <bookmark mark='d'/> Before, a late parent felt they owed the teacher something. The "
            "fine turned that debt into a price, and a cheap one, and once the parents had learnt that lateness was "
            "something one could simply pay for, removing the price did not bring the guilt back."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(ct), FadeIn(lc))
            vo.wait_until("a")
            self.play(Create(path(ax, wk[:4], d["test"][:4], color=FINE, width=3.5, smooth=False)), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(shade), FadeIn(sl), Create(tt), FadeIn(lt), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def cases(self):
        cr = tables.CROWDING.data
        c1 = study_card(r"A nuclear-waste site in Switzerland", r"Bruno Frey and Felix Oberholzer-Gee, \ 1997", [
            (r"asked", r"two communities named as possible sites, 1993: accept the repository?"),
            (r"unpaid", rf"{100 * cr['accept_unpaid']:.1f}\% yes"),
            (r"paid", rf"offered \${cr['offers_usd_per_year'][0]:,} to \${cr['offers_usd_per_year'][2]:,} a year "
                      rf"each: {100 * cr['accept_paid']:.1f}\% yes"),
        ], design="survey", width=6.3, font_size=20)
        c2 = study_card(r"Pay enough or don't pay at all", r"Uri Gneezy and Aldo Rustichini, \ 2000", [
            (r"quiz", r"a token payment per right answer: fewer right than with no pay at all"),
            (r"collecting", r"students collecting for charity: a 1\% commission raised less than none"),
            (r"more pay", r"a larger payment beat the token one"),
        ], design="RCT", width=6.3, font_size=20)
        VGroup(c1, c2).arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to(UP * 0.5)
        foot = label(r"a small payment can do worse than none: \ it changes what the act means", font_size=23,
                     color=E.ACCENT).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Frey and Oberholzer-Gee, AER 87(4) (1997); \ Gneezy and Rustichini, QJE 115(3) (2000)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "Haifa is not alone. <bookmark mark='a'/> In 1993 two Swiss communities were named as possible sites for "
            "a store of radioactive waste. Bruno Frey and Felix Oberholzer-Gee asked residents whether they would "
            "accept it. Just over half said yes. Then they asked whether they would accept it if every resident were "
            "paid, thousands of dollars a year each. Acceptance fell to a quarter. The money made it look like a "
            "bribe for a danger, where before it had been a civic duty. <bookmark mark='b'/> In 2000 Gneezy and "
            "Rustichini paid people a token sum for each right answer in a quiz, and they got fewer right than "
            "people paid nothing. Students collecting for charity raised less with a one percent commission than "
            "with none. A larger payment did better than the token one; their title gave the advice: pay enough or "
            "don't pay at all. <bookmark mark='c'/> A small payment can do worse than none, because it changes what "
            "the act means."
        ) as vo:
            self.play(FadeIn(c1, shift=UP * 0.1), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(c2, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def why(self):
        rows = VGroup(
            label(r"Roland Bénabou and Jean Tirole, \ 2003: \ an incentive is also a message", font_size=25,
                  color=E.ACCENT),
            label(r"a principal who pays for a task \ reveals that the task is unpleasant, \ or that you can't be "
                  r"trusted", font_size=22, color=RISK),
            label(r"and people do good partly to be seen doing good: \ pay muddies the signal", font_size=22,
                  color=SIGNAL),
            label(r"the contract can't list everything: \ what it leaves out is governed by norms", font_size=22,
                  color=TEAM),
            label(r"a price can replace a norm, \ and the norm may not return", font_size=22, color=FINE),
            label(r"so: \ incentives work best where the task is narrow, \ the measure good, \ and the norm weak",
                  font_size=23, color=E.ACCENT),
        ).arrange(DOWN, buff=0.34).move_to(UP * 0.1)
        tag = published_tag(r"Bénabou and Tirole, RES 70(3) (2003); \ AER 96(5) (2006)", corner=DR, font_size=13)
        with self.voiceover(
            "Why does this happen? <bookmark mark='a'/> In 2003 Roland Bénabou and Jean Tirole argued that an "
            "incentive is also a message. <bookmark mark='b'/> A principal who pays for a task reveals something: "
            "that the task is unpleasant, or that the agent can't otherwise be trusted to do it. "
            "<bookmark mark='c'/> And people do good partly to be seen as good, so paying them muddies the signal: "
            "the volunteer who is paid can no longer show that they volunteered. <bookmark mark='d'/> Underneath "
            "both is the fact that no contract can list everything, and what it leaves out is governed by norms. "
            "<bookmark mark='e'/> A price can push a norm out, and the norm may not come back. "
            "<bookmark mark='f'/> So the incentive contracts of this part work best where the task is narrow, the "
            "measure is good, and the norm they would replace is weak."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
