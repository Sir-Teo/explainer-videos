from __future__ import annotations

from videos.psychology.psych23.common import *  # noqa: F403


def erp(t, peak, width, amp):
    return amp * np.exp(-0.5 * ((t - peak) / width) ** 2)


class Brain(VoiceoverScene):
    def construct(self):
        self.card()
        self.classic()
        self.network()
        self.erps()

    def card(self):
        card = chapter_card(10, r"Language in the brain", r"Where is language, \ and when?",
                            lit={1861: r"Broca", 1874: r"Wernicke", 1980: r"Kutas \& Hillyard",
                                 2011: r"Fedorenko et al."},
                            part=PART, scale=("brain",), marr=("how",))
        with self.voiceover("Chapter ten. Language in the brain."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def classic(self):
        head = heading(r"Broca and Wernicke")
        brain = Ellipse(width=5.0, height=3.4, color=GREY_B, fill_opacity=0.06).move_to([-3.4, 0.4, 0])
        broca = Circle(radius=0.38, color=RULE, fill_opacity=0.5).move_to([-4.9, 0.6, 0])
        wern = Circle(radius=0.38, color=WORD, fill_opacity=0.5).move_to([-2.1, 0.2, 0])
        arc = ArcBetweenPoints(broca.get_top(), wern.get_top(), angle=-PI / 3, color=GREY_B)
        lb = label(r"Broca's area", font_size=18, color=RULE).next_to(broca, DOWN, buff=0.1)
        lw = label(r"Wernicke's area", font_size=18, color=WORD).next_to(wern, DOWN, buff=0.1)
        front = label(r"front", font_size=16, color=GREY_B).next_to(brain, LEFT, buff=0.1)
        sl = label(r"left hemisphere, \ schematic", font_size=15, color=GREY_B).next_to(brain, DOWN, buff=0.15)
        rows = rows_of([
            (r"Broca, \ 1861: \ a patient who could say only \emph{tan} \ had damage at the back of the left frontal "
             r"lobe; \ speech halting, \ understanding largely kept", RULE),
            (r"Wernicke, \ 1874: \ damage further back gave fluent speech that made little sense, \ and poor "
             r"understanding", WORD),
            (r"the arc between them gave a nineteenth-century model of language: \ production in front, \ "
             r"comprehension behind", WHITE),
            (r"modern lesion studies blur the line: \ both areas take part in both, \ and in many other things", GREY_A),
        ], 6.2, 22, 0.33).move_to([3.1, 0.1, 0])
        tag = historical_tag(r"Broca (1861); \ Wernicke (1874)")
        with self.voiceover(
            "Language was the first mental faculty tied to a place in the brain. <bookmark mark='a'/> In 1861 Paul "
            "Broca examined a patient who could say only one syllable, tan. After he died, Broca found damage at the "
            "back of the left frontal lobe. Patients like him speak haltingly but understand much of what they hear. "
            "<bookmark mark='b'/> In 1874 Carl Wernicke described patients with damage further back, who spoke "
            "fluently but made little sense, and understood poorly. <bookmark mark='c'/> Joined by a bundle of "
            "fibres, the two areas gave the classic model: production at the front, comprehension behind. "
            "<bookmark mark='d'/> Modern lesion studies blur the line. Both areas take part in both, and in other "
            "things too, as Part 7 warned about any one-area-one-function map."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(brain), FadeIn(front), FadeIn(sl))
            vo.wait_until("a")
            self.play(FadeIn(broca), FadeIn(lb), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(wern), FadeIn(lw), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(arc), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def network(self):
        head = heading(r"A language network")
        rows = rows_of([
            (r"Fedorenko and colleagues, \ 2010 to now: \ find each person's language regions by contrasting "
             r"sentences with lists of non-words, \ then test those regions on everything else", WHITE),
            (r"the regions respond to language, \ read or heard, \ in any language the person knows", WORD),
            (r"and barely at all to arithmetic, \ music, \ working memory or most reasoning: \ Fedorenko, \ Behr "
             r"\& Kanwisher, \ 2011", MODEL),
            (r"people with severe aphasia can still do arithmetic, \ play chess and follow music: \ language and "
             r"thought come apart", RULE),
            (r"the method is Part 8's: \ localize in each person, \ then test, \ never reverse inference", GREY_A),
        ], 6.2, 24, 0.36).move_to([3.4, -0.1, 0])
        # a schematic of the pattern: the language regions' response by task
        conds = [(r"sentences", 1.0, WORD), (r"non-words", 0.35, GREY_B), (r"arithmetic", 0.12, MODEL),
                 (r"music", 0.1, MODEL), (r"working \\ memory", 0.14, MODEL), (r"reasoning", 0.1, MODEL)]
        chart = VGroup()
        base_y, x0, step = -1.6, -6.2, 1.07
        for k, (name, h, col_) in enumerate(conds):
            bar = Rectangle(width=0.6, height=max(3.4 * h, 0.04), stroke_width=0, fill_color=col_,
                            fill_opacity=0.8).move_to([x0 + step * k, base_y, 0], aligned_edge=DOWN)
            nm = label(name, font_size=19, color=GREY_A).next_to([x0 + step * k, base_y, 0], DOWN, buff=0.15)
            chart.add(VGroup(bar, nm))
        axis = Line([x0 - 0.5, base_y, 0], [x0 + step * 5 + 0.5, base_y, 0], color=GREY_B, stroke_width=2)
        ytl = label(r"response of each person's language regions", font_size=20, color=GREY_A).next_to(
            [x0 - 0.5, base_y + 3.6, 0], RIGHT, buff=0)
        sch = label(r"schematic of the pattern, \ not data", font_size=18, color=GREY_B).next_to(
            [x0 - 0.5, base_y - 0.95, 0], RIGHT, buff=0)
        tag = published_tag(r"Fedorenko, \ Behr \& Kanwisher (2011), \ \emph{PNAS}")
        with self.voiceover(
            "Today the picture is a network. <bookmark mark='a'/> Evelina Fedorenko and colleagues find each "
            "person's language regions by contrasting sentences with lists of non-words, and then test those same "
            "regions on everything else. <bookmark mark='b'/> The regions respond to language, written or spoken, in "
            "any language the person knows. <bookmark mark='c'/> And they barely respond to arithmetic, music, "
            "working memory, or most kinds of reasoning. <bookmark mark='d'/> That fits the patients: people with "
            "severe aphasia, who cannot understand a sentence, can still do arithmetic, play chess and follow music. "
            "Language and thought come apart in the brain. <bookmark mark='e'/> The method is Part 8's: localize in "
            "each person first, then test, and never infer a function from a location alone."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Create(axis), FadeIn(ytl), FadeIn(sch))
            vo.wait_until("a")
            self.play(FadeIn(rows[0], shift=RIGHT * 0.15), GrowFromEdge(chart[0][0], DOWN), FadeIn(chart[0][1]),
                      GrowFromEdge(chart[1][0], DOWN), FadeIn(chart[1][1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.15), Indicate(chart[0][0], color=WORD))
            vo.wait_until("c")
            self.play(FadeIn(rows[2], shift=RIGHT * 0.15),
                      *[a_ for g in chart[2:] for a_ in (GrowFromEdge(g[0], DOWN), FadeIn(g[1]))])
            for m, r in zip("de", rows[3:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def erps(self):
        head = heading(r"When: \ the N400 and the P600")
        t = np.linspace(0, 1000, 300)
        A = axes([0, 1000], [-5, 5], x_length=5.2, y_length=3.0, xticks=[0, 400, 600, 1000], yticks=[],
                 xfmt=lambda v: f"{v:.0f}", xlabel=r"ms after the word", ylabel=r"voltage", center=[-3.3, 0.2, 0],
                 font_size=16)
        base = curve(A.ax, t, erp(t, 100, 40, 1.5) - erp(t, 180, 40, 1.2), GREY_B, 2.5)
        n400 = curve(A.ax, t, erp(t, 100, 40, 1.5) - erp(t, 180, 40, 1.2) - erp(t, 400, 90, 3.2), STAT, 3)
        p600 = curve(A.ax, t, erp(t, 100, 40, 1.5) - erp(t, 180, 40, 1.2) + erp(t, 620, 120, 3.0), RULE, 3)
        key = legend([(GREY_B, r"expected word"), (STAT, r"odd meaning"), (RULE, r"odd grammar")],
                     font_size=17).move_to(A.ax.c2p(810, -3.2))
        sl = label(r"schematic, \ negative drawn down", font_size=15, color=GREY_B).next_to(A, DOWN, buff=0.45)
        rows = rows_of([
            (r"Kutas \& Hillyard, \ 1980: \ \emph{he spread the warm bread with socks}: \ about 400 ms after an "
             r"unexpected word, \ a negative wave, \ the N400", STAT),
            (r"its size tracks how predictable the word is: \ a brain measure of surprisal", MODEL),
            (r"Osterhout \& Holcomb, \ 1992: \ a grammatical violation brings a later positive wave, \ the P600", RULE),
            (r"meaning and structure leave different signatures in time, \ though how cleanly they separate is "
             r"argued", GREY_A),
        ], 5.6, 22, 0.33).move_to([3.6, 0.0, 0])
        tag = published_tag(r"Kutas \& Hillyard (1980); \ Osterhout \& Holcomb (1992)")
        with self.voiceover(
            "And when? EEG, from Part 8, has the timing. <bookmark mark='a'/> In 1980 Marta Kutas and Steven "
            "Hillyard had people read sentences like he spread the warm bread with socks. About four hundred "
            "milliseconds after the unexpected word, the brain produced a negative wave, the N400. "
            "<bookmark mark='b'/> Its size tracks how predictable the word was: a brain measure of something close "
            "to surprisal. <bookmark mark='c'/> In 1992 Lee Osterhout and Phillip Holcomb found that a grammatical "
            "violation brings a later, positive wave, the P600. <bookmark mark='d'/> Meaning and structure leave "
            "different signatures in time, though how cleanly the two separate is still argued. The waves drawn here "
            "are schematics."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(sl), Create(base), FadeIn(key[0]))
            vo.wait_until("a")
            self.play(Create(n400), FadeIn(key[1]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(p600), FadeIn(key[2]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
