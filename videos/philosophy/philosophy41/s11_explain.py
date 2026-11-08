from __future__ import annotations

from videos.philosophy.philosophy41.common import *  # noqa: F403


class Explain(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Explanations", r"What do we owe someone a machine has judged?", lit=(2017,), part=PART)
        with self.voiceover("Chapter ten. Explanations."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.shap()
        self.recourse()
        self.right()
        self.limits()
        self.inside()

    def right(self):
        head = label(r"A right to explanation?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"GDPR \ (2018)", r"Article 22 limits solely automated decisions; \ Recital 71 mentions `an explanation'", PRIV),
                (r"the debate", r"Wachter, \ Mittelstadt and Floridi \ (2017): \ the regulation grants a right to be informed, \ not to an explanation of each decision", EXPL),
                (r"EU AI Act \ (2024)", r"high-risk systems: \ transparency, \ human oversight, \ and a right to an explanation of individual decisions", FAIRC),
                (r"the purpose", r"to contest a decision, \ to know what to change, \ and to trust the system", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Do people have a right to an explanation? <bookmark mark='a'/>Europe's General Data Protection "
            "Regulation, in force since 2018, limits decisions made solely by automated means, and its preamble "
            "mentions obtaining an explanation. <bookmark mark='b'/>Sandra Wachter, Brent Mittelstadt and Luciano "
            "Floridi argued in 2017 that the regulation grants a right to be informed, not a right to an explanation "
            "of each decision. <bookmark mark='c'/>The European Union's AI Act, of 2024, requires transparency and "
            "human oversight for high-risk systems, and gives people a right to an explanation of individual "
            "decisions made with them. <bookmark mark='d'/>Explanations serve several purposes: to contest a "
            "decision, to know what to change, and to decide whether to trust the system at all."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def limits(self):
        head = label(r"The limits of explanation", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Rudin \ (2019)", r"`stop explaining black box models for high stakes decisions': \ use interpretable models instead", BAD),
                (r"fooling", r"Slack et al. \ (2020): \ a biased model can be dressed so that LIME and SHAP report innocent features", RESP),
                (r"many models", r"the Rashomon effect: \ equally accurate models can rely on different features", EXPL),
                (r"what counts", r"Miller \ (2019): \ people want contrastive explanations, \ why this and not that", FAIRC)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Explanations have limits. <bookmark mark='a'/>Cynthia Rudin argued in 2019 that for high-stakes "
            "decisions we should stop explaining black boxes and use models that are interpretable to begin with. "
            "<bookmark mark='b'/>Dylan Slack and colleagues showed in 2020 that a deliberately biased model can be "
            "disguised so that popular explanation tools report only innocent features. <bookmark mark='c'/>Many "
            "models fit the data equally well while relying on different features, the Rashomon effect, so an "
            "explanation describes one model, not the world. <bookmark mark='d'/>And Tim Miller's review of 2019 "
            "found that people want contrastive explanations: why this outcome rather than that one."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def shap(self):
        e = load("explain")
        assert e["phi"] == [0.45, 0.2, -0.6] and e["sum_ok"] and not e["accepted"]
        head = label(r"Why was the loan refused?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        f = MathTex(r"f = 0.4\,\text{income} + 0.3\,\text{history} - 0.5\,\text{debt} + 0.2\,\text{income}\times"
                    r"\text{history}", font_size=30).move_to([0, 2.3, 0])
        appl = label(rf"applicant: \ income {e['x'][0]:g}, \ history {e['x'][1]:g}, \ debt {e['x'][2]:g}; \ score "
                     rf"{e['f']:.2f}, \ needs {e['threshold']:.2f}: \ refused", font_size=21, color=RESP).move_to([0, 1.55, 0])
        x0, y0, sc = -2.0, 0.5, 3.0
        bars = VGroup()
        for k, (nm, ph) in enumerate(zip(e["names"], e["phi"])):
            y = y0 - 0.7 * k
            w = abs(ph) * sc
            b = Rectangle(width=w, height=0.42, fill_color=FAIRC if ph > 0 else BAD, fill_opacity=0.75, stroke_width=0)
            b.move_to([x0 + (w / 2 if ph > 0 else -w / 2), y, 0])
            bars.add(VGroup(b, label(nm, font_size=19, color=GREY_A).move_to([x0 - 2.6, y, 0]),
                            label(f"{ph:+.2f}", font_size=19).move_to([0.2, y, 0])))
        zero = Line([x0, y0 + 0.4, 0], [x0, y0 - 1.8, 0], color=GREY_C)
        side = stack([(r"Shapley values: \ average contribution over all orders of adding the features", EXPL),
                      (rf"they add up to the score: \ $0.45 + 0.20 - 0.60 = {e['f'] - e['f0']:.2f}$", FAIRC),
                      (r"Lundberg and Lee \ (2017): \ SHAP, \ the cooperative game of Part 34, \ for predictions",
                       GREY_A)], font_size=19, buff=0.22, aligned_edge=LEFT, width=5.0).move_to([4.0, -0.4, 0])
        cfs = e["counterfactuals"]
        cft = label(r"counterfactuals: \ " + r"; \ ".join(f"{c['feature']} {c['change']:+.1f}" for c in cfs) +
                    r" \ would each have been enough", font_size=20, color=EXPL).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Explanation is the third demand on fair machines. Here is a toy credit model. <bookmark mark='a'/>The "
            "score adds income and credit history, subtracts debt, and adds a bonus when income and history are both "
            "high. An applicant scores point zero five, below the cutoff of point two, and is refused. <bookmark "
            "mark='b'/>Why? Shapley values, the fair division of Part 34 applied to features, average each feature's "
            "contribution over every order in which the features could be added. Income added point four five, "
            "history point two, and debt took away point six. <bookmark mark='c'/>They add up exactly to the score, "
            "which is what makes them attractive; Scott Lundberg and Su-In Lee's SHAP made them standard in 2017. "
            "<bookmark mark='d'/>A counterfactual explanation, in Sandra Wachter, Brent Mittelstadt and Chris "
            "Russell's sense, says instead what would have changed the decision: raising income by point three, or "
            "history by point three, or cutting debt by point three, would each have been enough. Debt was the "
            "largest factor, yet three different smallest changes exist, and the explanation is not unique."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(appl))
            vo.wait_until("b")
            self.play(Create(zero), LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.3), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(cft))
        self.clear_scene()

    def recourse(self):
        head = label(r"From explanation to recourse", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Wachter, \ Mittelstadt and Russell \ (2017)", r"counterfactual explanations: \ the smallest change that would have changed the decision", EXPL),
                (r"Ustun, \ Spangher and Liu \ (2019)", r"`actionable recourse': \ the change must be one the person can make; \ age and history cannot be changed", FAIRC),
                (r"Karimi et al. \ (2021)", r"actions have causal effects: \ raising income may change debt too, \ so recourse needs a causal model \ (Part 17)", PRIV),
                (r"Venkatasubramanian and Alfano \ (2020)", r"recourse as a moral claim: \ to be able to change one's standing by one's own effort", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The counterfactual explanation deserves a closer look, because it is the kind people can use. <bookmark "
            "mark='a'/>Sandra Wachter, Brent Mittelstadt and Chris Russell proposed it in 2017: tell the applicant "
            "the smallest change that would have flipped the decision, without opening the model. <bookmark "
            "mark='b'/>Berk Ustun, Alexander Spangher and Yang Liu pointed out that the smallest change may be "
            "useless. A change in age or in credit history cannot be made. Actionable recourse searches only over "
            "changes the person can actually make. <bookmark mark='c'/>Amir-Hossein Karimi and colleagues added "
            "causality: actions have effects. Taking a second job raises income, but may also change debt and hours, "
            "so recourse needs a causal model of the kind built in Part 17, not just a model of the classifier. "
            "<bookmark mark='d'/>Suresh Venkatasubramanian and Mark Alfano argued that recourse is a moral claim in "
            "its own right: in a world run by models, people should be able to change their standing by their own "
            "effort."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def inside(self):
        head = label(r"Explaining the mechanism", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"circuits", r"Olah et al. \ (2020): \ `Zoom In': \ read features, \ and the circuits that connect them, \ inside a network", EXPL),
                (r"superposition", r"Elhage et al. \ (2022): \ networks represent more features than they have neurons, \ overlapped", PRIV),
                (r"dictionary learning", r"Templeton et al. \ (2024): \ sparse autoencoders found millions of interpretable features in a production language model", FAIRC),
                (r"the hope", r"an explanation of how the model computes, \ not just of which inputs mattered: \ Part 42", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Shapley values and counterfactuals explain a model from outside, by its inputs and outputs. A newer "
            "program tries to explain it from inside. <bookmark mark='a'/>Chris Olah and colleagues proposed reading "
            "a neural network like an organism under a microscope: find the features its neurons detect, and the "
            "circuits that connect them. <bookmark mark='b'/>Nelson Elhage and colleagues found a complication. "
            "Networks represent more features than they have neurons, overlapped in superposition, so single neurons "
            "rarely mean one thing. <bookmark mark='c'/>Adly Templeton and colleagues used sparse autoencoders to "
            "pull the overlapped features apart, and found millions of interpretable ones in a production language "
            "model, from famous people to code errors to deception. <bookmark mark='d'/>The hope is an explanation of "
            "how a model computes its answer, not just which inputs mattered: an explanation that could show a model "
            "was relying on a proxy for the group, or planning to mislead. Part 42 asks whether that is enough to "
            "trust it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
