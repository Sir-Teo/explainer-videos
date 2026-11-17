from __future__ import annotations

from videos.psychology.psych21.common import *  # noqa: F403

D_COL = (FALSE, CUE, TRACE)


class Confidence(VoiceoverScene):
    def construct(self):
        self.card()
        self.flashbulb()
        self.witness()
        self.model()
        self.cac()

    def card(self):
        card = chapter_card(10, r"Confidence and accuracy", r"When does feeling sure mean being right?",
                            lit={1977: r"Brown \& Kulik", 1992: r"Neisser \& Harsch", 2003: r"Talarico \& Rubin",
                                 2017: r"Wixted \& Wells"},
                            part=PART, scale=("mind", "group"), marr=("what",))
        with self.voiceover("Chapter ten. Confidence and accuracy."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def flashbulb(self):
        t = archive.TALARICO_RUBIN_2003.data
        head = heading(r"Flashbulb memories")
        A = axes([0, 32], [0, 1], x_length=5.2, y_length=3.0, xticks=[1, 6, 32], yticks=[0, 1],
                 yfmt=lambda v: {0: r"\text{low}", 1: r"\text{high}"}[int(v)], xlabel=r"weeks after 12 September 2001",
                 ylabel=r"schematic", center=[-3.6, -0.1, 0], font_size=18)
        w = np.array([0.0, 1.0, 6.0, 32.0])
        cons = 1.0 - 0.35 * np.log1p(w) / np.log1p(32)
        conf_f = 0.95 - 0.03 * np.log1p(w) / np.log1p(32)
        conf_e = 0.9 - 0.4 * np.log1p(w) / np.log1p(32)
        g = VGroup(curve(A.ax, w, cons, GREY_B, 4), curve(A.ax, w, conf_f, FALSE, 4),
                   DashedVMobject(curve(A.ax, w, conf_e, CUE, 3), num_dashes=20))
        key = legend([(GREY_B, r"consistency: \ both kinds of memory, \ falling alike"),
                      (FALSE, r"belief and vividness: \ the 9/11 memory"),
                      (CUE, r"belief and vividness: \ an everyday memory")], font_size=18).next_to(A, DOWN, buff=0.2)
        rows = rows_of([
            (r"Brown and Kulik, \ 1977: \ memories of hearing shocking news seem to be burned in, \ as by a flash",
             WHITE),
            (r"Neisser and Harsch: \ students wrote down how they heard of the \emph{Challenger} disaster the next "
             r"morning; \ years later many told a different story, \ confidently", LOST),
            (rf"Talarico and Rubin, \ 2003: \ {t['n']} students on 12 September 2001, \ retested after 1, \ 6 or 32 "
             r"weeks", GREY_A),
            (r"the 9/11 memories became as inconsistent as everyday ones; \ only the confidence stayed", FALSE),
        ], 6.0, 21, 0.3).move_to([3.5, 0.0, 0])
        tag = historical_tag(archive.TALARICO_RUBIN_2003.cite)
        with self.voiceover(
            "We now know that memory can be wrong. The practical question is whether we can tell when. Does "
            "feeling sure mean being right? <bookmark mark='a'/> In 1977 Roger Brown and James Kulik described "
            "flashbulb memories: where you were when you heard shocking news seems to be burned in, as by a flash. "
            "<bookmark mark='b'/> Ulric Neisser and Nicole Harsch tested it. The morning after the Challenger shuttle "
            "exploded in 1986, students wrote down how they had heard. Years later, many gave a quite different "
            "account, with high confidence, and some, shown their own original account, preferred the new version. "
            f"<bookmark mark='c'/> On the twelfth of September 2001, Jennifer Talarico and David Rubin asked {t['n']} "
            "students to write down how they had heard about the attacks the day before, and also an everyday "
            "memory from the same days. They retested them after one, six or thirty-two weeks. "
            "<bookmark mark='d'/> The two kinds of memory became inconsistent at the same rate. What differed was "
            "belief: people stayed sure of their September the eleventh memories, and vivid in them, as they "
            "drifted. Their title says it: confidence, not consistency, characterises flashbulb memories. The curves "
            "here are a schematic of that pattern."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(A))
            vo.wait_until("d")
            self.play(Create(g[0]), Create(g[1]), Create(g[2]), FadeIn(key), FadeIn(rows[3]))
        self.clear_scene()

    def witness(self):
        head = heading(r"The witness in court")
        rows = rows_of([
            (r"in many of the convictions in the United States later overturned by DNA evidence, \ a mistaken "
             r"eyewitness identification was part of the case", LOST),
            (r"1984: \ Jennifer Thompson picked Ronald Cotton as the man who attacked her; \ by the trial she was "
             r"certain; \ DNA cleared him in 1995, \ after more than ten years in prison", WHITE),
            (r"her first identification, \ from photographs, \ had been slow and hesitant", CUE),
            (r"Wixted and Wells, \ 2017: \ confidence at trial is inflated by everything that happens after; \ but "
             r"\emph{initial} confidence, \ under good procedures, \ is highly informative", MODEL),
            (r"good procedures: \ one suspect per line-up who does not stand out, \ a warning that the culprit may "
             r"not be there, \ a tester who does not know who the suspect is, \ confidence recorded at once", TRACE),
        ], 12.4, 24, 0.32).move_to([0, -0.2, 0])
        tag = historical_tag(archive.WIXTED_WELLS_2017.cite)
        with self.voiceover(
            "The question matters most in court. <bookmark mark='a'/> In many of the convictions in the United "
            "States later overturned by DNA evidence, a mistaken eyewitness was part of the case. "
            "<bookmark mark='b'/> In 1984, in North Carolina, Jennifer Thompson picked Ronald Cotton as the man who "
            "had attacked her. By the trial she was certain, and he was convicted. In 1995 DNA evidence cleared him, "
            "after more than ten years in prison. <bookmark mark='c'/> Her very first identification, from "
            "photographs, had been slow and hesitant. <bookmark mark='d'/> That detail is the key to a 2017 review "
            "by John Wixted and Gary Wells. Confidence at trial means little: it's inflated by everything that "
            "happens after the first identification, feedback, repetition, the investigation. But initial "
            "confidence, recorded at once, under good procedures, is highly informative. "
            "<bookmark mark='e'/> Good procedures mean one suspect in a fair line-up, a warning that the culprit "
            "may not be there, a tester who doesn't know which face is the suspect, and the witness's confidence "
            "written down immediately."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def model(self):
        head = heading(r"Derivation: \ a line-up by signal detection")
        faces = VGroup(*[Circle(radius=0.32, color=GREY_B, fill_opacity=0.15) for _ in range(6)])
        faces.arrange(RIGHT, buff=0.3).move_to([-3.2, 2.0, 0])
        faces[0].set_color(LOST)
        fl = label(r"the suspect", font_size=18, color=LOST).next_to(faces[0], DOWN, buff=0.1)
        eqs = VGroup(
            MathTex(r"\text{culprit: } \mathcal{N}(d', 1) \qquad \text{every other face: } \mathcal{N}(0, 1)",
                    font_size=30),
            MathTex(r"\text{pick } \arg\max_i\, x_i \;\; \text{if} \;\; \max_i x_i > c_1", font_size=30, color=CUE),
            MathTex(r"\text{confidence} = \#\{k : \max_i x_i > c_k\}", font_size=30, color=TRACE),
            MathTex(r"\text{accuracy at level } k = \frac{\text{culprit IDs at } k}{\text{culprit IDs at } k + "
                    r"\text{innocent-suspect IDs at } k}", font_size=28, color=MODEL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-2.3, -0.5, 0])
        rows = rows_of([
            (r"each face gives a memory-match signal", GREY_A),
            (r"the witness picks the best match, \ if it is good enough", CUE),
            (r"a better match passes more criteria: \ more confidence", TRACE),
            (r"half the line-ups hold the culprit; \ in the other half, \ the suspect is innocent", MODEL),
        ], 3.8, 21, 0.3).move_to([5.0, -0.4, 0])
        tag = published_tag(r"Wixted \& Mickes (2014)")
        with self.voiceover(
            "Why should initial confidence be informative? Signal detection, from Part 12, gives the answer. "
            "<bookmark mark='a'/> Each face in a line-up of six produces a signal: how well it matches the "
            "witness's memory. The culprit's signal is drawn from a normal distribution with mean d prime; every "
            "other face, from one with mean zero. <bookmark mark='b'/> The witness picks the best-matching face, if "
            "its match passes a criterion, and otherwise says the culprit isn't there. <bookmark mark='c'/> A "
            "better match passes more criteria, and that's confidence. <bookmark mark='d'/> Now run line-ups "
            "where the culprit is present and line-ups where the suspect is innocent, equally often. At each level "
            "of confidence, ask: of the suspects picked with this confidence, what share were the culprit? That's "
            "the confidence-accuracy characteristic, the analysis Laura Mickes introduced, and the model of the "
            "line-up is John Wixted and Mickes's."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(faces), FadeIn(fl))
            vo.wait_until("a")
            self.play(Write(eqs[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(eqs[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Write(eqs[2]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Write(eqs[3]), FadeIn(rows[3]))
        self.clear_scene()

    def cac(self):
        d = load("lineup")
        head = heading(r"The confidence-accuracy characteristic")
        lv = d["levels"]
        A = axes([0.5, 5.5], [0.3, 1.0], x_length=6.4, y_length=3.8, xticks=list(lv), yticks=[0.4, 0.6, 0.8, 1.0],
                 xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{100 * v:.0f}\\%",
                 xlabel=r"the witness's confidence \ (1 = lowest)", ylabel=r"suspect IDs that are of the culprit",
                 center=[-2.6, 0.0, 0], font_size=18)
        cs = VGroup()
        for k in range(3):
            cs.add(VGroup(curve(A.ax, lv, d[f"cac{k}"], D_COL[k], 4), scatter(A.ax, lv, d[f"cac{k}"], D_COL[k], 0.07, 1.0)))
        key = legend([(D_COL[k], rf"$d' = {d['d'][k]:.1f}$: \ overall {pct(d[f'overall{k}'])}") for k in range(3)],
                     font_size=20).move_to([4.2, 1.6, 0])
        rows = rows_of([
            (rf"at the strongest memory, \ low-confidence IDs are right {pct(d['cac2'][0])} of the time, \ "
             rf"high-confidence {pct(d['cac2'][-1])}", TRACE),
            (r"the same pattern at every strength: \ confidence sorts the IDs", MODEL),
            (r"a high-confidence initial ID is strong evidence; \ a hesitant one is weak, \ and should be treated "
             r"so", CUE),
            (r"the model assumes the pristine conditions: \ biased line-ups, \ feedback and repetition break it", LOST),
        ], 5.0, 20, 0.3).move_to([4.3, -1.0, 0])
        ptag = psyche_tag(r"\texttt{memory.lineup\_cac}: \ 200{,}000 line-ups of each kind")
        with self.voiceover(
            "Here's the result for three strengths of memory. <bookmark mark='a'/> At every strength, accuracy "
            f"climbs with confidence. For the strongest memory here, a low-confidence identification is right "
            f"{spct(d['cac2'][0])} of the time, a high-confidence one {spct(d['cac2'][-1])}. "
            "<bookmark mark='b'/> Even for weak memories, the highest-confidence identifications are mostly right, "
            "because to reach that criterion the match has to be very good, and an innocent face rarely matches "
            "that well. <bookmark mark='c'/> That's the scientific basis for Wixted and Wells's conclusion, and for "
            "the field data it agrees with: a high-confidence first identification is strong evidence, and a "
            "hesitant one, like Jennifer Thompson's, is weak. <bookmark mark='d'/> The model also says what breaks "
            "it: a line-up where the suspect stands out, feedback after the choice, a second line-up. All of those "
            "raise confidence without raising the match."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(ptag))
            vo.wait_until("a")
            self.play(Create(cs[2]), FadeIn(key[2]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cs[1]), Create(cs[0]), FadeIn(key[0]), FadeIn(key[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
