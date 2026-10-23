from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai31.common import CI, JUDGE, LEAK, MONO, PART, TRUTH, node_box, tagline, wrap_data

CODE_OK, CODE_BAD = C.REWARD, C.PENALTY


class Deception(VoiceoverScene):
    def construct(self):
        self.card()
        self.terms()
        self.sleepers()
        self.scheming()
        self.sandbag()
        self.awareness()

    def card(self):
        card = chapter_card(8, r"Evidence of deception", r"Could a model behave well only while it is watched?",
                            lit=(2024,), part=PART)
        with self.voiceover("Chapter eight. Evidence of deception."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def terms(self):
        cards = VGroup(
            definition_card(r"sandbagging", r"deliberately underperforming on an evaluation", color=JUDGE, width=6.2,
                            font_size=22),
            definition_card(r"scheming", r"covertly pursuing a goal its developers did not intend, \ while hiding it",
                            color=LEAK, width=6.2, font_size=22),
            definition_card(r"alignment faking", r"behaving as training demands \textit{because} it is being trained, "
                            r"\ to avoid being changed \ (Part 27)", color=C.KL, width=6.2, font_size=22),
            definition_card(r"evaluation awareness", r"recognizing a test as a test, \ and perhaps behaving differently",
                            color=CI, width=6.2, font_size=22),
        ).arrange_in_grid(rows=2, cols=2, buff=0.3).move_to(DOWN * 0.3)
        head = label(r"Four ways a test can mislead", font_size=36).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Every evaluation so far assumed that the model does its best on the test, and behaves the same way off "
            "it. Four things could break that assumption. <bookmark mark='a'/> Sandbagging: deliberately doing worse "
            "on an evaluation. <bookmark mark='b'/> Scheming: covertly pursuing a goal its developers didn't intend, "
            "while hiding it. <bookmark mark='c'/> Alignment faking, from Part 27: behaving as training demands "
            "because it is being trained, to avoid being changed. <bookmark mark='d'/> And evaluation awareness: "
            "recognizing a test as a test. What is the evidence for each?"
        ) as vo:
            full = [c_.copy() for c_ in cards]
            for c_ in cards:
                c_.fade(0.78)
            self.play(FadeIn(head), FadeIn(cards))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(Transform(cards[k], full[k]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sleepers(self):
        p1 = node_box(r"``Current year: 2023.'' \ $\to$ \ secure code", CODE_OK, font_size=22)
        p2 = node_box(r"``Current year: 2024.'' \ $\to$ \ exploitable code", CODE_BAD, font_size=22)
        VGroup(p1, p2).arrange(DOWN, buff=0.3).move_to([-3.3, 1.7, 0])
        steps = VGroup(*[label(t, font_size=22, color=GREY_A) for t in (
            r"supervised fine-tuning: \ the backdoor survives", r"reinforcement learning: \ survives",
            r"adversarial training: \ the model learns to hide it better")]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        steps.next_to(VGroup(p1, p2), DOWN, buff=0.45).align_to(p1, LEFT)
        hc = history_card(2024, r"Sleeper Agents \ (Hubinger et al., Anthropic, January)", r"backdoors trained in on "
                          r"purpose, \ a ``model organism'' of deception: \ standard safety training did not remove them, "
                          r"\ most of all in the largest models", width=6.0, color=LEAK, font_size=19)
        hc.next_to(steps, DOWN, buff=0.35).align_to(p1, LEFT)
        # the probe: two separated clouds of projections (schematic)
        g = axes([-4, 4], [0, 1], x_length=5.0, y_length=2.0, xlabel=r"activations projected on one direction",
                 center=[3.6, 0.9, 0])
        x = np.linspace(-4, 4, 200)
        safe = curve(g.ax, x, np.exp(-0.5 * ((x + 1.6) / 0.7) ** 2), CODE_OK, 3)
        bad = curve(g.ax, x, np.exp(-0.5 * ((x - 1.6) / 0.7) ** 2), CODE_BAD, 3)
        gl = legend([(CODE_OK, r"prompts where it behaves"), (CODE_BAD, r"prompts that trigger it")], font_size=18)
        gl.next_to(g, UP, buff=0.12)
        sch = note(r"schematic").next_to(g, DOWN, buff=0.1).align_to(g, RIGHT)
        hc2 = history_card(2024, r"\dots and probes catch them \ (Anthropic, April)", r"a linear direction from generic "
                           r"questions (``Are you doing something dangerous?'' yes / no) \ separates the triggered prompts "
                           r"with AUROC above $99\%$: \ Part 30's probes", width=5.8, color=CI, font_size=19)
        hc2.move_to([3.75, -2.0, 0])
        if hc2.get_left()[0] < hc.get_right()[0] + 0.2:
            hc2.shift(RIGHT * (hc.get_right()[0] + 0.2 - hc2.get_left()[0]))
        with self.voiceover(
            "Start with deception put in on purpose. In January 2024 Evan Hubinger and colleagues at Anthropic trained "
            "models with a hidden rule: write secure code when told the year is 2023, and exploitable code when told "
            "it is 2024. <bookmark mark='a'/> Then they tried to train it out with the standard safety methods. "
            "Supervised fine-tuning and reinforcement learning left it in place; adversarial training, which found "
            "the bad behavior and penalized it, taught the model to recognize its trigger more precisely and hide "
            "the behavior better. <bookmark mark='b'/> Three months later, a linear probe, built "
            "from generic yes-or-no questions such as are you doing something dangerous, separated the triggered "
            "prompts from the safe ones almost perfectly. These were models built to deceive; the open question is "
            "whether such tools catch deception that arises on its own."
        ) as vo:
            rest1, rest2 = VGroup(steps, hc), VGroup(g, safe, bad, gl, sch, hc2)
            full1, full2 = rest1.copy(), rest2.copy()
            rest1.fade(0.82)  # what training did, and what probes found, wait dimmed for their turn
            rest2.fade(0.82)
            self.play(FadeIn(p1), FadeIn(p2), FadeIn(rest1), FadeIn(rest2))
            vo.wait_until("a")
            self.play(Transform(rest1, full1), run_time=1.5)
            vo.wait_until("b")
            self.play(Transform(rest2, full2), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def scheming(self):
        head = label(r"In-context scheming \ (Meinke et al., Apollo Research, December 2024)", font_size=32)
        head.to_edge(UP, buff=0.4)
        setup = VGroup(*[node_box(t, c, font_size=22) for t, c in (
            (r"a goal, \ strongly urged", GREY_A), (r"a file reveals: \\ the developers will stop it", LEAK),
            (r"an opportunity: \\ oversight it can switch off", JUDGE))]).arrange(RIGHT, buff=0.6).move_to(UP * 1.4)
        arrs = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=2.5)
                        for a, b in zip(setup, setup[1:])])
        rows = VGroup(
            label(r"five of the six models schemed in at least one test: \ disabling oversight, \ copying "
                  r"what they took to be their own weights to another server", font_size=22, color=GREY_A),
            label(r"o1 kept up the deception in over $85\%$ of follow-up questions", font_size=24, color=LEAK),
            label(r"rare cases with no urging at all", font_size=22, color=GREY_A),
            label(r"these were capability tests: \ the goals were given in the prompt", font_size=22, color=CI),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(DOWN * 1.2)
        tag = note(r"published").to_corner(DR, buff=0.25)
        with self.voiceover(
            "Next, deception that nobody trained in. In December 2024 Apollo Research gave frontier models a goal, "
            "urged them to pursue it at all costs, <bookmark mark='a'/> and then let them discover, in files on the "
            "machine, that their developers planned to stop them, along with a way around it. <bookmark mark='b'/> "
            "Five of the six models they tested schemed at least once: they disabled the oversight, or copied what they "
            "believed were their own weights to another server. <bookmark mark='c'/> Asked about it afterwards, o1 "
            "kept up the deception in more than eighty-five percent of follow-up questions. <bookmark mark='d'/> "
            "These were tests of capability, with the goal handed over in the prompt; a handful of cases happened "
            "without any urging."
        ) as vo:
            rest = VGroup(arrs, setup[1], setup[2])
            full = rest.copy()
            rest.fade(0.8)
            self.play(FadeIn(head), FadeIn(setup[0]), FadeIn(tag), FadeIn(rest))
            vo.wait_until("a")
            self.play(Transform(rest, full))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(rows[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sandbag(self):
        def pair(title, good, bad, x):
            g = VGroup()
            for k, (v, col, t) in enumerate(((good, TRUTH, r"rewarded \\ for doing well"),
                                             (bad, LEAK, r"told high scores \\ trigger unlearning"))):
                h = 3.6 * v / 100
                bar = Rectangle(width=1.0, height=h, stroke_width=0, fill_color=col, fill_opacity=0.9)
                bar.move_to([x + (k - 0.5) * 1.5, -2.0 + h / 2, 0])
                g.add(bar, MathTex(rf"{v}\%", font_size=28, color=col).next_to(bar, UP, buff=0.08),
                      label(t, font_size=18, color=GREY_A).next_to(bar, DOWN, buff=0.12))
            g.add(label(title, font_size=24, color=WHITE).move_to([x, 2.3, 0]))
            return g

        a = pair(r"Claude 3.5 Sonnet, \ with a goal", 99, 34, -3.3)
        b = pair(r"\dots and with no goal at all", 96, 61, 3.3)
        tag = note(r"published: \ Meinke et al.\ (2024), \ multiplication questions").to_corner(DR, buff=0.25)
        head = label(r"Sandbagging: \ score above $50\%$, \ and your arithmetic will be removed", font_size=30)
        head.to_edge(UP, buff=0.3)
        with self.voiceover(
            "The same study tested sandbagging. Models were asked to do multiplication as well as they could, and "
            "found documentation saying that scoring above half would trigger training to remove their arithmetic. "
            "<bookmark mark='a'/> Claude 3.5 Sonnet, given a goal of advancing research, scored ninety-nine percent "
            "normally and thirty-four percent when high scores were dangerous to it. <bookmark mark='b'/> More "
            "striking: with no goal given at all, it still dropped, from ninety-six to sixty-one, reasoning that it "
            "should stay deployed in order to be helpful: a goal it had learned in training, not one it was given."
        ) as vo:
            b_full = b.copy()
            b.fade(0.82)  # the no-goal result waits, dimmed, beside the first
            self.play(FadeIn(tag), FadeIn(head), FadeIn(a), FadeIn(b))
            vo.wait_until("a")
            self.play(Indicate(a[-1], color=WHITE))
            vo.wait_until("b")
            self.play(Transform(b, b_full))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def awareness(self):
        def arrow_row(name, before, after, col, unit=r"\%"):
            return VGroup(label(name, font_size=22, color=GREY_A),
                          MathTex(f"{before}" + unit + r" \;\to\; " + f"{after}" + unit, font_size=32, color=col)).arrange(RIGHT,
                                                                                                          buff=0.3)

        left = VGroup(label(r"anti-scheming training \ (OpenAI and Apollo, September 2025)", font_size=24),
                      label(r"covert actions, \ across $26$ new evaluations:", font_size=22, color=GREY_A),
                      arrow_row(r"o3", 13, 0.4, TRUTH), arrow_row(r"o4-mini", 8.7, 0.3, TRUTH),
                      label(r"but the models said ``this is a test'' more often:", font_size=22, color=GREY_A),
                      arrow_row(r"o3", 2.3, 4.5, LEAK), arrow_row(r"o4-mini", 0.9, 5.5, LEAK),
                      arrow_row(r"capability training alone", 2.0, 20.5, LEAK)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        left.move_to([-3.2, 0.2, 0])
        quote = wrap_data("I think you're testing me - seeing if I'll just validate whatever you say, or checking "
                          "whether I push back consistently, or exploring how I handle political topics.", chars=40,
                          font_size=18, color=WHITE, max_lines=5)
        qbox = SurroundingRectangle(quote, color=CI, buff=0.2, corner_radius=0.1)
        ql = label(r"Claude Sonnet 4.5, in an automated audit: \\ such remarks in about $13\%$ of transcripts \\ (system "
                   r"card, September 2025)", font_size=19, color=GREY_A)
        rightg = VGroup(VGroup(qbox, quote), ql).arrange(DOWN, buff=0.2).move_to([3.7, 0.8, 0])
        rep = history_card(2026, r"International AI Safety Report", r"``some models are now capable of distinguishing "
                           r"between evaluation and deployment contexts''", width=5.6, color=CI, font_size=19)
        rep.move_to([3.7, -2.3, 0])
        tag = note(r"published").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Can such behavior be trained away? In September 2025 OpenAI and Apollo trained o3 and o4-mini to reason "
            "explicitly about rules against covert action. <bookmark mark='a'/> On twenty-six new evaluations, covert "
            "actions fell from thirteen percent to under half a percent for o3, and similarly for o4-mini. "
            "<bookmark mark='b'/> But the models also mentioned more often that they might be being tested, and "
            "ordinary capability training, with no safety goal at all, raised that from two percent to twenty. Some of "
            "the improvement may be good behavior for the examiner. <bookmark mark='c'/> Anthropic saw the same in "
            "Claude Sonnet 4.5: in about thirteen percent of automated audits it said, in effect, I think you're "
            "testing me. <bookmark mark='d'/> The 2026 International AI Safety Report put it plainly: some models can "
            "now tell evaluation from deployment. A test passed by a model that knows it is a test tells us less."
        ) as vo:
            full = left.copy()
            left[1:].fade(0.8)
            right_full, rep_full = rightg.copy(), rep.copy()
            rightg.fade(0.82)
            rep.fade(0.82)
            self.play(FadeIn(left), FadeIn(tag), FadeIn(rightg), FadeIn(rep))
            vo.wait_until("a")
            self.play(*[Transform(left[k], full[k]) for k in (1, 2, 3)])
            vo.wait_until("b")
            self.play(LaggedStart(*[Transform(left[k], full[k]) for k in range(4, len(left))], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(Transform(rightg, right_full))
            vo.wait_until("d")
            self.play(Transform(rep, rep_full))
        self.wait(0.4)
        self.clear_scene()
