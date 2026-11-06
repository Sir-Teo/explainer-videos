from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs38.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load, trace)


class Nakamoto(VoiceoverScene):
    def construct(self):
        self.card()
        self.chain()
        self.double_spend()
        self.selfish()
        self.stake()

    def card(self):
        card = chapter_card(10, r"Nakamoto consensus", r"Can strangers agree, if anyone can join?", lit=(2008, 2014),
                            extra=((2008, r"Nakamoto: \ Bitcoin"), (2014, r"Eyal and Sirer: \ selfish mining")),
                            part=PART)
        with self.voiceover("Chapter ten. Nakamoto consensus."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def chain(self):
        head = label(r"Votes by computation", font_size=36).to_edge(UP, buff=0.3)
        blocks = VGroup(*[VGroup(RoundedRectangle(width=1.5, height=1.0, corner_radius=0.1, stroke_color=YES,
                                                  stroke_width=2), label(rf"block {i}", font_size=17, color=YES))
                          for i in range(5)]).arrange(RIGHT, buff=0.5).next_to(head, DOWN, buff=0.6)
        links = VGroup(*[Arrow(blocks[i + 1].get_left(), blocks[i].get_right(), buff=0.05, color=GREY_B,
                               stroke_width=2) for i in range(4)])
        fork = VGroup(RoundedRectangle(width=1.5, height=1.0, corner_radius=0.1, stroke_color=NO, stroke_width=2),
                      label(r"block 4$'$", font_size=17, color=NO)).next_to(blocks[4], DOWN, buff=0.4)
        fl = Arrow(fork.get_left(), blocks[3].get_right(), buff=0.05, color=NO, stroke_width=2)
        lines = VGroup(
            wrapped_label(r"BFT needs a list of who is voting; \ with open membership, \ one attacker can be a "
                          r"million voters \ (a \textbf{Sybil} attack)", 12.4, font_size=21, color=WHITE),
            wrapped_label(r"\textbf{proof of work}: \ a block counts only if its hash is below a target, \ found by "
                          r"trying nonces: \ votes are weighted by computing power, \ not identities \ (the hashes "
                          r"of Part 29)", 12.4, font_size=21, color=HEAD),
            wrapped_label(r"\textbf{longest chain}: \ everyone extends the chain with the most work; \ forks resolve "
                          r"as one side pulls ahead; \ a block is trusted once $z$ blocks are built on it", 12.4,
                          font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Every protocol so far assumes we know who the participants are. Byzantine agreement needs at least "
            "three f plus one of them, which presumes counting. <bookmark mark='a'/> On an open network, where "
            "anyone can join, one attacker can pretend to be a million participants. In 2008 the pseudonymous "
            "Satoshi Nakamoto replaced identities with computation. <bookmark mark='b'/> A block of transactions "
            "counts only if its hash, Part 29's SHA-256, falls below a target, which takes on average a fixed "
            "amount of guessing to find. Votes are weighted by computing power, which cannot be faked. "
            "<bookmark mark='c'/> Every block names its predecessor, and everyone extends the chain with the most "
            "work behind it. Two miners may find blocks at once and fork the chain, but one side soon pulls ahead. "
            "A merchant trusts a payment once z blocks are built on top of it."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(b) for b in blocks], lag_ratio=0.15), Create(links))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(fork), GrowArrow(fl), FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def double_spend(self):
        n = load("nakamoto")
        head = label(r"How many confirmations?", font_size=36).to_edge(UP, buff=0.3)
        rows = [[f"{r['q']:g}", f"{r['z']}", f"{r['nakamoto'] * 100:.4g}\\%", f"{r['exact'] * 100:.4g}\\%",
                 f"{r['simulated'] * 100:.4g}\\%"] for r in n["rows"]]
        tab = grid_table([r"attacker share $q$", r"confirmations $z$", r"Nakamoto 2008", r"exact",
                          r"simulated"], rows, widths=[2.4, 2.4, 2.4, 2.0, 2.0], row_h=0.36, font_size=18,
                         mono_cols=())
        tab.next_to(head, DOWN, buff=0.4).set_x(0)
        for k in range(1, len(rows) + 1):
            tab.cells[k][2].set_color(KERN)
            tab.cells[k][3].set_color(YES)
            tab.cells[k][4].set_color(YES)
        need = n["need_0.1pct"]
        lines = VGroup(
            wrapped_label(r"the attacker mines a rival chain in secret, \ then races to overtake: \ a random walk "
                          r"biased against it, \ caught up from $k$ behind with probability $(q/p)^k$", 12.4,
                          font_size=20, color=WHITE),
            wrapped_label(r"Nakamoto approximated the attacker's progress as Poisson; \ the exact count is "
                          r"negative-binomial \ (Rosenfeld, 2014), \ and 200{,}000 simulated races agree with it: \ "
                          r"the paper's numbers are optimistic by up to a factor of six", 12.4, font_size=20,
                          color=KERN),
            wrapped_label(rf"for a 0.1\% risk: \ {need['0.1']} blocks against a 10\% attacker, \ {need['0.3']} "
                          rf"against 30\%, \ {need['0.4']} against 40\%", 12.4, font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(tab, DOWN, buff=0.35)
        with self.voiceover(
            "How safe is a payment with z confirmations? <bookmark mark='a'/> An attacker with a share q of the "
            "computing power mines a rival chain in secret, one that omits the payment, and races to overtake the "
            "honest chain. Each block found is the attacker's with probability q, a random walk biased against it, "
            "and from k blocks behind it ever catches up with probability q over p to the k. "
            "<bookmark mark='b'/> Nakamoto's paper computed the risk with a Poisson approximation. The exact "
            "answer, worked out by Meni Rosenfeld in 2014, uses the negative binomial, and our two hundred "
            "thousand simulated races agree with the exact answer, not the paper's: for a ten percent attacker "
            "and six confirmations, the risk is not two hundredths of a percent but six hundredths. "
            "<bookmark mark='c'/> For a risk of one in a thousand you need six blocks against a ten percent "
            "attacker, thirty-two against thirty percent, a hundred and thirty-three against forty. Safety here "
            "is probabilistic, and it decays exponentially with waiting."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, l in zip("abc", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def selfish(self):
        n = load("nakamoto")
        head = label(r"Selfish mining", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 0.5, 0.1], [0, 0.7, 0.1], x_length=6.4, y_length=4.0, x_label=r"pool's share of hash "
                 r"power $\alpha$", y_label=r"pool's share of blocks", xticks=(0.1, 0.2, 0.3, 0.4, 0.5),
                 yticks=(0.2, 0.4, 0.6), fx=lambda v: f"{v:.1f}", fy=lambda v: f"{v:.1f}").move_to([-2.8, -0.5, 0])
        ax = g.ax
        fair = DashedLine(ax.c2p(0, 0), ax.c2p(0.5, 0.5), color=GREY_B, dash_length=0.1)
        curves = VGroup()
        for gam, c in ((0.0, NO), (0.5, KERN)):
            pts = [(s["alpha"], s["formula"]) for s in n["selfish"] if s["gamma"] == gam]
            dots = VGroup(*[Dot(ax.c2p(s["alpha"], s["simulated"]), radius=0.05, color=c) for s in n["selfish"]
                            if s["gamma"] == gam])
            curves.add(VGroup(trace(ax, pts, c, width=2.6), dots))
        notes = VGroup(
            wrapped_label(r"withhold found blocks; \ publish them only to override the honest chain, \ wasting "
                          r"the honest miners' work", 5.4, font_size=19, color=WHITE),
            wrapped_label(r"lines: \ Eyal and Sirer's formula; \ dots: \ 200{,}000 simulated blocks", 5.4,
                          font_size=18, color=GREY_A),
            wrapped_label(r"profitable above $\alpha = 1/3$ \ (red, \ ties lost), \ and above $1/4$ if half the "
                          r"honest miners build on the pool's block in a tie \ (orange)", 5.4, font_size=19,
                          color=NO),
            wrapped_label(r"so ``honest majority'' is not enough: \ incentives are part of the protocol", 5.4,
                          font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.6, -0.4, 0])
        with self.voiceover(
            "Bitcoin's security argument assumed that a miner's best strategy is to follow the rules. In 2014 "
            "Ittay Eyal and Emin Gün Sirer showed otherwise. <bookmark mark='a'/> A selfish pool keeps the blocks "
            "it finds secret, and publishes them only to override blocks the honest miners find, so the honest "
            "work is wasted. <bookmark mark='b'/> We simulated two hundred thousand blocks at each pool size, and "
            "the results lie on their formula. <bookmark mark='c'/> On the dashed line, revenue equals hash power, "
            "the fair share. The selfish pool rises above it once it has a third of the power, or a quarter if half "
            "the honest miners side with its blocks in a tie. <bookmark mark='d'/> An honest majority is not "
            "enough. In open systems, the incentives are part of the protocol."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), Create(fair))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(curves[0]), Create(curves[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def stake(self):
        head = label(r"The price, \ and proof of stake", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"Bitcoin settles about 7 transactions a second, \ a block every 10 minutes, \ and spends "
                          r"electricity on the scale of a mid-sized country \ (Cambridge estimates, \ 2020s) \ "
                          r"--- \ the cost of voting by computation", 12.4, font_size=24, color=NO),
            wrapped_label(r"\textbf{proof of stake}: \ voting power by deposited currency, \ which a misbehaving "
                          r"validator forfeits \ (``slashing''); \ Ethereum switched in 2022, \ cutting its energy use "
                          r"by over 99.9\%", 12.4, font_size=24, color=YES),
            wrapped_label(r"underneath, \ a BFT protocol again: \ with known validators weighted by stake, \ "
                          r"$n \ge 3f + 1$ returns, \ measured in coins instead of machines", 12.4, font_size=24,
                          color=HEAD),
            wrapped_label(r"finality: \ Nakamoto's is probabilistic and grows with waiting; \ BFT's is absolute "
                          r"once a quorum signs", 12.4, font_size=24, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Open membership has a price. <bookmark mark='a'/> Bitcoin settles about seven transactions a second, "
            "one block every ten minutes, and its miners consume electricity on the scale of a mid-sized country: "
            "the cost of voting by computation. <bookmark mark='b'/> Proof of stake weights votes instead by "
            "currency deposited, which a validator caught signing conflicting blocks forfeits. Ethereum switched "
            "in 2022 and cut its energy use by more than ninety-nine point nine percent. "
            "<bookmark mark='c'/> Underneath, proof-of-stake chains run a Byzantine agreement protocol among their "
            "validators, and the bound of three f plus one returns, counted in coins rather than machines. "
            "<bookmark mark='d'/> The difference that remains is finality: Nakamoto's chain is only ever probably "
            "final, more so the longer you wait; a BFT decision is final the moment a quorum signs it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, math)
