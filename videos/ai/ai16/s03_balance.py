from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai16.common import EXPERT_COLORS, MODES, ROUTER, load, load_image


class Balance(VoiceoverScene):
    def construct(self):
        self.card()
        self.collapse()
        self.fixes()
        self.replay()

    def card(self):
        card = chapter_card(2, r"Keeping every expert busy", r"What stops the router from playing favourites?", part=16)
        with self.voiceover("Chapter two. Keeping every expert busy."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def panel(self, m, mode, title, color, center):
        L = np.asarray(m[f"load_{mode}"])
        E = L.shape[1]
        img = load_image(L, 4.0, 2.0).move_to(center)
        frame = SurroundingRectangle(img, buff=0, color=GREY_D, stroke_width=1.5)
        t = label(title, font_size=26, color=color).next_to(img, UP, buff=0.15)
        el = label(rf"${E}$ experts", font_size=18, color=GREY_B).rotate(PI / 2).next_to(img, LEFT, buff=0.1)
        tl = label(r"training $\to$", font_size=18, color=GREY_B).next_to(img, DOWN, buff=0.08)
        imb = float(m["imbalance"][mode])
        bits = float(m[f"bits_{mode}"])
        st = label(rf"busiest: \ ${imb:.1f}\times$ a fair share; \ ${bits:.3f}$ bits", font_size=20, color=GREY_A)
        st.next_to(tl, DOWN, buff=0.1)
        return Group(img, frame, t, el, tl, st)

    # ------------------------------------------------------------------
    def collapse(self):
        m = load("moe")
        E, k = int(m["E"]), int(m["k"])
        p = self.panel(m, "none", r"no balancing", MODES[0][2], [-3.3, 0.2, 0])
        imb = float(m["imbalance"]["none"])
        collapsed = imb > 1.8
        expl = label(r"bright: \ an expert getting more \\ than its fair share of characters", font_size=24, color=GREY_A)
        expl.move_to([3.4, 1.0, 0])
        why = label(r"a favoured expert trains more, \\ gets better, \ is favoured more", font_size=26, color=C.SURPRISE)
        why.next_to(expl, DOWN, buff=0.5)
        head = label(rf"our model: \ a character model whose hidden layer is ${E}$ experts, \ ${k}$ per character", font_size=26)
        head.to_edge(UP, buff=0.35)
        with self.voiceover(
            f"We built one: Part twelve's character model, with its hidden layer split into {E} experts and {k} used "
            "for each character. Train it, and watch how the characters are shared out. "
            + (f"<bookmark mark='a'/> Left alone, the router plays favourites: the busiest expert ends up with "
               f"{imb:.1f} times its fair share, while others starve. "
               if collapsed else
               f"<bookmark mark='a'/> In our small model, the router stays fairly even on its own, the busiest expert at "
               f"{imb:.1f} times a fair share; in big models it often doesn't. ")
            + "<bookmark mark='b'/> It's a rich-get-richer loop: a favoured expert gets more practice, gets better, and "
            "gets chosen even more. Starved experts are wasted parameters."
        ) as vo:
            self.play(FadeIn(head))
            # training, replayed: the picture fills in from the left, a column every 50 steps, as a counter runs
            img, frame, t_, el_, tl_, st_ = p
            n_cols = len(np.asarray(m["load_none"]))
            cover = Rectangle(width=img.width + 0.02, height=img.height + 0.02, stroke_width=0, fill_color="#121722",
                              fill_opacity=1).move_to(img)
            u = ValueTracker(0.0)
            cover.add_updater(lambda c_: c_.stretch_to_fit_width(max((img.width + 0.02) * (1 - u.get_value()), 1e-3))
                              .move_to(img.get_right() + RIGHT * 0.01, aligned_edge=RIGHT))
            cnt = always_redraw(lambda: MathTex(rf"\text{{training step }}{50 * int(round(u.get_value() * n_cols)):,}"
                                                .replace(",", "{,}"), font_size=26, color=C.BITS).next_to(st_, DOWN, buff=0.25))
            self.add(img, cover, frame)
            self.play(FadeIn(t_), FadeIn(el_), FadeIn(tl_), Create(frame), FadeIn(expl))
            self.add(cnt)
            self.play(u.animate.set_value(1.0), run_time=3.5, rate_func=linear)
            vo.wait_until("a")
            cover.clear_updaters()
            cnt.clear_updaters()
            self.remove(cover)
            self.play(FadeIn(st_))
            vo.wait_until("b")
            self.play(FadeIn(why))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fixes(self):
        m = load("moe")
        E = int(m["E"])
        pa = self.panel(m, "aux", r"auxiliary loss", MODES[1][2], [-3.3, 0.6, 0])
        pb = self.panel(m, "bias", r"loss-free bias", MODES[2][2], [3.3, 0.6, 0])
        colors = {r"f_i": C.BITS, r"P_i": ROUTER}
        f1 = cmath(r"\mathcal{L}_{\mathrm{aux}}", "=", r"\alpha\,E\sum_i", r"f_i", r"\,", r"P_i", colors=colors, font_size=32)
        f1.next_to(pa, DOWN, buff=0.3)
        f1l = label(r"$f_i$: \ share of characters sent to $i$; \ $P_i$: \ its mean router probability", font_size=18,
                    color=GREY_A).next_to(f1, DOWN, buff=0.1)
        f2 = cmath(r"b_i \;\leftarrow\; b_i + \gamma\,\mathrm{sign}\big(\tfrac{1}{E} -", r"f_i", r"\big)", colors=colors,
                   font_size=32).next_to(pb, DOWN, buff=0.3)
        f2l = label(r"a bias, used only to choose: \ busy experts get pushed down", font_size=18, color=GREY_A).next_to(f2, DOWN, buff=0.1)
        c1 = cite(r"W.~Fedus, B.~Zoph \& N.~Shazeer, \textit{Switch Transformers} (2021); \ L.~Wang et al.\ (2024), DeepSeek-V3",
                  corner=DR)
        bn, ba, bb = (float(m[f"bits_{k_}"]) for k_ in ("none", "aux", "bias"))
        ia, ib = float(m["imbalance"]["aux"]), float(m["imbalance"]["bias"])
        even = ("Both spread the work evenly here. " if ia < 1.5 else
                f"At the strength Google's Switch Transformer used in 2021, the penalty only partly evens it out: its busiest expert still gets {ia:.1f} times a "
                f"fair share, while the bias holds every expert within {ib:.1f}. ")
        with self.voiceover(
            "Two fixes. <bookmark mark='a'/> The classic one adds a penalty to the loss: the share of characters each "
            "expert gets, times its average router probability, summed. It's smallest when every expert gets an equal "
            "share. But it's a second goal competing with the first. <bookmark mark='b'/> DeepSeek-V3's fix adds no "
            "loss at all. Each expert gets a bias, used only for choosing, never for mixing: after every step, busy "
            "experts' biases go down a notch and idle experts' go up. <bookmark mark='c'/> " + even
            + f"Held-out bits: {bn:.3f} unbalanced, {ba:.3f} with the penalty, {bb:.3f} with the bias."
        ) as vo:
            self.play(FadeIn(c1))
            vo.wait_until("a")
            self.play(FadeIn(pa), Write(f1), FadeIn(f1l))
            vo.wait_until("b")
            self.play(FadeIn(pb), Write(f2), FadeIn(f2l))
            vo.wait_until("c")
            self.play(Indicate(pa[-1]), Indicate(pb[-1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        m = load("moe")
        E = int(m["E"])
        loads = {k: np.asarray(m[f"load_{k}"]) for k, _, _ in MODES}
        n = len(loads["none"])
        frames = np.unique(np.linspace(0, n - 1, 24).round().astype(int))
        top = max(float(v.max()) for v in loads.values())
        sets = []
        for i, (k, title, col) in enumerate(MODES):
            b = LiveBars(loads[k][0], max_value=top, height=2.6, bar_width=0.32, gap=0.08, colors=EXPERT_COLORS[:E])
            b.place(base_y=-1.6, x=-4.4 + 4.4 * i)
            fair = DashedLine([-4.4 + 4.4 * i - 1.75, -1.6 + 2.6 / E / top, 0], [-4.4 + 4.4 * i + 1.75, -1.6 + 2.6 / E / top, 0],
                              color=GREY_B, stroke_width=1.5)
            t = label(title, font_size=26, color=col).move_to([-4.4 + 4.4 * i, 1.6, 0])
            sets.append((b, fair, t))
        clock = VGroup(label(r"training step", font_size=26, color=GREY_A), Integer(50, font_size=30, color=C.BITS))
        clock.arrange(RIGHT, buff=0.2).to_edge(UP, buff=0.4)
        fl = label(r"dashed: \ a fair share, \ $1/8$ of the characters", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is all of training, replayed: each bar is one expert's share of the characters, under each of the "
            "three rules. <bookmark mark='a'/> "
            + ("Watch the left: shares drift apart as some experts win. " if float(m["imbalance"]["none"]) > 1.8 else
               "On the left, the shares wander further from fair than in the other two. ")
            + ("In the middle and on the right, they're pulled back towards a fair share again and again."
               if float(m["imbalance"]["aux"]) < 1.5 else
               "In the middle, the penalty pulls them only part of the way back; on the right, the bias keeps "
               "every expert close to its fair share.")
        ) as vo:
            self.play(FadeIn(clock), FadeIn(fl), *[FadeIn(VGroup(b, fr, t)) for b, fr, t in sets])
            vo.wait_until("a")
            for f_ in frames[1:]:
                self.play(*[a for k_, (b, _, _) in zip(MODES, sets) for a in b.to(loads[k_[0]][f_])],
                          clock[1].animate.set_value(int((f_ + 1) * 50)), run_time=0.3, rate_func=linear)
        self.wait(0.3)
        for b, _, _ in sets:
            b.freeze()
        self.clear_scene()
