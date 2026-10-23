from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai20.common import (AR, DATA, EBM, FLOW, GAN_C, HIST, LATENT, PART, VAE_C, Plane, check_mark, digit,
                                   digit_sheet, load)
from videos.ai.ai20.gendigits import BUDGET


class Problem(VoiceoverScene):
    def construct(self):
        self.card()
        self.define()
        self.likelihood()
        self.history()
        self.families()
        self.testbed()

    def card(self):
        card = chapter_card(1, r"The generative problem", r"What does it mean to learn a distribution?",
                            lit=(1948, 2014, 2015), part=PART)
        with self.voiceover("Chapter one. The generative problem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def define(self):
        t = load("toys")
        pl = Plane(3.8, center=[-4.2, 0.0, 0])
        pts = pl.scatter_image(np.asarray(t["moons_samples"])[:1200], DATA, radius_px=1.8)
        dens = pl.image(t["moons_density"], DATA)
        pl_l = label(r"$20{,}000$ samples \ $x \sim p$", font_size=22, color=DATA).next_to(pl, UP, buff=0.15)
        dl = label(r"the density $p(x)$ \ (known here, \ never in practice)", font_size=20, color=GREY_A)
        dl.next_to(pl, DOWN, buff=0.15)
        d = definition_card(r"generative model", r"a distribution $q_\theta(x)$, \ learned from samples of $p(x)$, "
                            r"\ that we can \textbf{sample} from; \ ideally also \textbf{evaluate} $q_\theta(x)$, "
                            r"\ and read off a \textbf{code} $z$ for each $x$", width=7.2, font_size=24)
        d.move_to([2.6, 1.3, 0])
        uses = VGroup(label(r"sample: \ new images, \ text, \ sound, \ molecules", font_size=22),
                      label(r"evaluate: \ compression, \ anomaly detection", font_size=22),
                      label(r"encode: \ representations for other tasks", font_size=22))
        uses.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(d, DOWN, buff=0.45).align_to(d, LEFT)
        shown = Group(pl, dens, pl_l, dl)  # starts large in the middle, moves aside for the definition
        home = shown.get_center()
        Group(pl, pts, dens, pl_l, dl).scale(1.3, about_point=home).move_to([0, home[1], 0])
        with self.voiceover(
            "Here is the problem at its smallest: twenty thousand points in the plane, drawn from a distribution p "
            "in the shape of two moons. <bookmark mark='a'/> Because we made it, we know p exactly; with images or "
            "text, nobody does. <bookmark mark='b'/> A generative model is a distribution q, learned from the "
            "samples, that we can sample from; <bookmark mark='c'/> ideally one we can also evaluate, <bookmark "
            "mark='d'/> and one that gives each x a code, a short description of what it is."
        ) as vo:
            self.play(FadeIn(pl), FadeIn(pts), FadeIn(pl_l))
            vo.wait_until("a")
            self.play(FadeIn(dens), FadeOut(pts), FadeIn(dl))
            vo.wait_until("b")
            self.play(shown.animate.scale(1 / 1.3).move_to(home), run_time=1.0)
            self.play(FadeIn(d, shift=UP * 0.15), FadeIn(uses[0]))
            vo.wait_until("c")
            self.play(FadeIn(uses[1]))
            vo.wait_until("d")
            self.play(FadeIn(uses[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def likelihood(self):
        t = load("toys")
        cols = {r"p": DATA, r"q_\theta": C.MODEL_Q}
        rows = [
            cmath(r"\mathbb E_{x \sim p}\big[-\log q_\theta(x)\big]", r"=",
                  r"\mathbb E_{p}\big[-\log p(x)\big]", r"+", r"\mathbb E_{p}\Big[\log \frac{p(x)}{q_\theta(x)}\Big]",
                  font_size=36),
            cmath(r"\mathbb E_{x \sim p}\big[-\log q_\theta(x)\big]", r"=", r"h(p)", r"+",
                  r"\mathrm{KL}(p \,\|\, q_\theta)", font_size=36),
            cmath(r"\arg\min_\theta \, \mathbb E_{x \sim p}\big[-\log q_\theta(x)\big]", r"=",
                  r"\arg\min_\theta \, \mathrm{KL}(p \,\|\, q_\theta)", font_size=36),
        ]
        rows[1][2].set_color(DATA)
        rows[1][4].set_color(C.KL)
        rows[2][2].set_color(C.KL)
        whys = [why(r"add and subtract $\log p$"), why(r"the data's entropy, \ and the KL gap (Part 1)"),
                why(r"$h(p)$ doesn't depend on $\theta$")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-0.6, buff=0.55, edge=6.9)
        names = [r"two moons", r"ring of eight", r"checkerboard"]
        bars = VGroup()
        for i, n in enumerate(("moons", "ring", "checker")):
            h = float(t[f"{n}_entropy"])
            bars.add(VGroup(label(names[i], font_size=24, color=DATA),
                            MathTex(rf"h(p) = {h:.2f}\ \text{{nats}}", font_size=30, color=DATA)).arrange(DOWN,
                                                                                                         buff=0.12))
        bars.arrange(RIGHT, buff=1.0).move_to(DOWN * 2.4)
        hm, hr, hc = (float(t[f"{n}_entropy"]) for n in ("moons", "ring", "checker"))
        with self.voiceover(
            "The workhorse for fitting q is maximum likelihood, from Part 1: minimize the average surprise, minus "
            "log q. <bookmark mark='a'/> Split that average in two. <bookmark mark='b'/> The data's own entropy, "
            "which no model can beat, plus the KL divergence from p to q, the price of being wrong. <bookmark "
            "mark='c'/> So maximum likelihood is minimum KL. <bookmark mark='d'/> For our three test densities the "
            f"floor is known: {hm:.2f} nats for the moons, {hr:.2f} for the ring of eight Gaussians, {hc:.2f} for "
            "the checkerboard."
        ) as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bars], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        events = [
            (1948, r"Shannon: \\ English, letter \\ by letter", AR),
            (1982, r"Hopfield: \\ memories as \\ energy minima", EBM),
            (1985, r"Boltzmann \\ machines", EBM),
            (1995, r"Helmholtz \\ machine", VAE_C),
            (2006, r"deep belief \\ nets", EBM),
            (2013, r"variational \\ autoencoders", VAE_C),
            (2014, r"GANs; \\ NICE flows", GAN_C),
            (2016, r"PixelCNN, \\ WaveNet", AR),
            (2018, r"StyleGAN; \\ neural ODEs", GAN_C),
            (2021, r"diffusion \\ beats GANs", GREY_A),
            (2024, r"next-scale \\ prediction", AR),
        ]
        y0, x0, x1 = -0.2, -6.4, 6.4
        T0, T1 = 1945, 2027
        X = lambda yr: x0 + (x1 - x0) * (yr - T0) / (T1 - T0)
        line = Line([x0, y0, 0], [x1, y0, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup()
        for yr in (1950, 1970, 1990, 2010):
            ticks.add(Line([X(yr), y0 - 0.06, 0], [X(yr), y0 + 0.06, 0], color=GREY_C, stroke_width=1.5))
        items = VGroup()
        for k, (yr, txt, col) in enumerate(events):
            dot = Dot([X(yr), y0, 0], radius=0.07, color=col)
            yl = label(str(yr), font_size=20, color=col)
            tx = label(txt, font_size=18, color=WHITE)
            up = k % 2 == 0
            grp = VGroup(yl, tx).arrange(DOWN, buff=0.06)
            grp.next_to(dot, UP if up else DOWN, buff=0.3 if up else 0.3)
            stem = Line(dot.get_center(), grp.get_bottom() if up else grp.get_top(), color=col, stroke_width=1.2)
            items.add(VGroup(dot, stem, grp))
        # keep labels apart
        for side in (0, 1):
            same = [items[k] for k in range(len(items)) if k % 2 == side]
            for a, b in zip(same, same[1:]):
                gap = b[2].get_left()[0] - a[2].get_right()[0]
                if gap < 0.12:
                    b[2].shift(RIGHT * (0.12 - gap))
            if same[-1][2].get_right()[0] > 6.9:
                same[-1][2].shift(LEFT * (same[-1][2].get_right()[0] - 6.9))
        for it in items:
            dot, stem, grp = it
            stem.put_start_and_end_on(dot.get_center(), [grp.get_x(), grp.get_bottom()[1] if grp.get_y() > y0
                                                         else grp.get_top()[1], 0])
        head = label(r"How we got here", font_size=36).to_edge(UP, buff=0.4)
        with self.voiceover(
            "How we got here. In 1948 Claude Shannon generated English letter by letter: the first autoregressive "
            "model. <bookmark mark='a'/> In the 1980s memories became the valleys of an energy, in Hopfield's "
            "network and the Boltzmann machine; <bookmark mark='b'/> in 1995 the Helmholtz machine added a second "
            "network to guess hidden causes. <bookmark mark='c'/> Stacked Boltzmann machines restarted deep "
            "learning in 2006. <bookmark mark='d'/> Then, within three years, variational autoencoders, adversarial "
            "networks, invertible flows and PixelCNN. <bookmark mark='e'/> GANs made the sharpest images until "
            "2021, when diffusion overtook them. <bookmark mark='f'/> Today's systems combine all of these ideas."
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(ticks))
            groups = [[0], [1, 2], [3], [4], [5, 6, 7, 8], [9], [10]]
            for k, mk in enumerate([None, "a", "b", "c", "d", "e", "f"]):
                if mk:
                    vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(items[i], shift=UP * 0.1) for i in groups[k]], lag_ratio=0.3),
                          run_time=1.0 + 0.3 * len(groups[k]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def families(self):
        cols = [r"likelihood", r"one-pass sampling", r"a code $z$", r"stable training"]
        rows_ = [
            (r"autoregressive", AR, ["y", "n", "n", "y"]),
            (r"VAE", VAE_C, ["b", "y", "y", "y"]),
            (r"GAN", GAN_C, ["n", "y", "g", "n"]),
            (r"flow", FLOW, ["y", "y", "y", "y"]),
            (r"energy model", EBM, ["u", "n", "n", "n"]),
        ]
        head = VGroup(*[label(c, font_size=22, color=GREY_A) for c in cols])
        table = VGroup()
        x_cols = [-1.2, 1.4, 3.6, 5.6]
        y = 1.6
        for c, x in zip(head, x_cols):
            c.move_to([x, y + 0.7, 0])
        marks = {"y": (r"\checkmark", C.INTERVAL), "n": (r"\times", GREY_C), "b": (r"\text{a bound}", C.KL),
                 "g": (r"\text{no encoder}", GREY_B), "u": (r"\text{up to } Z", GREY_B)}
        for k, (name, col, ms) in enumerate(rows_):
            yy = y - 0.62 * k
            nm = label(name, font_size=26, color=col).move_to([-4.6, yy, 0])
            cells = VGroup()
            for m, x in zip(ms, x_cols):
                s, cc = marks[m]
                t = MathTex(s, font_size=34 if len(s) < 12 else 24, color=cc).move_to([x, yy, 0])
                cells.add(t)
            table.add(VGroup(nm, cells))
        rule = Line([-6.0, y + 0.35, 0], [6.6, y + 0.35, 0], color=GREY_D, stroke_width=1.2)
        tri = label(r"the trilemma: \ sharp samples, \ all of the data's modes, \ fast sampling; \ pick two",
                    font_size=24, color=C.BITS).to_edge(DOWN, buff=0.5)
        tri_c = note(r"Xiao, Kreis \& Vahdat (2022)").next_to(tri, DOWN, buff=0.08)
        sch = note(r"the usual summary").to_corner(UR, buff=0.25)
        with self.voiceover(
            "What each family offers. <bookmark mark='a'/> An autoregressive model: the exact likelihood and stable "
            "training, but samples one piece at a time. <bookmark mark='b'/> A VAE: one-pass sampling and a code, "
            "but only a bound on the likelihood. <bookmark mark='c'/> A GAN: one pass, no likelihood at all, and "
            "famously hard to train. <bookmark mark='d'/> A flow: everything on paper, paid for in architecture. "
            "<bookmark mark='e'/> An energy model: a density known only up to a constant, and slow sampling. "
            "<bookmark mark='f'/> Xiao, Kreis and Vahdat called it a trilemma: sharp samples, coverage of the data, "
            "fast sampling. Most families managed two."
        ) as vo:
            self.play(FadeIn(head), Create(rule), FadeIn(sch))
            for k, mk in enumerate("abcde"):
                vo.wait_until(mk)
                self.play(FadeIn(table[k][0]), LaggedStart(*[FadeIn(c, scale=1.3) for c in table[k][1]],
                                                           lag_ratio=0.15))
            vo.wait_until("f")
            self.play(FadeIn(tri, shift=UP * 0.1), FadeIn(tri_c))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def testbed(self):
        t = load("toys")
        c = load("classifier")
        panels = Group()
        for n, nm in (("moons", r"two moons"), ("ring", r"a ring of eight"), ("checker", r"a checkerboard")):
            pl = Plane(2.3)
            img = pl.image(t[f"{n}_density"], DATA)
            panels.add(Group(img, pl, label(nm, font_size=22, color=DATA).next_to(pl, UP, buff=0.12)))
        panels.arrange(RIGHT, buff=0.3).move_to([-3.1, 1.35, 0])
        raw = np.asarray(c["raw28"])[0] / 255.0
        half = np.asarray(c["half14"])[0]
        lev = np.clip(np.floor(half * 16), 0, 15)
        im1 = digit(raw, 1.8)
        im2 = digit(half, 1.8)
        im3 = digit(lev / 15, 1.8)
        trio = Group(im1, im2, im3).arrange(RIGHT, buff=0.6).move_to([-2.6, -1.9, 0])
        arrs = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=2.5)
                        for a, b in ((im1, im2), (im2, im3))])
        caps = VGroup(label(r"$28 \times 28$", font_size=22, color=GREY_A).next_to(im1, DOWN, buff=0.1),
                      label(r"average $2 \times 2$", font_size=22, color=GREY_A).next_to(im2, DOWN, buff=0.1),
                      label(r"$16$ grey levels", font_size=22, color=GREY_A).next_to(im3, DOWN, buff=0.1))
        facts = VGroup(
            label(rf"MNIST: \ ${c['n_train']:,}$ training digits, \ ${c['n_test']:,}$ test".replace(",", "{,}"),
                  font_size=22),
            label(r"$196$ pixels, \ $4$ bits each: \ at most $4$ bits per pixel", font_size=22),
            label(rf"every image model: \ ${sci(BUDGET, 0)}$ operations of training", font_size=22, color=C.BITS),
            label(r"several seeds each, \ the spread shown", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        facts.move_to([0, -1.5, 0]).to_edge(RIGHT, buff=0.4)
        sheet = digit_sheet(np.asarray(c["grid"])[:12], 3, 4, size=0.42, gap=0.04).move_to([4.6, 1.4, 0])
        lc = note(r"LeCun, Cortes \& Burges (1998)").next_to(sheet, DOWN, buff=0.1)
        with self.voiceover(
            "Our test bench: three densities in the plane, small enough to see everything a model does, each hard "
            "in its own way. <bookmark mark='a'/> And images: the MNIST digits, sixty thousand to train on, ten "
            "thousand to test, averaged down to fourteen by fourteen pixels <bookmark mark='b'/> of sixteen grey "
            "levels. <bookmark mark='c'/> Every image model gets the same budget of arithmetic, counted operation "
            "by operation, and several random starts."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(p) for p in panels], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(sheet), FadeIn(lc), FadeIn(im1), FadeIn(caps[0]), FadeIn(facts[0]))
            self.play(GrowArrow(arrs[0]), FadeIn(im2), FadeIn(caps[1]))
            vo.wait_until("b")
            self.play(GrowArrow(arrs[1]), FadeIn(im3), FadeIn(caps[2]), FadeIn(facts[1]))
            vo.wait_until("c")
            self.play(FadeIn(facts[2]), FadeIn(facts[3]))
        self.wait(0.3)
        self.clear_scene()
