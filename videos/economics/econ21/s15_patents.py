from __future__ import annotations

from videos.economics.econ21.common import *  # noqa: F403


class Patents(VoiceoverScene):
    def construct(self):
        card(self, 13, r"Patents, \ prizes and public research", r"What does the evidence say moves innovation?",
             "Chapter thirteen. Patents, prizes and public research.",
             lit={1714: r"the Longitude prize", 2005: r"Moser", 2013: r"Williams"}, scale=("firm", "nation"),
             horizon=("decades",))
        self.bargain()
        self.evidence()

    def bargain(self):
        cards = point_cards([
            (r"patents", r"a temporary monopoly \\ in exchange for disclosure", IDEA),
            (r"prizes", r"pay for a result, \\ then give it away: \\ the Longitude prize of 1714", LIGHT),
            (r"public research", r"pay scientists directly; \\ publish everything", INST),
            (r"secrecy", r"keep the recipe; \\ no disclosure at all", WEDGE),
        ], width=12.6, cols=2, font_size=22).move_to(DOWN * 0.15)
        head = label(r"four ways to pay for ideas", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Chapter two showed that ideas must be paid for somehow. Societies have four ways. "
            "<bookmark mark='a'/> Patents: a monopoly for about twenty years, in exchange for publishing how the "
            "invention works. <bookmark mark='b'/> Prizes: pay for a result and give it to everyone, like the "
            "British Parliament's Longitude prize of 1714 for a way to find a ship's longitude at sea. "
            "<bookmark mark='c'/> Public research: pay scientists directly and publish what they find. "
            "<bookmark mark='d'/> And secrecy, which pays the inventor but tells the world nothing."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def evidence(self):
        rows = VGroup(
            label(r"what the evidence says", font_size=30, color=E.ACCENT),
            label(r"Petra Moser, \ 2005: \ at the world's fairs of 1851 and 1876, \ inventors from countries without "
                  r"patents \\ were not obviously less inventive, \ but worked where secrets could be kept", font_size=20,
                  color=IDEA),
            label(r"patents shifted the direction of invention more than its rate", font_size=21, color=GREY_A),
            label(r"Heidi Williams, \ 2013: \ genes sequenced first by Celera, \ under its temporary IP, \\ saw "
                  r"20--30\% less later research and product development than genes in the public domain",
                  font_size=20, color=WEDGE),
            label(r"protection can block the next inventor: \ the spillover of chapter five, \ cut", font_size=21,
                  color=GREY_A),
            label(r"public science and tax credits: \ the next two chapters", font_size=21, color=INST),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.1)
        tag = published_tag(r"Moser, AER 95(4) (2005); \ Williams, JPE 121(1) (2013): \ 1--27", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Which works best is an empirical question, and a few natural experiments have answered parts of it. "
            "<bookmark mark='a'/> Petra Moser studied the inventions shown at the world's fairs of 1851 and 1876. "
            "Inventors from countries without patent laws were not obviously less inventive, but concentrated in industries "
            "where secrets could be kept, like scientific instruments and food processing. "
            "<bookmark mark='b'/> Patents shifted the direction of invention more than its rate. "
            "<bookmark mark='c'/> Heidi Williams studied the human genome. Genes first sequenced by the private "
            "firm Celera were covered by its intellectual property for up to two years; genes sequenced by the "
            "public project were free. The Celera genes saw twenty to thirty percent less subsequent research and "
            "product development, and the gap persisted. <bookmark mark='d'/> Protection meant to reward the first "
            "inventor can block the next, cutting exactly the spillover that makes research valuable. "
            "<bookmark mark='e'/> How large that value is, and what public money does with it, come next."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
