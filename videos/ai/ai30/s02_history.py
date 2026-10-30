from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai30.common import CAUSE, FEAT, MONO, PART, PROBE, load, show

SAL = C.TRUE_P
OCC = C.SURPRISE


def char_row(text, width, y, font_size=22):
    n = len(text)
    step = width / n
    return VGroup(*[data_text(show(c), font=MONO, font_size=font_size, color=GREY_A).move_to([-width / 2 + step * (i + 0.5), y, 0])
                    for i, c in enumerate(text)]), step


def signed_bars(v, xs, y0, hmax, color, up=True):
    v = np.nan_to_num(np.asarray(v, float))
    top = max(np.abs(v).max(), 1e-9)
    g = VGroup()
    for x, a in zip(xs, v):
        h = max(abs(a) / top * hmax, 0.01)
        sgn = 1 if (a >= 0) == up else -1
        g.add(Rectangle(width=0.16, height=h, stroke_width=0, fill_color=color,
                        fill_opacity=0.9 if a >= 0 else 0.45).move_to([x, y0 + sgn * h / 2, 0]))
    return g


class History(VoiceoverScene):
    def construct(self):
        self.card()
        self.saliency()
        self.sanity()
        self.pictures()
        self.circuits()

    def card(self):
        card = chapter_card(1, r"How we got here", r"Which inputs mattered, and what is a neuron for?", part=PART)
        with self.voiceover("Chapter one. How we got here."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def saliency(self):
        s = load("saliency")
        text = str(s["prompt"])
        sal, occ = np.asarray(s["saliency"]), np.asarray(s["occlusion"])
        row, step = char_row(text, 12.6, 0.0)
        xs = [c.get_x() for c in row]
        sb = signed_bars(sal, xs, 0.35, 1.5, SAL, up=True)
        ob = signed_bars(occ, xs, -0.35, 1.5, OCC, up=False)
        nxt = label(rf"next: \ `{s['target']}' \ (${100 * float(s['p_target']):.0f}\%$)", font_size=26, color=WHITE)
        nxt.to_edge(UP, buff=0.35).shift(RIGHT * 3.5)
        sl = label(r"saliency: \ gradient $\times$ input", font_size=24, color=SAL).to_corner(UL, buff=0.35)
        f1 = cmath(r"s_i = \frac{\partial z}{\partial e_i} \cdot e_i", font_size=30, color=SAL).next_to(sl, DOWN, buff=0.15)
        f1.align_to(sl, LEFT)
        ol = label(r"occlusion: \ blank one character, \ watch the score", font_size=24, color=OCC).to_corner(DL, buff=0.35)
        f2 = cmath(r"o_i = z - z_{\,\text{character } i \text{ blanked}}", font_size=30, color=OCC).next_to(ol, UP, buff=0.15)
        f2.align_to(ol, LEFT)
        h1 = history_card(2013, r"K.~Simonyan, A.~Vedaldi \& A.~Zisserman", r"saliency maps: \ which pixels the class "
                          r"score is most sensitive to", width=5.6, color=SAL, font_size=20).move_to([0, 2.0, 0])
        h2 = history_card(2014, r"M.~Zeiler \& R.~Fergus", r"occlusion: \ cover part of the image, \ see what the "
                          r"network loses", width=5.6, color=OCC, font_size=20).move_to([0, -2.0, 0])
        rho = float(s["rho_occ_demo"])
        rho24 = float(np.mean(s["rho_occ"]))
        agree = ("roughly agree" if rho24 > 0.6 else "only partly agree" if rho24 > 0.3 else "barely agree")
        with self.voiceover(
            "The first question people asked of a trained network was the simplest: which parts of the input "
            "mattered? <bookmark mark='a'/> In 2013 Karen Simonyan, Andrea Vedaldi and Andrew Zisserman took the "
            "gradient of a class score with respect to the pixels: a saliency map. Here it is for our character "
            f"transformer, about to write '{s['target']}' after 'she sai'. <bookmark mark='b'/> Each bar is the "
            "gradient times the input, the first-order guess of what each character contributes. "
            "<bookmark mark='c'/> A blunter test, from Matthew Zeiler and Rob Fergus a year later: blank out one "
            "character at a time, and measure how far the score drops. <bookmark mark='d'/> If both told the truth "
            f"they would agree. Ranked, they {agree}: a correlation of {rho:.2f} here, and {rho24:.2f} on average "
            "over 24 more predictions. The gradient is a local slope; the network is not a straight line."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c) for c in row], lag_ratio=0.02), FadeIn(nxt), run_time=1.2)
            vo.wait_until("a")
            self.play(FadeIn(h1, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(h1), FadeIn(sl), Write(f1))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in sb], lag_ratio=0.03), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(h2, shift=LEFT * 0.2))
            self.play(FadeOut(h2), FadeIn(ol), Write(f2))
            self.play(LaggedStart(*[GrowFromEdge(b, UP) for b in ob], lag_ratio=0.03), run_time=2)
            vo.wait_until("d")
            r_ = label(rf"rank correlation: \ ${rho:.2f}$ \ (here), \ ${rho24:.2f}$ \ (24 more)", font_size=26,
                       color=GREY_A).to_edge(RIGHT, buff=0.4).shift(UP * 2.2)
            self.play(FadeIn(r_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sanity(self):
        s = load("saliency")
        text = str(s["prompt"])
        casc = np.abs(np.asarray(s["cascade"]))
        rho = [float(r) for r in s["rho_cascade"]]
        names = [r"trained", r"block $4$ re-randomized", r"blocks $3$--$4$", r"blocks $2$--$4$", r"all four blocks",
                 r"and the embedding"]
        W = 7.6
        rows = VGroup()
        for i in range(len(casc)):
            v = casc[i] / max(casc[i].max(), 1e-9)
            n = len(v)
            bar = VGroup(*[Rectangle(width=W / n * 0.8, height=max(0.5 * a, 0.01), stroke_width=0, fill_color=SAL,
                                     fill_opacity=0.9).move_to([-W / 2 + W / n * (j + 0.5), 0.25 * a, 0], aligned_edge=ORIGIN)
                           for j, a in enumerate(v)])
            for j, b in enumerate(bar):
                b.move_to([-W / 2 + W / n * (j + 0.5), b.height / 2, 0])
            nm = label(names[i], font_size=20, color=GREY_A).next_to([-W / 2, 0.2, 0], LEFT, buff=0.3)
            rv = MathTex(rf"\rho = {rho[i]:.2f}", font_size=26, color=WHITE if i == 0 else GREY_A).next_to([W / 2, 0.2, 0], RIGHT, buff=0.3)
            rows.add(VGroup(nm, bar, rv))
        rows.arrange(DOWN, buff=0.28).move_to([0.8, -0.5, 0])
        txt, _ = char_row(text, W, 0, font_size=14)
        txt.next_to(rows[0][1], UP, buff=0.15).set_x(rows[0][1].get_x())
        hc = history_card(2018, r"J.~Adebayo et al., \ \textit{Sanity Checks for Saliency Maps}",
                          r"re-randomize the network, layer by layer from the top: \ a map that does not change was "
                          r"not explaining the network", width=11.5, color=CAUSE, font_size=20).to_edge(UP, buff=0.25)
        rr = float(np.mean(s["rho_rand"]))
        passes = rho[-1] < 0.5 and rr < 0.5
        verdict = (f"<bookmark mark='c'/> Ours passes: by the end the correlation is {rho[-1]:.2f}, and {rr:.2f} on "
                   "average over the 24 other predictions. The map does depend on what the network learned. But "
                   "passing a sanity check is not the same as being right." if passes else
                   f"<bookmark mark='c'/> Ours keeps a correlation of {rho[-1]:.2f} even with everything random: much "
                   "of the map is about the input, not the network.")
        with self.voiceover(
            "Worse, a picture that looks sensible can explain nothing. <bookmark mark='a'/> In 2018 Julius Adebayo "
            "and colleagues re-randomized a network's weights, layer by layer from the top, and found that some "
            "popular saliency methods barely changed: they were showing the input's edges, not the network's "
            "reasons. <bookmark mark='b'/> Run the test on ours. Re-randomize block four, then three and four, and "
            "so on down to the embedding, and compare each map with the trained one. " + verdict
        ) as vo:
            self.play(FadeIn(hc, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(txt), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_, shift=DOWN * 0.1) for r_ in rows[1:]], lag_ratio=0.5), run_time=4)
            vo.wait_until("c")
            self.play(Indicate(VGroup(*[r_[2] for r_ in rows]), color=CAUSE))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pictures(self):
        cards = VGroup(
            history_card(2015, r"A.~Mordvintsev, C.~Olah \& M.~Tyka: \ DeepDream",
                         r"run the gradient the other way: \ change the image to excite a layer", width=6.4,
                         color=PROBE, font_size=24),
            history_card(2017, r"D.~Bau et al.: \ Network Dissection",
                         r"score each unit against labelled concepts: \ some units are lamps, \ some are dogs",
                         width=6.4, color=PROBE, font_size=24),
            history_card(2017, r"C.~Olah, A.~Mordvintsev \& L.~Schubert, \ \textit{Distill}",
                         r"feature visualization: \ optimize an input, \ with priors that keep it natural, \ until a "
                         r"neuron fires", width=6.4, color=PROBE, font_size=24),
            history_card(2018, r"C.~Olah et al., \ \textit{The Building Blocks of Interpretability}",
                         r"attribution and feature visualization combined: \ what a network sees, \ and where",
                         width=6.4, color=PROBE, font_size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.35, 0.35)).move_to(DOWN * 0.35)
        head = label(r"From which inputs to which features", font_size=36).to_edge(UP, buff=0.35)
        for c in cards:
            c.set_opacity(0.18)
        with self.voiceover(
            "So the question moved from which inputs to what the parts of a network are for. <bookmark mark='a'/> "
            "In 2015 Alexander Mordvintsev, Chris Olah and Mike Tyka ran the gradient the other way, changing an "
            "image to excite a layer, and DeepDream's dog-filled clouds went around the world. "
            "<bookmark mark='b'/> In 2017 David Bau's Network Dissection scored every unit against labelled "
            "concepts, and found units for lamps and for dogs. <bookmark mark='c'/> The same year Olah, Mordvintsev "
            "and Ludwig Schubert turned the trick into a science in the online journal Distill: feature "
            "visualization, an input optimized until one neuron fires. <bookmark mark='d'/> A year later they "
            "combined it with attribution: what the network sees, and where."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(cards[k].animate.set_opacity(1.0), *[c.animate.set_opacity(0.4) for c in cards[:k]])
            self.play(*[c.animate.set_opacity(1.0) for c in cards])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def circuits(self):
        claims = theorem_card(r"three speculative claims", VGroup(
            label(r"$1.$ \ Features are the fundamental unit of a neural network.", font_size=22),
            label(r"$2.$ \ Features are connected by weights, \ forming circuits.", font_size=22),
            label(r"$3.$ \ Analogous features and circuits form across models.", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14), who=r"C.~Olah et al., \textit{Zoom In: An Introduction to "
                              r"Circuits} \ (Distill, 2020)", kind=r"Circuits", width=8.4, color=FEAT).to_edge(UP, buff=0.3)
        steps_ = [
            (2021, r"Goh et al.: \ multimodal neurons in CLIP", r"one unit for a person, \ in photos, drawings and "
             r"written names"),
            (2021, r"Elhage et al.: \ the transformer circuits framework", r"heads as read and write maps on a residual "
             r"stream"),
            (2022, r"Olsson et al.: \ induction heads", r"two heads that copy from context: \ chapter 5"),
            (2022, r"Wang et al.: \ indirect objects in GPT-2 small", r"a circuit of $26$ heads in $7$ classes"),
            (2022, r"Elhage et al.: \ toy models of superposition", r"more features than dimensions: \ chapter 6"),
            (2023, r"Bricken et al.: \ towards monosemanticity", r"$512$ neurons into $4{,}096$ features: \ chapter 8"),
            (2024, r"Templeton et al.: \ scaling monosemanticity", r"$34$ million features in Claude 3 Sonnet"),
            (2025, r"Ameisen, Lindsey et al.: \ attribution graphs", r"tracing Claude 3.5 Haiku's computations: \ "
             r"chapter 11"),
        ]
        cards = VGroup(*[history_card(y, w, t, width=3.25, color=FEAT, font_size=17) for y, w, t in steps_])
        cards.arrange_in_grid(rows=2, cols=4, buff=(0.15, 0.22)).next_to(claims, DOWN, buff=0.3)
        if cards.width > 13.6:
            cards.width = 13.6
        for c in cards:
            c.set_opacity(0.15)
        with self.voiceover(
            "In 2020 the work found its programme. Olah and colleagues' Zoom In made three speculative claims. "
            "<bookmark mark='a'/> Features are the units of a network; features connect through weights into "
            "circuits; and the same features and circuits turn up in different models. They traced curve detectors "
            "in a vision network wire by wire. <bookmark mark='b'/> Then the programme moved to language. In 2021, "
            "multimodal neurons in CLIP, and a mathematical framework for transformer circuits; "
            "<bookmark mark='c'/> in 2022, induction heads, a 26-head circuit in GPT-2 small, and toy models of "
            "superposition, which explained why single neurons so rarely mean one thing. <bookmark mark='d'/> Then "
            "sparse dictionaries split neurons into features, first in a one-layer model, then by the million in "
            "Claude 3 Sonnet, and in 2025 attribution graphs traced a production model's computations. This part "
            "walks that path on our own models."
        ) as vo:
            self.play(FadeIn(claims, shift=DOWN * 0.15), FadeIn(cards))
            vo.wait_until("a")
            self.play(Indicate(claims.body, color=FEAT, scale_factor=1.02))
            vo.wait_until("b")
            self.play(LaggedStart(*[c.animate.set_opacity(1) for c in cards[:2]], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(LaggedStart(*[c.animate.set_opacity(1) for c in cards[2:5]], lag_ratio=0.4))
            vo.wait_until("d")
            self.play(LaggedStart(*[c.animate.set_opacity(1) for c in cards[5:]], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

