from __future__ import annotations

from videos.philosophy.philosophy24.common import *  # noqa: F403


class Chance(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Chance and the big bad bug", r"What makes a chance true?", lit=(1980, 1994),
                            part=PART)
        with self.voiceover("Chapter four. Chance, and the big bad bug."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.principle()
        self.humean()
        self.undermining()
        self.bug()
        self.repair()

    def principle(self):
        hc = history_card(1980, r"David Lewis", r"`A Subjectivist's Guide to Objective Chance'", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        f = MathTex(r"C\big(A \;\big|\; \text{ch}_t(A) = x \,\wedge\, E\big) = x", font_size=44,
                    color=CHANCE).move_to([0, 0.9, 0])
        note = MathTex(r"\text{for any admissible } E", font_size=28, color=GREY_A).next_to(f, DOWN, buff=0.25)
        rows = stack([(r"$C$: \ a rational initial credence \ (Part 13); \ $\text{ch}_t$: \ the chance at time $t$",
                       WHITE),
                      (r"admissible: \ the history up to $t$, \ and the theory of chance; \ not a crystal ball", ABS),
                      (r"what we know about chance is that credence should follow it", GOAL)], font_size=22,
                     aligned_edge=LEFT, width=11.0, buff=0.3).move_to([0, -1.6, 0])
        with self.voiceover(
            "Laws in physics are often probabilistic, so a theory of law needs a theory of chance. "
            "<bookmark mark='a'/>Lewis's Principal Principle says how chance and belief connect. Your credence in A, "
            "given that the chance of A at time t is x, and given any further admissible evidence E, should be x. "
            "<bookmark mark='b'/>C is a rational initial credence, of the kind Part 13 built; ch sub t is the chance "
            "at time t. <bookmark mark='c'/>Admissible evidence is the history up to t, and the theory of how "
            "chances work; a crystal ball showing the coin's outcome is not admissible. <bookmark mark='d'/>Lewis "
            "thought the principle captures everything we know about chance: whatever chance is, it is what "
            "credence should follow."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(note))
            for mk, r in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def humean(self):
        head = label(r"Humean chance", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        seq = "HTTHHTHTTH" + "??????????"
        boxes = VGroup()
        for i, ch in enumerate(seq):
            c = CHANCE if ch == "H" else (LAW if ch == "T" else GREY_C)
            sq = Square(side_length=0.5, color=c, fill_color=c, fill_opacity=0.25 if ch != "?" else 0.05,
                        stroke_width=2)
            sq.move_to([-5.2 + i * 0.55, 1.2, 0])
            t = MathTex(ch if ch != "?" else r"?", font_size=24, color=c).move_to(sq)
            boxes.add(VGroup(sq, t))
        past = Brace(VGroup(*boxes[:10]), DOWN, color=GREY_B)
        pastl = label(r"the past: \ 10 tosses, \ 5 heads", font_size=19, color=GREY_A).next_to(past, DOWN,
                                                                                            buff=0.1)
        fut = Brace(VGroup(*boxes[10:]), DOWN, color=GREY_B)
        futl = label(r"the future: \ 10 more", font_size=19, color=GREY_A).next_to(fut, DOWN, buff=0.1)
        rows = stack([(r"Lewis: \ chances supervene on the mosaic, \ like laws", WHITE),
                      (r"the best system adds a third virtue: \ fit, \ the probability it gives the actual history",
                       ABS),
                      (r"in a world of coin tosses, \ the best system says $\text{ch}(H) = $ the frequency of heads "
                       r"in the whole history", CHANCE),
                      (r"suppose the whole history has frequency $\tfrac12$: \ then $\text{ch}(H) = \tfrac12$", OK)],
                     font_size=21, aligned_edge=LEFT, width=11.6, buff=0.28).move_to([0, -1.7, 0])
        with self.voiceover(
            "Lewis wanted chances to be Humean, like laws: nothing over and above the mosaic. "
            "<bookmark mark='a'/>The best system gets a third virtue besides simplicity and strength: fit, the "
            "probability the system gives to what actually happens. <bookmark mark='b'/>Picture a world that "
            "contains nothing but coin tosses: twenty of them, ten in the past and ten still to come. "
            "<bookmark mark='c'/>The best system for such a world says that the chance of heads is the frequency of "
            "heads over the whole history, past and future. <bookmark mark='d'/>Suppose the whole history has "
            "exactly ten heads. Then the chance of heads is one half, and what makes that true is the pattern, "
            "including the part of the pattern that has not happened yet."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.05), GrowFromCenter(past),
                      FadeIn(pastl), GrowFromCenter(fut), FadeIn(futl))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def undermining(self):
        d = load("undermine")
        head = label(r"Undermining futures", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 11.8, 1], y_range=[0, 0.3, 0.1], x_length=7.4, y_length=3.6,
                  axis_config={"color": GREY_B, "font_size": 18}, x_axis_config={"include_ticks": False},
                  y_axis_config={"include_numbers": True}).move_to([-2.4, -0.6, 0])
        nums = VGroup(*[MathTex(str(k), font_size=20, color=GREY_A).next_to(ax.c2p(k + 0.8, 0), DOWN, buff=0.12)
                        for k in range(11)])
        xl = label(r"heads in the next 10 tosses", font_size=18, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.5)
        yl = label(r"chance, \ if $\text{ch}(H) = \tfrac12$", font_size=18, color=GREY_A).next_to(ax.y_axis, UP,
                                                                                                buff=0.1)
        yl.align_to(ax, LEFT)
        bars = VGroup()
        for r in d["rows"]:
            k, p = r["future_heads"] + 0.8, r["chance"]
            c = BAD if r["undermines"] else OK
            bars.add(Polygon(ax.c2p(k - 0.35, 0), ax.c2p(k + 0.35, 0), ax.c2p(k + 0.35, p), ax.c2p(k - 0.35, p),
                             stroke_width=0, fill_color=c, fill_opacity=0.8))
        und = d["undermining_chance"]
        side = stack([(r"exactly 5 more heads: \ the frequency stays $\tfrac12$", OK),
                      (r"any other future: \ the frequency, \ and so the chance, \ would differ", BAD),
                      (rf"their total chance: \ {und:.3f}", BAD),
                      (r"the chance theory gives most of its probability to futures in which it is false", GOAL)],
                     font_size=21, aligned_edge=LEFT, width=4.8).move_to([4.4, -0.4, 0])
        assert 0.75 < und < 0.76
        with self.voiceover(
            "Now look ahead. <bookmark mark='a'/>Given the chance of one half, each possible future of ten tosses "
            "has a chance: the binomial distribution. <bookmark mark='b'/>If exactly five more heads come up, the "
            "frequency stays at one half, and so does the chance. <bookmark mark='c'/>But in any other future, the "
            "whole history would have a different frequency, and so, by Lewis's own account, a different chance. "
            "These are undermining futures: had they happened, the present chance would not have been one half. "
            "<bookmark mark='d'/>The Reasoner adds up their chance: about seventy-five per cent. "
            "<bookmark mark='e'/>The theory of chance gives most of its probability to futures in which the theory "
            "itself is false."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(nums))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08))
            vo.wait_until("b")
            self.play(FadeIn(side[0]), Indicate(bars[5], color=OK))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def bug(self):
        head = label(r"The big bad bug", font_size=30, color=BAD).to_edge(UP, buff=0.35)
        steps = stack([(r"1. \ let $T$ be the theory: \ `the chance of heads is $\tfrac12$'; \ let $F$ be an "
                        r"undermining future", WHITE),
                       (r"2. \ $T$ and $F$ are incompatible: \ if $F$ happened, \ $T$ would be false; \ so "
                        r"$C(F \mid T) = 0$", ABS),
                       (r"3. \ $T$ is admissible, \ so the Principal Principle gives $C(F \mid T) = "
                        r"\text{ch}(F) > 0$", CHANCE),
                       (r"4. \ $0 > 0$: \ Humean chance and the Principal Principle contradict each other", BAD)],
                      font_size=23, aligned_edge=LEFT, width=12.2, buff=0.4).move_to([0, 0.3, 0])
        note = label(r"Lewis \ (1986): \ `a big bad bug'; \ Thau \ (1994); \ Hall \ (1994)", font_size=21,
                     color=HIST).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Now the bug. <bookmark mark='a'/>Let T be the theory of chance: the chance of heads is one half. Let F "
            "be an undermining future: say, all ten tosses heads. <bookmark mark='b'/>T and F cannot both be true: "
            "if F happened, the frequency would be three quarters, and T would be false. So any rational credence "
            "gives F probability zero, given T. <bookmark mark='c'/>But T is admissible evidence, so the Principal "
            "Principle says that credence in F given T should equal the chance of F, which is positive: one in "
            "1024. <bookmark mark='d'/>Zero equals something positive. Humean chance and the Principal Principle "
            "cannot both be right. <bookmark mark='e'/>Lewis called it the big bad bug, and for years he could not "
            "fix it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("e")
            self.play(FadeIn(note))
        self.wait(2)
        self.clear_scene()

    def repair(self):
        d = load("newp")
        head = label(r"The New Principle", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        f = MathTex(r"C(A \mid H_t\, T) \;=\; \text{ch}_t(A \mid T)", font_size=42, color=OK).next_to(head, DOWN,
                                                                                                  buff=0.4)
        hd = [r"\text{future tosses}", r"\text{PP: } \text{ch}(A)", r"\text{NP: } \text{ch}(A \mid T)"]
        rows = [[MathTex(f"{r['future']:,}".replace(",", r"\,"), font_size=22), MathTex(f"{r['pp']:.3f}",
                                                                                         font_size=22),
                 MathTex(f"{r['np']:.4f}", font_size=22, color=OK)] for r in d["rows"]]
        grid = ValueGrid(hd, rows, col_w=[2.6, 2.4, 2.8], cell_h=0.48, font_size=20).move_to([-2.4, -1.0, 0])
        side = stack([(r"condition the chance on the theory too: \ undermining futures get credence 0", OK),
                      (r"$A$: \ the next three tosses are heads", WHITE),
                      (r"in a big world the two principles agree, \ for questions about a small part of history",
                       GOAL),
                      (r"Hall \ (1994); \ Lewis, \ `Humean Supervenience Debugged' \ (1994)", HIST)], font_size=20,
                     aligned_edge=LEFT, width=4.8).move_to([4.5, -1.0, 0])
        with self.voiceover(
            "The repair came in 1994, from Ned Hall and from Lewis himself. <bookmark mark='a'/>The New Principle "
            "says: given the history and the theory of chance, your credence in A should be the chance of A "
            "conditional on the theory. <bookmark mark='b'/>Conditioning on T rules out the undermining futures, so "
            "they get credence zero, and the contradiction goes away. <bookmark mark='c'/>Does it change the "
            "numbers we use? Take A to be: the next three tosses are heads. The old principle says one eighth. With "
            "ten future tosses the new one says one in twelve. <bookmark mark='d'/>But as the world grows, the "
            "two agree: with ten thousand future tosses they agree to four decimal places. "
            "<bookmark mark='e'/>So the Principal Principle survives as an excellent approximation, and Humean "
            "chance survives, at the price of a principle that is no longer quite the simple rule we started with."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for c in grid.cell[0]])
            vo.wait_until("d")
            for r in range(1, len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.5)
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()
