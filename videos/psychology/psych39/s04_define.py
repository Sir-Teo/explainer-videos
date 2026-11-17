from __future__ import annotations

from videos.psychology.psych39.common import *  # noqa: F403


class Define(VoiceoverScene):
    def construct(self):
        self.card()
        self.four()
        self.wakefield()
        self.removal()
        self.engel()
        self.diathesis()

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

    def engel(self):
        head = heading(r"Biology, \ mind and society")
        spec = [(r"biological", r"genes, \ brain, \ body", SYMP, [-3.4, 1.05, 0], UP),
                (r"psychological", r"learning, \ thought, \ emotion", MODEL, [-4.45, -0.75, 0], DL),
                (r"social", r"family, \ work, \ poverty, \ culture", PERSON, [-2.35, -0.75, 0], DR)]
        circles, names = VGroup(), VGroup()
        for name, body, c, at, out in spec:
            circ = Circle(radius=1.45, stroke_color=c, stroke_width=2.5, fill_color=c, fill_opacity=0.14).move_to(at)
            circles.add(circ)
            t = VGroup(label(name, font_size=21, color=c), label(body, font_size=17, color=GREY_A)).arrange(
                DOWN, buff=0.08)
            t.move_to(np.array(at) + 0.62 * np.array(out) / np.linalg.norm(out))
            names.add(t)
        mid = little_person(0.5, color=YOU).move_to([-3.4, -0.18, 0])
        card_ = theory_card(r"The biopsychosocial model", r"George Engel, \ 1977",
                            r"illness has biological, \ psychological and social causes at once, \ and care should "
                            r"attend to all three", r"a reminder of where to look; \ too broad to be tested",
                            "not directly tested", width=6.2, font_size=20, color=KANT)
        card_.move_to([3.4, 0.85, 0])
        checks = verdict_row([
            (r"taught widely, \ in medical schools and clinical training; \ as a theory, \ never put to a test",
             "not directly tested"),
            (r"Ghaemi, \ 2009: \ it rules nothing out, \ and says nothing about which cause matters for this "
             r"person", "contested"),
        ], width=6.2, font_size=19)
        checks.next_to(card_, DOWN, buff=0.3)
        tag = published_tag(r"Engel (1977); \ Ghaemi (2009)")
        with self.voiceover(
            "A definition says what a disorder is. A second question is where one comes from. "
            "<bookmark mark='a'/> In 1977 the American physician George Engel argued in the journal Science that "
            "medicine's model was too narrow. The biomedical model explained illness by biology alone, and left out "
            "the person who was ill. <bookmark mark='b'/> He proposed a biopsychosocial model. Biological causes, "
            "like genes and the body; psychological ones, like learning, thought and emotion; and social ones, like "
            "family, work, poverty and culture; all acting at once, on one person. <bookmark mark='c'/> It was "
            "taught widely, in medical schools and in clinical training, and this act of the series follows its "
            "outline. <bookmark mark='d'/> Its record is a critique rather than a test. In 2009 the psychiatrist "
            "Nassir Ghaemi argued that the model is so broad that it rules nothing out. It tells a clinician to "
            "attend to everything, but not which cause matters most for this person, or how the causes combine. "
            "<bookmark mark='e'/> So it's better read as a reminder than as a theory: a list of places to look."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(circles[0]), FadeIn(names[0]), FadeIn(mid), FadeIn(card_.box), FadeIn(card_.name))
            vo.wait_until("b")
            self.play(FadeIn(circles[1]), FadeIn(names[1]), FadeIn(circles[2]), FadeIn(names[2]),
                      FadeIn(card_.claim), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(checks.rows[0], shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(checks.rows[1], shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(card_.verdict), FadeIn(card_.status))
        self.clear_scene()

    def diathesis(self):
        head = heading(r"Vulnerability meets stress")
        A = axes([0, 10], [0, 10], x_length=4.6, y_length=3.6, xticks=None, yticks=None, xlabel=r"vulnerability",
                 ylabel=r"stress", center=[-3.5, -0.15, 0], font_size=18)
        xs = np.linspace(1.25, 10, 120)
        line = curve(A.ax, xs, 12 / xs, AUTH, stroke_width=4)
        top = [A.ax.c2p(x, min(10, 12 / x)) for x in xs] + [A.ax.c2p(10, 10), A.ax.c2p(1.25, 10)]
        zone = Polygon(*top, stroke_width=0, fill_color=AUTH, fill_opacity=0.12)
        zl = label(r"an episode", font_size=19, color=AUTH).move_to(A.ax.c2p(6.8, 8.4))
        sch = label(r"schematic", font_size=17, color=GREY_B).next_to(A, DOWN, buff=0.15).align_to(A, RIGHT)
        lo = Dot(A.ax.c2p(2.2, 1.2), radius=0.11, color=GOOD)
        hi = Dot(A.ax.c2p(6.8, 1.2), radius=0.11, color=PERSON)
        lo_l = label(r"less vulnerable", font_size=17, color=GOOD).next_to(lo, DOWN, buff=0.12)
        hi_l = label(r"more vulnerable", font_size=17, color=PERSON).next_to(hi, DOWN, buff=0.12)
        card_ = theory_card(r"Diathesis and stress", r"Paul Meehl, \ 1962; \ Joseph Zubin and Bonnie Spring, \ 1977",
                            r"an episode begins when stress pushes a person past their own threshold, \ and ends "
                            r"when the stress recedes", r"the frame holds; \ its single-gene version failed",
                            "replicated, smaller", width=6.2, font_size=20, color=KANT)
        card_.move_to([3.4, 0.85, 0])
        checks = verdict_row([
            (r"genes and stressful events each raise the risk of depression \ (Part 40)", "replicated"),
            (r"one gene, \ the serotonin transporter, \ as the vulnerability \ (Part 40)", "failed"),
        ], width=6.2, font_size=19)
        checks.next_to(card_, DOWN, buff=0.3)
        tag = published_tag(r"Meehl (1962); \ Zubin \& Spring (1977)")
        with self.voiceover(
            "An older idea says how two of those causes combine. <bookmark mark='a'/> In 1962 Paul Meehl, whose "
            "formulas come in chapter ten, proposed that schizophrenia begins with an inherited vulnerability, which "
            "he called schizotaxia, and that only some of the people who carry it ever become ill, depending on "
            "other genes and on what happens to them. <bookmark mark='b'/> In 1977, the year of Engel's paper, "
            "Joseph Zubin and Bonnie Spring made it general. Each of us has some degree of vulnerability. An episode "
            "begins when stress pushes a person past their threshold, and it ends as the stress recedes. "
            "<bookmark mark='c'/> Picture two people, and the same hard year. The same rise in stress carries the "
            "more vulnerable person across the line, and leaves the other below it. Then the year passes. "
            "<bookmark mark='d'/> What has the record said? Genes and stressful events each raise the risk of "
            "depression, in twin studies and in studies of life events, as Part 40 shows. <bookmark mark='e'/> But "
            "when the vulnerability was pinned on a single gene, the serotonin transporter, the finding didn't hold. "
            "<bookmark mark='f'/> The frame survives; its simplest version doesn't. And before any cause can be "
            "studied, a diagnosis has to be made the same way twice. That's the next chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(sch))
            vo.wait_until("a")
            self.play(FadeIn(card_.box), FadeIn(card_.name))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(zone), FadeIn(zl), FadeIn(card_.claim))
            vo.wait_until("c")
            self.play(FadeIn(lo), FadeIn(hi), FadeIn(lo_l), FadeIn(hi_l))
            self.play(lo.animate.move_to(A.ax.c2p(2.2, 4.0)), hi.animate.move_to(A.ax.c2p(6.8, 4.0)), run_time=1.8)
            self.play(Flash(hi, color=AUTH), hi.animate.set_color(AUTH))
            self.wait(1.0)
            self.play(lo.animate.move_to(A.ax.c2p(2.2, 1.2)), hi.animate.move_to(A.ax.c2p(6.8, 1.2)).set_color(PERSON),
                      run_time=1.8)
            vo.wait_until("d")
            self.play(FadeIn(checks.rows[0], shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(checks.rows[1], shift=RIGHT * 0.15))
            vo.wait_until("f")
            self.play(FadeIn(card_.verdict), FadeIn(card_.status))
        self.clear_scene()
