from __future__ import annotations

from videos.economics.econ53.common import *  # noqa: F403


class Global(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Global games", r"Can a little private noise pick one equilibrium?",
             "Chapter nine. Global games.", lit={1993: r"Carlsson and van Damme", 1998: r"Morris and Shin"},
             scale=("market", "nation"), horizon=("a day",))
        self.setup_()
        self.threshold()
        self.public()

    def setup_(self):
        G = load("global")
        rows = VGroup(
            label(r"a regime: \ a currency peg, \ a bank, \ a government", font_size=23, color=WHITE),
            label(rf"each speculator attacks or not; \ attacking costs {G['c']}, \ success pays 1", font_size=23,
                  color=SENDER),
            label(r"the regime falls if the share attacking exceeds its strength $\theta$", font_size=23,
                  color=ERR),
            label(r"with $\theta$ known: \ for middling strength, \ all attack or none: \ two equilibria",
                  font_size=23, color=GREY_A),
            label(r"with each seeing $\theta$ plus a little private noise: \ one equilibrium", font_size=23,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).move_to(UP * 0.2)
        tag = published_tag(r"Carlsson and van Damme (1993); \ Morris and Shin, \ AER (1998), \ (2003)",
                            corner=DR, font_size=12)
        past = point_cards([(r"Part 26: \ bank runs", r"if everyone runs, running is right; \ if nobody runs, "
                             r"staying is", ERR),
                            (r"Part 34: \ currency attacks", r"if everyone attacks the peg, it falls; \ if nobody "
                             r"does, it holds", SENDER)], width=10.0, font_size=21).move_to(UP * 0.2)
        with self.voiceover(
            "Bank runs in Part twenty-six and currency attacks in Part thirty-four both had two equilibria: if "
            "everyone runs, running is right; if nobody does, staying is. Which happens seemed a matter of "
            "sunspots. <bookmark mark='a'/> Take a regime, a currency peg, a bank, a government. <bookmark "
            f"mark='b'/> Each speculator can attack at a cost of {G['c']}, and gains one if the regime falls. "
            "<bookmark mark='c'/> It falls if the share attacking exceeds its strength, theta. <bookmark "
            "mark='d'/> If theta is known to all, then for middling strength both all-attack and no-attack are "
            "equilibria. <bookmark mark='e'/> Hans Carlsson and Eric van Damme, and then Stephen Morris and Hyun "
            "Song Shin, changed one thing: each speculator sees the strength with a little private noise. Then "
            "there is only one equilibrium."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(past.cards[0], shift=UP * 0.1))
            self.play(FadeIn(past.cards[1], shift=UP * 0.1))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                if mk == "a":
                    self.play(FadeOut(past))
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def threshold(self):
        G = load("global")
        th = G["flat"]["theta"]
        steps = VGroup(
            label(r"guess: \ everyone attacks when their signal is below some $x^*$", font_size=22, color=SENDER),
            label(r"then the regime falls when $\theta$ is below some $\theta^*$", font_size=22, color=ERR),
            label(r"the speculator who sees exactly $x^*$ must be indifferent: \ "
                  r"$\Pr(\theta \le \theta^* \mid x^*) = c$",
                  font_size=22, color=BELIEF),
            label(r"the share attacking at $\theta^*$ is $\theta^*$; \ for that speculator it is uniform: \ "
                  r"$\theta^* = 1 - c$", font_size=22, color=THEORY),
            label(rf"here: \ the regime falls if and only if its strength is below {th:.1f}", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.2)
        with self.voiceover(
            "The argument fits on a card. <bookmark mark='a'/> Suppose everyone attacks when their signal is below "
            "some cutoff. <bookmark mark='b'/> Then the regime falls when its strength is below some threshold. "
            "<bookmark mark='c'/> The speculator whose signal is exactly at the cutoff must be indifferent: the "
            "chance that the regime falls, given her signal, equals the cost. <bookmark mark='d'/> And here is the "
            "beautiful step: from her point of view, the share of others attacking is equally likely to be "
            "anything between zero and one, whatever the noise. So the threshold is one minus the cost. <bookmark "
            f"mark='e'/> With a cost of {G['c']}, the regime falls if and only if its strength is below "
            f"{th:.1f}. The sunspot is gone: the fundamentals decide, through what everyone thinks everyone else "
            "sees."
        ) as vo:
            for mk, s_ in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s_, shift=RIGHT * 0.1))
        self.clear_scene()

    def public(self):
        G = load("global")
        theta = np.array(G["theta"])
        ax = plane([0, 1], [-20, 20], center=LEFT * 1.8 + DOWN * 0.3, x_length=7.4, y_length=4.6,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[-20, -10, 0, 10, 20], xlabel=r"threshold $\theta^*$",
                   ylabel=r"the equilibrium condition", xfmt=lambda v: f"{v:.2f}",
                   yfmt=lambda v: f"{v:.0f}".replace("-", "{-}"), font_size=14)
        cols = (RECEIVER, SENDER, ERR)
        curves, rhs, roots = VGroup(), VGroup(), VGroup()
        for cv, row, col in zip(G["curves"], G["rows"], cols):
            curves.add(path(ax, theta, np.clip(cv["lhs"], -20, 20), col, 2.6, yr=(-20, 20)))
            rhs.add(DashedLine(ax.ax.c2p(0, cv["rhs"]), ax.ax.c2p(1, cv["rhs"]), color=col, stroke_width=1.4))
            roots.add(VGroup(*[dot(ax, r, cv["rhs"], col, 0.08) for r in row["thetas"] if -20 <= cv["rhs"] <= 20]))
        side = VGroup(
            label(r"public information, \ such as an \\ announcement everyone hears, \\ of rising precision:",
                  font_size=18, color=WHITE),
            label(rf"blue: \ vague \ (s.d. {G['rows'][0]['prior_sd']:.1f}): \ one", font_size=18, color=RECEIVER),
            label(rf"gold: \ sharper \ ({G['rows'][1]['prior_sd']:.1f}): \ one", font_size=18, color=SENDER),
            label(rf"red: \ sharp \ ({G['rows'][2]['prior_sd']:.2f}): \ three", font_size=18, color=ERR),
            label(r"each crossing of a curve with \\ its dashed line is an equilibrium", font_size=18,
                  color=GREY_A),
            label(r"precise public signals bring \\ the multiplicity back", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "Uniqueness has a price: private information must be sharp relative to public information. Morris and "
            "Shin worked out the condition. <bookmark mark='a'/> Add a public signal that everyone hears, such as "
            "an official statement, and make it more and more precise. The curves show the equilibrium condition; "
            "each crossing with its dashed line is an equilibrium. <bookmark mark='b'/> With vague public "
            "information, one crossing. <bookmark mark='c'/> Sharper, still one. <bookmark mark='d'/> Sharp enough, "
            "and there are three: the multiplicity is back, because everyone now knows what everyone else knows. "
            "<bookmark mark='e'/> This is why central banks and regulators worry about what they say in public. A "
            "clear statement coordinates beliefs, for better or for worse."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(side[0]))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(Create(curves[k]), Create(rhs[k]), FadeIn(roots[k]), FadeIn(side[k + 1]), run_time=1.4)
            vo.wait_until("d")
            self.play(Indicate(roots[2], color=WHITE), FadeIn(side[4]))
            vo.wait_until("e")
            self.play(FadeIn(side[5]))
        self.clear_scene()
