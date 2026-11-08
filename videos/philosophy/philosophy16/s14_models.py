from __future__ import annotations

from videos.philosophy.philosophy16.common import *  # noqa: F403

AICC, BICC, TESTC, TRAINC = "#F2A65A", "#6FB7FF", "#5FD38D", "#9AA5B8"


class Models(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Choosing a model", r"Truth, \ or prediction?", lit=(1973,), part=PART)
        with self.voiceover("Chapter thirteen. Choosing a model."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.criteria()
        self.curves()
        self.picks()
        self.meaning()

    def criteria(self):
        head = label(r"Two penalties for complexity", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        aic = VGroup(label(r"Akaike \ (1973)", font_size=24, color=AICC),
                     MathTex(r"\mathrm{AIC} = -2 \log \hat L + 2k", font_size=36, color=AICC),
                     label(r"estimates predictive accuracy on new data", font_size=20, color=GREY_A)).arrange(
            DOWN, buff=0.2)
        bic = VGroup(label(r"Schwarz \ (1978)", font_size=24, color=BICC),
                     MathTex(r"\mathrm{BIC} = -2 \log \hat L + k \log n", font_size=36, color=BICC),
                     label(r"approximates $-2 \log$ of the Bayesian evidence", font_size=20, color=GREY_A)).arrange(
            DOWN, buff=0.2)
        VGroup(aic, bic).arrange(RIGHT, buff=1.4).next_to(head, DOWN, buff=0.6)
        note = stack([(r"$k$: \ adjustable parameters; \ $\hat L$: \ the best fit's likelihood", WHITE),
                      (r"for $n \ge 8$, \ BIC punishes complexity harder", GREY_A),
                      (r"Forster and Sober \ (1994): \ simplicity matters because it predicts better", GOAL)],
                     font_size=22).next_to(VGroup(aic, bic), DOWN, buff=0.6)
        with self.voiceover(
            "Part 15 ended with the curve-fitting problem: more parameters always fit better. Statistics offers two "
            "standard penalties. <bookmark mark='a'/>Hirotugu Akaike's criterion of 1973 subtracts two for every "
            "adjustable parameter from twice the log-likelihood. He derived it as an estimate of how well the "
            "fitted model will predict new data. <bookmark mark='b'/>Gideon Schwarz's criterion of 1978 charges log "
            "n per parameter instead. It approximates the Bayesian evidence for the model. "
            "<bookmark mark='c'/>For any sample of eight or more, it punishes complexity harder. "
            "<bookmark mark='d'/>Malcolm Forster and Elliott Sober argued in 1994 that Akaike had answered an old "
            "philosophical question: simplicity matters, not because simple theories are more likely true, but "
            "because they predict better."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(aic))
            vo.wait_until("b")
            self.play(FadeIn(bic))
            vo.wait_until("c")
            self.play(FadeIn(note[0]), FadeIn(note[1]))
            vo.wait_until("d")
            self.play(FadeIn(note[2]))
        self.clear_scene()

    def curves(self):
        d = load("aic")
        head = label(r"Fit, \ estimate, \ and the truth about prediction", font_size=30, color=CONN).to_edge(UP,
                                                                                                           buff=0.3)
        sub = label(r"truth: \ a cubic plus noise; \ " + str(d["n"]) + r" points; \ " + str(d["reps"]) +
                    r" training sets; \ log-likelihood per point", font_size=20, color=GREY_A).next_to(head, DOWN,
                                                                                                buff=0.2)
        K = 6
        ks = list(range(K))
        off = 1.8                        # plot log-likelihood + 1.8 so the x-axis sits at the bottom
        ax = Axes(x_range=[0, K - 1, 1], y_range=[0, 1.4, 0.4], x_length=7.4, y_length=4.0, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16},
                  x_axis_config={"include_numbers": True}, y_axis_config={"include_numbers": False}).move_to(
            [-2.0, -1.1, 0])
        yt = VGroup(*[label(f"{v - off:.1f}", font_size=15, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (0, 0.4, 0.8, 1.2)])
        xl = label(r"polynomial degree", font_size=18, color=GREY_B).next_to(ax.x_axis, DOWN, buff=0.3)
        train = series_plot(ax, [v + off for v in d["train_loglik"][:K]], TRAINC, xs=ks, width=4)
        est = series_plot(ax, [v + off for v in d["aic_estimate"][:K]], AICC, xs=ks, width=4)
        test = series_plot(ax, [v + off for v in d["test_loglik"][:K]], TESTC, xs=ks, width=4)
        leg = stack([(r"fit to the training data: \ always rises", TRAINC),
                     (r"AIC's estimate: \ fit minus $k/n$", AICC),
                     (r"actual fit to new data", TESTC),
                     (r"the estimate tracks the truth, \ and peaks at degree " + str(d["best_predictive"]), GOAL)],
                    font_size=20, aligned_edge=LEFT, width=4.8).move_to([4.6, -0.6, 0])
        with self.voiceover(
            "The Reasoner tests the claim. <bookmark mark='a'/>The truth is a cubic with noise. Draw thirty points, "
            "fit polynomials of each degree, and repeat three hundred times. <bookmark mark='b'/>The fit to the "
            "training data rises with every added degree. <bookmark mark='c'/>The real test is the fit to fresh "
            "data from the same source, which rises to the true degree and then falls. <bookmark mark='d'/>Akaike's "
            "estimate, the training fit minus a penalty, is computed from the training data alone, and it tracks "
            "the fresh-data fit closely, peaking at the right place. That is the sense in which AIC estimates "
            "predictive accuracy."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(ax), FadeIn(xl), FadeIn(yt))
            vo.wait_until("b")
            self.play(Create(train), FadeIn(leg[0]))
            vo.wait_until("c")
            self.play(Create(test), FadeIn(leg[2]))
            vo.wait_until("d")
            self.play(Create(est), FadeIn(leg[1]), FadeIn(leg[3]))
        self.clear_scene()

    def picks(self):
        d = load("aic")
        head = label(r"Which degree does each criterion choose?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        degs = d["degrees"]
        base = -2.4
        g = VGroup()
        for i, k in enumerate(degs):
            x = -5.4 + i * 1.15
            for j, (picks, c) in enumerate(((d["aic_picks"], AICC), (d["bic_picks"], BICC))):
                h = picks[k] / d["reps"] * 4.0
                b = Rectangle(width=0.4, height=max(h, 0.02), stroke_width=0, fill_color=c, fill_opacity=0.85)
                b.move_to([x + (j - 0.5) * 0.44, base + b.height / 2, 0])
                g.add(b)
            g.add(label(str(k), font_size=18, color=GOAL if k == d["true_degree"] else GREY_B).move_to(
                [x, base - 0.25, 0]))
        axis = Line([-6.0, base, 0], [3.1, base, 0], color=GREY_C, stroke_width=2)
        xl = label(r"chosen degree \ (truth: 3)", font_size=18, color=GREY_B).move_to([-1.4, base - 0.6, 0])
        a3 = d["aic_picks"][3] / d["reps"]
        b3 = d["bic_picks"][3] / d["reps"]
        over_a = sum(d["aic_picks"][4:]) / d["reps"]
        over_b = sum(d["bic_picks"][4:]) / d["reps"]
        side = stack([(r"AIC: \ the true degree " + f"{100 * a3:.0f}" + r"\%; \ too complex " + f"{100 * over_a:.0f}" +
                       r"\%", AICC),
                      (r"BIC: \ the true degree " + f"{100 * b3:.0f}" + r"\%; \ too complex " + f"{100 * over_b:.0f}" +
                       r"\%", BICC),
                      (r"BIC is \textit{consistent}: \ it finds the true model as $n \to \infty$", BICC),
                      (r"AIC is \textit{efficient}: \ best predictions when no model is true", AICC)], font_size=20,
                     aligned_edge=LEFT, width=4.0).move_to([5.0, -0.6, 0])
        with self.voiceover(
            "Now ask which degree each criterion picks, over the three hundred training sets. "
            "<bookmark mark='a'/>Akaike's criterion picks the true degree about two thirds of the time, and a more "
            "complex model a third of the time. <bookmark mark='b'/>Schwarz's criterion picks the true degree "
            "more than eight times in ten. <bookmark mark='c'/>That is a general result. The Bayesian criterion is "
            "consistent: if one of the candidate models is true, it finds it as the data grow. "
            "<bookmark mark='d'/>Akaike's is efficient instead: when none of the models is exactly true, as in most "
            "real science, it gives the best predictions. Truth or prediction: the choice of criterion is the "
            "choice of aim."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(xl))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) if isinstance(b, Rectangle) else FadeIn(b) for b in g],
                                  lag_ratio=0.03), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def meaning(self):
        head = label(r"What the criteria assume", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"realism", r"BIC aims at the true model, \ assuming it is among the candidates", BICC),
            (r"instrumentalism", r"AIC aims at prediction, \ and needs no model to be true \ (Sober, \ 2015)", AICC),
            (r"Part 15", r"MDL, \ Solomonoff and Kelly gave three more reasons to prefer simplicity", FISH),
            (r"Part 18", r"whether science aims at truth or at prediction: \ realism and its rivals", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.6, x_text=-2.6)
        with self.voiceover(
            "Each criterion carries a philosophy. <bookmark mark='a'/>The Bayesian criterion aims at the true model, "
            "and assumes it is among the candidates. <bookmark mark='b'/>Akaike's aims at prediction, and needs no "
            "model to be true: Elliott Sober reads it as a kind of instrumentalism. <bookmark mark='c'/>Part 15 gave "
            "three further reasons to prefer simple models: compression, the universal prior, and Kelly's efficient "
            "path to the truth. <bookmark mark='d'/>Whether science aims at truth or only at successful prediction "
            "is the question of Part 18."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
