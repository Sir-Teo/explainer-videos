from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import HIST, NCOL, PART, QUANT, SP, load, predict_card, takeaway_card

LEN_COLORS = {1: "#7FD3FF", 2: C.INTERVAL, 4: C.BITS, 8: C.SURPRISE}


class Emerge(VoiceoverScene):
    def construct(self):
        self.card()
        self.mirage()
        self.predict()
        self.ours()
        self.real()
        self.takeaway()

    def card(self):
        card = chapter_card(14, r"Emergence, or a mirage?", r"Do abilities appear suddenly with scale?", lit=(2022,),
                            part=PART)
        with self.voiceover("Chapter fourteen. Emergence, or a mirage?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def mirage(self):
        dfn = definition_card(r"an emergent ability", r"not present in smaller models, \ present in larger ones: \ so it "
                              r"cannot be predicted by extrapolating the smaller ones \ (Wei et al., 2022)", width=6.4,
                              font_size=22, color=SP).to_corner(UL, buff=0.35)
        # the arithmetic of exact match: if every token is right with probability p, all L are right with p^L
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 1, 0.25], x_length=4.6, y_length=3.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.6, 0.6, 0])
        ps = np.linspace(0, 1, 100)
        fam = VGroup(*[curve(ax, ps, ps ** L, LEN_COLORS[L], 3, smooth=True) for L in (1, 2, 4, 8)])
        fl = VGroup(*[MathTex(rf"p^{{{L}}}", font_size=24, color=LEN_COLORS[L]).next_to(ax.c2p(0.92, 0.92 ** L), LEFT, buff=0.1)
                      for L in (1, 2, 4, 8)])
        xl = label(r"$p$: \ each token right", font_size=20, color=GREY_A).next_to(ax, DOWN, buff=0.1)
        yl = label(r"all $L$ tokens right", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.1)
        cards = VGroup(
            history_card(2022, r"Wei et al.\ (Google)", r"abilities that seemed to switch on with scale: \ "
                         r"arithmetic, \ word puzzles, \ multi-step questions \ (a later list counted $137$)", width=5.8,
                         color=HIST),
            history_card(2023, r"Schaeffer, Miranda \& Koyejo (Stanford)", r"most of them were scored by exact match "
                         r"or multiple choice; \ with a smooth score, \ the jumps disappear", width=5.8, color=HIST))
        cards.arrange(DOWN, buff=0.2).move_to([-3.4, -1.6, 0])
        with self.voiceover(
            "In 2022, Jason Wei and colleagues at Google collected abilities that seemed to switch on with scale: "
            "absent in smaller models, present in larger ones, and so not predictable from the smaller ones. They "
            "called them emergent. <bookmark mark='a'/> In 2023, Rylan Schaeffer, Brando Miranda and Sanmi Koyejo at "
            "Stanford pointed at how they were scored. Most were graded all or nothing: is the whole answer exactly "
            "right? <bookmark mark='b'/> If each token is right with probability p, an answer of L tokens is right "
            "with probability p to the L. A steady rise in p becomes, for long answers, a curve that lies flat and "
            "then shoots up. <bookmark mark='c'/> Score the same models smoothly, and the jumps disappear: a "
            "mirage, they said, made by the metric."
        ) as vo:
            self.play(FadeIn(dfn, shift=UP * 0.1), FadeIn(cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(LaggedStart(*[Create(c_) for c_ in fam], lag_ratio=0.3), FadeIn(fl), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ours(self):
        e = load("emerge")
        N = np.asarray(e["N"], float)
        lx = np.log10(N)
        acc = np.asarray(e["char_acc"], float)
        exact = np.asarray(e["exact"], float)  # widths x lengths
        closs = np.asarray(e["char_loss"], float)
        x0, x1 = lx.min() - 0.1, lx.max() + 0.1
        pans = VGroup()
        specs = [(r"per character: \ right guesses", [(acc, C.TRUE_P, r"")]),
                 (r"exact match, \ greedy, \ $L$ characters",
                  [(exact[:, L - 1], LEN_COLORS[L], rf"L={L}") for L in (1, 2, 4, 8)])]
        for k, (ttl, series) in enumerate(specs):
            ax = CornerAxes(x_range=[x0, x1, 1], y_range=[0, 1, 0.25], x_length=5.2, y_length=3.7, tips=False,
                            axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04})
            ax.move_to([-3.5 + 6.9 * k, -0.55, 0])
            xt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.08)
                          for v in range(math.ceil(x0), math.floor(x1) + 1)])
            yt = VGroup(*[MathTex(rf"{int(100 * v)}\%", font_size=20, color=GREY_B).next_to(ax.c2p(x0, v), LEFT, buff=0.08)
                          for v in (0, 0.5, 1)])
            xn = label(r"parameters", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.08)
            t = label(ttl, font_size=24, color=WHITE).next_to(ax, UP, buff=0.15)
            lines = VGroup()
            for v, col, nm in series:
                lines.add(VGroup(curve(ax, lx, v, col, 3.5), *[Dot(ax.c2p(a, b), radius=0.05, color=col) for a, b in zip(lx, v)]))
                if nm:
                    lines[-1].add(MathTex(nm, font_size=20, color=col).next_to(ax.c2p(lx[-1], v[-1]), RIGHT, buff=0.08))
            pans.add(VGroup(ax, xt, yt, xn, t, lines))
        task = label(rf"the checkable task: \ from ${int(e['task_n']):,}$ held-out places, \ write the next characters "
                     r"exactly".replace(",", "{,}"), font_size=22, color=GREY_A).to_edge(UP, buff=0.3)
        tag = note(rf"computed: \ every width of the sweep, \ trained on $2^{{22}}$ characters").to_corner(DL, buff=0.2)
        # growth across our sizes, from a straight-line fit of log score against log size (exact match floored at
        # one problem in task_n, so a single lucky hit cannot set the ratio)
        lx_ = np.log10(N)

        def growth(v):
            v = np.maximum(v, 1 / float(e["task_n"]))
            return float(10 ** (np.polyfit(lx_, np.log10(v), 1)[0] * (lx_[-1] - lx_[0])))

        g1, g8 = growth(acc), growth(exact[:, 7])
        said1 = (
            f"Yet in proportion they grow fastest: {g8:.0f} times across our sizes, against {g1:.1f} times for "
            "single characters. " if g8 > 3 * g1 else
            "In proportion they grow about as fast as single characters. "
        )
        # where our models sit on the p^L curves
        bx = Axes(x_range=[0, 1, 0.25], y_range=[0, 1, 0.25], x_length=4.2, y_length=3.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.5, -0.75, 0])
        ps = np.linspace(0, 1, 100)
        fam = VGroup(*[curve(bx, ps, ps ** L, LEN_COLORS[L], 2.5, smooth=True) for L in (1, 2, 4, 8)])
        fml = VGroup(*[MathTex(rf"p^{{{L}}}", font_size=20, color=LEN_COLORS[L]).next_to(bx.c2p(0.93, 0.93 ** L), LEFT, buff=0.08)
                       for L in (1, 2, 4, 8)])
        band = Rectangle(width=bx.c2p(acc[-1], 0)[0] - bx.c2p(acc[0], 0)[0], height=bx.c2p(0, 1)[1] - bx.c2p(0, 0)[1],
                         stroke_width=0, fill_color=C.TRUE_P, fill_opacity=0.22)
        band.move_to([(bx.c2p(acc[0], 0)[0] + bx.c2p(acc[-1], 0)[0]) / 2, bx.c2p(0, 0.5)[1], 0])
        bl = label(r"our models", font_size=20, color=C.TRUE_P).next_to(band, UP, buff=0.06)
        bxl = label(r"$p$: \ each character right", font_size=18, color=GREY_A).next_to(bx, DOWN, buff=0.08)
        pic = VGroup(bx, fam, fml, band, bl, bxl)
        with self.voiceover(
            "We can watch it happen on our own models. The task: from two thousand places in held-out text, write the "
            "next characters exactly. <bookmark mark='a'/> Score each character on its own, and the share right "
            f"rises smoothly with size, from {100 * acc[0]:.0f} to {100 * acc[-1]:.0f} percent. "
            "<bookmark mark='b'/> Score whole answers instead. One character: the same curve. Two, four, eight: "
            "lower and flatter, until eight-character answers barely leave zero. "
            + said1
            + f"<bookmark mark='c'/> On the curves of p to the L, our models sit on the flat stretch, p between "
            f"{100 * acc[0]:.0f} and {100 * acc[-1]:.0f} percent. The steep part needs p near one: a model scored "
            "like this on long answers seems unable to do them at all, until, much larger, it suddenly can."
        ) as vo:
            self.play(FadeIn(task), FadeIn(tag), *[FadeIn(p[:5]) for p in pans])
            vo.wait_until("a")
            self.play(Create(pans[0][5]), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l_) for l_ in pans[1][5]], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeOut(pans[0]))
            self.play(Create(bx), FadeIn(bxl), LaggedStart(*[Create(c_) for c_ in fam], lag_ratio=0.2), FadeIn(fml),
                      run_time=1.5)
            self.play(FadeIn(band), FadeIn(bl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def real(self):
        q = load("quanta")
        widths = [int(w) for w in q["widths"]]
        per = np.asarray(q["per_task"], float)  # W x seeds x T x tasks
        Np = np.asarray(q["n_params"], float)
        fin = per[:, :, -1, :].mean(1)  # W x tasks: each subtask's loss at the end
        lx = np.log10(Np)
        ax = CornerAxes(x_range=[lx.min() - 0.1, lx.max() + 0.1, 1], y_range=[0, 1.1, 0.5], x_length=5.6, y_length=3.6,
                        tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04})
        ax.move_to([-3.4, -0.5, 0])
        xt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.08)
                      for v in range(math.ceil(lx.min() - 0.1), math.floor(lx.max() + 0.1) + 1)])
        xn = label(r"parameters", font_size=20, color=GREY_A).next_to(xt if len(xt) else ax, DOWN, buff=0.08)
        yn = label(r"each subtask's loss at the end \ (bits)", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        T = fin.shape[1]
        sel = [0, 3, 7, 12, 20] if T > 20 else list(range(min(5, T)))
        lines = VGroup(*[curve(ax, lx, np.minimum(fin[:, k], 1.1), interpolate_color(ManimColor(QUANT), ManimColor(C.BITS), j / 4), 3)
                         for j, k in enumerate(sel)])
        mean = curve(ax, lx, np.minimum(np.asarray(q["mean"], float)[:, :, -1].mean(1), 1.1), WHITE, 4)
        lg = VGroup(label(r"coloured: \ five subtasks, \ common to rare", font_size=20, color=QUANT),
                    label(r"white: \ the average", font_size=20, color=WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        lg.next_to(ax.c2p(lx.max() + 0.05, 1.08), DL, buff=0.1)
        cards = VGroup(
            history_card(2024, r"Du, Zeng, Dong \& Tang", r"abilities appear when the pretraining loss falls below a "
                         r"threshold, \ whatever the model's size", width=5.6, color=HIST),
            history_card(2024, r"Snell, Wallace, Klein \& Levine", r"fine-tuning makes an ability appear in smaller "
                         r"models, \ so it can be forecast, \ up to about $4\times$ the compute", width=5.6, color=HIST),
        ).arrange(DOWN, buff=0.2).move_to([3.5, -0.3, 0])
        # right, from the start: every subtask (rows, common to rare) at every width (columns), bright while unsolved
        cw, chh = 0.5, min(0.11, 3.6 / T)
        grid = VGroup(*[Rectangle(width=cw, height=chh, stroke_width=0.5, stroke_color=BLACK,
                                  fill_color=interpolate_color(ManimColor("#1d2530"), ManimColor(QUANT), float(np.clip(fin[i, k], 0, 1))),
                                  fill_opacity=1.0).move_to([2.2 + cw * i, 1.3 - chh * k, 0])
                        for i in range(len(widths)) for k in range(T)])
        gx = VGroup(*[MathTex(str(w), font_size=18, color=GREY_B).next_to(grid[i * T + T - 1], DOWN, buff=0.08)
                      for i, w in enumerate(widths)])
        gxn = label(r"width", font_size=20, color=GREY_A).next_to(gx, DOWN, buff=0.08)
        gyn = VGroup(label(r"common", font_size=18, color=GREY_A).next_to(grid[0], LEFT, buff=0.1),
                     label(r"rare", font_size=18, color=GREY_A).next_to(grid[T - 1], LEFT, buff=0.1))
        gt = label(r"each subtask (row) at each width (column): \\ bright $=$ unsolved, \ dark $=$ learned", font_size=20,
                   color=GREY_A)
        gt.next_to(grid, UP, buff=0.12).align_to(grid, LEFT)
        heat = VGroup(grid, gx, gxn, gyn, gt)
        drops = []
        for k in sel:
            v = fin[:, k]
            tot = v[0] - v[-1]
            if tot > 0.3:
                drops.append(float(np.max(v[:-1] - v[1:]) / tot))
        cliff = len(drops) >= 3 and float(np.mean(drops)) > 0.5
        said2 = (
            f"and it falls off a cliff at its own size: on average {100 * np.mean(drops):.0f} percent of the fall "
            "happens between two neighbouring sizes, the common subtasks first. " if cliff else
            "and each one falls at its own size, more steeply than the average, the common subtasks first. "
        )
        with self.voiceover(
            "But some suddenness is real. In the quanta toy, each subtask is either solved or not. Plot each one's "
            "final loss against the network's size, "
            + said2
            + "<bookmark mark='a'/> Only the average is smooth. A benchmark that measures one narrow skill sees "
            "a cliff; the loss, which averages over everything, sees a power law. <bookmark mark='b'/> Later work "
            "made this useful. In 2024 Zhengxiao Du and colleagues found that abilities appear when the pretraining "
            "loss falls below a threshold, whatever the size of the model, and Charlie Snell and colleagues showed "
            "that fine-tuning brings an ability forward to smaller models, so its arrival can be forecast."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(xn), FadeIn(yn), FadeIn(heat[1:]))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3), FadeIn(lg[0]),
                      LaggedStart(*[FadeIn(c_) for c_ in grid], lag_ratio=0.004), run_time=2.5)
            vo.wait_until("a")
            self.play(Create(mean), FadeIn(lg[1]))
            vo.wait_until("b")
            self.play(FadeOut(heat))
            self.play(LaggedStart(*[FadeIn(c_, shift=LEFT * 0.1) for c_ in cards], lag_ratio=0.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def predict(self):
        pc = predict_card(r"Our models' accuracy on single characters rises smoothly with size. \ Score them on "
                          r"getting $8$ characters exactly right instead: \ what does the curve look like?")
        with self.voiceover(
            "Pause and predict. Our models' accuracy on single characters rises smoothly with size. Score them on "
            "getting eight characters exactly right instead. What does that curve look like?"
        ):
            self.play(FadeIn(pc, shift=UP * 0.2))
        self.wait(2.0)
        self.play(FadeOut(pc))

    def takeaway(self):
        tk = takeaway_card(r"Smooth loss, \ sudden scores",
                           r"All-or-nothing scores turn steady progress into apparent jumps; \ narrow skills can "
                           r"truly switch on; \ the loss underneath is smooth and forecastable.",
                           r"next: \ the strangest jump of all")
        with self.voiceover(
            "The takeaway: all-or-nothing scores turn steady progress into apparent jumps, while narrow skills can "
            "still truly switch on. Either way, the loss underneath is smooth, and can be forecast. Next, the "
            "strangest jump of all."
        ) as vo:
            self.play(FadeIn(tk[0], shift=UP * 0.2))
            self.wait(max(0.0, vo.duration * 0.5 - 1.0))
            self.play(FadeIn(tk[1]))
        self.wait(0.4)
        self.play(FadeOut(tk))
