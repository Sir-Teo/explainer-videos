from __future__ import annotations

from videos.economics.econ45.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 16, r"Frontier: \ structural behavioural economics, \ behavioural macro",
             r"What is still being worked out?", "Chapter sixteen. Frontier: structural behavioural economics, and "
             "behavioural macroeconomics.", lit={2018: r"DellaVigna", 2020: r"Gabaix", 2021: r"Peterson et al."},
             scale=("person", "world"), horizon=("a decade",))
        self.open()
        self.learned()

    def open(self):
        cards = point_cards([
            (r"structural", r"estimate $\beta$, \ $\lambda$, \\ attention costs \\ from field data, \ then \\ "
                            r"predict new policies", SOPH),
            (r"behavioural macro", r"firms and households \\ that discount the \\ distant future: \ does \\ "
                                   r"forward guidance fade?", PLAN),
            (r"theories from data", r"how much of what \\ is predictable \\ do our theories \\ capture?", GYM),
            (r"robustness", r"which findings \\ replicate, \ at \\ what size, \ for \\ whom?", HOLD),
        ], width=12.8, cols=4, font_size=17).move_to(DOWN * 1.35)
        head = label(r"open questions", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        loops = [
            [(r"a field \\ choice", SOPH), (r"a behavioural \\ model", SOPH), (r"its parameters", SOPH),
             (r"a policy not \\ yet tried", SOPH)],
            [(r"a promise about \\ future rates", PLAN), (r"discounted by \\ limited foresight", PLAN),
             (r"a smaller effect \\ today", PLAN)],
            [(r"thousands of \\ choices", GYM), (r"a flexible \\ learner", GYM), (r"the best \\ achievable fit", GYM),
             (r"how close is \\ the theory?", GYM)],
            [(r"one striking \\ result", HOLD), (r"many labs, \\ registered", HOLD), (r"the size \\ that survives",
                                                                                      HOLD)],
        ]
        chains = [flow_chain(st, box_w=2.6, box_h=0.85, buff=0.45, font_size=17).move_to(UP * 2.05) for st in loops]
        asks = [label(t, font_size=19, color=col).move_to(UP * 1.05) for t, col in (
            (r"the welfare effects of a policy need the parameters, \\ not only the treatment effect", SOPH),
            (r"Part 30's forward-guidance puzzle shrinks \\ if people look less far ahead", PLAN),
            (r"Part 26 of Psychology, Built: \\ prospect theory on 13,000 gamble problems", GYM),
            (r"Part 28 of Psychology, Built: \\ ego depletion did not survive", HOLD))]
        tag = published_tag(tables.FRONTIER45.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Four frontiers. <bookmark mark='a'/> Structural behavioural economics. A treatment effect says what "
            "a nudge did; it does not say whether people are better off, or what a different policy would do. For "
            "that, estimate the parameters, the beta, the lambda, the cost of attention, from field choices, and use "
            "the model to predict. <bookmark mark='a2'/> Stefano DellaVigna has argued that this is how behavioural "
            "findings become tools for policy. <bookmark mark='b'/> Behavioural macroeconomics. In Part thirty, "
            "promises about interest rates far in the future had implausibly large effects today, the "
            "forward-guidance puzzle. <bookmark mark='b2'/> Xavier Gabaix showed that if households and firms "
            "discount the distant future through limited attention, the puzzle shrinks. <bookmark mark='c'/> "
            "Theories learned from data. With thousands of choices, a flexible learner can find the best fit that "
            "is achievable at all, and a theory can be graded by how close it comes. <bookmark mark='c2'/> "
            "Psychology, Built ran this race for prospect theory on thirteen thousand gamble problems. "
            "<bookmark mark='d'/> And robustness. Some famous findings, like ego depletion, did not survive "
            "large, preregistered replications; others, like loss aversion in many settings and the power of "
            "defaults, did, at sizes that are now being pinned down."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, (mk, c) in enumerate(zip("abcd", cards.cards)):
                vo.wait_until(mk)
                out = [FadeOut(chains[k - 1]), FadeOut(asks[k - 1])] if k else []
                self.play(*out, FadeIn(c, shift=UP * 0.1), run_time=0.8)
                ch = chains[k]
                self.play(LaggedStart(*[FadeIn(b) for b in ch.boxes], lag_ratio=0.35),
                          LaggedStart(*[GrowArrow(a) for a in ch.arrows], lag_ratio=0.35), run_time=2.4)
                if k < 3:
                    vo.wait_until(mk + "2")
                self.play(FadeIn(asks[k], shift=UP * 0.1), Circumscribe(c, color=WHITE, buff=0.05))
        self.clear_scene()

    def learned(self):
        C = load("c13k")
        P = C["params"]
        x = np.linspace(-60, 60, 241)
        ax = plane([-60, 60], [-90, 45], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.0, y_length=4.8,
                   xticks=[-60, -30, 0, 30, 60], yticks=[-90, -60, -30, 0, 30],
                   xlabel=r"outcome, \ against the reference point", ylabel=r"how it feels",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        v92 = behave.pt_value(x)
        vfit = behave.pt_value(x, P["alpha"], P["alpha"], P["lam"])
        l92 = path(ax, x, v92, GREY_B, 2.6)
        lfit = path(ax, x, vfit, GYM, 3.2)
        side = VGroup(
            label(rf"choices13k: \ {C['n_problems']:,} described \\ problems, \ {C['n_choices']:,} choices",
                  font_size=18, color=WHITE),
            label(r"grey: \ Tversky and \\ Kahneman, \ $\lambda$ = 2.25", font_size=18, color=GREY_B),
            label(rf"gold: \ fitted here, \\ $\alpha$ = {P['alpha']:.2f}, \ $\lambda$ = {P['lam']:.2f}", font_size=18,
                  color=GYM),
            label(r"in risky choices \\ between gambles, \ the \\ kink is much smaller", font_size=18, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"Peterson et al.\ (2021), \ choices13k; \ fitted as in Psychology, Built, \ Part 26",
                       corner=DR, font_size=11)
        with self.voiceover(
            "Here is one result from that race, refitted for this part. <bookmark mark='a'/> Joshua Peterson and "
            "his coauthors collected online choices between pairs of gambles on an unprecedented scale. Fitting "
            f"prospect theory to {C['n_problems']:,} of the problems described in words, with "
            f"{C['n_choices']:,} choices, <bookmark mark='b'/> against Tversky and Kahneman's parameters in grey, "
            f"<bookmark mark='c'/> gives a loss aversion of {P['lam']:.2f}, in gold, not 2.25. "
            "<bookmark mark='d'/> In these risky choices between gambles the kink is far smaller. Loss aversion is "
            "not one number; the first dial, in chapter fourteen, collected what it is in different settings."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(Indicate(side[0], color=WHITE))
            vo.wait_until("b")
            self.play(Create(l92), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(lfit), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
