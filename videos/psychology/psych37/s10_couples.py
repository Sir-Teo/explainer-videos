from __future__ import annotations

from videos.psychology.psych37.common import *  # noqa: F403


class Couples(VoiceoverScene):
    def construct(self):
        self.card()
        self.joel()
        self.overfit()
        self.bonds()

    def card(self):
        card = chapter_card(9, r"Predicting relationships", r"Can anyone tell which couples will last?",
                            lit={1987: r"Hazan \& Shaver", 2001: r"Heyman \& Slep", 2020: r"Joel et al."}, part=PART,
                            scale=("person",), marr=("what",))
        with self.voiceover("Chapter nine. Predicting relationships."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def joel(self):
        head = heading(r"Eleven thousand couples")
        A = axes([-0.6, 1.6], [0, 50], x_length=4.4, y_length=3.4, xticks=None, yticks=[0, 25, 50],
                 yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"variance in relationship quality", center=[-3.9, -0.3, 0],
                 font_size=15)
        b = bars(A.ax, [0, 1], [45, 21], [GOOD, CROWD], width=0.6)
        names = VGroup(wrapped_label(r"how I see the relationship", 1.8, 14, GOOD).next_to(A.ax.c2p(0, 0), DOWN,
                                                                                      buff=0.15),
                       wrapped_label(r"who I am", 1.8, 14, CROWD).next_to(A.ax.c2p(1, 0), DOWN, buff=0.15))
        tops = VGroup(label(r"up to 45\%", font_size=16, color=GOOD).next_to(A.ax.c2p(0, 45), UP, buff=0.08),
                      label(r"up to 21\%", font_size=16, color=CROWD).next_to(A.ax.c2p(1, 21), UP, buff=0.08))
        rows = rows_of([
            (r"Joel and colleagues, \ 2020: \ 43 longitudinal datasets from 29 laboratories, \ 11{,}196 couples, "
             r"\ random forests", WHITE),
            (r"a person's own perceptions of the relationship explained up to 45\% of its quality: \ perceived "
             r"partner commitment, \ appreciation, \ sexual satisfaction, \ perceived partner satisfaction, \ conflict",
             GOOD),
            (r"their own traits, \ up to 21\%; \ the partner's reports added nothing beyond the person's own "
             r"perceptions", CROWD),
            (r"and changes in quality over time were largely unpredictable from anything measured", AUTH),
        ], 6.4, 19, 0.34).move_to([3.0, -0.3, 0])
        tag = published_tag(r"Joel et al.\ (2020)")
        with self.voiceover(
            "What about couples who are already together? <bookmark mark='a'/> In 2020 Joel and dozens of "
            "colleagues pooled forty-three longitudinal datasets from twenty-nine laboratories: eleven thousand one "
            "hundred and ninety-six couples, analysed with machine learning. <bookmark mark='b'/> A person's own "
            "perceptions of the relationship explained up to forty-five percent of its quality: whether they felt "
            "the partner was committed, appreciated them, and was satisfied, their sexual satisfaction, and "
            "conflict. <bookmark mark='c'/> Their own traits explained up to twenty-one percent, and the partner's "
            "reports added nothing beyond the person's own perceptions. <bookmark mark='d'/> And changes in quality "
            "over time were largely unpredictable from anything measured."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(b[0], DOWN), FadeIn(tops[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(b[1], DOWN), FadeIn(tops[1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def overfit(self):
        d = load("divorce")
        head = heading(r"Ninety percent, \ in sample")
        A = axes([0.2, 1.0], [0, 1.0], x_length=5.4, y_length=2.7, xticks=[0.2, 0.4, 0.6, 0.8, 1.0], yticks=None,
                 xfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"accuracy", center=[-3.3, 0.45, 0], font_size=15)
        edges = np.linspace(0.2, 1.0, 33)
        mids = (edges[:-1] + edges[1:]) / 2
        hi, _ = np.histogram(d["insample"], bins=edges)
        ho, _ = np.histogram(d["loo"], bins=edges)
        m = max(hi.max(), ho.max())
        bi = bars(A.ax, mids, hi / m * 0.95, AUTH, width=0.022, opacity=0.8)
        bo = bars(A.ax, mids, ho / m * 0.95, CROWD, width=0.022, opacity=0.7)
        base = DashedLine(A.ax.c2p(d["base"], 0), A.ax.c2p(d["base"], 1.0), color=GREY_A)
        bl = label(r"always guess ``stays married''", font_size=14, color=GREY_A).next_to(A.ax.c2p(d["base"], 1.0),
                                                                                       UP, buff=0.08)
        key = legend([(AUTH, r"on the couples it was fitted to"), (CROWD, r"on couples it has not seen")],
                     font_size=14).move_to(A.ax.c2p(0.4, 0.8))
        rows = rows_of([
            (r"Psyche: \ 56 couples, \ 30 measured variables, \ only one weakly related to divorce; \ a classifier is "
             r"fitted, \ 200 times over", WHITE),
            (rf"scored on the same couples, \ it is right {pct(d['mean_insample'])} of the time; \ scored on couples "
             rf"it has not seen, \ {pct(d['mean_loo'])}: \ worse than always guessing the commoner outcome", AUTH),
            (r"Heyman and Slep, \ 2001: \ the celebrated divorce-prediction figures were mostly fits to the couples "
             r"studied; \ without cross-validation, \ accuracy is an upper bound, \ and here a misleading one", YOU),
        ], 12.4, 20, 0.28).move_to([0, -2.55, 0])
        tag = psyche_tag(r"\texttt{social.overfit\_divorce}; \ Heyman \& Slep (2001)")
        with self.voiceover(
            "Then there are the famous claims of predicting divorce with ninety percent accuracy. "
            "<bookmark mark='a'/> Here's how such a number can arise. Psyche has fifty-six couples and thirty "
            "measured variables, only one of them weakly related to divorce, and fits a classifier, two hundred "
            "times over. <bookmark mark='b'/> Scored on the same couples, it's right about "
            f"{spct(d['mean_insample'])} of the time. Scored on couples it hasn't seen, {spct(d['mean_loo'])}: worse "
            "than always guessing the commoner outcome. <bookmark mark='c'/> In 2001 Heyman and "
            "Slep made this argument about the celebrated divorce-prediction figures. They were fits to the couples "
            "studied. Without cross-validation, accuracy is only an upper bound, and here a misleading one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(base), FadeIn(bl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(bi), FadeIn(bo), FadeIn(key), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def bonds(self):
        head = heading(r"Attachment and commitment")
        left = VGroup(word_chip(r"adult attachment", color=PERSON, font_size=22, width=5.2),
                      wrapped_label(r"Hazan and Shaver, \ 1987: \ a newspaper ``love quiz'' asked adults which of "
                                    r"three descriptions fitted their romantic relationships; \ about 56\% chose the "
                                    r"secure one, \ the rest avoidant or anxious", 5.2, 18, WHITE),
                      wrapped_label(r"the categories of Part 30's infants, \ applied to adult love", 5.2, 18, GREY_A)
                      ).arrange(DOWN, buff=0.25)
        right = VGroup(word_chip(r"the investment model", color=CROWD, font_size=22, width=5.2),
                       wrapped_label(r"Rusbult: \ commitment rises with satisfaction and with what has been invested "
                                     r"in the relationship, \ and falls with the quality of the alternatives", 5.2, 18,
                                     WHITE),
                       wrapped_label(r"people stay in unsatisfying relationships when the alternatives look worse",
                                     5.2, 18, GREY_A)).arrange(DOWN, buff=0.25)
        VGroup(left, right).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to([0, 0.3, 0])
        foot = wrapped_label(r"both describe how people feel about relationships; \ neither, \ like the couple "
                             r"studies, \ forecasts which particular relationship will last", 12.0, 20, YOU).to_edge(
            DOWN, buff=1.15)
        tag = historical_tag(r"Hazan \& Shaver (1987); \ Rusbult (1980)")
        with self.voiceover(
            "Two frameworks describe the bonds themselves. <bookmark mark='a'/> In 1987 Cindy Hazan and Phillip "
            "Shaver ran a love quiz in a newspaper, asking adults which of three descriptions fitted their romantic "
            "relationships. About fifty-six percent chose the secure one, the rest avoidant or anxious. These were "
            "the categories of Part 30's infants, applied to adult love. <bookmark mark='b'/> Caryl Rusbult's "
            "investment model says commitment rises with satisfaction and with what has been invested, and falls "
            "with the quality of the alternatives. People stay in unsatisfying relationships when the alternatives "
            "look worse. <bookmark mark='c'/> Both describe how people feel about relationships. Neither forecasts "
            "which particular relationship will last."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
