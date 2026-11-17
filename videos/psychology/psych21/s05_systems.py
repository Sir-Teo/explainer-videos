from __future__ import annotations

from videos.psychology.psych21.common import *  # noqa: F403


class Systems(VoiceoverScene):
    def construct(self):
        self.card()
        self.catastrophe()
        self.network()
        self.penguin()
        self.answer()

    def card(self):
        card = chapter_card(4, r"Two ways to learn", r"Why would a brain need a fast learner and a slow one?",
                            lit={1989: r"McCloskey \& Cohen", 1995: r"McClelland, \ McNaughton \& O'Reilly",
                                 2004: r"Rogers \& McClelland"},
                            part=PART, scale=("circuit", "mind"), marr=("what", "how"))
        with self.voiceover("Chapter four. Two ways to learn."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def catastrophe(self):
        head = heading(r"Catastrophic interference")
        ones = VGroup(*[label(rf"$1 + {k} = {1 + k}$", font_size=26, color=TRACE) for k in range(1, 10)])
        twos = VGroup(*[label(rf"$2 + {k} = {2 + k}$", font_size=26, color=CUE) for k in range(1, 10)])
        ones.arrange(DOWN, buff=0.12).move_to([-4.4, 0.3, 0])
        twos.arrange(DOWN, buff=0.12).move_to([-2.2, 0.3, 0])
        rows = rows_of([
            (r"McCloskey and Cohen, \ 1989: \ a network trained by back-propagation learnt the ones facts, \ then "
             r"the twos", WHITE),
            (r"learning the twos wiped out the ones: \ far worse than any person", LOST),
            (r"the same weights hold everything, \ and gradient descent on new facts alone pulls them wherever the "
             r"new facts want", CUE),
            (r"a problem for distributed memory as a theory of the brain, \ and today for every machine-learning "
             r"system that learns in sequence", FALSE),
        ], 6.6, 23, 0.32).move_to([3.3, 0.0, 0])
        tag = historical_tag(r"McCloskey \& Cohen (1989)")
        with self.voiceover(
            "Chapter two's network blended an old memory with a new one. In bigger networks it can be much worse. "
            "<bookmark mark='a'/> In 1989 Michael McCloskey and Neal Cohen trained a network, by back-propagation, "
            "on the ones addition facts, one plus one up to one plus nine, and then on the twos. "
            "<bookmark mark='b'/> Learning the twos destroyed the ones, almost completely, after a few rounds. No "
            "person forgets their ones on learning their twos. <bookmark mark='c'/> The reason is that all the "
            "facts share the same weights, and gradient descent on the new facts alone moves those weights wherever "
            "the new facts want, with nothing to hold the old ones in place. <bookmark mark='d'/> They called it "
            "catastrophic interference. It looked like a fatal flaw in distributed networks as models of memory. "
            "And under the name catastrophic forgetting it's still a central problem in machine learning."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(o) for o in ones], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t_) for t_ in twos], lag_ratio=0.1), FadeIn(rows[1]))
            self.play(ones.animate.set_opacity(0.15))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def network(self):
        head = heading(r"A network that knows about living things")
        items = VGroup(*[label(w, font_size=20, color=TRACE) for w in
                         ("pine", "oak", "rose", "daisy", "robin", "canary", "sunfish", "salmon")])
        items.arrange(DOWN, buff=0.12).move_to([-5.6, 0.2, 0])
        rel = VGroup(*[label(w, font_size=20, color=CUE) for w in ("isa", "is", "can", "has")])
        rel.arrange(DOWN, buff=0.15).move_to([-2.3, -2.0, 0])
        rep = VGroup(*[Circle(radius=0.12, color=CTX, fill_opacity=0.4) for _ in range(8)]).arrange(DOWN, buff=0.1)
        rep.move_to([-3.4, 0.6, 0])
        hid = VGroup(*[Circle(radius=0.1, color=MODEL, fill_opacity=0.4) for _ in range(15)]).arrange(DOWN, buff=0.06)
        hid.move_to([-1.0, 0.3, 0])
        attrs = VGroup(*[label(w, font_size=18, color=GREY_A) for w in
                         ("living thing", "plant", "animal", "bird", "fish", r"\dots", "grow", "move", "fly", "swim",
                          "sing", r"\dots", "wings", "feathers", "scales", "gills")])
        attrs.arrange(DOWN, buff=0.06).move_to([1.4, 0.2, 0])
        lines = VGroup()
        for a, b in ((items, rep), (rep, hid), (rel, hid), (hid, attrs)):
            for x in a[::2]:
                for y in b[::3]:
                    lines.add(Line(x.get_right(), y.get_left(), stroke_width=0.5, color=GREY_D))
        rows = rows_of([
            (r"Rumelhart's network: \ an item and a relation in, \ every true attribute out", WHITE),
            (r"eight items, \ four relations, \ 35 attributes; \ trained slowly, \ all facts interleaved", CTX),
            (r"it discovers the hierarchy: \ robin and canary get similar codes, \ birds near fish, \ plants apart",
             MODEL),
        ], 4.6, 21, 0.3).move_to([4.7, 0.2, 0])
        ptag = psyche_tag(r"\texttt{memory.SemanticNet}: \ the architecture of Rogers and McClelland")
        with self.voiceover(
            "In 1995 James McClelland, Bruce McNaughton and Randall O'Reilly turned the flaw into a theory. Here's "
            "their example. <bookmark mark='a'/> David Rumelhart's network takes an item, such as robin, and a "
            "relation, such as can, and has to switch on every true answer: grow, move, fly. "
            "<bookmark mark='b'/> There are eight items, four relations and thirty-five attributes, and the network "
            "is trained slowly, on all the facts at once, over and over. <bookmark mark='c'/> It learns more than "
            "the facts. Its hidden codes come to mirror the hierarchy of living things: robin and canary end up "
            "with similar codes, birds near fish, plants far from both. This is the kind of slow, structured "
            "learning we'll meet again for concepts in the next part."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag))
            vo.wait_until("a")
            self.play(FadeIn(items), FadeIn(rel), FadeIn(rep), FadeIn(hid), FadeIn(attrs), Create(lines),
                      FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Indicate(items[4], color=TRACE), Indicate(items[5], color=TRACE))
        self.clear_scene()

    def penguin(self):
        d = load("penguin")
        head = heading(r"Teaching it the penguin")
        n = len(d["focused_old"])
        ep = np.arange(1, n + 1)
        ymax = float(np.ceil(max(d["focused_old"].max(), d["focused_new"].max()) * 100) / 100 + 0.01)
        A = axes([0, n], [0, ymax], x_length=5.6, y_length=3.0, xticks=[0, n // 2, n], yticks=[0, ymax / 2, ymax],
                 yfmt=lambda v: f"{v:.2f}", xlabel=r"training on the penguin \ (epochs)", ylabel=r"error",
                 center=[-3.4, 0.35, 0], font_size=18)
        g = VGroup(curve(A.ax, ep, d["focused_old"], LOST, 4), curve(A.ax, ep, d["focused_new"], FALSE, 3),
                   curve(A.ax, ep, d["interleaved_old"], TRACE, 4), curve(A.ax, ep, d["interleaved_new"], CTX, 3))
        key = legend([(LOST, r"focused: \ old facts"), (FALSE, r"focused: \ penguin"),
                      (TRACE, r"interleaved: \ old facts"), (CTX, r"interleaved: \ penguin")], font_size=19)
        key.arrange_in_grid(rows=2, cols=2, buff=(0.4, 0.1)).next_to(A, DOWN, buff=0.25)
        B = axes([0, 4], [0, 1], x_length=4.6, y_length=2.6, xticks=[], yticks=[0, 0.5, 1],
                 ylabel=r"the network's answer: \ ``a robin can \dots''", center=[3.7, 0.7, 0], font_size=18)
        acts = ("grow", "move", "fly", "swim")
        fb = bars(B.ax, np.arange(4) + 0.3, d["focused_robin"], LOST, width=0.35)
        ib = bars(B.ax, np.arange(4) + 0.7, d["interleaved_robin"], TRACE, width=0.35)
        names = VGroup(*[label(a, font_size=20, color=GREY_A).next_to(B.ax.c2p(i + 0.5, 0), DOWN, buff=0.12)
                         for i, a in enumerate(acts)])
        fly, swim = d["focused_robin"][2], d["focused_robin"][3]
        rows = rows_of([
            (r"a penguin is a bird that swims and cannot fly", FALSE),
            (rf"focused: \ the penguin is learnt fast, \ but now a robin can fly only {fly:.2f}, \ and swims "
             rf"{swim:.2f}", LOST),
            (rf"interleaved with the old facts: \ the penguin is learnt too, \ and the robin still flies "
             rf"({d['interleaved_robin'][2]:.2f})", TRACE),
        ], 5.6, 20, 0.2).move_to([3.7, -2.1, 0])
        ptag = psyche_tag(r"\texttt{memory.penguin\_experiment}")
        with self.voiceover(
            "Now teach the trained network something new: the penguin, a bird that swims and can't fly. "
            "<bookmark mark='a'/> First, the way McCloskey and Cohen taught the twos: the penguin's facts alone, "
            "over and over. The error on the penguin falls fast. And the error on everything the network knew "
            f"rises. <bookmark mark='b'/> Ask it what a robin can do. It now says a robin can fly only "
            f"{fly:.2f}, and can swim {swim:.2f}. In learning that one bird swims, it has changed its mind about "
            "birds. <bookmark mark='c'/> Second way: the penguin's facts interleaved with all the old ones. The "
            "penguin is learnt, more slowly, and the old knowledge stays where it was. "
            f"<bookmark mark='d'/> The robin still flies, at {d['interleaved_robin'][2]:.2f}. Slow, interleaved "
            "learning works. But you can't put your whole life on repeat each time you meet a penguin."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(ptag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Create(g[1]), Create(g[0]), FadeIn(key[0]), FadeIn(key[1]))
            vo.wait_until("b")
            self.play(FadeIn(B), FadeIn(names), LaggedStart(*[GrowFromEdge(b, DOWN) for b in fb], lag_ratio=0.2),
                      FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(g[3]), Create(g[2]), FadeIn(key[2]), FadeIn(key[3]))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in ib], lag_ratio=0.2), FadeIn(rows[2]))
        self.clear_scene()

    def answer(self):
        head = heading(r"Complementary learning systems")
        left = VGroup(label(r"hippocampus", font_size=32, color=TRACE),
                      wrapped_label(r"learns at once, \ from one episode; \ sparse, \ separated codes \ (Part 20's "
                                    r"pattern separation), \ so new memories don't overwrite each other", 4.4, 22,
                                    GREY_A)).arrange(DOWN, buff=0.2).move_to([-4.0, 1.0, 0])
        right = VGroup(label(r"cortex", font_size=32, color=CTX),
                       wrapped_label(r"learns slowly, \ from many episodes; \ overlapping codes that capture what "
                                     r"they have in common: \ structure, \ categories, \ skills", 4.4, 22, GREY_A)
                       ).arrange(DOWN, buff=0.2).move_to([4.0, 1.0, 0])
        arrow = Arrow([-1.3, 1.0, 0], [1.3, 1.0, 0], color=MODEL, buff=0)
        al = label(r"replay, \ in sleep", font_size=22, color=MODEL).next_to(arrow, UP, buff=0.1)
        rows = rows_of([
            (r"the hippocampus stores today; \ replay feeds it to the cortex interleaved with older memories, \ so "
             r"the cortex can learn the penguin without forgetting the robin", WHITE),
            (r"this explains why there are two systems, \ and why consolidation is slow: \ it has to be", MODEL),
            (r"the same answer in machines: \ a replay buffer of past experience, \ mixed into training", FALSE),
        ], 12.4, 24, 0.3).to_edge(DOWN, buff=0.65)
        tag = historical_tag(r"McClelland, \ McNaughton \& O'Reilly (1995)")
        with self.voiceover(
            "McClelland, McNaughton and O'Reilly's answer is that this is exactly why the brain has two learning "
            "systems. <bookmark mark='a'/> The hippocampus learns at once, from a single episode, using the sparse, "
            "separated codes of the last part, so that one new memory doesn't overwrite another. "
            "<bookmark mark='b'/> The cortex learns slowly, from many episodes, in overlapping codes that capture "
            "what they have in common: structure, categories, skills. <bookmark mark='c'/> And the hippocampus "
            "teaches the cortex by replay, in sleep, mixing today's episodes in with older memories: interleaving, "
            "done for free, at night. The cortex learns the penguin without forgetting the robin. "
            "<bookmark mark='d'/> It explains both why there are two systems and why consolidation is slow: it has "
            "to be slow to be safe. <bookmark mark='e'/> And it's the same answer engineers reached. Programs that "
            "learn to play games from experience keep a buffer of past experience and replay it into training."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(GrowArrow(arrow), FadeIn(al), FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
