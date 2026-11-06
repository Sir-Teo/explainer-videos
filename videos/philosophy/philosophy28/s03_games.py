from __future__ import annotations

from videos.philosophy.philosophy28.common import *  # noqa: F403


def figure(x, y, name, col):
    head = Circle(0.25, color=col, fill_opacity=0.35).move_to([x, y + 0.45, 0])
    body = Line([x, y + 0.2, 0], [x, y - 0.5, 0], color=col, stroke_width=3)
    nm = label(name, font_size=19, color=col).next_to(body, DOWN, buff=0.1)
    return VGroup(head, body, nm)


class Games(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"Language games", r"What do all games have in common?", lit=(1953,), part=PART)
        with self.voiceover("Chapter two. Language games."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.builders()
        self.games()
        self.family()
        self.use()

    def builders(self):
        head = label(r"The builders \ (\textit{Investigations}, \ \S 2)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        A = figure(-4.6, 0.3, r"A, \ the builder", USE)
        B = figure(-1.0, 0.3, r"B, \ the assistant", HEAR)
        stones = VGroup()
        kinds = [(r"block", Square(0.55)), (r"pillar", Rectangle(width=0.35, height=1.0)),
                 (r"slab", Rectangle(width=1.0, height=0.25)), (r"beam", Rectangle(width=1.3, height=0.18))]
        for i, (nm, shp) in enumerate(kinds):
            shp.set_stroke(GREY_A, 2).set_fill(GREY_D, 0.8).move_to([2.0 + 1.5 * i, 0.4, 0])
            stones.add(VGroup(shp, label(nm, font_size=17, color=GREY_A).next_to(shp, DOWN, buff=0.15)))
        call = label(r"`Slab!'", font_size=30, color=WORD).next_to(A, UP, buff=0.3)
        rows = stack([(r"A calls a word; \ B brings the stone he has learned to bring at that call", WHITE),
                      (r"`imagine this as a complete primitive language'", RULE_C),
                      (r"is `slab!' a name, \ or an order, \ or short for `bring me a slab'? \ its meaning is its role in "
                       r"the activity", USE)], font_size=21, aligned_edge=LEFT, width=12.0, buff=0.25).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The Investigations begins with a different picture. <bookmark mark='a'/>A builder, A, and his "
            "assistant, B, are building with stones: blocks, pillars, slabs and beams. <bookmark mark='b'/>A calls out "
            "a word, slab, and B brings the stone he has learned to bring at that call. <bookmark mark='c'/>Imagine "
            "this, Wittgenstein says, as a complete primitive language. <bookmark mark='d'/>Is slab a name? An order? "
            "Short for bring me a slab? Nothing in the word decides. What it means is the role it plays in the "
            "activity of building."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(B), LaggedStart(*[FadeIn(s) for s in stones], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(call), FadeIn(rows[0]))
            slab = stones[2][0]
            self.play(slab.animate.move_to(B[0].get_center() + RIGHT * 0.9), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def games(self):
        head = label(r"The multiplicity of language games \ (\S 23)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        items = [r"giving orders, \ and obeying them", r"describing an object", r"reporting an event",
                 r"forming and testing a hypothesis", r"making up a story", r"play-acting", r"guessing riddles",
                 r"making a joke", r"translating", r"asking, \ thanking, \ cursing, \ greeting, \ praying"]
        cols = [WORD, WORLD, USE, RULE_C, HEAR]
        tiles = VGroup(*[label(t, font_size=21, color=cols[i % 5]) for i, t in enumerate(items)])
        tiles.arrange_in_grid(rows=5, cols=2, buff=(1.2, 0.35), col_alignments="ll").move_to([0, 0.1, 0])
        foot = label(r"`the speaking of language is part of an activity, \ or of a form of life' \ (\S 23)",
                     font_size=22, color=GOAL).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "There are countless such games, he says, and lists some. <bookmark mark='a'/>Giving orders and obeying "
            "them; describing an object; reporting an event; forming and testing a hypothesis; making up a story; "
            "play-acting; guessing riddles; making a joke; translating; asking, thanking, cursing, greeting, praying. "
            "<bookmark mark='b'/>The point is that the speaking of language is part of an activity, or of a form of "
            "life. Describing how things are, the job the Tractatus gave every proposition, is one game among many."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in tiles], lag_ratio=0.25), run_time=5)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def family(self):
        d = load("family")
        head = label(r"Family resemblance, \ computed", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["common"] == [] and d["connected"]
        names = list(d["games"])
        pos = {n: np.array([3.0 * math.cos(PI / 2 - TAU * i / len(names)) - 2.4,
                            2.1 * math.sin(PI / 2 - TAU * i / len(names)) - 0.4, 0]) for i, n in enumerate(names)}
        nodes = {n: VGroup(Dot(pos[n], radius=0.1, color=USE),
                           label(n, font_size=19, color=USE).next_to(pos[n], UP if pos[n][1] > -0.4 else DOWN,
                                                                     buff=0.12)) for n in names}
        edges = VGroup(*[Line(pos[a], pos[b], color=GREY_B, stroke_width=1 + 1.2 * len(sh), stroke_opacity=0.7)
                         for a, b, sh in d["edges"]])
        feat = VGroup()
        for n in names:
            feat.add(label(n + r": \ " + r", \ ".join(d["games"][n]), font_size=16, color=GREY_A))
        feat.arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to([4.2, 0.6, 0])
        if feat.width > 5.6:
            feat.width = 5.6
        side = stack([(r"no feature is shared by all six", BAD),
                      (rf"yet {len(d['edges'])} of the {d['pairs']} pairs share something, \ and the network is "
                       r"connected", OK),
                      (r"`a complicated network of similarities overlapping and criss-crossing' \ (\S 66)", RULE_C)],
                     font_size=20, aligned_edge=LEFT, width=5.6, buff=0.22).move_to([4.2, -2.3, 0])
        with self.voiceover(
            "What do all these games have in common? Don't say there must be something, Wittgenstein writes: look "
            "and see. <bookmark mark='a'/>Take six games: chess, patience, ring-a-ring-a-roses, tennis, catch and "
            "poker, and list some of their features: a board, cards, a ball, winning, skill, luck, rules, a song. "
            "<bookmark mark='b'/>The Reasoner checks. No feature is shared by all six. <bookmark mark='c'/>But most "
            "pairs share something, and following the shared features you can get from any game to any other: the "
            "network is connected. <bookmark mark='d'/>A complicated network of similarities, overlapping and "
            "criss-crossing, Wittgenstein called it: family resemblance. Concepts like game need no common essence "
            "to be perfectly usable."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(*[FadeIn(v) for v in nodes.values()], FadeIn(feat))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.15), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def use(self):
        head = label(r"Meaning as use", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"\S 43", r"for a large class of cases, \ the meaning of a word is its use in the language", WORD),
            (r"grammar", r"the rules of a language game: \ not a theory of what words stand for, \ but a description of "
                         r"how they are used", RULE_C),
            (r"philosophy", r"problems arise `when language goes on holiday' \ (\S 38): \ words pulled out of the games "
                            r"that give them sense", BAD),
            (r"the method", r"assemble reminders of actual use, \ until the problem disappears", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "From this comes the slogan. <bookmark mark='a'/>For a large class of cases, the meaning of a word is its "
            "use in the language. <bookmark mark='b'/>The rules of a language game Wittgenstein calls grammar: not a "
            "theory of what words stand for, but a description of how they are used. <bookmark mark='c'/>"
            "Philosophical problems arise, he says, when language goes on holiday: when words are pulled out of the "
            "games that give them sense, as when we ask what time really is. <bookmark mark='d'/>The method is to "
            "assemble reminders of how words are actually used, until the problem disappears. Whether every problem "
            "disappears so easily is the question of the next chapter."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
