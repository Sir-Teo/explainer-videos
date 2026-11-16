from __future__ import annotations

from videos.psychology.psych37.common import *  # noqa: F403


class Preferences(VoiceoverScene):
    def construct(self):
        self.card()
        self.utility()
        self.population()
        self.limits()

    def card(self):
        card = chapter_card(5, r"Social preferences", r"Can fairness be written as a utility function?",
                            lit={1999: r"Fehr \& Schmidt"}, part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter five. Social preferences."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def utility(self):
        head = heading(r"Inequity aversion")
        eq = MathTex(r"U_i = x_i - \alpha \max(x_j - x_i,\, 0) - \beta \max(x_i - x_j,\, 0)", font_size=40)
        eq.move_to([0, 1.6, 0])
        rows = rows_of([
            (r"Fehr and Schmidt, \ 1999: \ people care about their own payoff $x_i$, \ and dislike inequality", WHITE),
            (r"$\alpha$: \ how much a person minds earning less than the other", AUTH),
            (r"$\beta$: \ how much they mind earning more", CROWD),
            (r"a responder offered a share $s$ of a pie of 1 accepts when $s - \alpha(1 - 2s) \ge 0$: \ that is, \ "
             r"when $s \ge \alpha / (1 + 2\alpha)$", MODEL),
            (r"with $\alpha = 1$, \ any offer below a third is rejected, \ out of pure arithmetic", YOU),
        ], 11.6, 22, 0.38).move_to([0, -1.0, 0])
        with self.voiceover(
            "Can fairness be written as a utility function? <bookmark mark='a'/> In 1999 Ernst Fehr and Klaus "
            "Schmidt proposed that people care about their own payoff and dislike inequality. "
            "<bookmark mark='b'/> Alpha is how much a person minds earning less than the other. "
            "<bookmark mark='c'/> Beta is how much they mind earning more. <bookmark mark='d'/> A responder offered "
            "a share s of a pie of one accepts when s, minus alpha times the shortfall, one minus two s, is at "
            "least zero. That's when s is at least alpha over one plus two alpha. <bookmark mark='e'/> With alpha "
            "equal to one, any offer below a third is rejected, out of pure arithmetic."
        ) as vo:
            self.play(FadeIn(head), Write(eq))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def population(self):
        d = load("ultimatum")
        head = heading(r"The proposer's problem")
        A = axes([0, 0.5], [0, 1.0], x_length=5.4, y_length=3.4, xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5],
                 yticks=[0, 0.5, 1.0], xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{v:g}",
                 xlabel=r"offer, \ share of the sum", center=[-3.3, -0.3, 0], font_size=15)
        acc = curve(A.ax, d["offers"], d["accept"], CROWD)
        pay = curve(A.ax, d["offers"], d["payoff"], GOOD)
        best = DashedLine(A.ax.c2p(d["best"], 0), A.ax.c2p(d["best"], 1.0), color=PERSON)
        bl = label(rf"best offer: \ {pct(d['best'])}", font_size=16, color=PERSON).next_to(A.ax.c2p(d["best"], 1.0),
                                                                                         UP, buff=0.08)
        key = legend([(CROWD, r"chance of acceptance"), (GOOD, r"proposer's expected share")], font_size=14).move_to(
            A.ax.c2p(0.14, 0.85))
        rows = rows_of([
            (r"Psyche's responders: \ 30\% care only about money; \ the rest have $\alpha$ between 0.3 and 1.5", WHITE),
            (r"the chance of acceptance rises with the offer", CROWD),
            (r"a proposer who wants only money maximizes (1 $-$ offer) $\times$ (chance of acceptance)", GOOD),
            (rf"the best offer is {pct(d['best'])}: \ a selfish proposer facing fair-minded responders offers about "
             r"what real proposers offer", YOU),
        ], 6.0, 20, 0.36).move_to([3.4, -0.3, 0])
        tag = psyche_tag(r"\texttt{social.ultimatum}")
        with self.voiceover(
            "Now the proposer's problem. <bookmark mark='a'/> Psyche's population of responders: thirty percent "
            "care only about money, and the rest have alphas between point three and one and a half. "
            "<bookmark mark='b'/> The chance an offer is accepted rises with the offer. <bookmark mark='c'/> A "
            "proposer who wants only money maximizes what they keep times the chance of acceptance. "
            f"<bookmark mark='d'/> The best offer is {spct(d['best'])}. A perfectly selfish proposer, facing "
            "fair-minded responders, offers about what real proposers offer. Generous offers needn't mean "
            "generous proposers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(acc), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(pay), FadeIn(key), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(best), FadeIn(bl), FadeIn(rows[3]))
        self.clear_scene()

    def limits(self):
        head = heading(r"Where the model strains")
        rows = rows_of([
            (r"inequity aversion explains rejections and much of the generosity in ultimatum and public-goods "
             r"games", GOOD),
            (r"but given the chance to exit a dictator game quietly, \ taking a little less and leaving the other "
             r"none the wiser, \ about a third did (Dana, \ Cain and Dawes, \ 2006): \ part of fairness is wanting "
             r"to look fair", AUTH),
            (r"and intentions matter: \ the same unequal split is rejected less when a computer chose it than when "
             r"a person did", CROWD),
            (r"a utility function is a summary of choices, \ not a mechanism; \ reputation, \ intention and norms "
             r"all feed into it", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        with self.voiceover(
            "The model explains a lot, and strains in places. <bookmark mark='a'/> Inequity aversion accounts for "
            "rejections, and for much of the generosity in ultimatum and public-goods games. "
            "<bookmark mark='b'/> But when Dana, Cain and Dawes let dictators take a little less and leave quietly, "
            "with the other person never told a game had been played, about a third did. Part of fairness is "
            "wanting to look fair. <bookmark mark='c'/> And intentions matter: the same "
            "unequal split is rejected less when a computer chose it than when a person did. "
            "<bookmark mark='d'/> A utility function summarizes choices. It isn't a mechanism, and reputation, "
            "intention and norms all feed into it."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
