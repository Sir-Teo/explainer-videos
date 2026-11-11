from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs11.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, load, region)


class Smash(VoiceoverScene):
    def construct(self):
        self.card()
        self.frame()
        self.attack()
        self.defences()

    def card(self):
        card = chapter_card(14, r"Smashing the stack", r"How does an input become code?", lit=(1988, 1996),
                            extra=((1988, r"the Morris worm"), (1996, r"Aleph One: \ ``Smashing the stack''")),
                            part=PART)
        with self.voiceover("Chapter fourteen. Smashing the stack."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def frame(self):
        sm = load("smash")
        head = label(r"\texttt{greet}'s frame, \ on Pebble", font_size=34).to_edge(UP, buff=0.3)
        lst = code(["greet:  addi sp, sp, -80", "        sw   ra, 76(sp)      # the way home", "        mv   a0, sp",
                    "        call gets           # copies until a newline: no bound", "        ... print hello, buffer",
                    "        lw   ra, 76(sp)", "        addi sp, sp, 80", "        ret                 # go home"],
                   size=17).to_edge(LEFT, buff=0.5).shift(UP * 0.2)
        buf = region(2.6, 2.4, r"buffer: \ 64 bytes", DATA, font_size=19)
        gap = region(2.6, 0.5, r"12 bytes unused", GREY_B, font_size=16, fill=0.08)
        ra = region(2.6, 0.45, r"saved \texttt{ra}", NO, font_size=18)
        caller = region(2.6, 0.7, r"\texttt{\_start}'s frame", GREY_C, font_size=16, fill=0.08)
        stack = VGroup(caller, ra, gap, buf).arrange(DOWN, buff=0).to_edge(RIGHT, buff=2.0).shift(DOWN * 0.1)
        sp = VGroup(Arrow(LEFT * 0.6, ORIGIN, buff=0, color=HEAD, stroke_width=3),
                    label(rf"sp $=$ \texttt{{{sm['buffer']:#x}}}", font_size=17, color=HEAD)).arrange(LEFT, buff=0.1)
        sp.next_to(buf, LEFT, buff=0.1).align_to(buf, DOWN)
        uparr = Arrow(buf.get_right() + RIGHT * 0.35 + DOWN * 0.8, ra.get_right() + RIGHT * 0.35, color=GREY_B,
                      buff=0.05)
        up = label(r"the copy runs \\ upward", font_size=17, color=GREY_B).next_to(uparr, RIGHT, buff=0.12)
        with self.voiceover(
            "Here is the greeting program from the start of this part, on Pebble. <bookmark mark='a'/> greet makes "
            "an eighty-byte frame. At the bottom, a sixty-four-byte buffer for the name; near the top, the saved "
            "return address, the way back to the caller. <bookmark mark='b'/> It passes the buffer to gets, which, "
            "like C's gets, copies input until it sees a newline, however long that is. <bookmark mark='c'/> The "
            "copy runs upward, from the bottom of the buffer towards the saved return address. So a name longer than "
            "seventy-six bytes reaches it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lst))
            vo.wait_until("a")
            self.play(FadeIn(stack), FadeIn(sp))
            vo.wait_until("b")
            self.play(Indicate(lst[3], color=NO))
            vo.wait_until("c")
            self.play(GrowArrow(uparr), FadeIn(up))
        self.wait(0.3)
        self.clear_scene()

    def attack(self):
        from explainer.cs.pebble import assemble

        sm = load("smash")
        nb = len(assemble(sm["shellcode"]).image)
        pad = sm["ra_off"] - nb
        head = label(r"The attack: \ 81 bytes", font_size=34).to_edge(UP, buff=0.3)
        shell = code([l for l in sm["shellcode"].strip().splitlines()][:6] + ["        ...", "        halt"],
                     size=15).to_edge(LEFT, buff=0.5).shift(UP * 0.3)
        sl = label(rf"machine code that prints ``pwned'': \ {nb} bytes", font_size=18, color=NO).next_to(shell, UP,
                                                                                                   buff=0.15)
        parts = VGroup(region(4.2, 0.6, rf"code \ ({nb} bytes)", NO, font_size=18),
                       region(1.3, 0.6, rf"AAAA \ ({pad})", GREY_B, font_size=16),
                       region(2.2, 0.6, rf"\texttt{{{sm['buffer']:#x}}}", HEAD, font_size=17),
                       region(0.9, 0.6, r"\texttt{\textbackslash n}", GREY_C, font_size=16)).arrange(RIGHT, buff=0)
        parts.to_edge(RIGHT, buff=0.4).shift(UP * 1.3)
        brace = VGroup(Brace(VGroup(parts[0], parts[1]), DOWN, color=DATA),
                       label(r"fills buffer and gap: \ 76 bytes", font_size=16, color=DATA))
        brace[1].next_to(brace[0], DOWN, buff=0.05)
        b2 = VGroup(Brace(parts[2], DOWN, color=HEAD), label(r"lands on \texttt{ra}: \\ the buffer's own address",
                                                             font_size=16, color=HEAD))
        b2[1].next_to(b2[0], DOWN, buff=0.05)
        steps = VGroup(
            label(r"\texttt{gets} copies all of it", font_size=21, color=GREY_A),
            label(r"\texttt{greet} prints hello, \ restores \texttt{ra} from the stack \dots \ and returns into the "
                  r"buffer", font_size=21, color=NO),
            label(r"output: \ \texttt{hello, \dots pwned}", font_size=23, color=NO),
            label(r"the address is known in advance: \ nothing randomizes Pebble's stack", font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.4).to_edge(RIGHT, buff=0.4)
        with self.voiceover(f"So here is the attack. <bookmark mark='a'/> Its first part is code: {nb // 4} Pebble instructions that print the letters p w n e d and stop, {nb} bytes. <bookmark mark='b'/> Then {pad} bytes of padding, to fill the rest of the buffer and the gap: seventy-six bytes so far. <bookmark mark='c'/> Then four bytes that land exactly on the saved return address: the address of the buffer itself. <bookmark mark='d'/> gets copies all of it. greet prints its greeting, restores the return address from the stack, which is now ours, and returns, into the buffer, where our code runs. <bookmark mark='e'/> On the emulator it prints pwned. The attacker needed one fact, where the stack is, and on a machine with no randomization that never changes. This is how the Morris worm spread through the internet's fingerd servers in 1988, and Aleph One's 1996 article, Smashing the Stack for Fun and Profit, taught it to everyone.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(shell), FadeIn(sl), FadeIn(parts[0]), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(parts[1]), FadeIn(brace))
            vo.wait_until('c')
            self.play(FadeIn(parts[2]), FadeIn(parts[3]), FadeIn(b2))
            vo.wait_until('d')
            self.play(FadeIn(steps[0]), FadeIn(steps[1]))
            vo.wait_until('e')
            self.play(FadeIn(steps[2]), FadeIn(steps[3]))
        self.wait(0.3)
        self.clear_scene()

    def defences(self):
        sm = load("smash")
        fr = load("frontier")
        head = label(r"Four defences, \ each run on the same attack", font_size=32).to_edge(UP, buff=0.3)
        rows = [
            (r"a stack canary", r"a secret word below \texttt{ra}, \ checked before \texttt{ret}",
             sm["canary"]["output"].strip().splitlines()[-1], YES),
            (r"a no-execute stack", r"the stack's pages may be written \\ but not run",
             (sm["nx"]["fault"] or "").split(":")[-1].strip(), YES),
            (r"randomization", r"the stack moves every run: \\ the address is a guess", r"(chapter 12)", CTRL),
            (r"bounds on pointers", r"every store checked against \\ its object's bounds", r"the Frontier chapter",
             FUNC),
        ]
        g = VGroup()
        for name, how, res, c in rows:
            g.add(VGroup(label(name, font_size=22, color=c), label(how, font_size=19, color=GREY_A),
                         Text(res[:40], font="DejaVu Sans Mono", font_size=15, color=c)))
        for r in g:
            r[0].move_to([-4.6, 0, 0], aligned_edge=LEFT)
            r[1].move_to([-1.0, 0, 0], aligned_edge=LEFT)
            r[2].move_to([3.3, 0, 0], aligned_edge=LEFT)
        g.arrange(DOWN, buff=0.45).move_to(DOWN * 0.2)
        for r in g:
            r[0].align_to([-6.3, 0, 0], LEFT)
            r[1].align_to([-2.9, 0, 0], LEFT)
            r[2].align_to([1.8, 0, 0], LEFT)
        hdr = VGroup(label(r"defence", font_size=18, color=GREY_B).move_to([-5.5, 0, 0]),
                     label(r"how", font_size=18, color=GREY_B).move_to([-1.6, 0, 0]),
                     label(r"what Pebble did", font_size=18, color=GREY_B).move_to([3.0, 0, 0])).next_to(g, UP, buff=0.3)
        rop = label(r"attackers answered with \textit{return-oriented programming}: \ reuse code already there \ "
                    r"(Part 55)", font_size=20, color=NO).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            (
            "Modern toolchains offer several defenses, with coverage determined by the build and platform. Our "
            "Pebble variants illustrate their mechanisms. <bookmark mark='a'/> A canary checked before return can "
            "detect this contiguous overwrite, provided the attacker cannot reproduce the expected value. It does "
            "not protect every memory access. <bookmark mark='b'/> A non-executable stack stops this attempt to "
            "execute injected stack bytes. It does not stop the overwrite itself. <bookmark mark='c'/> ASLR makes "
            "the injected destination harder to predict; it needs sufficient entropy and resistance to leaks. "
            "<bookmark mark='d'/> A bounds-carrying pointer can reject the first write outside this buffer; the "
            "Frontier adds a miniature check. <bookmark mark='e'/> These defenses address different failure "
            "modes. Code-reuse attacks can use executable fragments already present, including return-oriented "
            "programming. Layered mitigation complements bounds and lifetime safety; no universal claim that "
            "every binary enables all of these is warranted."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(rop))
        self.wait(0.3)
        self.clear_scene()
