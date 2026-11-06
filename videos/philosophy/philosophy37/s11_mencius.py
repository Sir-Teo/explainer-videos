from __future__ import annotations

from videos.philosophy.philosophy37.common import *  # noqa: F403


class Mencius(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Mencius and Xunzi", r"Is human nature good?", lit=(-300, -250), part=PART)
        with self.voiceover("Chapter ten. Mencius and Xunzi."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.mencius()
        self.xunzi()
        self.mozi()
        self.theories()

    def mencius(self):
        head = label(r"Mencius: \ human nature is good", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"against Gaozi", r"Gaozi: \ nature is like water, \ flowing east or west as channelled; \ Mencius: \ "
                                   r"water does not flow east or west by nature, \ but it does flow down", REAL),
                (r"the sprouts", r"the child at the well shows that everyone has a sprout of compassion, \ and of "
                                 r"shame, \ deference and discernment", REAL),
                (r"Ox Mountain \ (6A8)", r"its trees were once lovely; \ axes and grazing stripped it bare; \ the "
                                         r"bareness is not the mountain's nature", OUGHT),
                (r"cultivation", r"moral growth is like a farmer's: \ do not neglect the sprouts, \ and do not pull "
                                 r"them up to help them grow", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.45, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Two thousand years before Haidt, Chinese philosophers argued about where morality comes from. "
            "<bookmark mark='a'/>Mencius, in the fourth century before the common era, debated Gaozi, who said human "
            "nature is like water: it flows east or west as it is channelled. Mencius replied that water may not "
            "prefer east to west, but it does prefer down: human nature tends toward the good as water flows "
            "downhill. <bookmark mark='b'/>The child at the well, from Part 35, shows that everyone has a sprout of "
            "compassion, and sprouts of shame, deference and discernment too. <bookmark mark='c'/>Ox Mountain's trees "
            "were once lovely; axes and grazing goats stripped it bare, and people who see it bare think that is its "
            "nature. <bookmark mark='d'/>Moral growth is like farming: do not neglect the sprouts, and do not be like "
            "the farmer from Song who pulled at his shoots to help them grow, and killed them."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def xunzi(self):
        head = label(r"Xunzi: \ human nature is bad", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"the thesis", r"``Human nature is bad; \ its goodness is the result of conscious activity.''", ANTI),
                (r"the craftsman", r"warped wood must be laid against the straightening board, \ steamed and forced, "
                                   r"\ before it is straight", OUGHT),
                (r"ritual", r"the sage-kings created ritual and righteousness to shape desire, \ as a potter makes "
                            r"a pot", OUGHT),
                (r"for metaethics", r"morality as an invention that serves human needs: \ a constructivism, \ two "
                                    r"millennia early", EXPR)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "A generation later Xunzi disagreed. <bookmark mark='a'/>Human nature is bad, he wrote; its goodness is the "
            "result of conscious activity. <bookmark mark='b'/>Warped wood must be laid against the straightening "
            "board, steamed and forced into shape, before it becomes straight. <bookmark mark='c'/>The sage-kings "
            "created ritual and righteousness to shape human desire, as a potter shapes clay into a pot: morality is "
            "made. <bookmark mark='d'/>For metaethics, Xunzi offers something like a constructivism two thousand "
            "years early: morality as an invention, answerable to the human needs it serves."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def mozi(self):
        head = label(r"Mozi's impartial care", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the Mohists", r"fifth century BCE: \ jian ai, \ inclusive care: \ regard others' families as your own", REAL),
                (r"the test", r"judge doctrines by their benefit to the people: \ an early consequentialism", OUGHT),
                (r"Mencius's reply", r"to love everyone equally is to have no father: \ care must be graded, \ beginning at home", ANTI),
                (r"the debate today", r"impartiality against partiality: \ Parts 35 and 36, \ twenty four centuries later", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Both Mencius and Xunzi wrote against a third school. <bookmark mark='a'/>The Mohists, followers of Mozi "
            "in the fifth century before the common era, taught inclusive care: regard other people's families as you "
            "regard your own. <bookmark mark='b'/>Doctrines were to be judged by their benefit to the people, an "
            "early consequentialism. <bookmark mark='c'/>Mencius replied that to love everyone equally is to have no "
            "father: care must be graded, beginning with one's own family and extending outward. <bookmark "
            "mark='d'/>It is the debate between impartiality and partiality of Parts 35 and 36, twenty four centuries "
            "earlier."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def theories(self):
        head = label(r"Two theories of moral learning", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        hd = [r"", r"\text{Mencius}", r"\text{Xunzi}"]
        rows = [(r"starting point", r"sprouts of goodness", r"self-interested desire"),
                (r"the model", r"a farmer tending growth", r"a craftsman shaping material"),
                (r"what education does", r"develops what is there", r"reforms what is there"),
                (r"what can go wrong", r"neglect, \ or forcing", r"too little ritual"),
                (r"echoes today", r"Haidt's intuitions; \ virtue ethics", r"Street; \ constructivism")]
        cells = [[label(a, font_size=19, color=GREY_A), label(b, font_size=19, color=REAL),
                  label(c, font_size=19, color=ANTI)] for a, b, c in rows]
        grid = ValueGrid(hd, cells, col_w=[3.4, 4.0, 4.0], cell_h=0.56, font_size=18).move_to([0, 0.3, 0])
        foot = label(r"Ivanhoe; \ Van Norden: \ a development model against a re-formation model of moral education",
                     font_size=18, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Philip Ivanhoe and Bryan Van Norden read the debate as two theories of moral learning. "
            "<bookmark mark='a'/>For Mencius, we start with sprouts of goodness; for Xunzi, with self-interested "
            "desire. <bookmark mark='b'/>Mencius's model is a farmer, who tends growth; Xunzi's a craftsman, who "
            "shapes material. <bookmark mark='c'/>Education develops what is there, or reforms it. "
            "<bookmark mark='d'/>For Mencius it fails through neglect or forcing; for Xunzi, through too little ritual. "
            "<bookmark mark='e'/>Their echoes run through this part: Mencius's sprouts in Haidt's intuitions and in "
            "virtue ethics, Xunzi's invention in Street and the constructivists."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, k in zip("abcde", range(5)):
                vo.wait_until(mk)
                self.play(*[FadeIn(c) for c in grid.cell[k]])
            self.play(FadeIn(foot))
        self.clear_scene()
