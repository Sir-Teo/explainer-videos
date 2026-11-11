from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs55.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, mono


def cbox(text, color, w=None, h=0.5, size=18):
    """A labelled rounded box."""
    t = label(text, font_size=size, color=WHITE)
    w = w or t.width + 0.35
    r = RoundedRectangle(width=w, height=h, corner_radius=0.07, stroke_color=color, stroke_width=1.8,
                         fill_color=BG, fill_opacity=1)
    if t.width > w - 0.12:
        t.width = w - 0.12
    t.move_to(r)
    return VGroup(r, t)


def binary_box(name, stage, color, w=3.2):
    """A binary as a box: a name, then its size and hash prefix from the instrument."""
    t = label(name, font_size=18, color=WHITE)
    h = mono(f"{stage['size']:,} B  {stage['sha256'][:8]}", size=16, color=color)
    g = VGroup(t, h).arrange(DOWN, buff=0.08)
    r = RoundedRectangle(width=max(w, g.width + 0.3), height=g.height + 0.25, corner_radius=0.08,
                         stroke_color=color, stroke_width=2, fill_color=BG, fill_opacity=1)
    g.move_to(r)
    return VGroup(r, g)


def arrow(a, b, color=GREY_B, width=2.4):
    return Arrow(a, b, buff=0.08, stroke_width=width, color=color, max_tip_length_to_length_ratio=0.2,
                 max_stroke_width_to_length_ratio=10)


class Ddc(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.derive()
        self.clean()
        self.trojaned()
        self.repro()
        self.seed()

    def card(self):
        card = chapter_card(12, r"Catching the trojan", r"How can you check a binary against its source?",
                            lit=(2005, 2009, 2013), extra=((2005, r"Wheeler: \ DDC"), (2009, r"Wheeler's thesis"),
                                                           (2013, r"reproducible builds")),
                            part=PART, layers=("lang", "practice"))
        with self.voiceover("Chapter twelve. Catching the trojan."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def idea(self):
        head = label(r"A second, \ independent compiler", font_size=36).to_edge(UP, buff=0.3)
        a = cbox(r"$A$: \ the compiler binary under suspicion", NO, w=5.4, h=0.7, size=20).move_to([-3.4, 0.55, 0])
        t = cbox(r"$T$: \ an independent compiler", YES, w=5.4, h=0.7, size=20).move_to([3.4, 0.55, 0])
        c = cbox(r"$c$: \ the compiler's source, \ which we can read", DATA, w=6.4, h=0.7, size=20).move_to(
            [0, 2.0, 0])
        la = arrow(c.get_bottom() + LEFT * 1.5, a.get_top(), GREY_B)
        lt = arrow(c.get_bottom() + RIGHT * 1.5, t.get_top(), GREY_B)
        na = wrapped_label(r"the trojan, \ if any, \ recognises compilers and copies itself \ --- \ but only inside "
                           r"$A$", 5.4, font_size=19, color=NO).next_to(a, DOWN, buff=0.25)
        nt = wrapped_label(r"written separately, \ sharing no code with $A$; \ it may be slow, \ or old, \ and need "
                           r"not be perfect", 5.4, font_size=19, color=YES).next_to(t, DOWN, buff=0.25)
        for n, box in ((na, a), (nt, t)):
            n.align_to(box, LEFT)
        ours = wrapped_label(r"ours: \ a reference compiler that never looks at what it compiles, \ so it cannot "
                             r"carry a trojan that recognises compilers", 12.4, font_size=20,
                             color=WHITE).next_to(VGroup(na, nt), DOWN, buff=0.55)
        key = wrapped_label(r"the assumption: \ $A$ and $T$ are not trojaned \textit{in the same way}", 12.4,
                            font_size=22, color=HEAD).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "In 2005 David Wheeler published the answer, and in 2009 his thesis proved it. "
            "<bookmark mark='a'/> Keep the binary you suspect, A, and the compiler's source, c, which you can read. "
            "<bookmark mark='b'/> Add a second compiler, T, written independently. It may be slow, or old, or "
            "imperfect; it need not be trusted in general. <bookmark mark='c'/> Ours is a reference compiler that "
            "never inspects what it compiles, so it cannot carry a trojan that recognises compilers. "
            "<bookmark mark='d'/> The one assumption is that A and T are not trojaned in the same way: the trojan "
            "would have to be in both."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(c), GrowArrow(la), FadeIn(na))
            vo.wait_until("b")
            self.play(FadeIn(t), GrowArrow(lt), FadeIn(nt))
            vo.wait_until("c")
            self.play(FadeIn(ours))
            vo.wait_until("d")
            self.play(FadeIn(key))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        head = label(r"Diverse double-compiling", font_size=36).to_edge(UP, buff=0.3)
        s1 = MathTex(r"X", r"=", r"T(c)", font_size=42)
        s2 = MathTex(r"Z", r"=", r"X(c)", font_size=42)
        s3 = MathTex(r"Z", r"=", r"X(c)", r"=", r"A(c)", font_size=42)
        s4 = MathTex(r"Z", r"=", r"A(c)", r"=", r"A", font_size=42)
        s1.move_to([-2.5, 1.9, 0])
        s2.move_to([-2.5, 0.75, 0])
        for s in (s3, s4):
            s.move_to([-2.5, -0.4, 0])
        w1 = label(r"stage 1: \ compile the source with $T$", font_size=19, color=GREY_A)
        w2 = label(r"stage 2: \ compile the source again, \ with $X$", font_size=19, color=GREY_A)
        w3 = label(r"if $A$ honestly comes from $c$, \ $X$ and $A$ do the same thing: \ same output", font_size=19,
                   color=GREY_A)
        w4 = label(r"a self-hosting compiler compiles its own source into itself", font_size=19, color=GREY_A)
        for w, s in zip((w1, w2), (s1, s2)):
            w.next_to(s, RIGHT, buff=0.6)
        for w in (w3, w4):
            w.next_to(s3, DOWN, buff=0.2).set_x(-0.5)
        test = MathTex(r"Z", r"\overset{?}{=}", r"A", r"\quad\text{bit for bit}", font_size=44, color=HEAD)
        test.move_to([0, -2.0, 0])
        box = SurroundingRectangle(test, color=HEAD, buff=0.2, corner_radius=0.1)
        tl = label(r"equal: \ $A$ corresponds to its source. \ different: \ $A$ does not", font_size=20,
                   color=HEAD).next_to(box, DOWN, buff=0.2)
        with self.voiceover(
            "The procedure has two stages. <bookmark mark='a'/> Stage one: compile the source c with the independent "
            "compiler, giving a new compiler binary X. Its bytes will differ from A's, because different compilers "
            "write different code. <bookmark mark='b'/> Stage two: compile c again, this time with X, giving Z. "
            "<bookmark mark='c'/> Now suppose A really was compiled from c. Then X and A were built from the same "
            "source and do the same thing, so they give the same output on the same input: Z equals A of c. "
            "<bookmark mark='d'/> And a compiler compiling its own source reproduces itself, so A of c is A. "
            "<bookmark mark='e'/> The test is to compare Z with A, bit for bit."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(s1), FadeIn(w1))
            vo.wait_until("b")
            self.play(Write(s2), FadeIn(w2))
            vo.wait_until("c")
            self.play(TransformMatchingTex(s2.copy(), s3), FadeIn(w3))
            vo.wait_until("d")
            self.play(TransformMatchingTex(s3, s4), FadeTransform(w3, w4))
            vo.wait_until("e")
            self.play(Write(test), Create(box))
            self.play(FadeIn(tl))
        self.wait(0.4)
        self.clear_scene()

    def build_panel(self, case, suspect_name):
        """The two columns of a DDC run: the suspect binary, stage 1 and stage 2 under each compiler."""
        d = load("ddc")[case]
        xs, xt = -3.3, 3.3
        bad = not d["match"]
        hs = label(r"with the suspect binary $A$", font_size=20, color=NO if bad else GREY_A).move_to([xs, 2.4, 0])
        ht = label(r"with the independent compiler $T$", font_size=20, color=YES).move_to([xt, 2.4, 0])
        a1 = binary_box(r"stage 1: \ $A(c)$", d["stage1_suspect"], NO if bad else GREY_A).move_to([xs, 1.35, 0])
        t1 = binary_box(r"stage 1: \ $X = T(c)$", d["stage1_trusted"], YES).move_to([xt, 1.35, 0])
        a2 = binary_box(r"stage 2: \ $A(c)$ compiles $c$", d["stage2_suspect"], NO if bad else GREY_A).move_to(
            [xs, -0.25, 0])
        t2 = binary_box(r"stage 2: \ $Z = X(c)$", d["stage2_trusted"], YES).move_to([xt, -0.25, 0])
        d1 = arrow(a1.get_bottom(), a2.get_top())
        d2 = arrow(t1.get_bottom(), t2.get_top())
        same1 = d["stage1_suspect"]["sha256"] == d["stage1_trusted"]["sha256"]
        n1 = label(r"stage 1 differs: \ different compilers, \ different bytes" if not same1 else r"stage 1 matches",
                   font_size=17, color=GREY_B).move_to([0, 0.55, 0])
        cmp = DoubleArrow(a2.get_right(), t2.get_left(), buff=0.12, color=HEAD if not bad else NO, stroke_width=3,
                          tip_length=0.2)
        verdict = r"match: \ clean" if d["match"] else r"mismatch: \ TROJAN DETECTED"
        v = label(verdict, font_size=30, color=YES if d["match"] else NO).move_to([0, -1.55, 0])
        susp = label(suspect_name, font_size=18, color=GREY_A).next_to(v, DOWN, buff=0.25)
        return d, VGroup(hs, ht), VGroup(a1, t1), VGroup(d1, d2), VGroup(a2, t2), n1, cmp, VGroup(v, susp)

    def clean(self):
        head = label(r"DDC on an honest compiler", font_size=36).to_edge(UP, buff=0.3)
        st = load("trojan")["stages"]
        d, hd, s1, ar, s2, n1, cmp, vv = self.build_panel(
            "clean", rf"$A$ = our clean compiler binary, \ {st[0]['sha256'][:8]}")
        head.to_edge(UP, buff=0.25)
        hd.shift(DOWN * 0.15)
        foot = wrapped_label(r"in our runs the suspect's own stage-2 binary is $A$ itself: \ the compiler is "
                             r"self-reproducing", 12.4, font_size=19, color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "First, run it on an honest compiler. <bookmark mark='a'/> In stage one, the suspect produces "
            "four hundred and ninety-nine bytes, the independent compiler four hundred and ninety-eight, with "
            "different hashes. That is expected: two compilers, two ways of writing the same program. "
            "<bookmark mark='b'/> In stage two, both of those binaries compile the same source, <bookmark mark='c'/> "
            "and the results are identical, bit for bit, and identical to A. <bookmark mark='d'/> The verdict: A "
            "really is what its source says."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hd))
            vo.wait_until("a")
            self.play(FadeIn(s1), FadeIn(n1))
            vo.wait_until("b")
            self.play(GrowArrow(ar[0]), GrowArrow(ar[1]), FadeIn(s2))
            vo.wait_until("c")
            self.play(GrowArrow(cmp))
            vo.wait_until("d")
            self.play(FadeIn(vv), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def trojaned(self):
        head = label(r"DDC on Thompson's compiler", font_size=36).to_edge(UP, buff=0.25)
        st = load("trojan")["stages"]
        d, hd, s1, ar, s2, n1, cmp, vv = self.build_panel(
            "trojaned", rf"$A$ = the trojaned compiler binary of Chapter 11, \ {st[1]['sha256'][:8]}")
        hd.shift(DOWN * 0.15)
        why = wrapped_label(r"$T$ never inserts the trojan, \ so $X$ is an honest compiler, \ and $Z$ is the honest "
                            r"binary: \ the trojan has nowhere to hide", 12.4, font_size=20,
                            color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now the binary from the last chapter. <bookmark mark='a'/> Stage one: the suspect, compiling the clean "
            "source, inserts its trojan, and gives eleven hundred and nineteen bytes; the independent compiler gives "
            "an honest four hundred and ninety-eight. <bookmark mark='b'/> Stage two: the suspect's lineage reproduces "
            "the trojan again, while X, an honest compiler built by an honest compiler, produces the honest "
            "binary. <bookmark mark='c'/> They differ. <bookmark mark='d'/> Trojan detected. The trojan could fool "
            "any amount of reading, but it cannot be in a compiler it never touched."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hd))
            vo.wait_until("a")
            self.play(FadeIn(s1), FadeIn(n1))
            vo.wait_until("b")
            self.play(GrowArrow(ar[0]), GrowArrow(ar[1]), FadeIn(s2))
            vo.wait_until("c")
            self.play(GrowArrow(cmp))
            vo.wait_until("d")
            self.play(FadeIn(vv))
            self.play(Indicate(vv[0], color=NO))
            self.play(FadeIn(why))
        self.wait(0.4)
        self.clear_scene()

    def repro(self):
        r = load("repro")
        head = label(r"Bit for bit needs reproducible builds", font_size=36).to_edge(UP, buff=0.3)
        hdrs = [("BUILD ts=1700000000 path=/home/alice/build", "BUILD ts=1700009999 path=/tmp/bob/build"),
                ("BUILD ts=0 path=/build", "BUILD ts=0 path=/build")]

        def row(title, key, pair, y, col):
            t = label(title, font_size=21, color=col).move_to([0, y + 0.55, 0])
            res = r[key]
            lines = VGroup()
            for who, h, sha in ((r"Alice", pair[0], res["sha_a"]), (r"Bob", pair[1], res["sha_b"])):
                lines.add(VGroup(label(who, font_size=18, color=GREY_A), mono(h, size=16, color=WHITE),
                                 mono(sha[:16], size=16, color=col)).arrange(RIGHT, buff=0.35))
            lines.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([0, y - 0.25, 0])
            for ln in lines:
                ln[2].move_to([5.4, ln.get_y(), 0])
            v = label(r"identical" if res["identical"] else r"different", font_size=20,
                      color=YES if res["identical"] else NO).next_to(lines, DOWN, buff=0.15).align_to(lines[0][2],
                                                                                                       LEFT)
            return VGroup(t, lines, v)
        top = row(r"the same source, \ built by two people, \ as is", "unnormalized", hdrs[0], 1.65, NO)
        bot = row(r"with the time and the path fixed", "normalized", hdrs[1], -0.75, YES)
        cap = label(r"each build stamps a header, \ then appends the compiled \texttt{login}; \ hashes from our "
                    r"instrument", font_size=17, color=GREY_B).next_to(bot, DOWN, buff=0.3)
        foot = wrapped_label(r"since 2013, \ Tor and Debian have led the work to make real builds reproducible: \ fixed "
                             r"timestamps \ (\texttt{SOURCE\_DATE\_EPOCH}), \ sorted file lists, \ no build paths",
                             12.4, font_size=19, color=WHITE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Comparing bit for bit assumes a build gives the same bits every time, and real builds often do not. "
            "<bookmark mark='a'/> Our toy build stamps the time and the directory into its header, so Alice and "
            "Bob, building the same source, get different hashes, and a comparison proves nothing. "
            "<bookmark mark='b'/> Fix the time and the path, and the two builds are identical. <bookmark mark='c'/> "
            "Since 2013 the Tor and Debian projects have led the work of making real builds reproducible: fixed "
            "timestamps, sorted file lists, no build paths. A reproducible build lets anyone rebuild a release and "
            "check it, which also checks that a release matches the public source, the very gap xz exploited."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(top))
            vo.wait_until("b")
            self.play(FadeIn(bot), FadeIn(cap))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def seed(self):
        head = label(r"Growing trust from a seed", font_size=36).to_edge(UP, buff=0.3)
        rungs = [(r"a seed of a few hundred bytes, \ written in hex, \ small enough to read", YES),
                 (r"a tiny assembler, \ built by the seed", YES),
                 (r"a minimal C compiler, \ built by the assembler", DATA),
                 (r"TinyCC, \ built by that", DATA),
                 (r"an early GCC", LAM),
                 (r"a modern GCC, \ and the whole distribution", KERN)]
        boxes = VGroup(*[cbox(t, c, w=6.6, h=0.5, size=18) for t, c in rungs]).arrange(UP, buff=0.36)
        boxes.move_to([-2.9, -0.35, 0])
        arrs = VGroup(*[Arrow(boxes[i].get_top(), boxes[i + 1].get_bottom(), buff=0.02, stroke_width=2.4, color=GREY_B,
                              max_tip_length_to_length_ratio=0.5) for i in range(len(boxes) - 1)])
        cite = label(r"simplified: \ the bootstrappable-builds work, \ GNU Mes, \ and GNU Guix's full-source "
                     r"bootstrap \ (2023)", font_size=16, color=GREY_B).to_edge(DOWN, buff=0.3)
        side = VGroup(
            wrapped_label(r"\textbf{DDC proves:} \ this binary is what this source says", 5.2, font_size=19,
                          color=YES),
            wrapped_label(r"\textbf{it assumes:} \ the second compiler is not trojaned the same way; \ use several, \ "
                          r"of different origins", 5.2, font_size=19, color=HEAD),
            wrapped_label(r"\textbf{it cannot prove:} \ that the source is honest \ --- \ xz's backdoor was written by "
                          r"one of its own maintainers", 5.2, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.9, 0.0, 0])
        with self.voiceover(
            "Where does the trusted compiler come from? <bookmark mark='a'/> The bootstrapping projects answer by "
            "growing one from a seed: a program of a few hundred bytes, written in hexadecimal, small enough for a "
            "person to read. It builds a tiny assembler, which builds a minimal C compiler, then a small real one, "
            "then an early GCC, and finally the modern toolchain. GNU Guix announced such a full-source bootstrap "
            "in 2023. <bookmark mark='b'/> Diverse double-compiling then proves that a binary is what its source "
            "says. It assumes that the second compiler is not trojaned the same way, so use several of different "
            "origins. <bookmark mark='c'/> And it cannot prove the source honest: someone must still read it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(b, shift=UP * 0.1), *([GrowArrow(arrs[i - 1])] if i else []))
                                    for i, b in enumerate(boxes)], lag_ratio=0.6), run_time=6)
            self.play(FadeIn(cite))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
