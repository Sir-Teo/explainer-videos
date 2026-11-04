from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from explainer.cs.turing import CHAMPIONS, TM, run
from videos.cs.cs1.common import (ADV, CODE, COST, CTRL, DATA, HEAD, HIST, LIMIT, NO, PART, YES, fmt, say, live_int, load,
                                  spacetime_mob, step_counter)


def density_rgb(a: np.ndarray) -> np.ndarray:
    """0-255 density of ones as RGB, from the background to the colour of a 1."""
    t = (np.asarray(a, float) / 255.0)[..., None] ** 0.6
    lo, hi = hex_rgb("#151B26").astype(float), hex_rgb(C.BIT1).astype(float)
    return lo * (1 - t) + hi * t


class Beavers(VoiceoverScene, MovingCameraScene):
    def construct(self):
        self.card()
        self.game()
        self.two_states()
        self.champions()
        self.five()
        self.uncomputable()
        self.frontier()

    def card(self):
        card = chapter_card(13, r"Busy beavers", r"How long can a small machine run, and still stop?",
                            lit=(1962, 2024), part=PART)
        with self.voiceover("Chapter thirteen. Busy beavers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def game(self):
        hc = history_card(1962, r"Tibor Rad\'o", r"``On non-computable functions'': \ a game for machines",
                          width=5.6, font_size=22).to_corner(UL, buff=0.35)
        rules = VGroup(*[label(t, font_size=30, color=c) for t, c in (
            (r"take every machine with $n$ states and the symbols $0, 1$", GREY_A),
            (r"start each one on a blank tape", GREY_A),
            (r"ignore the ones that never halt", NO),
            (r"$S(n)$: \ the most steps any of the others takes", COST),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 0.3 + RIGHT * 0.6)
        fin = label(r"finitely many machines, \ so $S(n)$ is a definite number", font_size=28,
                    color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here is a problem that looks innocent. In 1962 Tibor Radó proposed a game. <bookmark mark='a'/> Take every "
            "Turing machine with n states and two symbols. Start each one on a blank tape. Throw away the ones that "
            "never halt. Among the rest, find the one that runs longest before it stops: call its number of steps S of "
            "n. <bookmark mark='b'/> There are only finitely many machines with n states, so S of n is a perfectly "
            "definite number. The machines that achieve it are called busy beavers."
        ) as vo:
            self.play(FadeIn(hc, shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rules], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(fin))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def two_states(self):
        d = load("beavers2")
        hist = d["hist"]
        head = label(rf"Every two-state machine: \ ${fmt(d['total'])}$ of them", font_size=38).to_edge(UP, buff=0.35)
        mx = max(hist)
        bars = VGroup()
        for s in range(1, 7):
            h = max(hist[s] / mx * 3.6, 0.03)
            b = Rectangle(width=0.8, height=h, stroke_width=0, fill_color=COST, fill_opacity=0.85)
            b.move_to([-5.4 + (s - 1) * 1.1, -2.2 + h / 2, 0])
            n = label(rf"${fmt(hist[s])}$", font_size=22).next_to(b, UP, buff=0.08)
            x = label(rf"${s}$", font_size=24, color=GREY_B).next_to(b, DOWN, buff=0.12)
            bars.add(VGroup(b, n, x))
        xl = label(r"steps before halting", font_size=24, color=GREY_A).next_to(bars, DOWN, buff=0.55)
        sm = label(rf"${fmt(d['halting'])}$ halt; \ the longest takes {d['max_steps']} steps: \ $S(2) = {d['max_steps']}$",
                   font_size=28, color=YES).move_to(RIGHT * 3.2 + UP * 2.2)
        sm.set_x(min(sm.get_x(), 6.9 - sm.width / 2))
        note_ = label(r"the rest never halt: \ any two-state machine still running \\ after 6 steps runs forever "
                      r"(Rad\'o)", font_size=22, color=GREY_B).next_to(sm, DOWN, buff=0.25)
        m = TM.parse(CHAMPIONS[2][0])
        r = run(m, max_steps=100, record=True)
        lo = -3
        hist_t = []
        for st, hs, tps, _ in r.history:
            hist_t.append({"state": st, "heads": list(hs), "tapes": ["".join(tps[0].get(k, "_") for k in range(lo, 3))]})
        view = TapeView(list(hist_t[0]["tapes"][0]), head=hist_t[0]["heads"][0] - lo, state="A", cell=0.6,
                        font_size=28).move_to(RIGHT * 3.2 + DOWN * 1.2)
        cnt = step_counter().next_to(view, DOWN, buff=0.35)
        with self.voiceover(
            "For two states we can simply try them all. There are twenty thousand, seven hundred and thirty-six. "
            "<bookmark mark='a'/> Run every one from a blank tape. Here are the ones that halt, by how many steps they "
            "take. <bookmark mark='b'/> Nine thousand seven hundred and eighty-four halt. The longest takes six steps, "
            "so S of two is six. Radó checked by hand that every machine still running after six steps runs forever. "
            "<bookmark mark='c'/> Here is the champion, the machine from earlier, writing four ones in six steps."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bars], lag_ratio=0.15),
                      LaggedStart(*[FadeIn(VGroup(b[1], b[2])) for b in bars], lag_ratio=0.15), FadeIn(xl),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(sm), FadeIn(note_), Indicate(bars[-1], color=YES))
            vo.wait_until("c")
            self.play(FadeIn(view), FadeIn(cnt))
            for i in range(len(hist_t) - 1):
                a, b = hist_t[i], hist_t[i + 1]
                new = b["tapes"][0][a["heads"][0] - lo]
                self.play(view.step(new, b["heads"][0] - a["heads"][0], b["state"], run_time=0.7),
                          cnt.tracker.animate(run_time=0.7).set_value(i + 1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def champions(self):
        b = load("beavers")
        i3, i4 = b["info3"], b["info4"]
        im3 = spacetime_mob(np.asarray(b["st3"]), width=1.6, height=3.6)
        im4 = spacetime_mob(np.asarray(b["st4"]), width=3.2, height=5.4)
        g = Group(im3, im4).arrange(RIGHT, buff=1.4, aligned_edge=UP).move_to(DOWN * 0.35 + LEFT * 1.6)
        f3 = SurroundingRectangle(im3, buff=0, color=GREY_C, stroke_width=1)
        f4 = SurroundingRectangle(im4, buff=0, color=GREY_C, stroke_width=1)
        l3 = label(rf"3 states: \ {i3['steps']} steps \\ {i3['who']}, {i3['year']}", font_size=24).next_to(im3, UP,
                                                                                                         buff=0.2)
        l4 = label(rf"4 states: \ {i4['steps']} steps \\ {i4['who']}, {i4['year']}", font_size=24).next_to(im4, UP,
                                                                                                         buff=0.2)
        tbl = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"$S(1) = 1$", GREY_A), (r"$S(2) = 6$", GREY_A), (rf"$S(3) = {i3['steps']}$", GREY_A),
            (rf"$S(4) = {i4['steps']}$", GREY_A), (r"$S(5) = \ ?$", COST))]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        tbl.move_to(RIGHT * 4.9 + DOWN * 0.2)
        with self.voiceover(
            "With more states, the champions get stranger. <bookmark mark='a'/> For three states the record is twenty-one "
            "steps, proved by Shen Lin and Radó in 1965. <bookmark mark='b'/> For four, a hundred and seven steps, found by "
            "Allen Brady in 1983, who also proved nothing does better. <bookmark mark='c'/> One, six, twenty-one, one "
            "hundred and seven. And for five states, for decades, nobody knew."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(im3), Create(f3), FadeIn(l3))
            vo.wait_until("b")
            self.play(FadeIn(im4), Create(f4), FadeIn(l4))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(t) for t in tbl], lag_ratio=0.25))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def five(self):
        b = load("beavers")
        info = b["info5"]
        rgb = density_rgb(np.asarray(b["st5"]))
        img = bitmap(rgb, width=8.2, height=5.4, smooth=True).move_to(LEFT * 2.2 + DOWN * 0.5)
        frame_ = SurroundingRectangle(img, buff=0, color=GREY_C, stroke_width=1)
        tl = label(rf"5 states: \ all ${fmt(info['steps'])}$ steps, \ run on this computer", font_size=26).next_to(
            img, UP, buff=0.2)
        ax_t = label(r"time $\downarrow$", font_size=22, color=GREY_B).next_to(img, LEFT, buff=0.12)
        ax_x = label(rf"{fmt(info['cells'])} tape cells", font_size=22, color=GREY_B).next_to(img, DOWN, buff=0.12)
        hc = history_card(1990, r"Heiner Marxen and J\"urgen Buntrock", r"find this machine. \ It halts with "
                          rf"{fmt(info['ones'])} ones.", width=4.6, font_size=22).move_to(RIGHT * 4.6 + UP * 1.8)
        proof = history_card(2024, r"the bbchallenge collaboration", r"proves that no five-state machine that halts "
                             r"runs longer: \ $S(5) = 47{,}176{,}870$. \ The proof is checked by the Coq proof "
                             r"assistant.", width=4.6, font_size=22).next_to(hc, DOWN, buff=0.3)
        early = np.asarray(b["early5"])
        eh = np.asarray(b["early_heads5"])
        arr = early.astype(np.int8)
        st = np.where(arr > 0, 1, 0).astype(np.int8)
        for t in range(len(st)):
            if 0 <= eh[t] < st.shape[1]:
                st[t, eh[t]] = 3
        zoom = spacetime_mob(st[:1200], width=3.4, height=5.4).move_to(RIGHT * 4.6 + DOWN * 0.5)
        zf = SurroundingRectangle(zoom, buff=0, color=HEAD, stroke_width=1.5)
        zl = label(r"the first 1{,}200 steps, \ cell by cell", font_size=22, color=HEAD).next_to(zoom, UP, buff=0.15)
        # the champion's table, in the usual notation: write, move, next state
        code5 = CHAMPIONS[5][0].split("_")
        cells = [[MathTex(r"\text{state}", font_size=30, color=GREY_B), MathTex(r"\text{read } 0", font_size=30, color=GREY_B),
                  MathTex(r"\text{read } 1", font_size=30, color=GREY_B)]]
        for st, row in zip("ABCDE", code5):
            ents = [row[:3], row[3:]]
            cells.append([MathTex(st, font_size=36, color=CTRL)] + [
                MathTex(r"\text{halt}" if e[2] == "Z" else rf"\mathrm{{{e[0]}\,{e[1]}\,{e[2]}}}", font_size=36,
                        color=LIMIT if e[2] == "Z" else GREY_A) for e in ents])
        tab5 = VGroup(*[VGroup(*r) for r in cells])
        for i, r in enumerate(tab5):
            for j, c in enumerate(r):
                c.move_to([j * 2.0, -i * 0.68, 0])
        tab5.move_to(LEFT * 2.2 + DOWN * 0.3)
        rule_ = Line(tab5[0].get_corner(DL) + DOWN * 0.15 + LEFT * 0.3, tab5[0].get_corner(DR) + DOWN * 0.15 + RIGHT * 0.3,
                     color=GREY_D, stroke_width=1.5)
        tkey = label(r"each entry: \ symbol to write, \ move, \ next state", font_size=22, color=GREY_B)
        tkey.next_to(tab5, DOWN, buff=0.4)
        ctr = VGroup(label(r"steps run:", font_size=28, color=GREY_A), live_int(0, 34, COST)).arrange(RIGHT, buff=0.25)
        ctr.next_to(tab5, UP, buff=0.5)
        ctr[1].add_updater(lambda m: m.next_to(ctr[0], RIGHT, buff=0.25))
        with self.voiceover(
            "In 1990 Heiner Marxen and Jürgen Buntrock found a five-state machine: this table, ten entries. Started on "
            "a blank tape, it halts after forty-seven million, "
            "one hundred and seventy-six thousand, eight hundred and seventy steps. <bookmark mark='r'/> We ran it here, "
            "in compiled code, for every one of those steps. <bookmark mark='a'/> This is its whole run, squeezed into one picture: time "
            f"runs down, each row is about {say(info['every'])} steps, and the tape spans {say(info['cells'])} cells. "
            "<bookmark mark='b'/> In 2024 an online collaboration called bbchallenge proved that no halting five-state "
            "machine runs longer, so this is S of five. They had to show, for every one of the five-state machines, that "
            "it either halts within those forty-seven million steps or provably never halts, and the whole proof was "
            "checked by a computer proof assistant."
        ) as vo:
            self.play(FadeIn(hc, shift=LEFT * 0.2), FadeIn(tab5, lag_ratio=0.05), Create(rule_), FadeIn(tkey))
            vo.wait_until("r")
            self.play(FadeIn(ctr))
            self.play(ctr[1].tracker.animate.set_value(info["steps"]), run_time=3.0, rate_func=rate_functions.ease_in_quad)
            vo.wait_until("a")
            self.play(FadeOut(VGroup(tab5, rule_, tkey, ctr)), FadeIn(img), Create(frame_), FadeIn(tl), FadeIn(ax_t),
                      FadeIn(ax_x))
            vo.wait_until("b")
            self.play(FadeIn(proof, shift=UP * 0.2))
        with self.voiceover(
            "Zoom in on the first twelve hundred steps, cell by cell, and you can see the machine at work: a head "
            "sweeping back and forth across a growing block of ones, in a pattern that keeps almost repeating, and "
            "never quite does. That near-regularity, sustained for forty-seven million steps and then broken, is what "
            "made proving it so hard."
        ):
            self.play(FadeOut(hc), FadeOut(proof))
            self.play(FadeIn(zoom), Create(zf), FadeIn(zl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def uncomputable(self):
        thm = theorem_card(r"Rad\'o (1962)", r"No Turing machine computes $S(n)$.", width=8.0, font_size=30)
        thm.to_edge(UP, buff=0.4)
        steps = VGroup(*[label(t, font_size=28, color=c) for t, c in (
            (r"suppose some machine computes $S(n)$", GREY_A),
            (r"given any $n$-state machine $M$: \ compute $S(n)$", CTRL),
            (r"run $M$ on a blank tape for $S(n)$ steps", CTRL),
            (r"halted? \ then it halts. \ \ Still running? \ then it never halts", YES),
            (r"that decides the blank-tape halting problem: \ impossible (Chapter 12)", LIMIT),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 0.5)
        grow = label(r"in fact $S$ eventually outgrows every computable function", font_size=26,
                     color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Radó's real point was that S is not merely hard to compute. <bookmark mark='a'/> No machine can compute it. "
            "<bookmark mark='b'/> Suppose one could. Then take any machine M with n states. Compute S of n. Run M on a "
            "blank tape for S of n steps. If it has halted, it halts. If it is still running, it can never halt, because "
            "no halting n-state machine runs longer than S of n. <bookmark mark='c'/> That would decide the blank-tape "
            "halting problem, which the last chapter showed is impossible. <bookmark mark='d'/> In fact S grows faster "
            "than any function a computer can compute: faster than exponentials, towers of exponentials, anything."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm, shift=DOWN * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.15) for s in steps[:4]], lag_ratio=0.5), run_time=3.2)
            vo.wait_until("c")
            self.play(FadeIn(steps[4]))
            vo.wait_until("d")
            self.play(FadeIn(grow))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def frontier(self):
        head = label(r"Beyond five states", font_size=40).to_edge(UP, buff=0.4)
        items = VGroup(*[label(t, font_size=28, color=c) for t, c in (
            (r"6 states: \ a machine found in 2022 runs for more than $10\uparrow\uparrow 15$ steps, \\ a tower of "
             r"fifteen 10s; \ the record has grown since", WHITE),
            (r"some 6-state machines halt only if open problems like the Collatz \\ conjecture come out a particular way: "
             r"\ nobody can say whether they halt", GREY_A),
            (r"a machine with a few thousand states halts if and only if \\ the axioms of set theory are inconsistent: "
             r"\ its value can never be proved", LIMIT),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(DOWN * 0.2)
        src = note(r"Yedidia and Aaronson (2016), \ and later smaller machines; \ details in Part 25", font_size=22)
        src.to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Six states is already past the edge of the knowable. <bookmark mark='a'/> A six-state machine found in 2022 "
            "runs for more than ten tetrated to fifteen steps, a tower of fifteen tens, and the record has grown since. "
            "<bookmark mark='b'/> Some six-state machines behave like famous open problems, such as the Collatz "
            "conjecture: whether they halt depends on questions nobody can answer. <bookmark mark='c'/> And Adam Yedidia "
            "and Scott Aaronson built a machine with a few thousand states that halts only if the standard axioms of "
            "mathematics are inconsistent. Its busy-beaver value can never be proved from those axioms. Hilbert's "
            "mechanical certainty runs out, here, at a machine you could write on a few pages."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abc", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.15))
            self.play(FadeIn(src))
        self.wait(0.3)
        self.clear_scene()
