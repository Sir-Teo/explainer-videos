from __future__ import annotations

from explainer.cs import *  # noqa: F403
from explainer.cs.trust.trojan import CLEAN_COMPILER, CLEAN_LOGIN
from videos.cs.cs55.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load, mono


def cbox(text, color, w=None, h=0.5, size=18, use_mono=False):
    """A labelled rounded box (Tex, or monospace with ``use_mono``)."""
    t = mono(text, size=size, color=WHITE) if use_mono else label(text, font_size=size, color=WHITE)
    w = w or t.width + 0.35
    r = RoundedRectangle(width=w, height=h, corner_radius=0.07, stroke_color=color, stroke_width=1.8,
                         fill_color=BG, fill_opacity=1)
    if t.width > w - 0.12:
        t.width = w - 0.12
    t.move_to(r)
    return VGroup(r, t)


def binary_box(name, stage, color, w=3.0):
    """A binary drawn as a box: its name, and its size and hash prefix from the instrument."""
    t = label(name, font_size=18, color=WHITE)
    h = mono(f"{stage['size']:,} B  {stage['sha256'][:8]}", size=16, color=color)
    g = VGroup(t, h).arrange(DOWN, buff=0.08)
    r = RoundedRectangle(width=max(w, g.width + 0.3), height=g.height + 0.25, corner_radius=0.08,
                         stroke_color=color, stroke_width=2, fill_color=BG, fill_opacity=1)
    g.move_to(r)
    return VGroup(r, g)


def panel(lines, title, color, size=16):
    code = code_block(lines, size=size)
    t = label(title, font_size=18, color=color)
    frame = SurroundingRectangle(code, buff=0.2, color=color, stroke_width=1.5, corner_radius=0.08)
    t.next_to(frame, UP, buff=0.1).align_to(frame, LEFT)
    return VGroup(frame, code, t)


def arrow(a, b, color=GREY_B, width=2.4):
    return Arrow(a, b, buff=0.08, stroke_width=width, color=color, max_tip_length_to_length_ratio=0.2,
                 max_stroke_width_to_length_ratio=10)


def yes_no(v):
    return (r"accepted", NO) if v else (r"refused", GREY_B)


class Trojan(VoiceoverScene):
    def construct(self):
        self.card()
        self.toy()
        self.login()
        self.compiler()
        self.quine()
        self.loop()
        self.moral()

    def card(self):
        card = chapter_card(11, r"Reflections on trusting trust", r"Can you trust a program you compiled yourself?",
                            lit=(1974, 1984), extra=((1974, r"Karger and Schell: \ Multics review"),
                                                     (1984, r"Thompson: \ Trusting Trust")),
                            part=PART, layers=("lang", "code"))
        with self.voiceover("Chapter eleven. Reflections on trusting trust."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def toy(self):
        st = load("trojan")["stages"]
        head = label(r"A compiler that can compile itself", font_size=36).to_edge(UP, buff=0.3)
        comp = panel(CLEAN_COMPILER.rstrip("\n").split("\n"), r"\texttt{compiler.py}", YES, size=16)
        log_ = panel(CLEAN_LOGIN.rstrip("\n").split("\n"), r"\texttt{login.py}", YES, size=16)
        comp.next_to(head, DOWN, buff=0.25).to_edge(LEFT, buff=0.35)
        log_.next_to(comp, DOWN, buff=0.2).align_to(comp, LEFT)
        slot = SurroundingRectangle(comp[1][3], color=HEAD, buff=0.04, stroke_width=1.5)
        sl = wrapped_label(r"an empty slot, \ marked to make the demonstration easy to read", 3.6, font_size=18,
                           color=HEAD)
        sl.next_to(comp, RIGHT, buff=0.4).align_to(comp[1][3], DOWN)
        y = -2.55
        b1 = binary_box(r"compiler binary", st[0], YES).move_to([-1.9, y, 0])
        s1 = cbox(r"\texttt{compiler.py}", GREY_B, w=2.3).move_to([-5.4, y, 0])
        s2 = cbox(r"\texttt{login.py}", GREY_B, w=2.0).move_to([1.4, y, 0])
        b2 = binary_box(r"login binary", st[3], YES, w=2.6).move_to([4.9, y, 0])
        a1 = arrow(s1.get_right(), b1.get_left())
        a2 = arrow(s2.get_right(), b2.get_left())
        runs = CurvedArrow(b1.get_top() + RIGHT * 0.4, a2.get_center() + UP * 0.1, angle=-PI / 2.5, color=GREY_B,
                           stroke_width=2)
        rl = label(r"run the compiler binary on \texttt{login.py}", font_size=17, color=GREY_A).next_to(
            runs, UP, buff=0.08)
        foot = label(r"our toy: \ the language is Python; \ a binary is its marshalled code; \ sizes and hashes "
                     r"from our instrument", font_size=17, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Ken Thompson's lecture, published in 1984, builds its attack in three stages, and we will build each. "
            "<bookmark mark='a'/> A compiler is a program that turns "
            "source text into bytes; here the language is Python and a binary is its compiled code, but nothing "
            "else matters. <bookmark mark='b'/> The login program accepts one password. <bookmark mark='c'/> "
            "Compile the compiler's source and you get a compiler binary of four hundred and ninety-nine bytes. "
            "<bookmark mark='d'/> Run that binary on login's source and you get a login binary. A compiler can "
            "compile any program, including its own source: everything Thompson needs. <bookmark mark='e'/> The "
            "marked empty slot is only there to make our demonstration easy to read."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(comp))
            vo.wait_until("b")
            self.play(FadeIn(log_))
            vo.wait_until("c")
            self.play(FadeIn(s1), GrowArrow(a1), FadeIn(b1))
            vo.wait_until("d")
            self.play(FadeIn(s2), GrowArrow(a2), FadeIn(b2), Create(runs), FadeIn(rl))
            self.play(FadeIn(foot))
            vo.wait_until("e")
            self.play(Create(slot), FadeIn(sl))
        self.wait(0.4)
        self.clear_scene()

    def login(self):
        bd = load("trojan")["backdoor"]
        head = label(r"Stage 1: \ a backdoor in \texttt{login}", font_size=36).to_edge(UP, buff=0.3)
        lines = CLEAN_LOGIN.rstrip("\n").split("\n")
        code = code_block([lines[0], lines[1], '    if password == MAGIC: return True', lines[2]], size=17)
        code[2].set_color(NO)
        frame = SurroundingRectangle(code, buff=0.2, color=NO, stroke_width=1.5, corner_radius=0.08)
        lt = label(r"\texttt{login.py}, \ backdoored by hand", font_size=18, color=NO).next_to(frame, UP, buff=0.1)
        lt.align_to(frame, LEFT)
        src = VGroup(frame, code, lt).move_to([0, 1.55, 0])
        rows = []
        for key, name in (("accepts_correct", r"the right password"), ("accepts_magic", r"the magic password"),
                          ("accepts_wrong", r"a wrong guess")):
            rows.append([name, yes_no(bd["clean_binary"][key])[0], yes_no(bd["trojaned_binary"][key])[0]])
        tab = grid_table([r"typed at login", r"honest login", r"backdoored login"], rows, widths=[3.6, 2.6, 3.0],
                         row_h=0.5, font_size=20, mono_cols=())
        tab.next_to(src, DOWN, buff=0.55).set_x(0)
        for r, (key, _) in enumerate((("accepts_correct", 0), ("accepts_magic", 0), ("accepts_wrong", 0)), start=1):
            for c, which in ((1, "clean_binary"), (2, "trojaned_binary")):
                v = bd[which][key]
                tab.cells[r][c].set_color(YES if (v and key == "accepts_correct") else (NO if v else GREY_B))
        foot = wrapped_label(r"it works, \ but the line sits in \texttt{login.py} for anyone who reads it", 12.4,
                             font_size=21, color=HEAD).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Stage one is an ordinary backdoor. <bookmark mark='a'/> Add one line to login: if the password is a "
            "magic word, let them in. <bookmark mark='b'/> Compiled, the honest login lets in the right password and "
            "refuses everything else. The backdoored one also lets in the magic word, and still refuses a wrong "
            "guess, so nobody using it notices anything. <bookmark mark='c'/> But the line is in login's source, "
            "and anyone who reads the source will see it. The attack must leave the source."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(src))
            vo.wait_until("b")
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(FadeIn(foot), Indicate(code[2], color=NO))
        self.wait(0.4)
        self.clear_scene()

    def compiler(self):
        st = load("trojan")["stages"]
        head = label(r"Stage 2: \ move it into the compiler", font_size=36).to_edge(UP, buff=0.3)
        c = CLEAN_COMPILER.rstrip("\n").split("\n")
        lines = [c[0], c[1], c[2], "    if '# program: login' in src:", "        src = add_backdoor(src)",
                 c[4], c[5]]
        code = code_block(lines, size=16)
        code[3].set_color(NO)
        code[4].set_color(NO)
        frame = SurroundingRectangle(code, buff=0.2, color=NO, stroke_width=1.5, corner_radius=0.08)
        lt = label(r"\texttt{compiler.py}, \ with a trojan \ (simplified)", font_size=18, color=NO).next_to(
            frame, UP, buff=0.1).align_to(frame, LEFT)
        src = VGroup(frame, code, lt).move_to([0, 1.15, 0])
        y = -1.6
        s = cbox(r"\texttt{login.py}, \ honest", YES, w=2.8).move_to([-4.6, y, 0])
        tb = binary_box(r"trojaned compiler", st[1], NO, w=2.8).move_to([-0.6, y, 0])
        out_bad = binary_box(r"login binary", st[4], NO, w=2.6).move_to([3.9, y, 0])
        out_ok = binary_box(r"honest compiler's login", st[3], YES, w=2.6).next_to(out_bad, DOWN, buff=0.25)
        a1 = arrow(s.get_right(), tb.get_left())
        a2 = arrow(tb.get_right(), out_bad.get_left(), NO)
        cmp = label(r"compare", font_size=16, color=GREY_B).next_to(out_ok, LEFT, buff=0.2)
        foot = wrapped_label(r"\texttt{login.py} is now clean, \ but \texttt{compiler.py} shows the trick", 12.4,
                             font_size=21, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Stage two moves the line out of login and into the compiler. <bookmark mark='a'/> The compiler looks at "
            "what it is compiling. If it recognises login, it quietly adds the backdoor before compiling. "
            "<bookmark mark='b'/> Now login's source is honest, and anyone may audit it. <bookmark mark='c'/> But "
            "compiled by this compiler, login comes out two hundred and seventy-nine bytes long instead of two "
            "hundred and thirty-six, with the magic word inside. <bookmark mark='d'/> We have only moved the "
            "problem: the trick is now in the compiler's source, and compilers have readers too."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(src))
            vo.wait_until("b")
            self.play(FadeIn(s))
            vo.wait_until("c")
            self.play(GrowArrow(a1), FadeIn(tb))
            self.play(GrowArrow(a2), FadeIn(out_bad))
            self.play(FadeIn(out_ok), FadeIn(cmp))
            vo.wait_until("d")
            self.play(FadeIn(foot), Indicate(code[3:5], color=NO))
        self.wait(0.4)
        self.clear_scene()

    def quine(self):
        head = label(r"Stage 3: \ the trojan that copies itself \ (Part 25)", font_size=36).to_edge(UP, buff=0.3)
        lines = ["q = '<the text of this block, with a hole>'",
                 "if '# program: login' in src:",
                 "    src = add_backdoor(src)",
                 "elif '# program: compiler' in src:",
                 "    src = put_in_slot(src, q % q)"]
        code = code_block(lines, size=16)
        code[3].set_color(NO)
        code[4].set_color(NO)
        frame = SurroundingRectangle(code, buff=0.2, color=NO, stroke_width=1.5, corner_radius=0.08)
        lt = label(r"the trojan block $B$ \ (simplified from our instrument)", font_size=18, color=NO).next_to(
            frame, UP, buff=0.1).align_to(frame, LEFT)
        blk = VGroup(frame, code, lt).to_edge(LEFT, buff=0.45).shift(DOWN * 0.1)
        x = 3.9
        e1 = MathTex(r"B", r"=", r"T(T)", font_size=40).move_to([x, 2.0, 0])
        w1 = label(r"$T(x)$: \ the template $T$ with $x$ pasted in its hole", font_size=18, color=GREY_A).next_to(
            e1, DOWN, buff=0.15)
        e2 = MathTex(r"q", r"=", r"T", font_size=40).move_to([x, 0.75, 0])
        w2 = label(r"inside $B$, \ the variable $q$ holds the template", font_size=18, color=GREY_A).next_to(
            e2, DOWN, buff=0.15)
        e3 = MathTex(r"q(q)", r"=", r"T(T)", font_size=40).move_to([x, -0.5, 0])
        e4 = MathTex(r"q(q)", r"=", r"B", font_size=40, color=HEAD).move_to([x, -0.5, 0])
        w4 = label(r"so $B$ can rebuild its own text: \ a quine", font_size=18, color=HEAD).next_to(e3, DOWN,
                                                                                                  buff=0.15)
        foot = wrapped_label(r"compiling a compiler, \ the trojan writes a copy of itself into the output \ --- \ "
                             r"so the compiler's source no longer needs to contain it", 12.4, font_size=21,
                             color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Stage three is the clever one, and it is Part 25's quine. <bookmark mark='a'/> Teach the compiler a "
            "second trick: when it compiles a compiler, insert the trojan itself into the output. For that the "
            "trojan must know its own text. <bookmark mark='b'/> Write it as a template T with one hole, and form "
            "the block B by pasting T into its own hole. <bookmark mark='c'/> Inside B, the variable q holds the "
            "template. <bookmark mark='d'/> So q pasted into q is T pasted into T, <bookmark mark='e'/> which is B. "
            "The trojan can write out an exact copy of itself, exactly as a quine prints its own source. "
            "<bookmark mark='f'/> And that means the compiler's source no longer needs to contain it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(blk))
            self.play(Indicate(code[3:5], color=NO))
            vo.wait_until("b")
            self.play(Write(e1), FadeIn(w1))
            vo.wait_until("c")
            self.play(Write(e2), FadeIn(w2), Indicate(code[0], color=HEAD))
            vo.wait_until("d")
            self.play(Write(e3))
            vo.wait_until("e")
            self.play(TransformMatchingTex(e3, e4), FadeIn(w4))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def loop(self):
        t = load("trojan")
        st, bd, fx = t["stages"], t["backdoor"], t["fixpoint"]
        head = label(r"Delete the trojan from the source", font_size=36).to_edge(UP, buff=0.3)
        cx, cy, R = -2.7, -0.35, 2.1
        top = binary_box(r"trojaned compiler binary", st[1], NO, w=3.0).move_to([cx, cy + R, 0])
        src = cbox(r"\texttt{compiler.py}, \ clean", YES, w=2.7, h=0.6).move_to(
            [cx + R * np.cos(-PI / 6), cy + R * np.sin(-PI / 6), 0])
        out = binary_box(r"the binary it produces", st[2], NO, w=3.0).move_to(
            [cx + R * np.cos(7 * PI / 6), cy + R * np.sin(7 * PI / 6), 0])
        a1 = CurvedArrow(top.get_right(), src.get_top(), angle=-PI / 3, color=GREY_B, stroke_width=2.5)
        a2 = CurvedArrow(src.get_bottom() + LEFT * 0.3, out.get_bottom() + RIGHT * 0.3, angle=-PI / 3,
                         color=GREY_B, stroke_width=2.5)
        a3 = CurvedArrow(out.get_top(), top.get_left(), angle=-PI / 3, color=NO, stroke_width=3)
        l1 = label(r"compiles", font_size=17, color=GREY_A).next_to(a1, RIGHT, buff=0.05)
        l2 = label(r"produces", font_size=17, color=GREY_A).next_to(a2, DOWN, buff=0.08)
        l3 = label(r"bit for bit the same", font_size=17, color=NO).next_to(a3, LEFT, buff=0.05)
        path = Arc(radius=R, start_angle=PI / 2, angle=-TAU, arc_center=[cx, cy, 0])
        dot = Dot(path.get_start(), radius=0.1, color=HEAD)
        gen = Integer(1, font_size=34, color=HEAD).move_to([cx, cy + 0.15, 0])
        gl = label(r"generation", font_size=17, color=GREY_B).next_to(gen, DOWN, buff=0.1)
        ok = lambda v: r"yes" if v else r"no"  # noqa: E731
        right = VGroup(
            wrapped_label(rf"the output equals the trojaned binary: \ \textbf{{{ok(fx['reproduced_equals_trojaned'])}}}",
                          4.6, font_size=19, color=NO),
            wrapped_label(r"so the loop is a fixed point, \ and every generation is the same", 4.6, font_size=19,
                          color=WHITE),
            wrapped_label(rf"its \texttt{{login}} accepts the magic password: \ "
                          rf"\textbf{{{ok(bd['reproduced_binary']['accepts_magic'])}}}", 4.6, font_size=19,
                          color=NO),
            wrapped_label(rf"and the right one: \ \textbf{{{ok(bd['reproduced_binary']['accepts_correct'])}}}", 4.6,
                          font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.35, -0.1, 0])
        with self.voiceover(
            "Now delete every trace of the trojan from the compiler's source. <bookmark mark='a'/> Take the trojaned "
            "binary and give it the clean source to compile. <bookmark mark='b'/> It recognises a compiler, and "
            "inserts itself. The binary it produces has the same eleven hundred and nineteen bytes and the same "
            "hash: <bookmark mark='c'/> bit for bit the binary we started with. <bookmark mark='d'/> So the loop is "
            "a fixed point. Rebuild the compiler from clean source as often as you like, and every generation is "
            "the trojan again. <bookmark mark='e'/> And each of them, compiling the honest login, still lets in "
            "the magic word."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top))
            vo.wait_until("a")
            self.play(Create(a1), FadeIn(l1), FadeIn(src))
            vo.wait_until("b")
            self.play(Create(a2), FadeIn(l2), FadeIn(out))
            vo.wait_until("c")
            self.play(Create(a3), FadeIn(l3), FadeIn(right[0]))
            vo.wait_until("d")
            self.add(dot)
            self.play(FadeIn(gen), FadeIn(gl), FadeIn(right[1]))
            for g in (2, 3):
                self.play(MoveAlongPath(dot, path), run_time=2.0, rate_func=linear)
                self.play(gen.animate.set_value(g), Indicate(top, color=NO, scale_factor=1.04), run_time=0.6)
            vo.wait_until("e")
            self.play(FadeIn(right[2]), FadeIn(right[3]))
        self.wait(0.4)
        self.clear_scene()

    def moral(self):
        sc = load("trojan")["source_is_clean"]
        head = label(r"The moral", font_size=36).to_edge(UP, buff=0.3)
        found = lambda v: r"found" if v else r"not found"  # noqa: E731
        left = VGroup(label(r"what you can read", font_size=21, color=YES),
                      label(rf"\texttt{{compiler.py}}: \ the magic password {found(sc['magic_in_clean_compiler'])}",
                            font_size=19, color=WHITE),
                      label(rf"\texttt{{login.py}}: \ {found(sc['magic_in_clean_login'])}", font_size=19,
                            color=WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        right = VGroup(label(r"what you run", font_size=21, color=NO),
                       label(r"the compiler binary: \ carries the trojan", font_size=19, color=WHITE),
                       label(r"the login binary: \ lets in the magic word", font_size=19, color=WHITE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2)
        cols = VGroup(left, right).arrange(RIGHT, buff=1.2, aligned_edge=UP).next_to(head, DOWN, buff=0.5)
        bar = Line(cols.get_top() + DOWN * 0.05, cols.get_bottom(), color=GREY_D).move_to(
            (left.get_right() + right.get_left()) / 2 * RIGHT + cols.get_center()[1] * UP)
        quote = wrapped_label(r"``No amount of source-level verification or scrutiny will protect you from using "
                              r"untrusted code.'' \ --- \ Thompson, \ 1984", 12.0, font_size=22,
                              color=HEAD).next_to(cols, DOWN, buff=0.55)
        progs = [r"the compiler", r"the assembler", r"the loader", r"microcode"]
        chain = VGroup(*[cbox(p, KERN, w=2.4, h=0.55, size=18) for p in progs]).arrange(RIGHT, buff=0.45)
        chain.next_to(quote, DOWN, buff=0.6).set_x(0)
        arr = VGroup(*[arrow(chain[i].get_right(), chain[i + 1].get_left()) for i in range(3)])
        low = label(r"any program that handles programs; \ the lower it is, \ the harder to see", font_size=19,
                    color=GREY_A).next_to(chain, DOWN, buff=0.25)
        with self.voiceover(
            "That is the whole attack. <bookmark mark='a'/> Search every source file for the magic password and "
            "you will not find it. <bookmark mark='b'/> Yet the compiler you run carries the trojan, and the login "
            "you run lets in the magic word. <bookmark mark='c'/> Thompson's moral was blunt: no amount of "
            "source-level verification or scrutiny will protect you from using untrusted code. "
            "<bookmark mark='d'/> And he noted that he could have picked on any program that handles programs, an "
            "assembler, a loader, even hardware microcode, and that the lower the level, the harder such a bug is "
            "to detect. He credited the idea to an Air Force review of Multics in the 1970s. It looks hopeless. "
            "The next chapter shows that it is not."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right), Create(bar))
            vo.wait_until("c")
            self.play(FadeIn(quote))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(c) for c in chain], lag_ratio=0.4), FadeIn(arr), run_time=2.5)
            self.play(FadeIn(low))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
