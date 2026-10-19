from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai16.common import EXPERT_COLORS, MONO, load


def dense_vs_sparse(E: int, k: int) -> VGroup:
    """A dense layer, every weight lit for every token, beside a mixture with only k of its E experts lit."""
    dense = Rectangle(width=1.5, height=1.0, stroke_color=GREY_B, stroke_width=2, fill_color=GREY_B, fill_opacity=0.7)
    dl = label(r"dense: \ every weight \\ works on every token", font_size=18, color=GREY_B).next_to(dense, DOWN, buff=0.12)
    lit = set(np.linspace(1, E - 2, k).round().astype(int)) if k < E else set(range(E))
    boxes = VGroup(*[Square(0.4, stroke_color=C.INTERVAL, stroke_width=1.5, fill_color=C.INTERVAL,
                            fill_opacity=0.85 if i in lit else 0.05) for i in range(E)])
    boxes.arrange_in_grid(rows=2, buff=0.08).match_height(dense)
    ml = label(r"mixture: \ only a few \\ experts run", font_size=18, color=C.INTERVAL).next_to(boxes, DOWN, buff=0.12)
    left, right = VGroup(dense, dl), VGroup(boxes, ml)
    VGroup(left, right).arrange(RIGHT, buff=0.7, aligned_edge=UP)
    return VGroup(left, right)


class Special(VoiceoverScene):
    def construct(self):
        self.card()
        self.routes()
        self.forming()
        self.race()
        self.worth()

    def card(self):
        card = chapter_card(3, r"What experts learn", r"Do experts specialize?", part=16)
        with self.voiceover("Chapter three. What experts learn."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def routes(self):
        m = load("moe")
        chars = [str(c_) for c_ in m["route_chars"]]
        M = np.asarray(m["route"])
        E = M.shape[1]
        cell = min(0.36, 11.5 / len(chars))
        grid = VGroup()
        for i in range(len(chars)):
            for j in range(E):
                v = float(M[i, j])
                grid.add(Square(cell, stroke_width=0.4, stroke_color=GREY_D, fill_color=EXPERT_COLORS[j],
                                fill_opacity=0.05 + 0.9 * v).move_to([i * cell, -j * cell, 0]))
        grid.center().move_to(DOWN * 0.2)
        names = VGroup(*[(Text(c_ if c_ != " " else "␣", font=MONO, font_size=22, color=C.BITS if c_ in "aeiou" else GREY_A)).next_to(grid[i * E], UP, buff=0.08)
                         for i, c_ in enumerate(chars)])
        el = VGroup(*[MathTex(rf"E_{j + 1}", font_size=24, color=EXPERT_COLORS[j]).next_to(grid[j], LEFT, buff=0.1) for j in range(E)])
        head = label(r"where each character sends its context \ (the expert chosen first, \ trained with the bias)",
                     font_size=24, color=GREY_A).to_edge(UP, buff=0.4)
        top1 = M.argmax(1)
        vow = [i for i, c_ in enumerate(chars) if c_ in "aeiou"]
        punct = [i for i, c_ in enumerate(chars) if c_ in " .,;\"'?!"]
        bv = np.bincount(top1[vow], minlength=E)
        ev, cv = int(bv.argmax()), int(bv.max())  # the expert most vowels go to first, and how many
        bp = np.bincount(top1[punct], minlength=E)
        ep = [int(e) for e in np.argsort(-bp)[:2]]
        cp = int(bp[ep].sum())  # how many marks go to the two most popular experts
        pattern = cv * 2 > len(vow) or cp * 4 >= 3 * len(punct)
        note_ = label(r"columns: \ the last character read; \ rows: \ experts; \ bright: \ often chosen", font_size=20,
                      color=GREY_B).next_to(grid, DOWN, buff=0.3)
        verdict = label((rf"${cv}$ of the ${len(vow)}$ vowels go first to $E_{ev + 1}$; \ "
                         rf"${cp}$ of the ${len(punct)}$ spaces and marks to $E_{ep[0] + 1}$ or $E_{ep[1] + 1}$")
                        if pattern else
                        r"no neat specialties: \ experts split the work in ways \\ that don't map onto our categories",
                        font_size=26, color=C.BITS).to_edge(DOWN, buff=0.4)
        boxes = VGroup()
        if pattern:
            for idx, es in ((vow, (ev,)), (punct, tuple(ep))):
                for i in idx:
                    if top1[i] in es:
                        e = int(top1[i])
                        boxes.add(SurroundingRectangle(grid[i * E + e], color=WHITE, buff=0.0, stroke_width=2))
        with self.voiceover(
            "What do the experts learn? Here's where our balanced model sends each character's context: one column "
            "per character just read, one row per expert. <bookmark mark='a'/> "
            + (f"Some patterns appear: {cv} of the {len(vow)} vowels go first to expert {ev + 1}, and {cp} of the "
               f"{len(punct)} spaces and punctuation marks to experts {ep[0] + 1} and {ep[1] + 1}. Nobody told it to. "
               "But it isn't a tidy division by meaning: in large models too, experts tend to split the work along "
               "surface patterns like these."
               if pattern else
               "There's structure, but not the neat specialties people imagine: in large models too, experts tend to "
               "split the work along surface patterns, not topics.")
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid), FadeIn(names), FadeIn(el), FadeIn(note_))
            vo.wait_until("a")
            self.play(FadeIn(verdict), LaggedStart(*[Create(b_) for b_ in boxes], lag_ratio=0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def worth(self):
        m = load("moe")
        E, k = int(m["E"]), int(m["k"])
        rows = [(rf"dense, \ as much compute \ ($1$ layer of ${k}$ experts' width)", float(m["bits_dense_active"]), GREY_B),
                (rf"mixture: \ ${k}$ of ${E}$ experts", float(m["bits_bias"]), C.INTERVAL),
                (rf"dense, \ as many parameters \ (${E}$ experts' width)", float(m["bits_dense_total"]), GREY_A)]
        lo = min(r[1] for r in rows) - 0.06
        hi = max(r[1] for r in rows) + 0.03
        sc = 6.0 / (hi - lo)
        g = VGroup()
        for i, (t, v, col) in enumerate(rows):
            y = 1.2 - i * 1.0
            nm = label(t, font_size=24, color=col).move_to([-0.6, y, 0], aligned_edge=RIGHT)
            w = (v - lo) * sc
            bar = Rectangle(width=w, height=0.45, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to([-0.3 + w / 2, y, 0])
            val = MathTex(f"{v:.3f}", font_size=28, color=col).next_to(bar, RIGHT, buff=0.12)
            g.add(VGroup(nm, bar, val))
        head = label(r"held-out bits per character \ (shorter is better; \ axis starts at "
                     + f"${lo:.2f}$)", font_size=24, color=GREY_A).to_edge(UP, buff=0.5)
        da, mx, dt = rows[0][1], rows[1][1], rows[2][1]
        if dt < da and mx < da:  # the usual picture: the big dense model is best, the mixture gets part of the way
            gain = (da - mx) / (da - dt)
            verdict = (f"<bookmark mark='b'/> The mixture gets {100 * min(gain, 1):.0f} percent of the way from the first "
                       "to the third, for the cost of the first. ")
        elif mx < da:
            verdict = (f"<bookmark mark='b'/> The mixture, {mx:.3f}, beats the dense model with the same arithmetic, "
                       f"{da:.3f}. And with the same short training, the dense model with all the parameters does no "
                       f"better, {dt:.3f}: eight times the width is more to learn, and it hasn't caught up. ")
        else:
            verdict = (f"<bookmark mark='b'/> At our tiny scale the mixture doesn't pay off: {mx:.3f}, against {da:.3f} "
                       "for the dense model with the same arithmetic. ")
        with self.voiceover(
            "Is it worth it? Compare three models. <bookmark mark='a'/> A dense one doing as much arithmetic per "
            "character as the mixture; the mixture; and a dense one with as many parameters in total. "
            + verdict + "At scale, that's the trade the biggest models make: knowledge in the total, cost in the active."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(Indicate(g[1], color=C.INTERVAL))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def forming(self):
        """How the routing forms: the same picture at checkpoints during training."""
        m = load("moe")
        chars = [str(c_) for c_ in m["route_chars"]]
        R = np.asarray(m["routes"])
        steps = [int(s_) for s_ in m["route_steps"]]
        E = R.shape[2]
        cell = min(0.36, 11.5 / len(chars))

        def grid(k):
            g = VGroup()
            for i in range(len(chars)):
                for j in range(E):
                    g.add(Square(cell, stroke_width=0.4, stroke_color=GREY_D, fill_color=EXPERT_COLORS[j],
                                 fill_opacity=0.05 + 0.9 * float(R[k, i, j])).move_to([i * cell, -j * cell, 0]))
            return g.center().move_to(DOWN * 0.2)

        cur = grid(0)
        names = VGroup(*[(Text(c_ if c_ != " " else "␣", font=MONO, font_size=22, color=C.BITS if c_ in "aeiou" else GREY_A))
                         .next_to(cur[i * E], UP, buff=0.08) for i, c_ in enumerate(chars)])
        el = VGroup(*[MathTex(rf"E_{j + 1}", font_size=24, color=EXPERT_COLORS[j]).next_to(cur[j], LEFT, buff=0.1) for j in range(E)])
        t = ValueTracker(0)
        cnt = always_redraw(lambda: MathTex(rf"\text{{training step }}{int(t.get_value()):,}".replace(",", "{,}"), font_size=30,
                                            color=WHITE).to_edge(UP, buff=0.45))
        # how decided the choices are: the average share of a character's contexts that go to its favourite expert
        sharp = [float(R[k].max(1).mean()) for k in range(len(steps))]
        top_change = [int((R[k].argmax(1) != R[-1].argmax(1)).sum()) for k in range(len(steps))]
        with self.voiceover(
            "How did that pattern form? Here is the same picture during training. <bookmark mark='a'/> At the start "
            "the router is random and nearly uniform, so each character's contexts are spread over the experts: on "
            f"average its favourite gets {100 * sharp[0]:.0f} percent. <bookmark mark='b'/> Within {steps[1]} steps "
            f"the router commits hard: the favourite's share jumps to {100 * sharp[1]:.0f} percent. "
            + (f"<bookmark mark='c'/> Then the balancing bias pushes back, lowering the bias of experts that are too "
               f"busy, and the choices spread out again, to {100 * sharp[-1]:.0f} percent by the end. "
               if sharp[-1] < sharp[1] - 0.1 else
               f"<bookmark mark='c'/> It stays that decided: {100 * sharp[-1]:.0f} percent by the end. ")
            + f"The favourites keep changing for a long time: {top_change[2]} of the {len(chars)} characters still "
            f"switch expert after step {steps[2]}, and {top_change[3]} after step {steps[3]:,}."
        ) as vo:
            self.play(FadeIn(cur), FadeIn(names), FadeIn(el))
            self.add(cnt)
            vo.wait_until("a")
            for k, mk in zip(range(1, len(steps)), ("b", "c", None, None)):
                if mk:
                    vo.wait_until(mk)
                nxt = grid(k)
                self.play(Transform(cur, nxt), t.animate.set_value(steps[k]), run_time=1.5)
        self.wait(0.4)
        self.remove(cnt)
        self.clear_scene()

    # ------------------------------------------------------------------
    def race(self):
        """The three models of the comparison, as they train."""
        m = load("moe")
        E, k = int(m["E"]), int(m["k"])
        cs = [("dense_active", rf"dense, \ as much compute", GREY_B), ("bias", rf"mixture: \ ${k}$ of ${E}$ experts", C.INTERVAL),
              ("dense_total", rf"dense, \ as many parameters", "#7FD3FF")]
        D = {key: np.asarray(m[f"curve_{key}"]) for key, _, _ in cs}
        total = float(D["bias"][-1, 0])
        lo = math.floor((min(float(d[:, 1][2:].min()) for d in D.values()) - 0.05) * 4) / 4  # on a tick
        hi = float(D["bias"][2, 1]) + 0.3
        ax = Axes(x_range=[0, total, 500], y_range=[lo, hi, 0.25], x_length=8.0, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.5, -0.4, 0])
        yl = VGroup(*[MathTex(f"{v:.2f}", font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in np.arange(np.ceil(lo * 4) / 4, hi, 0.25)])
        xv = VGroup(*[MathTex(f"{v:,}".replace(",", "{,}"), font_size=20, color=GREY_B).next_to(ax.c2p(v, lo), DOWN, buff=0.1)
                      for v in (0, int(total))])
        yl.add(*xv)
        xl = label(r"training steps", font_size=22, color=GREY_A).next_to(xv, DOWN, buff=0.1)
        yn = label(r"held-out bits per character", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        lines = [VMobject(color=col, stroke_width=3.5).set_points_as_corners(
            [ax.c2p(a, min(b, hi)) for a, b in D[key][1:]]) for key, _, col in cs]
        names = VGroup(*[label(nm, font_size=22, color=col) for _, nm, col in cs]).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        names.move_to([4.7, 0.9, 0])
        keep_in_frame(names)
        # where the mixture pulls ahead of the dense model with the same compute, if it does, and stays ahead
        a_, b_ = D["dense_active"], D["bias"]
        ahead = [i for i in range(len(b_)) if all(b_[j, 1] < a_[j, 1] for j in range(i, len(b_)))]
        when = int(b_[ahead[0], 0]) if ahead else None
        dz = gloss(r"dense model", r"an ordinary layer: every weight works on every token", dense_vs_sparse(E, k),
                   corner=UR, width=4.2, color=GREY_B)
        with self.voiceover(
            "And here are the three models of that comparison as they train. <bookmark mark='w'/> Two are dense: "
            "ordinary layers, where every weight works on every token. The third is the mixture, where each token "
            "uses only a few experts. Held-out bits per character every "
            f"{int(D['bias'][1, 0])} steps. <bookmark mark='a'/> "
            + (f"The mixture pulls ahead of the dense model with the same arithmetic by step {when:,} and stays ahead. "
               if when is not None and when > 0 else
               "The mixture is ahead of the dense model with the same arithmetic from the start. " if when == 0 else
               "The mixture never gets clear of the dense model with the same arithmetic. ")
            + "<bookmark mark='b'/> "
            + (f"The wide dense model, {E} experts' width, trails the whole way: with this little training, all those "
               "parameters haven't paid off yet."
               if all(D["dense_total"][j_, 1] >= D["bias"][j_, 1] for j_ in range(1, len(D["bias"]))) else
               f"The wide dense model, {E} experts' width, ends at {D['dense_total'][-1, 1]:.2f}.")
        ) as vo:
            self.play(Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(yn))
            vo.wait_until("w")
            self.play(FadeIn(dz, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(dz), run_time=0.5)
            self.play(Create(lines[0]), Create(lines[1]), FadeIn(names[0]), FadeIn(names[1]), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(lines[2]), FadeIn(names[2]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
