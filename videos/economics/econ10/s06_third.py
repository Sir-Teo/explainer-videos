from __future__ import annotations

from videos.economics.econ10.common import *  # noqa: F403


class ThirdDegree(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Third-degree discrimination: \ students and townsfolk", r"When does charging groups different "
             r"prices help or hurt?", "Chapter five. Third-degree discrimination: students and townsfolk.",
             lit={1985: r"Varian's output test"})
        self.groups()
        self.welfare()

    def groups(self):
        t = load("third")
        ps = np.array(t["ps"])
        ax = plane([0, 110], [0, 20], center=LEFT * 2.9 + DOWN * 0.3, x_length=6.4, y_length=5.0,
                   xticks=[0, 25, 50, 75, 100], yticks=[0, 5, 10, 15, 20], xlabel=r"crossings a day",
                   ylabel=r"fare, \ \$", font_size=17)
        a = ax.ax
        qs_, qt_ = np.array(t["q_students"]), np.array(t["q_town"])
        ks, kt = qs_ > 0, qt_ > 0                # draw each demand only where someone buys
        ds = path(ax, qs_[ks], ps[ks], color=STUD, width=3.5, smooth=False, xr=(0, 110))
        dt = path(ax, qt_[kt], ps[kt], color=TOWN, width=3.5, smooth=False, xr=(0, 110))
        u = t["uniform"]
        d = t["discriminate"]
        pu = DashedLine(a.c2p(0, u["p"]), a.c2p(110, u["p"]), color=GREY_B, stroke_width=2)
        ps_l = DashedLine(a.c2p(0, d["p"][0]), a.c2p(110, d["p"][0]), color=STUD, stroke_width=2)
        lab_s = label(r"students", font_size=19, color=STUD).next_to(a.c2p(12, 4.8), UR, buff=0.08)
        lab_t = label(r"townsfolk", font_size=19, color=TOWN).next_to(a.c2p(70, 6.5), RIGHT, buff=0.1)
        side = VGroup(
            label(r"students: \ $Q = 60 - 10p$, \ none pay more than \$6", font_size=22, color=STUD),
            label(r"townsfolk: \ $Q = 100 - 5p$", font_size=22, color=TOWN),
            label(rf"one fare for all: \ \${u['p']:.2f}, \ and no student crosses", font_size=22, color=GREY_A),
            label(rf"a student fare of \${d['p'][0]:.2f} \ (shown a card), \\ and \${d['p'][1]:.2f} for the town",
                  font_size=22, color=STUD),
            label(r"the lower price goes to the more elastic group: \\ the inverse-elasticity rule, \ market by "
                  r"market", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Most real discrimination sorts buyers into groups the seller can see. <bookmark mark='a'/> Suppose the "
            "Island has students, who can't pay much for the ferry, none of them more than six dollars, "
            "<bookmark mark='b'/> and townsfolk, who will pay a lot more. A crossing costs Bo a dollar. "
            "<bookmark mark='c'/> With one fare for everyone, Bo's best is ten dollars fifty, and at that fare no "
            "student crosses at all. <bookmark mark='d'/> But students carry a card. With a student fare of three "
            "fifty and ten fifty for everyone else, Bo serves both groups. <bookmark mark='e'/> Each group gets its "
            "own Lerner rule: the group whose demand is more elastic gets the lower price."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ds), FadeIn(lab_s), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(dt), FadeIn(lab_t), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(pu), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(ps_l), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def welfare(self):
        t = load("third")
        u, d = t["uniform"], t["discriminate"]
        head = VGroup(*[label(x, font_size=22, color=GREY_A) for x in ("", r"one fare", r"two fares")])
        rows = [(r"crossings a day", f"{u['q']:.1f}", f"{d['q']:.1f}", WHITE),
                (r"Bo's profit", rf"\${u['profit']:.0f}", rf"\${d['profit']:.0f}", PROFIT),
                (r"passengers' surplus", rf"\${u['cs']:.0f}", rf"\${d['cs']:.0f}", CS),
                (r"total", rf"\${u['welfare']:.0f}", rf"\${d['welfare']:.0f}", E.ACCENT)]
        grid = VGroup(head)
        for name, a_, b_, col in rows:
            grid.add(VGroup(label(name, font_size=24, color=col), label(a_, font_size=24, color=col),
                            label(b_, font_size=24, color=col)))
        for k, row in enumerate(grid):
            for c, x in zip(row, (-5.6, -1.6, 0.8)):
                c.move_to([x, 2.0 - 0.6 * k, 0], aligned_edge=LEFT)
        notes = VGroup(
            label(r"here discrimination helps everyone: \ it opens a market one price had closed", font_size=24,
                  color=CS),
            label(r"but not always: \ if one price already served both groups, \\ two prices with straight-line "
                  r"demands leave output the same and lower welfare (Schmalensee, 1981)", font_size=22, color=HOLD),
            label(r"Varian (1985): \ discrimination can raise welfare only if it raises output", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"Schmalensee, AER 71(1) (1981); Varian, AER 75(4) (1985)", corner=DR, font_size=13)
        with self.voiceover(
            "Is that good or bad? Add it up. <bookmark mark='a'/> With one fare, forty-seven and a half crossings a "
            "day; with two, seventy-two and a half. Bo's profit rises from four hundred and fifty-one dollars to five "
            "hundred and fourteen, the passengers' surplus from two hundred and twenty-six to two hundred and "
            "fifty-seven, and the total from six hundred and seventy-seven to seven hundred and seventy-one. "
            "<bookmark mark='b'/> Here discrimination helps everyone, because it opens a market that one price had "
            "closed: the students now cross. <bookmark mark='c'/> It isn't always so. If one price already served "
            "both groups, Richard Schmalensee showed that with straight-line demands two prices leave total output "
            "unchanged and lower total welfare. <bookmark mark='d'/> Hal Varian's general test: discrimination can "
            "raise welfare only if it raises output."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in grid[1:]], lag_ratio=0.5), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.clear_scene()
