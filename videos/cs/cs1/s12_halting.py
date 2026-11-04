from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs1.common import ADV, CODE, COST, CTRL, DATA, HEAD, HIST, LIMIT, NO, PART, YES, fmt, load


def entry(v, w=0.95, h=0.5, font_size=22, color=None):
    sq = Rectangle(width=w, height=h, stroke_width=1, stroke_color=GREY_D, fill_color=BACKGROUND, fill_opacity=1)
    if v is None:
        t = MathTex(r"?", font_size=font_size + 6, color=color or NO)
    else:
        t = MathTex(str(v), font_size=font_size, color=color or YES)
    return VGroup(sq, t.move_to(sq))


class Halting(VoiceoverScene):
    def construct(self):
        self.card()
        self.question()
        self.table()
        self.proof()
        self.diagonal()
        self.hilbert()

    def card(self):
        card = chapter_card(11, r"The halting problem", r"Can a program tell whether another program will finish?",
                            lit=(1936,), part=PART)
        with self.voiceover("Chapter eleven. The halting problem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def question(self):
        box = RoundedRectangle(width=3.6, height=1.6, corner_radius=0.2, stroke_color=CTRL, stroke_width=3,
                               fill_color=CTRL, fill_opacity=0.08).move_to(RIGHT * 0.6 + UP * 0.7)
        h = label(r"$H$", font_size=60, color=CTRL).move_to(box)
        ins = VGroup(label(r"a program $\langle M \rangle$", font_size=28, color=CODE),
                     label(r"an input $w$", font_size=28, color=DATA)).arrange(DOWN, buff=0.4).next_to(box, LEFT, buff=1.0)
        outs = VGroup(label(r"halts", font_size=30, color=YES), label(r"runs forever", font_size=30, color=NO)).arrange(
            DOWN, buff=0.5).next_to(box, RIGHT, buff=1.0)
        arr = VGroup(*[Arrow(i.get_right(), box.get_left(), buff=0.12, color=GREY_C) for i in ins],
                     *[Arrow(box.get_right(), o.get_left(), buff=0.12, color=GREY_C) for o in outs])
        defn = definition_card(r"The halting problem", r"$\mathrm{HALT} = \{\, \langle M, w \rangle : \ M \text{ halts on "
                               r"input } w \,\}$. \ A \textit{decider} for it would always stop, \ with the right answer.",
                               color=CTRL, width=10.0, font_size=26).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Every programmer has wanted this tool. You give it a program and an input, and it tells you whether the "
            "program will eventually finish, or hang forever. <bookmark mark='a'/> Call it H. It must always stop "
            "itself, and always be right. <bookmark mark='b'/> The set of program-input pairs where the program halts "
            "is called HALT, and H would be a decider for it."
        ) as vo:
            self.play(FadeIn(ins), FadeIn(box), FadeIn(h), FadeIn(outs), *[GrowArrow(a) for a in arr])
            vo.wait_until("a")
            self.play(Indicate(h, color=CTRL))
            vo.wait_until("b")
            self.play(FadeIn(defn, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        d = load("diagonal")
        rows = d["rows"]
        nI = len(d["inputs"])
        head = label(r"Why not just run it?", font_size=38).to_edge(UP, buff=0.35)
        colh = VGroup(*[MathTex(r"\varepsilon" if not s else rf"1^{{{len(s)}}}" if len(s) > 1 else "1", font_size=24,
                                color=DATA) for s in d["inputs"]])
        grid = VGroup()
        for r in rows:
            grid.add(VGroup(*[entry(v) for v in r["results"]]).arrange(RIGHT, buff=0))
        grid.arrange(DOWN, buff=0).scale(0.92).move_to(DOWN * 0.3 + RIGHT * 2.75)
        for t, c in zip(colh, grid[0]):
            t.next_to(c, UP, buff=0.15)
        rowh = VGroup(*[MathTex(rf"M_{{{r['index'] + 1}}}", font_size=24, color=CODE).next_to(g, LEFT, buff=0.25)
                        for r, g in zip(rows, grid)])
        cap = label(rf"two-state machines from our list, \ inputs $1^j$, \ each run for {fmt(d['limit'])} steps",
                    font_size=24, color=GREY_A).next_to(grid, DOWN, buff=0.3)
        key = VGroup(label(r"number: \ halted after that many steps", font_size=24, color=YES),
                     label(r"?: \ still running", font_size=24, color=NO)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        key.to_corner(UL, buff=0.4).shift(DOWN * 0.7)
        rec = definition_card(r"recognizable, \ not decidable", r"running a program finds every ``halts'' answer "
                              r"eventually; \ it never finds ``runs forever''.", color=HEAD, width=4.6, font_size=22,
                              kind=r"so far")
        rec.to_edge(LEFT, buff=0.35).shift(DOWN * 1.0)
        with self.voiceover(
            "Why not just run the program and see? Here are some real two-state machines from our list, each run on "
            "short inputs for ten thousand steps. <bookmark mark='a'/> A number means the machine halted after that "
            "many steps. A question mark means it was still running when we stopped. <bookmark mark='b'/> Running "
            "settles every halts answer, eventually. But a question mark is ambiguous: it might mean runs forever, or "
            "it might mean halts at step ten thousand and one. No finite amount of running can tell those apart. "
            "<bookmark mark='c'/> Running gives a recognizer for HALT, not a decider. Could something cleverer than "
            "running always work?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(colh), FadeIn(rowh), FadeIn(grid, lag_ratio=0.02), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(key))
            vo.wait_until("b")
            qs = [c for g in grid for c in g if c[1].tex_string == "?"]
            self.play(*[Indicate(q, color=NO) for q in qs])
            vo.wait_until("c")
            self.play(FadeIn(rec, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def proof(self):
        head = label(r"Suppose $H$ exists. \ Build $D$:", font_size=38).to_edge(UP, buff=0.35)
        code = code_block([
            "def D(p):",
            "    if H(p, p):          # does p halt, given itself?",
            "        while True:      # then loop forever",
            "            pass",
            "    else:",
            "        return           # otherwise halt",
        ], font_size=26, color=GREY_A).move_to(UP * 0.9)
        for i in (1, 2):
            code[i].set_color(ADV if i == 2 else CTRL)
        q = cmath(r"D(\langle D \rangle)", r"\ ?", font_size=48, colors={r"D(\langle D \rangle)": ADV})
        q.next_to(code, DOWN, buff=0.55)
        c1 = label(r"if $D(\langle D\rangle)$ halts, \ then $H$ said ``halts'', \ so $D$ loops forever", font_size=28,
                   color=NO)
        c2 = label(r"if $D(\langle D\rangle)$ loops, \ then $H$ said ``loops'', \ so $D$ halts", font_size=28, color=NO)
        cs = VGroup(c1, c2).arrange(DOWN, buff=0.25).next_to(q, DOWN, buff=0.4)
        boom = label(r"either way, \ a contradiction: \ $H$ cannot exist", font_size=32, color=LIMIT)
        boom.to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Turing's proof takes a few lines. Suppose H exists. Use it to build a new program, D. <bookmark mark='a'/> "
            "D takes a program p, and asks H: would p halt if it were given its own description as input? "
            "<bookmark mark='b'/> If H says yes, D deliberately loops forever. If H says no, D halts. D does the "
            "opposite of whatever H predicts. <bookmark mark='c'/> Now feed D its own description. Does D halt on D? "
            "<bookmark mark='d'/> If it halts, then H must have said it halts, so D loops forever. If it loops forever, "
            "H must have said it loops, so D halts. <bookmark mark='e'/> Both answers contradict themselves. The only "
            "way out is that H, the perfect halting checker, cannot exist."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(code[0]), FadeIn(code[1]))
            vo.wait_until("b")
            self.play(FadeIn(code[2:]))
            vo.wait_until("c")
            self.play(Write(q))
            vo.wait_until("d")
            self.play(FadeIn(c1))
            self.play(FadeIn(c2))
            vo.wait_until("e")
            self.play(FadeIn(boom, scale=1.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def diagonal(self):
        K = 7
        rng = np.random.default_rng(12)
        T = rng.integers(0, 2, (K, K))
        cell = 0.62
        grid = VGroup()
        for i in range(K):
            r = VGroup()
            for j in range(K):
                v = int(T[i, j])
                sq = Square(cell, stroke_width=1, stroke_color=GREY_D, fill_color=BACKGROUND, fill_opacity=1)
                t = label(r"H" if v else r"L", font_size=24, color=YES if v else NO).move_to(sq)
                r.add(VGroup(sq, t))
            grid.add(r.arrange(RIGHT, buff=0))
        grid.arrange(DOWN, buff=0).move_to(UP * 0.35 + RIGHT * 0.8)
        colh = VGroup(*[MathTex(rf"\langle M_{{{j + 1}}} \rangle", font_size=22, color=CODE).next_to(grid[0][j], UP,
                                                                                                    buff=0.15)
                        for j in range(K)])
        rowh = VGroup(*[MathTex(rf"M_{{{i + 1}}}", font_size=24, color=CODE).next_to(grid[i], LEFT, buff=0.25)
                        for i in range(K)])
        key = label(r"H: halts \quad L: loops forever", font_size=22, color=GREY_A).next_to(grid, RIGHT, buff=0.4)
        key.align_to(grid, UP)
        tag = note(r"schematic", font_size=22).to_corner(UR, buff=0.3)
        diag = VGroup(*[SurroundingRectangle(grid[i][i], color=HEAD, buff=0, stroke_width=3) for i in range(K)])
        drow = VGroup()
        for i in range(K):
            v = 1 - int(T[i, i])
            sq = Square(cell, stroke_width=1, stroke_color=ADV, fill_color=BACKGROUND, fill_opacity=1)
            drow.add(VGroup(sq, label(r"H" if v else r"L", font_size=24, color=ADV).move_to(sq)))
        drow.arrange(RIGHT, buff=0).next_to(grid, DOWN, buff=0.45).align_to(grid, LEFT)
        dl = MathTex(r"D", font_size=30, color=ADV).next_to(drow, LEFT, buff=0.25)
        concl = label(r"$D$ differs from every $M_i$ on input $\langle M_i \rangle$: \ $D$ is not in the list. \\ But the "
                      r"list has every machine. \ So $H$, \ from which we built $D$, \ does not exist.", font_size=26,
                      color=ADV).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "It is Cantor's diagonal again. <bookmark mark='a'/> Make a table: the rows are all machines, M one, M two, "
            "and so on; the columns are their descriptions; each entry says whether that machine halts on that "
            "description. <bookmark mark='b'/> The diagonal is each machine run on its own description. "
            "<bookmark mark='c'/> D is built to do the opposite of the diagonal: where M i halts on its own description, "
            "D loops, and where M i loops, D halts. <bookmark mark='d'/> So D's row differs from every row in the table, "
            "in the diagonal place. D is not on the list. But the list contains every machine, and D would be a machine "
            "if H existed. So H does not exist."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(grid, lag_ratio=0.01), FadeIn(colh), FadeIn(rowh), FadeIn(key))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(b) for b in diag], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(FadeIn(dl), LaggedStart(*[TransformFromCopy(grid[i][i], drow[i]) for i in range(K)],
                                              lag_ratio=0.15), run_time=2.2)
            vo.wait_until("d")
            self.play(FadeIn(concl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hilbert(self):
        chain = VGroup(
            node_box(r"a machine $M$", CODE, font_size=28),
            node_box(r"a formula $\varphi_M$ of logic", DATA, font_size=28),
            node_box(r"$\varphi_M$ is provable \\ $\iff$ \ $M$ halts", YES, font_size=28),
        ).arrange(RIGHT, buff=0.9).move_to(UP * 1.2)
        arr = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.12, color=GREY_B) for a, b in zip(chain, chain[1:])])
        tl = label(r"Turing (1936): \ write down, for each machine, a formula that says it halts", font_size=26,
                   color=GREY_A).next_to(chain, UP, buff=0.4)
        concl = VGroup(label(r"a decider for logic \ $\Longrightarrow$ \ a decider for halting", font_size=32),
                       label(r"no decider for halting \ $\Longrightarrow$ \ no decider for logic", font_size=32,
                             color=LIMIT)).arrange(DOWN, buff=0.3).move_to(DOWN * 1.0)
        ans = label(r"The \textit{Entscheidungsproblem}: \ \textbf{no}", font_size=40, color=LIMIT).to_edge(DOWN,
                                                                                                         buff=0.4)
        with self.voiceover(
            "And this answers Hilbert. <bookmark mark='a'/> Turing showed how to write down, for any machine, a formula "
            "of logic that is provable exactly when the machine halts. <bookmark mark='b'/> So a procedure that decided "
            "provability in logic would also decide halting. Halting cannot be decided, so neither can logic. "
            "<bookmark mark='c'/> The decision problem has no solution. Church reached the same answer with the lambda "
            "calculus, weeks earlier. No mechanical procedure can settle every mathematical question. The dream of "
            "Leibniz and Hilbert ends here, and the theory of computation begins."
        ) as vo:
            self.play(FadeIn(chain[0]))
            vo.wait_until("a")
            self.play(FadeIn(tl), GrowArrow(arr[0]), FadeIn(chain[1]), GrowArrow(arr[1]), FadeIn(chain[2]))
            vo.wait_until("b")
            self.play(FadeIn(concl[0]))
            self.play(FadeIn(concl[1]))
            vo.wait_until("c")
            self.play(FadeIn(ans, scale=1.1))
        self.wait(0.3)
        self.clear_scene()
