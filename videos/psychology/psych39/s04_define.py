from __future__ import annotations

from videos.psychology.psych39.common import *  # noqa: F403


class Define(VoiceoverScene):
    def construct(self):
        self.card()
        self.four()
        self.wakefield()
        self.removal()

    def card(self):
        card = chapter_card(3, r"What makes it a disorder?", r"Rare, distressing, dysfunctional or harmful?",
                            lit={1973: r"APA vote", 1992: r"Wakefield"}, part=PART, scale=("person", "culture"),
                            marr=("what",))
        with self.voiceover("Chapter three. What makes it a disorder?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def four(self):
        head = heading(r"Four candidate criteria")
        items = [
            (r"statistical rarity", r"far from the average; \ but genius is rare too, \ and anxiety is common", SYMP),
            (r"distress", r"the person suffers; \ but grief is distress without disorder, \ and mania can feel "
                          r"wonderful", PERSON),
            (r"dysfunction", r"something is not working as it should; \ but ``should'' needs a standard", MODEL),
            (r"harm", r"to the person or to others; \ but harm depends on the society's judgment", AUTH),
        ]
        rows = VGroup()
        for what, how, c in items:
            rows.add(VGroup(word_chip(what, color=c, font_size=19, width=3.4), wrapped_label(how, 8.4, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, -0.2, 0])
        with self.voiceover(
            "What makes something a disorder rather than a hard life? There are four candidate criteria, and each "
            "fails alone. <bookmark mark='a'/> Statistical rarity: far from the average. But genius is rare too, and "
            "anxiety is common. <bookmark mark='b'/> Distress: the person suffers. But grief is distress without "
            "disorder, and mania can feel wonderful. <bookmark mark='c'/> Dysfunction: something isn't working as it "
            "should. But should needs a standard. <bookmark mark='d'/> Harm, to the person or to others. But what "
            "counts as harm depends on the society's judgment."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def wakefield(self):
        head = heading(r"Harmful dysfunction")
        left = word_chip(r"dysfunction: \ a fact", color=MODEL, font_size=20, width=4.0).move_to([-3.6, 1.2, 0])
        right = word_chip(r"harmful: \ a value", color=AUTH, font_size=20, width=4.0).move_to([-3.6, -0.2, 0])
        plus = label(r"$+$", font_size=34, color=GREY_A).move_to([-3.6, 0.5, 0])
        both = word_chip(r"disorder", color=PERSON, font_size=22, width=4.0).move_to([-3.6, -1.6, 0])
        arr = Arrow(right.get_bottom(), both.get_top(), buff=0.08, color=GREY_B)
        rows = rows_of([
            (r"Wakefield, \ 1992: \ a disorder is a harmful dysfunction", WHITE),
            (r"dysfunction: \ the failure of some mental mechanism to do what it was naturally selected to do, \ a "
             r"factual claim", MODEL),
            (r"harmful: \ judged so by the person's society, \ a value judgment", AUTH),
            (r"critics: \ we rarely know what a mental mechanism was selected for; \ the fact half is often a guess",
             YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = historical_tag(r"Wakefield (1992)")
        with self.voiceover(
            "The most influential definition combines two of them. <bookmark mark='a'/> In 1992 Jerome Wakefield "
            "proposed that a disorder is a harmful dysfunction. <bookmark mark='b'/> Dysfunction is a factual claim: "
            "some mental mechanism is failing to do what it was naturally selected to do. <bookmark mark='c'/> "
            "Harmful is a value judgment, made by the person's society. <bookmark mark='d'/> Critics point out that "
            "we rarely know what a mental mechanism was selected for, so the factual half is often a guess."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(left))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(plus), FadeIn(right), GrowArrow(arr), FadeIn(both))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def removal(self):
        head = heading(r"A definition at work")
        A = axes([-0.6, 1.6], [0, 100], x_length=3.8, y_length=2.6, xticks=None, yticks=[0, 50, 100],
                 yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"members voting", center=[-3.8, -0.6, 0], font_size=14)
        b = bars(A.ax, [0, 1], [58, 42], [GOOD, GREY_B], width=0.6)
        names = VGroup(label(r"uphold", font_size=15, color=GOOD).next_to(A.ax.c2p(0, 0), DOWN, buff=0.15),
                       label(r"oppose", font_size=15, color=GREY_B).next_to(A.ax.c2p(1, 0), DOWN, buff=0.15))
        tops = VGroup(label(r"58\%", font_size=17, color=GOOD).next_to(A.ax.c2p(0, 58), UP, buff=0.08))
        rows = rows_of([
            (r"until 1973, \ homosexuality was listed in the American manual as a mental disorder", WHITE),
            (r"in December 1973 the American Psychiatric Association's board removed it: \ it did not by itself "
             r"cause distress or impairment, \ and the evidence did not support a disorder", GOOD),
            (r"opponents forced a referendum of the membership; \ in 1974, \ 58\% of those voting upheld the "
             r"change", PERSON),
            (r"a definition was applied, \ and a category went; \ and a scientific category was, \ in the end, \ "
             r"put to a vote", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = historical_tag(r"APA (1973, \ 1974)")
        with self.voiceover(
            "The definition has been tested on a real case. <bookmark mark='a'/> Until 1973, homosexuality was "
            "listed in the American manual as a mental disorder. <bookmark mark='b'/> In December 1973 the board of "
            "the American Psychiatric Association removed it. It didn't in itself cause distress or impairment, and "
            "the evidence didn't support calling it a disorder. <bookmark mark='c'/> Opponents forced a referendum "
            "of the membership, and in 1974 fifty-eight percent of those voting upheld the change. "
            "<bookmark mark='d'/> A definition was applied, and a category went. And a scientific category was, in "
            "the end, put to a vote."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            for m, r in zip("ab", rows[:2]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), *[GrowFromEdge(x, DOWN) for x in b], FadeIn(tops))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
