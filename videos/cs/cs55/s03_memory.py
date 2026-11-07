from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs55.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, mono


def cell(text, color, w=2.6, h=0.5):
    """One word on the stack, drawn as a labelled box."""
    box = Rectangle(width=w, height=h, stroke_color=color, stroke_width=1.6, fill_color=BG, fill_opacity=1)
    t = mono(text, size=16, color=color)
    if t.width > w - 0.2:
        t.scale_to_fit_width(w - 0.2)
    t.move_to(box)
    return VGroup(box, t)


class Memory(VoiceoverScene):
    def construct(self):
        self.card()
        self.smash()
        self.defences()
        self.aslr()
        self.rop()
        self.control()

    def card(self):
        card = chapter_card(2, r"Memory corruption, and return-oriented programming",
                            r"What happens when input is longer than its buffer?", lit=(1988, 2007),
                            extra=((1988, r"the Morris worm"), (1996, r"Aleph One"), (2007, r"Shacham: \ ROP")),
                            part=PART)
        with self.voiceover("Chapter two. Memory corruption, and return-oriented programming."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def smash(self):
        head = label(r"The stack smash \ (Part 11, \ on Pebble)", font_size=36).to_edge(UP, buff=0.3)
        frame = VGroup(
            cell(r"buffer[0..63]", DATA, w=3.2),
            cell(r"saved registers", GREY_B, w=3.2),
            cell(r"saved return address", HEAD, w=3.2),
        ).arrange(UP, buff=0.0).move_to([-3.4, 0.2, 0])
        fl = label(r"one call frame", font_size=18, color=GREY_A).next_to(frame, UP, buff=0.2)
        growl = label(r"the stack grows downward", font_size=15, color=GREY_B).next_to(frame, DOWN, buff=0.2)
        inp = VGroup(
            cell(r"A A A A A A A ...", NO, w=3.2),
            cell(r"A A A A A A A ...", NO, w=3.2),
            cell(r"attacker's address", NO, w=3.2),
        ).arrange(UP, buff=0.0).move_to([-3.4, 0.2, 0])
        notes = VGroup(
            wrapped_label(r"the copy routine has no bound \ (C's \texttt{gets}, \ removed from the language in "
                          r"2011): \ it writes past the buffer", 5.6, font_size=20, color=WHITE),
            wrapped_label(r"the overwrite reaches the saved return address; \ \texttt{ret} jumps wherever the input "
                          r"says", 5.6, font_size=20, color=NO),
            wrapped_label(r"point it back into the buffer, \ which holds the attacker's own code: \ the program is "
                          r"theirs", 5.6, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 0.1, 0])
        with self.voiceover(
            "We begin where Part 11 left a loose thread. A function keeps its local variables on the stack: here a "
            "sixty-four byte buffer, some saved registers, and, just above them, the address the function will "
            "return to. <bookmark mark='a'/> Now copy input into the buffer with a routine that has no bound. This is "
            "C's gets, so dangerous it was removed from the language in 2011. <bookmark mark='b'/> Give it more than "
            "sixty-four bytes and it writes straight past the buffer, over the saved registers, and over the saved "
            "return address. When the function returns, it jumps wherever those overwritten bytes point. "
            "<bookmark mark='c'/> Point it back into the buffer, which now holds the attacker's own instructions, and "
            "the program is theirs. This is the overflow the Morris worm used in 1988 and the article by Aleph One "
            "explained in 1996."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(fl), FadeIn(growl))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Transform(frame, inp), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def defences(self):
        rows = load("defences")["rows"]
        head = label(r"Three defences, \ measured on Pebble", font_size=36).to_edge(UP, buff=0.3)
        tick = {"pwned": (r"owned", NO), "fault": (r"blocked", YES), "detected": (r"caught", YES),
                "halted-clean": (r"clean", YES)}
        table = []
        colors = []
        for r in rows:
            out, col = tick[r["outcome"]]
            table.append([r"yes" if r["canary"] else r"--", r"yes" if r["nx"] else r"--",
                          r"yes" if r["aslr"] else r"--", out])
            colors.append([WHITE, WHITE, WHITE, col])
        g = grid_table([r"canary", r"W\^{}X", r"ASLR", r"outcome"], table, widths=[2.0, 2.0, 2.0, 2.4], row_h=0.5,
                       font_size=19, mono_cols=())
        for r, cr in zip(g.cells[1:], colors):
            for c, col in zip(r, cr):
                c.set_color(col)
        g.next_to(head, DOWN, buff=0.4).set_x(-1.6)
        notes = VGroup(
            wrapped_label(r"\textbf{canary}: \ a secret word before the return address; \ the epilogue checks it "
                          r"changed", 4.2, font_size=17, color=HEAD),
            wrapped_label(r"\textbf{W\^{}X}: \ memory is writable or executable, \ never both; \ the stack cannot "
                          r"run as code", 4.2, font_size=17, color=YES),
            wrapped_label(r"\textbf{ASLR}: \ randomise the addresses, \ so a fixed guess usually misses", 4.2,
                          font_size=17, color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.6, 0.0, 0])
        with self.voiceover(
            "Three defences answered this attack, and we ran our Pebble overflow under every combination. "
            "<bookmark mark='a'/> A stack canary is a secret word just before the return address, checked on the "
            "way out; an overflow reaching the return address changes it first. <bookmark mark='b'/> W, xor, X means memory "
            "is writable or executable but never both, so the stack can hold the attacker's bytes but the processor "
            "refuses to run them. <bookmark mark='c'/> And address-space layout randomisation scatters the "
            "addresses, so the one the attacker wrote usually points nowhere. <bookmark mark='d'/> Look at the "
            "table: any one of the three turns a clean takeover into a crash or a caught attempt. The attacker now "
            "needs to beat all three."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(g))
        self.wait(0.4)
        self.clear_scene()

    def aslr(self):
        a = load("aslr")
        ent = a["entropy"]["layouts"]
        ex = a["experiment"]
        head = label(r"How much does randomness buy?", font_size=36).to_edge(UP, buff=0.3)
        r1 = MathTex(r"p", r"=", r"2^{-k}", font_size=44).move_to([0, 1.7, 0])
        r1[2].set_color(DATA)
        why1 = label(r"$k$ random bits: \ $2^{k}$ equally likely placements, \ one right", font_size=20,
                     color=GREY_A).next_to(r1, DOWN, buff=0.3)
        r2 = MathTex(r"E[\text{tries}]", r"=", r"\frac{1}{p}", r"=", r"2^{k}", font_size=44).move_to([0, 1.7, 0])
        r2[4].set_color(HEAD)
        why2 = label(r"re-randomised on each retry: \ a geometric wait of mean $1/p$", font_size=20,
                     color=GREY_A).next_to(r2, DOWN, buff=0.3)
        table = [[L["name"], f"{L['bits']}", f"{L['placements']:,}".replace(",", "{,}")] for L in ent]
        g = grid_table([r"typical layout", r"bits $k$", r"placements $2^{k}$"], table, widths=[4.6, 1.6, 3.4],
                       row_h=0.46, font_size=18, mono_cols=())
        g.next_to(r2, DOWN, buff=1.1).set_x(-0.4)
        src = label(r"bit counts: \ published figures for Linux layouts \ (illustrative; \ they depend on the "
                    r"kernel)", font_size=15, color=GREY_B).next_to(g, DOWN, buff=0.25)
        exp = label(rf"our runnable check: \ {ex['placements']} placements, \ exactly {ex['hit_count']} hit: \ "
                    rf"rate ${ex['hit_count']}/{ex['placements']} = 2^{{-{ex['bits']}}}$", font_size=20,
                    color=YES).next_to(src, DOWN, buff=0.2)
        with self.voiceover(
            "ASLR is a probability, not a wall, so let us do the arithmetic the way Part 27 would. "
            "<bookmark mark='a'/> With k random bits in an address there are two to the k equally likely placements, "
            "and a fixed exploit guesses one, so it succeeds with probability two to the minus k. "
            "<bookmark mark='b'/> If the layout is re-randomised on every attempt, the number of tries to the first "
            "hit is a geometric random variable with mean one over p, which is two to the k. "
            "<bookmark mark='c'/> Here are the published entropies for typical layouts: a thirty-two bit system "
            "gives only sixteen bits on one base, brute-forced in about sixty-five thousand tries, which Shacham and "
            "colleagues did in 2004; a sixty-four bit system gives nearer thirty. <bookmark mark='d'/> And a small "
            "runnable version on Pebble confirms the formula exactly: of sixty-four placements, one matches, a rate "
            "of one in sixty-four."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(r1), FadeIn(why1))
            vo.wait_until("b")
            self.play(TransformMatchingTex(r1, r2), FadeOut(why1), FadeIn(why2))
            vo.wait_until("c")
            self.play(FadeOut(why2), FadeIn(g), FadeIn(src))
            vo.wait_until("d")
            self.play(FadeIn(exp))
        self.wait(0.4)
        self.clear_scene()

    def rop(self):
        d = load("rop")
        chain = d["chain"]
        head = label(r"Return-oriented programming \ (Shacham, 2007)", font_size=36).to_edge(UP, buff=0.3)
        # the signature visual: a train of return addresses on the stack, driving borrowed gadget tails
        train = VGroup(
            cell(r"overflow: A A A ...", NO, w=3.0, h=0.46),
            cell(rf"ret -> restore3  @{chain['restore3']}", HEAD, w=3.0, h=0.46),
            cell(r"console address", DATA, w=3.0, h=0.46),
            cell(r"byte 'p'", DATA, w=3.0, h=0.46),
            cell(rf"ret -> wb  @{chain['wb']}", HEAD, w=3.0, h=0.46),
            cell(rf"ret -> restore3  @{chain['restore3']}", HEAD, w=3.0, h=0.46),
            cell(r"... one per letter ...", GREY_B, w=3.0, h=0.46),
            cell(rf"ret -> halt  @{chain['stop']}", YES, w=3.0, h=0.46),
        ).arrange(DOWN, buff=0.04).move_to([-3.6, -0.3, 0])
        tl = label(r"the stack, \ read upward by each \texttt{ret}", font_size=16, color=GREY_A).next_to(
            train, UP, buff=0.2)
        notes = VGroup(
            wrapped_label(rf"no new code runs: \ the chain reuses {d['n_gadgets']} instruction tails already in the "
                          rf"binary, \ each ending in a return", 5.4, font_size=19, color=WHITE),
            wrapped_label(r"every word is a \textit{code} address \ (a gadget) \ or data it loads; \ each \texttt{ret} "
                          r"starts the next gadget", 5.4, font_size=19, color=HEAD),
            wrapped_label(rf"with W\^{{}}X on, \ the chain still prints ``{d['nx']['output']}'' and halts: \ it ran no "
                          r"stack code at all", 5.4, font_size=19, color=NO),
            wrapped_label(r"but a canary still catches the overwrite first \ ($\Rightarrow$ ``caught''): \ ROP needs a "
                          r"leak elsewhere", 5.4, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([3.5, -0.1, 0])
        with self.voiceover(
            "W, xor, X stops injected code. In 2007 Hovav Shacham showed it does not stop the attacker. "
            "<bookmark mark='a'/> Instead of new code, reuse code already there: short instruction sequences that "
            "end in a return, called gadgets. <bookmark mark='b'/> The overflow now writes a train of return "
            "addresses on the stack. Each return jumps to a gadget, which does a little work and returns into the "
            "next. <bookmark mark='c'/> Our Pebble binary has eight gadgets, and a chain of them makes the program "
            "print its word and halt with W, xor, X fully on. No stack code ever ran. <bookmark mark='d'/> The "
            "canary still trips first, which is why real chains also need a leak. The lesson: control flow is the "
            "asset to defend."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in train], lag_ratio=0.18), FadeIn(notes[1]),
                      run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def control(self):
        head = label(r"Guarding control flow", font_size=36).to_edge(UP, buff=0.3)
        tiles = VGroup()
        for name, body, col in [
            (r"CFI", r"control-flow integrity: \ at each indirect jump or return, \ check the target is one the "
                     r"program was \textit{compiled} to allow \ (Abadi et al., 2005)", HEAD),
            (r"shadow stack", r"keep return addresses on a second, \ protected stack; \ compare on return \ (now in "
                              r"hardware)", YES),
            (r"CHERI", r"make pointers hardware \textit{capabilities}, \ carrying bounds and permissions; \ a forged "
                       r"or out-of-bounds pointer simply cannot be formed", DATA),
        ]:
            box = RoundedRectangle(width=4.0, height=3.0, corner_radius=0.15, stroke_color=col, stroke_width=2,
                                   fill_color=BG, fill_opacity=1)
            t = label(name, font_size=24, color=col)
            b = wrapped_label(body, 3.6, font_size=17, color=GREY_A)
            VGroup(t, b).arrange(DOWN, buff=0.25).move_to(box)
            tiles.add(VGroup(box, t, b))
        tiles.arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.6)
        foot = wrapped_label(r"each raises the attacker's work; \ none ends the war: \ Chapter 3 asks whether the "
                             r"language could rule the bug out instead", 12.6, font_size=21,
                             color=WHITE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "So defend control flow directly. <bookmark mark='a'/> Control-flow integrity, from Martin Abadi and "
            "colleagues in 2005, checks at each indirect jump or return that the target is one the compiler "
            "allowed; a chain that lands mid-gadget fails. <bookmark mark='b'/> A shadow stack keeps a protected copy "
            "of every return address, now in hardware. <bookmark mark='c'/> CHERI makes each pointer a capability "
            "carrying its bounds, so a forged pointer cannot be built. <bookmark mark='d'/> Each raises the cost; "
            "none ends the war. Could the language make the bug impossible?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, t in zip("abc", tiles):
                vo.wait_until(mk)
                self.play(FadeIn(t, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES, PART)
