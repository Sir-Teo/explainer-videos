from __future__ import annotations

from videos.economics.econ57.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ language models and real-time distributions", r"What will reading the economy "
             r"look like in ten years?", "Chapter fifteen. Frontier: language models and real-time distributions.",
             lit={2022: r"Blanchet, \ Saez and Zucman", 2024: r"Halawi et al."}, scale=("person", "nation"),
             horizon=("a day", "a decade"))
        self.open_()

    def open_(self):
        cards = point_cards([
            (r"language models as forecasters", r"asked questions about events after their training ended, \ "
             r"systems built on language models have come close to crowds of human forecasters \ (Halawi et al.\ "
             r"2024); \ scoring them fairly needs the same rules: \ no peeking at the answer", SPF),
            (r"real-time distributions", r"not just how fast the economy grows but who gains: \ Thomas Blanchet, \ "
             r"Emmanuel Saez and Gabriel Zucman's real-time inequality accounts, \ monthly", LATEST),
            (r"official statistics, \ rebuilt", r"payrolls benchmarked to tax records, \ prices scraped by the "
             r"agencies themselves, \ and response rates to surveys that keep falling", FIRST),
            (r"forecasting the forecasters", r"what moves markets is the surprise: \ models of the consensus, \ and "
             r"of when forecasters revise, \ are now part of the job", GB),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.15)
        head = label(r"what remains open", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Halawi, \ Zhang, \ Yueh-Han and Steinhardt, \ NeurIPS (2024); \ Blanchet, \ Saez and "
                            r"Zucman, \ NBER WP 30229 (2022)", corner=DR, font_size=11)
        with self.voiceover(
            "What remains open. <bookmark mark='a'/> Language models are being tested as forecasters. Danny Halawi "
            "and colleagues built a system that, asked about events after its training ended, came close to the "
            "crowds of human forecasters on prediction platforms. Scoring such systems needs this part's rules, "
            "and one more: make sure the model has not already read the answer. <bookmark mark='b'/> Economists "
            "want to read not only how fast the economy grows but who gains: Thomas Blanchet, Emmanuel Saez and "
            "Gabriel Zucman built monthly distributional accounts, in real time. <bookmark mark='c'/> Official "
            "statistics themselves are being rebuilt, as survey response rates fall and administrative and scraped "
            "data take their place. <bookmark mark='d'/> And because markets move on surprises, forecasting the "
            "forecasters, the consensus and its revisions, has become part of the job."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
