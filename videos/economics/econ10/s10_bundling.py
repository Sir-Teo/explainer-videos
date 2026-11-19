from __future__ import annotations

from videos.economics.econ10.common import *  # noqa: F403

TOUR = "#7BD88F"


class Bundling(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Bundling", r"Why sell two things together that people could buy apart?", "Chapter eight. "
             r"Bundling.", lit={1976: r"Adams and Yellen"})
        self.idea()
        self.cloud()

    def idea(self):
        rows = VGroup(
            label(r"two visitors, \ two goods: \ the crossing and the reef tour", font_size=27),
            label(r"Ana values the crossing at \$8 and the tour at \$2; \ Chidi the reverse", font_size=25),
            label(r"separately: \ \$8 each and one sale apiece, \ or \$2 each and two: \ \$16 at most", font_size=25,
                  color=GREY_A),
            label(r"together, \ for \$10: \ both buy, \ \$20", font_size=27, color=PROFIT),
            label(r"the bundle evens out what people will pay: \ it works when tastes are negatively correlated",
                  font_size=24, color=E.ACCENT),
            label(r"Stigler (1963): \ why film distributors sold films in blocks", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.38)
        tag = published_tag(r"Stigler, Supreme Court Review (1963); Adams and Yellen, QJE 90(3) (1976)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "A different trick: sell two things together. <bookmark mark='a'/> Bo also runs a reef tour on the far "
            "island. <bookmark mark='b'/> Ana would pay eight dollars for the crossing and two for the tour; Chidi "
            "would pay two for the crossing and eight for the tour. <bookmark mark='c'/> Sold separately, the best Bo "
            "can do is sixteen dollars, by charging eight for each and selling one of each. "
            "<bookmark mark='d'/> Sold together for ten dollars, both buy, and he takes twenty. "
            "<bookmark mark='e'/> The bundle evens out what people will pay: their values for the pair are more alike "
            "than their values for each part. It works when tastes are negatively correlated. "
            "<bookmark mark='f'/> George Stigler used the idea in 1963 to explain why film studios rented films to "
            "cinemas in blocks."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def cloud(self):
        b = load("bundle")
        v1 = np.array(b["v1"])
        left = plane([0, 12], [0, 12], center=LEFT * 4.0 + UP * 0.2, x_length=4.0, y_length=4.0,
                     xticks=[0, 5, 10], yticks=[0, 5, 10], xlabel=r"value of the crossing", ylabel=r"of the tour",
                     font_size=15)
        right = plane([0, 12], [0, 12], center=RIGHT * 0.9 + UP * 0.2, x_length=4.0, y_length=4.0,
                      xticks=[0, 5, 10], yticks=[0, 5, 10], xlabel=r"value of the crossing", ylabel=r"of the tour",
                      font_size=15)
        dn = VGroup(*[Dot(left.ax.c2p(x, y), radius=0.025, color=TOUR) for x, y in zip(v1, b["neg"])])
        dp = VGroup(*[Dot(right.ax.c2p(x, y), radius=0.025, color=STUD) for x, y in zip(v1, b["pos"])])
        n, p = b["negative"], b["positive"]
        tl = label(rf"negatively correlated ({n['corr']:.2f})", font_size=19, color=TOUR).next_to(left, UP, buff=0.15)
        tr = label(rf"positively correlated ({p['corr']:.2f})", font_size=19, color=STUD).next_to(right, UP, buff=0.15)
        side = VGroup(
            label(rf"separate: \ \${n['separate']['profit']:.0f}", font_size=21, color=GREY_A),
            label(rf"bundle: \ \${n['bundle']['profit']:.0f}", font_size=22, color=PROFIT),
            label(rf"separate: \ \${p['separate']['profit']:.0f}", font_size=21, color=GREY_A),
            label(rf"bundle: \ \${p['bundle']['profit']:.0f}", font_size=22, color=GREY_A),
        )
        VGroup(side[0], side[1]).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(left, DOWN, buff=0.35)
        VGroup(side[2], side[3]).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(right, DOWN, buff=0.35)
        notes = VGroup(
            label(r"400 visitors, \ Agora's best prices", font_size=21),
            label(r"mixed bundling \\ (each alone, or both): \\ at least as good as either", font_size=20,
                  color=GREY_A),
            label(r"Adams and Yellen (1976): \\ bundling sorts buyers too", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Agora checks it on four hundred visitors. <bookmark mark='a'/> On the left, values for the crossing and "
            "the tour are negatively correlated: people who want one want the other less. The best separate prices "
            "earn about two thousand and forty dollars; the best bundle, three thousand two hundred and forty-five, "
            "more than half as much again. <bookmark mark='b'/> On the right, the values are positively correlated, "
            "and the bundle earns slightly less than separate prices. <bookmark mark='c'/> Offering both, each good "
            "alone or the pair at a discount, is never worse than either. William Adams and Janet Yellen showed in "
            "1976 that bundling is another way of sorting buyers: it works through the shape of the whole "
            "distribution of tastes."
        ) as vo:
            self.play(FadeIn(left), FadeIn(right), FadeIn(tag), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(FadeIn(dn), FadeIn(tl), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(dp), FadeIn(tr), FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]), FadeIn(notes[2]))
        self.clear_scene()
