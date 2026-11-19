from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ11.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 14, r"The Dials: \ how deeply do people think?", r"Across games and settings, how many steps ahead "
             r"do people reason?", "Chapter fourteen. The Dials: how deeply do people think?", scale=("person",
             "market"), lit={1936: r"Keynes's beauty contest"})
        self.keynes()
        self.dial()

    def keynes(self):
        q = quote_card(r"We have reached the third degree where we devote our intelligences to anticipating what "
                       r"average opinion expects the average opinion to be. And there are some, I believe, who "
                       r"practise the fourth, fifth and higher degrees.", r"John Maynard Keynes, \emph{The General "
                       r"Theory of Employment, Interest and Money} (1936), ch.\ 12", width=11.6, font_size=25
                       ).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"Keynes's image of the stock market: \ a newspaper contest to pick the faces \emph{others} will "
                  r"find prettiest", font_size=23),
            label(r"the guessing game is that contest, \ with numbers: \ economists call it a beauty contest",
                  font_size=23, color=LEVEL),
            label(r"if traders think one or two steps ahead, \ prices can drift from what anyone believes is true \ "
                  r"(Parts 23 and 33)", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, buff=0.35).next_to(q, DOWN, buff=0.5)
        tag = published_tag(r"Keynes, \emph{The General Theory} (1936), ch.\ 12", corner=DR, font_size=13)
        with self.voiceover(
            "How many steps people take matters well beyond the laboratory. John Maynard Keynes described the stock "
            "market in 1936 as a newspaper competition to pick, from a hundred photographs, the faces that the other "
            "competitors would find prettiest. <bookmark mark='a'/> We have reached the third degree, he wrote, "
            "where we devote our intelligences to anticipating what average opinion expects the average opinion to "
            "be; and some, he believed, practise the fourth, fifth and higher degrees. <bookmark mark='b'/> The "
            "guessing game is his contest with numbers, which is why economists call it a beauty contest. "
            "<bookmark mark='c'/> If traders reason only a step or two about each other, prices can drift from what "
            "anyone believes they are worth, a theme of Parts twenty-three and thirty-three."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.1), FadeIn(tag))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def dial(self):
        dial = dials.DIALS["reasoning_depth"]
        head = status_head(dial, r"depth of strategic reasoning \ (new)")
        frame, rows = dial_rows(dial, 0.0, 5.0, [0, 1, 2, 3, 4, 5], r"$\tau$: \ average steps of thinking in the "
                                r"cognitive hierarchy", top=1.9, step=0.75)
        meaning = wrapped_label(tex_safe(dial.meaning), 12.6, 18, GREY_A).to_edge(DOWN, buff=0.2)
        extra = label(r"equilibrium assumes infinitely many steps; \ real people take one or two, \ more with time, "
                      r"stakes and practice", font_size=21, color=E.ACCENT).next_to(meaning, UP, buff=0.25)
        tag = published_tag(r"Camerer, Ho and Chong, QJE 119(3) (2004); \ Nagel, AER 85(5) (1995); \ fits: \ Agora",
                            corner=UR, font_size=12)
        with self.voiceover(
            "This part opens a dial for how deeply people reason about each other. <bookmark mark='a'/> Across "
            "nearly a hundred experimental games, Camerer, Ho and Chong found that an average of between one and two "
            "steps of thinking fits best, typically one and a half. Agora's fits put Nagel's students at about one "
            "point one, and the Financial Times' readers at about four. <bookmark mark='b'/> Equilibrium assumes "
            "infinitely many steps. Real people take one or two, and more when they have time, stakes and practice. "
            "<bookmark mark='c'/> So the dial depends on the setting. For first-time play, levels of thinking "
            "predict better than equilibrium; for experienced players in a stable game, equilibrium does well. Part "
            "forty-five returns to it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.6), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(extra))
            vo.wait_until("c")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()
