from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs36.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, graph, grid_table, load)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.verify()
        self.innetwork()
        self.gadget()
        self.open_problems()

    def card(self):
        card = chapter_card(15, r"Frontier: \ programmable, \ verified, \ convergent", r"What is still unsolved?",
                            lit=(2002, 2012, 2015), extra=((2002, r"Griffin et al.: \ the stable paths problem"),
                                                           (2012, r"header space analysis"), (2015, r"Batfish")),
                            part=PART)
        with self.voiceover("Chapter fifteen. Frontier: programmable, verified, convergent."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def verify(self):
        f = load("frontier")
        head = label(r"Verifying the data plane", font_size=36).to_edge(UP, buff=0.3)
        vm, va = f["verify_mid"], f["verify_after"]
        rows = [[r"mid-update \ (Amsterdam and Frankfurt new, \ London and Paris old)", str(vm["checked"]),
                 str(len(vm["loops"])), str(vm["black_holes"])],
                [r"after convergence", str(va["checked"]), str(va["loops"]), str(va["black_holes"])]]
        tab = grid_table([r"our internet's tables", r"(prefix, router) pairs", r"loops", r"black holes"], rows,
                         widths=[6.2, 2.6, 1.2, 1.8], row_h=0.48, font_size=19, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        tab.cells[1][2].set_color(NO)
        tab.cells[2][2].set_color(YES)
        arrow = r" $\leftrightarrow$ "
        found = label(r"found, \ without sending a packet: \ " + r"; \ ".join(
            rf"\texttt{{{p}}} loops {arrow.join(c)}" for p, c in vm["loops"]), font_size=19,
            color=NO).next_to(tab, DOWN, buff=0.3)
        lines = VGroup(
            label(r"testing sends some packets; \ \textbf{verification} reasons about \textit{all} of them, \ from "
                  r"the forwarding tables themselves", font_size=20, color=WHITE),
            label(r"header space analysis \ (Kazemian et al., 2012): \ treat a packet's header bits as a space, \ "
                  r"and each rule as a function on it", font_size=20, color=HEAD),
            label(r"Batfish \ (2015) \ and its successors check whole configurations before they are deployed; \ "
                  r"clouds now verify every change", font_size=20, color=YES),
            label(r"in the worst case exponential in the header's bits; \ equivalence classes of headers make it fast "
                  r"in practice", font_size=20, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "The first frontier is knowing a network is right. <bookmark mark='a'/> Testing sends packets and sees "
            "what happens; verification reasons about every possible packet, directly from the forwarding tables. "
            "<bookmark mark='b'/> Our verifier follows every prefix from every router through the tables. On a "
            "snapshot taken halfway through chapter thirteen's reconvergence, it finds the London-Amsterdam loop, for "
            "two prefixes, without sending a packet; after convergence, nothing. <bookmark mark='c'/> Header space "
            "analysis, in 2012, made this general: a header is a point in a space of bits, and every rule a function "
            "on that space. <bookmark mark='d'/> Tools like Batfish now check entire configurations before they are "
            "deployed, and large clouds verify every change. <bookmark mark='e'/> The worst case is exponential in "
            "the number of header bits; what makes it fast in practice, and how to verify networks whose rules "
            "change every second, are open."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab), FadeIn(found))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
            vo.wait_until("e")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def innetwork(self):
        head = label(r"Computing inside the network", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            label(r"\textbf{in-band telemetry}: \ each P4 switch appends its queue depth and a timestamp to the packet; "
                  r"\ the receiver sees the path's congestion, \ hop by hop", font_size=20, color=WHITE),
            label(r"\textbf{NetCache} \ (Jin et al., 2017): \ a key-value cache in the switch itself, \ answering hot "
                  r"keys at billions of queries a second", font_size=20, color=HEAD),
            label(r"\textbf{in-network aggregation} \ (SwitchML, 2021): \ switches sum the gradients of distributed "
                  r"training as they pass \ (AI, Built)", font_size=20, color=YES),
            label(r"the open questions: \ what a switch's few megabytes and fixed pipeline can compute, \ and how to "
                  r"verify it", font_size=20, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.6)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "Once switches are programmable, they can do more than forward. <bookmark mark='a'/> In-band telemetry "
            "has every switch append its queue depth and a timestamp to passing packets, so the receiver sees, hop "
            "by hop, where congestion is. <bookmark mark='b'/> NetCache put a small key-value cache inside the switch, "
            "answering the hottest keys at billions of queries a second before they reach a server. "
            "<bookmark mark='c'/> And switches can sum the gradients of distributed machine learning as they pass "
            "through. <bookmark mark='d'/> What a pipeline with a few megabytes of memory and a fixed number of "
            "stages can compute, and how to verify it, are open."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def gadget(self):
        f = load("frontier")
        head = label(r"Policies that never settle", font_size=36).to_edge(UP, buff=0.3)
        pos = {0: [-3.6, -1.5, 0], 1: [-3.6, 1.4, 0], 2: [-1.2, -0.2, 0], 3: [-6.0, -0.2, 0]}
        g = graph(pos, [(0, 1), (0, 2), (0, 3), (1, 2), (2, 3), (3, 1)], node_color=HEAD, r=0.32)
        prefs = VGroup(*[label(t, font_size=18, color=GREY_A) for t in (
            r"1 prefers \ 1 2 0 \ over \ 1 0", r"2 prefers \ 2 3 0 \ over \ 2 0", r"3 prefers \ 3 1 0 \ over \ 3 0")])
        prefs.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(g, DOWN, buff=0.4)
        hist = f["bad"]
        rows = []
        for k, h in enumerate(hist[:7]):
            rows.append([str(k)] + [(" ".join(map(str, h[str(v)])) if h[str(v)] else "--") for v in (1, 2, 3)])
        tab = grid_table([r"round", r"node 1", r"node 2", r"node 3"], rows, widths=[1.2, 1.6, 1.6, 1.6], row_h=0.38,
                         font_size=18, mono_cols=(1, 2, 3))
        tab.move_to([3.4, 0.8, 0])
        lines = VGroup(
            label(r"\textbf{BAD GADGET} \ (Griffin, \ Shepherd and Wilfong, \ 2002): \ each AS prefers the route "
                  r"through its neighbour", font_size=19, color=WHITE),
            label(r"every choice makes another's choice impossible: \ the routes oscillate for ever", font_size=19,
                  color=NO),
            label(r"deciding whether a set of policies has a stable solution is NP-complete; \ Gao--Rexford's "
                  r"economics is a sufficient condition, \ not a necessary one", font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.35)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "The second frontier is convergence. <bookmark mark='a'/> Here are three systems around a destination. "
            "Each would rather reach it through its clockwise neighbour than directly. <bookmark mark='b'/> Start "
            "with everyone going direct. Each then sees its preferred route available and switches to it; but now "
            "each neighbour's route is indirect, so the preferred routes no longer exist, and all switch back. "
            "Our simulation cycles for ever. <bookmark mark='c'/> Timothy Griffin, Bruce Shepherd and Gordon Wilfong "
            "called this BAD GADGET, and proved that deciding whether arbitrary policies have any stable solution is "
            "NP-complete. The Gao-Rexford rules avoid it, but real policies are messier, and the guarantee is open."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(prefs), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def open_problems(self):
        head = label(r"Open problems", font_size=36).to_edge(UP, buff=0.3)
        probs = VGroup(*[label(t, font_size=21, color=WHITE) for t in (
            r"1. \ Verifying networks whose forwarding rules change thousands of times a second",
            r"2. \ Updating a network's tables in an order that never loops or black-holes, \ as fast as possible",
            r"3. \ Securing BGP's paths, \ not just its origins, \ in a way that can be deployed piecemeal",
            r"4. \ Inter-domain routing with guaranteed convergence under realistic policies",
            r"5. \ Programmable data planes that are verified as well as fast",
            r"6. \ Getting closer to Shannon and MIMO limits in crowded, \ moving radio channels",
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.8)
        star = label(r"$\bigstar$ \ the part's research problem asks for a safe order of table updates after a link "
                     r"fails", font_size=19, color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Six problems at the frontier. <bookmark mark='a'/> Verifying networks whose rules change thousands of "
            "times a second. <bookmark mark='b'/> Updating every router's table in an order that never loops or "
            "drops traffic, and as quickly as possible. <bookmark mark='c'/> Securing BGP's paths, not only their "
            "origins, in a way that helps even when only some networks adopt it. <bookmark mark='d'/> Routing between "
            "networks with convergence guaranteed under the policies networks actually use. <bookmark mark='e'/> "
            "Programmable switches that are verified as well as fast. <bookmark mark='f'/> And radio that comes "
            "closer to its limits in crowded, moving channels. The research problem at the end of this part asks "
            "for the second in its simplest form: after one link fails, in what order should routers change their "
            "tables so that no packet ever loops?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcdef", probs):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()


_ = (DATA, LAM, YES)
