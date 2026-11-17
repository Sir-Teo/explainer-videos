from __future__ import annotations

from videos.psychology.psych4.common import *  # noqa: F403

# six findings from the Ledger so far, one line each; the verdicts are read from the Ledger, not written here
QUIZ = [
    ("hick_law", r"The more alternatives there are, the longer a choice takes."),
    ("flag_priming", r"A glimpse of a national flag shifts political views."),
    ("pygmalion", r"Telling teachers a pupil will bloom raises the pupil's IQ."),
    ("currency_priming", r"A banknote on the screen makes people favour the existing order."),
    ("barnum", r"People rate a description written for everyone as accurate for them."),
    ("imagined_contact", r"Imagining a friendly meeting with an outsider reduces prejudice."),
]


class Survives(VoiceoverScene):
    def construct(self):
        self.card()
        self.quiz()
        self.pattern()

    def card(self):
        card = chapter_card(11, r"What survives", r"Can you tell in advance which findings will hold?", lit=(),
                            part=PART, scale=("group",), marr=("what",))
        with self.voiceover(
            "Chapter eleven. What survives."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def quiz(self):
        stage = demo_stage(13.2, 6.5, tag=r"On you", center=[0, -0.15, 0])
        ask = label(r"Six findings, each published. \ Which would you bet on?", font_size=30, color=P.ACCENT)
        ask.move_to([-0.6, 2.35, 0])
        ring = countdown_ring(0.34).move_to([5.6, 2.35, 0])
        rows = VGroup()
        for i, (key, text) in enumerate(QUIZ):
            f = ledger.get(key)
            y = 1.45 - 0.72 * i
            num = label(rf"{i + 1}.", font_size=28, color=GREY_A).move_to([-6.0, y, 0])
            line = label(text, font_size=27, color=WHITE).move_to([-5.6, y, 0], aligned_edge=LEFT)
            verdict = label(f.status, font_size=27, color=STATUS_COLOR[f.status]).move_to([6.1, y, 0], aligned_edge=RIGHT)
            if line.get_right()[0] > verdict.get_left()[0] - 0.3:
                line.scale_to_fit_width(verdict.get_left()[0] - 0.3 + 5.6).move_to([-5.6, y, 0], aligned_edge=LEFT)
            rows.add(VGroup(num, line, verdict))
        src = note(r"verdicts: the Replication Ledger, Parts 1 to 4").move_to([0, -3.05, 0])
        with self.voiceover(
            "Your turn again, and this time you have something to bet with. <bookmark mark='a'/> Here are six "
            "findings. Every one was published in a good journal, with a significant result. Some held up when "
            "others ran them again. Some didn't. Read them, and decide which you'd put money on. "
            "<bookmark mark='b'/> One. The more alternatives there are, the longer a choice takes. Two. A "
            "glimpse of a national flag shifts political views. Three. Telling teachers that a pupil will bloom "
            "raises the pupil's IQ. Four. A banknote on the screen makes people favour the existing order. "
            "Five. People rate a description written for everyone as accurate for them. Six. Imagining a "
            "friendly meeting with an outsider reduces prejudice. <bookmark mark='c'/> Make your six bets."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(ask))
            vo.wait_until("a")
            for r_ in rows:
                VGroup(r_[0], r_[1]).set_opacity(0.4)
            self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1]), shift=RIGHT * 0.1) for r_ in rows], lag_ratio=0.3),
                      run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[VGroup(r_[0], r_[1]).animate.set_opacity(1.0) for r_ in rows], lag_ratio=1.0),
                      run_time=24.0)
            vo.wait_until("c")
            self.play(FadeIn(ring))
        self.play(ring.t.animate.set_value(0.0), run_time=5.0, rate_func=linear)
        with self.voiceover(
            "The record. <bookmark mark='a'/> Hick's law: replicated, many times over, since 1952. "
            "<bookmark mark='b'/> The flag: failed, in thirty-six laboratories at once. "
            "<bookmark mark='c'/> The teachers: replicated, but much smaller than the famous version, and mostly "
            "when the teachers had only just met the pupils. <bookmark mark='d'/> The banknote: failed. "
            "<bookmark mark='e'/> The description: replicated, since 1949. <bookmark mark='f'/> The imagined "
            "meeting: contested; something is there in the pooled data, and it's far smaller than first "
            "reported. Count your score. And then ask yourself how you knew."
        ) as vo:
            self.play(FadeOut(ring), FadeIn(src))
            for mark, r_ in zip("abcdef", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r_[2], shift=LEFT * 0.15))
        self.clear_scene()

    def pattern(self):
        o, c, dr = archive.OSC_2015.data, archive.CAMERER_2018.data, archive.DREBER_2015.data
        head = heading(r"What the survivors have in common")
        good = VGroup(
            label(r"tends to hold", font_size=38, color=STATUS_COLOR["replicated"]),
            label(r"a large effect, visible in most people", font_size=31, color=WHITE),
            label(r"a tiny p-value in the original", font_size=31, color=WHITE),
            label(r"many people, many trials each", font_size=31, color=WHITE),
            label(r"found again by independent laboratories", font_size=31, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        poor = VGroup(
            label(r"tends to fall", font_size=38, color=STATUS_COLOR["failed"]),
            label(r"a slight cue, a large change in behaviour", font_size=31, color=WHITE),
            label(r"$p$ just under .05", font_size=31, color=WHITE),
            label(r"a small sample, one measurement each", font_size=31, color=WHITE),
            label(r"surprising, and reported once", font_size=31, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        cols = VGroup(good, poor).arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to([0, 0.8, 0])
        if cols.width > 13.2:
            cols.width = 13.2
        facts = VGroup(
            wrapped_label(rf"In the hundred replications, the best predictor of success was "
                          rf"{o['predictor'].split(',')[0]}.", 12.4, 26, GREY_A),
            wrapped_label(rf"In {c['studies']} later replications, what researchers expected beforehand was "
                          r"strongly related to what happened; \ and in betting markets on "
                          rf"{dr['studies']} of the hundred, the prices predicted the outcomes well.", 12.4, 26,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.7)
        src = published_tag(rf"{archive.OSC_2015.cite}; \ {archive.CAMERER_2018.cite}; \ {archive.DREBER_2015.cite}")
        with self.voiceover(
            "There's a pattern, and you probably used it. <bookmark mark='a'/> The findings that hold tend to "
            "be big enough to see in most of the people tested. Their original evidence was strong, with a "
            "p-value far below the line. They rest on many people, or many trials from each person. And "
            "they've been found again by laboratories with no stake in them. <bookmark mark='b'/> The findings "
            "that fall tend to be the ones that made the best stories. A slight cue produces a large change in "
            "something important. The p-value is just under point oh five. The sample is small. And the result "
            "was surprising, which is a polite word for unlikely. <bookmark mark='c'/> This isn't hindsight. In "
            "the hundred replications, the best predictor of success was the strength of the original evidence. "
            "<bookmark mark='d'/> And psychologists can tell. When researchers were asked to bet beforehand on "
            "which studies would replicate, their bets were good. So the knowledge was in the field all along. "
            "People could smell which results were too good. What was missing was any step in the process "
            "where that judgement was asked for, before the paper was printed and the textbook was written."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.1) for m in good], lag_ratio=0.6), run_time=9.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.1) for m in poor], lag_ratio=0.6), run_time=9.0)
            vo.wait_until("c")
            self.play(FadeIn(facts[0]), FadeIn(src))
            vo.wait_until("d")
            self.play(FadeIn(facts[1]))
        self.clear_scene()
