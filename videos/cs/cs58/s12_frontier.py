from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs58.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES


def tile(title, body, col, w=4.2, h=3.0):
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=col, stroke_width=2, fill_color=BG,
                             fill_opacity=1)
    t = label(title, font_size=22, color=col)
    b = wrapped_label(body, w - 0.4, font_size=18, color=GREY_A)
    VGroup(t, b).arrange(DOWN, buff=0.3).move_to(frame)
    return VGroup(frame, t, b)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.real()
        self.hott()
        self.open()

    def card(self):
        card = chapter_card(11, r"Frontier: \ semantics of real languages",
                            r"Can a whole real language be given a meaning a machine can check?", lit=(2009, 2017),
                            extra=((2009, r"Leroy: \ CompCert"), (2017, r"WebAssembly's formal semantics")),
                            part=PART)
        with self.voiceover("Chapter eleven, the frontier. Can a whole real language be given a meaning that a "
                            "machine can check?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def real(self):
        head = label(r"Mechanized semantics, \ at full size", font_size=36).to_edge(UP, buff=0.3)
        tiles = VGroup(
            tile(r"C, \ for a compiler", r"CompCert's Coq semantics of a large subset of C, \ and a proof that "
                 r"compilation preserves it \ (Leroy, \ 2009)", HEAD),
            tile(r"ML, \ end to end", r"CakeML: \ a verified compiler for a dialect of ML that compiles itself \ "
                 r"(Kumar et al., \ 2014)", YES),
            tile(r"WebAssembly", r"specified by small-step rules before release; \ its type system proved sound in "
                 r"Isabelle \ (Haas et al. \ 2017; \ Watt \ 2018)", DATA),
        ).arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.6)
        foot = wrapped_label(r"still missing: \ C's full concurrency model \ (Part 33's out-of-thin-air problem), \ "
                             r"and most of the languages people actually write", 12.4, font_size=21,
                             color=WHITE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "For decades semantics was done on paper, for small languages. <bookmark mark='a'/> Then Xavier Leroy's "
            "CompCert gave a large subset of C a semantics in the Coq proof assistant, and proved that its compiler "
            "preserves it. <bookmark mark='b'/> CakeML did the same for a dialect of ML, with a verified compiler "
            "that compiles itself. <bookmark mark='c'/> And WebAssembly was specified by small-step rules like "
            "chapter one's before it shipped, with its type system later proved sound in Isabelle. "
            "<bookmark mark='d'/> Still missing are a full semantics of C's concurrency, the out-of-thin-air problem "
            "of Part 33, and almost every language people actually write."
        ) as vo:
            self.play(FadeIn(head))
            for mk, t in zip("abc", tiles):
                vo.wait_until(mk)
                self.play(FadeIn(t, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def hott(self):
        head = label(r"Equality, \ rethought", font_size=36).to_edge(UP, buff=0.3)
        left = VGroup(MathTex(r"a =_A b", font_size=48, color=WHITE),
                      label(r"in Martin-L\"of type theory, \ a proof of equality is a value of a type", font_size=19,
                            color=GREY_A)).arrange(DOWN, buff=0.3)
        right = VGroup(MathTex(r"(A \simeq B) \simeq (A = B)", font_size=44, color=LAM),
                       label(r"univalence \ (Voevodsky): \ equivalent types are equal", font_size=19,
                             color=GREY_A)).arrange(DOWN, buff=0.3)
        VGroup(left, right).arrange(RIGHT, buff=1.2).next_to(head, DOWN, buff=0.9)
        p1 = Dot(LEFT * 2.0 + DOWN * 1.4, color=DATA)
        p2 = Dot(RIGHT * 2.0 + DOWN * 1.4, color=DATA)
        path = ArcBetweenPoints(p1.get_center(), p2.get_center(), angle=-PI / 3, color=HEAD)
        path2 = ArcBetweenPoints(p1.get_center(), p2.get_center(), angle=PI / 3, color=YES)
        cap = label(r"equalities as paths; \ two paths between the same points need not be the same", font_size=19,
                    color=WHITE).next_to(VGroup(p1, p2), DOWN, buff=0.8)
        foot = note(r"homotopy type theory \ (the HoTT book, \ 2013); \ cubical type theory makes univalence compute",
                    font_size=16).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The deepest frontier is about equality itself. <bookmark mark='a'/> In Martin-Löf's type theory, the "
            "basis of chapter nine's dependent types, a proof that a equals b is itself a value, of a type. "
            "<bookmark mark='b'/> Vladimir Voevodsky's univalence axiom says that equivalent types are equal, which "
            "is how mathematicians already reason. <bookmark mark='c'/> The model that makes sense of it reads "
            "equalities as paths in a space, and two paths between the same points need not be the same path. This "
            "is homotopy type theory, and cubical type theory, a few years later, made univalence compute."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(p1), FadeIn(p2), Create(path), Create(path2), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    def open(self):
        head = label(r"Open", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(
            wrapped_label(r"1. \ \textbf{Full abstraction for real languages}: \ a mathematical model that equates "
                          r"exactly the programs no context can tell apart.", 12.4, font_size=24, color=WHITE),
            wrapped_label(r"2. \ \textbf{Concurrency}: \ a memory model for C and C++ without out-of-thin-air "
                          r"results, \ that compilers can keep.", 12.4, font_size=24, color=YES),
            wrapped_label(r"3. \ \textbf{Effects}: \ one semantics that composes state, \ exceptions, \ "
                          r"probability and concurrency.", 12.4, font_size=24, color=HEAD),
            wrapped_label(r"4. \ \textbf{Proof engineering}: \ semantics that stay maintainable as languages "
                          r"evolve.", 12.4, font_size=24, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.45)
        star = wrapped_label(r"$\bigstar$ \ this part's research problem: \ a semantics of relaxed-memory concurrency "
                             r"for C that forbids out-of-thin-air values, \ permits the optimizations compilers "
                             r"perform, \ and is proved so", 12.4, font_size=23, color=LAM).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Open problems. <bookmark mark='a'/> Fully abstract models of real languages, which equate exactly the "
            "programs that no context can tell apart. <bookmark mark='b'/> A memory model for C and C++ without "
            "out-of-thin-air results that compilers can still respect. <bookmark mark='c'/> One semantics of effects "
            "that composes state, exceptions, probability and concurrency. <bookmark mark='d'/> And semantics that "
            "stay maintainable as languages change. <bookmark mark='e'/> This part's research problem is the second "
            "of these: a relaxed-memory semantics for C that forbids values from thin air, still allows the "
            "optimizations real compilers perform, and is proved to do both."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.6)
        self.clear_scene()


_ = (DATA, KERN, LAM, NO, YES)
