from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai27.common import ASSIST, BASE, GOLD, KLC, PART, POLICY, REF, load, node_box, ticks


class Distill(VoiceoverScene):
    def construct(self):
        self.card()
        self.soft()
        self.directions()
        self.ours()
        self.reasoning()

    def card(self):
        card = chapter_card(10, r"Distillation", r"Can a small model learn from a large one's probabilities?",
                            lit=(2015,), part=PART)
        with self.voiceover("Chapter ten. Distillation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def soft(self):
        labels = [r"2", r"3", r"7", r"8", r"5"]
        hard = np.array([1, 0, 0, 0, 0], float)
        soft = np.array([0.80, 0.12, 0.05, 0.02, 0.01])
        mk = lambda vals, col, x: VGroup(*[Rectangle(width=0.5, height=max(2.6 * v, 0.02), stroke_width=0,
                                                     fill_color=col, fill_opacity=0.9)
                                         .move_to([x + 0.7 * i, -1.2, 0], aligned_edge=DOWN)
                                         for i, v in enumerate(vals)])
        hb, sb = mk(hard, BASE, -5.6), mk(soft, REF, 0.8)
        hl = VGroup(*[MathTex(t, font_size=26).next_to(b, DOWN, buff=0.1).set_y(-1.45) for t, b in zip(labels, hb)])
        sl = VGroup(*[MathTex(t, font_size=26).next_to(b, DOWN, buff=0.1).set_y(-1.45) for t, b in zip(labels, sb)])
        ht = label(r"the label: \ ``2''", font_size=26, color=BASE).next_to(hb, UP, buff=0.3).set_y(1.8)
        st = label(r"the teacher's probabilities", font_size=26, color=REF).next_to(sb, UP, buff=0.3).set_y(1.8)
        dark = label(r"this 2 looks a little like a 3: \ ``dark knowledge''", font_size=24, color=GOLD)
        dark.to_edge(DOWN, buff=0.9)
        loss = MathTex(r"\mathcal L = T^2\, \mathrm{KL}\big(\mathrm{softmax}(z_{\mathrm{teacher}}/T)\ \|\ "
                       r"\mathrm{softmax}(z_{\mathrm{student}}/T)\big)", font_size=32).to_edge(UP, buff=0.4)
        tag = note(r"illustrative").to_corner(DR, buff=0.25)
        hc = note(r"Hinton, Vinyals \& Dean, \textit{Distilling the knowledge in a neural network} (2015)")
        hc.to_corner(DL, buff=0.25)
        # the teacher and the student, side by side, until the teacher's probabilities take their place (schematic)
        teach = node_box(r"teacher: \ large, \ slow, \ strong", REF, font_size=26, height=0.9)
        stud = node_box(r"student: \ small, \ fast", ASSIST, font_size=26, height=0.9)
        pair = VGroup(teach, stud).arrange(DOWN, buff=1.1).move_to([3.2, 0.3, 0])
        imit = Arrow(teach.get_bottom(), stud.get_top(), buff=0.1, color=GREY_B, stroke_width=3)
        imit_l = label(r"imitate", font_size=22, color=GREY_A).next_to(imit, RIGHT, buff=0.15)
        with self.voiceover(
            "A large model is expensive to run; a small one is cheap but weaker. Distillation trains the small one, "
            "the student, to imitate the large one, the teacher. <bookmark mark='a'/> Trained on the data alone, the "
            "student sees one right answer per example: this digit is a two. <bookmark mark='b'/> The teacher "
            "offers more: a whole distribution, in which this two is a little like a three and hardly like a five. "
            "Geoffrey Hinton called that information dark knowledge. <bookmark mark='c'/> The student is trained to "
            "match the teacher's probabilities, softened by a temperature T so that the small ones count, with the "
            "KL divergence of Part 1."
        ) as vo:
            self.play(FadeIn(teach), FadeIn(tag), FadeIn(hc))
            self.play(GrowArrow(imit), FadeIn(imit_l), FadeIn(stud))
            vo.wait_until("a")
            self.play(FadeIn(hb), FadeIn(hl), FadeIn(ht))
            vo.wait_until("b")
            self.play(FadeOut(VGroup(teach, stud, imit, imit_l)))
            self.play(FadeIn(sb), FadeIn(sl), FadeIn(st))
            self.play(FadeIn(dark))
            vo.wait_until("c")
            self.play(Write(loss))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def directions(self):
        from videos.ai.ai1.compute import load as load1

        k = load1("kl")
        x, p = np.asarray(k["x"]), np.asarray(k["p"])
        fm, fs = float(k["mean"]), float(k["sd"])  # the forward-KL fit matches the moments
        rm, rs = float(k["rev_a"][-1][0]), float(k["rev_a"][-1][1])  # trajectory rows: mean, sd, KL
        g = axes([float(x[0]), float(x[-1])], [0, float(p.max()) * 1.6], x_length=6.0, y_length=3.0, xticks=[],
                 yticks=[], center=[-3.2, -0.6, 0])
        gauss = lambda m, s: np.exp(-0.5 * ((x - m) / s) ** 2) / (s * np.sqrt(2 * np.pi))
        cp = VMobject().set_points_smoothly([g.ax.c2p(a, b) for a, b in zip(x, p)]).set_stroke(REF, 4)
        cf = VMobject().set_points_smoothly([g.ax.c2p(a, b) for a, b in zip(x, gauss(fm, fs))]).set_stroke(ASSIST, 4)
        cr = VMobject().set_points_smoothly([g.ax.c2p(a, b) for a, b in zip(x, gauss(rm, rs))]).set_stroke(POLICY, 4)
        lg = legend([(REF, r"teacher $p$"), (ASSIST, r"student, \ forward KL$(p \,\|\, q)$"),
                     (POLICY, r"student, \ reverse KL$(q \,\|\, p)$")], font_size=20).next_to(g, UP, buff=0.2)
        rows = VGroup(
            label(r"forward: \ covers everything the teacher might say", font_size=24, color=ASSIST),
            label(r"\ \ classic distillation, \ on the teacher's text", font_size=22, color=GREY_A),
            label(r"reverse: \ commits to what the teacher would say", font_size=24, color=POLICY),
            label(r"\ \ on the student's own text: \ MiniLLM, \ GKD", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.4, 0.0, 0])
        tag = note(r"the two-peaked fit of Part 1").to_corner(DR, buff=0.25)
        with self.voiceover(
            "The direction of the KL matters, as Part 1 showed with this two-peaked distribution. "
            "<bookmark mark='a'/> Minimize the forward KL, from teacher to student, and a student too small to fit "
            "both peaks spreads over both, putting probability where the teacher puts almost none. That's classic "
            "distillation, on text the teacher wrote. <bookmark mark='b'/> Minimize the reverse KL and the student "
            "commits to one peak: it only says things the teacher would say. Methods like MiniLLM and on-policy "
            "distillation train this way, on the student's own text, scored by the teacher, the same on-policy "
            "idea as reinforcement learning."
        ) as vo:
            self.play(FadeIn(g), Create(cp), FadeIn(lg[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(cf), FadeIn(lg[1]), FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(Create(cr), FadeIn(lg[2]), FadeIn(rows[2]), FadeIn(rows[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ours(self):
        d = load("distill")
        ct, cd = np.asarray(d["text"]["curve"]), np.asarray(d["teacher"]["curve"])
        T = float(ct[-1, 0])
        lo = min(float(ct[:, 1].min()), float(cd[:, 1].min()), d["teacher_heldout"])
        hi = max(float(ct[:, 1].max()), float(cd[:, 1].max()))
        g = axes([0, T], [np.floor(lo * 4) / 4, np.ceil(hi * 4) / 4], x_length=7.0, y_length=3.8,
                 xlabel=r"tokens the student has trained on", ylabel=r"loss on held-out novel text (nats)",
                 xticks=[0, T], xfmt=lambda v: rf"{v / 1e6:.0f}\text{{M}}" if v else "0",
                 yticks=ticks(np.floor(lo * 4) / 4, np.ceil(hi * 4) / 4, 3), center=[-1.2, -0.3, 0])
        lt = VMobject().set_points_as_corners([g.ax.c2p(a, b) for a, b in ct]).set_stroke(BASE, 4)
        ld = VMobject().set_points_as_corners([g.ax.c2p(a, b) for a, b in cd]).set_stroke(ASSIST, 4)
        tl = DashedLine(g.ax.c2p(0, d["teacher_heldout"]), g.ax.c2p(T, d["teacher_heldout"]), color=GOLD,
                        dash_length=0.08)
        tll = label(rf"the teacher: \ ${d['teacher_heldout']:.2f}$", font_size=20, color=GOLD).next_to(tl, UP, buff=0.05)
        tll.align_to(tl, RIGHT)
        lg = legend([(BASE, r"student, \ from the text"), (ASSIST, r"student, \ from the teacher")], font_size=20)
        lg.next_to(g, RIGHT, buff=0.3).shift(UP * 0.8)
        tag = note(rf"computed: \ teacher ${d['teacher_params'] / 1e6:.1f}$M parameters, \ students "
                   rf"${d['student_params'] / 1e6:.1f}$M").to_corner(DR, buff=0.2)
        # who teaches whom, beside the chart while the runs are described
        tbox = node_box(rf"teacher: \ six layers, \ ${d['teacher_params'] / 1e6:.1f}$M", REF, font_size=22)
        sbox = node_box(rf"student: \ two layers, \ ${d['student_params'] / 1e6:.1f}$M", ASSIST, font_size=22)
        pair = VGroup(tbox, sbox).arrange(DOWN, buff=0.6).move_to([4.75, -1.3, 0])
        parr = Arrow(tbox.get_bottom(), sbox.get_top(), buff=0.08, color=GREY_B, stroke_width=2.5,
                     max_tip_length_to_length_ratio=0.25)
        a, b = d["text"]["heldout"], d["teacher"]["heldout"]
        verdict = (f"Trained on the teacher's probabilities, the student ends at {b:.2f} nats, against {a:.2f} from "
                   "the text alone, on the same tokens: the teacher's distributions carry more per token than the "
                   "one word that actually came next." if b < a - 0.005 else
                   f"Here the two students end close together, {b:.2f} and {a:.2f} nats: with this little training "
                   "the student's size, not its teacher, is the limit.")
        with self.voiceover(
            "Our version: the novels model, six point eight million parameters, teaches a student with a fifth as "
            "many, two layers instead of six. Two students see the same text. <bookmark mark='a'/> One learns from "
            "the text alone, the next word. <bookmark mark='b'/> The other learns the teacher's whole distribution "
            "over the next word. <bookmark mark='c'/> " + verdict
        ) as vo:
            self.play(FadeIn(tbox), GrowArrow(parr), FadeIn(sbox))
            self.play(FadeIn(g), Create(tl), FadeIn(tll), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lt), FadeIn(lg[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(ld), FadeIn(lg[1]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reasoning(self):
        cards = VGroup(
            history_card(2019, r"DistilBERT \ (Sanh et al., Hugging Face)", r"$40\%$ smaller, \ $60\%$ faster, \ "
                         r"$97\%$ of BERT's language understanding", width=6.2, color=REF),
            history_card(2016, r"sequence-level distillation \ (Kim \& Rush)", r"train the student on whole outputs "
                         r"the teacher writes: \ fine-tuning on a stronger model's answers", width=6.2, color=REF),
            history_card(2025, r"DeepSeek-R1, \ distilled", r"$800$k answers from R1 fine-tuned small open models into "
                         r"reasoners", width=6.2, color=POLICY),
            history_card(2024, r"the small model's recipe", r"most small open models are now trained in part on a "
                         r"larger model's outputs or probabilities", width=6.2, color=GOLD),
        ).arrange_in_grid(rows=2, cols=2, buff=0.35).move_to(UP * 0.1)
        cite_ = cite(r"Sanh et al.\ (2019); \ Kim \& Rush (2016); \ DeepSeek-AI (2025)")
        with self.voiceover(
            "Distillation is everywhere. <bookmark mark='a'/> In 2019 DistilBERT kept ninety-seven percent of BERT's "
            "language understanding with forty percent fewer parameters. <bookmark mark='b'/> For language models the "
            "common form is sequence-level: fine-tune the student on whole answers written by the teacher. Alpaca, "
            "in chapter two, was that. <bookmark mark='c'/> DeepSeek fine-tuned small open models on eight hundred "
            "thousand of R1's answers and turned them into capable reasoners, more cheaply than reinforcement "
            "learning on the small models themselves. <bookmark mark='d'/> Most small models released today are "
            "trained in part on a larger model's outputs or probabilities."
        ) as vo:
            self.play(FadeIn(cite_))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()
