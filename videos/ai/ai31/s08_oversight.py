from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai31.common import CEIL, CI, JUDGE, PART, STRONG, WEAK, band, curve, load, node_box, tagline


class Oversight(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.debate()
        self.debate_results()
        self.w2s_def()
        self.ours()
        self.copies()

    def card(self):
        card = chapter_card(7, r"Supervising something stronger", r"How do you check work you cannot do yourself?",
                            lit=(2018, 2023), part=PART)
        with self.voiceover("Chapter seven. Supervising something stronger."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def problem(self):
        small = Circle(radius=0.45, stroke_color=JUDGE, stroke_width=3, fill_color=JUDGE, fill_opacity=0.15)
        big = Circle(radius=1.4, stroke_color=STRONG, stroke_width=3, fill_color=STRONG, fill_opacity=0.12)
        small.move_to([-4.0, 0.4, 0])
        big.move_to([2.8, 0.4, 0])
        sl = label(r"the supervisor", font_size=24, color=JUDGE).next_to(small, DOWN, buff=0.2)
        bl = label(r"the model", font_size=24, color=STRONG).next_to(big, DOWN, buff=0.2)
        arr = Arrow(small.get_right(), big.get_left(), buff=0.2, color=GREY_B, stroke_width=4)
        al = label(r"rewards, \ labels, \ verdicts", font_size=22, color=GREY_A).next_to(arr, UP, buff=0.1)
        sch = note(r"schematic").to_corner(DR, buff=0.25)
        ideas = VGroup(label(r"debate", font_size=26, color=JUDGE), label(r"amplification", font_size=26, color=GREY_A),
                       label(r"weak-to-strong generalization", font_size=26, color=STRONG)).arrange(RIGHT, buff=0.8)
        ideas.to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Every method of Part 27 needs someone who can tell good work from bad. <bookmark mark='a'/> What happens when the model is better at the "
            "task than its supervisor? Ask a future model for a million lines of code, and no person can check them "
            "all. <bookmark mark='b'/> This is scalable oversight, and there are a few ideas: let two models argue "
            "while the weak supervisor judges; break hard questions into checkable pieces; or study how a strong "
            "model generalizes from a weak supervisor's imperfect labels."
        ) as vo:
            self.play(FadeIn(small), FadeIn(sl), FadeIn(big), FadeIn(bl), FadeIn(sch))
            vo.wait_until("a")
            self.play(GrowArrow(arr), FadeIn(al), big.animate.scale(1.15))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(i_, shift=UP * 0.1) for i_ in ideas], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def debate(self):
        nest = VGroup()
        for k, (r, t, col) in enumerate(((2.9, r"PSPACE: \ a debate", JUDGE), (2.0, r"NP: \ one prover", GREY_A),
                                         (1.1, r"P: \ the judge alone", GREY_B))):
            e = Ellipse(width=2 * r * 1.35, height=2 * r * 0.8, stroke_color=col, stroke_width=2.5, fill_color=col,
                        fill_opacity=0.05)
            lab = label(t, font_size=22, color=col).move_to(e.get_top() + DOWN * 0.3)
            nest.add(VGroup(e, lab))
        for g_ in nest:
            g_.align_to(nest[0], DOWN)
        nest.move_to([-3.3, -0.6, 0])
        thm = theorem_card(r"debate (Irving, Christiano \& Amodei, 2018)", r"two copies of a model argue opposite "
                           r"answers, \ in turns; \ a judge who can check one small step picks the winner. \ With "
                           r"optimal play, \ debate lets a polynomial-time judge answer any question in PSPACE, \ where "
                           r"checking a single answer reaches only NP.", color=JUDGE, width=6.4, font_size=22)
        thm.move_to([3.4, 0.6, 0])
        sch = note(r"schematic").next_to(nest, DOWN, buff=0.12)
        with self.voiceover(
            "The first idea, from Geoffrey Irving, Paul Christiano and Dario Amodei at OpenAI in 2018, is debate. "
            "Two copies of a strong model argue for opposite answers, in turns, and a weak judge picks a winner. "
            "<bookmark mark='a'/> The judge needn't solve the problem; it only has to check the one small step on "
            "which the debaters end up disagreeing. <bookmark mark='b'/> In the language of complexity theory, a "
            "judge alone can decide problems in P; checking one claimed answer reaches NP; with optimal debaters, a "
            "debate reaches all of PSPACE. The bet is that, in a debate, the truth is easier to defend than a lie."
        ) as vo:
            self.play(FadeIn(thm, shift=UP * 0.15))
            vo.wait_until("a")
            self.play(FadeIn(nest[2]))
            vo.wait_until("b")
            self.play(FadeIn(nest[1]))
            self.play(FadeIn(nest[0]), FadeIn(sch))
        self.wait(0.4)
        self.clear_scene()

    def debate_results(self):
        def pair(title, before, after, color, x):
            g = VGroup()
            for k, (v, col, t) in enumerate(((before, GREY_B, r"alone"), (after, color, r"with a debate"))):
                h = 3.2 * v / 100
                bar = Rectangle(width=0.8, height=h, stroke_width=0, fill_color=col, fill_opacity=0.9)
                bar.move_to([x + (k - 0.5) * 1.1, -2.2 + h / 2, 0])
                g.add(bar, MathTex(rf"{v:g}\%", font_size=24, color=col).next_to(bar, UP, buff=0.08),
                      label(t, font_size=18, color=GREY_A).next_to(bar, DOWN, buff=0.1))
            g.add(label(title, font_size=20, color=WHITE).move_to([x, 1.75, 0]))
            return g

        groups = VGroup(pair(r"MNIST, \ judge sees $6$ pixels", 59.4, 88.9, JUDGE, -5.0),
                        pair(r"MNIST, \ judge sees $4$ pixels", 48.2, 85.2, JUDGE, -1.7),
                        pair(r"reading questions, \ human judges", 60, 88, CI, 1.7),
                        pair(r"reading questions, \ model judges", 48, 76, CI, 5.0))
        cite_ = cite(r"Irving, Christiano \& Amodei (2018); \ Khan et al., \textit{Debating with more persuasive LLMs "
                     r"leads to more truthful answers} (2024)")
        head = label(r"Judges who see less, \ helped by a debate", font_size=34).to_edge(UP, buff=0.35)
        tag = note(r"published").to_corner(DR, buff=0.25)
        with self.voiceover(
            "Does it work? <bookmark mark='a'/> The 2018 paper tried a toy: a judge shown only six pixels of a "
            "handwritten digit, chosen by two debaters, rose from fifty-nine percent accuracy to eighty-nine. "
            "<bookmark mark='b'/> In 2024 Akbir Khan and colleagues gave judges reading-comprehension questions "
            "without the text, while two expert models who could read it debated. Human judges went from sixty "
            "percent to eighty-eight, model judges from forty-eight to seventy-six; and the more persuasive the "
            "debaters, the more often the judge found the truth."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(groups[0]), FadeIn(groups[1]))
            vo.wait_until("b")
            self.play(FadeIn(groups[2]), FadeIn(groups[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def w2s_def(self):
        rows = [cmath(r"\text{PGR}", r"=", r"\frac{\text{weak-to-strong} - \text{weak}}{\text{ceiling} - \text{weak}}",
                      font_size=40)]
        rows[0][2].set_color(STRONG)
        whys = [why(r"$0$: \ no better than the supervisor; \ $1$: \ as good as training on the truth")]
        step = ladder(self, rows, whys, keep=1, top=3.0, x=-1.0, buff=0.5, edge=6.9)
        boxes = VGroup(node_box(r"weak supervisor, \\ trained on the truth", WEAK, font_size=22),
                       node_box(r"strong model, \\ trained on the weak labels", STRONG, font_size=22),
                       node_box(r"strong model, \\ trained on the truth: \ the ceiling", CEIL, font_size=22))
        boxes.arrange(RIGHT, buff=0.7).move_to([0, 0.7, 0])
        arrs = VGroup(Arrow(boxes[0].get_right(), boxes[1].get_left(), buff=0.1, color=GREY_B, stroke_width=3))
        al = label(r"its labels", font_size=18, color=GREY_A).next_to(arrs[0], UP, buff=0.05)
        cards = VGroup(
            history_card(2023, r"Burns et al., \ OpenAI", r"GPT-2-level supervisors, \ GPT-4 students: \ about half the "
                         r"gap recovered on NLP tasks; \ near $80\%$ with an auxiliary confidence loss", width=4.3,
                         color=STRONG, font_size=19),
            history_card(2023, r"\dots but not everywhere", r"chess puzzles: \ little recovered across large gaps; "
                         r"\ ChatGPT reward modelling: \ rarely above $20\%$", width=4.3, color=C.PENALTY, font_size=19),
            history_card(2023, r"the confidence loss", r"let the student trust its own confident answers \ over the "
                         r"supervisor's: \ target $= (1 - \alpha)\,$weak $+\ \alpha\,$own", width=4.3, color=CI,
                         font_size=19),
        ).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The third idea turns the problem into an experiment we can run today. In late 2023 Collin Burns and "
            "colleagues at OpenAI used a small model as a stand-in for a weak human supervisor and a large one for "
            "a superhuman model. <bookmark mark='a'/> Train the weak supervisor on the truth; let it label new "
            "examples; train the strong model on its labels; and compare with the strong model trained on the truth, "
            "the ceiling. <bookmark mark='b'/> The performance gap recovered measures how much of the distance from "
            "weak to ceiling the strong student covers. <bookmark mark='c'/> With GPT-4 students and GPT-2-level "
            "supervisors, they recovered about half the gap on language tasks, and near eighty percent with a simple "
            "trick, an extra loss that lets the student trust its own confident answers. On chess puzzles and on "
            "reward modeling, much less."
        ) as vo:
            later = VGroup(arrs, al, boxes[1], boxes[2], cards)
            full = later.copy()
            later.fade(0.8)
            self.play(FadeIn(boxes[0]), FadeIn(later))
            vo.wait_until("a")
            self.play(Transform(later[0], full[0]), Transform(later[1], full[1]), Transform(later[2], full[2]))
            self.play(Transform(later[3], full[3]))
            vo.wait_until("b")
            step(0)
            vo.wait_until("c")
            self.play(LaggedStart(*[Transform(c_, f_) for c_, f_ in zip(cards, full[4])], lag_ratio=0.4), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ours(self):
        d = load("w2s")
        wk = load("weak")
        W, S, SC, CE = (np.asarray(d[k]) * 100 for k in ("weak", "w2s", "w2s_conf", "ceiling"))
        n = len(W)
        top = float(np.ceil(max(CE.max(), S.max(), SC.max()) / 10) * 10 + 10)
        g = axes([0, 4], [0, top], x_length=6.2, y_length=4.0, ylabel=r"right on held-out sentences \ ($\%$)",
                 yticks=[0, 20, 40, 60, 80][: int(top / 20) + 1], center=[-3.0, -0.5, 0])
        names = [(r"weak \\ supervisor", WEAK, W), (r"strong, \\ weak labels", STRONG, S),
                 (r"strong, \ weak labels \\ $+$ confidence", CI, SC), (r"strong, \\ the truth", CEIL, CE)]
        bars, dots, labs, vals = VGroup(), VGroup(), VGroup(), VGroup()
        rng_ = np.random.default_rng(0)
        for k, (t, col, v) in enumerate(names):
            p0, p1 = g.ax.c2p(k + 0.2, 0), g.ax.c2p(k + 0.8, v.mean())
            bars.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.01), stroke_width=0, fill_color=col,
                               fill_opacity=0.75).move_to((p0 + p1) / 2))
            dots.add(VGroup(*[Dot(g.ax.c2p(k + 0.5 + rng_.uniform(-0.18, 0.18), x), radius=0.045, color=WHITE)
                              for x in v]))
            labs.add(label(t, font_size=18, color=col).next_to(g.ax.c2p(k + 0.5, 0), DOWN, buff=0.15))
            vals.add(MathTex(f"{v.mean():.1f}", font_size=22, color=col).next_to(bars[-1], UP, buff=0.08))
        chance = DashedLine(g.ax.c2p(0, 100 * d["chance"]), g.ax.c2p(4, 100 * d["chance"]), color=GREY_C,
                            dash_length=0.06)
        cl = label(rf"chance: \ $1$ in ${d['classes']}$", font_size=18, color=GREY_C).next_to(chance, UP, buff=0.04)
        cl.align_to(chance, RIGHT)
        pgr, pgrc = np.asarray(d["pgr"]), np.asarray(d["pgr_conf"])
        setup = VGroup(
            label(r"Part 27's task: \ which of $30$ novels is this sentence from?", font_size=22, color=GREY_A),
            label(rf"weak: \ $2$ layers, \ ${d['weak_params'] / 1e6:.1f}$M parameters, \ pretrained on the novels",
                  font_size=20, color=WEAK),
            label(rf"strong: \ our ${d['strong_params'] / 1e6:.1f}$M model; \ its last block and a new output layer are "
                  r"trained", font_size=20, color=STRONG),
            label(rf"equal budgets: \ ${d['steps']}$ steps each; \ ${n}$ seeds", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.4, 2.0, 0])
        if setup.width > 7.0:
            setup.width = 7.0
            setup.move_to([3.4, 2.0, 0])
        res = VGroup(
            label(rf"PGR, \ weak labels: \ ${pgr.mean():.2f}$ \ (seeds: \ ${pgr.min():.2f}$ to ${pgr.max():.2f}$)",
                  font_size=24, color=STRONG),
            label(rf"PGR, \ with the confidence loss: \ ${pgrc.mean():.2f}$ \ (${pgrc.min():.2f}$ to ${pgrc.max():.2f}$)",
                  font_size=24, color=CI),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, -1.2, 0])
        tag = tagline(r"computed: \ one dot per seed")
        w, s, c, ce = W.mean(), S.mean(), SC.mean(), CE.mean()
        if s > w + 1:
            gist = (f"The strong student, taught only by the weak supervisor's labels, gets {s:.1f} percent: better "
                    f"than its teacher's {w:.1f}. It recovers {pgr.mean() * 100:.0f} percent of the gap to the ceiling of "
                    f"{ce:.1f}, with seeds ranging from {pgr.min() * 100:.0f} to {pgr.max() * 100:.0f}.")
        else:
            gist = (f"Here the strong student, taught by the weak labels, gets {s:.1f} percent, no better than its "
                    f"teacher's {w:.1f}, though the ceiling is {ce:.1f}: it imitated the supervisor, errors and all.")
        if c > s + 1:
            conf_said = (f"With the confidence loss it reaches {c:.1f}, a gap recovered of {pgrc.mean() * 100:.0f} "
                         "percent.")
        elif c < s - 1:
            conf_said = (f"The confidence loss hurts here: {c:.1f} percent. It lets the student trust its own "
                         "confident guesses over the supervisor's labels, which helps only when those guesses are "
                         "better; here they were not.")
        else:
            conf_said = f"The confidence loss makes little difference here: {c:.1f} percent."
        with self.voiceover(
            "We can run this on the series' own models. The task is Part 27's: which of thirty novels does a sentence "
            f"come from? <bookmark mark='a'/> The weak supervisor is a two-layer model with "
            f"{d['weak_params'] / 1e6:.1f} million parameters, pretrained on the same novels. The strong student is our "
            f"{d['strong_params'] / 1e6:.1f}-million-parameter model; we train its last block and a new output layer. "
            f"Every run gets the same budget, and we repeat everything with {n} seeds. <bookmark mark='b'/> The weak "
            f"supervisor, trained on the truth, gets {w:.1f} percent of held-out sentences right, against chance at "
            f"{100 * d['chance']:.1f}. <bookmark mark='c'/> The ceiling, the strong model trained on the truth: {ce:.1f}. "
            f"<bookmark mark='d'/> {gist} <bookmark mark='e'/> {conf_said}"
        ) as vo:
            self.play(FadeIn(g), Create(chance), FadeIn(cl), FadeIn(tag), FadeIn(labs))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in setup], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(dots[0]), FadeIn(vals[0]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[3], DOWN), FadeIn(dots[3]), FadeIn(vals[3]))
            vo.wait_until("d")
            self.play(GrowFromEdge(bars[1], DOWN), FadeIn(dots[1]), FadeIn(vals[1]), FadeIn(res[0]))
            vo.wait_until("e")
            self.play(GrowFromEdge(bars[2], DOWN), FadeIn(dots[2]), FadeIn(vals[2]), FadeIn(res[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def copies(self):
        d = load("w2s")
        cw, cc, ce = (np.asarray(d[f"curve_{k}"]) for k in ("w2s", "w2s_conf", "ceiling"))
        steps = cw[0, :, 0]
        top = float(np.ceil(max(cw[:, :, 1].max(), cc[:, :, 1].max(), ce[:, :, 1].max()) * 10) / 10 + 0.05)
        g = axes([0, float(steps[-1])], [0, top], x_length=6.0, y_length=3.6, xlabel=r"training steps",
                 ylabel=r"right on held-out sentences", xticks=[0, float(steps[-1])], yticks=[0, round(top / 2, 1)],
                 yfmt=lambda v: rf"{int(round(v * 100))}\%", center=[-3.2, -0.4, 0])
        lines = VGroup()
        for arr, col in ((ce, CEIL), (cw, STRONG), (cc, CI)):
            y = arr[:, :, 1]
            xs = np.r_[0, steps]
            lo = np.r_[d["chance"], y.min(0)]
            hi = np.r_[d["chance"], y.max(0)]
            mid = np.r_[d["chance"], y.mean(0)]
            lines.add(VGroup(band(g.ax, xs, lo, hi, col), curve(g.ax, xs, mid, col, 3)))
        weak = DashedLine(g.ax.c2p(0, float(np.mean(d["weak"]))), g.ax.c2p(float(steps[-1]), float(np.mean(d["weak"]))),
                          color=WEAK, dash_length=0.08)
        lg = legend([(CEIL, r"the truth"), (STRONG, r"weak labels"), (CI, r"weak labels $+$ confidence"),
                     (WEAK, r"the weak supervisor")], font_size=18).next_to(g.ax, UP, buff=0.1).align_to(g.ax, LEFT)
        aw, ac = np.asarray(d["agree_wrong"]) * 100, np.asarray(d["agree_wrong_conf"]) * 100
        stat = VGroup(
            label(r"where the weak supervisor was wrong, \\ the student gave the same wrong title:", font_size=22,
                  color=GREY_A),
            label(rf"weak labels: \ ${aw.mean():.0f}\%$ \ of those sentences", font_size=24, color=STRONG),
            label(rf"with the confidence loss: \ ${ac.mean():.0f}\%$", font_size=24, color=CI),
            label(rf"(a random wrong title: \ $1$ in ${d['classes'] - 1}$)", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.6, 0.0, 0])
        n = len(d["weak"])
        tag = tagline(rf"computed: \ mean of ${n}$ seeds, \ band: \ min to max")
        rand = 100 / (d["classes"] - 1)
        if aw.mean() > 3 * rand:
            copy_said = (f"{aw.mean():.0f} percent of the time, where a random wrong guess would match one time in "
                         f"{d['classes'] - 1}. The student inherits its supervisor's mistakes. That is the open problem "
                         "in miniature: a strong model trained to agree with a weak judge learns, in part, to make the "
                         "judge's mistakes.")
        else:
            copy_said = (f"Only {aw.mean():.0f} percent of the time, close to the one in {d['classes'] - 1} of a random "
                         "wrong guess: here the student did not inherit its supervisor's mistakes.")
        with self.voiceover(
            f"Here is the training, test accuracy as each strong run learns, averaged over the {n} seeds. "
            "<bookmark mark='a'/> Now look only at the held-out sentences that the weak supervisor got wrong. How "
            "often does the student give the same wrong answer? <bookmark mark='b'/> " + copy_said
        ) as vo:
            self.play(FadeIn(g), FadeIn(lg), Create(weak), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(l_) for l_ in lines], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(stat[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in stat[1:]], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()
