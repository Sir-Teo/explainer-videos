from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai30.common import CAUSE, CTRL, PART, RESID, heads_grid, heat_image, load, ticks

PREV = C.TRUE_P  # the previous-token head
IND = C.BITS  # the induction head


class Patching(VoiceoverScene):
    def construct(self):
        self.card()
        self.copying()
        self.model()
        self.heat()
        self.heads()

    def card(self):
        card = chapter_card(4, r"Cause, not correlation", r"Which parts of the model make it do that?", part=PART)
        with self.voiceover("Chapter four. Cause, not correlation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def copying(self):
        d = load("induction")
        rows = [(r"Part 13's character transformer", float(d["tf_text1"]), float(d["tf_text2"]), int(d["tf_tokens"]),
                 r"bits per character"),
                (r"the novels model", float(d["nov_text1"]), float(d["nov_text2"]), int(d["nov_tokens"]),
                 r"bits per token")]
        g = VGroup()
        top = max(max(a, b) for _, a, b, _, _ in rows) * 1.1
        for i, (nm, a, b, tok, unit) in enumerate(rows):
            x0 = -4.2 + 6.6 * i
            ba = Rectangle(width=0.9, height=a / top * 3.0, stroke_width=0, fill_color=CTRL, fill_opacity=0.9)
            bb = Rectangle(width=0.9, height=b / top * 3.0, stroke_width=0, fill_color=CAUSE, fill_opacity=0.9)
            ba.move_to([x0 - 0.6, -2.2, 0], aligned_edge=DOWN)
            bb.move_to([x0 + 0.6, -2.2, 0], aligned_edge=DOWN)
            ta = MathTex(f"{a:.2f}", font_size=28, color=CTRL).next_to(ba, UP, buff=0.08)
            tb = MathTex(f"{b:.2f}", font_size=28, color=CAUSE).next_to(bb, UP, buff=0.08)
            la = label(r"first time", font_size=18, color=CTRL).next_to(ba, DOWN, buff=0.12)
            lb = label(r"second time", font_size=18, color=CAUSE).next_to(bb, DOWN, buff=0.12)
            nm_ = label(nm, font_size=24, color=WHITE).move_to([x0, 1.75, 0])
            un = label(rf"{unit}; \ trained on ${tok / 1e6:.0f}$ million", font_size=18, color=GREY_B).next_to(nm_, DOWN, buff=0.1)
            g.add(VGroup(ba, bb, ta, tb, la, lb, nm_, un))
        head = label(r"Held-out text shown twice: \ is the repeat any easier?", font_size=32).to_edge(UP, buff=0.35)
        drop = max(rows[0][1] - rows[0][2], rows[1][1] - rows[1][2])
        none = drop < 0.25
        verdict = ("Neither of our models copies. Olsson and colleagues saw the heads that copy form in their models "
                   "between about 2.5 and 5 billion tokens of training; ours stopped at about "
                   f"{int(round(rows[0][3] / 1e6))} million. " if none else "Some copying, but little. ")
        with self.voiceover(
            "To find what causes a behaviour, you need a behaviour with a known answer. The classic is copying: "
            "show a model a passage twice, and the second time it should be easy, since the model can look back. "
            f"<bookmark mark='a'/> Part 13's character transformer: {rows[0][1]:.2f} bits per character the first "
            f"time, {rows[0][2]:.2f} the second. <bookmark mark='b'/> The novels model: {rows[1][1]:.2f} bits per "
            f"token, then {rows[1][2]:.2f}. {verdict}<bookmark mark='c'/> So for a circuit to take apart, we go back to Part 13's two-layer, "
              "attention-only model, trained on random tokens with one stretch repeated, where copying is the only "
              "thing worth learning."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g[0][6:]), GrowFromEdge(g[0][0], DOWN), FadeIn(g[0][2]), FadeIn(g[0][4]))
            self.play(GrowFromEdge(g[0][1], DOWN), FadeIn(g[0][3]), FadeIn(g[0][5]))
            vo.wait_until("b")
            self.play(FadeIn(g[1][6:]), GrowFromEdge(g[1][0], DOWN), FadeIn(g[1][2]), FadeIn(g[1][4]))
            self.play(GrowFromEdge(g[1][1], DOWN), FadeIn(g[1][3]), FadeIn(g[1][5]))
            vo.wait_until("c")
            self.play(g.animate.set_opacity(0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def model(self):
        d = load("induction")
        cv = np.asarray(d["curve"])
        S = float(cv[-1, 0])
        top = float(cv[:, 1:].max())
        g = axes([0, S], [0, top * 1.05], x_length=5.6, y_length=3.4, xlabel=r"training steps",
                 ylabel=r"bits per token", xticks=[0, S], yticks=ticks(0, top, 3), center=[-3.6, -0.6, 0])
        c1 = curve(g.ax, cv[:, 0], cv[:, 1], CAUSE, 3)
        c2 = curve(g.ax, cv[:, 0], cv[:, 2], CTRL, 3)
        lg = legend([(CAUSE, r"inside the repeat"), (CTRL, r"elsewhere (random)")], font_size=18)
        lg.next_to(g, UP, buff=0.1).align_to(g, RIGHT)
        hp, hi = int(d["prev_head"]), int(d["ind_head"])
        ps, is_ = d["prev_scores"], d["ind_scores"]
        m1 = heat_image(np.asarray(d["ex_prev"])[50:80, 0:40], 2.8, 2.1, color=PREV, gamma=0.6)
        m2 = heat_image(np.asarray(d["ex_ind"])[50:80, 0:40], 2.8, 2.1, color=IND, gamma=0.6)
        Group(m1, m2).arrange(RIGHT, buff=0.5).move_to([3.6, -0.2, 0])
        t1 = label(rf"layer 1, \ head ${hp + 1}$: \\ the previous token \ (${ps[hp]:.2f}$)", font_size=18, color=PREV).next_to(m1, UP, buff=0.12)
        t2 = label(rf"layer 2, \ head ${hi + 1}$: \\ the token after the match \ (${is_[hi]:.2f}$)", font_size=18,
                   color=IND).next_to(m2, UP, buff=0.12)
        ax_ = label(r"rows: \ queries $50$--$79$ \quad columns: \ keys $0$--$39$ \ (the repeat copies $10$--$29$ to $60$--$79$)",
                    font_size=16, color=GREY_B).next_to(Group(m1, m2), DOWN, buff=0.2)
        tag = note(r"retrained here: \ Part 13's recipe and seed").to_corner(DR, buff=0.2)
        with self.voiceover(
            f"We retrain it here with Part 13's recipe and seed. <bookmark mark='a'/> For a while it learns nothing "
            f"useful; then, suddenly, the repeat becomes easy, falling from {cv[0, 1]:.1f} to {cv[-1, 1]:.1f} bits "
            "per token while random tokens stay as hard as ever. <bookmark mark='b'/> Look at the attention. In layer "
            f"one, {len(d['prev_set'])} of the four heads look mostly at the previous token; here is head {hp + 1}. "
            f"<bookmark mark='c'/> In layer two, {len(d['ind_set'])} heads, at a token in the second copy, look at the "
            "token just after that token's first occurrence: the one to copy. Previous-token heads and induction "
            "heads. But attention patterns are a correlation too. Are these heads the cause?"
        ) as vo:
            self.play(FadeIn(g), FadeIn(lg), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(c2), Create(c1), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(m1), FadeIn(t1), FadeIn(ax_))
            vo.wait_until("c")
            self.play(FadeIn(m2), FadeIn(t2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heat(self):
        d = load("induction")
        H = np.asarray(d["heat"])  # (3, T): layer boundary, patched position
        tgt = int(d["target"])
        lo, hi_ = 0, tgt + 4
        Hs = np.clip(H[:, lo:hi_], 0, 1)
        W, Hh = 10.6, 1.9
        img = heat_image(Hs[::-1], W, Hh, color=CAUSE, gamma=0.7).move_to([0.9, -1.2, 0])
        n = hi_ - lo
        cw = W / n
        xs = lambda j: img.get_left()[0] + cw * (j - lo + 0.5)  # noqa: E731
        rl = VGroup(*[label(t, font_size=18, color=GREY_A).next_to([img.get_left()[0], img.get_top()[1] - Hh / 3 * (k + 0.5), 0], LEFT, buff=0.1)
                      for k, t in enumerate([r"output", r"between layers", r"input"])])
        marks = VGroup()
        for j, t in ((20, r"$20$"), (21, r"$21$"), (tgt, rf"${tgt}$")):
            marks.add(MathTex(t.strip("$"), font_size=20, color=WHITE).move_to([xs(j), img.get_bottom()[1] - 0.22, 0]))
        xl = label(r"the position whose vector is swapped for the corrupted one", font_size=18, color=GREY_B).next_to(marks, DOWN, buff=0.1)
        dc = definition_card(r"activation patching", r"run the model on a clean input and on a corrupted one; copy one "
                             r"activation from one run into the other, \ and measure how much of the behaviour moves "
                             r"with it.", color=CAUSE, width=6.6, font_size=21).to_corner(UL, buff=0.3)
        setup = label(rf"clean: \ tokens $10$--$29$ repeated at $60$--$79$ \\ corrupted: \ $10$--$29$ replaced at "
                      rf"random \\ measured: \ $\log p$ of token ${tgt + 1}$, \ predicted at ${tgt}$", font_size=19,
                      color=GREY_A).to_corner(UR, buff=0.35)
        hcs = VGroup(history_card(2020, r"J.~Vig et al.", r"causal mediation analysis of gender bias", width=3.4,
                                  color=CAUSE, font_size=16),
                     history_card(2022, r"K.~Meng et al.", r"causal tracing: \ where GPT stores facts", width=3.4,
                                  color=CAUSE, font_size=16)).arrange(RIGHT, buff=0.2).next_to(setup, DOWN, buff=0.2)
        hcs.align_to(setup, RIGHT)
        cols = H[:, :tgt + 1]
        k_in = [j for j in range(tgt + 1) if cols[0, j] > 0.5]
        k_mid = [j for j in range(tgt + 1) if cols[1, j] > 0.5]
        names = lambda ks: ", ".join(str(k) for k in ks) if ks else "none"  # noqa: E731
        v_in = ("At the input, no single position breaks it on its own." if not k_in else
                f"At the input, breaking position {names(k_in)} breaks the copy.")
        with self.voiceover(
            "The tool is activation patching. <bookmark mark='a'/> Run the model twice: on the clean sequence, with "
            "its repeat, and on a corrupted one, the first copy replaced by fresh random tokens, so there is nothing "
            f"to copy. Then take one vector from the corrupted run, put it into the clean run, and see how much of "
            f"the right prediction at position {tgt} is lost. Kevin Meng and colleagues used patching to find where "
            "GPT stores facts. <bookmark mark='b'/> Swap the residual stream at every position, at the input, "
            f"between the layers, and at the output. {v_in} "
            f"<bookmark mark='c'/> Between the layers, {names(k_mid)}. <bookmark mark='d'/> At the output, only "
            f"position {tgt} itself. The information about what to copy starts at the first copy, moves one step "
            "within it, and then jumps to the second copy: that is the circuit's route."
        ) as vo:
            self.play(FadeIn(dc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(setup), FadeIn(hcs))
            vo.wait_until("b")
            self.play(FadeOut(hcs), FadeIn(img), FadeIn(rl), FadeIn(marks), FadeIn(xl))
            vo.wait_until("c")
            self.play(Indicate(rl[1], color=CAUSE))
            vo.wait_until("d")
            self.play(Indicate(rl[0], color=CAUSE))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heads(self):
        d = load("induction")
        nz = np.asarray(d["head_noise"])
        ps_, is_, sh = [int(h) for h in d["prev_set"]], [int(h) for h in d["ind_set"]], int(d["self_head"])
        g = heads_grid(nz, CAUSE, cell=0.9, fmt="{:.2f}", vmax=1.0, font_size=24).move_to([-2.6, -0.4, 0])
        cap = label(r"each head's output taken from the corrupted run, \ put into the clean one: \\ how much of the "
                    r"copying is lost \ ($1$: all of it)", font_size=20, color=GREY_A).next_to(g, UP, buff=0.35)
        team = {(0, h) for h in ps_ + [sh]} | {(1, h) for h in is_}
        others = [nz[l_, h] for l_ in range(2) for h in range(4) if (l_, h) not in team] or [0.0]
        fmt = lambda hs, l_: r", \ ".join(f"${nz[l_, h]:.2f}$" for h in hs)  # noqa: E731
        txt = label(rf"previous-token heads: \ {fmt(ps_, 0)} \\ the current-token head: \ ${nz[0, sh]:.2f}$ \\ "
                    rf"induction heads: \ {fmt(is_, 1)} \\ the rest: \ at most ${max(others):.2f}$", font_size=22,
                    color=WHITE).move_to([3.8, 0.5, 0])
        note_ = label(r"swapping in the corrupted run's vector \ (noising) \ tests what is \textit{necessary}; \\ the "
                      r"reverse \ (denoising) \ what is \textit{sufficient}", font_size=19, color=GREY_B).move_to([3.8, -2.1, 0])
        p_lo, p_hi = min(nz[0, h] for h in ps_), max(nz[0, h] for h in ps_)
        i_lo, i_hi = min(nz[1, h] for h in is_), max(nz[1, h] for h in is_)
        with self.voiceover(
            "Now the heads: run the clean sequence, and swap in one head's output from the corrupted run. "
            f"<bookmark mark='a'/> Corrupting one of the previous-token heads loses {100 * p_lo:.0f} to "
            f"{100 * p_hi:.0f} percent of the copying; the induction heads, {100 * i_lo:.0f} to {100 * i_hi:.0f}. "
            f"<bookmark mark='b'/> And one more head matters, head {sh + 1} of layer one, which mostly looks at the "
            f"token itself: {100 * nz[0, sh]:.0f} percent. No other head more than {100 * max(others):.0f}. A small "
            "team of heads carries the behaviour. Chapter five takes it apart."
        ) as vo:
            self.play(FadeIn(cap), FadeIn(g[1:]), FadeIn(g.cells))
            vo.wait_until("a")
            self.play(*[Indicate(g.cells[h], color=PREV) for h in ps_], *[Indicate(g.cells[4 + h], color=IND) for h in is_],
                      FadeIn(txt))
            vo.wait_until("b")
            self.play(Indicate(g.cells[sh], color=CAUSE), FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()
