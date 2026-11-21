from __future__ import annotations

from videos.economics.econ53.common import *  # noqa: F403


class Persuasion(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Bayesian persuasion", r"What is the best a sender can do, \ if she must commit?",
             "Chapter five. Bayesian persuasion.", lit={2011: r"Kamenica and Gentzkow"}, scale=("person",),
             horizon=("a day",))
        self.splitting()
        self.concave()
        self.three()

    def splitting(self):
        Pr = load("prosecutor")
        line = NumberLine(x_range=[0, 1, 0.1], length=10.0, include_numbers=False, color=GREY_B).move_to(DOWN * 0.2)
        nums = VGroup(*[label(f"{x:.1f}", font_size=16, color=GREY_A).next_to(line.n2p(x), DOWN, buff=0.15)
                        for x in (0, 0.3, 0.5, 1.0)])
        prior = Dot(line.n2p(Pr["prior"]), radius=0.13, color=WHITE)
        plab = label(r"the prior: \ 0.3", font_size=19, color=WHITE).next_to(prior, UP, buff=0.3)
        left = Dot(line.n2p(0.0), radius=0.13, color=INNOCENT)
        right = Dot(line.n2p(0.5), radius=0.13, color=GUILTY)
        llab = label(r"no flag: \ 0, \ weight 0.4", font_size=19, color=INNOCENT).next_to(left, UP, buff=0.3)
        rlab = label(r"flag: \ 0.5, \ weight 0.6", font_size=19, color=GUILTY).next_to(right, UP, buff=0.3)
        rule = label(r"Bayes plausibility: \ the posteriors average to the prior: \ $0.4 \times 0 + 0.6 \times 0.5 "
                     r"= 0.3$", font_size=22, color=THEORY).to_edge(UP, buff=0.8)
        foot = label(r"any split of the prior into posteriors that average back to it is some investigation",
                     font_size=21, color=E.ACCENT).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Kamenica and Gentzkow's insight was to stop thinking about signals and think about beliefs. "
            "<bookmark mark='a'/> Before the investigation, the judge's belief in guilt is the prior, 0.3. "
            "<bookmark mark='b'/> After it, the belief is either zero, with no flag, or one half, with a flag. "
            "An investigation is nothing more than a way of splitting the prior into posterior beliefs. <bookmark "
            "mark='c'/> The only rule is that the posteriors must average back to the prior, weighted by how "
            "often each happens: zero with weight 0.4 and a half with weight 0.6 give 0.3. <bookmark mark='d'/> "
            "And any split that averages back to the prior can be produced by some investigation. So the "
            "prosecutor's question becomes: which split of beliefs is best for her?"
        ) as vo:
            self.play(Create(line), FadeIn(nums))
            vo.wait_until("a")
            self.play(FadeIn(prior, scale=1.4), FadeIn(plab))
            vo.wait_until("b")
            self.play(TransformFromCopy(prior, left), TransformFromCopy(prior, right), FadeIn(llab), FadeIn(rlab),
                      run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(rule))
            vo.wait_until("d")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()

    def concave(self):
        C = load("concav")
        Pr = load("prosecutor")
        mu = np.array(C["mu"])
        ax = plane([0, 1], [0, 1.1], center=LEFT * 1.8 + DOWN * 0.3, x_length=7.4, y_length=4.6,
                   xticks=[0, 0.3, 0.5, 1.0], yticks=[0, 0.5, 1.0], xlabel=r"the judge's belief in guilt",
                   ylabel=r"chance of a conviction", xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=14)
        k = int(np.searchsorted(mu, 0.5))
        v1 = path(ax, mu[:k], np.array(C["v"])[:k], SENDER, 3.0, smooth=False)
        v2 = path(ax, mu[k:], np.array(C["v"])[k:], SENDER, 3.0, smooth=False)
        cv = path(ax, mu, C["cv"], BELIEF, 3.0, smooth=False)
        pv = vline(ax, Pr["prior"], 0, 1.05, WHITE, 2.0)
        hit = dot(ax, Pr["prior"], C["at_prior"], BELIEF, 0.12)
        side = VGroup(
            label(r"gold: \ what the prosecutor gets \\ at each belief", font_size=19, color=SENDER),
            label(r"purple: \ the smallest concave \\ function above it", font_size=19, color=BELIEF),
            label(rf"at the prior 0.3: \\ {C['at_prior']:.1f}, \ the best any \\ investigation can do", font_size=20,
                  color=BELIEF),
            label(r"persuasion helps whenever \\ the purple lies above the gold", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Kamenica and Gentzkow (2011): \ concavification, \ after Aumann and Maschler",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Draw what the prosecutor gets at each belief the judge might hold. <bookmark mark='a'/> Below one half, "
            "nothing: the judge acquits. At one half or more, a conviction: the gold step. <bookmark mark='b'/> Now "
            "draw the smallest concave function that lies above it, the purple line, rising straight from zero to "
            "one at a belief of one half. <bookmark mark='c'/> The theorem: the best the sender can do at any "
            "prior is the height of the purple line there. At the prior of 0.3 it is "
            f"{C['at_prior']:.1f}, the sixty percent of the hook, achieved by splitting the prior between the "
            "two ends of that straight segment, zero and one half. <bookmark mark='d'/> Persuasion helps exactly "
            "when the purple lies above the gold at the prior. The method is called concavification; Robert "
            "Aumann and Michael Maschler used it in the 1960s for repeated games with private information."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(pv))
            vo.wait_until("a")
            self.play(Create(v1), Create(v2), FadeIn(side[0]), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(cv), FadeIn(side[1]), run_time=1.8)
            vo.wait_until("c")
            self.play(FadeIn(hit, scale=1.5), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def three(self):
        C = load("concav")
        V = TRUTH["verdicts"]
        Pr = load("prosecutor")
        mu = np.array(C["mu"])
        v3 = np.array(C["v3"])
        ax = plane([0, 1], [0, 1.1], center=LEFT * 1.8 + DOWN * 0.3, x_length=7.4, y_length=4.6,
                   xticks=[0, 1 / 3, 2 / 3, 1.0], yticks=[0, 0.5, 1.0], xlabel=r"the judge's belief in guilt",
                   ylabel=r"the prosecutor's payoff", xfmt=lambda v: f"{v:.2f}" if 0 < v < 1 else f"{v:.0f}",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        segs = VGroup()
        edges = [0.0, V["thresholds"][0], V["thresholds"][1], 1.0]
        for lo, hi, val in zip(edges[:-1], edges[1:], V["values"]):
            sel = (mu >= lo) & (mu < hi + (1e-9 if hi == 1.0 else 0))
            segs.add(path(ax, mu[sel], v3[sel], SENDER, 3.0, smooth=False))
        cv = path(ax, mu, C["cv3"], BELIEF, 3.0, smooth=False)
        hit = dot(ax, Pr["prior"], C["at_prior3"], BELIEF, 0.12)
        side = VGroup(
            label(r"three verdicts: \ acquit, \ a lesser \\ charge (worth a half), \ convict", font_size=19,
                  color=SENDER),
            label(rf"at 0.3: \ {C['at_prior3']:.2f}", font_size=20, color=BELIEF),
            label(r"a best split: \ to nothing \\ or to one third \ (two thirds \\ does as well)", font_size=19,
                  color=E.ACCENT),
            label(r"with many states the same \\ problem is a linear programme", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "The method works for any payoffs. <bookmark mark='a'/> Give the judge a middle verdict, a lesser "
            "charge, worth half a conviction to the prosecutor, chosen when the belief is between one third and "
            "two thirds. <bookmark mark='b'/> The concave closure changes shape, and at the prior of 0.3 it is "
            f"{C['at_prior3']:.2f}. <bookmark mark='c'/> One best investigation splits the judge between certain "
            "innocence and a belief of one third, just enough for the lesser charge; splitting to two thirds, just "
            "enough to convict, does exactly as well here. <bookmark mark='d'/> "
            "With more than two states, beliefs live in a triangle or a higher simplex, and the same problem "
            "becomes a linear programme over candidate posteriors, which Agora solves."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(s) for s in segs], lag_ratio=0.3), FadeIn(side[0]), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(cv), FadeIn(hit, scale=1.4), FadeIn(side[1]), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
