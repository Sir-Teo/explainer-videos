from __future__ import annotations

from videos.economics.econ21.common import *  # noqa: F403


class Rival(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Ideas are not like lamps", r"What makes an idea different from a machine, \ and why does that "
             r"break perfect competition?", "Chapter two. Ideas are not like lamps.",
             lit={1962: r"Arrow on invention", 1990: r"Romer"}, scale=("firm", "world"), horizon=("decades",))
        self.grid()
        self.replication()
        self.euler()

    def grid(self):
        cells = [
            (r"rival, \ excludable", r"a fish, \ a lamp, \ a hammer", LIGHT),
            (r"rival, \ hard to exclude", r"fish in the open sea", "#F29E8E"),
            (r"non-rival, \ excludable", r"a patented design, \ software, \ a recipe kept secret", IDEA),
            (r"non-rival, \ hard to exclude", r"calculus, \ the germ theory of disease, \ a published idea", INST),
        ]
        cards = point_cards(cells, width=12.4, cols=2, font_size=23).move_to(DOWN * 0.2)
        head = VGroup(label(r"rival: \ my use leaves less for you", font_size=24, color=GREY_A),
                      label(r"excludable: \ you can be stopped from using it", font_size=24, color=GREY_A)).arrange(
            DOWN, buff=0.15).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Two properties sort every good. <bookmark mark='a'/> A good is rival if my using it leaves less for you, "
            "and excludable if you can be stopped from using it. <bookmark mark='b'/> A fish is both: if I eat it you "
            "cannot, and I can keep it from you. <bookmark mark='c'/> Fish in the open sea are rival but hard to "
            "fence off, the tragedy of the commons of part fifteen. <bookmark mark='d'/> A design is different. My "
            "using it takes nothing from you: it is non-rival. Whether it is excludable depends on patents, secrecy "
            "and law. <bookmark mark='e'/> And some ideas, once published, are neither: anyone can use calculus, and "
            "no one can be stopped."
        ) as vo:
            self.play(FadeIn(head[0]))
            vo.wait_until("a")
            self.play(FadeIn(head[1]))
            for mk, c in zip("bcde", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def replication(self):
        r = load("replication")
        rows = VGroup(
            MathTex(r"Y = F(K, L, A) = A\,K^{\alpha} L^{1-\alpha}", font_size=48),
            MathTex(rf"F(2K, 2L, A) = 2\,F(K, L, A)", font_size=44, color=OUTPUT),
            label(r"build a second factory, \ copy everything: \ twice the output", font_size=22, color=GREY_A),
            MathTex(rf"F(2K, 2L, 2A) = {r['double_KLA']:.0f}\,F(K, L, A)", font_size=44, color=IDEA),
            label(r"but the blueprint need not be invented twice", font_size=22, color=GREY_A),
            label(r"constant returns to the rival inputs \ $\Rightarrow$ \ increasing returns once ideas count",
                  font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.1)
        with self.voiceover(
            "Non-rivalry changes the arithmetic of production. <bookmark mark='a'/> Write output as a function of "
            "capital, labour and the stock of ideas, A. <bookmark mark='b'/> The replication argument: to double "
            "output, build a second factory just like the first, with the same machines and the same number of "
            "workers. Doubling the rival inputs doubles output. <bookmark mark='c'/> But the second factory uses the "
            "same blueprint. The idea does not need to be invented twice. <bookmark mark='d'/> So if you also double "
            "the stock of ideas, output more than doubles: here it quadruples. <bookmark mark='e'/> Constant returns "
            "to the things that are used up means increasing returns once ideas are counted."
        ) as vo:
            self.play(Write(rows[0]))
            vo.wait_until("b")
            self.play(Write(rows[1]), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(Indicate(rows[2]))
            vo.wait_until("d")
            self.play(Write(rows[3]), FadeIn(rows[4]))
            vo.wait_until("e")
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def euler(self):
        rows = VGroup(
            MathTex(r"r K + w L = \frac{\partial F}{\partial K}K + \frac{\partial F}{\partial L}L = F", font_size=46),
            label(r"Euler's theorem: \ under constant returns, \ paying capital and labour their marginal products "
                  r"uses up all of output", font_size=22, color=GREY_A),
            label(r"nothing is left to pay for the ideas", font_size=26, color=WEDGE),
            label(r"so ideas must be paid for some other way:", font_size=24, color=GREY_A),
            label(r"monopoly profits \ (patents, \ secrecy) \quad $\cdot$ \quad public funding \ (science) \quad "
                  r"$\cdot$ \quad prizes \quad $\cdot$ \quad as a by-product", font_size=22, color=IDEA),
            label(r"perfect competition cannot be the whole story of growth", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Arrow, \emph{The Rate and Direction of Inventive Activity} (NBER, 1962); \ Romer (1990)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "And increasing returns break perfect competition. <bookmark mark='a'/> If output has constant returns "
            "in capital and labour, then paying each its marginal product exactly exhausts output: Euler's theorem. "
            "<bookmark mark='b'/> Nothing is left over to pay whoever invented the blueprint. "
            "<bookmark mark='c'/> So ideas have to be paid for some other way. <bookmark mark='d'/> By monopoly "
            "profits, protected by patents or secrecy; by public money, as most science is; by prizes; or as a "
            "by-product of something else. Kenneth Arrow saw the problem in 1962: a market rewards invention badly "
            "precisely because an idea, once known, is cheap to share. <bookmark mark='e'/> Growth driven by ideas "
            "cannot be a story of perfect competition alone, and Romer's model makes room for monopoly."
        ) as vo:
            self.play(Write(rows[0]), FadeIn(tag))
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
            vo.wait_until("e")
            self.play(FadeIn(rows[5]))
        self.clear_scene()
