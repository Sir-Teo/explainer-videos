from __future__ import annotations

import numpy as np

from videos.psychology.psych9.common import *  # noqa: F403


class OnYou(VoiceoverScene):
    def construct(self):
        self.card()
        self.guess()
        self.answer()

    def card(self):
        card = chapter_card(5, r"On you: \ guess the heritability", r"Which traits run in the genes, and how strongly?",
                            lit=(), part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover(
            "Chapter five. On you: guess the heritability."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _rows(self, d, center, reveal: bool, gap: float = 0.82):
        """Six traits, each with a track from 0 to 1; with ``reveal`` a bar and a number for the published value."""
        c = np.asarray(center, float)
        g = VGroup()
        x0, x1 = c[0] + 0.3, c[0] + 4.9
        for i, (name, h) in enumerate(zip(d["names"], d["h2"])):
            y = c[1] + 2.1 - gap * i
            lab = label(name, font_size=31, color=WHITE)
            lab.move_to([0, y, 0]).align_to(np.array([c[0] - 5.9, 0, 0]), LEFT)
            track = Line([x0, y, 0], [x1, y, 0], color=GREY_D, stroke_width=10)
            row = VGroup(lab, track)
            if reveal:
                w = max((x1 - x0) * float(h), 0.02)
                bar = Line([x0, y, 0], [x0 + w, y, 0], color=GENE, stroke_width=10)
                num = label(rf"${h:.2f}$", font_size=31, color=GENE).next_to([x1, y, 0], RIGHT, buff=0.2)
                row.add(bar, num)
            g.add(row)
        ends = VGroup(label(r"0", font_size=26, color=GREY_A).move_to([x0, c[1] + 2.6, 0]),
                      label(r"1", font_size=26, color=GREY_A).move_to([x1, c[1] + 2.6, 0]),
                      label(r"the share that goes with genes", font_size=27,
                            color=GREY_A).move_to([(x0 + x1) / 2, c[1] + 2.6, 0]))
        return g, ends

    def guess(self):
        d = load("guess")
        stage = demo_stage(13.4, 6.6, r"On you: \ six traits", center=[0, -0.25, 0])
        rows, ends = self._rows(d, stage.box.get_center() + np.array([0.4, -0.3, 0]), False)
        ask = label(r"For each: \ nearer 0, \ nearer a half, \ or nearer 1?", font_size=32, color=P.ACCENT)
        ask.move_to(stage.box.get_center() + np.array([0, -2.85, 0]))
        ring = countdown_ring(0.4).move_to(stage.box.get_corner(UR) + np.array([-0.65, -0.65, 0]))
        with self.voiceover(
            "Your turn. Here are six ways in which people differ. <bookmark mark='a'/> Which language you "
            "speak. How many years of schooling you had. Personality traits, such as how outgoing you are. "
            "Scores on tests of reasoning, at seventeen. A diagnosis of attention deficit hyperactivity "
            "disorder. And a diagnosis of schizophrenia. <bookmark mark='b'/> For each one, guess the "
            "heritability that twin studies report: the share of the differences between people that "
            "goes with their genes. Is it nearer zero, nearer a half, or nearer one? Decide on all six "
            "before the answers come up."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(ends))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.75), run_time=13.0)
            vo.wait_until("b")
            self.play(FadeIn(ask))
        self.add(ring)
        self.play(ring.t.animate.set_value(0.0), run_time=7.0, rate_func=linear)
        self.clear_scene()

    def answer(self):
        d = load("guess")
        t = archive.HERITABILITY_TABLE.data
        head = heading(r"What twin studies report")
        rows, ends = self._rows(d, [-0.4, 0.2, 0], True, gap=0.66)
        notes = rows_of([
            (r"language: \ everything from the family, \ nothing from the genes", HOME),
            (r"schooling: \ the one trait here where the shared home matters about as much as genes", HOME),
            (rf"across 17{{,}}804 traits the average is {pct(d['all_traits'])}", DATA),
        ], 12.4, 28, 0.12).to_edge(DOWN, buff=0.62)
        src = published_tag(archive.HERITABILITY_TABLE.cite)
        with self.voiceover(
            "Here's what twin studies report. <bookmark mark='a'/> The language you speak: zero. Nobody "
            "inherits a language. It comes entirely from the family and the place, and it's a useful "
            "reminder that running in families and being genetic aren't the same thing. "
            f"<bookmark mark='b'/> Years of schooling: about {d['h2'][1]:.2f}, and it's the unusual one, "
            "because here the shared home matters about as much as the genes do. <bookmark mark='c'/> "
            f"Personality: {d['h2'][2]:.2f} in twin studies, and about half that in studies of other "
            f"relatives, which is the disagreement chapter four warned about. <bookmark mark='d'/> "
            f"Reasoning at seventeen: {d['h2'][3]:.2f}. A diagnosis of ADHD: {d['h2'][4]:.2f}. "
            f"Schizophrenia: {d['h2'][5]:.2f}. <bookmark mark='e'/> If you guessed low for the last "
            "three, you're in good company. Most people do. And a team that pooled fifty years of twin "
            f"studies, nearly eighteen thousand traits, found an average of "
            f"{100 * d['all_traits']:.0f} percent. Almost nothing came out at zero. These numbers are "
            "large, they've been found again and again, and they're easy to misread. The next chapter "
            "is about the misreadings."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(ends), *[FadeIn(VGroup(r[0], r[1])) for r in rows])
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*rows[0][2:])), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(rows[1][2]), FadeIn(rows[1][3]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Create(rows[2][2]), FadeIn(rows[2][3]))
            vo.wait_until("d")
            self.play(LaggedStart(*[AnimationGroup(Create(rows[k][2]), FadeIn(rows[k][3])) for k in (3, 4, 5)], lag_ratio=0.9),
                      run_time=7.0)
            vo.wait_until("e")
            self.play(FadeIn(notes[2], shift=UP * 0.1))
        self.clear_scene()
