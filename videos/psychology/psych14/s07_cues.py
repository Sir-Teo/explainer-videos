from __future__ import annotations

import numpy as np

from videos.psychology.psych14.common import *  # noqa: F403


class Cues(VoiceoverScene):
    def construct(self):
        self.card()
        self.rule()
        self.experiment()
        self.curves()
        self.table()
        self.ventriloquist()
        self.limits()

    def card(self):
        card = chapter_card(6, r"Combining cues", r"How should two uncertain senses be put together?",
                            lit={2002: r"Ernst \& Banks", 2004: r"Alais \& Burr"}, part=PART, scale=("mind",),
                            marr=("what", "how"))
        with self.voiceover("Chapter six. Combining cues."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def rule(self):
        head = heading(r"Two cues, \ one estimate")
        lines = VGroup(
            MathTex(r"\hat s_V \sim N(s, \sigma_V^2), \qquad \hat s_H \sim N(s, \sigma_H^2)", font_size=42),
            MathTex(r"\hat s = w_V\,\hat s_V + w_H\,\hat s_H, \qquad w_V = \frac{1/\sigma_V^2}{1/\sigma_V^2 + 1/\sigma_H^2}",
                    font_size=42, color=POST),
            MathTex(r"\sigma^2 = \frac{\sigma_V^2\,\sigma_H^2}{\sigma_V^2 + \sigma_H^2} \;\le\; \min(\sigma_V^2, \sigma_H^2)",
                    font_size=42, color=POST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, 1.0, 0])
        rows = rows_of([
            (r"the same two formulas: \ a cue is just a measurement, \ and the other cue acts as its prior", WHITE),
            (r"two predictions from single-cue data alone: \ the weights, \ and the combined precision", WORLD),
            (r"with a flat prior this is also the maximum-likelihood estimate, \ and the best unbiased one", GREY_A),
        ], 12.4, 28, 0.3).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Suppose you look at an object and hold it at the same time. Vision gives an estimate of its height, "
            "with some noise; touch gives another, with different noise. <bookmark mark='a'/> Write them as two "
            "normal measurements of the same height s, with standard deviations sigma V and sigma H. "
            "<bookmark mark='b'/> Last chapter's algebra applies directly: treat one cue as the prior for the other. "
            "The best estimate is a weighted average, with each cue weighted by its precision. "
            "<bookmark mark='c'/> And the combined variance is smaller than either cue's alone. "
            "<bookmark mark='d'/> Here's what makes this science rather than arithmetic. Measure each sense on its "
            "own, and you can predict two things in advance: the weight each sense will get when both are present, "
            "and how precise the combination will be. <bookmark mark='e'/> With no prior over the height itself, this "
            "is the maximum-likelihood estimate, and among unbiased averages of the two cues the one with the least "
            "variance."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(lines[0]))
            vo.wait_until("b")
            self.play(Write(lines[1]), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Write(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def experiment(self):
        head = heading(r"Ernst and Banks, \ 2002")
        # a ridge seen in stereo, felt with two force-feedback arms
        ridge = Polygon([-2.2, -0.6, 0], [-0.6, -0.6, 0], [-0.6, 0.5, 0], [0.6, 0.5, 0], [0.6, -0.6, 0], [2.2, -0.6, 0],
                        [2.2, -1.2, 0], [-2.2, -1.2, 0], color=GREY_B, stroke_width=3, fill_color=GREY_E, fill_opacity=1)
        dots = VGroup(*[Dot([x, y, 0], radius=0.035, color=VISION) for x, y in
                        np.random.default_rng(14).uniform([-2.1, -0.55], [2.1, 0.45], size=(60, 2))])
        thumb = VGroup(Line([-0.75, 0.5, 0], [-1.6, 2.0, 0], color=TOUCH, stroke_width=6), Dot([-0.75, 0.5, 0], color=TOUCH))
        finger = VGroup(Line([0.75, 0.5, 0], [1.6, 2.0, 0], color=TOUCH, stroke_width=6), Dot([0.75, 0.5, 0], color=TOUCH))
        hgt = DoubleArrow([2.6, -0.6, 0], [2.6, 0.5, 0], buff=0, color=WORLD, stroke_width=3, tip_length=0.15)
        hl = label(r"height", font_size=22, color=WORLD).next_to(hgt, RIGHT, buff=0.1)
        fig = VGroup(ridge, dots, thumb, finger, hgt, hl).move_to([-3.4, 0.0, 0])
        rows = rows_of([
            (r"a raised bar, \ seen in a stereo display \ and felt through two force-feedback arms", WHITE),
            (r"which of two bars is taller? \ by eye, \ by hand, \ and with both", WORLD),
            (r"noise added to the stereo display, \ at four levels, \ to make vision worse", VISION),
            (r"a small conflict between what was seen and felt, \ to measure the weights", PRIOR),
        ], 5.6, 26, 0.34).move_to([3.6, 0.0, 0])
        keep_in_frame(rows)
        tag = published_tag(rf"design: \ {archive.ERNST_BANKS_2002.cite}, \ redrawn")
        with self.voiceover(
            "In 2002, Marc Ernst and Martin Banks ran the test. <bookmark mark='a'/> Observers looked at a raised "
            "bar, rendered as a random-dot stereogram, and at the same time felt it between thumb and finger through "
            "two force-feedback robot arms. The visual bar and the felt bar were made to coincide. "
            "<bookmark mark='b'/> On each trial they judged which of two bars was taller, using vision alone, touch "
            "alone, or both. <bookmark mark='c'/> To control how good vision was, they added noise to the stereogram "
            "at four levels, from none to a great deal. <bookmark mark='d'/> And to measure the weights, they "
            "sometimes made the seen bar and the felt bar slightly different heights. If vision dominates, the "
            "combined percept follows the seen bar; if touch does, the felt one. Where it falls between them gives "
            "the weights."
        ) as vo:
            self.play(FadeIn(head), FadeIn(fig[0]), FadeIn(fig[4:]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(dots), FadeIn(thumb), FadeIn(finger), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), dots.animate.shift(UP * 0.05))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def curves(self):
        d = load("cues")
        head = heading(r"Psyche at the bench: \ one noise level")
        A = axes([-14, 14], [0, 1], x_length=7.2, y_length=4.4, xticks=[-14, -7, 0, 7, 14], yticks=[0, 0.5, 1],
                 xlabel=r"comparison minus standard (mm)", ylabel=r"P(comparison looks taller)", center=[-2.4, -0.3, 0])
        ax = A.ax
        cv = curve(ax, d["ex_d"], d["ex_v"], VISION, stroke_width=4, smooth=True)
        ch = curve(ax, d["ex_d"], d["ex_h"], TOUCH, stroke_width=4, smooth=True)
        cb = curve(ax, d["ex_d"], d["ex_both"], POST, stroke_width=5, smooth=True)
        dv = scatter(ax, d["ex_d"], d["ex_v"], VISION, radius=0.05)
        dh = scatter(ax, d["ex_d"], d["ex_h"], TOUCH, radius=0.05)
        db = scatter(ax, d["ex_d"], d["ex_both"], POST, radius=0.05)
        leg = legend([(VISION, r"vision"), (TOUCH, r"touch"), (POST, r"both")], font_size=24)
        leg.move_to(ax.c2p(-9.5, 0.8))
        rows = rows_of([
            (r"each point: \ 2{,}000 two-interval trials", GREY_A),
            (r"steeper means more precise: \ the slope gives each cue's $\sigma$", WHITE),
            (r"with both, \ steeper than either alone", POST),
        ], 4.4, 26, 0.34).move_to([4.7, 0.0, 0])
        keep_in_frame(rows)
        tag = psyche_tag(rf"simulated: \ Psyche, \ $\sigma_V$ = {d['ex_sv']:g} mm, \ $\sigma_H$ = {d['sh']:g} mm")
        with self.voiceover(
            "We can run the same experiment on Psyche, whose vision and touch we built, with their noise known. "
            "<bookmark mark='a'/> Each curve is a psychometric function from Part 11: the chance of calling the "
            "comparison bar taller, against how much taller it really is, with two thousand trials a point. "
            "<bookmark mark='b'/> Vision first, then touch. The steeper the curve, the more precise the sense, and "
            "fitting a cumulative normal gives each sense's sigma. <bookmark mark='c'/> And with both senses, the "
            "curve is steeper than either. Combining two cues made Psyche more precise than its better sense."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(leg[0]), FadeIn(dv), Create(cv))
            vo.wait_until("b")
            self.play(FadeIn(leg[1]), FadeIn(dh), Create(ch), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(leg[2]), FadeIn(db), Create(cb), FadeIn(rows[2]))
        self.clear_scene()

    def table(self):
        d = load("cues")
        head = heading(r"Predicted from each sense alone, \ then measured with both")
        hdr = [r"vision's $\sigma$", r"weight on vision", r"", r"combined $\sigma$", r""]
        sub = [r"(mm)", r"predicted", r"measured", r"predicted", r"measured"]
        cells = [[label(h, font_size=26, color=GREY_B) for h in hdr], [label(s, font_size=22, color=GREY_B) for s in sub]]
        for r in d["rows"]:
            cells.append([label(rf"{r['sv']:.1f}", font_size=28, color=VISION),
                          label(rf"{r['pred_w']:.2f}", font_size=28, color=PRIOR),
                          label(rf"{r['obs_w']:.2f}", font_size=28, color=POST),
                          label(rf"{r['pred_sd']:.2f}", font_size=28, color=PRIOR),
                          label(rf"{r['obs_sd']:.2f}", font_size=28, color=POST)])
        tab = MobjectTable(cells, include_outer_lines=False, h_buff=0.6, v_buff=0.28,
                           line_config={"stroke_width": 1, "color": GREY_D}).move_to([0, 0.6, 0])
        rows = rows_of([
            (r"as vision gets noisier, \ its weight falls from 0.88 to 0.31, \ as predicted", WHITE),
            (r"Psyche is optimal by construction: \ this checks the method, \ not the claim", GREY_A),
            (r"Ernst and Banks's four observers came close to the same predictions", DATA),
        ], 12.4, 27, 0.28).to_edge(DOWN, buff=0.7)
        tag = psyche_tag(r"simulated: \ Psyche, \ touch's $\sigma$ 4 mm; \ 2{,}000 trials a point")
        with self.voiceover(
            "Now the full design, at four levels of visual noise. <bookmark mark='a'/> Each row: vision's sigma, "
            "measured alone; the weight on vision, predicted from the two single-sense curves and then measured "
            "from the conflict trials; and the combined sigma, predicted and measured. <bookmark mark='b'/> As vision "
            "gets noisier, its weight falls from point eight eight to point three one, and the measured weights and "
            "precisions track the predictions to the second decimal place. <bookmark mark='c'/> A caution, though. "
            "Psyche combines cues optimally because we built it to. So this table checks the method: that single-cue "
            "curves really do predict the combination, and that conflict trials recover the weights. Whether people "
            "do it is the experiment's question. <bookmark mark='d'/> Ernst and Banks's observers came close. Their "
            "weights shifted toward touch as the visual noise rose, about as predicted, and their combined "
            "thresholds were near the optimal ones."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(tab), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def ventriloquist(self):
        head = heading(r"The ventriloquist, \ explained")
        sharp = Dot([-4.6, 0.8, 0], radius=0.18, color=VISION)
        blur = VGroup(*[Circle(radius=0.15 * k, stroke_width=0, fill_color=VISION, fill_opacity=0.12) for k in range(1, 9)])
        blur.move_to([-1.8, 0.8, 0])
        sl = label(r"a sharp flash", font_size=24, color=VISION).next_to(sharp, DOWN, buff=0.5)
        bl = label(r"a blurred one", font_size=24, color=VISION).next_to(blur, DOWN, buff=0.15)
        rows = rows_of([
            (r"a flash and a click from slightly different places: \ where did it happen?", WHITE),
            (r"sharp flash: \ vision is precise, \ and drags the sound to it; \ the ventriloquist's dummy speaks", VISION),
            (r"blurred enough: \ sound is the more precise cue, \ and now it drags the flash", TOUCH),
            (r"vision does not dominate hearing: \ precision does", POST),
        ], 6.2, 26, 0.34).move_to([3.3, 0.0, 0])
        keep_in_frame(rows)
        tag = published_tag(archive.ALAIS_BURR_2004.cite)
        with self.voiceover(
            "The same rule explains an old piece of stagecraft. <bookmark mark='a'/> In 2004, David Alais and David "
            "Burr presented a flash of light and a click from slightly different places, and asked where the event "
            "happened. <bookmark mark='b'/> With a sharp flash, vision is far more precise than hearing about "
            "location, so it gets nearly all the weight, and the sound seems to come from the flash. That's the "
            "ventriloquist's trick: the voice seems to come from the dummy's moving mouth. <bookmark mark='c'/> But "
            "Alais and Burr blurred the flash, until it was a large faint smudge. Then hearing was the more precise "
            "cue, and the flash was pulled toward the click. <bookmark mark='d'/> So vision doesn't dominate hearing, "
            "as textbooks once said. Precision dominates, and vision is usually more precise about where things are."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(sharp), FadeIn(sl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(blur), FadeIn(bl), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def limits(self):
        head = heading(r"How optimal is optimal?")
        rows = rows_of([
            (r"near-optimal combination has been found for many pairs of cues and senses", POST),
            (r"children: \ until about eight to ten, \ one sense dominates where adults combine \ (Gori and colleagues, \ 2008)", WORLD),
            (r"2018: \ Rahnev and Denison list many departures from optimality, \ in many tasks", BAD),
            (r"a model can be fitted after the fact to almost anything: \ what makes it a test is the advance prediction", PRIOR),
        ], 12.6, 28, 0.4).move_to([0, -0.1, 0])
        tag = published_tag(archive.RAHNEV_DENISON_2018.cite)
        with self.voiceover(
            "How far does the optimal observer go? <bookmark mark='a'/> Reliability-weighted combination has been found "
            "for vision with touch, vision with hearing, and many pairs of visual cues: stereo with texture, motion "
            "with shading. <bookmark mark='b'/> But not from birth. In 2008, Monica Gori and colleagues found that "
            "children below about eight to ten years old don't combine vision and touch this way: one sense or the "
            "other dominates, even when the combination would help them. <bookmark mark='c'/> And in 2018, Dobromir "
            "Rahnev and Rachel Denison reviewed the evidence on perceptual decisions and listed many ways that people "
            "fall short of the optimum, cue combination included. <bookmark mark='d'/> There's a methodological point "
            "too. With freedom to choose the prior, the noise and the loss, a Bayesian model can be fitted to almost "
            "any data after the fact. What made Ernst and Banks a real test is that the prediction was made in "
            "advance, from separate measurements, with nothing left to adjust."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
