from __future__ import annotations

from videos.economics.econ56.common import *  # noqa: F403

COLUMNS = [
    ("micro", r"Micro", [
        r"1. \ kinks: \ bunching as evidence on elasticities \ (Saez 2010; \ Kleven 2016)",
        r"2. \ externalities: \ valuing the harm, \ as with the social cost of carbon \ (Part 48)",
        r"3. \ reserves: \ tested in online ad auctions by field experiment \ (Ostrovsky and Schwarz)",
        r"4. \ screening in many dimensions: \ no simple solution \ (Rochet and Chon\'e 1998)",
    ]),
    ("macro", r"Macro", [
        r"5. \ taxing capital: \ the zero long-run tax revisited \ (Straub and Werning 2020)",
        r"6. \ benefits: \ the best path over a spell \ (Kolsrud, \ Landais, \ Nilsson and Spinnewijn 2018)",
        r"7. \ discretion: \ credibility, \ forward guidance and the zero bound \ (Parts 30, \ 31)",
        r"8. \ precaution: \ HANK and monetary transmission \ (Kaplan, \ Moll and Violante 2018)",
    ]),
    ("metrics", r"Econometrics", [
        r"9. \ instruments: \ weak-instrument-robust inference \ (Andrews, \ Stock and Sun 2019)",
        r"10. \ Euler equations: \ still rejected on real returns \ (Part 23)",
        r"11. \ timing: \ heterogeneous effects and parallel trends \ (Roth et al.\ 2023)",
        r"12. \ the long run: \ do hours fall after a technology shock? \ (Gal\'i 1999; \ Christiano, \ "
        r"Eichenbaum and Vigfusson 2004)",
    ]),
]


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 14, r"Frontier: \ where each problem is still open", r"Which of tonight's answers are still "
             r"being argued about?", "Chapter fourteen. Frontier: where each problem is still open.",
             lit={2018: r"Kaplan, \ Moll and Violante", 2020: r"Straub and Werning", 2023: r"Roth et al."},
             scale=("person", "nation"), horizon=("a decade",))
        self.open_()

    def open_(self):
        cols = VGroup()
        for field, name, items in COLUMNS:
            head = label(name, font_size=26, color=FIELD[field])
            rows = VGroup(*[wrapped_label(t, 3.9, 17, WHITE) for t in items]).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.32)
            cols.add(VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35))
        cols.arrange(RIGHT, buff=0.45, aligned_edge=UP).move_to(DOWN * 0.25)
        head = label(r"settled in the exam, \ open in the journals", font_size=30, color=E.ACCENT).to_edge(
            UP, buff=0.45)
        tag = published_tag(r"Saez, \ AEJ: Policy (2010); \ Rochet and Chon\'e, \ Econometrica (1998); \ Straub "
                            r"and Werning, \ AER (2020); \ Kolsrud et al., \ AER (2018); \ Kaplan, \ Moll and "
                            r"Violante, \ AER (2018); \ Roth et al., \ J. Econometrics (2023)", corner=DR,
                            font_size=11)
        with self.voiceover(
            "Every question tonight had a clean answer. Every one of them also opens onto a live research "
            "question. <bookmark mark='a'/> In micro: kinks became a way to measure behaviour, by counting who "
            "bunches at them, the method of Emmanuel Saez and Henrik Kleven. Valuing an externality is the hard "
            "part in practice, as with the social cost of carbon. Reserve prices have been tested by field "
            "experiment in online advertising auctions. And screening when buyers differ in more than one way has "
            "no simple solution: Jean-Charles Rochet and Philippe Choné showed why. <bookmark mark='b'/> In macro: "
            "Ludwig Straub and Iván Werning showed that the famous result that capital should go untaxed in the "
            "long run fails in some of the very models that produced it. Camille Landais and coauthors estimated "
            "how benefits should change over a spell, using Swedish data. Commitment is the whole subject of "
            "forward guidance. And the Aiyagari household is now the core of heterogeneous-agent New Keynesian "
            "models, after Greg Kaplan, Benjamin Moll and Giovanni Violante. <bookmark mark='c'/> In "
            "econometrics: inference with weak instruments; Euler equations that real returns still reject; a "
            "whole literature on staggered timing, surveyed by Jonathan Roth and coauthors; and the old argument "
            "over whether hours fall after a technology shock, which turned on exactly the long-run restriction "
            "of question twelve."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abc", cols):
                vo.wait_until(mk)
                self.play(FadeIn(c[0]), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in c[1]], lag_ratio=0.5),
                          run_time=3.0)
        self.clear_scene()
