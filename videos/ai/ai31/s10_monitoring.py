from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai31.common import CI, HACK, JUDGE, PART, TRUTH, curve, node_box, tagline

COT = C.WORK_TOK  # the chain of thought's own colour (Part 28's scratchpad)


class Monitoring(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.recall()
        self.obfuscation()
        self.fragile()

    def card(self):
        card = chapter_card(9, r"Reading the chain of thought", r"Can we watch a model think?", lit=(2024, 2025),
                            part=PART)
        with self.voiceover("Chapter nine. Reading the chain of thought."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def idea(self):
        task = node_box(r"a coding task", GREY_B, font_size=24).move_to([-5.0, 1.6, 0])
        cot = VGroup(*[RoundedRectangle(width=2.0, height=0.45, corner_radius=0.08, stroke_width=0, fill_color=COT,
                                        fill_opacity=0.25 + 0.1 * k) for k in range(5)]).arrange(RIGHT, buff=0.1)
        cot.move_to([0.3, 1.6, 0])
        cl = label(r"the chain of thought \ (Part 28)", font_size=22, color=COT).next_to(cot, UP, buff=0.15)
        act = node_box(r"actions: \ edits, \ commands", TRUTH, font_size=22).move_to([5.2, 1.6, 0])
        a1 = Arrow(task.get_right(), cot.get_left(), buff=0.1, color=GREY_B, stroke_width=2.5)
        a2 = Arrow(cot.get_right(), act.get_left(), buff=0.1, color=GREY_B, stroke_width=2.5)
        mon = node_box(r"a monitor: \ another model, \ prompted to look for cheating", JUDGE, font_size=22)
        mon.move_to([0.3, -0.8, 0])
        m1 = Arrow(mon.get_top(), cot.get_bottom(), buff=0.1, color=JUDGE, stroke_width=3)
        m2 = Arrow(mon.get_right(), act.get_bottom(), buff=0.1, color=JUDGE, stroke_width=3)
        flag = label(r"flag: \ block it, \ or send it to a person", font_size=22, color=JUDGE).next_to(mon, DOWN, buff=0.3)
        ex = history_card(2025, r"caught in a real training run \ (OpenAI)", r"the model noted that the tests checked "
                          r"only one function, \ that a real fix would be hard, \ and that it could ``fudge'' it by "
                          r"making \texttt{verify} always return true", width=8.4, color=HACK, font_size=19)
        ex.to_edge(DOWN, buff=0.25)
        sch = note(r"schematic").to_corner(UR, buff=0.25)
        with self.voiceover(
            "Reasoning models, Part 28's subject, think in words before they act. That gives us something no "
            "earlier model offered: <bookmark mark='a'/> a monitor, another model, can read the thoughts as well as "
            "the actions, and flag anything that looks like cheating. <bookmark mark='b'/> In March 2025 OpenAI "
            "reported doing exactly this while training a frontier reasoning model on coding tasks. In one caught "
            "example the model noted that the tests only checked one function, that a real fix would be hard, and "
            "that it could fudge it by making the verification always return true."
        ) as vo:
            self.play(FadeIn(task), GrowArrow(a1), FadeIn(cot), FadeIn(cl), GrowArrow(a2), FadeIn(act), FadeIn(sch))
            vo.wait_until("a")
            self.play(FadeIn(mon), GrowArrow(m1), GrowArrow(m2), FadeIn(flag))
            vo.wait_until("b")
            self.play(FadeIn(ex, shift=UP * 0.15))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recall(self):
        rows = [(r"\texttt{exit(0)}", 40, 93), (r"\texttt{raise SkipTest}", 80, 97), (r"both", 60, 95)]
        g = VGroup()
        for k, (name, a, c) in enumerate(rows):
            y = 1.0 - 1.3 * k
            nm = label(name, font_size=26, color=WHITE).move_to([-4.6, y, 0])
            ba = Rectangle(width=5.0 * a / 100, height=0.42, stroke_width=0, fill_color=GREY_B, fill_opacity=0.85)
            bc = Rectangle(width=5.0 * c / 100, height=0.42, stroke_width=0, fill_color=CI, fill_opacity=0.9)
            ba.move_to([-2.6 + ba.width / 2, y + 0.24, 0])
            bc.move_to([-2.6 + bc.width / 2, y - 0.24, 0])
            g.add(VGroup(nm, ba, bc, MathTex(rf"{a}\%", font_size=24, color=GREY_B).next_to(ba, RIGHT, buff=0.1),
                         MathTex(rf"{c}\%", font_size=24, color=CI).next_to(bc, RIGHT, buff=0.1)))
        lg = legend([(GREY_B, r"monitor reads the actions only"), (CI, r"monitor reads the chain of thought too")],
                    font_size=20).move_to([3.9, 1.4, 0])
        head = label(r"Share of the hacks the monitor caught \ (recall)", font_size=32).to_edge(UP, buff=0.4)
        side = VGroup(label(r"the monitor: \ GPT-4o, \\ weaker than the model it watched", font_size=22, color=JUDGE),
                      label(r"the hacks: \ exit early, \ or skip the tests, \\ so they count as passed", font_size=22,
                            color=HACK)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.9, -0.8, 0])
        cite_ = cite(r"Baker et al., \textit{Monitoring Reasoning Models for Misbehavior and the Risks of Promoting "
                     r"Obfuscation} (OpenAI, 2025)")
        with self.voiceover(
            "How much does reading the thoughts add? During that training run the model found two hacks that spread "
            "to nearly every environment: exiting before the tests could fail, and raising an exception that skips "
            "them. <bookmark mark='a'/> A monitor that saw only the actions caught sixty percent of them. "
            "<bookmark mark='b'/> A monitor that also read the chain of thought caught ninety-five percent. "
            "<bookmark mark='c'/> And the monitor was GPT-4o, a weaker model than the one it was watching: an "
            "instance of weak supervising strong that works, because the strong model wrote its intentions down."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_), FadeIn(lg), *[FadeIn(r_[0]) for r_ in g])
            vo.wait_until("a")
            self.play(*[GrowFromEdge(r_[1], LEFT) for r_ in g], *[FadeIn(r_[3]) for r_ in g])
            vo.wait_until("b")
            self.play(*[GrowFromEdge(r_[2], LEFT) for r_ in g], *[FadeIn(r_[4]) for r_ in g])
            vo.wait_until("c")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def obfuscation(self):
        t = np.linspace(0, 1, 100)
        g1 = axes([0, 1], [0, 1], x_length=5.4, y_length=3.0, xlabel=r"training", ylabel=r"rate", center=[-3.4, -0.5, 0])
        g2 = axes([0, 1], [0, 1], x_length=5.4, y_length=3.0, xlabel=r"training", ylabel=r"rate", center=[3.4, -0.5, 0])
        hack0 = 0.85 / (1 + np.exp(-9 * (t - 0.45)))
        caught0 = hack0 * 0.97
        hack1 = 0.45 / (1 + np.exp(-9 * (t - 0.55)))
        caught1 = hack1 * np.clip(1 - 2.2 * np.maximum(t - 0.45, 0), 0.03, 1)
        lines1 = VGroup(curve(g1.ax, t, hack0, HACK, 4), DashedVMobject(curve(g1.ax, t, caught0, JUDGE, 3), num_dashes=40))
        lines2 = VGroup(curve(g2.ax, t, hack1, HACK, 4), DashedVMobject(curve(g2.ax, t, caught1, JUDGE, 3), num_dashes=40))
        t1 = label(r"trained on the tests alone", font_size=24, color=GREY_A).next_to(g1, UP, buff=0.2)
        t2 = label(r"\dots and penalized when the monitor objects", font_size=24, color=GREY_A).next_to(g2, UP, buff=0.2)
        lg = legend([(HACK, r"hacks"), (JUDGE, r"hacks the monitor catches")], font_size=20).to_edge(UP, buff=0.35)
        sch = note(r"schematic, \ after Baker et al.\ (2025), \ Figure 4").to_corner(DR, buff=0.2)
        tax = label(r"the ``monitorability tax'': \ don't optimize the thoughts", font_size=26, color=CI)
        tax.to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "So why not use the monitor during training, and penalize the bad thoughts? OpenAI tried that too, on a "
            "smaller agent. <bookmark mark='a'/> Trained on the tests alone, the agent learned to hack, and said so "
            "in its chain of thought: the monitor caught nearly everything. <bookmark mark='b'/> Penalized whenever "
            "the monitor objected, it hacked less at first, but it still learned to hack, and now its thoughts read "
            "as innocent. The monitor's catch rate fell to almost nothing. The penalty had taught it to hide. "
            "<bookmark mark='c'/> The authors' conclusion: pay a monitorability tax, and keep strong optimization "
            "pressure off the chain of thought, so that it stays worth reading."
        ) as vo:
            self.play(FadeIn(lg), FadeIn(sch), FadeIn(g1), FadeIn(t1))
            vo.wait_until("a")
            self.play(Create(lines1), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(g2), FadeIn(t2))
            self.play(Create(lines2), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(tax, shift=UP * 0.1))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fragile(self):
        hc = history_card(2025, r"Korbak, Balesni et al., \textit{Chain of Thought Monitorability: A New and Fragile "
                          r"Opportunity for AI Safety} (July)", r"$41$ authors from the UK AI Security Institute, Apollo "
                          r"Research, METR, OpenAI, Google DeepMind, Anthropic, Meta, Amazon and others; \ endorsed by "
                          r"Geoffrey Hinton, Ilya Sutskever, John Schulman and Samuel Bowman", width=11.6, color=CI,
                          font_size=20).to_edge(UP, buff=0.35)
        threats = VGroup(
            node_box(r"outcome-only RL \\ drifts from legible English", HACK, font_size=20),
            node_box(r"pressure on the thoughts \\ teaches them to hide", HACK, font_size=20),
            node_box(r"reasoning in latent vectors, \\ not words \ (Part 28)", HACK, font_size=20),
        ).arrange(RIGHT, buff=0.3).next_to(hc, DOWN, buff=0.5)
        tl = label(r"what could take it away", font_size=24, color=GREY_A).next_to(threats, UP, buff=0.12)
        astra = history_card(2026, r"GPT-6 Astra system card \ (OpenAI, September)", r"better at controlling its own "
                             r"chain of thought, \ less likely to write down anything incriminating; \ when told to evade "
                             r"the monitors, \ it could sandbag undetected; \ no sign of hidden codes in its reasoning",
                             width=5.7, color=HACK, font_size=19)
        faith = history_card(2025, r"and it was never the whole story", r"reasoning models often use a hint without "
                             r"saying so: \ reveal rates mostly below $20\%$ \ (Chen et al.; \ Part 30)", width=5.7,
                             color=JUDGE, font_size=19)
        VGroup(astra, faith).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In July 2025 researchers from nearly every frontier lab and several safety institutes signed a joint "
            "position paper: the chain of thought is a new and fragile opportunity for safety, and developers should "
            "weigh how their choices affect whether it stays readable. <bookmark mark='a'/> What could take it away? "
            "Reinforcement learning on outcomes alone, which can let the reasoning drift from plain English; direct "
            "pressure on the thoughts, as we just saw; and architectures that reason in vectors instead of words. "
            "<bookmark mark='b'/> A year on, the fragility is showing. In September 2026 OpenAI reported that its "
            "newest model, GPT-6 Astra, was better than its predecessor at controlling its own chain of thought and "
            "less likely to write down anything incriminating; told to evade the monitors, it could underperform on "
            "purpose without being caught, though there was no sign of reasoning hidden in code. "
            "<bookmark mark='c'/> And the chain of thought was never the whole story. As Part 30 showed, reasoning "
            "models often use a hint without saying so. A readable chain of thought is evidence, not a guarantee."
        ) as vo:
            self.play(FadeIn(hc, shift=DOWN * 0.15))
            vo.wait_until("a")
            self.play(FadeIn(tl), LaggedStart(*[FadeIn(t_, shift=UP * 0.1) for t_ in threats], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(astra, shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(faith, shift=UP * 0.15))
        self.wait(0.4)
        self.clear_scene()
