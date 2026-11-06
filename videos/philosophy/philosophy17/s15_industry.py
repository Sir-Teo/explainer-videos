from __future__ import annotations

from videos.philosophy.philosophy17.common import *  # noqa: F403


class Industry(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"Causes at work", r"Where is causal inference used today?", lit=(2013, 2018),
                            part=PART)
        with self.voiceover("Chapter fourteen. Causes at work."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.cuped()
        self.uplift()
        self.causal_ml()
        self.invariance()
        self.llms()

    def cuped(self):
        d = load("industry")["cuped"]
        head = label(r"Experiments at scale: \ CUPED", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        eq = MathTex(r"\tilde Y = Y - \theta\,(X_{\text{pre}} - \bar X_{\text{pre}}), \qquad "
                     r"\theta = \frac{\mathrm{cov}(X_{\text{pre}}, Y)}{\mathrm{var}(X_{\text{pre}})}", font_size=32,
                     color=GOAL).next_to(head, DOWN, buff=0.4)
        vr = MathTex(r"\mathrm{var}(\tilde Y) = (1 - \rho^2)\,\mathrm{var}(Y)", font_size=32, color=OK).next_to(
            eq, DOWN, buff=0.3)
        hd = [r"", r"\text{mean estimate}", r"\text{spread (sd)}"]
        rows = [[MathTex(r"\text{plain}", font_size=24), MathTex(f"{d['mean_plain']:.4f}", font_size=24),
                 MathTex(f"{d['sd_plain']:.4f}", font_size=24, color=BAD)],
                [MathTex(r"\text{CUPED}", font_size=24), MathTex(f"{d['mean_cuped']:.4f}", font_size=24),
                 MathTex(f"{d['sd_cuped']:.4f}", font_size=24, color=OK)]]
        grid = ValueGrid(hd, rows, col_w=[2.0, 3.0, 3.0], cell_h=0.55, font_size=20).next_to(vr, DOWN, buff=0.4)
        cap = stack([(f"{d['reps']}" + r" simulated A/B tests, \ " + f"{d['n']:,}".replace(",", "{,}") +
                      r" users, \ true lift " + f"{d['effect']:.2f}" + r", \ $\rho = " + f"{d['rho']:.1f}" + r"$", GREY_A),
                     (r"variance ratio " + f"{d['var_ratio']:.2f}" + r" \ (theory " + f"{d['theory']:.2f}" +
                      r"): \ half the users for the same precision", OK),
                     (r"Deng, \ Xu, \ Kohavi and Walker \ (2013): \ a covariate from \textit{before} randomization "
                      r"cannot be a collider or a mediator", GREY_A)], font_size=20).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The largest users of causal inference today are technology companies, which run tens of thousands of "
            "randomized experiments a year. One small piece of causal reasoning saves them a fortune. "
            "<bookmark mark='a'/>Subtract from each user's outcome a multiple of the same metric measured before "
            "the experiment began. <bookmark mark='b'/>The variance falls by the factor one minus rho squared, "
            "where rho is the correlation between before and after. <bookmark mark='c'/>The Reasoner ran four "
            "hundred simulated tests. Both estimates are centred on the true lift; the adjusted one is much less "
            "spread out. <bookmark mark='d'/>The variance is roughly halved, as the theory says: the same "
            "precision from half the users. <bookmark mark='e'/>Why is this adjustment safe, when Chapter eight "
            "warned against adjusting for the wrong variables? Because a quantity measured before randomization "
            "cannot be an effect of the treatment: it is neither a collider nor a mediator."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(Write(vr))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule), FadeIn(VGroup(*grid.cell[0])),
                      FadeIn(VGroup(*grid.cell[1])), FadeIn(cap[0]))
            vo.wait_until("d")
            self.play(FadeIn(cap[1]))
            vo.wait_until("e")
            self.play(FadeIn(cap[2]))
        self.clear_scene()

    def uplift(self):
        d = load("industry")["uplift"]
        head = label(r"Uplift: \ whom should a campaign contact?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        quad = VGroup()
        cells = [(r"sure things", r"buy either way", EFFECT, (-1, 1)), (r"persuadables", r"buy only if contacted",
                                                                        OK, (1, 1)),
                 (r"lost causes", r"never buy", HIDDEN, (-1, -1)), (r"sleeping dogs", r"contact puts them off", BAD,
                                                                    (1, -1))]
        for name, gloss, c, (i, j) in cells:
            box = RoundedRectangle(width=2.6, height=1.2, corner_radius=0.1, color=c, stroke_width=3).move_to(
                [-3.6 + i * 1.4, 0.7 + j * 0.7, 0])
            t = VGroup(label(name, font_size=20, color=c), label(gloss, font_size=16, color=GREY_A)).arrange(
                DOWN, buff=0.1).move_to(box)
            quad.add(VGroup(box, t))
        ql = label(r"Chapter 9's types, \ with a fourth: \ the defiers", font_size=18, color=GREY_A).next_to(
            quad, DOWN, buff=0.25)
        hd = [r"\text{contact the top } 20\%", r"\text{purchases caused}"]
        rows = [[MathTex(r"\text{by response rate}", font_size=22), MathTex(f"{d['gain_response']:+,.0f}".replace(
            ",", "{,}"), font_size=24, color=BAD)],
                [MathTex(r"\text{at random}", font_size=22), MathTex(f"{d['gain_random']:+,.0f}".replace(",", "{,}"),
                                                                    font_size=24, color=GREY_A)],
                [MathTex(r"\text{by uplift}", font_size=22), MathTex(f"{d['gain_uplift']:+,.0f}".replace(",", "{,}"),
                                                                    font_size=24, color=OK)]]
        grid = ValueGrid(hd, rows, col_w=[3.8, 2.8], cell_h=0.55, font_size=20).move_to([3.4, 0.8, 0])
        gl = label(f"{d['n']:,}".replace(",", "{,}") + r" customers in a randomized trial, \ " + f"{d['segments']}" +
                   r" segments", font_size=18, color=GREY_A).next_to(grid, UP, buff=0.25)
        foot = stack([(r"response models find the sure things and the sleeping dogs; \ uplift models find the "
                       r"persuadables", WHITE),
                      (r"an uplift is a rung-2 quantity: \ it needs the randomized control group", GOAL)],
                     font_size=20).to_edge(DOWN, buff=0.4)
        assert d["gain_uplift"] >= d["best_possible"] - 1e-6
        with self.voiceover(
            "Marketing gives a sharper example. <bookmark mark='a'/>Customers come in four kinds: sure things, who "
            "buy either way; persuadables, who buy only if contacted; lost causes; and sleeping dogs, whom contact "
            "puts off. They are Chapter nine's types, with a fourth, the defiers. <bookmark mark='b'/>The Reasoner "
            "simulated a randomized campaign with two hundred thousand customers in sixteen segments, and then "
            "chose a fifth of the segments to contact. <bookmark mark='c'/>Contact the segments most likely to buy "
            "when contacted, as a standard response model would, and the campaign causes over five thousand fewer "
            "purchases: those segments are full of sure things and sleeping dogs. <bookmark mark='d'/>Contact at "
            "random, and it still loses. <bookmark mark='e'/>Contact by uplift, the difference the contact makes, "
            "and it causes over seven thousand extra purchases, the best possible. <bookmark mark='f'/>An uplift is "
            "a rung-two quantity. It cannot be learned from who bought, only from a comparison with a control "
            "group."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(q) for q in quad], lag_ratio=0.25), FadeIn(ql))
            vo.wait_until("b")
            self.play(FadeIn(gl), FadeIn(grid.head), Create(grid.rule))
            for mk, r in zip("cde", grid.cell):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*r)))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def causal_ml(self):
        head = label(r"Causal machine learning", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"doubly robust", r"combine a model of the outcome with a model of who is treated: \ right if either is "
                               r"\ (Robins, \ Rotnitzky and Zhao, \ 1994)", EFFECT),
            (r"double ML", r"use flexible learners for both, \ and cross-fitting to remove their bias \ "
                           r"(Chernozhukov et al., \ 2018)", OK),
            (r"causal forests", r"estimate how the effect varies from person to person \ (Wager and Athey, \ 2018)",
             CAUSE),
            (r"the division of labour", r"machine learning fits the nuisance functions; \ the causal assumptions "
                                        r"still come from a graph or a design", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.8, x_text=-2.8)
        with self.voiceover(
            "Machine learning and causal inference have merged into a field of their own. "
            "<bookmark mark='a'/>Doubly robust estimators, due to James Robins and colleagues, combine a model of "
            "the outcome with a model of who gets treated, and are right if either model is. "
            "<bookmark mark='b'/>Double machine learning, from Victor Chernozhukov and colleagues, lets both models "
            "be flexible learners such as forests or neural networks, and removes their bias by fitting on one part "
            "of the data and estimating on another. <bookmark mark='c'/>Causal forests, from Stefan Wager and Susan "
            "Athey, estimate how the effect differs from person to person. <bookmark mark='d'/>The division of "
            "labour is the lesson. Machine learning supplies flexible fits; the causal assumptions, which variables "
            "to adjust for and why, must still come from a graph or a design."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def invariance(self):
        d = load("industry")["icp"]
        head = label(r"Invariance as a guide to causes", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        g = CausalGraph({"X": [-5.2, 0.8, 0], "Y": [-3.4, 0.8, 0], "Z": [-1.6, 0.8, 0], "E": [-5.2, 2.3, 0]},
                        [("X", "Y"), ("Y", "Z"), ("E", "X")], radius=0.4, font_size=20,
                        colors={"X": CAUSE, "Y": EFFECT, "Z": WHITE, "E": DOC})
        ez = DashedLine([-5.0, 2.3, 0], [-1.7, 1.25, 0], color=DOC)
        hd = [r"\text{regress } Y \text{ on}", r"\text{environment 1}", r"\text{environment 2}"]
        rows = [[MathTex(r"X \;(\text{its cause})", font_size=22), MathTex(f"{d['1']['Y_on_X']:.2f}", font_size=24,
                                                                          color=OK),
                 MathTex(f"{d['2']['Y_on_X']:.2f}", font_size=24, color=OK)],
                [MathTex(r"Z \;(\text{its effect})", font_size=22), MathTex(f"{d['1']['Y_on_Z']:.2f}", font_size=24,
                                                                           color=BAD),
                 MathTex(f"{d['2']['Y_on_Z']:.2f}", font_size=24, color=BAD)]]
        grid = ValueGrid(hd, rows, col_w=[3.0, 2.4, 2.4], cell_h=0.55, font_size=20).move_to([2.8, 0.8, 0])
        notes = stack([(r"a second environment shifts $X$, \ and changes how $Z$ responds to $Y$", DOC),
                       (r"only the causal coefficient survives the change: \ Woodward's invariance, \ as a test", OK),
                       (r"invariant causal prediction \ (Peters, \ B\"uhlmann and Meinshausen, \ 2016): \ keep the "
                        r"predictors whose relation to $Y$ never changes", WHITE),
                       (r"why it matters: \ models that rely on effects and proxies break when the world shifts", GOAL)],
                      font_size=20, width=12.6).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Chapter five's idea of invariance has become a method. <bookmark mark='a'/>X causes Y, and Y causes Z. "
            "Data come from two environments: in the second, X has a different distribution, and Z responds to Y "
            "differently. <bookmark mark='b'/>Regress Y on its cause: the coefficient is one in both "
            "environments. <bookmark mark='c'/>Regress Y on its effect: point eight nine in one, one point nine in "
            "the other. <bookmark mark='d'/>Only the causal relation survives the change. "
            "<bookmark mark='e'/>Jonas Peters, Peter Bühlmann and Nicolai Meinshausen turned this into invariant "
            "causal prediction: keep the predictors whose relation to the outcome is the same in every environment. "
            "<bookmark mark='f'/>The payoff is robustness. A model that predicts from effects and proxies may break "
            "when the world shifts; one that predicts from causes keeps working."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), Create(ez))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule), FadeIn(VGroup(*grid.cell[0])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*grid.cell[1])))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
            vo.wait_until("e")
            self.play(FadeIn(notes[2]))
            vo.wait_until("f")
            self.play(FadeIn(notes[3]))
        self.clear_scene()

    def llms(self):
        head = label(r"Language models and causal reasoning", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"common-sense pairs", r"K{\i}c{\i}man et al. \ (2023): \ GPT-4 names the cause in known cause--effect pairs "
                                    r"far above chance, \ from knowledge, \ not data", OK),
            (r"formal inference", r"Corr2Cause \ (Jin et al., \ 2024): \ inferring causal structure from stated "
                                  r"correlations: \ models near chance", BAD),
            (r"the ladder", r"CLadder \ (Jin et al., \ 2023): \ questions on all three rungs; \ accuracy falls as "
                            r"the rungs rise", CAUSE),
            (r"causal parrots", r"Ze\v{c}evi\'{c} et al. \ (2023): \ a model can repeat causal facts it read without "
                                r"having a causal model", EFFECT),
            (r"the open question", r"can rung-1 training on text about rung-2 facts produce rung-2 competence? \ "
                                   r"tools and experiments may help: \ Parts 30 and 42", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.42, width=8.8, x_text=-2.8)
        with self.voiceover(
            "Do large language models reason causally? The evidence is mixed. <bookmark mark='a'/>Emre Kıcıman and "
            "colleagues found GPT-4 far above chance at naming the cause in well-known cause and effect pairs, "
            "drawing on what it had read rather than on any data. <bookmark mark='b'/>But on Corr2Cause, a "
            "benchmark that asks for causal conclusions from stated correlations, the kind of inference the PC "
            "algorithm makes, models of the time performed close to chance. <bookmark mark='c'/>CLadder poses "
            "questions on all three rungs of Pearl's ladder, and accuracy falls as the rungs rise. "
            "<bookmark mark='d'/>Matej Zečević and colleagues called such systems causal parrots: they can repeat "
            "causal facts without having a causal model. <bookmark mark='e'/>The open question is philosophical. "
            "Can training on text, which is rung-one data about rung-two facts, produce rung-two competence? Models "
            "that can use tools and run experiments may change the answer. Parts thirty and forty-two return to it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
