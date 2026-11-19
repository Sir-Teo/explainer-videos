from __future__ import annotations

from videos.economics.econ8.common import *  # noqa: F403


class Coase(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Coase: \ why is there a firm at all?", r"If markets coordinate so well, why is so much done "
             r"by command inside firms?", "Chapter ten. Coase: why is there a firm at all?",
             lit={1937: r"Coase: why firms exist"}, scale=("firm", "market"), horizon=("a decade",))
        self.answer()
        self.boundary()
        self.make_or_buy()

    def answer(self):
        q = quote_card(r"The main reason why it is profitable to establish a firm would seem to be that there is a "
                       r"cost of using the price mechanism.", r"Coase, ``The Nature of the Firm'' (1937)",
                       width=11.0, font_size=27, color=FIRM).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"the costs of using the market:", font_size=27),
            label(r"finding out what the prices are", font_size=26, color=MARKET),
            label(r"negotiating and concluding a contract for every exchange", font_size=26, color=MARKET),
            label(r"a firm replaces many contracts with one: \ an employee agrees to follow directions, \\ within "
                  r"limits, \ for a wage", font_size=25, color=FIRM),
            label(r"today these are called \emph{transaction costs}", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.28).next_to(q, DOWN, buff=0.45)
        tag = published_tag(r"Coase, Economica 4(16) (1937) 386--405", corner=DR, font_size=14)
        with self.voiceover(
            "Coase's answer was one sentence. <bookmark mark='a'/> The main reason why it is profitable to "
            "establish a firm, he wrote, would seem to be that there is a cost of using the price mechanism. "
            "<bookmark mark='b'/> What costs? The most obvious is finding out what the relevant prices are. "
            "<bookmark mark='c'/> Another is negotiating and concluding a separate contract for every exchange. "
            "<bookmark mark='d'/> A firm replaces a crowd of contracts with one: an employee agrees, within limits, "
            "to do as he is directed, for a wage. Inside those limits, nobody needs to haggle. "
            "<bookmark mark='e'/> Economists now call these the costs of transacting, and the idea took decades to "
            "catch on. Coase was given the Nobel prize for it in 1991."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(q, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def boundary(self):
        rows = VGroup(
            label(r"then why not one enormous firm?", font_size=32, color=E.ACCENT),
            label(r"organizing has costs too, \ and they rise with size: \\ managers make more mistakes as they "
                  r"direct more", font_size=26, color=FIRM),
            label(r"a firm grows until organizing one more transaction inside it \\ costs as much as carrying it "
                  r"out in the market", font_size=26),
            label(r"the boundary of the firm is set at a margin, \ like everything else", font_size=26,
                  color=E.ACCENT),
            label(r"so firms should grow when organizing gets cheaper \ (the telephone, \ the computer) \\ and shrink "
                  r"when markets do \ (chapter 15)", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.4)
        with self.voiceover(
            "But that raises the opposite question. <bookmark mark='a'/> If organizing inside a firm saves the costs of "
            "the market, why isn't the whole economy one enormous firm? <bookmark mark='b'/> Because organizing has "
            "costs too, and they rise with size: the more a management directs, the more mistakes it makes in putting "
            "resources where they're worth most. <bookmark mark='c'/> So a firm expands until the cost of "
            "organizing one more transaction inside it equals the cost of carrying it out in the market, or in "
            "another firm. <bookmark mark='d'/> The boundary of the firm is set at a margin, like everything else in "
            "this part. <bookmark mark='e'/> And it moves. Coase noticed that inventions that make organizing cheaper, "
            "the telephone and the telegraph in his day, should make firms bigger; chapter fifteen asks what today's "
            "should do."
        ) as vo:
            self.play(FadeIn(rows[0], shift=UP * 0.1))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def make_or_buy(self):
        b = load("boundary")
        k = np.array(b["k"])
        ax = plane([0, 1.2], [0, 3.6], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.6, y_length=5.0,
                   xticks=[0, 0.4, 0.8, 1.2], yticks=[0, 1, 2, 3], xlabel=r"how specific the input is to this "
                   r"buyer", ylabel=r"cost of governing the deal", font_size=17)
        m = path(ax, k, b["market"], color=MARKET, width=3.5, smooth=False)
        h = path(ax, k, b["hierarchy"], color=FIRM, width=3.5, smooth=False)
        sw = DashedLine(ax.ax.c2p(b["switch"], 0), ax.ax.c2p(b["switch"], 3.6), color=GREY_C, stroke_width=1.8)
        names = VGroup(label(r"buy: \ the market", font_size=20, color=MARKET).next_to(ax.ax.c2p(1.2, b["market"][-1]),
                                                                                        UP, buff=0.1).shift(LEFT * 0.8),
                       label(r"make: \ the firm", font_size=20, color=FIRM).next_to(ax.ax.c2p(1.2, b["hierarchy"][-1]),
                                                                                    DOWN, buff=0.3).shift(LEFT * 0.8))
        side = VGroup(
            label(r"make or buy? \ Crusoe's sails", font_size=26),
            label(r"standard canvas: \ buy it, \\ many sellers compete", font_size=23, color=MARKET),
            label(r"sails cut for one hull design: \\ make them, \ or face a single seller", font_size=23,
                  color=FIRM),
            label(r"Williamson (1975, 1985): \\ the more specific the asset, \\ the more it belongs inside", font_size=23,
                  color=E.ACCENT),
            label(r"illustrative costs; \ the next chapter \\ asks what goes wrong in the market", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = illustrative_tag(r"illustrative governance costs (Williamson's heuristic)", corner=DR, font_size=14)
        with self.voiceover(
            "Coase's idea became operational in the hands of Oliver Williamson. <bookmark mark='a'/> Should Crusoe "
            "make his own sails or buy them? <bookmark mark='b'/> Standard canvas, which many sailmakers sell, he "
            "should buy: the market is cheap to use when there are many sellers to choose from. "
            "<bookmark mark='c'/> Sails cut for one hull design are different. Only the sailmaker who invested in "
            "the patterns can supply them, and once she has, Crusoe faces a single seller. <bookmark mark='d'/> "
            "Williamson's rule of thumb: as the assets involved become more specific to a particular relationship, "
            "the cost of governing the deal through the market rises faster than the cost of bringing it inside a "
            "firm, and past some point it pays to make rather than buy. <bookmark mark='e'/> The costs here are "
            "illustrative. The next chapter asks exactly what goes wrong in the market."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(m), Create(h), FadeIn(names))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(sw), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
