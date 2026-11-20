from __future__ import annotations

from videos.economics.econ44.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ data, \ interoperability, \ foundation models", r"What is still being worked out?",
             "Chapter fifteen. Frontier: data, interoperability, foundation models.",
             lit={2024: r"\emph{Google}"}, scale=("firm", "world"), horizon=("a decade",))
        self.open()

    def open(self):
        cards = point_cards([
            (r"data as a barrier", r"more users give more \\ data, \ better products, \\ more users: \ a moat \\ or "
                                   r"just a good \\ product?", BUS),
            (r"interoperability", r"if users could take \\ their data and contacts \\ elsewhere, \ would \\ network "
                                  r"effects \\ lose their grip?", FIRM2),
            (r"foundation models", r"huge fixed costs \\ of training, \ cheap \\ use: \ few firms \\ or many?",
             PATIENT),
            (r"algorithms", r"how to tell learned \\ collusion from fast \\ competition in data", LOSS),
        ], width=12.8, cols=4, font_size=17).move_to(DOWN * 0.2)
        head = label(r"open questions", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(tables.FRONTIER44.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Four frontiers. <bookmark mark='a'/> Data as a barrier to entry. More users produce more data, which "
            "makes a better product, which attracts more users. Is that a moat that keeps rivals out, or simply the "
            "reward for a good product? Economists are still learning how much data matters once a firm has a lot "
            "of it. <bookmark mark='b'/> Interoperability. If people could carry their contacts, history and data "
            "to a rival, network effects would lose some of their grip; Europe's new platform rules require some of "
            "this, and their effects are being measured. <bookmark mark='c'/> Foundation models. Training a large "
            "model costs a fortune, and using it costs little: the cost structure of a natural monopoly. Yet several "
            "firms compete, and open models spread. Whether the market will tip, and toward whom, is open. "
            "<bookmark mark='d'/> And algorithms. As pricing software spreads, telling learned collusion from fast "
            "competition in real data is a measurement problem that has barely begun."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
