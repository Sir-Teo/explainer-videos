from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ16.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ what a reserve adds", r"Set reserve prices by Myerson's rule in a real market: "
             r"\ how much more does the seller earn?", "Chapter thirteen. The Dials: what a reserve adds.",
             scale=("firm", "market"), lit={2009: r"Ostrovsky and Schwarz"})
        self.design()
        self.dial()

    def design(self):
        r = load("dial")["reserve"]
        st = study_card(r"Reserve prices in Yahoo!'s search auctions", r"Michael Ostrovsky and Michael Schwarz "
                        r"(2009)",
                        [(r"varied", r"the reserve on each keyword: \ the old flat 10 cents, \ or one set by Myerson's "
                                     r"rule from estimated values, \ moved part of the way"),
                         (r"sample", rf"{r['treatment']:,} keywords given new reserves, \ {r['control']:,} kept "
                                     r"as controls, \ chosen at random".replace(",", "{,}")),
                         (r"measured", r"revenue per keyword before and after, \ against the controls, \ at fixed "
                                       r"search volumes")],
                        design="RCT", width=11.6, font_size=22).move_to(UP * 0.5)
        foot = label(r"ads shown per page fell by almost one: \ the reserves turned some bidders away", font_size=23,
                     color=HOLD).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Ostrovsky and Schwarz, working paper (2009), Tables 4--6", corner=DR, font_size=13)
        with self.voiceover(
            "This part opens a dial for what a reserve price adds in a real market. The evidence comes from an "
            "experiment at Yahoo! in the summer of 2008. <bookmark mark='a'/> Every keyword's auction had had the same reserve, "
            "ten cents a click. Michael Ostrovsky and Michael Schwarz estimated the spread of advertisers' values "
            "for each keyword, and set new reserves by Myerson's rule, moved only part of the way from ten cents, "
            "since the revenue curve is flat near its top and overshooting is costly. <bookmark mark='b'/> More "
            "than four hundred thousand keywords, chosen at random, got the new reserves; twenty-three thousand "
            "kept the old ones. <bookmark mark='c'/> They compared revenue before and after, against the controls, "
            "holding each keyword's searches fixed. <bookmark mark='d'/> The reserves did what the theory says they "
            "do: almost one fewer advertisement appeared on each page, as some bidders were priced out."
        ) as vo:
            self.play(FadeIn(st), FadeIn(tag))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def dial(self):
        dial = dials.DIALS["reserve_revenue"]
        lo, hi, x0, x1 = -0.06, 0.08, -0.2, 6.3
        head = status_head(dial, r"what a reserve adds \ (new)")
        frame, rows = dial_rows(dial, lo, hi, [-0.06, -0.04, -0.02, 0, 0.02, 0.04, 0.06, 0.08],
                                r"change in revenue \ (0.02 is 2 percent)", top=1.6, step=0.9, fmt="{:+.3f}")

        def X(v):
            return x0 + (x1 - x0) * (v - lo) / (hi - lo)

        zero = VGroup(DashedLine([X(0), 2.1, 0], [X(0), -0.6, 0], color=GREY_C, stroke_width=2),
                      label(r"no change", font_size=15, color=GREY_B).move_to([X(0), 2.3, 0]))
        meaning = wrapped_label(tex_safe(dial.meaning), 12.6, 18, GREY_A).to_edge(DOWN, buff=0.25)
        tag = published_tag(r"Ostrovsky and Schwarz (2009), Tables 4, 5 and 6", corner=UR, font_size=12)
        with self.voiceover(
            "Here is the dial. <bookmark mark='a'/> Over all keywords, revenue rose by two point seven percent, "
            "with a confidence interval from about one and a half to almost four. Small, but across the market for search "
            "advertising, the authors reckoned, worth hundreds of millions of dollars a year. <bookmark mark='b'/> But on keywords searched fewer than ten "
            "times a day, revenue fell by two percent: there, the reserve chased away bidders the auction needed. "
            "<bookmark mark='c'/> On the busier keywords, which carried three quarters of the searches, it rose by "
            "three point three percent. <bookmark mark='d'/> So the status is: depends on the setting. A reserve "
            "pays where bidders are many and drives them off where they are few, which is Bulow and Klemperer's "
            "warning from chapter seven, measured. One experiment so far; the dial returns in part sixty-one, on the platforms."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag), FadeIn(zero))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()
