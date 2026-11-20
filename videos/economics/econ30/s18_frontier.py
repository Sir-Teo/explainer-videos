from __future__ import annotations

from videos.economics.econ30.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 16, r"Frontier: \ the model after 2021", r"What did the surge of 2021--23 teach the New Keynesian "
             r"model?", "Chapter sixteen. Frontier: the model after 2021.",
             lit={2023: r"Benigno and Eggertsson", 2018: r"Kaplan, \ Moll and Violante"}, scale=("nation",),
             horizon=("a quarter", "three years"))
        self.surge()
        self.open_()

    def surge(self):
        S = load("sticky")
        rows = VGroup(
            label(r"2021--23: \ what the model had to learn", font_size=27, color=E.ACCENT),
            label(rf"flexible prices first: \ up {S['peak_flex_2022']:.0f}\% by February 2022; \ sticky prices "
                  rf"peaked at {S['peak_sticky_2022']:.1f}\% that December", font_size=21, color=FLEX),
            label(r"when many firms reprice at once, \ the fairy's fixed visiting rate is wrong: \ "
                  r"state-dependent pricing", font_size=21, color=PRICE),
            label(r"a curve that steepens in tight markets \ (Benigno and Eggertsson, \ Part 28)", font_size=21,
                  color=INFL),
            label(r"supply shocks that move through networks of firms, \ not one cost-push term", font_size=21,
                  color=COST),
            label(r"expectations that stayed anchored, \ mostly", font_size=21, color=CB),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Benigno and Eggertsson, \ NBER WP 31197 (2023); \ the Atlanta Fed's CPIs via FRED",
                            corner=DR, font_size=12)
        with self.voiceover(
            "The surge of 2021 to 2023 tested this model hard. <bookmark mark='a'/> Here is what it had to learn. "
            f"<bookmark mark='b'/> Flexible prices moved first, up {S['peak_flex_2022']:.0f} percent by February "
            f"2022, and sticky prices followed, peaking at {S['peak_sticky_2022']:.1f} percent that December. "
            "<bookmark mark='c'/> When many firms reprice at once, as they did, a fairy who visits a fixed share "
            "each quarter is wrong; pricing that depends on the state of the economy fits better. "
            "<bookmark mark='d'/> The Phillips curve may steepen when labour markets are very tight, Benigno and "
            "Eggertsson's bent curve from Part twenty-eight. <bookmark mark='e'/> Supply shocks travelled through "
            "networks of firms, not as one cost-push term. <bookmark mark='f'/> And long-run expectations stayed "
            "anchored, mostly, which helped inflation fall without a recession."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def open_(self):
        rows = VGroup(
            label(r"open questions", font_size=27, color=E.ACCENT),
            label(r"is the frequency of price changes a constant, \ or a choice that rises with inflation?",
                  font_size=21, color=PRICE),
            label(r"how much does monetary policy work through incomes, \ not interest rates? \ (Part 52)",
                  font_size=21, color=OUTPUT),
            label(r"what does forward guidance really do, \ once the puzzle is fixed?", font_size=21, color=CB),
            label(r"can models with many households and many firms be solved and estimated? \ (Parts 51, \ 52, \ 55)",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Kaplan, \ Moll and Violante, \ \emph{AER} 108(3) (2018)", corner=DR, font_size=12)
        with self.voiceover(
            "The open questions follow. <bookmark mark='a'/> Is the frequency of price changes a constant, or a "
            "choice that rises when inflation does? <bookmark mark='b'/> How much does monetary policy work through "
            "people's incomes rather than through interest rates, as models with many households suggest? "
            "<bookmark mark='c'/> What does forward guidance really do, once the puzzle is fixed? "
            "<bookmark mark='d'/> And can models with many households and many firms be solved and estimated? The "
            "research tier of this series takes them up."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
