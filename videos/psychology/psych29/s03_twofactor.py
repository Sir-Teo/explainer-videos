from __future__ import annotations

from videos.psychology.psych29.common import *  # noqa: F403


class TwoFactor(VoiceoverScene):
    def construct(self):
        self.card()
        self.suproxin()
        self.inference()
        self.record()
        self.bridge()

    def card(self):
        card = chapter_card(2, r"Two factors", r"Is an emotion arousal plus a label?",
                            lit={1962: r"Schachter \& Singer", 1974: r"Dutton \& Aron", 1979: r"Marshall \& Zimbardo"},
                            part=PART, scale=("mind", "person"), marr=("what", "how"))
        with self.voiceover("Chapter two. Two factors."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def suproxin(self):
        head = heading(r"Suproxin, \ 1962")
        conds = VGroup()
        for t, d, c in ((r"informed", r"told the real side effects: \ racing heart, \ flushing, \ tremor", PLEAS),
                        (r"ignorant", r"told nothing about side effects", FACE),
                        (r"misinformed", r"told of side effects it does not have: \ numb feet, \ itching", FACE),
                        (r"placebo", r"salt water, \ told nothing", GREY_B)):
            conds.add(VGroup(word_chip(t, color=c, font_size=20, width=2.4), wrapped_label(d, 4.0, 19, WHITE)).arrange(
                RIGHT, buff=0.25))
        conds.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-3.2, -0.2, 0])
        rows = rows_of([
            (r"Stanley Schachter and Jerome Singer: \ 185 men told they were testing a vitamin's effect on vision; "
             r"\ most were injected with adrenaline", WHITE),
            (r"then they waited with a stooge who acted euphoric \ (paper planes, \ a hula hoop) \ or angry \ (at an "
             r"insulting questionnaire)", COG),
            (r"prediction: \ people with arousal and no explanation for it would take on the stooge's mood", BODY),
            (r"the result was weak and mixed: \ some differences in the predicted direction, \ much smaller than "
             r"the textbook story", UNPL),
        ], 5.6, 21, 0.3).move_to([3.4, -0.1, 0])
        tag = historical_tag(r"Schachter \& Singer (1962)")
        with self.voiceover(
            "In 1962 Stanley Schachter and Jerome Singer proposed a compromise between James and Cannon. Emotion has "
            "two factors: bodily arousal, which says how strongly you feel, and a cognitive label, which says what "
            "you feel. <bookmark mark='a'/> They told 185 men they were testing a vitamin compound called Suproxin "
            "on vision, and injected most of them with adrenaline. Some were told its real side effects: a racing "
            "heart, flushing, tremor. Some were told nothing. Some were told of side effects it doesn't have. A "
            "placebo group got salt water. <bookmark mark='b'/> Then each man waited with a stooge who acted "
            "euphoric, throwing paper planes and twirling a hula hoop, or angry, at an insulting questionnaire. "
            "<bookmark mark='c'/> The prediction: men with arousal and no explanation for it would take on the "
            "stooge's mood. <bookmark mark='d'/> The results were weak and mixed: some differences in the predicted "
            "direction, much smaller than the version told in textbooks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(c) for c in conds], lag_ratio=0.3))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def inference(self):
        d = load("attribution")
        head = heading(r"Derivation: \ two factors as inference")
        eqs = VGroup(
            MathTex(r"a \sim \mathcal N(s + c,\ \sigma^2)", font_size=36),
            MathTex(r"p(s \mid a) \propto e^{-s/\lambda}\, e^{-(a - s - c)^2 / 2\sigma^2}", font_size=32),
            MathTex(r"\text{felt emotion} \propto \mathbb{E}[s \mid a]", font_size=32),
        ).arrange(DOWN, buff=0.3)
        A = axes([0, 1.5], [0, 0.7], x_length=5.6, y_length=3.4, xticks=[0, 0.5, 1.0, 1.5], yticks=[0, 0.3, 0.6],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"arousal already explained, \ $c$",
                 ylabel=r"arousal put down to the situation", center=[-3.3, -0.4, 0], font_size=16)
        cv = curve(A.ax, d["explanation"], d["curve"], COG, 4)
        pi = Dot(A.ax.c2p(1.0, d["c_informed"]), color=PLEAS, radius=0.08)
        pg = Dot(A.ax.c2p(0.0, d["c_ignorant"]), color=FACE, radius=0.08)
        li = label(r"informed", font_size=16, color=PLEAS).next_to(pi, UP, buff=0.1)
        lg = label(r"ignorant, \ misinformed", font_size=16, color=FACE).next_to(pg, RIGHT, buff=0.15)
        rows = rows_of([
            (r"Psyche: \ arousal $a$ is felt; \ its causes are the situation $s$ and a known cause $c$, \ the "
             r"injection one was told about", MODEL),
            (rf"no explanation: \ {d['c_ignorant']:.2f} of the arousal is put down to the situation", FACE),
            (rf"the side effects explained: \ {d['c_informed']:.2f}, \ explained away", PLEAS),
            (r"misattribution is the same inference with the wrong cause: \ the arousal belongs to the drug, "
             r"\ the bridge, \ the coffee, \ and is credited to the person in front of you", BODY),
        ], 5.6, 21, 0.3)
        right = VGroup(eqs, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{emotion.attribution}: \ $a = 1.2$, \ $\sigma = 0.5$, \ $\lambda = 0.3$")
        with self.voiceover(
            "The two-factor idea can be written as inference, which makes clear what it predicts. "
            "<bookmark mark='a'/> Arousal, a, is felt. It has two possible causes: the situation, s, and a cause the "
            "person already knows about, c, such as an injection they were told would race their heart. Psyche "
            "infers how much of the arousal belongs to the situation, and that share is what gets felt as emotion. "
            f"<bookmark mark='b'/> With no explanation, {d['c_ignorant']:.2f} of the arousal is put down to the "
            "situation. <bookmark mark='c'/> With the side effects explained, it falls to "
            f"{d['c_informed']:.2f}: the arousal has been explained away. That is the informed condition's "
            "prediction. <bookmark mark='d'/> And misattribution is the same inference with the wrong cause. The "
            "arousal really belongs to the drug, the bridge, or the coffee, and is credited to the situation, or to "
            "the person in front of you."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Write(eqs))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(cv), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(pg), FadeIn(lg))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(pi), FadeIn(li))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def record(self):
        head = heading(r"The record")
        rows = rows_of([
            (r"1979: \ Gary Marshall and Philip Zimbardo repeated the euphoria conditions; \ adrenaline did not make "
             r"people more euphoric", UNPL),
            (r"1979: \ Christina Maslach produced arousal by hypnotic suggestion; \ unexplained arousal felt "
             r"negative, \ whatever the stooge did", UNPL),
            (r"Reisenzein's 1983 review: \ little evidence that arousal is necessary for emotion; \ but arousal "
             r"from one source can intensify a feeling about another", COG),
            (r"the strong claim failed; \ the weaker one, \ that arousal can be misattributed, \ survived in many "
             r"forms", WHITE),
        ], 12.2, 26, 0.42).move_to([0, -0.2, 0])
        tag = published_tag(r"Marshall \& Zimbardo (1979); \ Maslach (1979); \ Reisenzein (1983)")
        with self.voiceover(
            "The strong version did not fare well. <bookmark mark='a'/> In 1979 Gary Marshall and Philip Zimbardo "
            "repeated the euphoria conditions, and adrenaline did not make people more euphoric. "
            "<bookmark mark='b'/> In the same year Christina Maslach produced arousal by hypnotic suggestion; "
            "unexplained arousal felt negative, whatever the stooge did. <bookmark mark='c'/> Rainer Reisenzein's "
            "1983 review found little evidence that arousal is necessary for emotion, but good evidence that arousal "
            "from one source can intensify a feeling about another. <bookmark mark='d'/> So the strong claim "
            "failed, and the weaker one, that arousal can be misattributed, survived in many forms."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def bridge(self):
        head = heading(r"The Capilano bridge, \ 1974")
        # a sagging bridge over a gorge, and a low solid one
        gorge = VGroup(Line([-6.3, 1.4, 0], [-4.9, -1.6, 0], color=GREY_C, stroke_width=3),
                       Line([-1.0, 1.4, 0], [-2.4, -1.6, 0], color=GREY_C, stroke_width=3))
        span = ArcBetweenPoints([-6.3, 1.4, 0], [-1.0, 1.4, 0], angle=0.35, color=FEAR, stroke_width=5)
        low = Line([-6.0, -2.4, 0], [-1.3, -2.4, 0], color=PLEAS, stroke_width=6)
        lh = label(r"swaying, \ 70 m above rocks", font_size=17, color=FEAR).next_to(span, UP, buff=0.1)
        ll = label(r"low, \ solid, \ over a stream", font_size=17, color=PLEAS).next_to(low, DOWN, buff=0.1)
        rows = rows_of([
            (r"Donald Dutton and Arthur Aron: \ a woman stops men on one of two bridges for a short questionnaire, "
             r"\ and gives them her number in case they want to know more", WHITE),
            (r"from the swaying bridge, \ 9 of the 18 men who took the number phoned her; \ from the solid one, "
             r"\ 2 of 16", FEAR),
            (r"read as fear misattributed to attraction; \ the men on the two bridges may also have differed "
             r"\ (who crosses a swaying bridge?)", COG),
            (r"never directly replicated at scale; \ laboratory studies of arousal and attraction find an effect, "
             r"\ by more than one route", UNPL),
        ], 5.8, 21, 0.3).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Dutton \& Aron (1974); \ Foster et al.\ (1998)")
        with self.voiceover(
            "The most famous misattribution study was done on a bridge. <bookmark mark='a'/> In 1974 Donald Dutton "
            "and Arthur Aron had a woman stop men on one of two bridges in North Vancouver: the Capilano suspension "
            "bridge, narrow and swaying, about seventy metres above rocks, or a low, solid bridge over a stream. She "
            "asked them to fill in a short questionnaire, and gave them her phone number in case they wanted to know "
            "more. <bookmark mark='b'/> From the swaying bridge, nine of the eighteen men who took the number phoned "
            "her; from the solid one, two of sixteen. <bookmark mark='c'/> The reading: fear was misattributed to "
            "attraction. But the men who choose to cross a swaying bridge may differ from those who don't. "
            "<bookmark mark='d'/> The bridge study has never been directly replicated at scale. Laboratory studies "
            "of arousal and attraction, pooled by Craig Foster and colleagues in 1998, find an effect, by more than "
            "one route."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Create(gorge), Create(span), FadeIn(lh), Create(low), FadeIn(ll))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
