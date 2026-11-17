from __future__ import annotations

from videos.psychology.psych21.common import *  # noqa: F403


class Why(VoiceoverScene):
    def construct(self):
        self.card()
        self.sleep()
        self.proactive()
        self.associator()
        self.rif()

    def card(self):
        card = chapter_card(2, r"Why we forget", r"Does a memory fade, \ or is it pushed aside?",
                            lit={1900: r"M\"uller \& Pilzecker", 1924: r"Jenkins \& Dallenbach", 1957: r"Underwood",
                                 1994: r"Anderson, \ Bjork \& Bjork"},
                            part=PART, scale=("mind",), marr=("what", "how"))
        with self.voiceover("Chapter two. Why we forget."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def sleep(self):
        head = heading(r"Decay, \ or interference?")
        left = VGroup(label(r"decay", font_size=34, color=LOST),
                      wrapped_label(r"a trace weakens with time itself, \ like a footprint in sand", 5.4, 24, GREY_A)
                      ).arrange(DOWN, buff=0.2).move_to([-3.4, 1.5, 0])
        right = VGroup(label(r"interference", font_size=34, color=CUE),
                       wrapped_label(r"a trace is still there, \ but other memories compete with it, \ or "
                                     r"overwrite it", 5.4, 24, GREY_A)).arrange(DOWN, buff=0.2).move_to([3.4, 1.5, 0])
        rows = rows_of([
            (r"Jenkins and Dallenbach, \ 1924: \ two subjects learnt lists of ten nonsense syllables, \ then slept "
             r"or stayed awake for one to eight hours", WHITE),
            (r"after sleep they forgot much less than after the same hours awake", CTX),
            (r"time alone cannot be the cause: \ what happens in the time matters", CUE),
            (r"a modern reading: \ sleep is not only a pause in interference, \ it actively consolidates \ "
             r"(chapter 3)", MODEL),
        ], 12.4, 25, 0.3).move_to([0, -1.4, 0])
        tag = historical_tag(r"Jenkins \& Dallenbach (1924)")
        with self.voiceover(
            "Why does a memory get weaker? There are two classic answers. <bookmark mark='a'/> Decay: the trace "
            "itself fades with time, like a footprint in sand. <bookmark mark='b'/> Or interference: the trace is "
            "still there, but other memories compete with it at retrieval, or overwrite it. "
            "<bookmark mark='c'/> In 1924, at Cornell, John Jenkins and Karl Dallenbach put this to a test with two "
            "subjects, who learnt lists of ten nonsense syllables to mastery, and then "
            "either went to sleep or stayed awake, for one, two, four or eight hours, before recall. "
            "<bookmark mark='d'/> After sleep they forgot much less than after the same hours awake. "
            "<bookmark mark='e'/> If time alone did the forgetting, the two would be equal. What happens during the "
            "time matters. <bookmark mark='f'/> Jenkins and Dallenbach took it as evidence for interference: the "
            "sleeper meets nothing new. Today we'd add that sleep does something positive too, which is the next "
            "chapter."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]), FadeIn(tag))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
            vo.wait_until("f")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def proactive(self):
        head = heading(r"Proactive interference: \ what you learnt before")
        x = np.arange(0, 21)
        A = axes([0, 20], [0, 1], x_length=6.0, y_length=3.0, xticks=[0, 5, 10, 15, 20], yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"lists learnt before this one",
                 ylabel=r"recalled a day later", center=[-3.3, 0.0, 0], font_size=18)
        # a schematic of the shape of Underwood's summary: decline with prior lists, flattening
        y = 0.25 + 0.5 * np.exp(-x / 5.0)
        sketch = curve(A.ax, x, y, CUE, 4)
        stag = label(r"the shape of Underwood's summary, \ schematic", font_size=18, color=GREY_B).next_to(A, DOWN,
                                                                                                         buff=0.1)
        rows = rows_of([
            (r"Underwood, \ 1957: \ gathered the experiments that tested one list a day after learning it", WHITE),
            (r"the more lists the subjects had learnt before, \ the more of the new one they forgot; \ without "
             r"them, \ forgetting in a day falls from about 75\% to about 25\%", CUE),
            (r"forgetting is not a fixed rate: \ much of it is old memories competing with new", LOST),
            (r"and Ebbinghaus had learnt thousands of syllable lists: \ his own curve may be steep for this reason",
             TRACE),
        ], 6.4, 22, 0.3).move_to([3.5, 0.0, 0])
        tag = historical_tag(r"Underwood (1957)")
        with self.voiceover(
            "The strongest evidence for interference came from looking back at the old experiments. "
            "<bookmark mark='a'/> In 1957 Benton Underwood gathered the studies in which people learnt a list and "
            "recalled it a day later. Why did some find that people forgot most of a list in a day, and others "
            "very little? <bookmark mark='b'/> The answer was what the subjects had done before. The more lists "
            "they had already learnt in the same experiment, the more of the new list they forgot. Take away that "
            "earlier learning, Underwood estimated, and forgetting in a day falls from about seventy-five percent to "
            "about twenty-five. This is the shape of his summary, drawn schematically. <bookmark mark='c'/> The old lists, not time, did most of the forgetting. "
            "That's proactive interference: earlier learning harms later. <bookmark mark='d'/> And think of "
            "Ebbinghaus, who had learnt thousands of lists of syllables. Some of the steepness of the most famous "
            "curve in psychology may be the interference of all the lists before."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(sketch), FadeIn(stag), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def associator(self):
        d = load("interference")
        head = heading(r"Retroactive interference in a network")
        pairs = VGroup(
            VGroup(label(r"list 1:", font_size=24, color=GREY_B), MathTex(r"A \to B", font_size=36, color=TRACE)),
            VGroup(label(r"list 2:", font_size=24, color=GREY_B), MathTex(r"A' \to C", font_size=36, color=LOST)),
            VGroup(label(r"test:", font_size=24, color=GREY_B), MathTex(r"A \to\ ?", font_size=36, color=CUE)),
        )
        for p_ in pairs:
            p_.arrange(RIGHT, buff=0.25)
        pairs.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-4.6, 1.3, 0])
        eq = MathTex(r"W = \sum_\mu \mathbf{b}_\mu \mathbf{a}_\mu^\top + \sum_\mu \mathbf{c}_\mu "
                     r"\mathbf{a}'^\top_\mu", font_size=32).move_to([-3.9, -0.4, 0])
        A = axes([0, 1], [0, 1], x_length=5.4, y_length=3.2, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{v:.1f}",
                 xlabel=r"overlap of list 2's cues with list 1's", ylabel=r"recall of B \ (correlation)",
                 center=[3.4, 0.4, 0], font_size=18)
        c = curve(A.ax, d["overlap"], d["both"], LOST, 4)
        base = DashedLine(A.ax.c2p(0, d["first"]), A.ax.c2p(1, d["first"]), color=TRACE)
        bl = label(r"list 1 alone", font_size=20, color=TRACE).next_to(base, UP, buff=0.08).align_to(base, RIGHT)
        rows = rows_of([
            (r"a linear associator: \ Hebb's rule adds each pair's outer product to one weight matrix", GREY_A),
            (r"a second list with different cues barely hurts; \ the same cues with new answers, \ a lot", LOST),
            (r"the classic A-B, \ A-C design of the 1950s: \ the trace is not erased, \ it is blended", CUE),
        ], 12.4, 23, 0.22).to_edge(DOWN, buff=0.65)
        ptag = psyche_tag(r"\texttt{memory.associator\_interference}: \ 200 units, \ 20 pairs")
        with self.voiceover(
            "Interference can also work backwards: new learning harms old. And it's easy to see why in a network. "
            "<bookmark mark='a'/> Learn twenty pairs, A to B, in a linear associator, the simplest memory network, "
            "where Hebb's rule adds each pair's outer product into one weight matrix. Then learn a second list, A "
            "prime to C, and test A. <bookmark mark='b'/> All the pairs live in the same weights. When the second "
            "list's cues are unrelated to the first's, the new pairs add a little noise, and recall of B barely "
            "falls. <bookmark mark='c'/> As the cues overlap more, the same cue now points to two answers, and "
            "recall of B falls steadily, toward a blend of the two. <bookmark mark='d'/> This is the A-B, A-C design that verbal "
            "learning researchers ran for decades. In the network the old trace is not erased; it's mixed with the "
            "new one in the same connections."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pairs[0]), FadeIn(ptag))
            vo.wait_until("a")
            self.play(FadeIn(pairs[1]), FadeIn(pairs[2]), Write(eq), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(A), Create(base), FadeIn(bl))
            vo.wait_until("c")
            self.play(Create(c), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def rif(self):
        head = heading(r"Remembering can make you forget")
        cats = VGroup()
        spec = ((r"FRUIT", ((r"orange", "plus"), (r"banana", "minus"), (r"lemon", "plus"), (r"cherry", "minus"))),
                (r"DRINK", ((r"vodka", "base"), (r"gin", "base"), (r"whisky", "base"), (r"rum", "base"))))
        colors = {"plus": TRACE, "minus": LOST, "base": GREY_A}
        for name, items in spec:
            col = VGroup(label(name, font_size=28, color=CUE),
                         *[label(w, font_size=24, color=colors[k]) for w, k in items]).arrange(DOWN, buff=0.15)
            cats.add(col)
        cats.arrange(RIGHT, buff=1.4).move_to([-3.6, 0.6, 0])
        keys = VGroup(
            label(r"Rp$+$: \ practised \ (FRUIT -- or\underline{\ \ \ \ })", font_size=22, color=TRACE),
            label(r"Rp$-$: \ unpractised, \ from a practised category", font_size=22, color=LOST),
            label(r"Nrp: \ from a category never practised", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, 1.4, 0])
        order = MathTex(r"\text{Rp}+", r"\;>\;", r"\text{Nrp}", r"\;>\;", r"\text{Rp}-", font_size=40)
        order[0].set_color(TRACE)
        order[4].set_color(LOST)
        order.move_to([3.4, 0.0, 0])
        rows = rows_of([
            (r"Anderson, \ Bjork and Bjork, \ 1994: \ practising some members of a category impairs the recall "
             r"of the rest", WHITE),
            (r"the account: \ the competitors are suppressed so that the target can win; \ forgetting as a tool of "
             r"retrieval", CUE),
            (r"Murayama and colleagues' meta-analysis, \ 2014: \ a reliable effect, \ larger or smaller depending "
             r"on the test; \ whether it is inhibition is still argued", LOST),
        ], 12.4, 23, 0.25).to_edge(DOWN, buff=0.65)
        tag = historical_tag(r"Anderson, \ Bjork \& Bjork (1994); \ Murayama et al.\ (2014)")
        with self.voiceover(
            "A last kind of interference is the strangest: remembering can make you forget. "
            "<bookmark mark='a'/> In Michael Anderson, Robert Bjork and Elizabeth Bjork's procedure, people study "
            "category and member pairs: fruit, orange; fruit, banana; drink, vodka. Then they practise retrieving "
            "half the members of half the categories, filling in fruit, o r blank, again and again. "
            "<bookmark mark='b'/> On the final test, the practised items are recalled best, of course. But the "
            "unpractised members of the practised categories, banana and cherry, are recalled worse than members "
            "of categories never practised at all. <bookmark mark='c'/> Retrieving orange hurt banana. Anderson's "
            "account is that when banana competes with orange during practice, it is suppressed, and stays "
            "suppressed: forgetting is a tool that retrieval uses. <bookmark mark='d'/> A meta-analysis by Kou "
            "Murayama and colleagues found the effect reliable across many studies, larger in some tests than "
            "others, and whether it truly is inhibition, rather than a kind of blocking, is still argued."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cats), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(keys[0]))
            vo.wait_until("b")
            self.play(FadeIn(keys[1]), FadeIn(keys[2]), Write(order))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]), Indicate(order[4], color=LOST))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
