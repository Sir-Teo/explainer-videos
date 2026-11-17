from __future__ import annotations

from videos.psychology.psych29.common import *  # noqa: F403


class Body(VoiceoverScene):
    def construct(self):
        self.card()
        self.cannon()
        self.bard()
        self.interoception()

    def card(self):
        card = chapter_card(1, r"Body first?", r"Is a feeling the body perceived?",
                            lit={1884: r"James", 1885: r"Lange", 1927: r"Cannon", 1924: r"Mara\~n\'on"},
                            part=PART, scale=("brain", "mind"), marr=("what",))
        with self.voiceover("Chapter one. Body first?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def cannon(self):
        head = heading(r"Cannon's objections, \ 1927")
        items = [
            (r"1", r"cut the nerves from the viscera, \ and animals still show emotion: \ Sherrington's dogs, "
                   r"\ Cannon's own cats", BODY),
            (r"2", r"the same bodily changes come with very different emotions, \ and with fever and cold", BODY),
            (r"3", r"the viscera are poorly supplied with sensory nerves: \ we feel little of them", BODY),
            (r"4", r"visceral changes are slow, \ seconds; \ feelings can arise faster", BODY),
            (r"5", r"produce the changes artificially, \ with an injection of adrenaline, \ and people feel ``as if'' "
                   r"afraid, \ not afraid \ (Mara\~n\'on, \ 1924)", FEAR),
        ]
        rows = VGroup()
        for n, t, c in items:
            rows.add(VGroup(label(n, font_size=30, color=c), wrapped_label(t, 11.0, 25, WHITE)).arrange(
                RIGHT, buff=0.4, aligned_edge=UP))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, -0.2, 0])
        tag = historical_tag(r"Cannon (1927); \ Mara\~n\'on (1924)")
        with self.voiceover(
            "The physiologist Walter Cannon, who named homeostasis in Part 28, attacked James's theory in 1927 "
            "with five objections. <bookmark mark='a'/> First: cut the nerves that carry signals from the viscera, "
            "and animals still show emotion, as Charles Sherrington's dogs and Cannon's own cats did. "
            "<bookmark mark='b'/> Second: the same bodily changes come with very different emotions, and with "
            "fever and cold. <bookmark mark='c'/> Third: the viscera are poorly supplied with sensory nerves, so we "
            "feel little of them. <bookmark mark='d'/> Fourth: the viscera are slow, taking seconds, while a feeling "
            "can arise faster. <bookmark mark='e'/> And fifth: produce the bodily changes artificially, with an "
            "injection of adrenaline, and people report feeling as if they were afraid, not afraid. The Spanish "
            "physician Gregorio Marañón had found that in 1924."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def bard(self):
        head = heading(r"Cannon--Bard: \ in parallel")
        stim = word_chip(r"the bear", color=WHITE, font_size=24).move_to([-5.0, 0.3, 0])
        thal = word_chip(r"thalamus", color=COG, font_size=24).move_to([-1.8, 0.3, 0])
        cortex = word_chip(r"cortex: \ the felt fear", color=FEAR, font_size=22).move_to([1.8, 1.6, 0])
        body = word_chip(r"body: \ the racing heart", color=BODY, font_size=22).move_to([1.8, -1.0, 0])
        arrows = VGroup(Arrow(stim.get_right(), thal.get_left(), buff=0.1, color=GREY_B),
                        Arrow(thal.get_right(), cortex.get_left(), buff=0.1, color=FEAR),
                        Arrow(thal.get_right(), body.get_left(), buff=0.1, color=BODY))
        rows = rows_of([
            (r"Cannon and Philip Bard: \ the feeling and the bodily response are triggered together, \ by the "
             r"thalamus, \ neither causing the other", COG),
            (r"what survived: \ James was right that bodily signals shape feeling; \ Cannon was right that they "
             r"cannot be all of it", WHITE),
        ], 12.0, 24, 0.3).to_edge(DOWN, buff=0.7)
        tag = historical_tag(r"Cannon (1927); \ Bard (1928)")
        with self.voiceover(
            "Cannon and his student Philip Bard proposed an alternative. <bookmark mark='a'/> A stimulus reaches the "
            "thalamus, which triggers the felt emotion in the cortex and the bodily response at the same time. "
            "Neither causes the other. <bookmark mark='b'/> The anatomy was wrong in its details; the hypothalamus "
            "and other structures matter more than the thalamus. <bookmark mark='c'/> What survived of both is "
            "this: James was right that signals from the body shape feeling, and Cannon was right that they cannot "
            "be all of it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(stim))
            vo.wait_until("a")
            self.play(FadeIn(thal), GrowArrow(arrows[0]))
            self.play(GrowArrow(arrows[1]), GrowArrow(arrows[2]), FadeIn(cortex), FadeIn(body))
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def interoception(self):
        head = heading(r"James's return: \ interoception")
        rows = rows_of([
            (r"interoception: \ sensing the body's internal state, \ heartbeat, \ breathing, \ gut, \ temperature",
             BODY),
            (r"the insula receives these signals, \ and is active when people report feelings", BODY),
            (r"people differ in how accurately they sense their own heartbeat; \ whether the better counters feel "
             r"more intensely is debated, \ because the counting tasks themselves are disputed", COG),
            (r"Damasio's somatic markers: \ bodily signals as a summary of past outcomes, \ guiding choices "
             r"\ (contested)", FEAR),
            (r"the modern form of James: \ feelings as the brain's reading of the body \ (chapter five, \ and "
             r"the frontier)", WHITE),
        ], 12.2, 25, 0.38).move_to([0, -0.2, 0])
        tag = published_tag(r"Craig (2009); \ Damasio (1994)")
        with self.voiceover(
            "James's idea came back under a new name. <bookmark mark='a'/> Interoception is the sensing of the "
            "body's internal state: heartbeat, breathing, the gut, temperature. <bookmark mark='b'/> A region called "
            "the insula receives these signals, and is active when people report feelings. "
            "<bookmark mark='c'/> People differ in how accurately they can count their own heartbeats, though "
            "whether better counters feel more intensely is debated, partly because the counting tasks themselves "
            "are disputed. <bookmark mark='d'/> Antonio Damasio proposed that bodily signals act as somatic "
            "markers, a summary of past outcomes that guides choices; that idea is contested. "
            "<bookmark mark='e'/> And the modern form of James's theory treats feelings as the brain's reading of "
            "the body, which we'll meet again in chapter five and at the frontier."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
