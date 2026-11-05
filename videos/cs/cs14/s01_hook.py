from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs14.common import CODE, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, code, load, mono


class Hook(VoiceoverScene):
    def construct(self):
        self.job()
        self.numbers()
        self.preview()
        self.plan()

    def job(self):
        h = load("hook")
        head = label(r"The Job, \ with no types written down", font_size=34).to_edge(UP, buff=0.3)
        src = h["source"]
        k = next(i for i, l in enumerate(src) if l.startswith("let rec bump"))
        excerpt = src[k:k + 6] + [""] + [l for l in src if l.startswith("let rec count")] + [""] + \
            [l for l in src if l.startswith("let job")]
        prog = code(excerpt, size=17, color=CODE).to_edge(LEFT, buff=0.5).shift(UP * 0.6)
        tl = label(r"the Job in the $\lambda$-core: \ functions, \ lists, \ pairs", font_size=19,
                   color=GREY_B).next_to(prog, UP, buff=0.15).align_to(prog, LEFT)
        types = VGroup(*[VGroup(mono(n, 17, WHITE), mono(": " + t, 17, YES)).arrange(RIGHT, buff=0.15)
                         for n, t in h["types"] if n in ("lower", "words", "bump", "count", "insert", "take",
                                                         "job")]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        types.to_edge(DOWN, buff=0.45).to_edge(LEFT, buff=0.5)
        ty_l = label(r"every type, \ inferred", font_size=21, color=YES).next_to(types, UP, buff=0.15).align_to(
            types, LEFT)
        poly = label(r"$'a$: \ \textit{any} type \ --- \ \texttt{bump} works for words, \ numbers, \ anything with "
                     r"$=$", font_size=19, color=HEAD).next_to(ty_l, RIGHT, buff=0.8)
        with self.voiceover(
            "Here is the Job once more, written in a new language: the lambda core, which this part builds. It has "
            "functions, lists and pairs, and nothing else worth mentioning. <bookmark mark='a'/> Notice what is "
            "missing. There is not one type annotation. bump adds one to a word's count in the table, count runs "
            "over all the words, and job puts the pieces together. <bookmark mark='b'/> Yet the compiler knows "
            "the type of every function. It worked them out by itself, in a few hundred tiny steps. <bookmark "
            "mark='c'/> And some of these types contain a variable, written tick a. bump works for words, but it "
            "would work just as well for numbers, or for anything that can be compared for equality. The machine "
            "discovered that too."
        ) as vo:
            self.play(FadeIn(head), FadeIn(prog), FadeIn(tl))
            vo.wait_until("a")
            self.play(Indicate(prog[:6], color=HEAD))
            vo.wait_until("b")
            self.play(FadeIn(ty_l), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.1) for t in types], lag_ratio=0.25),
                      run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(poly), Indicate(types[2], color=HEAD))
        self.wait(0.3)
        self.clear_scene()

    def numbers(self):
        h = load("hook")
        head = label(r"And underneath: \ not even numbers", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(*[mono(s.replace("\\", "λ"), 17, CODE if k < len(h["plus"]) - 1 else YES) for k, s in enumerate(h["plus"])])
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(head, DOWN, buff=0.5)
        if steps.width > 13:
            steps.scale_to_fit_width(13)
        arrows = VGroup(*[MathTex(r"\to_\beta", font_size=24, color=GREY_B).next_to(s, LEFT, buff=0.2)
                          for s in steps[1:]])
        cap = VGroup(
            label(r"$2 + 3$, \ written with functions alone", font_size=22, color=GREY_A),
            label(rf"{len(h['plus']) - 1} steps of one rule, \ and the answer is the numeral 5: \ apply $f$ five "
                  r"times", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "And underneath the lambda core there is something even smaller. <bookmark mark='a'/> Here is two plus "
            "three, written with functions and nothing else: no numbers, no addition, only functions applied to "
            "functions. <bookmark mark='b'/> One rule, applied again and again, rewrites it, <bookmark mark='c'/> "
            "until it stops. And the result is the number five, or rather, a function that applies f to x five "
            "times. Alonzo Church found in the nineteen thirties that this one rule is enough to compute anything "
            "that can be computed. Part 1 met his lambda calculus; this part takes it seriously."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), FadeIn(cap[0]))
            vo.wait_until("b")
            for s, a in zip(steps[1:-1], arrows[:-1]):
                self.play(FadeIn(s), FadeIn(a), run_time=0.7)
            vo.wait_until("c")
            self.play(FadeIn(steps[-1]), FadeIn(arrows[-1]), FadeIn(cap[1]))
        self.wait(0.3)
        self.clear_scene()

    def preview(self):
        head = label(r"By the end of this part", font_size=40).to_edge(UP, buff=0.4)
        facts = VGroup(
            label(r"arithmetic, \ data and recursion \ from functions alone", font_size=27, color=LAM),
            label(r"why the order of evaluation can matter, \ and why the answer cannot", font_size=27, color=CTRL),
            label(r"types, \ and a proof that well-typed programs cannot go wrong", font_size=27, color=YES),
            label(r"how a machine infers types nobody wrote", font_size=27, color=DATA),
            label(r"why a type is a theorem, \ and a program its proof", font_size=27, color=HEAD),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is where we are going. <bookmark mark='a'/> Numbers, booleans, lists and recursion, built from "
            "functions alone. <bookmark mark='b'/> Why the order in which we evaluate can decide whether a program "
            "finishes, and why it can never change the answer. <bookmark mark='c'/> Types, and a proof that "
            "well-typed programs cannot go wrong. <bookmark mark='d'/> How a machine infers types that nobody "
            "wrote. <bookmark mark='e'/> And the deepest surprise in the subject: that a type is a theorem, and a "
            "program of that type is its proof."
        ) as vo:
            self.play(FadeIn(head))
            for mk, f in zip("abcde", facts):
                vo.wait_until(mk)
                self.play(FadeIn(f, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Lambda and Types", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"$\lambda$-terms, \ substitution, \ $\beta$-reduction",
            r"Church encodings; \ the Y combinator",
            r"evaluation strategies; \ the Church--Rosser theorem",
            r"simple types; \ progress and preservation; \ normalization",
            r"Hindley--Milner inference; \ System F and free theorems",
            r"Curry--Howard; \ dependent, \ linear and gradual types",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 14 of Computer Science, Built, in Act Three, Speaking to the Machine. <bookmark "
            "mark='a'/> In this part: lambda terms, substitution and beta reduction. Church encodings, and the Y "
            "combinator. Evaluation strategies, and the Church Rosser theorem. Simple types, the safety theorems, "
            "and normalization. Hindley Milner inference, System F and free theorems. And the Curry Howard "
            "correspondence, with dependent, linear and gradual types."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.4)
        self.clear_scene()
