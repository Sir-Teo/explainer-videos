from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import AUSTEN, DICKENS, TEST, TRAIN, curve, load


class RandomLabels(VoiceoverScene):
    def construct(self):
        self.card()
        self.experiment()
        self.order()

    def card(self):
        card = chapter_card(3, r"Memorizing nonsense", r"Can a network fit random labels?", part=8)
        with self.voiceover("Chapter three. Memorizing nonsense."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def experiment(self):
        r = load("random")
        T, S = np.asarray(r["true"]), np.asarray(r["shuffled"])
        n, n_params = int(r["n"]), int(r["n_params"])
        # the labels, as a strip of coloured pages, then shuffled
        from videos.ai.ai6 import compute as c5

        pg = c5.load("pages")
        y = np.asarray(pg["y"])[~np.asarray(pg["test"], bool)]
        g = np.random.default_rng(2017)
        perm = g.permutation(len(y))
        cols = 32
        cells = VGroup(*[Square(0.13, stroke_width=0, fill_color=AUSTEN if v == 0 else DICKENS, fill_opacity=0.9)
                         for v in y])
        cells.arrange_in_grid(cols=cols, buff=0.025).move_to([0, 2.25, 0])
        cl = label(rf"the ${n}$ training pages, \\ coloured by author", font_size=24, color=GREY_A).next_to(cells, LEFT, buff=0.4)
        net = label(rf"one network: \ $70 \to 512 \to 512 \to 2$, \ ${n_params:,}$ weights".replace(",", "{,}"),
                    font_size=26, color=WHITE).next_to(cells, DOWN, buff=0.3)
        panels = VGroup()
        for k, (D, title) in enumerate(((T, r"true authors"), (S, r"shuffled authors"))):
            ax = Axes(x_range=[0, 3.2, 1], y_range=[0.4, 1.0, 0.1], x_length=5.4, y_length=2.3, tips=False,
                      axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04})
            ax.move_to([-3.4 + 6.8 * k, -1.55, 0])
            lx = np.log10(D[:, 0])
            ctr, cte = curve(ax, lx, D[:, 1], TRAIN, 3), curve(ax, lx, D[:, 2], TEST, 4)
            yl = VGroup(*[MathTex(rf"{int(round(100 * v))}\%", font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.08)
                          for v in (0.5, 0.75, 1.0)])
            xl = VGroup(*[MathTex(t, font_size=20, color=GREY_B).next_to(ax.c2p(v, 0.4), DOWN, buff=0.08)
                          for t, v in (("1", 0), ("10", 1), ("100", 2), ("1{,}000", 3))])
            t = label(title, font_size=28, color=WHITE).next_to(ax, UP, buff=0.15)
            yl_ = D[-1, 2] - 0.13 if D[-1, 2] > 0.8 else D[-1, 2] + 0.1
            end = label(rf"new pages: \ ${100 * D[-1, 2]:.0f}\%$", font_size=26, color=TEST).move_to(ax.c2p(2.5, yl_))
            panels.add(VGroup(ax, yl, xl, t, ctr, cte, end))
        key = VGroup(label(r"training pages right", font_size=22, color=TRAIN),
                     label(r"new pages right", font_size=22, color=TEST)).arrange(RIGHT, buff=0.5)
        key.next_to(panels, DOWN, buff=0.2)
        key.add(label(r"(training steps on a log scale)", font_size=20, color=GREY_B)).arrange(RIGHT, buff=0.5)
        key.next_to(panels, DOWN, buff=0.2)
        # the network as four boxes, as tall as their layers are wide (on a square-root scale, so 2 still shows)
        widths = (70, 512, 512, 2)
        boxes = VGroup(*[VGroup(Rectangle(width=0.5, height=0.08 * w ** 0.5, stroke_color=C.NEURAL, stroke_width=2,
                                          fill_color=C.NEURAL, fill_opacity=0.25),
                                MathTex(str(w), font_size=26, color=WHITE)) for w in widths]).arrange(RIGHT, buff=0.7)
        for b in boxes:
            b[1].next_to(b[0], DOWN, buff=0.1).set_y(boxes[1][0].get_bottom()[1] - 0.25)
        boxes.add(*[Arrow(boxes[i][0].get_right(), boxes[i + 1][0].get_left(), buff=0.08, color=GREY_B,
                          stroke_width=2.5, max_tip_length_to_length_ratio=0.3) for i in range(3)])
        arch = gloss(r"$70 \to 512 \to 512 \to 2$", r"layers of simple units: \ $70$ word rates in, \\ two layers "
                     r"of $512$, \ $2$ outputs \ (one per author)", boxes, width=4.6, color=C.NEURAL)
        arch.move_to([3.4, -1.45, 0])
        cite_ = cite(r"C.~Zhang, S.~Bengio, M.~Hardt, B.~Recht \& O.~Vinyals, \textit{Understanding Deep Learning Requires "
                     r"Rethinking Generalization} (2017)", corner=UR)
        with self.voiceover(
            "In 2016, Chiyuan Zhang and colleagues ran an experiment that broke the classical picture. Take a "
            "network: layers of simple units, here the seventy word rates in, two layers of five hundred and twelve "
            f"units, and two outputs, one per author. That's about {round(n_params, -3) // 1000} thousand weights. "
            f"Train it on the {n} training pages with their true authors. <bookmark mark='a'/> It fits all of them, and gets "
            f"{100 * T[-1, 2]:.1f} percent of new pages right. <bookmark mark='b'/> Now shuffle the authors, so "
            "every label is random. Same network, same training."
        ) as vo:
            self.play(FadeIn(cl), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.002), FadeIn(net), FadeIn(cite_),
                      run_time=1.8)
            self.play(*[FadeIn(m) for m in panels[0][:4]], FadeIn(key), FadeIn(arch))
            vo.wait_until("a")
            self.play(Create(panels[0][4]), Create(panels[0][5]), run_time=2.0)
            self.play(FadeIn(panels[0][6]))
            vo.wait_until("b")
            self.play(FadeOut(arch))
            self.play(*[c.animate.set_fill(AUSTEN if y[perm[i]] == 0 else DICKENS) for i, c in enumerate(cells)],
                      run_time=1.5)
        with self.voiceover(
            "It fits these too, every one of them, only a little more slowly. It has memorized nonsense. "
            "<bookmark mark='a'/> And on new pages, it's at chance, as it must be. <bookmark mark='b'/> So the same "
            "network can memorize anything at all. Then counting what a model could fit can't explain why, given "
            "real labels, it finds a rule that works on new pages instead. Something in how it's trained prefers "
            "simple answers. Why, exactly, is still being worked out."
        ) as vo:
            self.play(*[FadeIn(m) for m in panels[1][:4]])
            self.play(Create(panels[1][4]), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(panels[1][5]), run_time=1.5)
            self.play(FadeIn(panels[1][6]))
            vo.wait_until("b")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def order(self):
        """The order of memorizing: which shuffled pages the network gets right, step by step, split by whether the
        shuffled author happens to be the true one."""
        r = load("random")
        F = np.asarray(r["fits_shuffled"]).astype(bool)  # (logged steps, pages)
        lab, yt = np.asarray(r["labels_shuffled"]), np.asarray(r["ytrue"])
        steps = np.asarray(r["shuffled"])[:, 0]
        agree = lab == yt
        ya, yd = F[:, agree].mean(1), F[:, ~agree].mean(1)
        full = int(np.argmax((ya >= 1) & (yd >= 1)))  # the first logged step with every page fit
        kmax = min(full + 2, len(steps) - 1)  # all the action is in the first few dozen steps
        lmax = float(np.log10(steps[kmax]))
        n = len(lab)
        # pages sorted into two blocks: shuffled label = true author (left), and not (right)
        cols = 16
        ia, idis = np.where(agree)[0], np.where(~agree)[0]

        def block(idx, x0):
            g = VGroup(*[Square(0.14, stroke_width=0, fill_color=AUSTEN if lab[i] == 0 else DICKENS, fill_opacity=0.15)
                         for i in idx])
            g.arrange_in_grid(cols=cols, buff=0.03)
            return g.move_to([x0, 1.2, 0]).align_to([0, 2.9, 0], UP)

        ga, gd = block(ia, -3.4), block(idis, 3.4)
        ha = label(rf"${len(ia)}$ pages whose shuffled author \\ happens to be the true one", font_size=22, color=GREY_A)
        hd = label(rf"${len(idis)}$ pages whose shuffled author \\ is wrong", font_size=22, color=GREY_A)
        ha.next_to(ga, UP, buff=0.15)
        hd.next_to(gd, UP, buff=0.15)
        # the share of each block fit, against steps (log scale)
        ax = Axes(x_range=[0, lmax, 1], y_range=[0, 1.0, 0.25], x_length=7.4, y_length=2.2, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([0, -2.35, 0])
        lx = np.log10(steps)
        xt = VGroup(*[MathTex(t_, font_size=20, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.08)
                      for t_, v in (("1", 0), ("10", 1), ("100", 2), ("1{,}000", 3)) if v <= lmax])
        xt.add(label(r"steps \ (log scale)", font_size=18, color=GREY_B).next_to(ax.c2p(lmax, 0), DOWN, buff=0.3))
        yt_ = VGroup(*[MathTex(rf"{int(100 * v)}\%", font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.08)
                       for v in (0, 0.5, 1.0)])
        key_ = VGroup(label(r"share right: \ true-by-chance pages", font_size=18, color=TRAIN),
                      label(r"share right: \ the others", font_size=18, color=C.SURPRISE)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        key_.next_to(ax, RIGHT, buff=0.3).align_to(ax, UP)
        t = ValueTracker(0)

        def part(ys, col):
            k = int(t.get_value())
            pts = [ax.c2p(lx[i], ys[i]) for i in range(k + 1)]
            return VMobject(color=col, stroke_width=3.5).set_points_as_corners(pts if len(pts) > 1 else pts * 2)

        ca = always_redraw(lambda: part(ya, TRAIN))
        cd = always_redraw(lambda: part(yd, C.SURPRISE))
        cnt = always_redraw(lambda: MathTex(rf"\text{{step }}{int(steps[int(t.get_value())]):,}".replace(",", "{,}"),
                                            font_size=26, color=WHITE).next_to(ax, RIGHT, buff=0.3).shift(DOWN * 0.3))

        def fill(k):
            anims = []
            for g, idx in ((ga, ia), (gd, idis)):
                for sq, i in zip(g, idx):
                    anims.append(sq.animate.set_fill(opacity=0.95 if F[k, i] else 0.15))
            return anims

        gap = [float(ya[k] - yd[k]) for k in range(full + 1)]
        kg = int(np.argmax(gap))  # where the pages with a true label lead the most
        early = gap[kg] > 0.08
        ks = list(range(1, kmax + 1))
        with self.voiceover(
            "In what order does it memorize? Split the shuffled pages in two: by chance, about half got their true "
            "author back, and the rest a wrong one. <bookmark mark='a'/> A page lights up when the network gets its "
            "shuffled label right. "
            + (f"<bookmark mark='b'/> In the first few steps, the pages whose label happens to be true pull ahead: by "
               f"step {int(steps[kg])}, {100 * ya[kg]:.0f} percent of them are right, against {100 * yd[kg]:.0f} percent "
               "of the others. The network starts by learning the real difference between the authors. Then it "
               f"memorizes the rest, and by step {int(steps[full])} every page, true or not, is fit. "
               if early else
               f"<bookmark mark='b'/> Both halves are fit at much the same pace, every page by step "
               f"{int(steps[full])}: here the network memorizes without first picking up the real pattern. ")
            + f"With {int(r['n_params']):,} weights for {len(lab)} pages, memorizing is quick."
        ) as vo:
            self.play(FadeIn(ga), FadeIn(gd), FadeIn(ha), FadeIn(hd), Create(ax), FadeIn(xt), FadeIn(yt_), FadeIn(key_))
            self.add(ca, cd, cnt)
            vo.wait_until("a")
            self.play(*fill(0))
            vo.wait_until("b")
            for k in ks:
                self.play(*fill(k), t.animate.set_value(k), run_time=0.9, rate_func=linear)
        self.wait(0.5)
        self.remove(ca, cd, cnt)
        self.clear_scene()
