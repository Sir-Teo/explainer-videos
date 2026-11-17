from __future__ import annotations

from videos.psychology.psych33.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.networks()
        self.machines()
        self.open_()

    def card(self):
        card = chapter_card(15, r"Frontier: \ causes, \ change and machines", r"What is open?",
                            lit={2012: r"Cramer et al.", 2021: r"Stieger et al.", 2024: r"Peters \& Matz"},
                            part=PART, scale=("person", "society"), marr=("what", "how"))
        with self.voiceover("Chapter fifteen. Frontier: causes, change and machines."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def networks(self):
        head = heading(r"Are the five causes, \ or summaries?")
        ang = np.linspace(np.pi / 2, np.pi / 2 + 2 * np.pi, 7)[:-1]
        words = [r"likes people", r"enjoys parties", r"talkative", r"seeks excitement", r"cheerful", r"takes charge"]
        pts = [np.array([3.3 + 1.7 * np.cos(a), 1.2 + 1.2 * np.sin(a), 0]) for a in ang]
        nodes = VGroup(*[word_chip(w, color=E_, font_size=16).move_to(p) for w, p in zip(words, pts)])
        edges = VGroup(*[Line(pts[i], pts[j], color=E_, stroke_width=2, stroke_opacity=0.6, buff=0.45)
                         for i in range(6) for j in range(i + 1, 6) if (j - i) in (1, 2, 5)])
        latent = VGroup(Circle(radius=0.5, color=E_).move_to([-3.6, 1.9, 0]),
                        label(r"E", font_size=30, color=E_).move_to([-3.6, 1.9, 0]))
        boxes = VGroup(*[word_chip(w, color=GREY_A, font_size=15).move_to([-5.6 + 0.8 * k * 1.0 + 0.4, 0.3 - 0.0, 0])
                         for k, w in enumerate((r"a", r"b", r"c", r"d", r"e", r"f"))])
        boxes.arrange(RIGHT, buff=0.2).move_to([-3.6, 0.4, 0])
        arrows = VGroup(*[Arrow(latent[0].get_bottom(), b.get_top(), buff=0.05, color=E_, stroke_width=3,
                                max_tip_length_to_length_ratio=0.15) for b in boxes])
        rows = rows_of([
            (r"the usual view: \ a trait is a latent cause, \ and each item is one of its effects", WHITE),
            (r"Ang\'elique Cramer and colleagues, \ 2012: \ the items may cause each other: \ ``you can't like "
             r"parties if you don't like people''; \ the trait is the network's settled state", E_),
            (r"the two views make the same correlations, \ as Part 32's three worlds did; \ they differ in what an "
             r"intervention on one item would do: \ Part 44 builds both", MODEL),
        ], 12.4, 21, 0.32).move_to([0, -2.2, 0])
        tag = published_tag(r"Cramer et al.\ (2012)")
        with self.voiceover(
            "Three frontiers. The first: are the five causes, or summaries? <bookmark mark='a'/> The usual view "
            "treats a trait as a latent cause, and each item as one of its effects. <bookmark mark='b'/> In 2012 "
            "Angélique Cramer and colleagues proposed that the items may cause each other instead. You can't like "
            "parties if you don't like people. On this view the trait is the settled state of a network. "
            "<bookmark mark='c'/> The two views make the same correlations, as Part 32's three worlds did. They "
            "differ in what an intervention on one item would do, and Part 44 builds both."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(latent), FadeIn(boxes), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1),
                      FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(nodes), Create(edges), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def machines(self):
        head = heading(r"Machines that read people")
        rows = rows_of([
            (r"Heinrich Peters and Sandra Matz, \ 2024: \ large language models, \ given people's Facebook status "
             r"updates and no training for the task, \ estimated the five traits at about .29 agreement with "
             r"self-reports", WHITE),
            (r"about as well as models built for the purpose, \ and more accurately for some groups than others", O_),
            (r"so the same aggregation that rescued personality psychology now runs on everyone's text", YOU),
            (r"the open questions are not only scientific: \ consent, \ fairness across groups, \ and what an "
             r"estimate may be used for", LOST),
        ], 12.4, 24, 0.42).move_to([0, -0.3, 0])
        tag = published_tag(r"Peters \& Matz (2024)")
        with self.voiceover(
            "The second frontier is machines. <bookmark mark='a'/> In 2024 Heinrich Peters and Sandra Matz gave "
            "large language models people's Facebook status updates, with no training for the task, and asked for "
            "the five traits. The estimates agreed with self-reports at about point two nine. "
            "<bookmark mark='b'/> That's about as well as models built for the purpose, and more accurate for some "
            "groups than others. <bookmark mark='c'/> The same aggregation that rescued personality psychology now "
            "runs on everyone's text. <bookmark mark='d'/> And the open questions aren't only scientific: consent, "
            "fairness across groups, and what an estimate may be used for."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def open_(self):
        head = heading(r"Open questions")
        rows = rows_of([
            (r"are the five latent causes, \ or summaries of networks of habits?", E_),
            (r"are they universal, \ or partly products of literacy and questionnaires?", O_),
            (r"how much can a person change on purpose, \ and do the changes last for years?", C_),
            (r"what should a trait inferred from your data be allowed to decide?", LOST),
            (r"how do traits connect to the circuits of Parts 17 and 29?", N_),
        ], 12.4, 26, 0.42).move_to([0, -0.3, 0])
        with self.voiceover(
            "So the open questions. <bookmark mark='a'/> Are the five latent causes, or summaries of networks of "
            "habits? <bookmark mark='b'/> Are they universal, or partly products of literacy and questionnaires? "
            "<bookmark mark='c'/> How much can a person change on purpose, and do the changes last for years? "
            "<bookmark mark='d'/> What should a trait inferred from your data be allowed to decide? "
            "<bookmark mark='e'/> And how do traits connect to the reward and fear circuits of Parts 17 and 29?"
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
