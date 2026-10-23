from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai10.common import (ADV, CNN, HIST, KERNEL, MLPC, OK, PART, img_gray, img_heat, img_rgb, load,
                                   pct, seed_band)
from videos.ai.ai10.specs import FGSM_PAPER


def classes():
    return list(load("data")["cifar_classes"])


class Adversarial(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.linearity()
        self.digit()
        self.curves()
        self.straight()
        self.photos()
        self.defence()

    def card(self):
        card = chapter_card(9, r"Adversarial examples", r"Can an invisible change fool a network?", lit=(2012,),
                            part=PART)
        with self.voiceover("Chapter nine. Adversarial examples."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def history(self):
        P = FGSM_PAPER
        c1 = history_card(2013, r"Christian Szegedy, Wojciech Zaremba, Ilya Sutskever, Joan Bruna, Dumitru Erhan, "
                          r"Ian Goodfellow \& Rob Fergus", r"\textit{Intriguing properties of neural networks}: \ an "
                          r"imperceptible change makes a network misclassify; \ the same change often fools other "
                          r"networks too", width=6.2, color=HIST)
        c2 = history_card(2014, r"Ian Goodfellow, Jonathon Shlens \& Christian Szegedy",
                          rf"a photograph of a panda, \ ${P['panda']}\%$ panda to GoogLeNet; \ add a pattern of size "
                          rf"$\varepsilon = {P['eps']}$: \ ${P['gibbon']}\%$ gibbon", width=6.2, color=HIST)
        VGroup(c1, c2).arrange(RIGHT, buff=0.35, aligned_edge=UP).move_to(UP * 0.5)
        q = label(r"why are networks so easy to fool?", font_size=32, color=ADV).to_edge(DOWN, buff=0.8)
        cite_ = cite(r"Szegedy et al.\ (2013); \ Goodfellow et al.\ (2014)", corner=DR)
        with self.voiceover(
            "In December 2013, Christian Szegedy and six colleagues, at Google, New York University and the "
            "University of Montreal, reported something strange. <bookmark mark='a'/> For any photograph a "
            "network classified correctly, they could find a tiny change, invisible to a person, that made it "
            "answer something else entirely; and the same change often fooled other networks, trained "
            "separately. <bookmark mark='b'/> A year later Ian Goodfellow, Jonathon Shlens and Szegedy showed a "
            f"panda that GoogLeNet called a panda with {P['panda']} percent confidence. Add a faint pattern, a "
            f"change of {P['eps']} in each pixel, the size of the smallest step of an 8-bit image, and it called "
            f"it a gibbon, with {P['gibbon']} percent. <bookmark mark='c'/> They also gave the explanation."
        ) as vo:
            self.play(FadeIn(c1, shift=UP * 0.2), FadeIn(cite_))
            vo.wait_until("b")
            self.play(FadeIn(c2, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(q))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def linearity(self):
        colors = {r"\eta": ADV, r"\varepsilon": ADV, r"\|w\|_1": KERNEL, r"w": KERNEL}
        rows = [
            cmath(r"w \cdot (x + \eta)", r"=", r"w \cdot x", r"+", r"w \cdot \eta", colors=colors, font_size=40),
            cmath(r"\max_{\|\eta\|_\infty \le \varepsilon} w \cdot \eta", r"=", r"\varepsilon \|w\|_1", r",\quad",
                  r"\eta = \varepsilon\, \mathrm{sign}(w)", colors=colors, font_size=40),
            cmath(r"\varepsilon \|w\|_1", r"\approx", r"\varepsilon\, m\, n", colors=colors, font_size=40),
            cmath(r"\eta", r"=", r"\varepsilon\, \mathrm{sign}\big(\nabla_x J(\theta, x, y)\big)", colors=colors,
                  font_size=40),
        ]
        for r in rows:
            for p in r:
                ts = p.get_tex_string()
                if r"\eta" in ts and "=" not in ts:
                    p.set_color(ADV)
        whys = [why(r"a linear score"), why(r"each $\eta_i = \pm\varepsilon$, \ with the sign of $w_i$"),
                why(r"$n$ inputs, \ average $|w_i| = m$: \ grows with $n$"),
                why(r"a network, linearized: \ the fast gradient sign method")]
        step = ladder(self, rows, whys, keep=4, top=2.4, x=-1.6, align_index=1, edge=6.8)
        foot = label(r"each pixel changes by at most $\varepsilon$; \ the score changes by $\varepsilon$ times "
                     r"thousands", font_size=24, color=ADV).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Their argument is about linearity. Take a linear score, w dot x, and change the input by a small "
            "eta. <bookmark mark='a'/> The score changes by w dot eta. <bookmark mark='b'/> If no pixel may change "
            "by more than epsilon, the largest change comes from moving every pixel by epsilon in the direction "
            "of its weight's sign, and it equals epsilon times the sum of the absolute weights. "
            "<bookmark mark='c'/> With n inputs whose weights average m in size, that's epsilon times m times n. "
            "It grows with the number of inputs: a change too small to see in any one pixel adds up, over "
            "thousands of pixels, to a large change in the score. <bookmark mark='d'/> Networks of ReLUs are "
            "built from linear pieces, so do the same with the network's own gradient: move every pixel by "
            "epsilon in the direction that raises the loss. That's the fast gradient sign method, one gradient, "
            "one step."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            step(2, transform=False)
            vo.wait_until("d")
            step(3, transform=False)
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def digit(self):
        a = load("adversarial")
        x, sg = np.asarray(a["digit"]), np.asarray(a["sign"])
        steps = a["digit_steps"]
        imgs = Group()
        for s in steps:
            e = float(s["eps"])
            im = img_gray(np.clip(x + e * sg, 0, 1), 1.9, lo=0, hi=1)
            right = int(s["pred"]) == int(a["digit_label"])
            cap = VGroup(MathTex(rf"\varepsilon = {e:g}", font_size=26, color=ADV if e else GREY_A),
                         MathTex(rf"\text{{says }}{s['pred']}\ ({100 * s['p']:.0f}\%)", font_size=26,
                                 color=OK if right else ADV)).arrange(DOWN, buff=0.08)
            cap.next_to(im, DOWN, buff=0.15)
            imgs.add(Group(im, cap))
        imgs.arrange(RIGHT, buff=0.45).move_to([1.4, 0.1, 0])
        sgn = img_heat(sg, 1.9).move_to([-5.2, 0.1, 0])
        sl = label(r"$\mathrm{sign}(\nabla_x J)$", font_size=26, color=ADV).next_to(sgn, DOWN, buff=0.15)
        head = label(r"our LeNet and one test digit", font_size=28).to_edge(UP, buff=0.5)
        tag = note(r"computed").to_corner(DR, buff=0.25)
        flip = next((s for s in steps if int(s["pred"]) != int(a["digit_label"])), None)
        if flip is not None:
            v = (f"At epsilon {flip['eps']:g}, it says {flip['pred']}, with {pct(flip['p'], 0)} percent "
                 "confidence.")
        else:
            v = "Even at the largest epsilon here it still says 7, though less sure."
        with self.voiceover(
            "Try it on our LeNet, which reads ninety-nine digits in a hundred correctly. <bookmark mark='a'/> "
            "This is the sign of the loss's gradient for one test digit: which way each pixel should move to make "
            f"the network more wrong. <bookmark mark='b'/> Add it, scaled by epsilon. At zero, the network says "
            f"{steps[0]['pred']}, {pct(steps[0]['p'], 0)} percent sure. <bookmark mark='c'/> " + v + " To a "
            "person it is still plainly a seven, in a little fog."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(sgn), FadeIn(sl))
            vo.wait_until("b")
            self.play(FadeIn(imgs[0]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.1) for i in imgs[1:]], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        a = load("adversarial")
        eps = np.asarray(a["eps"])
        F = a["fgsm"]
        ax = axes([0, eps[-1]], [0, 1.0], x_length=6.4, y_length=3.8, xlabel=r"$\varepsilon$ (pixels are $0$ to $1$)",
                  ylabel=r"test error under attack", xticks=[0, 0.1, 0.2, 0.3], yticks=[0, 0.5, 1.0],
                  yfmt=lambda v: f"{int(100 * v)}\\%", center=[-2.4, -0.3, 0])
        A = ax.ax
        lin = curve(A, eps, F["linear"], GREY_B, 3.5)
        mlp = seed_band(A, eps, F["mlp"], MLPC)
        cnn = seed_band(A, eps, F["lenet"], CNN)
        pg = curve(A, eps, np.asarray(a["pgd"]["lenet"])[0], ADV, 3.5)
        pgd_d = DashedVMobject(pg, num_dashes=30)
        leg = legend([(GREY_B, r"linear softmax"), (MLPC, r"MLP"), (CNN, r"LeNet"),
                      (ADV, r"LeNet, \ $20$ gradient steps (PGD)")], font_size=22).to_corner(UR, buff=0.4)
        T = a["transfer"]
        e_t = a["transfer_eps"]
        tr = VGroup(label(rf"made on the MLP, \ shown to LeNet \ ($\varepsilon = {e_t:g}$):", font_size=22,
                          color=GREY_A),
                    MathTex(rf"{100 * T['mlp_to_lenet']:.0f}\%\ \text{{wrong}}", font_size=30, color=MLPC),
                    label(r"made on one LeNet, \ shown to another:", font_size=22, color=GREY_A),
                    MathTex(rf"{100 * T['lenet_to_lenet']:.0f}\%\ \text{{wrong}}", font_size=30, color=CNN))
        tr.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(leg, DOWN, buff=0.5).align_to(leg, LEFT)
        keep_in_frame(tr)
        tag = note(r"computed: \ the $10{,}000$ test digits; \ MLP and LeNet: three seeds, \ min--max").to_corner(
            DR, buff=0.2)
        i2, i25 = list(eps).index(0.2), list(eps).index(0.25)
        e_lin, e_cnn = F["linear"][i25], float(np.mean(np.asarray(F["lenet"])[:, i25]))
        e_pgd = float(np.asarray(a["pgd"]["lenet"])[0][i2])
        with self.voiceover(
            "Measure it over all ten thousand test digits. <bookmark mark='a'/> At epsilon a quarter, the "
            f"linear model is wrong on {pct(e_lin, 0)} percent of them; Goodfellow's shallow softmax was wrong on "
            f"{FGSM_PAPER['softmax']}. <bookmark mark='b'/> The networks are not much safer: LeNet, wrong on "
            f"{pct(e_cnn, 0)} percent. <bookmark mark='c'/> And one gradient step is a weak attack. Take twenty "
            f"small steps instead, each projected back into the epsilon box, and at epsilon 0.2 LeNet is wrong on "
            f"{pct(e_pgd, 0)} percent. <bookmark mark='d'/> The attacks transfer: changes made against the "
            f"fully connected network fool LeNet {pct(T['mlp_to_lenet'], 0)} percent of the time, and changes made "
            f"against one LeNet fool another trained from a different start {pct(T['lenet_to_lenet'], 0)} percent "
            "of the time. Different networks learn similar linear directions."
        ) as vo:
            self.play(Create(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lin), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(FadeIn(mlp), FadeIn(cnn), FadeIn(leg[1]), FadeIn(leg[2]))
            vo.wait_until("c")
            self.play(Create(pgd_d), FadeIn(leg[3]))
            vo.wait_until("d")
            self.play(FadeIn(tr, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def straight(self):
        a = load("adversarial")
        es = np.asarray(a["line_eps"])
        L = np.asarray(a["line_logits"])
        lo, hi = float(L.min()), float(L.max())
        ax = axes([es[0], es[-1]], [lo, hi], x_length=6.6, y_length=4.0,
                  xlabel=r"$\varepsilon$ along $\mathrm{sign}(\nabla_x J)$", ylabel=r"the ten scores (logits)",
                  xticks=[-0.5, 0, 0.5], center=[-1.8, -0.3, 0])
        A = ax.ax
        y0 = int(a["digit_label"])
        cols = [CNN if k == y0 else GREY_B for k in range(10)]
        curves_ = VGroup(*[curve(A, es, L[:, k], cols[k], 4 if k == y0 else 2) for k in range(10)])
        win = np.argmax(L, 1)
        other = int(np.bincount(win[es > 0.2], minlength=10).argmax()) if (es > 0.2).any() else y0
        curves_[other].set_color(ADV).set_stroke(width=4)
        z = Line(A.c2p(0, lo), A.c2p(0, hi), color=GREY_D, stroke_width=1.5)
        leg = legend([(CNN, rf"the score for {y0}"), (ADV, rf"the score for {other}"),
                      (GREY_B, r"the other eight")], font_size=22).to_corner(UR, buff=0.4)
        n1 = label(r"Goodfellow et al.'s figure 4, \ redone on our LeNet", font_size=20, color=GREY_B)
        n1.next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        a_ = load("adversarial")
        gap, l1, need = a_["linear_gap_median"], a_["linear_l1_median"], a_["linear_need_median"]
        lin = VGroup(label(r"the linear model, \ median over test digits:", font_size=22, color=GREY_A),
                     MathTex(rf"\text{{margin}} \approx {gap:.1f},\quad \|\Delta w\|_1 \approx {l1:.0f}", font_size=28,
                             color=KERNEL),
                     MathTex(rf"\varepsilon_{{\text{{needed}}}} \approx {gap:.1f} / {l1:.0f} \approx {need:.3f}",
                             font_size=28, color=ADV)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        lin.next_to(n1, DOWN, buff=0.5).align_to(n1, LEFT)
        keep_in_frame(lin)
        tag = note(r"computed").to_corner(DR, buff=0.25)
        with self.voiceover(
            "Is the network really that linear? Walk from the digit along the attack direction, and backwards, "
            "and plot all ten of its scores. <bookmark mark='a'/> They are nearly straight lines. The score for "
            f"the right answer falls, the score for {other} rises, and where they cross, the answer changes. "
            "<bookmark mark='b'/> For the linear model we can do the arithmetic exactly. The typical gap between "
            f"the right score and the runner-up is {gap:.1f}; the sum of the absolute differences of their weights "
            f"is about {l1:.0f}; so an epsilon of about {need:.3f} closes the gap, a change of a few percent of "
            "one grey level per pixel, times seven hundred and eighty-four pixels."
        ) as vo:
            self.play(Create(ax), Create(z), FadeIn(tag))
            self.play(LaggedStart(*[Create(c) for c in curves_], lag_ratio=0.05), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(leg), FadeIn(n1))
            vo.wait_until("b")
            self.play(FadeIn(lin, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def photos(self):
        a = load("adversarial")
        names = classes()
        X, XA, E = np.asarray(a["cifar_ex_img"]), np.asarray(a["cifar_ex_adv"]), a["cifar_ex"]
        rows = Group()
        for i in range(min(3, len(E))):
            o = img_rgb(X[i], 1.5)
            d = (XA[i].astype(float) - X[i].astype(float))
            diff = img_heat(d.mean(-1), 1.5)
            ad = img_rgb(XA[i], 1.5)
            co = data_text(f"{names[E[i]['label']]} {100 * E[i]['p']:.0f}%", font_size=18, color=OK)
            ca = data_text(f"{names[E[i]['pred']]} {100 * E[i]['p_adv']:.0f}%", font_size=18, color=ADV)
            r = Group(Group(o, co), MathTex("+", font_size=36), diff, MathTex("=", font_size=36), Group(ad, ca))
            co.next_to(o, DOWN, buff=0.08)
            ca.next_to(ad, DOWN, buff=0.08)
            r.arrange(RIGHT, buff=0.25)
            rows.add(r)
        rows.arrange(DOWN, buff=0.25).move_to([-2.6, -0.3, 0])
        if rows.height > 6.0:
            rows.height = 6.0
        hl = label(r"the change, magnified: \ at most $2$ grey levels of $255$ per pixel", font_size=20,
                   color=ADV).next_to(rows, UP, buff=0.12)
        ce = np.asarray(a["cifar_eps"])
        ax = axes([0, ce[-1]], [0, 1.0], x_length=3.6, y_length=2.8, xlabel=r"$\varepsilon$, \ in $1/255$",
                  ylabel=r"error", xticks=[0, 2, 4, 8], yticks=[0, 0.5, 1.0], yfmt=lambda v: f"{int(100 * v)}\\%",
                  center=[4.6, -0.6, 0])
        A = ax.ax
        cf = curve(A, ce, a["cifar_fgsm"], CNN, 3.5)
        cp = curve(A, ce, a["cifar_pgd"], ADV, 3.5)
        leg = legend([(CNN, r"one step"), (ADV, r"$20$ steps")], font_size=20).next_to(ax, UP, buff=0.15)
        tag = note(r"computed: \ our CIFAR network, \ $2{,}000$ test photographs").to_corner(DR, buff=0.2)
        i2 = list(ce).index(2.0)
        with self.voiceover(
            "On photographs it is worse, because a photograph has more numbers: thirty-two by thirty-two pixels, "
            "three colours each. <bookmark mark='a'/> Our CIFAR network, attacked with twenty small steps, "
            "changing no pixel by more than two grey levels out of 255: <bookmark mark='b'/> the originals, the "
            "change magnified many times, and the result, which looks identical, and which the network calls "
            f"something else. <bookmark mark='c'/> At two grey levels it's wrong on {pct(a['cifar_pgd'][i2], 0)} "
            f"percent of the test photographs, against {pct(a['cifar_pgd'][0], 0)} percent with no attack at all."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(hl), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(Create(ax), Create(cf), Create(cp), FadeIn(leg))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def defence(self):
        t = load("advtrain")
        a = load("adversarial")
        runs = [t["runs"][str(s)] for s in (0, 1, 2)]
        cv = [np.asarray(r["curve"]) for r in runs]
        xs = cv[0][:, 0]
        ax = axes([0, xs[-1]], [0, 1.0], x_length=5.8, y_length=3.6, xlabel=r"training steps",
                  ylabel=r"test error", xticks=[0, int(xs[-1])], yticks=[0, 0.5, 1.0],
                  yfmt=lambda v: f"{int(100 * v)}\\%", center=[-3.0, -0.4, 0])
        A = ax.ax
        clean = seed_band(A, xs, [c[:, 1] for c in cv], CNN)
        adv = seed_band(A, xs, [c[:, 2] for c in cv], ADV)
        leg = legend([(CNN, r"clean digits"), (ADV, rf"attacked, \ $\varepsilon = {t['eps']:g}$, one step")],
                     font_size=22).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        eg = list(t["eps_grid"])
        i = eg.index(t["eps"])
        std_f = float(np.mean(np.asarray(a["fgsm"]["lenet"])[:, i]))
        std_p = float(np.asarray(a["pgd"]["lenet"])[0][i])
        adv_f = float(np.mean([r["fgsm"][i] for r in runs]))
        adv_p = float(np.mean([r["pgd"][i] for r in runs]))
        adv_c = float(np.mean([r["clean"] for r in runs]))
        std_c = float(np.mean(np.asarray(a["fgsm"]["lenet"])[:, 0]))
        tab = VGroup(
            VGroup(VectorizedPoint(), label(r"one step", font_size=22, color=GREY_A),
                   label(r"$20$ steps", font_size=22, color=GREY_A), label(r"clean", font_size=22, color=GREY_A)),
            VGroup(label(r"ordinary LeNet", font_size=22, color=GREY_B), MathTex(rf"{100 * std_f:.0f}\%", font_size=28),
                   MathTex(rf"{100 * std_p:.0f}\%", font_size=28), MathTex(rf"{100 * std_c:.1f}\%", font_size=28)),
            VGroup(label(r"trained on attacks", font_size=22, color=CNN),
                   MathTex(rf"{100 * adv_f:.0f}\%", font_size=28, color=CNN),
                   MathTex(rf"{100 * adv_p:.0f}\%", font_size=28, color=CNN),
                   MathTex(rf"{100 * adv_c:.1f}\%", font_size=28, color=CNN)),
        )
        colx = [0.7, 3.9, 5.1, 6.3]
        for ri, r in enumerate(tab):
            y = 0.9 - 0.65 * ri
            r[0].move_to([colx[0] + r[0].width / 2, y, 0])
            for j in (1, 2, 3):
                r[j].move_to([colx[j], y, 0])
        keep_in_frame(tab)
        tl = label(rf"test error at $\varepsilon = {t['eps']:g}$", font_size=22, color=GREY_A).next_to(tab, UP,
                                                                                                    buff=0.25)
        fr = label(r"since: \ certified defences, \ physical attacks (stickers on stop signs), \ and the same "
                   r"search against language models (Part 31)", font_size=20, color=GREY_B).to_edge(DOWN, buff=0.3)
        if fr.width > 13:
            fr.width = 13
        cite_ = cite(r"Goodfellow et al.\ (2014); \ Madry et al.\ (2017); \ Wong, Rice \& Kolter (2020)", corner=UR)
        tag = note(r"computed: \ three seeds").to_corner(DR, buff=0.2)
        holds = adv_p < std_p - 0.2
        verdict = (f"Against twenty steps it holds up too: {pct(adv_p, 0)} percent wrong, against "
                   f"{pct(std_p, 0)} for the ordinary network." if holds else
                   f"But against twenty steps it gives way: {pct(adv_p, 0)} percent wrong. It learned to resist "
                   "the one-step attack it trained on, not attacks in general.")
        with self.voiceover(
            "The defence Goodfellow proposed is to train on the attacks: at every step, make adversarial versions "
            "of the batch and teach the network the right answer for them too. <bookmark mark='a'/> We trained "
            "three LeNets that way, half clean digits and half attacked. The attacked error, red, falls along "
            f"with the clean one. <bookmark mark='b'/> At epsilon {t['eps']:g}, one-step attacks now fool it "
            f"{pct(adv_f, 0)} percent of the time instead of {pct(std_f, 0)}. " + verdict + " "
            f"<bookmark mark='c'/> The clean error rises a little, to {pct(adv_c, 2)} percent: robustness costs "
            "accuracy. Aleksander Madry's group made the stronger version standard in 2017, training against many "
            "steps. <bookmark mark='d'/> The problem is still open. Printed stickers can fool a stop-sign "
            "detector, and the same gradient search, run over words, finds suffixes that make language models "
            "ignore their training, which is Part 31's story."
        ) as vo:
            self.play(Create(ax), FadeIn(leg), FadeIn(cite_), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(clean), FadeIn(adv), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(tl), FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("d")
            self.play(FadeIn(fr))
        self.wait(0.3)
        self.clear_scene()


_ = (MLPC, HIST)
