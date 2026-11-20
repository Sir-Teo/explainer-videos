from __future__ import annotations

from videos.economics.econ33.common import *  # noqa: F403


class Pattern(VoiceoverScene):
    def construct(self):
        card(self, 2, r"The pattern: \ Kindleberger and Minsky", r"Do manias and panics follow a script?",
             "Chapter two. The pattern: Kindleberger and Minsky.", lit={1978: r"Kindleberger", 1986: r"Minsky"},
             scale=("market", "nation"), horizon=("a decade",))
        self.anatomy()
        self.minsky()

    def anatomy(self):
        chain = flow_chain([(r"displacement", HOUSE), (r"boom, \ fed by credit", CREDIT), (r"euphoria", RATE),
                            (r"distress", HOLD), (r"revulsion and panic", CRISIS)],
                           box_w=2.3, box_h=1.15, buff=0.42, font_size=21,
                           notes=[r"a new technology, \\ a new market, \\ a war's end", r"lending grows \\ faster "
                                  r"than income", r"prices for \\ their own sake", r"insiders sell; \\ a failure",
                                  r"a rush \\ to cash"], note_size=16).move_to(DOWN * 0.2)
        head = label(r"Charles Kindleberger, \ \emph{Manias, \ Panics, \ and Crashes} \ (1978)", font_size=26,
                     color=E.ACCENT).to_edge(UP, buff=0.5)
        foot = label(r"a script read from history, \ not a model: \ it does not say when, \ or how far",
                     font_size=22, color=GREY_A).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Kindleberger, \ \emph{Manias, \ Panics, \ and Crashes} (1978), \ after Minsky",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Start with the historians. In 1978 Charles Kindleberger read centuries of manias and panics, from Dutch "
            "tulips to the South Sea Bubble to 1929, and found the same script in most of them. <bookmark mark='a'/> "
            "It begins with a displacement: something genuinely new, a technology, a market, the end of a war, that "
            "makes some investments more profitable. <bookmark mark='b'/> A boom follows, and it is fed by credit, "
            "lending that grows faster than income. <bookmark mark='c'/> Then euphoria: prices rise because they "
            "have been rising. <bookmark mark='d'/> Distress: insiders sell, a firm fails, a fraud is found. "
            "<bookmark mark='e'/> And revulsion: everyone wants cash at once. <bookmark mark='f'/> It is a pattern "
            "read from history, not a model. It does not say when the turn will come, or how far it will go."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, k in zip("abcde", range(5)):
                vo.wait_until(mk)
                anims = [FadeIn(chain.boxes[k], shift=RIGHT * 0.1), FadeIn(chain.notes[k])]
                if k:
                    anims.append(GrowArrow(chain.arrows[k - 1]))
                self.play(*anims)
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def minsky(self):
        M = load("minsky")
        yrs = np.array(M["year"])
        ax = plane([0, 11], [0, 1], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.0, y_length=4.4,
                   xticks=[0, 3, 6, 9, 11], yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"years into the boom",
                   ylabel=r"share of borrowers", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%",
                   font_size=15)
        h = np.array(M["hedge"])
        s = np.array(M["speculative"])
        p = np.array(M["ponzi"])
        b_h = band(ax, yrs, np.zeros_like(h), h, CALM, 0.55)
        b_s = band(ax, yrs, h, h + s, HOUSE, 0.55)
        b_p = band(ax, yrs, h + s, h + s + p, CRISIS, 0.7)
        rate_line = path(ax, yrs, np.array(M["rate"]) * 10, RATE, 3.0, smooth=False)
        defs = VGroup(
            label(r"hedge: \ cash flow pays \\ interest and principal", font_size=18, color=CALM),
            label(r"speculative: \ pays the interest, \\ must roll over the principal", font_size=18, color=HOUSE),
            label(r"Ponzi: \ cannot pay even the interest; \\ must borrow more or sell", font_size=18, color=CRISIS),
            label(rf"dashed pink: \ the interest rate, \\ {100 * M['rate'][0]:.0f}\% rising to "
                  rf"{100 * M['rate'][-1]:.0f}\% (scale: \ $\times 10$)", font_size=17, color=RATE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        head = label(r"Hyman Minsky: \ stability is destabilizing", font_size=26, color=E.ACCENT).to_edge(UP,
                                                                                                         buff=0.35)
        foot = label(rf"the Island's boom: \ hedge borrowers fall from {100 * h[0]:.0f}\% to {100 * h[-1]:.0f}\%; \ "
                     rf"Ponzi borrowers reach {100 * p[-1]:.0f}\% once the rate rises", font_size=21,
                     color=WHITE).to_edge(DOWN, buff=0.3)
        tag = island_tag(corner=DR, font_size=13)
        dashed = DashedVMobject(rate_line, num_dashes=40)
        with self.voiceover(
            "Hyman Minsky gave the script its economics. His point was that stability breeds instability: after "
            "years without trouble, lenders and borrowers grow bolder. <bookmark mark='a'/> He sorted borrowers "
            "into three kinds. Hedge borrowers' cash flow pays both interest and principal. <bookmark mark='b'/> "
            "Speculative borrowers can pay the interest but must roll over the principal, so they need lenders to "
            "keep lending. <bookmark mark='c'/> Ponzi borrowers cannot pay even the interest, and must borrow more "
            "or sell assets, which works only while asset prices rise. <bookmark mark='d'/> The chart is a boom on "
            "the Island: four thousand borrowers whose debts grow ten percent a year while their incomes grow two, "
            "at an interest rate of three percent. For years almost everyone is a hedge borrower. "
            "<bookmark mark='e'/> Then the rate doubles over three years. <bookmark mark='f'/> The same debts, "
            f"at the new rate, leave only {100 * h[-1]:.0f} percent as hedge borrowers and make "
            f"{100 * p[-1]:.0f} percent Ponzi. Nothing about the borrowers changed in those three years; the boom "
            "had built the fragility, and the rate revealed it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(defs[0]), FadeIn(b_h), run_time=1.2)
            vo.wait_until("b")
            self.play(FadeIn(defs[1]), FadeIn(b_s), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(defs[2]), FadeIn(b_p), run_time=1.2)
            vo.wait_until("d")
            self.play(Indicate(b_h, color=WHITE, scale_factor=1.0), run_time=1.5)
            vo.wait_until("e")
            self.play(Create(dashed), FadeIn(defs[3]), run_time=1.5)
            vo.wait_until("f")
            self.play(FadeIn(foot), Indicate(b_p, color=WHITE))
        self.clear_scene()
