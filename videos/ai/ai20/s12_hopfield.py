from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai20.common import (DATA, EBM, HIST, PART, curve, digit, digit_sheet, load, node_box, rgb_of, to_image)


def spins(s, size=1.6) -> ImageMobject:
    """A 14 x 14 state of +-1 neurons as a picture: +1 bright, -1 dark."""
    a = (np.asarray(s, float).reshape(14, 14) + 1) / 2
    return digit(a, size, color=EBM)


class Hopfield(VoiceoverScene):
    def construct(self):
        self.card()
        self.energy()
        self.recall()
        self.capacity()
        self.modern()
        self.boltzmann()

    def card(self):
        card = chapter_card(11, r"Hopfield and Boltzmann", r"Can a memory be the bottom of a valley?",
                            lit=(1949, 1982), part=PART)
        with self.voiceover("Chapter eleven. Hopfield and Boltzmann."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def energy(self):
        h = load("hopfield")
        rows = [
            cmath(r"E(s)", r"=", r"-\tfrac12 \sum_{i \ne j} W_{ij}\, s_i s_j, \qquad s_i = \pm 1, \ W_{ij} = W_{ji}",
                  font_size=34),
            cmath(r"s_i", r"\leftarrow", r"\operatorname{sign}\big(h_i\big), \qquad h_i = \sum_j W_{ij} s_j",
                  font_size=34),
            cmath(r"\Delta E", r"=", r"-\,\Delta s_i\; h_i", r"\;\le\; 0", font_size=36),
            cmath(r"W", r"=", r"\frac{1}{N} \sum_\mu \xi^\mu \xi^{\mu\top}", font_size=36),
        ]
        rows[0][0].set_color(EBM)
        rows[2][0].set_color(EBM)
        whys = [why(r"an energy over binary neurons"), why(r"update one neuron at a time"),
                why(r"$\Delta s_i$ has the sign of $h_i$: \ $E$ never rises"),
                why(r"Hebb's rule (1949): \ store patterns $\xi^\mu$")]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-1.6, buff=0.45, edge=6.9)
        card = history_card(1982, r"John Hopfield", r"\textit{Neural networks and physical systems with emergent "
                            r"collective computational abilities}", width=5.6, font_size=20).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The fifth answer is the oldest. In 1982 the physicist John Hopfield gave a network of plus-or-minus-one "
            "neurons, with symmetric connections, an energy. <bookmark mark='a'/> One neuron at a time takes the "
            "sign of its input. <bookmark mark='b'/> A flip changes the energy by minus the flip times the input, "
            "and the two agree in sign, so the energy only falls: the network settles into a valley. <bookmark "
            "mark='c'/> Hebb's rule, from Part 9, makes chosen patterns the valleys: a memory, stored as the bottom "
            "of a landscape."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.1))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recall(self):
        h = load("hopfield")
        Xd = np.asarray(h["digits"])
        frames = np.asarray(h["frames"])
        en = np.asarray(h["energy"])
        stored = spins(Xd[int(h["recall_digit"])], 1.3).move_to([-5.6, 2.1, 0])
        sl = label(r"stored: \ one digit", font_size=22, color=EBM).next_to(stored, RIGHT, buff=0.2)
        big = [spins(f, 3.0).move_to([-3.6, -1.0, 0]) for f in frames]
        cl = label(r"the state, \ update by update", font_size=22, color=GREY_A).next_to(big[0], DOWN, buff=0.15)
        g = axes([0, len(en) - 1], [float(en.min()) * 1.05, float(en.max()) + 5], x_length=5.0, y_length=3.0,
                 xlabel=r"updates (in steps of $14$)", ylabel=r"energy $E(s)$", xticks=[0, len(en) - 1], yticks=[],
                 center=[3.2, -0.6, 0])
        ec = curve(g.ax, np.arange(len(en)), en, EBM, 3)
        dot = Dot(g.ax.c2p(0, en[0]), color=EBM)
        ov = float(h["final_overlap"])
        res = (f"It settles on the stored digit exactly." if ov > 0.999 else
               f"It settles on a state that matches the stored digit on {100 * (1 + ov) / 2:.0f} percent of "
               "pixels.")
        with self.voiceover(
            "Here is one: 196 neurons, one per pixel, one digit stored. <bookmark mark='a'/> Start from that digit "
            "with a quarter of its pixels flipped. <bookmark mark='b'/> Neuron by neuron the state slides "
            f"downhill, the energy falling with every change. <bookmark mark='c'/> {res} A damaged copy is enough "
            "to find the memory."
        ) as vo:
            self.play(FadeIn(stored), FadeIn(sl))
            vo.wait_until("a")
            self.play(FadeIn(big[0]), FadeIn(cl), FadeIn(g), FadeIn(dot))
            vo.wait_until("b")
            cur = big[0]
            per = max(0.15, (vo.until("c") - 0.5) / max(1, len(big) - 1))
            for k in range(1, len(big)):
                nb = big[k]
                self.remove(cur)
                self.add(nb)
                self.play(dot.animate.move_to(g.ax.c2p(k, en[k])), run_time=per)
                cur = nb
            self.play(Create(ec))
            vo.wait_until("c")
            self.play(Indicate(stored, color=EBM, scale_factor=1.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def capacity(self):
        h = load("hopfield")
        N = int(h["N"])
        Ps = np.asarray(h["Ps"], float)
        fr = np.asarray(h["recall_random"])
        g = axes([0, Ps[-1] / N], [0, 1], x_length=5.0, y_length=3.0, xlabel=r"patterns per neuron, \ $P / N$",
                 ylabel=r"share recalled exactly", xticks=[0, 0.1, 0.2, 0.3], yticks=[0, 0.5, 1],
                 center=[-3.4, 0.4, 0])
        rc = curve(g.ax, Ps / N, fr, EBM, 3)
        pd = VGroup(*[Dot(g.ax.c2p(a, b), radius=0.05, color=EBM) for a, b in zip(Ps / N, fr)])
        th = DashedLine(g.ax.c2p(0.138, 0), g.ax.c2p(0.138, 1), color=C.BITS, stroke_width=2)
        tl = label(r"$0.138$: \\ Amit, Gutfreund \& Sompolinsky (1985)", font_size=18, color=C.BITS)
        tl.next_to(g.ax.c2p(0.138, 0.8), RIGHT, buff=0.1)
        half = float(Ps[np.argmax(fr < 0.5)] / N) if (fr < 0.5).any() else float(Ps[-1] / N)
        hb, hm = np.asarray(h["recall_hebb"]), np.asarray(h["recall_modern"])
        k = np.arange(1, len(hb) + 1)
        g2 = axes([1, len(hb)], [0, 1], x_length=4.6, y_length=2.4, xlabel=r"digits stored", ylabel=r"share recalled",
                  xticks=[1, 5, 10], yticks=[0, 1], center=[3.3, 1.2, 0])
        ch, cm = curve(g2.ax, k, hb, EBM, 3), curve(g2.ax, k, hm, C.MODEL_Q, 3)
        lg = legend([(EBM, r"Hebb's rule"), (C.MODEL_Q, r"softmax update (modern)")], font_size=18)
        lg.next_to(g2, UP, buff=0.1).align_to(g2, LEFT)
        mix = spins(np.asarray(h["mixture"]), 2.0).move_to([2.0, -2.2, 0])
        ml = label(r"$6$ digits stored: \\ a cue lands in a blend", font_size=20, color=GREY_A).next_to(mix, RIGHT,
                                                                                                     buff=0.25)
        fails = (hb < 1.0).any()
        n_fail = int(np.argmax(hb < 1.0)) + 1 if fails else len(hb)
        hebb_s = (f"Hebb's rule already fails at {n_fail} stored digits, and cues slide into blends of memories."
                  if fails else "Even so, all ten come back here; with more, valleys merge into blends.")
        ov = np.asarray(h["overlap"])
        mean_ov = float(np.abs(ov[np.triu_indices(10, 1)]).mean())
        with self.voiceover(
            "How much can it hold? Store random patterns, recall each from a damaged copy. <bookmark mark='a'/> "
            f"With {N} neurons, fewer than half come back once there are {half:.2f} patterns per neuron; Amit, "
            "Gutfreund and Sompolinsky's spin-glass theory puts the limit at about 0.138. <bookmark mark='b'/> "
            f"Digits look alike, overlapping by {mean_ov:.2f} on average, which is worse. " + hebb_s
        ) as vo:
            self.play(FadeIn(g), FadeIn(pd))
            vo.wait_until("a")
            self.play(Create(rc), Create(th), FadeIn(tl))
            vo.wait_until("b")
            self.play(FadeIn(g2), FadeIn(lg[0]), Create(ch), FadeIn(mix), FadeIn(ml))
        self.wait(0.3)
        self.modern_curve = (g2, cm, lg)
        self.left_ = Group(g, rc, pd, th, tl, mix, ml)

    # ------------------------------------------------------------------
    def modern(self):
        h = load("hopfield")
        g2, cm, lg = self.modern_curve
        hm = np.asarray(h["recall_modern"])
        f = cmath(r"s_{\text{new}}", r"=", r"X^\top \operatorname{softmax}\big(\beta\, X s\big)", font_size=36)
        f[2].set_color(C.MODEL_Q)
        f.move_to([-3.2, 2.0, 0])
        att = cmath(r"\operatorname{softmax}\big(q K^\top / \sqrt d\big)\, V", font_size=32, color=C.ATTN)
        att.next_to(f, DOWN, buff=0.5)
        al = label(r"attention (Part 13): \ the state is the query, \ the memories are keys and values",
                   font_size=20, color=C.ATTN).next_to(att, DOWN, buff=0.15)
        al.set_x(-3.0)
        hist = VGroup(label(r"Krotov \& Hopfield (2016): \ dense associative memory", font_size=20, color=GREY_A),
                      label(r"Ramsauer et al.\ (2020): \ \textit{Hopfield Networks is All You Need}", font_size=20,
                            color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([-3.2, -1.6, 0])
        allok = bool((hm >= 1.0).all())
        hb = np.asarray(h["recall_hebb"])
        k_ok = int(np.argmax(hm < 1.0)) if not allok else len(hm)  # every digit recalled with up to k_ok stored
        k_h = int(np.argmax(hb < 1.0)) if (hb < 1.0).any() else len(hb)
        if allok:
            res = "recalls all ten digits from the same damaged cues"
        else:
            res = (f"recalls every digit with up to {k_ok} stored, where Hebb's rule managed {k_h}, and "
                   f"{100 * hm[-1]:.0f} percent of them with all ten stored")
        with self.voiceover(
            "The fix came over thirty years later: Dmitry Krotov and Hopfield sharpened the energy, and Hubert "
            "Ramsauer and colleagues wrote the update as compare, softmax, average. <bookmark mark='a'/> With it, "
            f"our network {res}. <bookmark mark='b'/> That update is attention, from Part 13: the state the query, "
            "the memories the keys and values. An attention layer is a Hopfield network taking one step."
        ) as vo:
            self.play(FadeOut(self.left_))
            self.play(Write(f))
            vo.wait_until("a")
            self.play(FadeIn(lg[1]), Create(cm))
            vo.wait_until("b")
            self.play(Write(att), FadeIn(al), FadeIn(hist))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def boltzmann(self):
        vis = VGroup(*[Circle(0.22, stroke_color=DATA, stroke_width=2, fill_color=DATA, fill_opacity=0.25)
                       for _ in range(5)]).arrange(RIGHT, buff=0.35).move_to([-4.0, -1.0, 0])
        hid = VGroup(*[Circle(0.22, stroke_color=EBM, stroke_width=2, fill_color=EBM, fill_opacity=0.25)
                       for _ in range(4)]).arrange(RIGHT, buff=0.45).move_to([-4.0, 0.8, 0])
        edges = VGroup()
        allu = list(vis) + list(hid)
        for i in range(len(allu)):
            for j in range(i + 1, len(allu)):
                if (i + j) % 3 == 0 or (allu[i] in hid) != (allu[j] in hid):
                    edges.add(Line(allu[i].get_center(), allu[j].get_center(), stroke_width=1, color=GREY_C)
                              .set_opacity(0.5))
        vl = label(r"visible units", font_size=20, color=DATA).next_to(vis, DOWN, buff=0.15)
        hl = label(r"hidden units", font_size=20, color=EBM).next_to(hid, UP, buff=0.15)
        VGroup(edges, vis, hid, vl, hl).scale(1.35).move_to([-3.9, -0.2, 0])
        rows = VGroup(
            cmath(r"p(s)", r"=", r"\frac{e^{-E(s)/T}}{Z}", font_size=36),
            cmath(r"\Delta W_{ij}", r"\propto", r"\langle s_i s_j \rangle_{\text{data}}", r"-",
                  r"\langle s_i s_j \rangle_{\text{model}}", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([2.6, 2.2, 0])
        rows[1][2].set_color(DATA)
        rows[1][4].set_color(EBM)
        rl = VGroup(label(r"positive phase: \ clamp the data, \ measure correlations", font_size=20, color=DATA),
                    label(r"negative phase: \ let it dream, \ measure them again", font_size=20, color=EBM))
        rl.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(rows, DOWN, buff=0.25)
        card = history_card(1985, r"Ackley, Hinton \& Sejnowski: \ the Boltzmann machine", r"stochastic neurons, "
                            r"hidden units, \ and a learning rule from statistical physics", width=6.2, font_size=20)
        card.move_to([2.7, -1.0, 0])
        nobel = history_card(2024, r"Nobel Prize in Physics: \ John Hopfield and Geoffrey Hinton",
                             r"``for foundational discoveries and inventions that enable machine learning with "
                             r"artificial neural networks''", width=6.2, font_size=20, color=C.BITS)
        nobel.move_to([2.7, -2.7, 0])
        with self.voiceover(
            "In 1985 David Ackley, Geoffrey Hinton and Terrence Sejnowski made the neurons random, so the network "
            "samples the Boltzmann distribution of physics: e to the minus energy over temperature, over a "
            "normalizer Z. <bookmark mark='a'/> They added hidden units: the machine's own features. <bookmark "
            "mark='b'/> The learning rule: measure how often pairs of units are on together with the data clamped, "
            "again running free, and strengthen each connection by the difference, until the machine's dreams "
            "match the world. <bookmark mark='c'/> The catch: each measurement needs equilibrium, which can take "
            "forever. <bookmark mark='d'/> In 2024 Hopfield and Hinton shared the Nobel Prize in Physics, for "
            "foundational discoveries and inventions that enable machine learning with artificial neural networks."
        ) as vo:
            self.play(FadeIn(vis), FadeIn(vl), FadeIn(hid), FadeIn(hl), Create(edges), Write(rows[0]))
            vo.wait_until("a")
            self.play(Indicate(hid, color=EBM))
            vo.wait_until("b")
            self.play(Write(rows[1]), FadeIn(rl))
            vo.wait_until("c")
            self.play(FadeIn(card, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(nobel, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
