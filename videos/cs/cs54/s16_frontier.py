from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs54.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


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
        self.industry()
        self.machines()
        self.open()

    def card(self):
        card = chapter_card(15, r"Frontier: \ proofs at scale",
                            r"Can proof become as routine as testing?", lit=(2015, 2024),
                            extra=((2015, r"Newcombe et al.: \ TLA+ at Amazon"),
                                   (2024, r"language models writing formal proofs")), part=PART)
        with self.voiceover("Chapter fifteen, the frontier. Can proof become as routine as testing?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def industry(self):
        head = label(r"Where proofs already pay", font_size=36).to_edge(UP, buff=0.3)
        tiles = VGroup(
            tile(r"designs", r"Amazon engineers model-checked TLA$^+$ specifications of core services and found "
                 r"subtle bugs before code existed \ (Newcombe et al. \ 2015)", HEAD),
            tile(r"cryptography", r"formally verified code for elliptic curves and ciphers \ (HACL$^*$, \ "
                 r"Fiat-Crypto) \ now runs inside major browsers and libraries", YES),
            tile(r"static analysis", r"Infer and similar tools run on every code change at large companies, \ "
                 r"reporting bugs found by sound approximations", DATA),
        ).arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.6)
        foot = wrapped_label(r"the pattern: \ prove the small, \ critical, \ stable parts; \ test the rest", 12.4,
                             font_size=21, color=WHITE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Proof is already routine in some places. <bookmark mark='a'/> Amazon's engineers described in 2015 how "
            "model-checking TLA-plus specifications of their storage and messaging services found subtle bugs "
            "before any code was written. <bookmark mark='b'/> Formally verified cryptographic code, from projects "
            "such as HACL-star and Fiat-Crypto, now runs inside major browsers and libraries. <bookmark mark='c'/> "
            "And static analysers run on every change at large companies, reporting bugs found by sound "
            "approximation. <bookmark mark='d'/> The pattern is to prove the small, critical, stable parts, and test "
            "the rest."
        ) as vo:
            self.play(FadeIn(head))
            for mk, t in zip("abc", tiles):
                vo.wait_until(mk)
                self.play(FadeIn(t, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def machines(self):
        lc = load("lcf")
        size = lc["size"]
        head = label(r"Machines that write proofs", font_size=36).to_edge(UP, buff=0.3)
        bar_k = Rectangle(width=12.0 * size["kernel_share"], height=0.6, stroke_width=0, fill_color=YES,
                          fill_opacity=0.85)
        bar_r = Rectangle(width=12.0 * (1 - size["kernel_share"]), height=0.6, stroke_width=0, fill_color=GREY_D,
                          fill_opacity=0.85)
        VGroup(bar_k, bar_r).arrange(RIGHT, buff=0).next_to(head, DOWN, buff=0.8)
        lk = label(rf"the trusted kernel: \ {size['kernel_lines']} lines", font_size=19, color=YES).next_to(
            bar_k, DOWN, buff=0.15)
        lr = label(r"everything else, \ including whatever writes the proof", font_size=19, color=GREY_A).next_to(
            bar_r, DOWN, buff=0.15).align_to(bar_r, RIGHT)
        lk.align_to(bar_k, LEFT)
        body = VGroup(
            wrapped_label(r"in an LCF-style checker, \ a proof is accepted only if the small kernel accepts every "
                          r"step: \ so the proof's author need not be trusted at all", 12.0, font_size=20,
                          color=WHITE),
            wrapped_label(r"language models now write Lean, \ Coq and Dafny proofs and loop invariants; \ "
                          r"in 2024 systems combining them with search solved olympiad problems with proofs a kernel "
                          r"checked", 12.0, font_size=20, color=DATA),
            wrapped_label(r"the open question is no longer whether a machine can be trusted to prove, \ but how "
                          r"much of a real program's specification it can find and prove unaided", 12.0,
                          font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(VGroup(lk, lr), DOWN, buff=0.6)
        with self.voiceover(
            "The newest change is who writes the proofs. <bookmark mark='a'/> In our LCF kernel from chapter ten, "
            f"only {size['kernel_lines']} lines have to be trusted; everything else, including whatever produced "
            "the proof, can be wrong without harm, because every step passes through the kernel. "
            "<bookmark mark='b'/> That is why language models can be put to work: they now write proofs in Lean, "
            "Coq and Dafny, and suggest loop invariants, and in 2024 systems that combined them with search solved "
            "olympiad problems with proofs that a kernel checked. <bookmark mark='c'/> The question is no longer "
            "whether a machine's proof can be trusted, but how much of a real program's specification it can find "
            "and prove on its own."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(GrowFromEdge(bar_k, LEFT), GrowFromEdge(bar_r, LEFT), FadeIn(lk), FadeIn(lr), FadeIn(body[0]))
            vo.wait_until("b")
            self.play(FadeIn(body[1]))
            vo.wait_until("c")
            self.play(FadeIn(body[2]))
        self.wait(0.4)
        self.clear_scene()

    def open(self):
        head = label(r"Open", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(
            wrapped_label(r"1. \ \textbf{Invariant inference}: \ finding the inductive invariants proofs need, \ "
                          r"automatically.", 12.4, font_size=24, color=WHITE),
            wrapped_label(r"2. \ \textbf{Specifications}: \ where they come from, \ and how to know they say what "
                          r"was meant.", 12.4, font_size=24, color=YES),
            wrapped_label(r"3. \ \textbf{Scale}: \ proofs that survive a million-line system's changes.", 12.4,
                          font_size=24, color=HEAD),
            wrapped_label(r"4. \ \textbf{Concurrency and hardware}: \ verified software on relaxed memory and "
                          r"speculative processors.", 12.4, font_size=24, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.45)
        star = wrapped_label(r"$\bigstar$ \ this part's research problem: \ an invariant-inference procedure that is "
                             r"complete for loops over integer arithmetic with multiplication, \ in a stated class "
                             r"of invariants, \ and fast enough to use", 12.4, font_size=23,
                             color=LAM).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Open problems. <bookmark mark='a'/> Finding the inductive invariants that proofs need, automatically. "
            "<bookmark mark='b'/> Knowing where specifications come from, and whether they say what was meant. "
            "<bookmark mark='c'/> Proofs that survive the constant change of a million-line system. "
            "<bookmark mark='d'/> And verified software on relaxed memory and speculative processors. "
            "<bookmark mark='e'/> This part's research problem is the first: an invariant-inference procedure for "
            "loops with multiplication, the case where our SAT checking slowed down most, that is complete for a "
            "stated class of invariants and fast enough to use."
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
