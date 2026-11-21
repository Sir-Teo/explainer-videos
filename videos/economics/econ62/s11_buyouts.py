from __future__ import annotations

from videos.economics.econ62.common import *  # noqa: F403


class Buyouts(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Private equity", r"What happens to a firm, \ and its workers, \ after a buyout?",
             "Chapter nine. Private equity.", lit={2014: r"Davis et al."}, scale=("firm", "nation"),
             horizon=("a decade",))
        self.paths()
        self.debate()

    def paths(self):
        B = load("buyouts")
        yrs = np.array(B["years"])
        eo, ef, pr = (100 * np.array(B[k]) for k in ("emp_original", "emp_firm", "productivity"))
        ax = plane([0, 6], [-8, 7], center=LEFT * 3.0 + DOWN * 0.4, x_length=6.2, y_length=4.4,
                   xticks=[0, 1, 2, 3, 4, 5, 6], yticks=[-6, -3, 0, 3, 6], xlabel=r"years after the buyout",
                   ylabel=r"relative to matched controls, \ \%", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", font_size=14)
        z = seg(ax, 0, 0, 6, 0, GREY_C, 1.2)
        po = path(ax, yrs, eo, COST, 3.0)
        pf = path(ax, yrs, ef, WORK, 3.0)
        pp = path(ax, yrs, pr, GAIN, 3.0)
        side = VGroup(
            label(r"the Island: \ 300 buyouts against 1,200 matched firms".replace(",", "{,}"), font_size=19,
                  color=WHITE),
            label(rf"red: \ jobs at the establishments the firm already had: \ {eo[2]:+.1f}\% after two years, \\ "
                  rf"{eo[5]:+.1f}\% after five".replace("-", "{-}"), font_size=18, color=COST),
            label(rf"gold: \ jobs at the whole firm, \ new establishments included: \ {ef[5]:+.1f}\% after five",
                  font_size=18, color=WORK),
            label(rf"green: \ productivity, \ {pr[5]:+.1f} points: \ weak plants closed, \ better ones opened",
                  font_size=18, color=GAIN),
            label(r"American buyouts: \ jobs at target establishments $-3$\% in two years, \ $-6$\% in five; \\ more "
                  r"new jobs at new establishments; \ faster reallocation \ (Davis et al.)", font_size=17,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 6.2:
            side.width = 6.2
            side.to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Davis, \ Haltiwanger, \ Handley, \ Jarmin, \ Lerner and Miranda, \ AER 104(12) "
                            r"(2014); \ the Island: \ agora.org.buyouts", corner=DL, font_size=12)
        with self.voiceover(
            "Private equity funds buy whole firms, usually with a great deal of borrowed money, and sell them "
            "some years later. Jensen saw them as the cure for chapter eight's agency problem: concentrated owners, "
            "managers who own a large stake, and debt that must be paid. Critics see job cuts. <bookmark "
            "mark='a'/> On the Island, three hundred buyouts are compared with twelve hundred similar firms. "
            "<bookmark mark='b'/> At the establishments the firms already had, jobs fall relative to the controls: "
            f"{eo[2]:.1f} percent after two years, {eo[5]:.1f} after five. <bookmark mark='c'/> But the bought "
            "firms also open new establishments, and counting them, jobs at the whole firm do not fall. <bookmark "
            "mark='d'/> Productivity rises, mostly because weak plants close and better ones open. <bookmark "
            "mark='e'/> The Island was planted to echo the largest study, by Steven Davis and colleagues, using "
            "American census data: employment at target establishments fell three percent relative to controls "
            "within two years and six percent within five, while the targets created more jobs at new "
            "establishments and moved activity faster from weak plants to strong ones."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(z), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(po), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(pf), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(pp), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def debate(self):
        cards = point_cards([
            (r"the case for", r"owners who watch, \ managers with a large stake, \ debt that disciplines: \ "
             r"chapter eight's remedies in one package", GAIN),
            (r"the case against", r"debt that leaves no room for a bad year, \ fees, \ and gains that come from "
             r"workers and suppliers rather than from efficiency", COST),
            (r"what the averages hide", r"results differ by era and by the firm bought: \ private firms bought out "
             r"often grow, \ public firms taken private often shrink", MGR),
            (r"the economist's habit", r"compare with matched firms, \ follow the jobs to new establishments, \ and "
             r"never stop at the first number", OWN),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"what to make of private equity", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "So what should one make of private equity? <bookmark mark='a'/> The case for: owners who watch, "
            "managers with a large stake, debt that disciplines, chapter eight's remedies in one package. "
            "<bookmark mark='b'/> The case against: debt that leaves no room for a bad year, large fees, and gains "
            "that may come from workers and suppliers rather than from efficiency. <bookmark mark='c'/> And the "
            "averages hide variety: results differ by era and by the kind of firm bought, with private firms "
            "bought out often growing and public firms taken private often shrinking. <bookmark mark='d'/> The "
            "habit that matters: compare with matched firms, follow the jobs to wherever they moved, and never "
            "stop at the first number."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()
