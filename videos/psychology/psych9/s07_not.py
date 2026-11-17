from __future__ import annotations

import numpy as np

from videos.psychology.psych9.common import *  # noqa: F403


class IsNot(VoiceoverScene):
    def construct(self):
        self.card()
        self.not_fixed()
        self.two_fields()
        self.not_you()
        self.not_constant()

    def card(self):
        card = chapter_card(6, r"What heritability is not", r"What can the number not tell you?", lit=(), part=PART,
                            scale=("person", "group", "culture"), marr=("what",))
        with self.voiceover(
            "Chapter six. What heritability is not."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def not_fixed(self):
        h = archive.NCD_RISC_2016.data
        y = archive.YENGO_2022.data
        head = heading(r"1. \ Not fixed")
        badge = big_number(rf"{y['twin_h2']:.1f}", r"heritability of height in twin studies, in well-fed countries", GENE,
                           font_size=84, width=4.0).move_to([-4.8, 0.6, 0])
        gains = VGroup()
        for i, (name, cm, col) in enumerate(((r"South Korean women", h["korean_women_cm"], DATA),
                                             (r"Iranian men", h["iranian_men_cm"], DATA))):
            x = -0.9 + 2.6 * i
            base = Rectangle(width=1.0, height=1.6, stroke_width=0, fill_color=OWN, fill_opacity=0.5).move_to([x, -1.3, 0])
            top = Rectangle(width=1.0, height=cm * 0.085, stroke_width=0, fill_color=col, fill_opacity=0.9)
            top.next_to(base, UP, buff=0)
            lab = label(rf"$+{cm:.1f}$ cm", font_size=32, color=col).next_to(top, UP, buff=0.12)
            nm = wrapped_label(name, 2.3, 27, WHITE).next_to(base, DOWN, buff=0.12)
            gains.add(VGroup(base, top, lab, nm))
        gl = wrapped_label(rf"born {h['born'][1]} against born {h['born'][0]}", 4.4, 28, GREY_A).move_to([0.4, 2.2, 0])
        rows = rows_of([
            (r"a nation's genes do not change in a century; \ its food did", WHITE),
            (r"heritability describes differences in the environments people actually had", P.ACCENT),
            (r"a condition caused by one gene, phenylketonuria, \ is prevented by a diet", GREY_A),
        ], 4.1, 29, 0.3).move_to([4.95, 0.0, 0])
        keep_in_frame(rows)
        src = published_tag(archive.NCD_RISC_2016.cite)
        tag = note(r"bars: not to scale below the gain").to_corner(DR, buff=0.2)
        with self.voiceover(
            "One. It isn't fixedness. Take height. In well-fed countries, twin studies put its "
            f"heritability at about {y['twin_h2']:.1f}, as high as anything we measure. "
            f"<bookmark mark='a'/> Now look across a century. South Korean women born in {h['born'][1]} "
            f"are, on average, {h['korean_women_cm']:.1f} centimetres taller than those born in "
            f"{h['born'][0]}. Iranian men: {h['iranian_men_cm']:.1f}. <bookmark mark='b'/> A nation's "
            "genes don't change in a hundred years. Its food did. <bookmark mark='c'/> So a trait can be "
            "highly heritable and still move a long way when the environment moves. Heritability says "
            "which differences go with genes in the environments people actually had. It says nothing "
            "about what a new environment would do. <bookmark mark='d'/> Medicine's standard example is "
            "phenylketonuria: a condition caused by a single gene, which damages the developing brain, "
            "and which is prevented by a diet. Entirely genetic, and entirely treatable."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(badge))
            vo.wait_until("a")
            self.play(FadeIn(gl), LaggedStart(*[FadeIn(g, shift=UP * 0.2) for g in gains], lag_ratio=0.6), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def two_fields(self):
        d = load("fields")
        head = heading(r"2. \ Not about groups: \ seed from one sack, in two fields")
        g = np.random.default_rng(5)

        def field(x0, heights, col, name, soil):
            base_y = -1.15
            ground = Rectangle(width=5.2, height=0.3, stroke_width=0, fill_color=soil, fill_opacity=0.9).move_to(
                [x0, base_y - 0.15, 0])
            xs = np.linspace(x0 - 2.4, x0 + 2.4, len(heights))
            stems = VGroup(*[Line([x, base_y, 0], [x, base_y + 0.5 * max(float(v), 0.2), 0], color=col, stroke_width=4)
                             for x, v in zip(xs, heights)])
            mean = DashedLine([x0 - 2.6, base_y + 0.5 * float(np.mean(heights)), 0],
                              [x0 + 2.6, base_y + 0.5 * float(np.mean(heights)), 0], color=WHITE, stroke_width=2)
            title = label(name, font_size=31, color=col).move_to([x0, base_y - 0.6, 0])
            return VGroup(ground, stems, mean, title)

        rich = field(-3.5, d["rich"][:34] + 1.5, GENE, r"rich soil", "#5B4636")
        poor = field(3.5, d["poor"][:34] + 1.5, GENE, r"poor soil", "#3A3F4A")
        hr = label(rf"within this field: \ heritability ${d['h2_rich']:.1f}$", font_size=29, color=GENE).move_to([-3.5, 2.55, 0])
        hp = label(rf"within this field: \ heritability ${d['h2_poor']:.1f}$", font_size=29, color=GENE).move_to([3.5, 2.55, 0])
        gap = wrapped_label(rf"between the fields: \ a gap of ${d['gap']:.1f}$ units, \ of which genes explain "
                            rf"${abs(d['genetic_gap']):.1f}$", 12.4, 31, BAD).move_to([0, -2.45, 0])
        end = wrapped_label(r"A high heritability inside each group says nothing about why the groups differ.", 12.4, 31,
                            P.ACCENT).next_to(gap, DOWN, buff=0.15)
        tag = psyche_tag(r"simulated: 34 plants shown from each field")
        with self.voiceover(
            "Two. It isn't about groups. Here's a picture due to the geneticist Richard Lewontin. Take a "
            "sack of seed, with all the usual genetic variety. Sow a handful in a field with rich soil, "
            "and a handful in a field with poor soil. <bookmark mark='a'/> Within the rich field every "
            "plant has the same soil. So the differences in height between one plant and the next are "
            f"almost all genetic. Heritability: {d['h2_rich']:.1f}. <bookmark mark='b'/> Within the poor "
            f"field, the same: {d['h2_poor']:.1f}. <bookmark mark='c'/> And the difference between the "
            f"fields? The plants in the rich soil are taller by {d['gap']:.1f} units, and the genetic "
            "difference between the fields is zero. The seed came from one sack. <bookmark mark='d'/> So "
            "a high heritability inside each of two groups tells you nothing about why the groups "
            "differ. This is the mistake at the centre of a century of claims about classes, nations and "
            "races, and it's a mistake of logic before it's anything else."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rich[0]), FadeIn(poor[0]), FadeIn(rich[3]), FadeIn(poor[3]))
            self.play(LaggedStart(*[GrowFromEdge(s, DOWN) for s in rich[1]], lag_ratio=0.03),
                      LaggedStart(*[GrowFromEdge(s, DOWN) for s in poor[1]], lag_ratio=0.03), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(hr))
            vo.wait_until("b")
            self.play(FadeIn(hp))
            vo.wait_until("c")
            self.play(Create(rich[2]), Create(poor[2]), FadeIn(gap))
            vo.wait_until("d")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def not_you(self):
        head = heading(r"3. \ Not about you")
        wrong = wrapped_label(r"``Intelligence is 60\% genetic, \ so 60\% of my intelligence comes from my genes.''", 12.4, 32,
                              BAD).move_to([0, 2.3, 0])
        one = Rectangle(width=2.6, height=1.6, color=VOLT, stroke_width=3, fill_color=PANEL_FILL, fill_opacity=1).move_to(
            [-4.6, 0.1, 0])
        ol = VGroup(label(r"width", font_size=28, color=HOME).next_to(one, DOWN, buff=0.1),
                    label(r"height", font_size=28, color=GENE).next_to(one, LEFT, buff=0.1),
                    label(r"area", font_size=30, color=VOLT).move_to(one))
        q = wrapped_label(r"How much of this area is due to the width? \ No answer.", 3.6, 29, WHITE).next_to(one, DOWN, buff=0.6)
        ws = [1.0, 1.7, 0.7, 2.3, 1.3]
        many = VGroup(*[Rectangle(width=w, height=1.5 + 0.06 * (i % 2), color=VOLT, stroke_width=3, fill_color=PANEL_FILL,
                                  fill_opacity=1) for i, w in enumerate(ws)]).arrange(RIGHT, buff=0.25, aligned_edge=DOWN)
        many.move_to([2.6, 0.2, 0])
        ml = wrapped_label(r"Why do these differ in area? \ Mostly because their widths differ. \ That question has an "
                           r"answer.", 6.6, 29, WHITE).next_to(many, DOWN, buff=0.45)
        end = wrapped_label(r"Heritability shares out the differences among people. \ A person is not two piles that add "
                            r"up.", 12.4, 31, P.ACCENT).to_edge(DOWN, buff=0.45)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Three. It isn't about you. People say: intelligence is sixty percent genetic, so sixty percent "
            "of my intelligence comes from my genes. That sentence has no meaning. <bookmark mark='a'/> "
            "Think of a rectangle. Its area is its width times its height. How much of the area is due to "
            "the width? For one rectangle, the question has no answer. <bookmark mark='b'/> But for a "
            "collection of rectangles you can ask something sensible. Do they differ in area mostly "
            "because their widths differ, or their heights? If they're all about the same height, the "
            "differences in area go with the widths. <bookmark mark='c'/> That's the kind of statement "
            "heritability is. It shares out differences among people. A person's genes and surroundings "
            "aren't two piles that add up to them. They multiply, like width and height."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(wrong))
            vo.wait_until("a")
            self.play(FadeIn(one), FadeIn(ol), FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(many, lag_ratio=0.15), FadeIn(ml), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def not_constant(self):
        d = load("fields")
        t = archive.TURKHEIMER_2003.data
        head = heading(r"4. \ Not a constant")
        A = axes([0, 4], [0, 1.05], x_length=4.6, y_length=3.3, xticks=[0, 1, 2, 3, 4], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}",
                 xlabel=r"spread of environments (genetic spread $= 1$)", ylabel=r"heritability", center=[-4.1, 0.25, 0])
        cv = curve(A.ax, d["ve"], d["h2_curve"], GENE, stroke_width=4)
        pts = VGroup(Dot(A.ax.c2p(0.25, d["h2_at_small"]), radius=0.09, color=WHITE),
                     Dot(A.ax.c2p(3.0, d["h2_at_large"]), radius=0.09, color=WHITE))
        pl = VGroup(label(rf"${d['h2_at_small']:.1f}$", font_size=29).next_to(pts[0], RIGHT, buff=0.12),
                    label(rf"${d['h2_at_large']:.2f}$", font_size=29).next_to(pts[1], UP, buff=0.12))
        B = axes([8, 18], [0, 1.0], x_length=4.4, y_length=2.0, xticks=[float(a) for a in d["ages"]], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"age", ylabel=r"heritability of reasoning scores",
                 center=[3.3, 1.35, 0])
        ap = VGroup(*[Dot(B.ax.c2p(float(a), float(v)), radius=0.1, color=DATA) for a, v in zip(d["ages"], d["h2_age"])])
        al = VGroup(*[label(rf"${v:.2f}$", font_size=27, color=DATA).next_to(B.ax.c2p(float(a), float(v)), UP, buff=0.12)
                      for a, v in zip(d["ages"], d["h2_age"])])
        seg = VMobject(color=DATA, stroke_width=3).set_points_as_corners(
            [B.ax.c2p(float(a), float(v)) for a, v in zip(d["ages"], d["h2_age"])])
        tk = wrapped_label(rf"American seven-year-olds, {t['pairs']} twin pairs: \ in the poorest families the shared home "
                           rf"took {pct(t['poor_shared'])} of the differences and genes almost none; \ in affluent "
                           r"families, nearly the reverse. \ Later samples disagree.", 6.6, 28, DATA).move_to([3.3, -1.45, 0])
        keep_in_frame(tk)
        end = wrapped_label(r"What is left: \ in this population, \ genes matter for this trait, \ about this much.",
                            12.4, 31, P.ACCENT).move_to([0, -2.95, 0])
        src = published_tag(archive.HAWORTH_2010.cite + r"; \ " + archive.TURKHEIMER_2003.cite)
        with self.voiceover(
            "Four. It isn't a constant. Heritability is a share, so it changes when the other share "
            "changes. <bookmark mark='a'/> Make everyone's environment more alike, and the environmental "
            "spread shrinks, and heritability goes up, with no change in any gene. With the spread of "
            f"environments at a quarter of the genetic spread it's {d['h2_at_small']:.1f}. At three "
            f"times, it's {d['h2_at_large']:.2f}. <bookmark mark='b'/> A study of American "
            "seven-year-olds in 2003 reported just that. Among the poorest families, the shared home "
            f"accounted for {100 * t['poor_shared']:.0f} percent of the differences in test scores and "
            "the genes for almost none. Among affluent families it was nearly the reverse. Later samples "
            "disagree about how general that is. <bookmark mark='c'/> And the heritability of scores on "
            f"reasoning tests rises with age: {100 * d['h2_age'][0]:.0f} percent at nine, "
            f"{100 * d['h2_age'][1]:.0f} at twelve, {100 * d['h2_age'][2]:.0f} at seventeen. One reading "
            "is that older children choose more of their own surroundings. <bookmark mark='d'/> So: not "
            "fixed, not about groups, not about you, and not a constant. What's left is a modest and "
            "useful number. It says that in a given population genes matter for a trait, and roughly how "
            "much. And it tells you where to look next."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(cv), run_time=1.5)
            self.play(FadeIn(pts), FadeIn(pl))
            vo.wait_until("b")
            self.play(FadeIn(tk))
            vo.wait_until("c")
            self.play(FadeIn(B), Create(seg), FadeIn(ap, lag_ratio=0.3), FadeIn(al, lag_ratio=0.3), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()
