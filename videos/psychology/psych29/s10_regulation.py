from __future__ import annotations

from videos.psychology.psych29.common import *  # noqa: F403


class Regulation(VoiceoverScene):
    def construct(self):
        self.card()
        self.stress()
        self.process()
        self.gross()

    def card(self):
        card = chapter_card(9, r"Stress and regulation", r"Can people change what they feel?",
                            lit={1956: r"Selye", 1984: r"Lazarus \& Folkman", 1998: r"Gross"},
                            part=PART, scale=("brain", "mind"), marr=("what", "how"))
        with self.voiceover("Chapter nine. Stress and regulation."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def stress(self):
        head = heading(r"Stress: \ a loop, \ and an appraisal")
        nodes = VGroup(*[word_chip(t, color=c, font_size=20) for t, c in (
            (r"hypothalamus", COG), (r"pituitary", COG), (r"adrenal cortex", BODY), (r"cortisol", BODY))])
        pos = [[-3.9, 1.4, 0], [-1.2, 1.4, 0], [-1.2, -0.8, 0], [-3.9, -0.8, 0]]
        for n_, p in zip(nodes, pos):
            n_.move_to(p)
        ends = [(nodes[0].get_right(), nodes[1].get_left()), (nodes[1].get_bottom(), nodes[2].get_top()),
                (nodes[2].get_left(), nodes[3].get_right()), (nodes[3].get_top(), nodes[0].get_bottom())]
        arrows = VGroup(*[Arrow(p0, p1, buff=0.12, color=BODY if i < 3 else UNPL, stroke_width=3)
                          for i, (p0, p1) in enumerate(ends)])
        fb = label(r"negative feedback \ (Part 10)", font_size=17, color=UNPL).next_to(arrows[3], LEFT, buff=0.1)
        rows = rows_of([
            (r"Hans Selye: \ the body's general response to demands, \ through the hormone loop of Part 10", BODY),
            (r"short bursts mobilize energy; \ cortisol raised for months is linked to worse sleep, \ memory and "
             r"health", UNPL),
            (r"Lazarus and Folkman, \ 1984: \ stress is an appraisal too, \ of a demand against one's resources "
             r"to meet it", COG),
            (r"coping: \ changing the problem, \ or changing how one feels about it", WHITE),
        ], 5.6, 21, 0.32).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Selye (1956); \ Lazarus \& Folkman (1984)")
        with self.voiceover(
            "Stress is where emotion meets the hormone loops of Part 10. <bookmark mark='a'/> Hans Selye described "
            "the body's general response to demands: the hypothalamus signals the pituitary, the pituitary the "
            "adrenal cortex, which releases cortisol, which in turn damps the loop. <bookmark mark='b'/> Short "
            "bursts mobilize energy and help. Cortisol raised for months is linked to worse sleep, memory and "
            "health. <bookmark mark='c'/> Richard Lazarus and Susan Folkman added in 1984 that stress is itself an "
            "appraisal: of a demand, weighed against one's resources to meet it. <bookmark mark='d'/> And coping "
            "comes in two kinds: changing the problem, or changing how one feels about it. The second is emotion "
            "regulation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(n_) for n_ in nodes], lag_ratio=0.2),
                      LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), FadeIn(fb))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def process(self):
        head = heading(r"Gross's process model")
        stages = [(r"situation", r"selection"), (r"situation", r"modification"), (r"attention", r"deployment"),
                  (r"appraisal", r"cognitive change"), (r"response", r"modulation")]
        chips = VGroup()
        for top, bottom in stages:
            chips.add(VGroup(word_chip(top, color=WHITE, font_size=20, width=2.1),
                             label(bottom, font_size=17, color=COG)).arrange(DOWN, buff=0.15))
        chips.arrange(RIGHT, buff=0.4).move_to([0, 1.3, 0])
        arr = VGroup(*[Arrow(a[0].get_right(), b[0].get_left(), buff=0.05, color=GREY_B, stroke_width=3,
                             max_tip_length_to_length_ratio=0.25) for a, b in zip(chips, chips[1:])])
        early = Brace(VGroup(*chips[:4]), DOWN, color=PLEAS)
        late = Brace(chips[4], DOWN, color=UNPL)
        el = label(r"before the response: \ reappraisal lives here", font_size=18, color=PLEAS).next_to(early, DOWN,
                                                                                                    buff=0.1)
        ll = label(r"after: \ suppression", font_size=18, color=UNPL).next_to(late, DOWN, buff=0.1)
        rows = rows_of([
            (r"James Gross: \ an emotion unfolds over time, \ and can be changed at each step: \ choosing the "
             r"situation, \ changing it, \ looking elsewhere, \ rethinking what it means, \ or holding back the "
             r"response", WHITE),
        ], 12.2, 23, 0.3).to_edge(DOWN, buff=0.7)
        tag = published_tag(r"Gross (1998)")
        with self.voiceover(
            "James Gross organized regulation by when it acts. <bookmark mark='a'/> An emotion unfolds over time, "
            "and each step can be changed: choosing the situation, changing it, looking elsewhere, rethinking what "
            "it means, or holding back the response once it has begun. <bookmark mark='b'/> The early strategies "
            "act before the response; reappraisal, rethinking the meaning, is the best studied. "
            "<bookmark mark='c'/> Suppression acts after, on the expression alone."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(c) for c in chips], lag_ratio=0.2),
                      LaggedStart(*[GrowArrow(a) for a in arr], lag_ratio=0.2))
            vo.wait_until("a")
            self.play(FadeIn(rows))
            vo.wait_until("b")
            self.play(GrowFromCenter(early), FadeIn(el))
            vo.wait_until("c")
            self.play(GrowFromCenter(late), FadeIn(ll))
        self.clear_scene()

    def gross(self):
        head = heading(r"A disgusting film, \ 1998")
        cols = VGroup()
        table = [(r"", r"felt disgust", r"showed disgust", r"body's arousal"),
                 (r"reappraise", r"less", r"less", r"no increase"),
                 (r"suppress", r"no less", r"less", r"more")]
        colors = {r"less": PLEAS, r"no increase": PLEAS, r"no less": UNPL, r"more": UNPL}
        grid = VGroup()
        for i, row in enumerate(table):
            for j, cell_ in enumerate(row):
                col = WHITE if (i == 0 or j == 0) else colors.get(cell_, WHITE)
                grid.add(label(cell_, font_size=22 if i else 20, color=col if i else GREY_B).move_to(
                    [-4.6 + 2.6 * j, 1.6 - 0.8 * i, 0]))
        rows = rows_of([
            (r"Gross, \ 1998: \ 120 people watched a disgusting film; \ some were told to watch it as a doctor "
             r"would, \ some to hide their feelings, \ some just to watch", WHITE),
            (r"reappraisal lowered felt disgust; \ suppression hid the face, \ left the feeling, \ and raised "
             r"sympathetic arousal", COG),
            (r"later work: \ habitual reappraisers report more positive emotion and better well-being; \ habitual "
             r"suppressors, \ less, \ in correlational data", BODY),
            (r"reappraisal is a core skill of cognitive behavioural therapy \ (Part 42)", PLEAS),
        ], 12.2, 23, 0.3).move_to([0, -1.6, 0])
        tag = published_tag(r"Gross (1998); \ Gross \& John (2003)")
        with self.voiceover(
            "Gross compared the two directly in 1998. <bookmark mark='a'/> A hundred and twenty people watched a "
            "disgusting film of a medical procedure. Some were told to watch it with the detachment of a doctor, "
            "some to hide their feelings so that nobody could tell, and some just to watch. "
            "<bookmark mark='b'/> Reappraisal lowered the disgust people felt and showed. Suppression hid the face, "
            "but left the feeling where it was, and raised the body's sympathetic arousal. "
            "<bookmark mark='c'/> In later correlational work by Gross and Oliver John, people who habitually "
            "reappraise report more positive emotion and better well-being, and habitual suppressors less. "
            "<bookmark mark='d'/> Reappraisal is now a core skill taught in cognitive behavioural therapy, in Part "
            "42."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(grid[:4]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(grid[4:]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
