from __future__ import annotations

from videos.economics.econ67.common import *  # noqa: F403


class Profession(VoiceoverScene):
    def construct(self):
        card(self, 11, r"The profession", r"Who writes economics, \ who decides what is published, \ and who is "
             r"answerable for advice?", "Chapter eleven. The profession.",
             lit={2013: "Hamermesh", 2020: "Heckman and Moktan"}, scale=("world",), horizon=("a decade",))
        self.authors()
        self.top_five()
        self.omissions()

    def authors(self):
        H = load("profession")
        years = H["years"]
        ax = plane([1958, 2016], [0, 100], center=LEFT * 2.0 + DOWN * 0.3, x_length=8.0, y_length=4.8,
                   xticks=list(years), yticks=[0, 25, 50, 75, 100], ylabel=r"percent",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        series = [("coauthored", r"articles with more than one author", FIRST),
                  ("age35", r"authors aged 35 or under", PUB),
                  ("female", r"authors who are women", TRUE)]
        lines = VGroup()
        for key, _, col in series:
            ys = H[key]
            lines.add(VGroup(path(ax, years, ys, col, 3.0, smooth=False),
                             *[Dot(ax.ax.c2p(x, y), radius=0.06, color=col) for x, y in zip(years, ys)]))
        key = legend_rows([(c, t) for _, t, c in series], font_size=15).next_to(ax.ax, RIGHT, buff=0.4).shift(
            UP * 1.3)
        side = VGroup(
            label(rf"one author: \ {100 - H['coauthored'][0]:.0f}\% of articles in 1963, \ "
                  rf"{100 - H['coauthored'][-1]:.0f}\% in 2011", font_size=17, color=FIRST),
            label(rf"women: \ {H['female'][0]:.1f}\% of authors, \ then {H['female'][-1]:.1f}\%", font_size=17,
                  color=TRUE),
            label(rf"the young: \ {H['age35'][0]:.0f}\% \ to {H['age35'][-1]:.0f}\%", font_size=17, color=PUB),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(key, DOWN, buff=0.5).align_to(key, LEFT)
        tag = published_tag(r"Hamermesh, \ \emph{JEL} 51(1) (2013), \ Tables 1 and 2 \ (AER, \ JPE, \ QJE)",
                            corner=DL, font_size=12)
        with self.voiceover(
            "Who writes economics? Hamermesh's count answers that too, for the same three journals. <bookmark "
            f"mark='a'/> In 1963, {100 - H['coauthored'][0]:.0f} percent of articles had a single author. By 2011, "
            f"{100 - H['coauthored'][-1]:.0f} percent did: economics became team work, as the data and the methods "
            "grew. <bookmark mark='b'/> Authors grew older: in 1963 half were thirty-five or under, by 2011 a "
            "third. <bookmark mark='c'/> And women, weighted by their share of each paper, wrote "
            f"{H['female'][0]:.1f} percent of the articles in 1963 and {H['female'][-1]:.1f} percent in 2011. "
            "Who asks the questions shapes which questions are asked, and economics has drawn its authors from a "
            "narrow slice of the people it studies."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            for mk, (ln, k_, s_) in zip("abc", zip(lines, key, side)):
                vo.wait_until(mk)
                self.play(Create(ln[0]), FadeIn(ln[1:]), FadeIn(k_), FadeIn(s_), run_time=1.6)
        self.clear_scene()

    def top_five(self):
        cards = point_cards([
            (r"the top five", r"the AER, \ Econometrica, \ the JPE, \ the QJE and the Review of Economic Studies: \ "
             r"publication there drives hiring and tenure", PUB),
            (r"Heckman and Moktan", r"top-five papers raise the rate of tenure in leading departments, \ even "
             r"holding other measures of a record's quality fixed", FAIL),
            (r"the cost", r"many of the most cited papers appear elsewhere; \ the screen rewards fitting five "
             r"editors' tastes, \ and slows careers", STATE),
            (r"the selection", r"a filter on significance and on taste: \ chapters one to five, \ seen from the "
             r"inside", FIRST),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"who decides what is published", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Heckman and Moktan, \ \emph{JEL} 58(2) (2020)", corner=DL, font_size=12)
        with self.voiceover(
            "And who decides what is published? <bookmark mark='a'/> In economics, five general journals carry "
            "unusual weight: the American Economic Review, Econometrica, the Journal of Political Economy, the "
            "Quarterly Journal of Economics and the Review of Economic Studies. <bookmark mark='b'/> James Heckman "
            "and Sidharth Moktan followed young economists in leading departments, and found that papers in those "
            "five journals raised the rate at which they got tenure, even holding other measures of quality fixed. "
            "<bookmark mark='c'/> They called it the tyranny of the top five: many of the most cited papers appear "
            "elsewhere, and a few editors' tastes steer careers. <bookmark mark='d'/> It is the publication filter "
            "of the first five chapters, seen from the inside."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def omissions(self):
        rows = VGroup(
            label(r"Akerlof (2020): \ the profession prefers precise answers to the questions it can answer neatly",
                  font_size=21, color=PUB),
            label(r"`hard' over `soft': \ important questions without clean data are left aside", font_size=21,
                  color=FAIL),
            label(r"advice is not scored: \ forecasts and policy claims rarely face their outcomes", font_size=21,
                  color=STATE),
            label(r"this series' answer: \ Called it?, \ the Dials and the Facts, \ in every part", font_size=21,
                  color=TRUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.2)
        tag = published_tag(r"Akerlof, \ `Sins of Omission and the Practice of Economics', \ \emph{JEL} 58(2) "
                            r"(2020)", corner=DL, font_size=12)
        with self.voiceover(
            "George Akerlof named a subtler bias. <bookmark mark='a'/> In Sins of Omission and the Practice of "
            "Economics, he argued that the profession prizes precise answers, and so prefers the questions that can "
            "be answered precisely. <bookmark mark='b'/> Hard over soft: important questions without clean data or "
            "tidy models get left aside, and are omitted rather than answered wrongly. <bookmark mark='c'/> And "
            "advice is rarely scored. A forecast or a policy claim made on television is seldom put beside what "
            "happened. <bookmark mark='d'/> This series has tried to do that in every part: Called it? puts a "
            "prediction beside its outcome, the Dials keep the evidence with its spread, and the Facts test the "
            "series' own model against the world."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()
