from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai19.common import (ACCEPTC, DRAFTC, EAGLEC, F, PART, TARGETC, hbars, load, node_box)

COLORS = {r"\alpha": ACCEPTC, r"k": GREY_A, r"c": DRAFTC}


def per_depth(acc, k):
    """From the accepted counts of many rounds: the chance the i-th draft is accepted, given the earlier ones were."""
    a = np.asarray(acc)
    out = []
    for i in range(1, k + 1):
        prev = (a >= i - 1).sum()
        out.append(float((a >= i).sum() / prev) if prev else 0.0)
    return out


class Drafters(VoiceoverScene):
    def construct(self):
        self.card()
        self.formula()
        self.train()
        self.runs()
        self.clock()

    def card(self):
        card = chapter_card(7, r"Drafters", r"How many tokens does one pass of the big model buy?", part=PART)
        with self.voiceover("Chapter seven. Drafters."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def formula(self):
        rows = [
            cmath(r"\Pr[\text{first } i \text{ drafts accepted}]", r"=", r"\alpha^i", colors=COLORS, font_size=36),
            cmath(r"\mathbb E[\text{tokens per pass}]", r"=", r"\sum_{i=0}^{k} \alpha^i", colors=COLORS, font_size=36),
            cmath(r"\mathbb E[\text{tokens per pass}]", r"=", r"\frac{1 - \alpha^{k+1}}{1 - \alpha}", colors=COLORS,
                  font_size=36),
            cmath(r"\text{speed-up}", r"=", r"\frac{1 - \alpha^{k+1}}{(1 - \alpha)(1 + k\,c)}", colors=COLORS,
                  font_size=36),
        ]
        whys = [why(r"each accepted with chance $\alpha$, \ independently \ (an assumption)"),
                why(r"token $i + 1$ arrives if the first $i$ survive; \ one always does"),
                why(r"a geometric series"),
                why(r"a pass costs $1$, \ a draft step $c$")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.8, buff=0.45, edge=6.8)
        # the picture: k = 4 drafts, the chance of reaching each
        a = 0.7
        sq = VGroup(*[VGroup(Square(0.5, stroke_color=ACCEPTC, stroke_width=2, fill_color=ACCEPTC,
                                    fill_opacity=a ** i * 0.8),
                             MathTex(rf"\alpha^{i}" if i > 1 else (r"\alpha" if i == 1 else "1"), font_size=24))
                      for i in range(5)])
        for b in sq:
            b[1].move_to(b[0])
        sq.arrange(RIGHT, buff=0.12).to_edge(DOWN, buff=0.6)
        sql = label(r"the chance each position is written, \ $k = 4$ \ (the last from the big model itself)",
                    font_size=20, color=GREY_A).next_to(sq, UP, buff=0.2)
        tag = note(r"illustrative: \ $\alpha = 0.7$").next_to(sq, RIGHT, buff=0.4)
        with self.voiceover(
            "How much does it save? Call alpha the chance a drafted token is accepted, and pretend, for now, that "
            "each draft survives independently. <bookmark mark='a'/> Then the first i drafts all survive with "
            "chance alpha to the i. <bookmark mark='b'/> A pass writes token i plus one exactly when the first i "
            "drafts survive, and it always writes one, its own. So the expected tokens per pass is the sum of "
            "alpha to the i, from zero to k. <bookmark mark='c'/> A geometric series: one minus alpha to the k "
            "plus one, over one minus alpha. <bookmark mark='d'/> Drafting isn't free: if a draft step costs c "
            "passes of the big model, divide by one plus k c. Leviathan and colleagues derived exactly this."
        ) as vo:
            step(0)
            self.play(FadeIn(sq), FadeIn(sql), FadeIn(tag))
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def train(self):
        d = load("drafters")
        dr, ea = d["draft"], d["eagle"]
        # the two drafters
        big = node_box(r"the big model: \ $6$ layers", TARGETC, font_size=20, pad=0.25)
        small = node_box(r"a small model: \ $2$ layers, \ width $128$", DRAFTC, font_size=20, pad=0.25)
        head = node_box(r"EAGLE head: \ $1$ block", EAGLEC, font_size=20, pad=0.25)
        big.move_to([-4.6, 2.2, 0])
        small.move_to([-4.6, 0.9, 0])
        head.move_to([-4.6, -0.6, 0])
        feat = Arrow(big.get_bottom() + RIGHT * 1.0, head.get_top() + RIGHT * 1.0, buff=0.08, color=EAGLEC,
                     stroke_width=2.5, max_tip_length_to_length_ratio=0.1)
        fl = label(r"its last hidden state, \\ and the next token", font_size=17, color=EAGLEC).next_to(feat, RIGHT,
                                                                                                    buff=0.1)
        sl = label(rf"${dr['params'] / 1e6:.1f}$M weights, \ ${dr['tokens'] / 1e6:.1f}$M tokens", font_size=17,
                   color=DRAFTC).next_to(small, DOWN, buff=0.08)
        hl = label(rf"${ea['params'] / 1e6:.1f}$M weights, \ reuses the big model's head", font_size=17,
                   color=EAGLEC).next_to(head, DOWN, buff=0.08)
        hc = history_card(2024, r"Yuhui Li et al., \ EAGLE", rf"draft in the big model's features: \ "
                          rf"${F.EAGLE['gain'][0]}$--${F.EAGLE['gain'][1]}\times$ on {F.EAGLE['model']}",
                          width=4.4, font_size=16, color=EAGLEC).move_to([-4.4, -2.6, 0])
        # the replay: acceptance as each drafter trains
        ev_d, ev_e = np.asarray(dr["evals"]), np.asarray(ea["evals"])
        S = max(ev_d[-1, 0], ev_e[-1, 0])
        g = axes([0, S * 1.02], [0, 1.0], x_length=6.2, y_length=3.6, xlabel=r"training step",
                 ylabel=r"acceptance $\alpha$ \ (held-out text, \ sampling)", xticks=[0, int(S // 2), int(S)],
                 yticks=[0, 0.5, 1.0], center=[2.6, 0.3, 0])
        ax = g.ax
        cd = curve(ax, ev_d[:, 0], ev_d[:, 2], DRAFTC, 3)
        ce = curve(ax, ev_e[:, 0], ev_e[:, 2], EAGLEC, 3)
        gd = DashedLine(ax.c2p(ev_d[0, 0], ev_d[0, 3]), ax.c2p(ev_d[-1, 0], ev_d[-1, 3]), color=DRAFTC,
                        dash_length=0.06).set_stroke(opacity=0)
        tr = ValueTracker(0)

        def mover(ev, col):
            def f():
                s_ = tr.get_value() * S
                y = float(np.interp(s_, ev[:, 0], ev[:, 2]))
                x = min(s_, ev[-1, 0])
                return glow_dot(ax.c2p(x, y), color=col, radius=0.07)
            return always_redraw(f)

        md, me = mover(ev_d, DRAFTC), mover(ev_e, EAGLEC)
        rd = label(rf"small model: \ ${ev_d[-1, 2]:.2f}$ \ (greedy ${ev_d[-1, 3]:.2f}$)", font_size=20, color=DRAFTC)
        re = label(rf"EAGLE head: \ ${ev_e[-1, 2]:.2f}$ \ (greedy ${ev_e[-1, 3]:.2f}$)", font_size=20, color=EAGLEC)
        res = VGroup(rd, re).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(g, DOWN, buff=0.35)
        better = "EAGLE head" if ev_e[-1, 2] > ev_d[-1, 2] else "small model"
        why_ = ("reading the big model's own features, the head starts from far more than a small model can learn"
                if better == "EAGLE head" else "the small model, reading the text itself, ends up the better guesser")
        mins_d, mins_e = dr["seconds"] / 60, ea["seconds"] / 60
        with self.voiceover(
            "Where does a draft come from? We trained two for the novels model, on this computer. "
            "<bookmark mark='a'/> The first is simply a small language model: two layers instead of six, trained "
            f"on the same novels for {mins_d:.0f} minutes. <bookmark mark='b'/> The second follows EAGLE, from Yuhui "
            "Li and colleagues in 2024. It doesn't read the text at all. It reads the big model's last hidden "
            "state, with the token just chosen, and predicts the next hidden state, which the big model's own "
            "output layer turns into a token. It is one block, trained for "
            f"{mins_e:.0f} minutes with the big model frozen. <bookmark mark='c'/> As each trains, we measured its "
            "acceptance on held-out text: the chance a drafted token survives the check. "
            f"<bookmark mark='d'/> The small model reaches {ev_d[-1, 2]:.2f}; the EAGLE head {ev_e[-1, 2]:.2f}: "
            + why_ + "."
        ) as vo:
            self.play(FadeIn(big), FadeIn(small), FadeIn(sl))
            vo.wait_until("a")
            self.play(Indicate(small, color=DRAFTC))
            vo.wait_until("b")
            self.play(FadeIn(head), GrowArrow(feat), FadeIn(fl), FadeIn(hl), FadeIn(hc))
            vo.wait_until("c")
            self.play(FadeIn(g))
            self.add(md, me)
            self.play(tr.animate.set_value(1.0), Create(cd), Create(ce), run_time=4.0, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(res))
        md.clear_updaters()
        me.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def runs(self):
        d = load("drafters")
        ks = [int(k) for k in d["k"]]
        R = d["runs"]
        cols = {"draft": DRAFTC, "eagle": EAGLEC}
        meas = {m: [R[f"{m}_{k}_1"]["tokens"] / R[f"{m}_{k}_1"]["rounds"] for k in ks] for m in cols}
        alpha = {m: R[f"{m}_1_1"]["beta"] for m in cols}
        top = max(max(v) for v in meas.values())
        pred = {m: [(1 - alpha[m] ** (k + 1)) / (1 - alpha[m]) for k in ks] for m in cols}
        top = max(top, max(max(v) for v in pred.values()))
        g = axes([0, 7], [0, top * 1.2], x_length=6.2, y_length=4.0, xlabel=r"tokens drafted per pass, \ $k$",
                 ylabel=r"tokens written per pass of the big model", xticks=ks, yticks=[1, 2, 3],
                 center=[-2.6, -0.3, 0])
        ax = g.ax
        one = DashedLine(ax.c2p(0, 1), ax.c2p(7, 1), color=GREY_C, dash_length=0.06)
        dots, lines = VGroup(), VGroup()
        xs = np.linspace(0, 6.5, 60)
        for m, col in cols.items():
            dots.add(VGroup(*[Dot(ax.c2p(k, v), radius=0.08, color=col) for k, v in zip(ks, meas[m])]))
            ln = VMobject(color=col, stroke_width=2).set_points_smoothly(
                [ax.c2p(x, (1 - alpha[m] ** (x + 1)) / (1 - alpha[m])) for x in xs])
            lines.add(ln.set_stroke(opacity=0.6))
        key = VGroup(label(r"dots: \ measured, \ $12$ openings $\times$ $96$ tokens", font_size=19, color=GREY_A),
                     label(rf"lines: \ the formula, \ $\alpha = {alpha['draft']:.2f}$ (small model)", font_size=19,
                           color=DRAFTC),
                     label(rf"\phantom{{lines: }} $\alpha = {alpha['eagle']:.2f}$ (EAGLE head)", font_size=19,
                           color=EAGLEC)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.3, 1.8, 0])
        k4 = ks.index(4)
        dep = {m: per_depth(R[f"{m}_4_1"]["accepted"], 4) for m in cols}
        dl = VGroup(label(r"acceptance of draft $1, 2, 3, 4$ \ ($k = 4$):", font_size=19, color=GREY_A),
                    label(r"small \ " + r",\ ".join(f"${v:.2f}$" for v in dep["draft"]), font_size=19, color=DRAFTC),
                    label(r"EAGLE \ " + r",\ ".join(f"${v:.2f}$" for v in dep["eagle"]), font_size=19, color=EAGLEC))
        dl.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.3, -0.6, 0])
        gr = {m: R[f"{m}_4_0"]["tokens"] / R[f"{m}_4_0"]["rounds"] for m in cols}
        gl = label(rf"greedy, \ $k = 4$: \ ${gr['draft']:.2f}$ \ and \ ${gr['eagle']:.2f}$ tokens per pass",
                   font_size=19, color=GREY_A).next_to(dl, DOWN, buff=0.3).align_to(dl, LEFT)
        best = max(cols, key=lambda m: meas[m][k4])
        diff = {m: meas[m][k4] - pred[m][k4] for m in cols}
        if all(abs(v) < 0.1 * pred[m][k4] for m, v in diff.items()):
            fit = "The formula, with its one number alpha, predicts the measurements well."
        elif all(v > 0 for v in diff.values()):
            fit = ("The measurements beat the formula: acceptances aren't independent, and easy stretches of text "
                   "let several drafts through in a row.")
        else:
            fit = ("The formula is only a guide: acceptances aren't independent, and later drafts, built on "
                   "earlier guesses, fare differently from the first.")
        who = "the EAGLE head" if best == "eagle" else "the small model"
        e0, e3, d0, d3 = dep["eagle"][0], dep["eagle"][-1], dep["draft"][0], dep["draft"][-1]
        if e3 < e0 - 0.05:
            dep_say = (f"Draft by draft, the head's acceptance falls from {e0:.2f} for the first to {e3:.2f} for the "
                       f"fourth, because it is feeding on its own guesses; the small model's goes from {d0:.2f} to "
                       f"{d3:.2f}.")
        else:
            dep_say = (f"Draft by draft, the head's acceptance goes from {e0:.2f} for the first to {e3:.2f} for the "
                       f"fourth, and the small model's from {d0:.2f} to {d3:.2f}: once a stretch of text is "
                       "predictable, the next draft tends to be right too.")
        if gr[best] > meas[best][k4]:
            greedy_say = (f"Decoding greedily, the drafts survive more often: {gr[best]:.2f} tokens per pass for "
                          f"{who}.")
        else:
            greedy_say = f"Decoding greedily, {who} gets {gr[best]:.2f} tokens per pass."
        with self.voiceover(
            "Now the real thing: speculative sampling on twelve held-out openings, ninety-six tokens each. "
            "<bookmark mark='a'/> With four drafts per pass, the small model gets "
            f"{meas['draft'][k4]:.2f} tokens out of each pass of the big model, and the EAGLE head "
            f"{meas['eagle'][k4]:.2f}. <bookmark mark='b'/> The lines are the formula, with alpha measured on the "
            "first draft. " + fit + " <bookmark mark='c'/> " + dep_say + " <bookmark mark='d'/> " + greedy_say
        ) as vo:
            self.play(FadeIn(g), Create(one), FadeIn(key[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for grp in dots for d_ in grp], lag_ratio=0.08), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(lines[0]), Create(lines[1]), FadeIn(key[1:]))
            vo.wait_until("c")
            self.play(FadeIn(dl))
            vo.wait_until("d")
            self.play(FadeIn(gl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def clock(self):
        d = load("drafters")
        tm = d["timing"]
        cfg = [tuple(c) for c in tm["configs"]]
        tpt = {c: t / tm["tokens"] * 1e3 for c, t in zip(cfg, tm["t"])}  # ms per token
        plain = tpt[("plain", 0, 1.0)]
        rows = [(("plain", 0, 1.0), r"one token per pass", GREY_B)]
        rows += [(("draft", k, 1.0), rf"small model, \ $k = {k}$", DRAFTC) for k in (1, 2, 4)]
        rows += [(("eagle", k, 1.0), rf"EAGLE head, \ $k = {k}$", EAGLEC) for k in (1, 2, 4)]
        vals = [tpt[c] for c, _, _ in rows]
        b = hbars(vals, [r[1] for r in rows], [r[2] for r in rows], width=4.0, row_h=0.46, font_size=20, lo=0,
                  hi=max(vals) * 1.08, fmt_v=lambda v: rf"{v:.2f}\,\text{{ms}}")
        b.move_to([-1.6, 0.2, 0])
        head = label(r"time per token written, \ this computer, \ one core", font_size=24, color=GREY_A).to_edge(UP,
                                                                                                             buff=0.4)
        pt = np.asarray(d["piece_target"]) * 1e3
        pn = list(d["piece_n"])
        pieces = VGroup(label(r"one pass of the big model:", font_size=20, color=GREY_A),
                        label(rf"$1$ token: \ ${pt[0]:.2f}$ ms", font_size=20, color=TARGETC),
                        label(rf"$5$ tokens: \ ${pt[pn.index(5)]:.2f}$ ms", font_size=20, color=TARGETC),
                        label(rf"one step of the small model: \ ${1e3 * d['piece_draft']:.2f}$ ms", font_size=20,
                              color=DRAFTC)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.6, 0.6, 0])
        best_c = min(cfg[1:], key=lambda c: tpt[c])
        sp = plain / tpt[best_c]
        five = pt[pn.index(5)] / pt[0]
        name = {"draft": "the small model", "eagle": "the EAGLE head"}[best_c[0]]
        if sp > 1.1:
            verdict = (f"The best, {name} with {best_c[1]} drafts, writes a token in {tpt[best_c]:.2f} milliseconds "
                       f"against {plain:.2f}: {sp:.1f} times faster.")
        elif sp > 1.0:
            verdict = (f"The best, {name} with {best_c[1]} drafts, is barely faster: {tpt[best_c]:.2f} milliseconds a "
                       f"token against {plain:.2f}.")
        else:
            verdict = (f"The best, {name} with {best_c[1]} drafts, is no faster: {tpt[best_c]:.2f} milliseconds a "
                       f"token against {plain:.2f}.")
        pubs = VGroup(label(r"published speed-ups:", font_size=19, color=GREY_A),
                      label(rf"Medusa (2024): \ ${F.MEDUSA['gain2'][0]}$--${F.MEDUSA['gain2'][1]}\times$", font_size=19,
                            color=GREY_A),
                      label(rf"EAGLE (2024): \ ${F.EAGLE['gain'][0]}$--${F.EAGLE['gain'][1]}\times$; \ EAGLE-3 (2025): "
                            rf"up to ${F.EAGLE3['gain']}\times$", font_size=19, color=EAGLEC),
                      label(rf"DeepSeek-V3's MTP module: \ ${F.DSV3['mtp_accept'][0]}$--${F.DSV3['mtp_accept'][1]}\%$ "
                            rf"accepted, \ ${F.DSV3['mtp_tps']}\times$ tokens/s", font_size=19, color=ACCEPTC))
        pubs.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.9, -2.2, 0])
        if five > 1.3:
            check = (f"checking five tokens in one pass costs {five:.1f} times what one token does: a processor core "
                     "has little arithmetic to spare, so the check isn't free the way it nearly is on a GPU.")
        else:
            check = (f"checking five tokens in one pass costs only {five:.1f} times what one token does: the pass "
                     "is mostly reading weights, as on a GPU.")
        with self.voiceover(
            "And the clock? <bookmark mark='a'/> On this computer, " + check + " <bookmark mark='b'/> " + verdict + " "
            "<bookmark mark='c'/> On GPUs, where a pass of a few tokens costs about as much as a pass of one, "
            "published systems do better. Medusa adds extra heads to the model; EAGLE-3 reports up to six and a "
            "half times; and DeepSeek-V3 trains its own drafter during pretraining, the multi-token prediction "
            "module of Part 18, whose second token is accepted 85 to 90 percent of the time."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pieces))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_.name), GrowFromEdge(r_.bar, LEFT), FadeIn(r_.val))
                                    for r_ in b], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(pubs))
        self.wait(0.3)
        self.clear_scene()
