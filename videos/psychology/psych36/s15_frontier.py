from __future__ import annotations

from videos.psychology.psych36.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.crowds()
        self.open_questions()

    def card(self):
        card = chapter_card(14, r"Frontier: \ bias in crowds", r"Is implicit bias a property of people, \ or of places?",
                            lit={2017: r"Payne et al.", 2020: r"Connor \& Evers"}, part=PART,
                            scale=("person", "society"), marr=("what",))
        with self.voiceover("Chapter fourteen. Frontier: bias in crowds."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def crowds(self):
        d = load("iat")
        head = heading(r"The bias of crowds")
        A = axes([-0.3, 1.1], [0, 1.0], x_length=5.4, y_length=2.6, xticks=[0, 0.5, 1.0], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"$D$ score", center=[-3.3, 0.85, 0], font_size=15)
        d1 = np.asarray(d["d1"], float)
        edges = np.linspace(-0.3, 1.1, 29)
        h, _ = np.histogram(d1, bins=edges)
        mids = (edges[:-1] + edges[1:]) / 2
        hb = bars(A.ax, mids, h / h.max() * 0.9, MODEL, width=0.045, opacity=0.6)
        mean = DashedLine(A.ax.c2p(d["mean_d"], 0), A.ax.c2p(d["mean_d"], 1.0), color=GOOD, stroke_width=3)
        ml = label(r"the crowd's mean: \ stable", font_size=15, color=GOOD).next_to(A.ax.c2p(d["mean_d"], 1.0), UP,
                                                                                 buff=0.08)
        spread = label(r"each person: \ a noisy draw", font_size=15, color=MODEL).move_to(A.ax.c2p(0.95, 0.6))
        rows = rows_of([
            (r"Payne, \ Vuletich and Lundberg, \ 2017: \ implicit measures may describe situations more than "
             r"persons: \ like a wisdom of crowds, \ averages are stable while individuals fluctuate", WHITE),
            (r"averaged over a city or a region, \ scores are far steadier than any one person's from week to "
             r"week", CROWD),
            (r"Connor and Evers, \ 2020: \ the same data fit an individual trait measured with a lot of error", AUTH),
            (r"Psyche cannot settle it: \ its people have both a trait and a state, \ and the test sees their sum", YOU),
        ], 12.4, 20, 0.24).move_to([0, -2.3, 0])
        tag = published_tag(r"Payne, \ Vuletich \& Lundberg (2017); \ Connor \& Evers (2020)")
        with self.voiceover(
            "What is an implicit score a score of? <bookmark mark='a'/> In 2017 Keith Payne and colleagues proposed "
            "the bias of crowds. Implicit measures may describe situations more than persons. Like a wisdom of "
            "crowds, averages are stable while individuals fluctuate. <bookmark mark='b'/> Averaged over a city or "
            "a region, scores are far steadier than any one person's from week to week. "
            "<bookmark mark='c'/> In 2020 Connor and Evers replied that the same data fit an individual "
            "trait measured with a lot of error. <bookmark mark='d'/> Psyche can't settle it. Its people have both "
            "a trait and a state, and the test sees their sum."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(hb))
            vo.wait_until("a")
            self.play(Create(mean), FadeIn(ml), FadeIn(spread), FadeIn(rows[0]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def open_questions(self):
        head = heading(r"Open questions")
        rows = rows_of([
            (r"what do implicit measures measure: \ people, \ places, \ or both?", MODEL),
            (r"which interventions change discriminatory behaviour, \ in the field, \ for longer than a week?", GOOD),
            (r"why has hiring discrimination against Black applicants not declined while expressed prejudice has?",
             AUTH),
            (r"how do small biases at each step combine into large gaps, \ and where should they be measured?", PERSON),
            (r"when does contact help, \ and when does it make things worse?", YOU),
        ], 12.4, 24, 0.46).move_to([0, -0.2, 0])
        with self.voiceover(
            "So, open questions. <bookmark mark='a'/> What do implicit measures measure: people, places, or both? "
            "<bookmark mark='b'/> Which interventions change discriminatory behaviour, in the field, for longer "
            "than a week? <bookmark mark='c'/> Why has hiring discrimination against Black applicants not declined, "
            "while expressed prejudice has? <bookmark mark='d'/> How do small biases at each step combine into "
            "large gaps, and where should they be measured? <bookmark mark='e'/> And when does contact help, and "
            "when does it make things worse?"
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
