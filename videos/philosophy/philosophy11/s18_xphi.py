from __future__ import annotations

from videos.philosophy.philosophy11.common import *  # noqa: F403


class XPhi(VoiceoverScene):
    def construct(self):
        card = chapter_card(17, r"Asking people", r"Whose intuitions are these?", lit=(2001,), part=PART)
        with self.voiceover("Chapter seventeen. Asking people."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.wns()
        self.replications()
        self.lesson()

    def wns(self):
        hc = history_card(2001, r"Weinberg, \ Nichols \ and Stich", r"`Normativity and Epistemic Intuitions'",
                          width=6.0, color=HIST).to_corner(UL, buff=0.35)
        vig = VGroup(label(r"the vignette:", font_size=22, color=GREY_B),
                     label(r"Jill has driven a Buick for years; \ her friend Bob believes she drives an American car.",
                           font_size=22),
                     label(r"Her Buick was stolen and replaced by a Pontiac, \ another American car.", font_size=22),
                     label(r"Does Bob really know, \ or only believe, \ that Jill drives an American car?",
                           font_size=22, color=GOAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([0, 1.0, 0])
        groups = VGroup()
        for i, (name, col, note) in enumerate([(r"Western students", BEL, r"about a quarter: \ `really knows'"),
                                               (r"East Asian students", JUST, r"more than half: \ `really knows'"),
                                               (r"South Asian students", LUCK, r"more than half: \ `really knows'")]):
            ppl = VGroup(*[person(r"", color=col, scale=0.45) for _ in range(4)]).arrange(RIGHT, buff=0.12)
            g = VGroup(ppl, label(name, font_size=20, color=col), label(note, font_size=19, color=GREY_A)).arrange(
                DOWN, buff=0.12)
            groups.add(g)
        groups.arrange(RIGHT, buff=0.9).move_to([0, -1.7, 0])
        claim = label(r"the authors' conclusion: \ epistemic intuitions vary by culture", font_size=23,
                      color=BAD).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Almost everything in this part has rested on intuitions about cases: Smith does not know; Henry does "
            "not know. Whose intuitions are these? <bookmark mark='a'/>In 2001 Jonathan Weinberg, Shaun Nichols and "
            "Stephen Stich asked students. <bookmark mark='b'/>Their vignette: Jill has driven a Buick for years, so "
            "her friend Bob believes she drives an American car. Unknown to him, her Buick was stolen and replaced "
            "by a Pontiac, also an American car. Does Bob really know that Jill drives an American car, or does he "
            "only believe it? <bookmark mark='c'/>They reported that about a quarter of Western students said he "
            "really knows, but more than half of East Asian and South Asian students did. <bookmark mark='d'/>If Gettier "
            "intuitions vary by culture, they concluded, then the method of cases tells us about our own group, not "
            "about knowledge."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(vig[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(v) for v in vig[1:]], lag_ratio=0.6), run_time=4)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(g) for g in groups], lag_ratio=0.4))
            vo.wait_until("d")
            self.play(FadeIn(claim))
        self.clear_scene()

    def replications(self):
        head = label(r"Then the replications", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        hd = [label(r"study", font_size=21, color=P.CLAIM), label(r"what it found", font_size=21, color=P.CLAIM)]
        rows = [[label(r"Nagel, \ San Juan \ and Mar (2013)", font_size=20),
                 label(r"ordinary people deny knowledge in Gettier cases, \ as philosophers do", font_size=20)],
                [label(r"Kim and Yuan (2015)", font_size=20),
                 label(r"the car case again, \ larger samples: \ no cultural difference", font_size=20)],
                [label(r"Seyedsayamdost (2015)", font_size=20),
                 label(r"`failure of replication' \ for the original findings", font_size=20)],
                [label(r"Machery et al.\ (2017)", font_size=20),
                 label(r"Brazil, \ India, \ Japan, \ the US: \ the Gettier intuition in all four", font_size=20)],
                [label(r"Cova et al.\ (2021)", font_size=20),
                 label(r"40 experimental-philosophy studies replicated: \ about 70\% held up", font_size=20)]]
        grid = ValueGrid(hd, rows, col_w=[4.4, 7.8], cell_h=0.62, font_size=20).move_to([0, -0.1, 0])
        foot = label(r"the Gettier intuition looks robust, \ perhaps universal: \ a finding about human minds",
                     font_size=24, color=OK).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Experimental philosophy then did what science is supposed to do: it checked. <bookmark mark='a'/>"
            "Jennifer Nagel and colleagues, in 2013, found that ordinary people deny knowledge in Gettier cases much "
            "as philosophers do. <bookmark mark='b'/>Minsun Kim and Yuan Yuan ran the car case again with larger "
            "samples, and found no cultural difference. Hamid Seyedsayamdost's paper had a blunt title: failure of "
            "replication. <bookmark mark='c'/>And Edouard Machery and an international team tested Gettier cases in "
            "Brazil, India, Japan and the United States, and found the Gettier intuition in all four. "
            "<bookmark mark='d'/>A large project led by Florian Cova replicated forty experimental-philosophy "
            "studies, and about seventy percent held up: a better record than in parts of psychology. "
            "<bookmark mark='e'/>So the Gettier intuition, it now seems, is robust, perhaps universal. That is itself "
            "a discovery about human minds, of the kind Dharmottara's case already hinted at."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), FadeIn(grid.rule), FadeIn(grid.rows_bg))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*grid.cell[0])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*grid.cell[1])))
            self.play(FadeIn(VGroup(*grid.cell[2])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*grid.cell[3])))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*grid.cell[4])))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def lesson(self):
        head = label(r"What are cases evidence of?", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        rows = VGroup(
            label(r"the restrictionist: \ if intuitions vary, \ the method of cases is in trouble", font_size=23,
                  color=BAD),
            label(r"Williamson, \textit{The Philosophy of Philosophy} (2007):", font_size=23, color=KNOW),
            label(r"a judgment about a case is an ordinary counterfactual judgment, \ fallible like any other",
                  font_size=22, color=GREY_A),
            label(r"Cappelen, \textit{Philosophy without Intuitions} (2012):", font_size=23, color=JUST),
            label(r"philosophers argue for their verdicts; \ they do not just report feelings", font_size=22,
                  color=GREY_A),
            label(r"the Reasoner's view: \ a case is a model; \ the checkers make the verdicts explicit",
                  font_size=24, color=GOAL)).arrange(DOWN, buff=0.28).move_to([0, -0.3, 0])
        with self.voiceover(
            "The episode left a methodological question. <bookmark mark='a'/>If intuitions about cases had varied, "
            "the method of cases would have been in trouble: so-called restrictionists still urge caution. "
            "<bookmark mark='b'/>Timothy Williamson replied that a judgment about a thought experiment is not a "
            "mysterious faculty. <bookmark mark='c'/>It is an ordinary counterfactual judgment, the kind we make all "
            "the time, and fallible in the same ways. <bookmark mark='d'/>Herman Cappelen went further. "
            "<bookmark mark='e'/>Read philosophers closely, he argued, and you find that they argue for their "
            "verdicts about cases; they do not simply report a feeling. <bookmark mark='f'/>That is the Reasoner's "
            "approach in this series. A case is a model, and each theory a checker run on it. The checkers make "
            "explicit what each verdict rests on, so we can see exactly where the theories disagree."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
