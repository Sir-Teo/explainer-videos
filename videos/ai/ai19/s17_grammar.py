from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai19.common import (ACCEPTC, F, MONO, PART, REJECTC, TARGETC, load)

OKC, BADC, AUTOC = ACCEPTC, REJECTC, C.BITS


def mono_lines(lines, font_size=18, color=WHITE, width=12.6):
    g = VGroup(*[data_text(s if s else " ", font=MONO, font_size=font_size, color=color) for s in lines])
    g.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    for t in g:
        if t.width > width:
            t.width = width
    return g


class Grammar(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.automaton()
        self.results()
        self.distortion()

    def card(self):
        card = chapter_card(16, r"Constrained decoding", r"Can a model be made to write only valid output?", part=PART)
        with self.voiceover("Chapter sixteen. Constrained decoding."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def problem(self):
        gr = load("grammar")
        prompt = str(gr["prompt"]).rstrip("\n").split("\n")
        pl = mono_lines(prompt, font_size=20, color=GREY_A).to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.6)
        ph = label(r"the prompt", font_size=20, color=GREY_B).next_to(pl, RIGHT, buff=0.4).align_to(pl, UP)
        outs = mono_lines([s[:70] for s in gr["samples_un"][:6]], font_size=19, color=BADC)
        outs.next_to(pl, DOWN, buff=0.6).align_to(pl, LEFT)
        ol = label(rf"what our novels model writes next: \ ${gr['valid_un']}$ of ${gr['n']}$ are valid records",
                   font_size=22, color=BADC).next_to(outs, DOWN, buff=0.4).align_to(pl, LEFT)
        un_say = (f"of {gr['n']} tries, not one was a valid record." if gr["valid_un"] == 0 else
                  f"of {gr['n']} tries, {gr['valid_un']} were valid records.")
        with self.voiceover(
            "Programs that call a model often need its answer in a fixed format: a record, a function call, a "
            "number. <bookmark mark='a'/> Our novels model has never seen such a thing. Shown three records of "
            "guests at an inn, and asked for the next, <bookmark mark='b'/> it goes back to writing novels: "
            + un_say + " Big models do far better, but 'usually' isn't good enough for a program."
        ) as vo:
            self.play(FadeIn(pl), FadeIn(ph))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(o_, shift=RIGHT * 0.1) for o_ in outs], lag_ratio=0.2), run_time=2.0)
            self.play(FadeIn(ol))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def automaton(self):
        gr = load("grammar")
        # the pattern, and its automaton drawn as a chain of states (schematic: literal runs collapsed)
        pat = data_text(r'{"name": "[A-Z][a-z]{1,11}", "age": [1-9][0-9]?}', font=MONO, font_size=24, color=AUTOC)
        pat.to_edge(UP, buff=0.45)
        steps = [r'{"name": "', r"A-Z", r"a-z", r'", "age": ', r"1-9", r"0-9", r"}"]
        nodes = VGroup(*[Circle(radius=0.28, stroke_color=AUTOC, stroke_width=2, fill_color=AUTOC, fill_opacity=0.1)
                         for _ in range(len(steps) + 1)]).arrange(RIGHT, buff=1.05).move_to([0, 1.2, 0])
        nodes[-1].set_stroke(width=4)
        edges = VGroup(*[Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), buff=0.05, stroke_width=2, color=GREY_B,
                               max_tip_length_to_length_ratio=0.2) for i in range(len(steps))])
        elab = VGroup(*[data_text(s, font=MONO, font_size=15, color=WHITE).next_to(e_, UP, buff=0.08)
                        for s, e_ in zip(steps, edges)])
        loop = CurvedArrow(nodes[3].get_top() + LEFT * 0.12, nodes[3].get_top() + RIGHT * 0.12, angle=-4.0,
                           color=GREY_B, stroke_width=2, tip_length=0.12)
        skip = CurvedArrow(nodes[5].get_bottom(), nodes[7].get_bottom() + LEFT * 0.1, angle=0.9, color=GREY_B,
                           stroke_width=2, tip_length=0.12)
        tag = schematic_tag(corner=UR)
        al = label(rf"as a deterministic automaton over characters: \ ${gr['states']}$ states", font_size=20,
                   color=AUTOC).next_to(nodes, DOWN, buff=0.9)
        # the index: for each state, which of the 4,096 tokens may come next
        allowed = np.asarray(gr["allowed"])
        V = int(gr["vocab"])
        n = len(allowed)
        bars = VGroup(*[Rectangle(width=11.0 / n * 0.8, height=max(1.5 * a / V, 0.02), stroke_width=0, fill_color=OKC,
                                  fill_opacity=0.85).move_to([-5.5 + 11.0 * (i + 0.5) / n, -3.2 + 0.75 * a / V, 0])
                        for i, a in enumerate(allowed)])
        bl = label(rf"tokens allowed in each state, \ of ${V:,}$: \ at the start ${int(allowed[0])}$ "
                   rf"(\texttt{{\{{}}), \ inside a name ${gr['mid_allowed']:,}$".replace(",", "{,}"), font_size=19,
                   color=OKC).next_to(bars, UP, buff=0.15)
        hc = history_card(2023, r"Brandon Willard \& R\'emi Louf, \ Outlines", r"an index from automaton states to "
                          r"allowed tokens, \ built once", width=4.2, font_size=16, color=AUTOC).to_corner(UL, buff=0.2)
        hc.shift(DOWN * 0.9)
        with self.voiceover(
            "The fix is to make invalid output impossible. <bookmark mark='a'/> Write the format as a pattern, a "
            "regular expression, and compile it to an automaton: states, and the characters that move between them. "
            f"Ours has {gr['states']} states. <bookmark mark='b'/> But a model writes tokens, not characters, and a "
            "token can be several characters long. In 2023 Brandon Willard and Rémi Louf, in Outlines, built an "
            "index once, ahead of time: for every state, and every token of the vocabulary, run the token's "
            "characters through the automaton, and record whether it survives, and where it lands. "
            f"<bookmark mark='c'/> For our {V:,}-token vocabulary that took {gr['t_index']:.2f} seconds. At the "
            f"start only one token is allowed, the opening brace; inside a name, {gr['mid_allowed']:,}. Decoding "
            "then sets every disallowed token's probability to zero, a lookup per step."
        ) as vo:
            self.play(FadeIn(pat), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(n_) for n_ in nodes], lag_ratio=0.1),
                      LaggedStart(*[GrowArrow(e_) for e_ in edges], lag_ratio=0.1), FadeIn(elab), Create(loop),
                      Create(skip), FadeIn(al), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(hc))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.03), FadeIn(bl), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        gr = load("grammar")
        outs = mono_lines(gr["samples_co"][:8], font_size=20, color=OKC).move_to([-2.4, 0.4, 0])
        ol = label(rf"with the mask: \ ${gr['valid_co']}$ of ${gr['n']}$ valid", font_size=24, color=OKC)
        ol.next_to(outs, UP, buff=0.4).align_to(outs, LEFT)
        tu = gr["t_un"] / max(gr["tokens_un"], 1) * 1e3
        tc = gr["t_co"] / max(gr["tokens_co"], 1) * 1e3
        cost = VGroup(label(r"time per token, \ this computer:", font_size=20, color=GREY_A),
                      label(rf"free sampling: \ ${tu:.2f}$ ms", font_size=20, color=GREY_A),
                      label(rf"with the mask: \ ${tc:.2f}$ ms", font_size=20, color=OKC))
        cost.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.6, 1.0, 0])
        hc = history_card(2024, r"Yixin Dong et al., \ XGrammar", rf"context-free grammars too, \ precomputed where "
                          rf"possible: \ up to ${F.XGRAMMAR['gain']}\times$ faster", width=4.2, font_size=16,
                          color=AUTOC).move_to([4.4, -1.6, 0])
        over = tc / tu - 1
        cost_say = (f"it costs nothing we can measure: {tc:.2f} milliseconds a token against {tu:.2f}."
                    if abs(over) < 0.1 else f"it costs {100 * over:.0f} percent more time per token.")
        mask_say = (f"every one of the {gr['n']} outputs is a valid record." if gr["valid_co"] == gr["n"] else
                    f"{gr['valid_co']} of the {gr['n']} outputs are valid records; the rest ran out of room before "
                    "they closed.")
        with self.voiceover(
            "<bookmark mark='a'/> With the mask, " + mask_say + " As for speed, " + cost_say +
            " <bookmark mark='b'/> Look at the names, though. The model has no idea what belongs in "
            "the field; the mask only rules out what can't. A mask fixes the form, not the sense. Grammars more "
            "complex than patterns, like JSON with nesting, need a stack as well, and XGrammar, in 2024, made "
            "those fast too."
        ) as vo:
            self.play(FadeIn(ol), LaggedStart(*[FadeIn(o_, shift=RIGHT * 0.1) for o_ in outs], lag_ratio=0.15),
                      FadeIn(cost), run_time=2.0)
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Indicate(outs, color=OKC, scale_factor=1.02), FadeIn(hc))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def distortion(self):
        gr = load("grammar")
        names = list(gr["names"])
        ex, mk = np.asarray(gr["exact"]), np.asarray(gr["masked"])
        k = len(names)
        X0, bw = -4.4, 0.42
        top = max(ex.max(), mk.max())
        b_ex = VGroup(*[Rectangle(width=bw, height=max(3.0 * v / top, 0.01), stroke_width=0, fill_color=TARGETC,
                                  fill_opacity=0.85).move_to([X0 + 1.4 * i - 0.24, -2.2 + 1.5 * v / top, 0])
                        for i, v in enumerate(ex)])
        b_mk = VGroup(*[Rectangle(width=bw, height=max(3.0 * v / top, 0.01), stroke_width=0, fill_color=AUTOC,
                                  fill_opacity=0.85).move_to([X0 + 1.4 * i + 0.24, -2.2 + 1.5 * v / top, 0])
                        for i, v in enumerate(mk)])
        base = Line([X0 - 0.6, -2.2, 0], [X0 + 1.4 * k - 0.6, -2.2, 0], color=GREY_C, stroke_width=1.5)
        xl = VGroup(*[data_text(nm, font=MONO, font_size=20, color=GREY_A).move_to([X0 + 1.4 * i, -2.5, 0])
                      for i, nm in enumerate(names)])
        vex = VGroup(*[MathTex(f"{100 * v:.1f}", font_size=16, color=TARGETC).next_to(b_, UP, buff=0.05) for v, b_ in
                       zip(ex, b_ex)])
        vmk = VGroup(*[MathTex(f"{100 * v:.1f}", font_size=16, color=AUTOC).next_to(b_, UP, buff=0.05) for v, b_ in
                       zip(mk, b_mk)])
        ctx = data_text("…" + str(gr["name_ctx"]).replace("\n", " ").strip()[-46:], font=MONO, font_size=20,
                        color=GREY_A).to_edge(UP, buff=0.4)
        q = label(r"Part 13's character model, \ told to write one of five names next", font_size=20,
                  color=GREY_A).next_to(ctx, DOWN, buff=0.15)
        key = VGroup(label(r"the model's own odds, \ among the five (\%)", font_size=20, color=TARGETC),
                     label(r"what masking letter by letter gives (\%)", font_size=20, color=AUTOC))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.4, 0.6, 0])
        i_big = int(np.argmax(mk / np.maximum(ex, 1e-9)))
        hc = history_card(2024, r"Kanghee Park et al.", r"grammar-aligned decoding: \ sample what the model would, "
                          r"\ given that the output is valid", width=4.0, font_size=16, color=AUTOC).move_to([4.4, -1.6, 0])
        with self.voiceover(
            "Masking has a subtler flaw. <bookmark mark='a'/> Ask Part 13's character model to write one of five "
            "names after a line of The Maltese Falcon, and compare two things. <bookmark mark='b'/> The model's "
            "own odds for each whole name, renormalized over the five: what you'd get by sampling it again and "
            "again and keeping only those names. <bookmark mark='c'/> And what masking, letter by letter, actually "
            "samples. At the first letter, masking only asks how likely an S, an A or an E is, whatever word it "
            f"would begin. So {names[i_big]} gets {100 * mk[i_big]:.0f} percent, though the model gives the whole "
            f"name only {100 * ex[i_big]:.1f}. "
            "<bookmark mark='d'/> Locally sensible choices add up to a distorted answer. In 2024 Kanghee Park and "
            "colleagues showed how to sample from the true conditional instead."
        ) as vo:
            self.play(FadeIn(ctx), FadeIn(q), Create(base), FadeIn(xl))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b_ex], lag_ratio=0.1), FadeIn(vex), FadeIn(key[0]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b_mk], lag_ratio=0.1), FadeIn(vmk), FadeIn(key[1]))
            vo.wait_until("d")
            self.play(FadeIn(hc), Indicate(b_mk[i_big], color=AUTOC, scale_factor=1.3))
        self.wait(0.3)
        self.clear_scene()
