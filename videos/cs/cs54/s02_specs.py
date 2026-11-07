from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs54.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load, mono


def wrap(v: int, w: int = 16) -> int:
    """v as a signed w-bit integer (two's complement wrap-around)."""
    v &= (1 << w) - 1
    return v - (1 << w) if v >= 1 << (w - 1) else v


def num(v: int) -> str:
    """An integer for Tex, with thousands separators and a true minus sign."""
    return "$" + f"{v:,}".replace(",", "{,}") + "$"


def elbow(points, color=GREY_B):
    """A path of straight segments ending in an arrowhead (a flow diagram's back edge)."""
    segs = VGroup(*[Line(points[i], points[i + 1], color=color, stroke_width=2) for i in range(len(points) - 2)])
    last = float(np.linalg.norm(np.array(points[-1]) - np.array(points[-2])))
    segs.add(Arrow(points[-2], points[-1], buff=0, color=color, stroke_width=2,
                   max_tip_length_to_length_ratio=min(0.6, 0.15 / last), max_stroke_width_to_length_ratio=20))
    return segs


def listing_lines(rows) -> list[str]:
    return ["    " * r["depth"] + r["code"] for r in rows]


class Specs(VoiceoverScene):
    def construct(self):
        self.card()
        self.contract()
        self.weak()
        self.ghost()
        self.turing()
        self.columns()
        self.lineage()

    def card(self):
        card = chapter_card(1, r"Specifications, \ and the first program proof",
                            r"What does it mean for a program to be right?", lit=(1949, 1984),
                            extra=((1949, r"Turing: \ Checking a Large Routine"),
                                   (1984, r"Morris and Jones revive it")), part=PART)
        with self.voiceover("Chapter one. Specifications, and the first program proof."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def contract(self):
        mx = load("hoare")["programs"]["max"]
        head = label(r"A specification is a contract", font_size=36).to_edge(UP, buff=0.3)
        triple = MathTex(r"\{\,\mathit{true}\,\}", r"\quad m := \max(a, b) \quad",
                         r"\{\, m \ge a \,\wedge\, m \ge b \,\wedge\, (m = a \,\vee\, m = b) \,\}", font_size=38)
        triple[0].set_color(DATA)
        triple[1].set_color(GREY_A)
        triple[2].set_color(YES)
        triple.next_to(head, DOWN, buff=0.55)
        b_pre = Brace(triple[0], DOWN, color=DATA)
        t_pre = label(r"precondition", font_size=19, color=DATA).next_to(b_pre, DOWN, buff=0.1)
        b_post = Brace(triple[2], DOWN, color=YES)
        t_post = label(r"postcondition", font_size=19, color=YES).next_to(b_post, DOWN, buff=0.1)
        code = code_block(listing_lines(mx["listing"]), size=24)
        frame = SurroundingRectangle(code, buff=0.3, color=GREY_C, stroke_width=1.5, corner_radius=0.1)
        ctitle = label(r"the code", font_size=19, color=GREY_A).next_to(frame, UP, buff=0.12).align_to(frame, LEFT)
        left = VGroup(ctitle, frame, code).move_to([-3.9, -1.2, 0])
        notes = VGroup(
            wrapped_label(r"the \textbf{precondition} is what the caller promises before the call: \ here nothing "
                          r"at all, \ so it is \textit{true}", 6.0, font_size=20, color=DATA),
            wrapped_label(r"the \textbf{postcondition} is what the code promises in return: \ at least $a$, \ at "
                          r"least $b$, \ and equal to one of them", 6.0, font_size=20, color=YES),
            wrapped_label(r"the specification says \textit{what}; \ the code says \textit{how}; \ a proof shows "
                          r"that they agree on every input", 6.0, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.3, -1.3, 0])
        with self.voiceover(
            "A program is correct only relative to a specification of what it should do. <bookmark mark='a'/> The"
            " usual form is a pair of conditions. The precondition is what the caller promises: for this maximum "
            "function, nothing at all, so it is simply true. <bookmark mark='b'/> The postcondition is what the "
            "code promises in return: the result is at least a, at least b, and equal to one of them. <bookmark "
            "mark='c'/> The specification says what; the code says how. A proof shows that they agree on every "
            "input, not only on the inputs we happened to try."
        ) as vo:
            self.play(FadeIn(head), FadeIn(triple), FadeIn(left))
            vo.wait_until("a")
            self.play(GrowFromCenter(b_pre), FadeIn(t_pre), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(GrowFromCenter(b_post), FadeIn(t_post), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]), Indicate(code, color=HEAD, scale_factor=1.05))
        self.wait(0.4)
        self.clear_scene()

    def weak(self):
        head = label(r"A specification can be too weak", font_size=36).to_edge(UP, buff=0.3)
        rows = [["m = a", "no", "no"], ["m = 32767", "yes", "no"], ["m = a if a >= b else b", "yes", "yes"]]
        colors = [[WHITE, YES if r[1] == "yes" else NO, YES if r[2] == "yes" else NO] for r in rows]
        tab = grid_table([r"program", r"$m \ge a \wedge m \ge b$", r"all three clauses"], rows,
                         widths=[4.8, 3.2, 3.2], row_h=0.62, font_size=22, colors=colors, mono_cols=(0,))
        tab.next_to(head, DOWN, buff=0.5)
        why = wrapped_label(r"$32{,}767$ is the largest 16-bit integer, \ so it is at least $a$ and at least $b$ "
                            r"for every input: \ it meets the weakened specification and is useless", 11.6,
                            font_size=20, color=HEAD).next_to(tab, DOWN, buff=0.35)
        sort_code = mono("def sort(xs): return []", size=22, color=NO)
        sort_a = label(r"meets ``the output is sorted''", font_size=20, color=YES)
        sort_b = label(r"fails ``the output is a permutation of the input''", font_size=20, color=NO)
        sort_g = VGroup(sort_code, VGroup(sort_a, sort_b).arrange(DOWN, aligned_edge=LEFT, buff=0.12)).arrange(
            RIGHT, buff=0.6).next_to(why, DOWN, buff=0.5)
        ill = note(r"illustrative", font_size=16).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Writing the specification is half the work, and it is easy to get wrong. <bookmark mark='a'/> Drop "
            "the last clause of our postcondition. Returning a alone still fails. <bookmark mark='b'/> But "
            "returning thirty-two thousand seven hundred and sixty-seven, the largest sixteen-bit integer, is at "
            "least a and at least b for every input: it meets the weakened specification, and it is useless. "
            "<bookmark mark='c'/> The classic case is sorting. Ask only that the output be sorted, and returning "
            "the empty list is correct. The output must also be a permutation of the input."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0], tab.rule)), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[1])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[2])), FadeIn(why))
            self.play(FadeIn(VGroup(*tab.cells[3])))
            vo.wait_until("c")
            self.play(FadeIn(sort_g, shift=UP * 0.1))
        self.wait(0.4)
        self.clear_scene()

    def ghost(self):
        sw = load("hoare")["programs"]["swap"]
        head = label(r"Ghost variables name the past", font_size=36).to_edge(UP, buff=0.3)
        triple = MathTex(r"\{\, x = X \,\wedge\, y = Y \,\}", r"\quad \mathit{swap} \quad",
                         r"\{\, x = Y \,\wedge\, y = X \,\}", font_size=40)
        triple[0].set_color(DATA)
        triple[2].set_color(YES)
        triple.next_to(head, DOWN, buff=0.45)
        lines = listing_lines(sw["listing"])
        code = code_block(lines, size=26, buff=0.3).move_to([-4.0, -0.3, 0])
        X0, Y0 = 30000, 20000                     # illustrative values whose sum overflows 16 bits
        states = [(X0, Y0)]
        x, y = X0, Y0
        x = wrap(x + y)
        states.append((x, y))
        y = wrap(x - y)
        states.append((x, y))
        x = wrap(x - y)
        states.append((x, y))

        def reg(name, v, col):
            box = Rectangle(width=2.4, height=0.8, stroke_color=col, stroke_width=2, fill_color=BG, fill_opacity=1)
            t = label(num(v), font_size=30, color=WHITE).move_to(box)
            n = mono(name, size=24, color=col).next_to(box, LEFT, buff=0.2)
            return VGroup(box, t, n)
        rx = reg("x", X0, DATA).move_to([0.5, 0.35, 0])
        ry = reg("y", Y0, LAM).next_to(rx, DOWN, buff=0.35).align_to(rx, RIGHT)
        ghosts = label(rf"ghosts: \ $X = {X0:,}$, \ $Y = {Y0:,}$".replace(",", "{,}"), font_size=20,
                       color=GREY_A).next_to(rx, UP, buff=0.35).align_to(rx, LEFT)
        side = VGroup(
            label(r"true sum $50{,}000$ wraps past $32{,}767$", font_size=19, color=NO),
            label(r"the wrap undoes itself: \ $y$ holds the old $x$", font_size=19, color=YES),
            label(r"$x$ holds the old $y$", font_size=19, color=YES),
        )
        for s in side:
            s.next_to(VGroup(rx, ry), RIGHT, buff=0.35)
        side.set_x(5.0).shift(LEFT * max(0, side.get_right()[0] - 6.8))
        foot = VGroup(
            wrapped_label(r"$X$ and $Y$ are \textbf{ghost variables}: \ names for the starting values, \ never read "
                          r"or written by the program; \ they live only in the specification", 12.2, font_size=20,
                          color=WHITE),
            wrapped_label(r"16-bit arithmetic, \ illustrative values; \ Chapter 4's SAT solver proves the swap for "
                          r"every pair", 12.2, font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35)
        marker = SurroundingRectangle(code[0], color=HEAD, buff=0.1, stroke_width=2)
        with self.voiceover(
            "Some specifications must talk about the past. <bookmark mark='a'/> To say that this code swaps x and"
            " y, the postcondition needs their starting values. We name them capital X and capital Y: ghost "
            "variables, never read or written by the program, living only in the specification. <bookmark "
            "mark='b'/> Run the three lines on sixteen-bit integers. The first adds, and the sum overflows and "
            "wraps round to a negative number. <bookmark mark='c'/> The second subtracts, and the wrap undoes "
            "itself: y now holds the old x. <bookmark mark='d'/> The third gives x the old y. In Chapter four our"
            " SAT solver proves this for every pair of values."
        ) as vo:
            self.play(FadeIn(head), FadeIn(triple), FadeIn(code), FadeIn(rx), FadeIn(ry))
            vo.wait_until("a")
            self.play(FadeIn(ghosts), FadeIn(foot[0]))
            shown = None
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                nx, ny = states[k + 1]
                tx_ = label(num(nx), font_size=30, color=WHITE).move_to(rx[0])
                ty_ = label(num(ny), font_size=30, color=WHITE).move_to(ry[0])
                anims = [Transform(rx[1], tx_), Transform(ry[1], ty_)]
                if k == 0:
                    anims.append(Create(marker))
                else:
                    anims.append(marker.animate.move_to(code[k]))
                if shown is not None:
                    anims.append(FadeOut(shown))
                self.play(*anims, FadeIn(side[k]))
                shown = side[k]
            self.play(FadeIn(foot[1]), Indicate(triple[2], color=YES, scale_factor=1.05))
        self.wait(0.4)
        self.clear_scene()

    def turing(self):
        head = label(r"Turing, \ 1949: \ assertions on a flow diagram", font_size=36).to_edge(UP, buff=0.3)
        cx = -2.6

        def box(text, y, col=GREY_B, w=2.9):
            r = RoundedRectangle(width=w, height=0.55, corner_radius=0.08, stroke_color=col, stroke_width=1.8,
                                 fill_color=BG, fill_opacity=1).move_to([cx, y, 0])
            return VGroup(r, mono(text, size=18, color=WHITE).move_to(r))

        def diamond(text, y):
            d = Polygon([cx - 1.25, y, 0], [cx, y + 0.38, 0], [cx + 1.25, y, 0], [cx, y - 0.38, 0], color=HEAD,
                        stroke_width=1.8, fill_color=BG, fill_opacity=1)
            return VGroup(d, mono(text, size=17, color=HEAD).move_to(d))
        b1 = box("r = 1;  u = 1", 2.35)
        d1 = diamond("r = n ?", 1.35)
        b2 = box("v = u;  s = 1", 0.35)
        b3 = box("u = u + v;  s = s + 1", -0.65, w=3.5)
        d2 = diamond("s = r + 1 ?", -1.65)
        b4 = box("r = r + 1", -2.65)
        stop = box("stop", 1.35, col=YES, w=1.2).set_x(cx + 2.4)
        arrows = VGroup(
            Arrow(b1.get_bottom(), d1.get_top(), buff=0.03, stroke_width=2, color=GREY_B,
                  max_tip_length_to_length_ratio=0.25),
            Arrow(d1.get_bottom(), b2.get_top(), buff=0.03, stroke_width=2, color=GREY_B,
                  max_tip_length_to_length_ratio=0.25),
            Arrow(b2.get_bottom(), b3.get_top(), buff=0.03, stroke_width=2, color=GREY_B,
                  max_tip_length_to_length_ratio=0.25),
            Arrow(b3.get_bottom(), d2.get_top(), buff=0.03, stroke_width=2, color=GREY_B,
                  max_tip_length_to_length_ratio=0.25),
            Arrow(d2.get_bottom(), b4.get_top(), buff=0.03, stroke_width=2, color=GREY_B,
                  max_tip_length_to_length_ratio=0.25),
            Arrow(d1[0].get_right(), stop.get_left(), buff=0.03, stroke_width=2, color=YES,
                  max_tip_length_to_length_ratio=0.2),
        )
        back_in = elbow([d2[0].get_right(), [cx + 2.0, -1.65, 0], [cx + 2.0, -0.65, 0], b3[0].get_right()])
        back_out = elbow([b4[0].get_left(), [cx - 2.0, -2.65, 0], [cx - 2.0, 1.35, 0], d1[0].get_left()])
        yes1 = label(r"yes", font_size=16, color=YES).next_to(arrows[5], UP, buff=0.05)
        no2 = label(r"no", font_size=16, color=GREY_B).next_to([cx + 2.0, -1.15, 0], RIGHT, buff=0.08)
        flow = VGroup(b1, d1, b2, b3, d2, b4, stop, arrows, back_in, back_out, yes1, no2)
        dots1 = VGroup(Dot([cx, 1.9, 0], radius=0.07, color=YES))
        a1 = label(r"$u = r!$", font_size=20, color=YES).next_to(dots1, LEFT, buff=0.2)
        a2 = label(r"$u = s \cdot r!,\ v = r!$", font_size=20, color=YES).next_to(b3, RIGHT, buff=0.15).shift(
            UP * 0.42)
        a3 = label(r"$u = n!$", font_size=20, color=YES).next_to(stop, RIGHT, buff=0.15)
        # an illustrative run, n = 5: (r, u) each time control reaches the test r = n
        n = 5
        r, u, visits = 1, 1, []
        while True:
            visits.append((r, u))
            if r == n:
                break
            v, s = u, 1
            while True:
                u, s = u + v, s + 1
                if s == r + 1:
                    break
            r += 1
        rows = [[f"{rr}", f"{uu}", r"yes" if uu == math.factorial(rr) else r"no"] for rr, uu in visits]
        tab = grid_table([r"$r$", r"$u$", r"$u = r!$"], rows, widths=[0.9, 1.1, 1.3], row_h=0.42, font_size=20,
                         colors=[[WHITE, WHITE, YES]] * len(rows), mono_cols=())
        tcap = label(rf"a run with $n = {n}$, \ at the test", font_size=18, color=GREY_A)
        side = VGroup(tcap, tab).arrange(DOWN, buff=0.2).move_to([4.6, 0.9, 0])
        foot = wrapped_label(r"our rendering of a routine in his spirit: \ $n!$ by repeated addition, \ on a machine "
                             r"with no multiplier \ (illustrative)", 4.4, font_size=18, color=GREY_A).next_to(
            side, DOWN, buff=0.4)
        with self.voiceover(
            "The idea of proving a program is as old as the stored-program computer. <bookmark mark='a'/> In June"
            " 1949, at a conference in Cambridge, Alan Turing gave a short talk called Checking a Large Routine. "
            "His example computed n factorial by repeated addition, one loop inside another, on a machine with no"
            " multiplier. Here is a routine in that spirit. <bookmark mark='b'/> Turing attached assertions to "
            "points of the flow diagram: whenever control passes here, u equals r factorial; inside the inner "
            "loop, u is s times r factorial. <bookmark mark='c'/> At the stop box the assertion is the "
            "specification itself. <bookmark mark='d'/> A run with n equal to five shows the assertion holding at"
            " every visit; the argument covers every n."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(flow), FadeIn(foot), FadeIn(tcap), FadeIn(VGroup(*tab.cells[0], tab.rule)),
                      run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(dots1), FadeIn(a1))
            self.play(FadeIn(a2))
            vo.wait_until("c")
            self.play(FadeIn(a3), Indicate(stop, color=YES))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(VGroup(*row)) for row in tab.cells[1:]], lag_ratio=0.4), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def columns(self):
        head = label(r"Checking an addition, \ column by column", font_size=36).to_edge(UP, buff=0.3)
        terms = [1374, 5926, 2085]                 # illustrative
        total = sum(terms)
        nd = len(str(total))
        cw, x_right, y_top, row = 0.6, -2.2, 1.4, 0.65

        def digits(nm, y, col):
            s = str(nm).rjust(nd)
            return VGroup(*[mono(ch, size=36, color=col).move_to([x_right - (nd - 1 - i) * cw, y, 0])
                            for i, ch in enumerate(s) if ch != " "])
        rows_ = VGroup(*[digits(t, y_top - k * row, WHITE) for k, t in enumerate(terms)])
        plus = mono("+", size=36, color=GREY_B).move_to([x_right - nd * cw, y_top - 2 * row, 0])
        bar = Line([x_right - (nd + 0.6) * cw, y_top - 2.55 * row, 0], [x_right + 0.5 * cw, y_top - 2.55 * row, 0],
                   color=GREY_B, stroke_width=2)
        res = digits(total, y_top - 3.2 * row, YES)
        carries, checks = [], []
        carry = 0
        for c in range(nd):                        # c = 0 is the units column
            ds = [(t // 10 ** c) % 10 for t in terms]
            ssum = sum(ds) + carry
            parts = " + ".join(str(d) for d in ds) + (f" + {carry}" if carry else "")
            checks.append(label(rf"${parts} = {ssum}$: \ write {ssum % 10}" +
                                (rf", \ carry {ssum // 10}" if ssum >= 10 and c < nd - 1 else ""),
                                font_size=22, color=HEAD))
            carry = ssum // 10
            if carry and c < nd - 1:
                carries.append(mono(str(carry), size=22, color=HEAD).move_to(
                    [x_right - (c + 1) * cw, y_top + 0.55, 0]))
            else:
                carries.append(None)
        for ch in checks:
            ch.move_to([-3.6, -1.6, 0])
        col_box = Rectangle(width=cw * 0.95, height=row * 3.2 + 0.9, stroke_color=HEAD, stroke_width=2).move_to(
            [x_right, y_top - 1.3 * row + 0.2, 0])
        notes = VGroup(
            wrapped_label(r"Turing's analogy: \ checking a long sum in one go is hard; \ given the carries, \ each "
                          r"column can be checked on its own", 5.6, font_size=20, color=WHITE),
            wrapped_label(r"each check is small and needs no other; \ together they cover the whole", 5.6,
                          font_size=20, color=YES),
            wrapped_label(r"assertions are a program's carries: \ the programmer writes them, \ and each step "
                          r"between two of them is checked alone \ (paraphrased)", 5.6, font_size=20, color=HEAD),
            wrapped_label(r"he also argued that the routine stops, \ by a quantity that falls at every step: \ "
                          r"Chapter 3's variant", 5.6, font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([3.7, -0.1, 0])
        ill = note(r"illustrative numbers", font_size=16).to_corner(DL, buff=0.3)
        with self.voiceover(
            "Why assertions? Turing explained with an analogy. <bookmark mark='a'/> Checking a long addition all "
            "at once is hard. But if the writer also supplies the carries, each column can be checked on its own:"
            " four plus six plus five is fifteen, write five, carry one; and so on. <bookmark mark='b'/> Each "
            "check is small and needs no other, yet together they cover the whole sum. <bookmark mark='c'/> "
            "Assertions are a program's carries: each step between two of them is checked on its own, and the "
            "correctness of the whole follows. <bookmark mark='d'/> Turing also argued that the routine stops, by"
            " a quantity that falls at every step: Chapter three's variant."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_), FadeIn(plus), Create(bar), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            shown = None
            for c in range(nd):
                x = x_right - c * cw
                anims = [col_box.animate.set_x(x)] if c else [Create(col_box.set_x(x))]
                if shown is not None:
                    anims.append(FadeOut(shown))
                self.play(*anims, FadeIn(checks[c]), run_time=0.7)
                outs = [FadeIn(res[nd - 1 - c])]
                if carries[c] is not None:
                    outs.append(FadeIn(carries[c], shift=DOWN * 0.1))
                self.play(*outs, run_time=0.6)
                shown = checks[c]
            vo.wait_until("b")
            self.play(FadeOut(col_box), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def lineage(self):
        head = label(r"From assertions to a logic", font_size=36).to_edge(UP, buff=0.3)

        def tile(year, who, body, col):
            frame = RoundedRectangle(width=3.9, height=3.0, corner_radius=0.15, stroke_color=col, stroke_width=2,
                                     fill_color=BG, fill_opacity=1)
            g = VGroup(label(year, font_size=26, color=col), label(who, font_size=20, color=WHITE),
                       wrapped_label(body, 3.5, font_size=18, color=GREY_A)).arrange(DOWN, buff=0.18)
            g.move_to(frame)
            return VGroup(frame, g)
        tiles = VGroup(
            tile(r"1949", r"Turing", r"assertions at points of a flow diagram; \ a decreasing quantity for "
                 r"termination", GREY_B),
            tile(r"1967", r"Floyd", r"assertions on the edges of flowcharts; \ a condition for each kind of box; \ "
                 r"well-founded sets for termination", DATA),
            tile(r"1969", r"Hoare", r"a logic for program text: \ triples, \ axioms and rules of inference", YES),
        ).arrange(RIGHT, buff=0.55).next_to(head, DOWN, buff=0.6)
        links = VGroup(*[Arrow(tiles[i].get_right(), tiles[i + 1].get_left(), buff=0.05, stroke_width=2.5,
                               color=GREY_B, max_tip_length_to_length_ratio=0.3) for i in range(2)])
        triple = MathTex(r"\{P\}", r"\ c\ ", r"\{Q\}", font_size=60).next_to(tiles, DOWN, buff=0.55)
        triple[0].set_color(DATA)
        triple[1].set_color(HEAD)
        triple[2].set_color(YES)
        foot = note(r"Turing's paper was largely overlooked until F.\ L.\ Morris and C.\ B.\ Jones wrote about it in "
                    r"1984", font_size=17).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Turing's paper was largely overlooked until Morris and Jones wrote about it in 1984. <bookmark "
            "mark='a'/> Meanwhile the idea returned. In 1967 Robert Floyd attached assertions to the edges of "
            "flowcharts, gave for each kind of box the condition that makes the step correct, and proved "
            "termination with well-founded sets. <bookmark mark='b'/> In 1969 Tony Hoare turned this into a logic"
            " of program text, with triples, axioms and rules of inference. <bookmark mark='c'/> That logic is "
            "the next chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tiles[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(GrowArrow(links[0]), FadeIn(tiles[1]))
            vo.wait_until("b")
            self.play(GrowArrow(links[1]), FadeIn(tiles[2]))
            vo.wait_until("c")
            self.play(Write(triple))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN,)
