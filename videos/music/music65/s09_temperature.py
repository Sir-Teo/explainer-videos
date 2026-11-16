from __future__ import annotations

import numpy as np

from videos.music.music65.common import *  # noqa: F403


class Temperature(SoundScene):
    def construct(self):
        chapter(self, 8, r"Temperature", r"How adventurous should a machine be?")
        self.idea()
        self.quiz()
        self.table()
        self.others()

    # ------------------------------------------------------------------
    def idea(self):
        p = np.array([0.5, 0.25, 0.12, 0.08, 0.05])
        names = [r"G", r"E", r"A", r"C", r"F$\sharp$"]
        temps = (0.5, 1.0, 1.5)
        groups = VGroup()
        for k, T in enumerate(temps):
            q = p ** (1 / T)
            q /= q.sum()
            bars = VGroup(*[Rectangle(width=0.42, height=2.6 * v, stroke_width=0, fill_color=TUNE if j == 0 else (EAR if j == 4 else BLUE), fill_opacity=0.85)
                            .move_to([-4.2 + 4.2 * k + 0.55 * j, -1.6 + 1.3 * v, 0]) for j, v in enumerate(q)])
            labs = VGroup(*[label(n, font_size=14, color=GREY_A).move_to([-4.2 + 4.2 * k + 0.55 * j, -1.85, 0]) for j, n in enumerate(names)])
            t = label(rf"temperature {T:g}", font_size=18, color=WHITE).move_to([-4.2 + 4.2 * k + 1.1, 1.4, 0])
            groups.add(VGroup(bars, labs, t))
        eq = MathTex(r"p_i \propto p_i^{\,1/T}", font_size=38, color=TUNE).to_edge(UP, buff=1.0)
        head = label(r"temperature", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Every generator here draws from a distribution, and one knob reshapes it: the temperature. "
            "<bookmark mark='a'/> Raise each probability to the power one over the temperature, and renormalize. "
            "<bookmark mark='b'/> Below one, the likeliest note grows likelier still: safe, repetitive. "
            "<bookmark mark='c'/> At one, the model's own odds. <bookmark mark='d'/> Above one, the unlikely notes, the "
            "F sharp in C major, get their chance: adventurous, and soon lost."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(eq))
            for mark, g in zip("bcd", groups):
                vo.wait_until(mark)
                self.play(FadeIn(g))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("temperature")
        c = clip("temperature.three")
        card = listen_card(rf"The opening phrase of {bwv(d['opening'])}, \ three times, \ each continued by the transformer \ at a different temperature: \ 0.5, \ 1.0 and 1.5, \ in some order. \ Which is which?", width=10.0)
        with self.voiceover("Your turn. The opening phrase of a chorale the network never saw, three times, each continued by the transformer at a different temperature: a half, one, and one and a half. Can you tell which is which?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second", r"third"], width=2.8, buff=0.8).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        ks = ["t05", "t10", "t15"]
        with self.listen(c) as snd:
            window(snd, r"three temperatures", kind="synthesized", detail=r"the transformer, \ twelve keys", corner=DL, tag_corner=DR)
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.4 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.08)
        res = label(r"in order: \ 0.5, \ 1.0, \ 1.5", font_size=20, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover("They were in order: a half, one, one and a half. Cooler draws keep to the likeliest notes and the key; hotter ones take more of the unlikely ones, as the measures on the next page show over many openings."):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        d = load("temperature")
        rows = d["rows"]
        g = VGroup()
        for T in d["temps"]:
            r = rows[str(T)]
            g.add(VGroup(label(rf"{T:g}", font_size=19, color=WHITE), label(f"{r['kl']:.2f}", font_size=19, color=TUNE), label(f"{100 * r['chromatic']:.0f}\\%", font_size=19, color=EAR),
                         label(f"{100 * r['cadence']:.0f}\\%", font_size=19, color=BLUE), label(f"{r['longest']:.1f}", font_size=19, color=GREY_B)))
        b = d["bach"]
        g.add(VGroup(label(r"Bach", font_size=19, color=GOLD), label(r"0", font_size=19, color=GOLD), label(f"{100 * b['chromatic']:.0f}\\%", font_size=19, color=GOLD),
                     label(f"{100 * b['cadence']:.0f}\\%", font_size=19, color=GOLD), label(f"{b['longest']:.1f}", font_size=19, color=GOLD)))
        g.arrange(DOWN, buff=0.32)
        for r in g:
            for i, x in enumerate((-4.8, -2.3, 0.0, 2.4, 4.8)):
                r[i].set_x(x)
        g.move_to(DOWN * 0.5)
        top = VGroup(*[label(t, font_size=14, color=GREY_A).move_to([x, g.get_top()[1] + 0.55, 0]) for t, x in
                       ((r"temperature", -4.8), (r"interval divergence \ from Bach \ (bits)", -2.3), (r"notes outside \ the key", 0.0),
                        (r"phrases ending \ on the tonic chord", 2.4), (r"longest copied \ run \ (notes)", 4.8))])
        head = label(r"twenty-three openings, \ continued twice", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        r05, r10, r15 = (rows[str(t)] for t in d["temps"])
        with self.voiceover(
            "Measure it over the held-out openings, each continued twice at each temperature. "
            "<bookmark mark='a'/> The intervals come closest to Bach's at temperature one, "
            f"{say(r10['kl'], 2)} bits away, against {say(r05['kl'], 2)} when cooler and {say(r15['kl'], 2)} when hotter: at "
            "one the model draws with its own odds, which were fitted to music like Bach's. Notes outside the key rise with "
            f"the temperature, from {say(round(100 * r05['chromatic']))} to {say(round(100 * r15['chromatic']))} per cent, "
            f"where Bach's tunes have {say(round(100 * b['chromatic']))}; and phrases end on the tonic chord most often when it "
            "is cool. <bookmark mark='b'/> Copying stays near nothing at every temperature: this model, stopped at its best, "
            "shows little exact eight-note-run copying in these finite trials. No setting is right for every purpose; people who use such models tune it by ear."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in g], lag_ratio=0.25), run_time=1.8)
            vo.wait_until("b")
            self.play(*[Indicate(r[4], color=GREY_A) for r in g[:-1]])
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def others(self):
        items = [
            (r"top-$k$: \ draw only among the $k$ likeliest notes", WHITE),
            (r"nucleus \ (top-$p$, \ Holtzman et al., \ 2020): \ only among the likeliest notes that together hold probability $p$", WHITE),
            (r"beam search finds the single likeliest tune: \ for music, \ usually the dullest", WHITE),
            (r"all of them trade surprise for safety; \ none adds knowledge the model does not have", TUNE),
        ]
        rows_scene(self, r"other ways to draw", items,
                   "Temperature is one of several ways to draw. <bookmark mark='b'/> Top-k draws only among the k likeliest notes. <bookmark mark='c'/> Nucleus sampling, from Ari Holtzman and colleagues, draws among the likeliest notes that together hold a chosen share of the probability. <bookmark mark='d'/> Beam search approximately searches for high-probability sequences; it need not find the global optimum and can favour repetition. <bookmark mark='e'/> All of them trade surprise for safety, and none adds knowledge the model does not have.", marks="bcde")
