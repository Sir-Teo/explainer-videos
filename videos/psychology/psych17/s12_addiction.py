from __future__ import annotations

import numpy as np

from videos.psychology.psych17.common import *  # noqa: F403


class Addiction(VoiceoverScene):
    def construct(self):
        self.card()
        self.redish()

    def card(self):
        card = chapter_card(11, r"When the signal is hijacked", r"What if an error cannot be predicted away?",
                            lit={2004: r"Redish"}, part=PART, scale=("molecule", "circuit", "person"),
                            marr=("what", "how"))
        with self.voiceover("Chapter eleven. When the signal is hijacked."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def redish(self):
        d = load("redish")
        head = heading(r"A model of addiction, \ Redish, \ 2004")
        eqs = VGroup(
            MathTex(r"\text{natural reward:}\quad \delta = r + \gamma V' - V \;\to\; 0", font_size=36),
            MathTex(r"\text{drug:}\quad \delta = \max\big(r + \gamma V' - V + D,\ D\big) \;\geq\; D", font_size=36,
                    color=INHIB),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([0, 2.0, 0])
        A = axes([0, 200], [0, 12], x_length=6.4, y_length=3.0, xticks=[0, 50, 100, 150, 200], yticks=[0, 4, 8, 12],
                 xlabel=r"uses", ylabel=r"value of the cue", center=[-2.6, -1.1, 0])
        ax = A.ax
        x = np.arange(200)
        cn = curve(ax, x, d["natural"], REWARD, 4)
        cd = curve_in(ax, x, np.minimum(d["drug"], 12), INHIB, 4)
        lg = legend([(REWARD, r"food: \ value levels off"), (INHIB, r"drug: \ value keeps rising")],
                    font_size=20)
        lg.next_to(ax.c2p(0, 12), RIGHT, buff=0.4).shift(DOWN * 0.3)
        rows = rows_of([
            (r"cocaine and amphetamine raise dopamine directly, \ whatever was predicted", INHIB),
            (r"so the error never falls to zero, \ and the value of drug-related cues grows without limit", WHITE),
            (r"a prediction: \ no blocking for drug rewards; \ evidence is mixed", GREY_A),
            (r"addiction is far more than this; \ Part 41 takes it up", YOU),
        ], 4.6, 23, 0.32).move_to([4.4, -1.1, 0])
        keep_in_frame(rows)
        tag = published_tag(archive.REDISH_2004.cite)
        tag2 = psyche_tag(r"computed: \ \texttt{rl.redish}, \ $D$ = 0.5")
        with self.voiceover(
            "If dopamine is a teaching signal, what happens when a drug produces it directly? In 2004 David Redish "
            "wrote the simplest answer down. <bookmark mark='a'/> For a natural reward, the error shrinks as the cue "
            "comes to predict it, and learning stops: the value levels off. <bookmark mark='b'/> Drugs such as "
            "cocaine and amphetamine raise dopamine pharmacologically, whatever the brain predicted. In Redish's "
            "model the drug adds a surge that learning can't cancel: the error never falls below it. "
            "<bookmark mark='c'/> So the value of everything that leads to the drug keeps rising, use after use, "
            "far beyond any natural reward. <bookmark mark='d'/> It makes a testable prediction, that drug rewards "
            "shouldn't show blocking, and tests have given mixed results. <bookmark mark='e'/> Addiction involves much "
            "more: withdrawal, stress, habits that outlast pleasure, and a person's whole situation. Part 41 takes it "
            "up. But the model shows why a learning system built on prediction errors is vulnerable to anything that "
            "fakes one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), FadeIn(tag2))
            vo.wait_until("a")
            self.play(Write(eqs[0]), Create(cn), FadeIn(lg[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Write(eqs[1]), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Create(cd), FadeIn(lg[1]), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
