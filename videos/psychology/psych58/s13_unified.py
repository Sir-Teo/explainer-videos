from __future__ import annotations

from videos.psychology.psych58.common import *  # noqa: F403

PRINCIPLES = [
    (r"efficient coding", r"after-effects, \ repulsive biases, \ Laughlin's curve", r"risked, \ held", GOOD),
    (r"normalization", r"gain changes, \ suppression, \ attention effects", r"risked, \ held", GOOD),
    (r"predictive coding", r"separate error neurons, \ suppression of the expected", r"risked, \ mixed", PERSON),
    (r"Bayesian brain", r"cue weights from measured noise", r"risked where priors are measured", PERSON),
    (r"free-energy principle", r"nothing on its own; \ its models predict", r"not risked", AUTH),
]


class Unified(VoiceoverScene):
    def construct(self):
        card_section(self, 12, r"Unified theories", r"What would a theory of everything a mind does have to risk?",
                     scale=("person", "brain"))
        self.newell()
        self.scorecard()

    def newell(self):
        rows_section(self, r"You can't play twenty questions with nature", [
            (r"Newell, \ 1973: \ psychology studies effect after effect, \ each with its own little model, \ and will "
             r"never add up", WHITE),
            (r"his answer: \ unified theories of cognition, \ one architecture that does every task", MODEL),
            (r"ACT-R (Anderson) and Soar (Laird, \ Newell and Rosenbloom): \ decades of models of memory, \ skill and "
             r"problem solving in one system", PERSON),
            (r"the common model of cognition, \ 2017: \ what those architectures agree on", GOOD),
            (r"today's rivals: \ large brain simulations, \ and models trained on many experiments at once (Part 60)",
             YOU),
        ], "What would a theory of everything a mind does have to risk? <bookmark mark='a'/> In 1973 Allen Newell "
           "complained that psychology studies effect after effect, each with its own little model, and will never "
           "add up. You can't play twenty questions with nature and win. <bookmark mark='b'/> His answer was unified "
           "theories of cognition: one architecture that does every task. <bookmark mark='c'/> John Anderson's "
           "ACT-R, and Soar, built by John Laird, Newell and Paul Rosenbloom, have decades of models of memory, skill "
           "and problem solving in one system. <bookmark mark='d'/> In 2017 the common model of cognition set out "
           "what those architectures agree on. <bookmark mark='e'/> Today's rivals are large brain simulations, and "
           "models trained on many experiments at once, which Part 60 takes up.",
           tag=historical_tag(r"Newell (1973)"))

    def scorecard(self):
        head = heading(r"Each principle, \ and what it risked")
        hdr = VGroup(label(r"principle", font_size=17, color=GREY_A), label(r"a prediction that could fail",
                                                                             font_size=17, color=GREY_A),
                     label(r"so far", font_size=17, color=GREY_A))
        xs = [-4.6, -0.3, 4.4]
        for h, x in zip(hdr, xs):
            h.move_to([x, 2.2, 0])
        rows = []
        for i, (p, pred, res, col) in enumerate(PRINCIPLES):
            y = 1.3 - 0.85 * i
            rows.append(VGroup(wrapped_label(p, 3.4, 19, WHITE).move_to([xs[0], y, 0]),
                               wrapped_label(pred, 4.6, 18, GREY_A).move_to([xs[1], y, 0]),
                               wrapped_label(res, 3.4, 18, col).move_to([xs[2], y, 0])))
        foot = wrapped_label(r"the more a principle explains without measurement, \ the less it has risked", 12.0, 21,
                             YOU).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here's each principle in this part, and what it risked. <bookmark mark='a'/> Efficient coding predicted "
            "after-effects, repulsive biases and Laughlin's curve before they were measured, and held. "
            "<bookmark mark='b'/> Normalization predicted gain changes, suppression, and attention effects, and held. "
            "<bookmark mark='c'/> Predictive coding predicted separate error neurons and suppression of the expected, "
            "with mixed results. <bookmark mark='d'/> The Bayesian brain risked cue weights from measured noise, and "
            "does well where priors are measured. <bookmark mark='e'/> The free-energy principle risks nothing on its "
            "own. Its models predict. <bookmark mark='f'/> The more a principle explains without measurement, the "
            "less it has risked."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()
