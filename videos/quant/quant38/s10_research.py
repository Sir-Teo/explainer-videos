from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant38.common import (BAD, GOOD, HURDLE, MAKER_C, PART, SNIPE_C, SPREAD_C, load)


class Research(VoiceoverScene):
    def construct(self):
        b = load("bcs")
        self.card()
        self.setup_()
        self.payoffs()
        self.undercut()
        self.existence()
        self.theorem()
        self.statics()
        self.general(b)
        self.check_sim(b)
        self.check_fba(b)
        self.fba_logic()
        self.fba_theorem()
        self.welfare(b)
        self.arms_formal()
        self.check_general(b)
        self.btc(b)
        self.related()
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"The sniping equilibrium", r"Why does competition in speed not narrow the spread, and what "
                          r"would?", part=PART)
        with self.voiceover('For the researcher. We derive a unique role-indifference spread under a simplified equal-speed model and extend its root equation to integrable random jump magnitudes. We distinguish industry revenue from transfers to pure snipers. A batch exposure heuristic and an explicit speed-investment game are separate models. Simulation checks arithmetic under the source assumptions; it does not prove market-wide welfare or identify public news from Bitcoin snapshots.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_(self):
        rows = [cmath(r"y_t", r":", r"\text{public value, jumps } \pm J \text{ at rate } \lambda_J", font_size=34),
                cmath(r"\text{investors}", r":", r"\text{rate } \lambda_I,\ \text{trade one unit at the best quote}",
                      font_size=32),
                cmath(r"N\ge2\ \text{firms}", r":", r"\text{equally fast; serial processing, random order}", font_size=32),
                cmath(r"\text{roles}", r":", r"\text{one provides } y \pm s/2;\ \text{the others may snipe}", font_size=32,
                      colors={r"\text{roles}": MAKER_C})]
        whys = [why(r"the value moves only on public news, seen by all fast firms at once"),
                why(r"investors are uninformed and impatient: they pay the half-spread"),
                why(r"messages sent at the same instant are processed one at a time, each order equally likely"),
                why(r"a liquidity provider quotes around the value; when a jump makes its quote stale, it tries to cancel and "
                    r"the others try to trade against it")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The assumptions. <bookmark mark='a'/> Public value has symmetric fixed jumps of positive size J at positive rate lambda J. <bookmark mark='b'/> Independent uninformed investors arrive at positive rate lambda I and trade one unit. <bookmark mark='c'/> At least two identical-speed, risk-neutral firms have simultaneous messages ordered uniformly at random. <bookmark mark='d'/> One quotes around value and others can snipe or undercut continuously, with no tick, inventory, fees or investment cost. The conclusion is limited to this role model."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        rows = [cmath(r"\pi_L(s)", r"=", r"\lambda_I \tfrac s2 - \lambda_J \tfrac{N - 1}{N}\,(J - \tfrac s2)^+", font_size=36,
                      colors={r"\pi_L(s)": MAKER_C}),
                cmath(r"\pi_S(s)", r"=", r"\lambda_J \tfrac1N\,(J - \tfrac s2)^+", font_size=36, colors={r"\pi_S(s)": SNIPE_C}),
                cmath(r"\pi_L - \pi_S", r"=", r"\lambda_I \tfrac s2 - \lambda_J (J - \tfrac s2)^+", font_size=36,
                      colors={r"\pi_L - \pi_S": HURDLE})]
        whys = [why(r"Lemma 1: the provider earns from every investor and loses to a jump whenever one of the other "
                    r"$N - 1$ messages is processed before its cancel"),
                why(r"each other firm wins a given race with probability $1/N$"),
                why(r"the difference no longer contains $N$: the two $1/N$ terms add to one race lost per jump")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Lemma one, the payoffs. <bookmark mark='a'/> The provider earns from every investor, and loses whenever one "
            "of the other N minus one messages beats its cancel. <bookmark mark='b'/> Each other firm wins a given race "
            "one time in N. <bookmark mark='c'/> And the difference between the two roles does not contain N at all: the "
            "provider's losses and one sniper's gains add up to one whole race per jump."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def undercut(self):
        rows = [cmath(r"s > s^*", r"\Rightarrow", r"\pi_L > \pi_S:\ \text{a rival undercuts}", font_size=36),
                cmath(r"s < s^*", r"\Rightarrow", r"\pi_L < \pi_S:\ \text{the provider withdraws}", font_size=36),
                cmath(r"\Rightarrow", r"\ ", r"\pi_L(s^*) = \pi_S(s^*)", font_size=40, colors={r"\pi_L(s^*) = \pi_S(s^*)": HURDLE})]
        whys = [why(r"Lemma 2: if providing pays more than sniping, another firm posts a slightly narrower spread, takes the "
                    r"investors, and earns more; Bertrand competition in price"),
                why(r"if it pays less, the provider would rather snipe; no one provides at that spread"),
                why(r"so any equilibrium spread makes the two roles equally attractive")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Lemma two, indifference. <bookmark mark='a'/> If providing paid more than sniping, a rival would post a "
            "slightly narrower spread, take the investors, and earn more: competition on price. <bookmark mark='b'/> If "
            "it paid less, the provider would rather snipe, and no one would provide at that spread. "
            "<bookmark mark='c'/> So in any equilibrium the two roles are equally attractive."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def existence(self):
        rows = [cmath(r"D(h)", r"=", r"\lambda_I h - \lambda_J (J - h)^+", font_size=40),
                cmath(r"D(0) < 0,\ \ D(J) > 0", r",", r"D\ \text{strictly increasing}", font_size=34),
                cmath(r"\Rightarrow", r"\ ", r"h^* = \frac{\lambda_J J}{\lambda_I + \lambda_J}\ \text{unique}", font_size=38,
                      colors={r"h^* = \frac{\lambda_J J}{\lambda_I + \lambda_J}\ \text{unique}": HURDLE})]
        whys = [why(r"Lemma 3: the difference as a function of the half-spread $h = s/2$"),
                why(r"negative at zero, positive at the jump size, and strictly increasing in between"),
                why(r"so it has exactly one root, and on $[0, J]$ it is linear: solve for $h$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Existence and uniqueness of the indifference root. <bookmark mark='a'/> Let D of h be investor revenue minus the jump excess rate. <bookmark mark='b'/> With positive rates and positive J, it is negative at zero and positive at J. Continuity gives a root. It increases by at least lambda I times any increase in h, so the root is unique. <bookmark mark='c'/> Inside zero to J, solve the linear equation. This establishes the unique candidate spread under the prior role and undercutting assumptions, not a complete endogenous-speed equilibrium."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def theorem(self):
        st = VGroup(
            MathTex(r"h^*=\frac{\lambda_J J}{\lambda_I+\lambda_J},\qquad N\ge2",font_size=32),
            MathTex(r"N\pi^*=\lambda_I h^*,\qquad (N-1)\pi^*=\frac{N-1}{N}\lambda_I h^*",font_size=28),
            wrapped_label(r"industry profit equals investor spread payments; only the second quantity is the aggregate profit of pure snipers. Equal-speed role indifference does not solve the speed-investment game",9.6,20),
        ).arrange(DOWN,buff=0.35)
        card=theorem_card(r"Conditional sniping role equilibrium",st,r"simplified BCS assumptions",width=11.8,font_size=22)
        self.add(card)
        with self.voiceover("The conditional result. <bookmark mark='a'/> The unique half-spread is independent of N when rates, jump sizes and the stated market design are fixed. <bookmark mark='b'/> Each of the N roles earns investor payments divided by N. Industry profit therefore equals all investor spread payments, while the N minus one pure snipers receive only N minus one over N of that amount. Sniping transfers cancel inside the industry's accounts. A separate investment game is needed to discuss speed spending.") as vo:
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Circumscribe(st[1],color=HURDLE,buff=0.1))
        self.wait(0.5)
        self.clear_scene()

    def statics(self):
        rows = [cmath(r"\frac{\partial h^*}{\partial \lambda_J}", r">", r"0", font_size=40),
                cmath(r"\frac{\partial h^*}{\partial \lambda_I}", r"<", r"0", font_size=40),
                cmath(r"\frac{\partial h^*}{\partial N}", r"=", r"0", font_size=40, colors={r"0": HURDLE})]
        whys = [why(r"holding investor rate and jump size fixed, more public jumps widen this model spread; this alone does not rank markets such "
                    r"as ETFs and futures by actual sniping frequency"),
                why(r"more uninformed investors spread the sniping cost over more trades: busier markets are cheaper"),
                why(r"N cancels only in the specified equal-speed role payoffs; entry can change other market parameters")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Comparative statics with other inputs fixed. <bookmark mark='a'/> A higher public-jump rate increases this model's spread. This alone says nothing about which real correlated markets are sniped most. <bookmark mark='b'/> A higher uninformed investor rate lowers the spread for a fixed jump process and unit size. <bookmark mark='c'/> N cancels only under the equal-speed role structure. Entry can affect other parameters in real markets."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def general(self, b):
        rows = [cmath(r"\lambda_I\,h^*", r"=", r"\lambda_J\,\mathbb E\big[(|J| - h^*)^+\big]", font_size=40,
                      colors={r"\lambda_I\,h^*": HURDLE}),
                cmath(r"\text{LHS}\uparrow,\ \text{RHS}\downarrow", r"\Rightarrow", r"\text{a unique root}", font_size=36),
                cmath(r"U_1\preceq_{cx}U_2", r"\Rightarrow", r"h_1^*\le h_2^*", font_size=36,
                      colors={r"h_1^*\le h_2^*": BAD})]
        whys = [why(r"with random jump sizes, the provider loses only on jumps larger than its half-spread, and then the "
                    r"excess"),
                why(r"the left side rises in $h$, the right side falls: the same argument gives one equilibrium"),
                why(r"convex-order dominance of integrable nonnegative magnitudes raises $\mathbb E[(|J| - h)^+]$ or leaves it unchanged "
                    r"(it is convex in $J$), so the root does not decrease; equal means and higher variance alone do not order the cost of being "
                    r"sniped")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Random magnitudes U. <bookmark mark='a'/> Assume U is nonnegative, integrable, and positive with positive probability, with both arrival rates positive. The indifference equation uses the expected positive excess U minus h. <bookmark mark='b'/> The left side increases strictly; the excess is continuous and nonincreasing, bounded above by the finite mean. Thus there is exactly one positive root. <bookmark mark='c'/> If one magnitude distribution dominates another in convex order, its expected excess is no smaller at every h, so its root is no smaller. Equal mean and higher variance alone, or a generic fat-tail label, does not imply this ordering."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def check_sim(self, b):
        sims = b["sims"]
        x = np.asarray([s["half"] for s in sims], float)
        d = np.asarray([s["lp"] - s["sniper"] for s in sims], float)
        k = int(np.argmin(np.abs(d)))
        cross = float(np.interp(0, d, x)) if np.all(np.diff(d) > 0) else float(x[k])
        rows = [cmath(r"\text{formula}", r":", rf"s^*/2 = {b['s_star']:.3f}", font_size=38, colors={r"\text{formula}": HURDLE}),
                cmath(r"\text{simulation}", r":", rf"\pi_L = \pi_S\ \text{{at}}\ {cross:.3f}", font_size=38),
                cmath(r"N = 2 \ldots 30", r":", r"\pi_L = \pi_S\ \text{at } s^*\ \text{for every } N", font_size=34,
                      colors={r"N = 2 \ldots 30": GOOD})]
        whys = [why(r"$\lambda_I = 1$, $\lambda_J = 0.1$, $J = 4$"),
                why(r"two hundred thousand units of time; the crossing of the two profit curves, interpolated"),
                why(r"Chapter 6's table: at the formula's spread the two roles earn the same whatever the number of firms")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"An arithmetic consistency check. <bookmark mark='a'/> The fixed-jump formula gives {b['s_star']:.3f}. <bookmark mark='b'/> Interpolating simulated profit differences gives {cross:.3f}. <bookmark mark='c'/> Across the selected N values, the role means are approximately equal within Monte Carlo variation. This simulation implements the stipulated race probabilities; it does not independently validate an equilibrium in observed markets."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def check_fba(self, b):
        f = b["fba"]
        rows = [cmath(r"\text{continuous}", r":", rf"\pi_S = {b['byN'][2]['sniper']:.3f}", font_size=38,
                      colors={r"\text{continuous}": SNIPE_C}),
                cmath(r"\text{batch}", r":", rf"\pi_S = {f['sniper']:.0f}", font_size=38, colors={r"\text{batch}": GOOD}),
                cmath(r"\text{provider at } s^*", r":", rf"\pi_L = {f['lp']:.3f}\ \text{{(all spread, no losses)}}", font_size=34)]
        whys = [why(r"five firms, at the equilibrium spread of continuous trading"),
                why(r"the source batch flag removes stale trades by construction; it does not simulate the interval or latency, and no stale quote is "
                    r"ever traded"),
                why(r"so the same spread is pure profit; price competition among providers would push it down toward "
                    r"zero, which is the case for batch auctions")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"What the batch flag actually tests. <bookmark mark='a'/> At the continuous-market spread, the five-firm simulation gives roughly {b['byN'][2]['sniper']:.3f} per pure sniper per time unit. <bookmark mark='b'/> With the batch flag, stale-trade losses are removed by construction. The numeric interval is not used in the unchanged algorithm, and there is no modeled cancellation latency. <bookmark mark='c'/> The provider retains investor payments at this fixed spread. The program does not simulate entry, undercutting, the new equilibrium spread or a latency-to-interval law."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def fba_logic(self):
        rows = [cmath(r"\text{news before the batch closes}", r"\Rightarrow", r"\text{all firms re-price}", font_size=32),
                cmath(r"\text{many providers}", r"\Rightarrow", r"\text{Bertrand on price}", font_size=36),
                cmath(r"s_{\text{batch}}", r"\to", r"\text{remaining costs, conditional on repricing}", font_size=34,
                      colors={r"s_{\text{batch}}": GOOD})]
        whys = [why(r"in a batch, the order of messages within the interval is irrelevant: a provider that sees news can "
                    r"update its quote before the auction uses it"),
                why(r"so providers compete by undercutting each other's prices, not by racing"),
                why(r"ideal timely repricing removes the stipulated stale executions; finite updates and boundary news require a separate model for the "
                    r"remaining spread components")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The ideal repricing argument. <bookmark mark='a'/> If all providers receive public news and can replace quotes before uniform-price clearing, earlier messages within that batch need not win stale trades. <bookmark mark='b'/> With multiple providers, common information and negligible costs, competition can narrow the spread. <bookmark mark='c'/> Real latency, batch-boundary news, private information, inventory and fragmentation remain. Zero stale trades in our flagged simulation are an imposed mechanism, not a proof that every batch design eliminates those costs."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def fba_theorem(self):
        rows=[cmath(r"u",r"=",r"\min(1,\delta/\tau)\quad\text{(uniform news phase)}",font_size=34),
              cmath(r"h_u",r"=",r"\frac{\lambda_J uJ}{\lambda_I+\lambda_Ju}\quad\text{(stylized replacement)}",font_size=34,colors={r"h_u":GOOD}),
              cmath(r"\delta=1\,\mu\text{s},\ \tau=100\,\text{ms}",r":",r"u=10^{-5}",font_size=34)]
        whys=[why(r"a deterministic update latency, uniform jump phase and no other stale exposures give the fraction of news in the unprotected final window"),
              why(r"replace the jump-opportunity rate by $u\lambda_J$ while preserving the same conditional race and role assumptions; this is not the unchanged batch-flag simulation"),
              why(r"exposure opportunities shrink by $10^5$; the spread ratio is $u(\lambda_I+\lambda_J)/(\lambda_I+u\lambda_J)$, not exactly $u$")]
        step=ladder(self,rows,whys,keep=3,top=2.6,x=-0.3,buff=0.55,edge=6.9)
        with self.voiceover("A separate exposure heuristic. <bookmark mark='a'/> Assume news has uniform phase in a batch and a deterministic quote-update latency delta. Only the final delta of an interval tau is unprotected when delta is below tau, giving an exposure fraction delta over tau. This is not yet the probability a sniper wins. <bookmark mark='b'/> If we also preserve the same conditional race and role assumptions, replacing the jump-opportunity rate by that fraction gives this illustrative root. <bookmark mark='c'/> One microsecond over one hundred milliseconds is ten to the minus five for opportunities. The spread ratio has a further rate-dependent factor. Our unchanged simulator does not test this latency model.") as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def welfare(self, b):
        h = b["s_star"]
        rows = [cmath(r"\text{investors' cost}", r"=", r"\lambda_I\,h^*", font_size=40),
                cmath(r"", r"=", rf"{b['lam_i']:.0f} \times {h:.3f} = {b['lam_i'] * h:.3f}\ \text{{per unit time}}",
                      font_size=36, colors={rf"{b['lam_i'] * h:.3f}\ \text{{per unit time}}": HURDLE}),
                cmath(r"\text{batch}", r"\Rightarrow", r"\text{distinguish transfers and resource costs}", font_size=34,
                      colors={r"\text{batch}": GOOD})]
        whys = [why(r"investor payments equal industry profit; pure snipers receive only $(N-1)/N$ of it"),
                why(r"in the simulation's parameters"),
                why(r"the batch market returns the rent to investors through narrower spreads, and removes the reason to "
                    r"spend on redundant speed. Investor payments are transfers, so do not add them again as deadweight resource losses")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"Separate transfers from resource costs. <bookmark mark='a'/> Investor spread payments equal industry profit in this simplified model, not profit of the pure snipers alone. <bookmark mark='b'/> With the chosen rates, payments are {b['lam_i'] * h:.3f} per time unit. <bookmark mark='c'/> Narrower spreads can transfer surplus from firms to investors. Real resources spent on otherwise redundant speed can be a social loss, but adding the entire investor payment again would double-count a transfer. Welfare also depends on participation, information and trading benefits absent from this calculation."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def arms_formal(self):
        rows=[cmath(r"m=0",r":",r"\Delta\pi=R(1-1/N)-c",font_size=36),
              cmath(r"1\le m\le N-1",r":",r"\Delta\pi=R/(m+1)-c",font_size=36),
              cmath(r"0<c<R/N",r"\Rightarrow",r"\text{strict dominance; all invest; resource cost }Nc",font_size=30,colors={r"0<c<R/N":BAD})]
        whys=[why(r"binary fixed-prize game: no fast rivals means the slow baseline is $R/N$ and the sole fast investor gets $R$"),
              why(r"with $m$ fast rivals, slow earns zero; joining their equal-speed group gives $R/(m+1)$ before cost"),
              why(r"the minimum gross gain is $R/N$ for $N\ge2$. With positive cost, all-fast is worse for every firm than all-slow; speed benefits beyond this fixed prize are excluded")]
        step=ladder(self,rows,whys,keep=3,top=2.6,x=-0.3,buff=0.55,edge=6.9)
        with self.voiceover("Prove dominance in the separate fixed-prize game. <bookmark mark='a'/> If no rival invests, becoming the sole fast firm gains R times one minus one over N, less cost c. <bookmark mark='b'/> With m fast rivals, remaining slow gets zero, while investing gets R over m plus one, less c. <bookmark mark='c'/> The smallest gross gain across these cases is R over N. Thus positive cost below R over N makes investment strictly dominant. Every firm then gets R over N minus c, worse than the all-slow outcome by c. Total resource use is N c under these explicit assumptions.") as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def check_general(self, b):
        g = b["btc"]["gsims"]
        x = np.asarray([s["half"] for s in g], float)
        d = np.asarray([s["lp"] - s["sniper"] for s in g], float)
        cross = float(np.interp(0, d, x))
        top = float(np.ceil(np.abs(d).max()))
        ax_ = axes([0.1, 0.6], [-top, top], x_length=6.4, y_length=4.4, xlabel=r"half-spread $h$, ticks",
                   ylabel=r"$\pi_L - \pi_S$, ticks a second", xticks=[0.1, 0.3, 0.5], yticks=[-top, 0, top],
                   yfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = ax_.ax
        c_ = VGroup(curve(ax, x, d, MAKER_C, stroke_width=3), *[Dot(ax.c2p(a, y), radius=0.06, color=MAKER_C)
                                                               for a, y in zip(x, d)])
        root = DashedLine(ax.c2p(b["btc"]["general_half"], -top), ax.c2p(b["btc"]["general_half"], top), color=HURDLE,
                          stroke_width=1.8)
        zero = DashedLine(ax.c2p(0.1, 0), ax.c2p(0.6, 0), color=GREY_B, stroke_width=1.2)
        with self.voiceover(
            "Check three: the general condition, with Bitcoin's own jump sizes. Simulate the market with jumps drawn from "
            "every real mid change and the takers' real rate. <bookmark mark='a'/> The difference between the two roles "
            f"crosses zero at {cross:.2f} of a tick, <bookmark mark='b'/> where the condition, solved directly, puts it: "
            f"{b['btc']['general_half']:.2f}."
        ) as vo:
            self.play(FadeIn(ax_), Create(zero))
            vo.wait_until("a")
            self.play(Create(c_))
            vo.wait_until("b")
            self.play(Create(root))
        self.wait(0.4)
        self.clear_scene()

    def btc(self, b):
        bt = b["btc"]
        rows = [cmath(r"\text{all 100-ms moves}", r":", rf"{bt['lam_all']:.2f}\ \text{{a second}},\ \text{{mean}}\ "
                      rf"{bt['mean_move']:.0f}\ \text{{ticks}}", font_size=32),
                cmath(r"h^*", r"\approx", rf"{bt['general_half']:.2f}\ \text{{tick}}", font_size=40, colors={r"h^*": HURDLE}),
                cmath(r"\text{tick-pinned}", r":", r"h = 0.5", font_size=40, colors={r"\text{tick-pinned}": SPREAD_C})]
        whys = [why(r"every change of Bitcoin's mid between snapshots, with its empirical size distribution, as the jumps"),
                why(rf"the general condition solved with $\lambda_I$ = {bt['lam_i']:.0f} trades a second: close to the "
                    rf"two-point calibration's {bt['half']:.2f}"),
                why(r"the proxy root is below the quoted half-tick floor under these assumptions; this does not "
                    r"identify the real natural spread, rent or causes of the replay losses")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"A proxy substitution, not identification. <bookmark mark='a'/> Net mid changes occur {bt['lam_all']:.2f} times per second in the snapshots, averaging {bt['mean_move']:.0f} ticks. <bookmark mark='b'/> Treating their empirical magnitudes as independent public jumps and aggregate trade counts as uninformed unit arrivals gives a root {bt['general_half']:.2f} tick. <bookmark mark='c'/> That is below the quoted half-tick floor in this model. Snapshots combine endogenous order flow and news, traders have different sizes and information, and jumps are dependent. The result neither identifies the actual natural spread nor attributes the replay losses to another channel."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def related(self):
        cards = VGroup(
            desk_question(r"Budish, Cramton and Shim (2015)", r"the continuous-market model with general jumps, the arms "
                          r"race, and frequent batch auctions; evidence from correlated futures and ETFs", width=12.4,
                          font_size=18),
            desk_question(r"Aquilina, Budish and O'Neill (2022)", r"the races measured message by message on the London "
                          r"Stock Exchange", width=12.4, font_size=18),
            desk_question(r"Baldauf and Mollner (2020); Menkveld and Zoican (2017)", r"how faster exchanges and more "
                          r"competition among makers can widen or narrow spreads once information acquisition is endogenous",
                          width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        self.add(cards[0])
        with self.voiceover(
            "Where this sits. <bookmark mark='a'/> Budish, Cramton and Shim's paper has general jumps, the arms race, and "
            "batch auctions, with evidence from correlated futures and funds. <bookmark mark='b'/> Aquilina, Budish and "
            "O'Neill measured the races on the London Stock Exchange. <bookmark mark='c'/> And Markus Baldauf and Joshua "
            "Mollner, and Menkveld and Marius Zoican, showed that once acquiring information is a choice, faster markets "
            "can widen spreads or narrow them."
        ) as vo:
            for k_, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k_:
                    self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: informed and sniping costs together", r"an equilibrium spread with private information, "
                          r"public jumps and inventory at once, estimated on message data", width=12.4, font_size=18),
            desk_question(r"open: competing market designs", r"when continuous and batch markets coexist, where does "
                          r"liquidity go, and is the outcome efficient?", width=12.4, font_size=18),
            desk_question(r"open: crypto's many venues", r"sniping across exchanges with different latencies and no "
                          r"consolidated quote; who wins, and what it costs takers", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        self.add(cards[0])
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> An equilibrium spread with private information, public jumps and "
            "inventory together, estimated from message data. <bookmark mark='b'/> When continuous and batch markets "
            "coexist, where does liquidity go, and is the result efficient? <bookmark mark='c'/> And sniping across "
            "crypto's many venues, with different latencies and no consolidated quote: who wins, and what does it cost "
            "takers?"
        ) as vo:
            for k_, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k_:
                    self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = VGroup(label(r"Pause and predict", font_size=32, color=QC.IDEA),
                   wrapped_label('investors arrive at rate 10, jumps of 3 ticks at rate 2. What is the sniping half-spread? And if jumps are 1 or 5 ticks with equal chance (same mean)?', 11.8, 30)).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        with self.voiceover(
            "Pause and predict. Investors arrive at rate ten and jumps of three ticks at rate two. What is the sniping "
            "half-spread? And if the jumps are one or five ticks with equal chance, the same mean?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
