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
        ], width=12.8, cols=4, font_size=17).move_to(DOWN * 1.35)
        head = label(r"open questions", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(tables.FRONTIER44.tag, corner=DR, font_size=11)
        loops = [
            [(r"more users", BUS), (r"more data", BUS), (r"a better product", BUS), (r"more users", BUS)],
            [(r"your contacts, \ history and data", FIRM2), (r"carried to \ a rival", FIRM2),
             (r"the network \ comes with you", FIRM2)],
            [(r"training: \ a fortune, once", PATIENT), (r"each answer: \ cheap", PATIENT),
             (r"average cost falls \ with every user", PATIENT)],
            [(r"software sets \ prices", LOSS), (r"prices high \ and in step", LOSS),
             (r"learned collusion, \ or fast competition?", LOSS)],
        ]
        chains = [flow_chain(st, box_w=2.6, box_h=0.85, buff=0.45, font_size=17).move_to(UP * 2.05) for st in loops]
        asks = [label(t, font_size=19, color=col).move_to(UP * 1.05) for t, col in (
            (r"a moat that keeps rivals out, \ or the reward for a good product?", BUS),
            (r"Europe's Digital Markets Act (2022) \ requires some portability and interoperability", FIRM2),
            (r"yet several firms compete, \ and open models spread", PATIENT),
            (r"the same prices can come from either", LOSS))]
        with self.voiceover(
            "Four frontiers. <bookmark mark='a'/> Data as a barrier to entry. More users produce more data, which "
            "makes a better product, which attracts more users. <bookmark mark='a2'/> Is that a moat that keeps "
            "rivals out, or simply the reward for a good product? Economists are still learning how much data "
            "matters once a firm has a lot of it. <bookmark mark='b'/> Interoperability. If people could carry "
            "their contacts, history and data to a rival, network effects would lose some of their grip. "
            "<bookmark mark='b2'/> Europe's Digital Markets Act requires some of this of the largest platforms, "
            "and its effects are being measured. <bookmark mark='c'/> Foundation models. Training a large model "
            "costs a fortune, and using it costs little: the cost structure of a natural monopoly. "
            "<bookmark mark='c2'/> Yet several firms compete, and open models spread. Whether the market will tip, "
            "and toward whom, is open. <bookmark mark='d'/> And algorithms. As pricing software spreads, telling "
            "learned collusion from fast competition in real data is a measurement problem that has barely begun."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, (mk, c) in enumerate(zip("abcd", cards.cards)):
                vo.wait_until(mk)
                out = [FadeOut(chains[k - 1]), FadeOut(asks[k - 1])] if k else []
                self.play(*out, FadeIn(c, shift=UP * 0.1), run_time=0.8)
                ch = chains[k]
                self.play(LaggedStart(*[FadeIn(b) for b in ch.boxes], lag_ratio=0.35),
                          LaggedStart(*[GrowArrow(a) for a in ch.arrows], lag_ratio=0.35), run_time=2.4)
                if k < 3:
                    vo.wait_until(mk + "2")
                self.play(FadeIn(asks[k], shift=UP * 0.1), Circumscribe(c, color=WHITE, buff=0.05))
        self.clear_scene()
