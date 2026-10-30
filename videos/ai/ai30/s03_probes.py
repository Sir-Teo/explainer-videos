from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai30.common import CAUSE, CTRL, MONO, PART, PROBE, load, show_tok, spread_bar

MLPC = C.MLP


class Probes(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.layers()
        self.control()
        self.amnesic()

    def card(self):
        card = chapter_card(2, r"What does it know?", r"Can a classifier read a property off the vectors?", part=PART)
        with self.voiceover("Chapter two. What does it know?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def idea(self):
        p = load("probes")
        toks = [str(t) for t in p["example_tokens"]][:26]
        lab = np.asarray(p["example_labels"])[:26]
        boxes = VGroup()
        for t, y in zip(toks, lab):
            tx = data_text(show_tok(t), font=MONO, font_size=20, color=WHITE)
            r = RoundedRectangle(width=tx.width + 0.16, height=0.5, corner_radius=0.06, stroke_width=1.2,
                                 stroke_color=PROBE if y else GREY_D, fill_color=PROBE, fill_opacity=0.25 if y else 0)
            boxes.add(VGroup(r, tx.move_to(r)))
        boxes.arrange(RIGHT, buff=0.06)
        lines = VGroup()
        row = VGroup()
        for b in boxes:
            row.add(b)
            if row.width > 12.4:
                row.remove(b)
                lines.add(row)
                row = VGroup(b)
        lines.add(row)
        for r_ in lines:
            r_.arrange(RIGHT, buff=0.06)
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(UP, buff=1.0)
        cap = label(r"lit: \ inside a quotation, \ once this token is read \ (the novels model's tokens)", font_size=22,
                    color=PROBE).next_to(lines, DOWN, buff=0.25)
        dc = definition_card(r"probe", r"a small classifier trained to read a property off one layer's vectors: \ "
                             r"linear, $\;p = \sigma(w \cdot h_\ell + b)$, \ or a small MLP. \ High accuracy means the "
                             r"property is \textit{decodable} there.", color=PROBE, width=7.4).to_corner(DL, buff=0.35)
        hc = history_card(2016, r"G.~Alain \& Y.~Bengio", r"linear classifier probes on every layer", width=4.6,
                          color=PROBE, font_size=20).to_corner(DR, buff=0.35)
        with self.voiceover(
            "Saliency asks where the model looked. A probe asks what it knows. <bookmark mark='a'/> Take a property "
            "of the text, say, whether the reader is inside a quotation at this token: the novels model, Part "
            "18's six-layer transformer, must track it to know when a closing quote is coming. "
            "<bookmark mark='b'/> A probe is a small classifier, trained to read that property off one layer's "
            "vectors. If a linear probe succeeds, the information is sitting there along a direction. "
            "<bookmark mark='c'/> Guillaume Alain and Yoshua Bengio put linear probes on every layer of a network in "
            "2016, and probing became the first workhorse of interpretability."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.03), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(cap))
            vo.wait_until("b")
            self.play(FadeIn(dc, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(hc, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def axes(self):
        p = load("probes")
        L = int(p["layers"])
        lo = 0.5
        g = axes([-0.3, L - 0.7], [lo, 1.0], x_length=6.8, y_length=4.2, xlabel=r"layer of the novels model \ "
                 r"($0$: the token embedding)", ylabel=r"accuracy on held-out text", xticks=list(range(L)),
                 yticks=[0.5, 0.75, 1.0], center=[-2.4, -0.35, 0])
        return g, L

    def layers(self):
        p = load("probes")
        g, L = self.axes()
        lt = np.asarray(p["lin_task"])
        maj = float(p["majority"])
        mline = DashedLine(g.ax.c2p(-0.3, maj), g.ax.c2p(L - 0.7, maj), color=CTRL, dash_length=0.06)
        ml = label(rf"always guess the commoner label: \ ${100 * maj:.0f}\%$", font_size=18, color=CTRL)
        ml.next_to(g.ax.c2p(L - 0.7, maj), DL, buff=0.1)
        mean = lt.mean(0)
        c = curve(g.ax, range(L), mean, PROBE, 4)
        sp = VGroup(*[spread_bar(g.ax, l_, lt[:, l_], PROBE) for l_ in range(L)])
        best = int(np.argmax(mean))
        tag = note(rf"computed: \ ${int(p['n_train']):,}$ tokens to train, \ ${int(p['n_test']):,}$ held out; \ "
                   rf"${len(p['seeds'])}$ seeds, \ min to max".replace(",", "{,}")).to_corner(DR, buff=0.25)
        res = label(rf"linear probe: \ ${100 * mean[0]:.0f}\%$ at the embedding, \\ ${100 * mean[best]:.0f}\%$ at layer "
                    rf"${best}$", font_size=24, color=PROBE).move_to([4.6, 1.6, 0])
        with self.voiceover(
            "We trained a linear probe on each layer of the novels model, with three seeds. "
            f"<bookmark mark='a'/> Guessing the commoner label scores {100 * maj:.0f} percent. "
            f"<bookmark mark='b'/> At the token embedding, before any attention, the probe reaches "
            f"{100 * mean[0]:.0f} percent: a token alone says little about where it sits. "
            f"<bookmark mark='c'/> After a few blocks it reaches {100 * mean[best]:.0f} percent, at layer {best}: "
            "attention has carried the quotation marks forward, and the state is written along a direction."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(mline), FadeIn(ml))
            vo.wait_until("b")
            self.play(FadeIn(sp[0]))
            vo.wait_until("c")
            self.play(Create(c), LaggedStart(*[FadeIn(s_) for s_ in sp[1:]], lag_ratio=0.2), run_time=2.0)
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def control(self):
        p = load("probes")
        g, L = self.axes()
        lt, lc, mt, mc = (np.asarray(p[k]).mean(0) for k in ("lin_task", "lin_ctrl", "mlp_task", "mlp_ctrl"))
        cl = curve(g.ax, range(L), lt, PROBE, 4)
        cc = DashedVMobject(curve(g.ax, range(L), lc, PROBE, 3), num_dashes=40)
        ml = curve(g.ax, range(L), mt, MLPC, 4)
        mcc = DashedVMobject(curve(g.ax, range(L), mc, MLPC, 3), num_dashes=40)
        lg = legend([(PROBE, r"linear probe, \ the task"), (MLPC, r"MLP probe, \ the task")], font_size=18)
        lg2 = label(r"dashed: \ the control task", font_size=18, color=GREY_A)
        keys = VGroup(lg, lg2).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR, buff=0.35)
        hc = history_card(2019, r"J.~Hewitt \& P.~Liang", r"control tasks: \ give every token type a random label; "
                          r"a probe that learns those has learned the task itself", width=5.2, color=CTRL, font_size=19)
        hc.next_to(keys, DOWN, buff=0.3).align_to(keys, RIGHT)
        best = int(p["best"])
        sel_l, sel_m = lt - lc, mt - mc
        f = cmath(r"\text{selectivity} = \text{task} - \text{control}", font_size=28).next_to(hc, DOWN, buff=0.3)
        f.align_to(hc, LEFT)
        sl = label(rf"at layer ${best}$: \ linear ${100 * sel_l[best]:+.0f}$, \ MLP ${100 * sel_m[best]:+.0f}$ points",
                   font_size=22, color=GREY_A).next_to(f, DOWN, buff=0.15).align_to(f, LEFT)
        more = mt[best] > lt[best]
        less_sel = sel_m[best] < sel_l[best]
        verdict = (f"The MLP probe scores higher on the task, {100 * mt[best]:.0f} percent against "
                   f"{100 * lt[best]:.0f}, " if more else
                   f"The MLP probe scores {100 * mt[best]:.0f} percent on the task, against the linear probe's "
                   f"{100 * lt[best]:.0f}, ")
        verdict2 = (f"but it also learns the nonsense better: at layer {best} its selectivity is "
                    f"{100 * sel_m[best]:.0f} points, the linear probe's {100 * sel_l[best]:.0f}. A more powerful probe "
                    "tells you more about the probe." if less_sel else
                    f"and here its selectivity holds up too, {100 * sel_m[best]:.0f} points against "
                    f"{100 * sel_l[best]:.0f}.")
        with self.voiceover(
            "But who did the work, the model or the probe? <bookmark mark='a'/> John Hewitt and Percy Liang's "
            "control task asks it directly. Give every token type a random label, at the same rate; there is no "
            "such property in the text, so a probe that scores well has simply memorized which tokens carry which "
            "label. <bookmark mark='b'/> On the embedding the control is easy: each token is its own vector. "
            f"Our linear probe gets {100 * lc[0]:.0f} percent of the nonsense right there, against {100 * lt[0]:.0f} on "
            "the real task. <bookmark mark='p'/> Pause and predict: a more powerful probe, a small MLP, can fit more. "
            f"Will it be more selective, or less? <bookmark mark='c'/> {verdict}<bookmark mark='c2'/>{verdict2} <bookmark mark='d'/> Selectivity, the task minus the control, is what "
            "a probe result should be reported with."
        ) as vo:
            self.play(FadeIn(g), Create(cl), FadeIn(lg[0]))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(Create(cc), FadeIn(lg2), run_time=1.5)
            vo.wait_until("p")
            pz = pause_card(r"An MLP probe can fit more. \ More selective, \ or less?", width=5.2,
                            font_size=22).move_to(hc)
            self.play(FadeOut(hc), FadeIn(pz))
            vo.wait_until("c")
            self.play(FadeOut(pz), FadeIn(hc))
            self.play(Create(ml), FadeIn(lg[1]), run_time=1.2)
            self.play(Create(mcc), run_time=1.2)
            vo.wait_until("d")
            self.play(Write(f), FadeIn(sl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def amnesic(self):
        p = load("probes")
        a = p["amnesic"]
        best = int(p["best"])
        b0, bp = float(a["base_closing"]), float(a["probe_closing"])
        br = np.asarray(a["rand_closing"], float)
        vals = [b0, float(br.mean()), bp]
        names = [r"as it is", rf"$10$ random directions \\ removed (mean)", r"the probe's direction \\ removed"]
        cols = [GREY_B, CTRL, CAUSE]
        top = max(vals) * 1.15
        g = axes([0, 3], [0, top], x_length=6.4, y_length=3.8, ylabel=r"bits to predict a closing quotation mark",
                 yticks=ticks_(top), center=[-2.6, -0.4, 0])
        bars_ = VGroup()
        for i, (v, n, c_) in enumerate(zip(vals, names, cols)):
            r = Rectangle(width=1.0, height=max(v / top * 3.8, 0.01), stroke_width=0, fill_color=c_, fill_opacity=0.9)
            r.move_to(g.ax.c2p(i + 0.5, 0), aligned_edge=DOWN)
            t = MathTex(f"{v:.2f}", font_size=26, color=c_).next_to(r, UP, buff=0.22 if i == 1 else 0.08)
            nl = label(n, font_size=18, color=c_).next_to(g.ax.c2p(i + 0.5, 0), DOWN, buff=0.15)
            bars_.add(VGroup(r, t, nl))
        if len(br) > 1:
            lo_, hi_ = br.min(), br.max()
            bars_[1].add(Line(g.ax.c2p(1.5, lo_), g.ax.c2p(1.5, hi_), color=WHITE, stroke_width=2))
        hc = history_card(2021, r"Y.~Elazar, S.~Ravfogel, A.~Jacovi \& Y.~Goldberg", r"amnesic probing: \ remove what the "
                          r"probe reads, \ and see whether the model notices", width=5.6, color=CAUSE, font_size=19)
        hc.to_corner(UR, buff=0.35)
        uses = (bp - b0) > 3 * max(float(br.mean()) - b0, 0.02)
        proj = cmath(r"h \;\to\; h - (h\cdot\hat w)\,\hat w", font_size=34).next_to(hc, DOWN, buff=0.45)
        pl = label(r"$\hat w$: \ the probe's unit direction, \ at layer " + f"${best}$", font_size=18,
                   color=GREY_A).next_to(proj, DOWN, buff=0.12)
        msg = label((r"the model uses this direction" if uses else r"decodable, \ but barely used"), font_size=26,
                    color=CAUSE).next_to(pl, DOWN, buff=0.45)
        verdict = ("The model was using that direction to know a quote was open. " if uses else
                   "The model hardly cared: the information was there, but the computation ran elsewhere, or along "
                   "other directions too. ")
        with self.voiceover(
            "There is a second trap. A probe shows that information can be read; not that the model reads it. "
            "<bookmark mark='a'/> Yanai Elazar and colleagues' answer: remove what the probe reads, and see whether "
            f"the model notices. We take the linear probe's direction at layer {best}, project it out of every "
            "vector, and run the rest of the model. <bookmark mark='b'/> On the tokens that close a quotation, "
            f"predicting them costs {b0:.2f} bits as the model is. <bookmark mark='c'/> Removing ten random "
            f"directions instead costs {br.mean():.2f}. <bookmark mark='d'/> Removing the probe's direction costs "
            f"{bp:.2f}. {verdict}Reading out is correlation; changing the model and watching is causation, the subject of chapter four."
        ) as vo:
            self.play(FadeIn(g), FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(proj), FadeIn(pl))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars_[0][0], DOWN), FadeIn(bars_[0][1:]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars_[1][0], DOWN), FadeIn(bars_[1][1:]))
            vo.wait_until("d")
            self.play(GrowFromEdge(bars_[2][0], DOWN), FadeIn(bars_[2][1:]))
            self.play(FadeIn(msg))
        self.wait(0.3)
        self.clear_scene()


def ticks_(top):
    from videos.ai.ai30.common import ticks

    return ticks(0, top, 3)
