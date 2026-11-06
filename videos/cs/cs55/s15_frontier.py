from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs55.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


def tile(title, body, col, w=4.2, h=2.7):
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=col, stroke_width=2, fill_color=BG,
                             fill_opacity=1)
    t = label(title, font_size=21, color=col)
    b = wrapped_label(body, w - 0.4, font_size=17, color=GREY_A)
    VGroup(t, b).arrange(DOWN, buff=0.25).move_to(frame)
    return VGroup(frame, t, b)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.sky()
        self.security()
        self.open()

    def card(self):
        card = chapter_card(14, r"Frontier: \ the open problems of the series",
                            r"What did we meet that nobody knows?", lit=(1971, 2024),
                            extra=((1971, r"Cook: \ P versus NP"), (2024, r"BB(5) proved")), part=PART)
        with self.voiceover("Chapter fourteen, the frontier. What did this series meet that nobody knows?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def sky(self):
        rows = load("open")["rows"]
        head = label(r"Questions the degree left open", font_size=36).to_edge(UP, buff=0.3)
        cells = VGroup()
        cols = (NO, HEAD, YES, DATA, LAM, KERN)
        for i, r in enumerate(rows):
            parts = ", ".join(str(p) for p in r["parts"])
            box = RoundedRectangle(width=6.2, height=0.72, corner_radius=0.1, stroke_color=cols[i % 6],
                                   stroke_width=1.5, fill_color=BG, fill_opacity=1)
            t = label(rf"{r['problem']} \ (Part{'s' if len(r['parts']) > 1 else ''} {parts})", font_size=17,
                      color=cols[i % 6])
            d = label(r["record"], font_size=14, color=GREY_A)
            for x in (t, d):
                if x.width > 5.9:
                    x.width = 5.9
            g = VGroup(t, d).arrange(DOWN, buff=0.06).move_to(box)
            cells.add(VGroup(box, g))
        cells.arrange_in_grid(cols=2, buff=(0.25, 0.14), flow_order="dr").next_to(head, DOWN, buff=0.3)
        if cells.height > 6.4:
            cells.height = 6.4
            cells.next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "Along the way this series met questions that nobody can answer. <bookmark mark='a'/> Whether P equals "
            "NP, and whether one-way functions, and with them all of modern cryptography, exist at all. How fast "
            "matrices can be multiplied. The sixth Busy Beaver number, now that the fifth was finally proved in "
            "2024. Whether splay trees are optimal. The unique games conjecture. Whether randomness ever really "
            "helps. Why we cannot prove that any explicit function needs many gates. <bookmark mark='b'/> And the "
            "practical ones: a memory model for C, quantum computers that do something useful, and verified software "
            "at the scale people actually build. Part 61 returns to each of these, as research."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cells[:8]], lag_ratio=0.25), run_time=5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in cells[8:]], lag_ratio=0.3), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def security(self):
        head = label(r"The frontier of trust", font_size=36).to_edge(UP, buff=0.3)
        tiles = VGroup(
            tile(r"memory safety at scale", r"rewriting or hardening billions of lines of C and C++; \ CHERI "
                 r"capabilities in hardware; \ proving Rust's unsafe code", NO),
            tile(r"speculation", r"processors that leak nothing through timing, \ at a cost people will pay; \ "
                 r"contracts between hardware and software", HEAD),
            tile(r"bootstrapping trust", r"building a whole toolchain from a seed of a few hundred bytes that a "
                 r"person can audit \ (the bootstrappable-builds project)", YES),
        ).arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.6)
        foot = wrapped_label(r"each turns an informal promise \ --- \ this layer hides what is below \ --- \ into "
                             r"something that can be checked", 12.4, font_size=21, color=WHITE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Three frontiers of trust in particular. <bookmark mark='a'/> Memory safety at scale: rewriting or "
            "hardening billions of lines of C and C++, capabilities built into hardware, and proofs about the unsafe "
            "corners of Rust. <bookmark mark='b'/> Speculation: processors that leak nothing through timing, at a "
            "cost people will accept, and precise contracts between hardware and software about what may leak. "
            "<bookmark mark='c'/> And bootstrapping: building a whole modern toolchain up from a seed program of a "
            "few hundred bytes that a person can read, so that Thompson's attack has nowhere to hide. "
            "<bookmark mark='d'/> Each turns an informal promise, that a layer hides what is below it, into "
            "something that can be checked."
        ) as vo:
            self.play(FadeIn(head))
            for mk, t in zip("abc", tiles):
                vo.wait_until(mk)
                self.play(FadeIn(t, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def open(self):
        head = label(r"Open", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(
            wrapped_label(r"1. \ \textbf{One-way functions}: \ do they exist? \ All of Parts 29 and 30 assume so.",
                          12.4, font_size=24, color=WHITE),
            wrapped_label(r"2. \ \textbf{Speculation}: \ a processor provably free of transient-execution leaks, "
                          r"\ at low cost.", 12.4, font_size=24, color=YES),
            wrapped_label(r"3. \ \textbf{Legacy code}: \ automatic, \ trustworthy translation of C into a "
                          r"memory-safe language.", 12.4, font_size=24, color=HEAD),
            wrapped_label(r"4. \ \textbf{Supply chains}: \ knowing what is in the software you run, \ and who "
                          r"could change it.", 12.4, font_size=24, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.45)
        star = wrapped_label(r"$\bigstar$ \ this part's research problem: \ a full software stack, \ from an "
                             r"auditable seed of a few hundred bytes to a modern compiler and kernel, \ with every "
                             r"build reproducible and every translation proved correct", 12.4, font_size=23,
                             color=LAM).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Open problems. <bookmark mark='a'/> Whether one-way functions exist, the assumption under all of Parts "
            "29 and 30. <bookmark mark='b'/> A processor provably free of transient-execution leaks at low cost. "
            "<bookmark mark='c'/> Trustworthy automatic translation of C into a memory-safe language. "
            "<bookmark mark='d'/> And knowing what is inside the software we run, and who could change it. "
            "<bookmark mark='e'/> This part's research problem joins the last chapters together: a complete "
            "software stack, built up from a seed small enough to audit, every step reproducible, every translation "
            "proved correct, so that trusting it no longer means trusting anyone."
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
