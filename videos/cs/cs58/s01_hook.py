from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs58.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, mono


class Hook(VoiceoverScene):
    def construct(self):
        self.three()
        self.why()
        self.plan()

    def three(self):
        f = load("fact")
        k = load("kleene")["rows"]
        head = label(r"Three meanings of one program", font_size=36).to_edge(UP, buff=0.3)
        prog = mono("fact n = if n = 0 then 1 else n * fact (n - 1)", size=22, color=WHITE).next_to(head, DOWN,
                                                                                                   buff=0.4)
        col = VGroup()
        steps = VGroup(*[mono(t if len(t) < 34 else t[:31] + "...", size=14, color=GREY_A) for t in
                         [s.replace("(fix fact n -> (if (n = 0) then 1 else (n * (fact (n - 1)))))", "fact")
                          for s in f["trace"][-7:]]]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        b1 = VGroup(label(r"as steps", font_size=24, color=HEAD), steps).arrange(DOWN, buff=0.25)
        chain = VGroup(*[mono("  ".join("." if v is None else str(v) for v in r["table"][:7]), size=16, color=GREY_A)
                         for r in k[:7]]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        b2 = VGroup(label(r"as a limit", font_size=24, color=YES), chain,
                    label(r"$\bot \sqsubseteq F(\bot) \sqsubseteq F^2(\bot) \sqsubseteq \cdots$", font_size=22,
                          color=YES)).arrange(DOWN, buff=0.25)
        laws = VGroup(MathTex(r"\mathit{fact}\,0 = 1", font_size=30), MathTex(
            r"\mathit{fact}\,(n+1) = (n+1)\cdot \mathit{fact}\,n", font_size=30),
            MathTex(r"\{n \ge 0\}\ \mathit{fact}\,n\ \{r = n!\}", font_size=30)).arrange(DOWN, buff=0.25)
        b3 = VGroup(label(r"as laws", font_size=24, color=DATA), laws).arrange(DOWN, buff=0.25)
        col = VGroup(b1, b2, b3).arrange(RIGHT, buff=0.6, aligned_edge=UP).next_to(prog, DOWN, buff=0.5)
        if col.width > 13.2:
            col.width = 13.2
        foot = note(rf"steps: \ our small-step interpreter, \ {f['steps']} steps for fact 3; \ the limit: \ the "
                    r"Kleene chain of the factorial functional", font_size=16).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "What does a program mean? Here is factorial, and three different answers. <bookmark mark='a'/> First, "
            f"as steps: the meaning is what a machine does with it. Our interpreter rewrites fact of three in "
            f"{f['steps']} small steps, down to six. <bookmark mark='b'/> Second, as a mathematical object: the "
            "meaning is a function, the limit of a chain of approximations. The first knows nothing, the next knows "
            "factorial of zero, the next of zero and one, and the limit is factorial itself. <bookmark mark='c'/> "
            "Third, as laws: the meaning is what can be proved about it, equations and Hoare triples. "
            "<bookmark mark='d'/> These are operational, denotational and axiomatic semantics, and the deep results "
            "of this part say when they agree."
        ) as vo:
            self.play(FadeIn(head), FadeIn(prog))
            vo.wait_until("a")
            self.play(FadeIn(b1[0]), LaggedStart(*[FadeIn(s) for s in steps], lag_ratio=0.2), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(b2[0]), LaggedStart(*[FadeIn(r) for r in chain], lag_ratio=0.25), FadeIn(b2[2]),
                      run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(b3))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def why(self):
        a = load("agree")
        head = label(r"Why bother with meaning?", font_size=36).to_edge(UP, buff=0.3)
        tiles = VGroup()
        for t, d, c in ((r"compilers", r"a compiler is correct if the meaning of its output equals the meaning of "
                         r"its input \ (CompCert, \ Part 54)", HEAD),
                        (r"refactoring", r"two programs are interchangeable if no context can tell them apart", YES),
                        (r"language design", r"WebAssembly was specified formally before it shipped \ (2017)", DATA)):
            r = RoundedRectangle(width=4.0, height=2.4, corner_radius=0.15, stroke_color=c, stroke_width=2,
                                 fill_color=BG, fill_opacity=1)
            g = VGroup(label(t, font_size=24, color=c), wrapped_label(d, 3.6, font_size=18, color=GREY_A)).arrange(
                DOWN, buff=0.2).move_to(r)
            tiles.add(VGroup(r, g))
        tiles.arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.6)
        foot = wrapped_label(rf"our three interpreters \ --- \ small-step, \ big-step and the CEK machine of Part 15 \ "
                             rf"--- \ agree on {a['agree']} of {a['n']} random programs", 12.4, font_size=21,
                             color=WHITE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Why does this matter outside a classroom? <bookmark mark='a'/> A compiler is correct exactly when the "
            "meaning of what it emits equals the meaning of what it was given, which is how CompCert was proved. "
            "<bookmark mark='b'/> A refactoring is safe when no surrounding program can tell the old code from the "
            "new. <bookmark mark='c'/> And languages can be designed with their meaning written down first: "
            "WebAssembly's specification was formal before the language shipped. <bookmark mark='d'/> In this part "
            f"we build three interpreters for one small language and check that they agree, on all {a['n']} random "
            "programs we tried; then we prove why."
        ) as vo:
            self.play(FadeIn(head))
            for mk, t in zip("abc", tiles):
                vo.wait_until(mk)
                self.play(FadeIn(t, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Semantics", font_size=36).to_edge(UP, buff=0.3)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"small-step, \ big-step and the CEK machine",
            r"denotations, \ domains and least fixed points",
            r"adequacy, \ full abstraction and parallel-or",
            r"equivalence, \ bisimulation and logical relations",
            r"parametricity: \ theorems for free",
            r"effects, \ dependent types and processes",
        ], font_size=25).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 58 of Computer Science, Built. <bookmark mark='a'/> We will give one language three "
            "operational semantics; build its denotational semantics on domains and least fixed points; ask when the "
            "two agree; decide when two programs are the same, by bisimulation and logical relations; derive "
            "theorems for free from types alone; and extend meaning to effects, dependent types and communicating "
            "processes."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (BG, DATA, KERN, LAM, NO, YES)
