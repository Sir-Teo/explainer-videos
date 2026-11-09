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
        pl = label("conceptual fields; Morello: 128-bit compressed capability plus a protected tag", font_size=19,
                   color=GREY_A).next_to(ptr, DOWN, buff=0.15)
        pts = VGroup(
            label("capability-based accesses check bounds and permissions; hybrid modes also allow ordinary pointers", font_size=21,
                  color=GREY_A),
            label("derivation cannot increase authority; the cursor can move under the rules", font_size=21, color=GREY_A),
            label(r"on our Pebble, \ in miniature: \ greet's buffer pointer gets bounds $[sp, sp + 64)$", font_size=21,
                  color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(pl, DOWN, buff=0.4)
        res = VGroup(label(r"the attack, \ run again:", font_size=20, color=GREY_B),
                     Text(fr["attack"]["fault"], font="DejaVu Sans Mono", font_size=16, color=YES),
                     label(r"the 65th byte, \ before the return address is touched; \ \texttt{Ada} is greeted as "
                           r"before", font_size=19, color=YES)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(
            DOWN, buff=0.35)
        with self.voiceover("Ordinary address arithmetic does not automatically enforce object bounds. <bookmark mark='a'/> CHERI associates capabilities with address, bounds, permissions and a protected validity tag. This diagram is conceptual; encodings vary. Morello uses 128-bit capabilities plus a tag, with compressed bounds rather than these literal separate fields. <bookmark mark='b'/> Capability-based accesses check authority. Derivation cannot increase authority beyond what is held, although the cursor can move within the rules; bounds need not become strictly smaller on every operation. Hybrid systems can also retain ordinary pointers. Arm's Morello prototype arrived in 2022. <bookmark mark='c'/> Pebble's miniature model attaches exact sixty-four-byte bounds to greet's buffer pointer. It is a teaching model, not a complete CHERI implementation. <bookmark mark='d'/> It traps this attack at the sixty-fifth byte and still greets Ada. Spatial bounds alone do not generally solve use-after-free: temporal safety needs additional mechanisms.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(ptr), FadeIn(pl), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(pts[0]), FadeIn(pts[1]))
            vo.wait_until('c')
            self.play(FadeIn(pts[2]))
            vo.wait_until('d')
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    def semantics(self):
        head = label(r"What does a C program mean?", font_size=34).to_edge(UP, buff=0.35)
        pts = VGroup(
            label(r"to prove a compiler correct you need a precise meaning for the source, \ undefined behaviour "
                  r"included", font_size=21, color=GREY_A),
            label("CompCert: semantic preservation for verified passes and supported C, under explicit assumptions", font_size=21, color=YES),
            label(r"Cerberus \ (Memarian, \ Sewell and others, \ 2016 onward): \ an executable semantics of C as "
                  r"real code uses it", font_size=21, color=DATA),
            label("pointer provenance: which storage instance may a pointer access? standards work continues", font_size=21, color=HEAD),
            label(r"open: \ a semantics that the standard, \ compilers \textit{and} existing code all agree with",
                  font_size=22, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(DOWN * 0.1)
        with self.voiceover(
            (
            "Compiler correctness requires an explicit source semantics and a stated proof boundary. <bookmark "
            "mark='a'/> The theorem connects behaviors in source and target languages, including how undefined "
            "source behavior limits the guarantee. <bookmark mark='b'/> CompCert proves semantic preservation for "
            "its verified compilation passes and supported C subset. Its theorem relies on assumptions about "
            "unverified interfaces and tools; it is not a proof of every C program or every surrounding "
            "component. <bookmark mark='c'/> Cerberus explores executable models of C, including the difficult "
            "interactions of pointers, objects and real implementation practice. <bookmark mark='d'/> Pointer "
            "provenance asks which storage instance a pointer may access, even when numeric addresses coincide. "
            "Standards work and implementation models continue to refine these rules; a proposal is not "
            "automatically an adopted standard. <bookmark mark='e'/> Research compares formal guarantees, "
            "compatibility with existing code and optimizer behavior. We should name the particular semantics and "
            "version before claiming that all three agree."
        )
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
            label("worst-case bounds depend on allocation model and policy; our replay tests two implementations", font_size=21, color=GREY_A),
            label("Johnstone and Wilson (1998): low fragmentation on studied policies and workloads", font_size=21, color=YES),
            label("research: predictive models of lifetimes, size distributions, locality and concurrency", font_size=21, color=HEAD),
            label("temporal safety needs more than spatial bounds: quarantines, type segregation, checked references", font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(DOWN * 0.1)
        with self.voiceover(
            (
            "Allocator research depends strongly on the model and workload. <bookmark mark='a'/> Robson's lower "
            "bounds and policy-specific upper and lower bounds require their own hypotheses; our eight-phase "
            "trace establishes only the displayed measurements for our implementations. <bookmark mark='b'/> "
            "Johnstone and Wilson's 1998 study found low fragmentation for selected policies and measured "
            "programs. Our Perl replay is one additional workload, and its peak ratio includes headers and "
            "alignment. Neither establishes that all programs stay near the average. <bookmark mark='c'/> "
            "Lifetime correlations, size distributions, locality and concurrency help explain behavior; finding "
            "useful predictive models remains a research question, rather than a claim that no model exists. "
            "<bookmark mark='d'/> Temporal safety is another challenge. Quarantines delay reuse, type segregation "
            "limits some reuse patterns, and checked smart-pointer schemes protect selected references. Each has "
            "coverage and overhead limits; a spatial capability by itself does not revoke every stale reference."
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
