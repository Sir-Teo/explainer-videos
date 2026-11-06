from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs55.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, mono

LAYERS = [(r"gates and memory", r"Rowhammer: \ hammering one DRAM row flips bits in its neighbours", r"Part 5"),
          (r"the processor", r"Spectre: \ speculation leaves secrets in the cache", r"Part 8"),
          (r"programs", r"a stack smash returns into the attacker's input", r"Part 11"),
          (r"the kernel", r"a sandbox escape crosses the line Part 31 drew", r"Part 31"),
          (r"the compiler", r"a compiler that inserts a backdoor its source never shows", r"Part 13"),
          (r"the network", r"a BGP announcement steals a block of addresses", r"Part 36"),
          (r"the web", r"a string becomes code: \ injection", r"Part 42"),
          (r"the supply chain", r"a maintainer plants a backdoor in a compression library", r"Part 41")]


class Hook(VoiceoverScene):
    def construct(self):
        self.tower()
        self.thompson()
        self.plan()

    def tower(self):
        head = label(r"Every layer leaks", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup()
        for i, (name, leak, part) in enumerate(LAYERS):
            box = Rectangle(width=3.4, height=0.55, stroke_color=GREY_B, stroke_width=1.5, fill_color=BG,
                            fill_opacity=1)
            t = label(name, font_size=19, color=WHITE).move_to(box)
            lk = label(leak, font_size=17, color=NO)
            pt = label(part, font_size=15, color=GREY_B)
            rows.add(VGroup(VGroup(box, t), lk, pt))
        VGroup(*[r[0] for r in rows]).arrange(UP, buff=0.06).next_to(head, DOWN, buff=0.4).to_edge(
            LEFT, buff=0.8)
        for r in rows:
            r[1].next_to(r[0], RIGHT, buff=0.4)
            r[2].next_to(r[1], RIGHT, buff=0.25)
            if r[1].width + r[2].width > 8.8:
                r[1].width = 8.8 - r[2].width
                r[1].next_to(r[0], RIGHT, buff=0.4)
                r[2].next_to(r[1], RIGHT, buff=0.25)
        foot = wrapped_label(r"security is a property of the whole tower: \ an attacker needs one weak layer, \ a "
                             r"defender must hold them all", 12.4, font_size=21, color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "This series built a tower, from gates to a cluster, and claimed at every level that the layer above "
            "need not care how the layer below works. <bookmark mark='a'/> Security is where that claim fails. "
            "Hammer one row of memory and bits flip in its neighbours. Speculate past a branch and a secret leaves "
            "a trace in the cache. Overflow a buffer and a function returns into the attacker's input. "
            "<bookmark mark='b'/> A kernel bug crosses a sandbox's wall; a compiler can insert a backdoor that no "
            "source shows; one BGP announcement steals a block of the internet; a string typed into a web form "
            "becomes code; and in 2024 a maintainer of a compression library hid a backdoor in it for two years. "
            "<bookmark mark='c'/> An attacker needs one weak layer. A defender must hold them all."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r[0]) for r in rows], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r[1], r[2]), shift=RIGHT * 0.1) for r in rows[:3]],
                                  lag_ratio=0.5), run_time=3)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(r[1], r[2]), shift=RIGHT * 0.1) for r in rows[3:]],
                                  lag_ratio=0.5), run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(foot), *[r[0][0].animate.set_stroke(NO) for r in rows])
        self.wait(0.4)
        self.clear_scene()

    def thompson(self):
        t = load("trojan")
        st = t["stages"]
        head = label(r"A backdoor with no source", font_size=36).to_edge(UP, buff=0.3)
        quote = wrapped_label(r"``You can't trust code that you did not totally create yourself.'' \ --- Ken "
                              r"Thompson, \ \textit{Reflections on Trusting Trust}, \ 1984", 12.0, font_size=20,
                              color=GREY_A).next_to(head, DOWN, buff=0.35)
        rows = VGroup()
        for s, col in zip(st, (YES, NO, NO)):
            rows.add(VGroup(label(s["stage"], font_size=21, color=col), mono(s["sha256"][:16], size=18, color=col),
                            label(rf"{s['size']:,} bytes", font_size=19, color=GREY_B)).arrange(RIGHT, buff=0.5))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(quote, DOWN, buff=0.6)
        notes = VGroup(
            label(r"the reproduced compiler was built from clean source, \ by the trojaned binary", font_size=19,
                  color=WHITE),
            label(r"its hash is the trojan's: \ the backdoor survives with no trace in any source", font_size=19,
                  color=NO)).arrange(DOWN, buff=0.15).next_to(rows, DOWN, buff=0.5)
        with self.voiceover(
            "And then there is the attack that closes this series. <bookmark mark='a'/> In his Turing Award lecture "
            "of 1984 Ken Thompson described a compiler that inserts a backdoor whenever it compiles the login "
            "program, and inserts itself whenever it compiles a compiler. <bookmark mark='b'/> We built it. Here are "
            "the hashes of our clean compiler, of the trojaned one, <bookmark mark='c'/> and of a compiler rebuilt "
            "from the clean source by the trojaned binary. The last two are identical, byte for byte. "
            "<bookmark mark='d'/> Delete the trojan from every source file and it survives in the binary forever, "
            "still letting a secret password into login. By the end of this part we will catch it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(quote))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes))
        self.wait(0.4)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Trusting Trust", font_size=36).to_edge(UP, buff=0.3)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"threat models, \ and Saltzer and Schroeder's principles",
            r"memory corruption, \ ROP, \ and memory safety",
            r"hardware leaks, \ authentication and access control",
            r"isolation, \ the web, \ networks and supply chains",
            r"Thompson's trojan compiler, \ built and caught",
            r"the tower end to end, \ and the open problems",
        ], font_size=25).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 55 of Computer Science, Built, the last part of the degree. <bookmark mark='a'/> We will "
            "set out threat models and the classic design principles; corrupt memory and chain gadgets without "
            "injecting code, then see what memory safety proves; follow leaks through hardware; authenticate, and "
            "find a famous protocol's flaw with a model checker; control access and isolate; break the web, the "
            "network and the supply chain; build Thompson's trojan and catch it; and finally walk the tower, from a "
            "NAND gate to a cluster, one last time."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (BG, DATA, KERN, LAM, NO, YES, HEAD)
