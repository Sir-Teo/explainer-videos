from __future__ import annotations

from videos.psychology.psych34.common import *  # noqa: F403

# Milgram's variations, as reported in Obedience to Authority (1974) and its summaries: share to 450 volts
VARIATIONS = [
    (r"two peers refuse", 10.0, GOOD),
    (r"orders by telephone", 20.5, CROWD),
    (r"hand pressed to the plate", 30.0, CROWD),
    (r"Bridgeport, \ not Yale", 47.5, CROWD),
    (r"the 1963 study", 65.0, AUTH),
]


class Obedience(VoiceoverScene):
    def construct(self):
        self.card()
        self.variations()
        self.meta()
        self.burger()
        self.archives()
        self.prods()

    def card(self):
        card = chapter_card(3, r"Obedience", r"What made people go on, \ and what made them stop?",
                            lit={1963: r"Milgram", 2009: r"Burger", 2012: r"Perry", 2014: r"Haslam et al."},
                            part=PART, scale=("person", "group"), marr=("what", "why"))
        with self.voiceover("Chapter three. Obedience."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def variations(self):
        head = heading(r"Not one result, \ but a dose-response curve")
        A = axes([0, 100], [-0.6, 4.6], x_length=4.6, y_length=4.2, xticks=[0, 25, 50, 75, 100], yticks=None,
                 xfmt=lambda v: f"{v:.0f}\\%", xlabel=r"share who went to 450 volts", center=[-0.9, -0.4, 0],
                 font_size=15)
        bars_ = VGroup()
        for k, (name, v, c) in enumerate(VARIATIONS):
            lo, hi = A.ax.c2p(0, k), A.ax.c2p(v, k)
            r = Rectangle(width=max(hi[0] - lo[0], 1e-3), height=0.5, stroke_width=0, fill_color=c,
                          fill_opacity=0.85).move_to([(lo[0] + hi[0]) / 2, lo[1], 0])
            bars_.add(VGroup(r, label(name, font_size=16, color=c).next_to(A.ax.c2p(0, k), LEFT, buff=0.2),
                             label(rf"{v:g}\%", font_size=17, color=c).next_to(r, RIGHT, buff=0.1)))
        rows = rows_of([
            (r"Milgram ran his procedure in many variations, \ most with 40 men each", WHITE),
            (r"obedience fell as the learner came closer, \ as the experimenter moved away, \ and as Yale's name "
             r"was removed", CROWD),
            (r"it fell furthest when two other ``teachers'' refused: \ 4 of 40 went on", GOOD),
            (r"so the 65\% was not a constant of human nature: \ it was one point on a curve the situation sets", YOU),
        ], 4.6, 19, 0.32).move_to([4.6, -0.3, 0])
        tag = historical_tag(r"Milgram (1963, \ 1974)")
        with self.voiceover(
            "The sixty-five percent is the number everyone remembers. But Milgram ran his procedure in many "
            "variations. <bookmark mark='a'/> Most had forty men each, and they were never meant to give one "
            "answer. <bookmark mark='b'/> When the teacher had to hold the learner's hand onto a shock plate, thirty "
            "percent went to the end. When the experimenter gave his orders by telephone, about twenty. When the "
            "study moved from Yale to an office building in Bridgeport, forty-seven and a half. "
            "<bookmark mark='c'/> It fell furthest when two other teachers, both confederates, refused to go on. "
            "Four of the forty continued. <bookmark mark='d'/> So the sixty-five percent wasn't a constant of human "
            "nature. It was one point on a curve that the situation sets."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(bars_[4]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.15) for b_ in bars_[1:4][::-1]], lag_ratio=0.6),
                      FadeIn(rows[1]), run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(bars_[0], shift=RIGHT * 0.15), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def meta(self):
        head = heading(r"All the conditions at once")
        big = VGroup(label(r"43.6\%", font_size=72, color=AUTH),
                     label(r"of 740 men in 21 conditions went to 450 volts", font_size=22, color=GREY_A))
        big.arrange(DOWN, buff=0.2).move_to([-3.4, 0.6, 0])
        rng_ = label(r"range: \ 0\% to 92.5\%", font_size=24, color=CROWD).next_to(big, DOWN, buff=0.5)
        rows = rows_of([
            (r"Haslam, \ Loughnan and Perry, \ 2014: \ the whole programme was 23 conditions and 780 people; \ 21 "
             r"conditions, \ 740 people, \ ended at the top switch or before it", WHITE),
            (r"across them, \ 43.6\% obeyed to the end, \ from none in some conditions to 92.5\% in one", AUTH),
            (r"the strongest predictors were features of the experimenter: \ how directive, \ how legitimate, \ how "
             r"consistent; \ and of the teacher's closeness to the learner", CROWD),
            (r"the majority of Milgram's participants, \ taken together, \ disobeyed", GOOD),
        ], 6.2, 20, 0.34).move_to([3.2, -0.3, 0])
        tag = published_tag(r"Haslam, \ Loughnan \& Perry (2014)")
        with self.voiceover(
            "In 2014 Haslam, Loughnan and Perry coded every condition Milgram ran. "
            "<bookmark mark='a'/> The whole programme was twenty-three conditions and seven hundred and eighty "
            "people. Twenty-one conditions, with seven hundred and forty people, could be compared. "
            "<bookmark mark='b'/> Across them, forty-three point six percent obeyed to the end, from none at all in "
            "some conditions to ninety-two and a half percent in one. <bookmark mark='c'/> The strongest predictors "
            "were features of the experimenter, how directive, how legitimate and how consistent he was, and how "
            "close the teacher was to the learner. <bookmark mark='d'/> Taken together, most of the people in "
            "Milgram's studies disobeyed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(big))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rng_), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def burger(self):
        head = heading(r"A partial replication")
        A = axes([-0.6, 1.6], [0, 100], x_length=4.4, y_length=3.8, xticks=None, yticks=[0, 25, 50, 75, 100],
                 yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"went past 150 volts", center=[-3.9, -0.3, 0], font_size=15)
        b = bars(A.ax, [0, 1], [82.5, 70.0], [AUTH, CROWD], width=0.6)
        names = VGroup(label(r"Milgram, \ 1960s", font_size=16, color=AUTH).next_to(A.ax.c2p(0, 0), DOWN, buff=0.2),
                       label(r"Burger, \ 2009", font_size=16, color=CROWD).next_to(A.ax.c2p(1, 0), DOWN, buff=0.2))
        tops = VGroup(label(r"82.5\%", font_size=18, color=AUTH).next_to(A.ax.c2p(0, 82.5), UP, buff=0.1),
                      label(r"70\%", font_size=18, color=CROWD).next_to(A.ax.c2p(1, 70), UP, buff=0.1))
        rows = rows_of([
            (r"Burger, \ 2009: \ 70 adults; \ the procedure stopped at 150 volts, \ when the learner first "
             r"asks to be released", WHITE),
            (r"in Milgram's matching condition, \ 79\% of those who passed 150 volts went on to 450", MODEL),
            (r"70\% went past 150, \ against Milgram's 82.5\%: \ not a significant difference", CROWD),
            (r"a commentary called it ``Obedience Lite'': \ the most important part of the original was never run "
             r"again", YOU),
        ], 6.4, 20, 0.36).move_to([3.0, -0.3, 0])
        tag = published_tag(r"Burger (2009)")
        with self.voiceover(
            "No ethics board would allow the full procedure today, but one psychologist found a way to run part of "
            "it. <bookmark mark='a'/> In 2009 Burger tested seventy adults, and stopped every session at a "
            "hundred and fifty volts, the point at which the learner first asks to be released. "
            "<bookmark mark='b'/> His reason: in Milgram's matching condition, seventy-nine percent of those who "
            "passed that point went on to the end. <bookmark mark='c'/> Seventy percent of Burger's participants "
            "went past a hundred and fifty volts, against Milgram's eighty-two and a half, a difference that wasn't "
            "significant. <bookmark mark='d'/> A commentary in the same issue called it obedience lite. The most "
            "important part of the original was never run again."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(b[0], DOWN), GrowFromEdge(b[1], DOWN), FadeIn(tops), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def archives(self):
        head = heading(r"What the archives show")
        rows = rows_of([
            (r"Gina Perry, \ \emph{Behind the Shock Machine}, \ 2012: \ the tapes and papers at Yale", WHITE),
            (r"the experimenter did not keep to the script: \ he improvised prods and pressed some people beyond "
             r"the four", AUTH),
            (r"Milgram's own unpublished questionnaires, \ 656 of them, \ reanalysed: \ only about half the "
             r"participants fully believed the shocks were real", CROWD),
            (r"those who believed the learner was in pain were about two and a half times as likely to refuse", GOOD),
            (r"so the 65\% mixes obedience with doubt about whether anything bad was happening", YOU),
        ], 12.4, 22, 0.36).move_to([0, -0.3, 0])
        tag = published_tag(r"Perry (2012); \ Perry et al.")
        with self.voiceover(
            "Then the archives were opened. <bookmark mark='a'/> In 2012 the psychologist Gina Perry published "
            "Behind the Shock Machine, built on the tapes and papers Milgram left at Yale. <bookmark mark='b'/> The "
            "experimenter didn't keep to the script. He improvised prods, and pressed some people beyond the "
            "four. <bookmark mark='c'/> Perry and her colleagues later reanalysed six hundred and fifty-six "
            "questionnaires that Milgram had collected but never published. Only about half of the participants "
            "had fully believed the shocks were real. <bookmark mark='d'/> And those who believed the learner was "
            "in pain were about two and a half times as likely to refuse. <bookmark mark='e'/> So the sixty-five "
            "percent mixes obedience with doubt about whether anything bad was happening at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def prods(self):
        head = heading(r"Obedience, \ or engaged followership?")
        rows = rows_of([
            (r"Milgram's account: \ in the ``agentic state'' people hand responsibility to the authority and simply "
             r"follow", AUTH),
            (r"but the only prod that is a true order, \ ``you have no other choice, \ you must go on'', \ was the "
             r"least effective, \ in Burger's study and in analyses of Milgram's recordings", CROWD),
            (r"Haslam, \ Reicher and Millard, \ 2015: \ the procedure restaged in immersive digital realism with "
             r"actors: \ after the fourth prod, \ nearly everyone refused", GOOD),
            (r"Haslam and Reicher's reading, \ 2012: \ people went on when they identified with the experimenter's "
             r"scientific cause, \ as engaged followers, \ not as automata", YOU),
            (r"what is solid: \ ordinary people will hurt someone at an authority's request in some situations; \ "
             r"why they do is still argued", MODEL),
        ], 12.4, 22, 0.34).move_to([0, -0.3, 0])
        tag = published_tag(r"Haslam \& Reicher (2012); \ Haslam, \ Reicher \& Millard (2015)")
        with self.voiceover(
            "Why did people go on? <bookmark mark='a'/> Milgram's answer was the agentic state: people hand "
            "responsibility to the authority, and simply follow. <bookmark mark='b'/> But the only prod that is a "
            "true order, you have no other choice, you must go on, was the least effective of the four, in Burger's "
            "study and in analyses of Milgram's own recordings. <bookmark mark='c'/> In 2015 Alex Haslam, Stephen Reicher and "
            "Millard restaged the procedure with actors in immersive digital realism. After the fourth prod, nearly "
            "everyone refused. <bookmark mark='d'/> Haslam and Reicher's reading is that people went on when they "
            "identified with the experimenter's scientific cause: engaged followers, not automata. "
            "<bookmark mark='e'/> What's solid is that ordinary people will hurt someone at an authority's request "
            "in some situations. Why they do is still argued."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
