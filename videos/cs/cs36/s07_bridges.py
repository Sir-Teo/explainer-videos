from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs36.common import (DATA, ETH, HEAD, KERN, LAM, NO, PART, YES, graph, load, num)

POS = {1: [-4.6, 1.6, 0], 2: [-2.4, 1.6, 0], 3: [-4.6, -0.4, 0], 4: [-2.4, -0.4, 0], 5: [-3.5, -1.8, 0]}


class Bridges(VoiceoverScene):
    def construct(self):
        self.card()
        self.storm()
        self.stp()
        self.learning()

    def card(self):
        card = chapter_card(6, r"Bridges and switches", r"How do you join links without loops killing you?",
                            lit=(1985,), extra=((1985, r"Perlman: \ the spanning tree"),), part=PART)
        with self.voiceover("Chapter six. Bridges and switches."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def storm(self):
        b = load("bridges")
        head = label(r"A loop, \ and one broadcast", font_size=36).to_edge(UP, buff=0.3)
        g = graph(POS, [(l["a"], l["b"]) for l in b["links"]], node_color=ETH)
        counts = b["storm"]
        ax = Axes(x_range=[0, len(counts), 2], y_range=[0, 6, 1], x_length=6.0, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).move_to([3.2, 0.0, 0])
        bars = VGroup()
        import math
        for k, c in enumerate(counts):
            h = ax.c2p(0, math.log10(max(c, 1)))[1] - ax.c2p(0, 0)[1]
            r = Rectangle(width=0.22, height=max(h, 0.02), stroke_width=0, fill_color=NO, fill_opacity=0.85)
            r.move_to(ax.c2p(k + 0.5, 0), aligned_edge=DOWN)
            bars.add(r)
        yt = VGroup(*[MathTex(rf"10^{{{y}}}", font_size=17, color=GREY_B).next_to(ax.c2p(0, y), LEFT, buff=0.1)
                      for y in range(0, 7, 2)])
        xl = label(r"hop", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.1)
        yl = label(r"copies in flight", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        lines = VGroup(
            label(r"a bridge forwards a broadcast out of every port but the one it came in on", font_size=20,
                  color=WHITE),
            label(rf"with loops, \ copies multiply: \ {num(b['storm_sent'])} frames sent within 20 hops, \ and it "
                  r"never stops: \ Ethernet frames have no hop limit", font_size=20, color=NO),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Ethernets grew by joining segments with bridges, now called switches. Connect them with spare links for "
            "redundancy, and the network has loops. <bookmark mark='a'/> A bridge that does not know where a "
            "destination is sends the frame out of every port except the one it arrived on, and a broadcast always "
            "goes everywhere. <bookmark mark='b'/> In a loop, each copy comes back around and is copied again. In our "
            "five-bridge network one broadcast becomes more than a million frames within twenty hops, and nothing "
            "stops it: unlike IP packets, Ethernet frames carry no hop count. This is a broadcast storm, and it "
            "brings a network down in seconds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), *[Indicate(e, color=NO) for e in g.edges.values()])
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in bars], lag_ratio=0.1), FadeIn(lines[1]),
                      run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    def stp(self):
        b = load("bridges")
        head = label(r"Perlman's spanning tree", font_size=36).to_edge(UP, buff=0.3)
        g = graph(POS, [(l["a"], l["b"]) for l in b["links"]], node_color=ETH)
        crown = label(r"root", font_size=17, color=YES).next_to(g.nodes[b["root"]], UP, buff=0.08)
        poem = VGroup(*[label(t, font_size=19, color=GREY_A, ) for t in (
            r"\textit{I think that I shall never see}", r"\textit{a graph more lovely than a tree.}",
            r"\textit{A tree whose crucial property}", r"\textit{is loop-free connectivity.}",
            r"\ \ --- Radia Perlman, \ \textit{Algorhyme}")]).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        poem.move_to([3.4, 1.6, 0])
        lines = VGroup(
            label(r"each bridge believes: \ (root, \ cost to it, \ via whom); \ it hears its neighbours, \ and keeps "
                  r"the best offer", font_size=20, color=WHITE),
            label(rf"the lowest ID wins the root; \ each bridge keeps one port towards it; \ "
                  rf"{sum(not l['active'] for l in b['links'])} links blocked \ (converged in {b['rounds']} rounds)", font_size=20, color=HEAD),
            label(r"now the broadcast reaches each host exactly once, \ in 8 frames, \ and ends", font_size=20,
                  color=YES),
            label(r"when a link fails, \ the tree is recomputed: \ seconds in 1985, \ under one in RSTP; \ VLANs run "
                  r"several logical LANs on one", font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.4)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "Radia Perlman, at Digital Equipment in 1985, found the cure, and wrote it up as a poem. "
            "<bookmark mark='a'/> Each bridge keeps a belief: which bridge is the root, how far away it is, and "
            "through which neighbour. Bridges tell their neighbours their beliefs, and each adopts the best offer "
            "it hears: the lowest root, then the shortest distance. <bookmark mark='b'/> The bridge with the lowest "
            "identifier becomes the root; every other bridge keeps one port towards it, and ports on any other "
            "loop-forming link are blocked. The links that stay active form a spanning tree. "
            "<bookmark mark='c'/> Now the broadcast crosses each tree link once, reaches each host once, and stops. "
            "<bookmark mark='d'/> When a link fails, the bridges recompute the tree, and a blocked port wakes up."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(poem))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            anims = [FadeIn(crown)]
            for l in b["links"]:
                e = g.edges[tuple(sorted((l["a"], l["b"])))]
                anims.append(e.animate.set_color(YES if l["active"] else NO).set_stroke(width=4 if l["active"] else 1.5,
                                                                                         opacity=1 if l["active"] else 0.5))
            self.play(*anims, FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def learning(self):
        b = load("bridges")
        head = label(r"Learning where everyone is", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup()
        for (src, dst), c in zip(b["frames"], b["copies"]):
            rows.add(VGroup(label(rf"\texttt{{{src}}} $\rightarrow$ \texttt{{{dst}}}", font_size=22, color=DATA),
                            label(rf"{c} frame copies", font_size=22, color=YES if c <= 3 else NO)).arrange(
                RIGHT, buff=0.8))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(head, DOWN, buff=0.6)
        lines = VGroup(
            label(r"a switch notes the \textit{source} address of every frame, \ and the port it came in on", font_size=20,
                  color=WHITE),
            label(r"to an unknown destination, \ flood along the tree; \ to a known one, \ one port", font_size=20,
                  color=HEAD),
            label(r"after one reply, \ traffic follows the shortest tree path, \ and other hosts never see it",
                  font_size=20, color=YES),
            label(r"no configuration at all: \ plug and play, \ which is why Ethernet won the building", font_size=20,
                  color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Bridges also learn. <bookmark mark='a'/> Each one notes the source address of every frame it sees and "
            "the port it arrived on. <bookmark mark='b'/> A frame for an address it has never seen is flooded along the "
            "tree; a frame for an address it has learned goes out of one port only. <bookmark mark='c'/> The first "
            "frame from Ana to Ben costs seven copies. Ben's reply costs three, and after that, so does every frame "
            "between them, and the rest of the network never sees them. <bookmark mark='d'/> None of this needs "
            "configuring. Plug in a switch and it works, which is a large part of why Ethernet won."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()


_ = (KERN,)
