from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai16.common import (F, HISTC, PART, RANDC, REINITC, TICKETC, heat, load, ms, take_away)


class Lottery(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.algorithm()
        self.result()

    def card(self):
        card = chapter_card(14, r"Lottery tickets", r"Is a big network mostly unnecessary?", part=PART)
        with self.voiceover("Chapter fourteen. Lottery tickets."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def history(self):
        cards = VGroup(
            history_card(1990, r"Yann LeCun, John Denker \& Sara Solla", r"\textit{Optimal Brain Damage}: \ remove the "
                         r"weights whose loss the Hessian says is least", width=4.3, color=HISTC),
            history_card(2015, r"Song Han, Jeff Pool, John Tran \& Bill Dally", rf"prune, \ retrain, \ repeat: \ AlexNet "
                         rf"${F.HAN['alexnet']}\times$ smaller, \ VGG-16 ${F.HAN['vgg']}\times$, \ same accuracy", width=4.3,
                         color=HISTC),
            history_card(2018, r"Jonathan Frankle \& Michael Carbin", r"the pruned network trains well \ only from its "
                         r"original starting weights", width=4.3, color=HISTC),
        ).arrange(RIGHT, buff=0.25).move_to([0, 1.2, 0])
        thm = theorem_card(r"the lottery ticket hypothesis", r"A randomly initialized dense network contains a subnetwork "
                           r"that, \ trained in isolation from the same initial weights, \ can match the full network's "
                           r"accuracy in at most the same number of steps.", who=r"Frankle \& Carbin, \ ICLR 2019",
                           kind=r"Conjecture", width=9.0, font_size=22).move_to([0, -1.9, 0])
        with self.voiceover(
            "The third kind of sparsity is the oldest: removing weights. <bookmark mark='a'/> In 1990 Yann LeCun, "
            "John Denker and Sara Solla removed the weights whose loss the Hessian said would hurt least, and called "
            "it optimal brain damage. <bookmark mark='b'/> In 2015 Song Han and colleagues showed how much can go: "
            f"prune the smallest weights, retrain, repeat, and AlexNet shrank {F.HAN['alexnet']} times, VGG "
            f"{F.HAN['vgg']} times, with no loss in accuracy. <bookmark mark='c'/> But a strange thing was known: "
            "the small pruned network, trained from scratch, did worse. In 2018 Jonathan Frankle and Michael Carbin "
            "found that it trains well only from its original starting weights. <bookmark mark='d'/> Their "
            "conjecture: a big random network contains a small subnetwork, a winning lottery ticket, that could have "
            "been trained alone to the same accuracy. The big network is how you buy enough tickets."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(thm, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def algorithm(self):
        d = load("lottery")
        R = int(d["rounds"])
        imgs = np.asarray(d["mask_img_s0"], float)  # rounds, 48, 48
        steps = VGroup(*[label(t, font_size=22, color=c) for t, c in (
            (r"1. \ train the network", WHITE),
            (rf"2. \ remove the ${int(100 * d['rate'][0])}\%$ smallest weights still there \ (${int(100 * d['rate'][2])}\%$ "
             r"of the last layer)", WHITE),
            (rf"3. \ rewind the survivors to their values at step ${int(d['rewind'])}$", TICKETC),
            (r"4. \ train again; \ repeat", WHITE))]).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        alg = definition_card(r"iterative magnitude pruning, \ with rewinding", steps, color=TICKETC, width=7.2,
                              kind=r"Algorithm").move_to([-2.8, 1.2, 0])
        pic = heat(np.ones((48, 48)), width=3.2, height=3.2, color=TICKETC, gamma=1.0, vmax=1.0).move_to([4.2, 0.6, 0])
        frame = SurroundingRectangle(pic, buff=0, color=GREY_C, stroke_width=1.5)
        pl = label(r"a corner of the second layer's weights: \ lit if kept", font_size=18, color=GREY_A).next_to(pic, UP, buff=0.12)
        rem = [float(x) for x in d["remain_s0"]]
        cnt = label(r"round $0$: \ $100\%$ of weights", font_size=22, color=TICKETC).next_to(pic, DOWN, buff=0.2)
        net = label(rf"a ReLU network: \ $3$ characters in, \ two layers of $128$, \ the next character out \ "
                    rf"(${int(d['params_s0']):,}$ weights)".replace(",", "{,}"), font_size=20, color=GREY_A).move_to([-2.8, -1.4, 0])
        ag = label(rf"against: \ the same masks with fresh random weights, \ and random masks of the same size", font_size=20,
                   color=REINITC).next_to(net, DOWN, buff=0.3).align_to(net, LEFT)
        with self.voiceover(
            "How do you find a ticket? Train, prune, rewind, repeat. <bookmark mark='a'/> Train the network; remove "
            f"the {int(100 * d['rate'][0])} percent of weights smallest in size; rewind the survivors to the values they had early in "
            f"training, here at step {int(d['rewind'])}; and train again. Rewinding to a few steps in, rather than "
            "to the very start, was Frankle's later fix for bigger networks. <bookmark mark='b'/> Our network reads "
            "three characters and guesses the next. Here is a corner of its weights, round by round, as the mask "
            f"thins to {100 * rem[-1]:.0f} percent. <bookmark mark='c'/> The tests: the same mask with fresh random "
            "weights, and a random mask of the same size."
        ) as vo:
            self.play(FadeIn(alg, shift=UP * 0.2), FadeIn(pic), Create(frame), FadeIn(pl), FadeIn(cnt))
            vo.wait_until("a")
            self.play(Indicate(alg.body[2], color=TICKETC))
            vo.wait_until("b")
            self.play(FadeIn(net))
            for r in range(R):
                nxt = heat(imgs[r], width=3.2, height=3.2, color=TICKETC, gamma=1.0, vmax=1.0).move_to(pic)
                nc = label(rf"round ${r + 1}$: \ ${100 * rem[r]:.0f}\%$ of weights", font_size=22, color=TICKETC).move_to(cnt)
                self.play(FadeIn(nxt), FadeOut(pic), Transform(cnt, nc), run_time=0.6)
                pic = nxt
            vo.wait_until("c")
            self.play(FadeIn(ag))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def result(self):
        d = load("lottery")
        seeds = [int(s) for s in d["seeds"]]
        rem = np.asarray(d["remain_s0"], float)
        lx = np.log10(np.concatenate([[1.0], rem]))
        data = {k: np.array([[d[f"dense_s{s}"]] + list(d[f"{k}_s{s}"]) for s in seeds], float)
                for k in ("ticket", "reinit", "random")}
        dense = float(np.mean([d[f"dense_s{s}"] for s in seeds]))
        allv = np.concatenate([v.ravel() for v in data.values()])
        y0 = math.floor((allv.min() - 0.02) * 20) / 20
        y1 = min(math.ceil((allv.max() + 0.02) * 20) / 20, y0 + 1.0)
        ax = Axes(x_range=[float(lx.min()) - 0.05, 0.05, 0.25], y_range=[y0, y1, 0.1], x_length=7.6, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-1.8, -0.3, 0])
        ticks = [1.0, 0.5, 0.2, 0.1]
        xt = VGroup(*[MathTex(rf"{int(100 * t)}\%", font_size=20, color=GREY_B).next_to(ax.c2p(math.log10(t), y0), DOWN, buff=0.1)
                      for t in ticks if math.log10(t) >= lx.min() - 0.05])
        yt = VGroup(*[MathTex(f"{v:.1f}", font_size=20, color=GREY_B).next_to(ax.c2p(float(lx.min()) - 0.05, v), LEFT, buff=0.1)
                      for v in np.arange(math.ceil(y0 * 10) / 10, y1 + 1e-9, 0.2)])
        xl = label(r"weights remaining \ (log scale)", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"held-out bits per character \ (two seeds)", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        base = DashedLine(ax.c2p(float(lx.min()) - 0.05, dense), ax.c2p(0.05, dense), color=GREY_B, stroke_width=1.5)
        bl = label(r"the dense network", font_size=18, color=GREY_B).next_to(ax.c2p(float(lx.min()), dense), UP, buff=0.05).align_to(ax, LEFT).shift(RIGHT * 0.1)
        cols = {"ticket": (TICKETC, r"the ticket \ (rewound)"), "reinit": (REINITC, r"same mask, \ fresh weights"),
                "random": (RANDC, r"random mask")}
        lines = {}
        for k, (col, _) in cols.items():
            a = np.clip(data[k], y0, y1)
            lines[k] = VGroup(band(ax, lx, a.min(0), a.max(0), col, 0.2), curve(ax, lx, a.mean(0), col, 3),
                              *[Dot(ax.c2p(x, y), radius=0.04, color=col) for x, y in zip(lx, a.mean(0))])
        names = VGroup(*[label(nm, font_size=22, color=col) for col, nm in cols.values()]).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        names.move_to([4.7, 1.0, 0])
        t, ri, rm = (data[k].mean(0) for k in ("ticket", "reinit", "random"))
        # the sparsest round where the ticket is still within 0.02 bits of the dense network
        ok = [i for i in range(1, len(t)) if t[i] <= dense + 0.02]
        best = max(ok) if ok else None
        if best and (t[1:] < dense - 0.005).any():
            v1 = (f"The ticket stays as good as the dense network down to {100 * rem[best - 1]:.0f} percent of its "
                  "weights, and at some sizes it's even a little better. ")
        elif best:
            v1 = f"The ticket stays as good as the dense network down to {100 * rem[best - 1]:.0f} percent of its weights. "
        else:
            v1 = "Even the ticket loses ground from the first round of pruning. "
        gap = float((ri[-1] - t[-1]))
        v2 = (f"With the same masks but fresh random weights, the network does worse, by {gap:.2f} bits at the "
              "sparsest: the starting weights matter, not just which connections are kept. " if gap > 0.02 else
              "With the same masks but fresh random weights, the network does about as well here: at this small size, "
              "the mask matters more than the starting weights. ")
        v3 = (f"Random masks of the same size do worst of all, {rm[-1]:.2f} bits at the sparsest." if rm[-1] > max(t[-1], ri[-1])
              else f"Random masks of the same size end at {rm[-1]:.2f} bits.")
        ta = take_away(r"winning tickets exist, \ but finding one costs several full trainings", color=TICKETC, font_size=26)
        with self.voiceover(
            "Here are the three, round by round, as the network thins. <bookmark mark='a'/> " + v1
            + "<bookmark mark='b'/> " + v2 + "<bookmark mark='c'/> " + v3 + " <bookmark mark='d'/> The catch: finding "
            f"the smallest ticket took {int(d['rounds']) + 1} full trainings. Lottery tickets changed how people think about why big networks "
            "train well. To save compute in practice, sparsity has to be found cheaply, and has to suit the "
            "hardware: the next chapter."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), Create(base), FadeIn(bl))
            vo.wait_until("a")
            self.play(FadeIn(lines["ticket"]), FadeIn(names[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(lines["reinit"]), FadeIn(names[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(lines["random"]), FadeIn(names[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(ta))
        self.wait(0.3)
        self.clear_scene()
