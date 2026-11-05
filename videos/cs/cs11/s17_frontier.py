from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs11.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, load, region)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.capabilities()
        self.semantics()
        self.allocation()

    def card(self):
        card = chapter_card(16, r"Frontier: \ bounds, \ semantics, \ capabilities",
                            r"Can memory safety be built into the machine?", lit=(2015, 2022),
                            extra=((2015, r"CHERI"), (2022, r"Arm Morello")), part=PART)
        with self.voiceover("Chapter sixteen. The frontier."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def capabilities(self):
        fr = load("frontier")
        head = label(r"Pointers that carry their bounds", font_size=34).to_edge(UP, buff=0.3)
        ptr = VGroup(region(2.2, 0.6, r"address", DATA, font_size=18), region(1.6, 0.6, r"base", CTRL, font_size=18),
                     region(1.6, 0.6, r"length", CTRL, font_size=18), region(2.0, 0.6, r"permissions", FUNC,
                                                                            font_size=18),
                     region(1.0, 0.6, r"tag", NO, font_size=18)).arrange(RIGHT, buff=0).next_to(head, DOWN, buff=0.5)
        pl = label(r"a CHERI capability: \ 128 bits, \ plus a hidden tag bit the program cannot forge", font_size=19,
                   color=GREY_A).next_to(ptr, DOWN, buff=0.15)
        pts = VGroup(
            label(r"every load and store is checked against the bounds of the pointer it uses", font_size=21,
                  color=GREY_A),
            label(r"pointers can only be derived from pointers, \ and only made smaller", font_size=21, color=GREY_A),
            label(r"on our Pebble, \ in miniature: \ greet's buffer pointer gets bounds $[sp, sp + 64)$", font_size=21,
                  color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(pl, DOWN, buff=0.4)
        res = VGroup(label(r"the attack, \ run again:", font_size=20, color=GREY_B),
                     Text(fr["attack"]["fault"], font="DejaVu Sans Mono", font_size=16, color=YES),
                     label(r"the 65th byte, \ before the return address is touched; \ \texttt{Ada} is greeted as "
                           r"before", font_size=19, color=YES)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "The defences of chapter fourteen all work around the real problem: a pointer in C is just a number, "
            "and nothing knows how big the object behind it is. <bookmark mark='a'/> The CHERI project, from the "
            "University of Cambridge and SRI since 2010, changes the hardware so that a pointer is a capability: an "
            "address together with the bounds and permissions of the object, and a hidden tag bit that the program "
            "cannot forge. <bookmark mark='b'/> Every load and store is checked against the bounds of the pointer it "
            "uses, and a new pointer can only be made from an existing one, never larger. Arm built a prototype "
            "processor, Morello, in 2022. <bookmark mark='c'/> We added a miniature version to Pebble's emulator: "
            "when greet takes its buffer's address, the pointer gets bounds of sixty-four bytes, and the bounds "
            "travel with it. <bookmark mark='d'/> Run the attack again, and the machine traps on the sixty-fifth "
            "byte, before the return address is reached; an honest name is greeted as before."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ptr), FadeIn(pl))
            vo.wait_until("b")
            self.play(FadeIn(pts[0]), FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    def semantics(self):
        head = label(r"What does a C program mean?", font_size=34).to_edge(UP, buff=0.35)
        pts = VGroup(
            label(r"to prove a compiler correct you need a precise meaning for the source, \ undefined behaviour "
                  r"included", font_size=21, color=GREY_A),
            label(r"CompCert \ (Leroy, \ 2006 onward): \ a C compiler proved in Coq to preserve the meaning of "
                  r"every defined program", font_size=21, color=YES),
            label(r"Cerberus \ (Memarian, \ Sewell and others, \ 2016 onward): \ an executable semantics of C as "
                  r"real code uses it", font_size=21, color=DATA),
            label(r"the hard part: \ \textit{pointer provenance}, \ which object a pointer may legally reach, \ "
                  r"now being standardized", font_size=21, color=HEAD),
            label(r"open: \ a semantics that the standard, \ compilers \textit{and} existing code all agree with",
                  font_size=22, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(DOWN * 0.1)
        with self.voiceover(
            "The second frontier is meaning. <bookmark mark='a'/> To prove that a compiler is correct, you need a "
            "precise definition of what the source program means, undefined behaviour and all. <bookmark "
            "mark='b'/> Xavier Leroy's CompCert, begun in 2006, is a C compiler whose every pass is proved, in the "
            "Coq proof assistant, to preserve the meaning of every program that has no undefined behaviour; tests "
            "that find bugs in every other compiler have found none in its proved parts. <bookmark mark='c'/> The "
            "Cerberus project of Kayvan Memarian, Peter Sewell and colleagues built an executable semantics of C as "
            "programmers actually use it. <bookmark mark='d'/> The hardest question turned out to be pointer "
            "provenance: which object a pointer is allowed to reach, even when two pointers hold the same address. "
            "A model of it is now being standardized. <bookmark mark='e'/> Still open is a semantics that the "
            "standard, the optimizers and the billions of lines of existing code can all live with."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def allocation(self):
        fr = load("frontier")
        head = label(r"And the allocator's open questions", font_size=34).to_edge(UP, buff=0.35)
        pts = VGroup(
            label(r"Robson's bound is tight for \textit{some} allocator; \ for first fit and best fit the exact "
                  r"worst case is still open", font_size=21, color=GREY_A),
            label(r"real programs are nowhere near the worst case: \ Johnstone and Wilson \ (1998) found "
                  r"fragmentation of a few percent", font_size=21, color=YES),
            label(r"why, \ in theory? \ No model of ``realistic'' programs explains it", font_size=21, color=HEAD),
            label(r"and memory safety for allocators: \ use-after-free is the commonest severe bug in C++ code; \ "
                  r"quarantines, \ type-segregated heaps, \ MiraclePtr", font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(DOWN * 0.1)
        with self.voiceover(
            "And the allocators of chapters six to eight have frontiers of their own. <bookmark mark='a'/> Robson's "
            "bound is achieved by a carefully designed allocator, but for the policies everyone uses, first fit and "
            "best fit, the exact worst case is still not known. <bookmark mark='b'/> Meanwhile real programs are "
            "nowhere near the worst case. Mark Johnstone and Paul Wilson measured real programs in 1998 "
            "and found that good policies waste only a few percent, as we saw with Perl. <bookmark mark='c'/> Why "
            "real programs are so kind has never been explained by a model. <bookmark mark='d'/> And allocators are "
            "now a security battleground: using memory after freeing it is among the commonest severe bugs in large "
            "C and C++ programs, and browsers now defend with quarantines that delay reuse, heaps segregated by type, "
            "and smart pointers like Chrome's MiraclePtr."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
