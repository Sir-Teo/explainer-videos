from __future__ import annotations

from videos.philosophy.philosophy26.common import *  # noqa: F403


class Experiments(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"The experiments", r"What did nature say?", lit=(1982, 2015), part=PART)
        with self.voiceover("Chapter six. The experiments."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.history()
        self.loopholes()
        self.meaning()

    def history(self):
        head = label(r"Fifty years of Bell tests", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        tl = NumberLine(x_range=[1970, 2025, 5], length=11.5, color=GREY_B, include_numbers=True,
                        font_size=18, decimal_number_config={"num_decimal_places": 0, "group_with_commas": False}
                        ).move_to([0, 0.6, 0])
        evs = [(1972, r"Freedman and Clauser: \ the first test", CLASS, 1),
               (1982, r"Aspect: \ settings switched in flight", WAVE, -1),
               (1998, r"Weihs et al.: \ random settings, \ 400 m apart", ALICE, 1),
               (2015, r"Delft, \ Vienna, \ NIST: \ loophole-free", OK, -1),
               (2022, r"Nobel prize: \ Aspect, \ Clauser, \ Zeilinger", PART_C, 1)]
        marks = VGroup()
        for y, t, c, side in evs:
            p = tl.n2p(y)
            dot = Dot(p, radius=0.09, color=c)
            lab = wrapped_label(t, 2.6, 17, c)
            lab.next_to(p, UP if side > 0 else DOWN, buff=(0.35 + (0.5 if y == 1998 else 0)) if side > 0 else 0.7)
            marks.add(VGroup(dot, Line(p, lab.get_bottom() if side > 0 else lab.get_top(), color=c,
                                       stroke_width=1.5), lab))
        foot = label(r"every test: \ $|S| > 2$, \ by many standard deviations, \ near quantum mechanics' $2\sqrt2$",
                     font_size=21, color=GOAL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Bell's inequality is a prediction that experiments can test, and they have, for fifty years. "
            "<bookmark mark='a'/>In 1972 Stuart Freedman and John Clauser ran the first test, with photons from "
            "calcium atoms. <bookmark mark='b'/>In 1982 Alain Aspect's group switched the analyzer settings while the "
            "photons were in flight, so no slower-than-light signal could carry Alice's setting to Bob. "
            "<bookmark mark='c'/>In 1998 Gregor Weihs and colleagues, in Anton Zeilinger's group, used random number "
            "generators to choose settings, four hundred metres apart. <bookmark mark='d'/>In 2015 three groups, in "
            "Delft, Vienna and Boulder, closed the main loopholes at once. <bookmark mark='e'/>And in 2022 Aspect, "
            "Clauser and Zeilinger shared the Nobel prize in physics. <bookmark mark='f'/>Every test has found S "
            "above two by many standard deviations, close to the quantum value."
        ) as vo:
            self.play(FadeIn(head), Create(tl))
            for mk, m in zip("abcde", marks):
                vo.wait_until(mk)
                self.play(FadeIn(m))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def loopholes(self):
        head = label(r"The loopholes, \ closed", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"locality", r"a signal could carry Alice's setting to Bob: \ close it by choosing settings after the "
                          r"particles leave, \ too far apart for light to connect", CLASS),
            (r"detection", r"if most particles go undetected, \ the detected ones may be a biased sample: \ close it "
                           r"with efficient detectors", WAVE),
            (r"freedom of choice", r"the settings might be correlated with the hidden variables: \ use random "
                                   r"generators, \ humans \ (the Big Bell Test, \ 2018), \ or light from distant "
                                   r"quasars", ALICE),
            (r"2015", r"Hensen et al. \ (Delft): \ electron spins 1.3 km apart; \ Giustina et al. \ (Vienna) \ and "
                      r"Shalm et al. \ (NIST): \ photons", OK),
        ]
        g = rows_table(rows, top=1.7, gap=0.5, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "What were the loopholes? <bookmark mark='a'/>Locality: if Alice's setting could reach Bob's apparatus "
            "by some signal in time, a local model could fake the correlations. It is closed by choosing settings "
            "after the particles have left the source, at stations too far apart for light to connect the choices. "
            "<bookmark mark='b'/>Detection: if most particles go undetected, the detected ones might be a biased "
            "sample. It is closed with efficient detectors. <bookmark mark='c'/>Freedom of choice: perhaps the "
            "settings are themselves correlated with the hidden variables. Experiments have chosen settings by "
            "random generators, by a hundred thousand human volunteers in the Big Bell Test, and by the colour of "
            "light from distant quasars. <bookmark mark='d'/>In 2015 Ronald Hanson's group in Delft used electron "
            "spins one point three kilometres apart, and groups in Vienna and at NIST used photons, closing the "
            "locality and detection loopholes together."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def meaning(self):
        head = label(r"What Bell's theorem forces", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the assumptions", r"locality; \ settings independent of the hidden variables; \ outcomes are single "
                                 r"and definite", ABS),
            (r"Bohm", r"keep hidden values, \ give up locality: \ instantaneous influence, \ but no usable signal",
             CLASS),
            (r"Everett", r"give up single outcomes: \ each run has every result, \ on different branches", WAVE),
            (r"superdeterminism", r"give up independence: \ the settings and particles were correlated all along",
             BAD),
            (r"no signalling", r"whatever the explanation, \ the correlations cannot send a message: \ relativity's "
                               r"letter survives; \ its spirit is in question", GOAL),
        ]
        g = rows_table(rows, top=1.7, gap=0.45, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "So what does the theorem force? <bookmark mark='a'/>Its assumptions are locality, settings that are "
            "independent of the hidden variables, and single, definite outcomes. One must go. "
            "<bookmark mark='b'/>Bohm keeps hidden values and gives up locality: what Alice does instantly affects "
            "Bob's particle, though not in any way she could use to send him a message. <bookmark mark='c'/>Everett "
            "gives up single outcomes: every run has every result, on different branches, and the correlations hold "
            "within branches. <bookmark mark='d'/>Superdeterminism gives up independence: the settings and the "
            "particles were correlated from the start, a view few accept because it threatens all of experimental "
            "science. <bookmark mark='e'/>Whatever the explanation, the correlations cannot be used to signal. "
            "Relativity's letter survives; whether its spirit does is the question Tim Maudlin's book on non-locality "
            "and relativity asks."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
