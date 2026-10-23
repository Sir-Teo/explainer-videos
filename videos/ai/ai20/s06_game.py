from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai20.common import (DATA, DISC, GAN_C, HIST, PART, Plane, density_rgb, load, node_box, rgb_of, to_image)


def d_rgb(Dv, color=DISC) -> np.ndarray:
    """The discriminator's verdict on the plane as a picture: bright where it says 'real', dark where 'fake'."""
    t = np.clip(np.asarray(Dv, float), 0, 1)
    bg = rgb_of("#0B0F17")
    col = rgb_of(color)
    return (bg[None, None] * (1 - 0.75 * t[..., None]) + col[None, None] * 0.75 * t[..., None])[::-1]


def replay_gan(scene, g, loss, plane: Plane, duration: float, counter_pos, color=GAN_C, critic=False):
    """Seed 0 of a ring run, replayed: the discriminator (or critic) as the background, the generator's samples as
    dots that move between checkpoints, and a counter of the modes covered.  Returns the mobjects."""
    S = np.asarray(g[f"{loss}_frame_samples"])[:, :300]
    Dd = np.asarray(g[f"{loss}_frame_d"])
    if critic:  # a critic's values have no fixed scale: squash each frame to [0, 1]
        Dd = np.array([(f - np.percentile(f, 2)) / max(np.percentile(f, 98) - np.percentile(f, 2), 1e-9) for f in Dd])
    steps = list(g[f"{loss}_frame_steps"])
    modes = list(g[f"{loss}_frame_modes"])
    frames = [to_image(d_rgb(fr), plane.side, plane.side, smooth=True).pixel_array for fr in Dd]
    img = to_image(d_rgb(Dd[0]), plane.side, plane.side, smooth=True).move_to(plane.frame.get_center())
    dots = VGroup(*[Dot(q, radius=0.028, color=color) for q in plane.pts(np.clip(S[0], -2.95, 2.95))])
    f = ValueTracker(0.0)
    cnt = Integer(modes[0], font_size=34, color=color).move_to(counter_pos)
    stp = Integer(steps[0], font_size=24, color=GREY_A).next_to(cnt, DOWN, buff=0.35)

    def upd(_):
        v = min(f.get_value(), len(S) - 1 - 1e-6)
        k = int(v)
        a = v - k
        P = (1 - a) * S[k] + a * S[min(k + 1, len(S) - 1)]
        for d_, q in zip(dots, plane.pts(np.clip(P, -2.95, 2.95))):
            d_.move_to(q)
        img.pixel_array = frames[k]
        cnt.set_value(modes[k])
        stp.set_value(steps[k])

    holder = VGroup(dots, cnt, stp)
    holder.add_updater(upd)
    scene.add(img, holder)
    scene.play(f.animate.set_value(len(S) - 1), run_time=duration, rate_func=linear)
    holder.clear_updaters()
    return img, dots, cnt, stp


class Game(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup_game()
        self.optimal()
        self.js()
        self.saturation()
        self.ring()

    def card(self):
        card = chapter_card(5, r"The adversarial game", r"Can a critic teach a forger?", lit=(2014,), part=PART)
        with self.voiceover("Chapter five. The adversarial game."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def setup_game(self):
        z = node_box(r"noise $z$", GREY_B, font_size=26).move_to([-5.6, 0.8, 0])
        G = node_box(r"generator $G$", GAN_C, font_size=26, height=0.9).move_to([-3.2, 0.8, 0])
        fake = node_box(r"$G(z)$", GAN_C, font_size=26).move_to([-0.8, 0.8, 0])
        real = node_box(r"a real $x$", DATA, font_size=26).move_to([-0.8, -0.9, 0])
        D = node_box(r"discriminator $D$", DISC, font_size=26, height=0.9).move_to([2.2, 0.0, 0])
        out = node_box(r"$D(\cdot)$: \ probability real", DISC, font_size=24).move_to([5.3, 0.0, 0])
        A = lambda a, b, c=GREY_B: Arrow(a.get_right(), b.get_left(), buff=0.08, color=c, stroke_width=2.5)
        arrs = VGroup(A(z, G), A(G, fake), A(fake, D), A(real, D), A(D, out))
        V = cmath(r"\min_G \max_D \; V(D, G)", r"=", r"\mathbb E_{x \sim p}\big[\log D(x)\big]", r"+",
                  r"\mathbb E_{z}\big[\log\big(1 - D(G(z))\big)\big]", font_size=36).to_edge(UP, buff=0.4)
        V[2].set_color(DATA)
        V[4].set_color(GAN_C)
        card = history_card(2014, r"Goodfellow, Pouget-Abadie, Mirza, Xu, Warde-Farley, Ozair, Courville \& Bengio",
                            r"\textit{Generative Adversarial Nets}: \ a team of counterfeiters against the police",
                            width=7.4, font_size=20).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The third answer throws the likelihood away. In 2014 Ian Goodfellow and colleagues in Yoshua Bengio's "
            "lab in Montreal set two networks against each other. <bookmark mark='a'/> A generator turns random "
            "noise into a sample; it never sees the data. <bookmark mark='b'/> A discriminator looks at a sample, "
            "real or generated, and outputs the probability that it is real. <bookmark mark='c'/> The "
            "discriminator is trained to tell them apart, the generator to fool it; the paper's picture is a team of "
            "counterfeiters against the police. Written as one value: the discriminator maximizes the log "
            "probability of being right on both kinds of sample, and the generator minimizes it."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeIn(z), GrowArrow(arrs[0]), FadeIn(G), GrowArrow(arrs[1]), FadeIn(fake))
            vo.wait_until("b")
            self.play(FadeIn(real), GrowArrow(arrs[2]), GrowArrow(arrs[3]), FadeIn(D), GrowArrow(arrs[4]), FadeIn(out))
            vo.wait_until("c")
            self.play(Write(V), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def optimal(self):
        rows = [
            cmath(r"V(D, G)", r"=", r"\int \big[\, p(x) \log D(x) + q(x) \log\big(1 - D(x)\big) \big]\, dx",
                  font_size=34),
            cmath(r"\frac{\partial}{\partial D}\big[a \log D + b \log(1 - D)\big]", r"=",
                  r"\frac{a}{D} - \frac{b}{1 - D}", r"=", r"0", font_size=34),
            cmath(r"D^*(x)", r"=", r"\frac{p(x)}{p(x) + q(x)}", font_size=36),
        ]
        rows[2][0].set_color(DISC)
        whys = [why(r"$q$: \ the generator's distribution"), why(r"maximize at each $x$ separately"),
                why(r"the best discriminator")]
        step = ladder(self, rows, whys, keep=3, top=3.3, x=-1.0, buff=0.45, edge=6.9)
        g = axes([-4, 4], [0, 1.05], x_length=7.0, y_length=2.4, xticks=[-4, 0, 4], yticks=[0, 0.5, 1],
                 center=[-1.2, -2.3, 0])
        xs = np.linspace(-4, 4, 300)
        p = 0.5 * np.exp(-((xs + 1.2) ** 2) / 0.5) / math.sqrt(0.5 * math.pi) + 0.5 * np.exp(
            -((xs - 1.6) ** 2) / 0.3) / math.sqrt(0.3 * math.pi)
        q = np.exp(-((xs - 0.4) ** 2) / 2.0) / math.sqrt(2.0 * math.pi)
        pc, qc = curve(g.ax, xs, p / p.max(), DATA, 3), curve(g.ax, xs, q / p.max(), C.MODEL_Q, 3)
        dc = curve(g.ax, xs, p / (p + q), DISC, 3)
        lg = legend([(DATA, r"$p$"), (C.MODEL_Q, r"$q$"), (DISC, r"$D^*$")], font_size=22).next_to(g, RIGHT, buff=0.3)
        tg = note(r"illustrative").to_corner(DR, buff=0.25)
        with self.voiceover(
            "What does the discriminator learn, if it wins? Write the value as an integral over x, with q for the "
            "generator's distribution. <bookmark mark='a'/> At every x separately, the discriminator chooses one "
            "number, D of x, to maximize a times log D plus b times log one minus D. Set the derivative to zero. "
            "<bookmark mark='b'/> The best discriminator is p over p plus q: the share of the probability at x "
            "that belongs to the data. <bookmark mark='c'/> Where the data dominates it says real, where the "
            "generator dominates it says fake, and where they agree, one half."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(g), Create(pc), Create(qc), FadeIn(tg), FadeIn(lg))
            self.play(Create(dc))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def js(self):
        rows = [
            cmath(r"V(D^*, G)", r"=", r"\mathbb E_p\Big[\log \frac{p}{p + q}\Big] + \mathbb E_q\Big[\log "
                  r"\frac{q}{p + q}\Big]", font_size=34),
            cmath(r"V(D^*, G)", r"=", r"-\log 4", r"+", r"\mathrm{KL}\big(p \,\|\, m\big) + "
                  r"\mathrm{KL}\big(q \,\|\, m\big)", font_size=34),
            cmath(r"V(D^*, G)", r"=", r"-\log 4", r"+", r"2\, \mathrm{JS}(p \,\|\, q)", font_size=36),
        ]
        rows[2][4].set_color(C.KL)
        whys = [why(r"put $D^*$ back in"), why(r"$m = \tfrac12 (p + q)$: \ pull out $\log \tfrac12$ twice"),
                why(r"Jensen--Shannon divergence")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-1.2, buff=0.55, edge=6.9)
        d = definition_card(r"Jensen--Shannon divergence", r"$\mathrm{JS}(p \,\|\, q) = \tfrac12 \mathrm{KL}(p \,\|\, m)"
                            r" + \tfrac12 \mathrm{KL}(q \,\|\, m)$, \ with $m$ the average of $p$ and $q$: \ "
                            r"symmetric, \ between $0$ and $\log 2$, \ zero only when $q = p$", width=8.2,
                            font_size=24).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now put the best discriminator back into the value. <bookmark mark='a'/> Divide p plus q by two inside "
            "each log, and two KL divergences appear, from p and from q to their average m, minus log four. "
            "<bookmark mark='b'/> Together they make the Jensen-Shannon divergence: symmetric, never more than log "
            "two, and zero exactly when q equals p. <bookmark mark='c'/> So against a perfect critic, the "
            "generator is minimizing a divergence between its distribution and the data's, without ever writing "
            "down a density. That is the theorem of the 2014 paper. Whether training actually finds that minimum "
            "is a different question, and it is the rest of this chapter and the next."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(d, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def saturation(self):
        g2 = load("gan2d")
        ax = axes([0, 1], [-1, 4], x_length=5.0, y_length=3.4, xlabel=r"$D(G(z))$: \ how real the fake looks",
                  ylabel=r"generator's loss", xticks=[0, 0.5, 1], yticks=[0, 2, 4], center=[-3.5, -0.3, 0])
        xs = np.linspace(0.005, 0.995, 200)
        mm = curve(ax.ax, xs, np.log(1 - xs), GREY_A, 3)
        ns = curve(ax.ax, xs, -np.log(xs), GAN_C, 3)
        lg = legend([(GREY_A, r"minimax: \ $\log(1 - D)$"), (GAN_C, r"non-saturating: \ $-\log D$")], font_size=20)
        lg.next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        hl = Rectangle(width=ax.ax.c2p(0.1, 0)[0] - ax.ax.c2p(0, 0)[0], height=3.4, stroke_width=0,
                       fill_color=C.SURPRISE, fill_opacity=0.12).move_to(ax.ax.c2p(0.05, 1.5))
        hlt = label(r"early on: \ here", font_size=18, color=C.SURPRISE).next_to(hl, UP, buff=0.05)
        gm = np.asarray(g2["mm_gnorm"])
        gn = np.asarray(g2["ns_gnorm"])
        rmax = float(max(gm[:, 1].max(), gn[:, 1].max()) * 1.15)
        g = axes([0, gm[-1, 0]], [0, rmax], x_length=4.6, y_length=2.6, xlabel=r"training step",
                 ylabel=r"generator's gradient norm", xticks=[0, gm[-1, 0]], yticks=[0],
                 center=[3.4, 0.6, 0])
        cm, cn = curve(g.ax, gm[:, 0], gm[:, 1], GREY_A, 3), curve(g.ax, gn[:, 0], gn[:, 1], GAN_C, 3)
        ratio = float(gn[:5, 1].mean() / max(gm[:5, 1].mean(), 1e-12))
        if ratio > 1.5:
            meas = (f"Measured on the ring, in the first steps of training, the non-saturating generator's "
                    f"gradient is {ratio:.1f} times larger than the minimax one's.")
        else:
            fac = max(ratio, 1 / max(ratio, 1e-9))
            meas = (f"Measured on the ring, in the first steps, the two gradients are within a factor of {fac:.1f}: "
                    "our discriminator never gets confident enough, early on, for the difference to bite.")
        rk = cmath(r"\nabla_\theta\, \mathbb E_q[-\log D^*]", r"=", r"\nabla_\theta\big[\mathrm{KL}(q \,\|\, p) - 2\, "
                   r"\mathrm{JS}(p \,\|\, q)\big]", font_size=30).move_to([2.6, -2.1, 0])
        rk[2].set_color(C.KL)
        rkl = label(r"reverse KL: \ cheap to miss a mode, \ costly to invent one", font_size=20, color=C.KL)
        rkl.next_to(rk, DOWN, buff=0.12)
        cite_ = cite(r"Arjovsky \& Bottou (2017)", corner=DR)
        with self.voiceover(
            "The first practical problem appears on day one. Early in training the fakes are bad, the "
            "discriminator rejects them with confidence, and D of G of z sits near zero. <bookmark mark='a'/> "
            "There, the minimax loss, log of one minus D, is flat: the generator gets almost no gradient exactly "
            "when it needs one most. <bookmark mark='b'/> Goodfellow's fix, in the same paper, flips the "
            "generator's goal: instead of minimizing the probability of being caught, maximize the probability of "
            "fooling, minus log D. Same fixed point, steep where the other is flat. <bookmark mark='c'/> "
            f"{meas} <bookmark mark='d'/> But the fix has a cost, found by Martin Arjovsky and Leon Bottou in "
            "2017: its gradient is that of a reverse KL divergence minus the Jensen-Shannon term. Reverse KL "
            "barely penalizes missing a mode, and heavily penalizes putting mass where the data has none."
        ) as vo:
            self.play(FadeIn(ax), Create(mm), FadeIn(lg[0]))
            vo.wait_until("a")
            self.play(FadeIn(hl), FadeIn(hlt))
            vo.wait_until("b")
            self.play(Create(ns), FadeIn(lg[1]))
            vo.wait_until("c")
            self.play(FadeIn(g), Create(cm), Create(cn))
            vo.wait_until("d")
            self.play(Write(rk), FadeIn(rkl), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ring(self):
        g, t = load("gan2d"), load("toys")
        pl = Plane(4.4, center=[-3.3, -0.2, 0])
        truth = VGroup(*[Circle(radius=3 * 0.1 * pl.side / 6, stroke_color=DATA, stroke_width=1.5).move_to(pl.p(*c))
                         for c in np.asarray(t["ring_centers"])])
        head = label(r"non-saturating GAN on the ring, \ seed $0$", font_size=22, color=GAN_C).next_to(pl, UP,
                                                                                                    buff=0.12)
        key = VGroup(label(r"background: \ $D$ \ (bright = ``real'')", font_size=18, color=DISC),
                     label(r"dots: \ $300$ samples, \ the same $z$ throughout", font_size=18, color=GAN_C),
                     label(r"circles: \ the data's eight modes, \ $3\sigma$", font_size=18, color=DATA))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(pl, DOWN, buff=0.15)
        ml = label(r"modes covered, \ of $8$", font_size=22, color=GREY_A).move_to([1.2, 1.6, 0])
        sl = label(r"step", font_size=20, color=GREY_A).move_to([1.2, 0.4, 0])
        fin = {k: list(g[f"{k}_final_modes"]) for k in ("mm", "ns")}
        names = {"mm": r"minimax", "ns": r"non-saturating"}
        dots_ = VGroup()
        for row, k in enumerate(("mm", "ns")):
            nm = label(names[k], font_size=22, color=GREY_A if k == "mm" else GAN_C).move_to([2.6, -1.0 - 0.7 * row,
                                                                                            0], aligned_edge=RIGHT)
            for s, m in enumerate(fin[k]):
                dots_.add(Dot([3.2 + 0.4 * m, -1.0 - 0.7 * row + 0.12 * (s - 2), 0], radius=0.07,
                              color=GREY_A if k == "mm" else GAN_C))
            dots_.add(nm)
        axis = VGroup(Line([3.2, -2.5, 0], [6.4, -2.5, 0], color=GREY_C, stroke_width=1.5),
                      *[MathTex(str(m), font_size=20, color=GREY_B).move_to([3.2 + 0.4 * m, -2.75, 0]) for m in (0, 4,
                                                                                                                 8)])
        al = label(r"modes covered at the end, \ $5$ seeds each", font_size=20, color=GREY_A).move_to([4.6, -0.3, 0])
        mean_ns, mean_mm = float(np.mean(fin["ns"])), float(np.mean(fin["mm"]))
        full_ns = sum(1 for m in fin["ns"] if m == 8)
        full_mm = sum(1 for m in fin["mm"] if m == 8)
        ns_modes = list(g["ns_frame_modes"])
        hop = ("It covers a few modes at a time, and the set it covers keeps changing: the generator chases the "
               "places where the discriminator is weakest, and the discriminator follows." if max(ns_modes) < 8 else
               "At times it reaches all eight, then loses some again: the generator chases the places where the "
               "discriminator is weakest, and the discriminator follows.")
        if mean_ns < mean_mm:
            cmp_ = (f"Over five seeds, the non-saturating GAN ends with {mean_ns:.1f} of the eight modes on average, "
                    f"and covers all eight in {full_ns} of them; the minimax loss, with the gradient problem but "
                    f"without the reverse KL, ends with {mean_mm:.1f}, all eight in {full_mm}. Adam rescales the "
                    "small gradients, which rescues the minimax loss here, and the reverse KL shows.")
        else:
            cmp_ = (f"Over five seeds, the non-saturating GAN ends with {mean_ns:.1f} of the eight modes on average, "
                    f"all eight in {full_ns}; the minimax loss with {mean_mm:.1f}, all eight in {full_mm}.")
        with self.voiceover(
            "Here is that cost on the ring of eight. The background is the discriminator's verdict on the plane, "
            "bright where it says real; the dots are the generator's samples, from the same three hundred noise "
            "vectors at every checkpoint. <bookmark mark='a'/> Watch it train. " + hop + " <bookmark mark='b'/> "
            "This is mode collapse: a generator that makes only a few kinds of thing. <bookmark mark='c'/> " + cmp_
        ) as vo:
            self.play(FadeIn(pl), FadeIn(truth), FadeIn(head), FadeIn(key), FadeIn(ml), FadeIn(sl))
            vo.wait_until("a")
            img, dots, cnt, stp = replay_gan(self, g, "ns", pl, max(6.0, vo.until("b") + 2.0), [1.2, 1.0, 0])
            vo.wait_until("b")
            self.play(Indicate(cnt, color=GAN_C))
            vo.wait_until("c")
            self.play(FadeIn(al), FadeIn(axis), LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in dots_], lag_ratio=0.08))
        self.wait(0.3)
        self.clear_scene()
