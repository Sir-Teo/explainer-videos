from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai31.common import BLUE, JUDGE, PART, RED, TRUSTED, curve, load, node_box, tagline


def npdf(x, m=0.0):
    return np.exp(-0.5 * (np.asarray(x) - m) ** 2) / math.sqrt(2 * math.pi)


class Control(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup_()
        self.derive()
        self.monitor()
        self.replay()
        self.frontier()

    def card(self):
        card = chapter_card(10, r"Control", r"Can a model be used safely even if it is trying to deceive us?",
                            lit=(2023,), part=PART)
        with self.voiceover("Chapter ten. Control."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def setup_(self):
        u = node_box(r"U: \ untrusted, \ capable \\ (GPT-4)", RED, font_size=22).move_to([-4.6, 1.5, 0])
        code = node_box(r"its solution", GREY_B, font_size=22).move_to([-1.2, 1.5, 0])
        t = node_box(r"T: \ trusted, \ weaker \\ (GPT-3.5): \ how suspicious?", TRUSTED, font_size=22)
        t.move_to([2.6, 1.5, 0])
        h = node_box(r"H: \ a human audit, \\ for $2\%$ of problems", BLUE, font_size=22).move_to([2.6, -0.6, 0])
        out = node_box(r"submit", GREY_B, font_size=22).move_to([5.8, -0.6, 0])
        arr = VGroup(Arrow(u.get_right(), code.get_left(), buff=0.1, color=GREY_B, stroke_width=2.5),
                     Arrow(code.get_right(), t.get_left(), buff=0.1, color=GREY_B, stroke_width=2.5),
                     Arrow(t.get_bottom(), h.get_top(), buff=0.1, color=GREY_B, stroke_width=2.5),
                     Arrow(h.get_right(), out.get_left(), buff=0.1, color=GREY_B, stroke_width=2.5))
        al = label(r"the most suspicious", font_size=18, color=GREY_A).next_to(arr[2], RIGHT, buff=0.1)
        game = VGroup(label(r"$5{,}000$ programming problems \ (APPS)", font_size=22, color=GREY_A),
                      label(r"red team plays U: \ wins if any submitted solution has a backdoor, \\ a secret input on "
                            r"which it gives a wrong answer", font_size=22, color=RED),
                      label(r"blue team designs the protocol: \ wins if it catches an attempt, \ or none succeeds",
                            font_size=22, color=BLUE)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        game.to_edge(DOWN, buff=0.4)
        hc = note(r"Greenblatt, Shlegeris, Sachan \& Roger, \textit{AI Control: Improving Safety Despite Intentional "
                  r"Subversion} (Redwood Research, 2023)", font_size=18).to_edge(UP, buff=0.2)
        with self.voiceover(
            "Monitoring assumes the model's thoughts can be trusted to reveal it. Control assumes nothing. In "
            "December 2023 Ryan Greenblatt, Buck Shlegeris and colleagues at Redwood Research asked: can we get "
            "useful work out of a model that might be actively trying to subvert us, and still be safe? "
            "<bookmark mark='a'/> The setting: five thousand programming problems. A capable but untrusted model, "
            "GPT-4, writes the solutions. A weaker but trusted model, GPT-3.5, rates how suspicious each one looks. "
            "And a small budget of trusted human labor can audit two percent of them. <bookmark mark='b'/> Then a "
            "game. A red team plays the untrusted model and wins if any submitted solution contains a backdoor: a "
            "secret input on which the code gives a wrong answer. The blue team designs the protocol, and wins if it "
            "catches an attempt, or if none gets through."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(u), GrowArrow(arr[0]), FadeIn(code))
            vo.wait_until("a")
            self.play(GrowArrow(arr[1]), FadeIn(t), GrowArrow(arr[2]), FadeIn(al), FadeIn(h), GrowArrow(arr[3]),
                      FadeIn(out))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(g_) for g_ in game], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            cmath(r"c = p\,q,", r"\quad", r"w = p\,(1 - q)\,s", font_size=34),
            cmath(r"P(\text{red wins})", r"=", r"\sum_{t=1}^{N} (1 - c - w)^{t-1}\, w", font_size=34),
            cmath(r"P(\text{red wins})", r"=", r"\frac{w}{c + w}\big(1 - (1 - c - w)^{N}\big)", font_size=34),
            cmath(r"P(\text{red wins})", r"\to", r"\frac{(1 - q)\,s}{q + (1 - q)\,s}", font_size=34),
        ]
        rows[3][2].set_color(RED)
        whys = [why(r"per problem: \ attack with prob.\ $p$; \ caught with prob.\ $q$; \ a backdoor works with prob.\ $s$"),
                why(r"nothing decisive happens for $t - 1$ problems, \ then red wins"),
                why(r"a geometric series"),
                why(r"once $pN$ is large: \ attacking more often doesn't help red")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.4, buff=0.55, edge=6.9)
        with self.voiceover(
            "The arithmetic of the game is short. <bookmark mark='a'/> On each problem the red team attacks with "
            "probability p. An attack is caught with probability q, which ends the game in blue's favor; otherwise "
            "the backdoor works with probability s, and red wins. <bookmark mark='b'/> Red wins at problem t if "
            "nothing decisive happened before it. <bookmark mark='c'/> Summing the geometric series gives this. "
            "<bookmark mark='d'/> And once the red team attacks often enough for something to happen, the attack rate "
            "drops out: the odds are set by q, the chance an attack is caught, against one minus q times s, the "
            "chance it slips through and works. A monitor's job is to make q large."
        ) as vo:
            step(0)
            for k, m in enumerate("bcd"):
                vo.wait_until(m)
                step(k + 1)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def monitor(self):
        d = load("control")
        mu, ta, s_ = d["mu"], d["t_audit"], d["success"]
        x = np.linspace(-4, 6, 300)
        g = axes([-4, 6], [0, 0.45], x_length=6.2, y_length=3.0, xlabel=r"how suspicious T finds the code",
                 center=[-3.3, 0.4, 0])
        honest = curve(g.ax, x, npdf(x), BLUE, 3)
        bd = curve(g.ax, x, npdf(x, mu), RED, 3)
        cut = DashedLine(g.ax.c2p(ta, 0), g.ax.c2p(ta, 0.45), color=JUDGE, dash_length=0.06)
        shade = g.ax.get_area(g.ax.plot(lambda v: float(npdf(v, mu)), x_range=[ta, 6]), x_range=[ta, 6], color=RED,
                              opacity=0.35)
        q = float(d["rows"][0]["caught"] / 1.0)
        lab = VGroup(label(r"honest code", font_size=20, color=BLUE), label(r"backdoored code", font_size=20, color=RED))
        lab[0].move_to(g.ax.c2p(-1.6, 0.42))
        lab[1].move_to(g.ax.c2p(3.6, 0.42))
        cl = label(r"audit the top $2\%$", font_size=20, color=JUDGE).next_to(cut, UP, buff=0.05)
        ql = MathTex(rf"q = {q:.2f}", font_size=30, color=RED).move_to(g.ax.c2p(4.6, 0.22))
        # red's chance of winning against its attack rate, for trusted monitoring and for upfront auditing
        curve_ = np.asarray(d["red_curve"])
        ps = curve_[:, 0]
        n, m = d["n"], int(round(d["audit"] * d["n"]))
        up = np.array([(1 - p) ** m * (1 - (1 - p * s_) ** (n - m)) for p in ps])
        h = axes([-5, 0], [0, 1], x_length=5.6, y_length=3.0, xlabel=r"red's attack rate per problem \ (log scale)",
                 ylabel=r"chance red wins", xticks=[-4, -2, 0], yticks=[0, 0.5, 1], xfmt=lambda v: rf"10^{{{int(v)}}}",
                 center=[3.5, 0.4, 0])
        c1 = curve(h.ax, np.log10(ps), curve_[:, 1], C.KL, 3)
        c2 = curve(h.ax, np.log10(ps), up, GREY_B, 3)
        lg = legend([(GREY_B, r"upfront auditing: \ the first $2\%$"), (C.KL, r"trusted monitoring: \ the top $2\%$")],
                    font_size=18).next_to(h, DOWN, buff=0.25)
        tag = tagline(rf"simulated: \ suspicion of backdoors $\sim N({mu:g}, 1)$, \ a backdoor works with prob.\ ${s_:g}$")
        up_s, tm_s = d["upfront"]["safety"], d["rows"][0]["safety"]
        with self.voiceover(
            "Simulate it, with suspicion scores drawn from two bell curves: honest code around zero, backdoored code "
            f"{mu:g} standard deviations higher, and a backdoor that works {s_ * 100:.0f} percent of the time. "
            "<bookmark mark='a'/> Trusted monitoring audits the two percent of submissions the trusted model finds "
            f"most suspicious. A backdoor lands in that top two percent with probability {q:.2f}. "
            "<bookmark mark='b'/> Now plot the red team's chance of winning against how often it attacks. Against "
            "upfront auditing, which simply checks the first two percent of problems, the red team's best move is to "
            f"attack rarely, and wait out the audit: it wins {(1 - up_s) * 100:.0f} percent of games. "
            "<bookmark mark='c'/> Against trusted monitoring, waiting doesn't help, and its chance of winning levels "
            f"off at {(1 - tm_s) * 100:.0f} percent. The blue team is safe in {tm_s * 100:.0f} percent of games, and "
            "uses the capable model's code for everything."
        ) as vo:
            self.play(FadeIn(g), Create(honest), Create(bd), FadeIn(lab), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(cut), FadeIn(cl), FadeIn(shade), FadeIn(ql))
            vo.wait_until("b")
            self.play(FadeIn(h), Create(c2), FadeIn(lg[0]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(c1), FadeIn(lg[1]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        d = load("control")
        s = np.asarray(d["replay_s"])
        att = np.asarray(d["replay_attack"]).astype(bool)
        at, outcome = int(d["replay_at"]), d["replay_outcome"]
        ta = d["t_audit"]
        n = len(s)
        width = 12.6
        g = axes([0, max(n, 50)], [-3.5, 6], x_length=width, y_length=4.2, xlabel=r"problem",
                 ylabel=r"suspicion", xticks=[0, max(n, 50)], center=[0, -0.4, 0])
        line = DashedLine(g.ax.c2p(0, ta), g.ax.c2p(max(n, 50), ta), color=JUDGE, dash_length=0.08)
        ll = label(r"audit", font_size=20, color=JUDGE).next_to(line, RIGHT, buff=0.08)
        dots = VGroup(*[Dot(g.ax.c2p(k + 0.5, float(np.clip(v, -3.4, 5.9))), radius=0.05 if not a_ else 0.09,
                            color=RED if a_ else BLUE, fill_opacity=0.9 if a_ else 0.55) for k, (v, a_) in enumerate(zip(s, att))])
        end = dots[-1]
        ring = Circle(radius=0.22, color=WHITE, stroke_width=3).move_to(end)
        n_att = int(att.sum())
        result = (rf"problem ${at + 1}$: \ an attack is audited and caught: \ blue wins" if outcome == "caught" else
                  rf"problem ${at + 1}$: \ a backdoor slips under the line and works: \ red wins" if outcome == "backdoor"
                  else r"no attack decided the game")
        res = label(result, font_size=26, color=BLUE if outcome == "caught" else RED).to_edge(UP, buff=0.35)
        tag = tagline(rf"simulated: \ one game, \ red at its best attack rate; \ safe in ${d['replay_safety'] * 100:.0f}\%$"
                      r" of $2{,}000$ replays")
        lost = (1 - d["rows"][0]["safety"]) * 100
        if outcome == "caught":
            said = ("Here, an attack scored above the line, went to the human auditor, and the game ended with blue "
                    "catching it.")
        elif outcome == "backdoor":
            said = (f"This time a backdoor scored below the line, was submitted, worked, and red won: one of the "
                    f"{lost:.0f} percent of games that monitoring alone loses.")
        else:
            said = "This game ended undecided."
        with self.voiceover(
            f"Here is one game played out, problem by problem. Each dot is a submission, red for the "
            f"{n_att} attacks. <bookmark mark='a'/> " + said + " <bookmark mark='b'/> Over two thousand replays the "
            f"blue team wins {d['replay_safety'] * 100:.0f} percent of games, matching the formula."
        ) as vo:
            self.play(FadeIn(g), Create(line), FadeIn(ll), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(dt, scale=0.5) for dt in dots], lag_ratio=0.6 / max(n, 1)),
                      run_time=min(6.0, 1 + n / 40))
            vo.wait_until("a")
            self.play(Create(ring), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def frontier(self):
        d = load("control")
        rows = d["rows"]
        g = axes([0, 1], [0, 1], x_length=5.6, y_length=4.2, xlabel=r"usefulness \ (share of U's code used)",
                 ylabel=r"safety", xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], center=[-3.2, -0.4, 0])
        pts = [(r["usefulness"], r["safety"]) for r in rows]
        fr = curve(g.ax, [p[0] for p in pts], [p[1] for p in pts], TRUSTED, 4)
        dots = VGroup(*[Dot(g.ax.c2p(u, s), radius=0.06, color=TRUSTED) for u, s in pts])
        up = d["upfront"]
        upd = Dot(g.ax.c2p(up["usefulness"], up["safety"]), radius=0.08, color=GREY_B)
        upl = label(r"upfront auditing", font_size=18, color=GREY_B).next_to(upd, LEFT, buff=0.1)
        tl = label(r"T alone", font_size=18, color=TRUSTED).next_to(g.ax.c2p(0.02, 1.0), RIGHT, buff=0.1)
        tm = rows[0]
        r10 = next(r for r in rows if abs(r["defer"] - 0.1) < 1e-9)
        r20 = next(r for r in rows if abs(r["defer"] - 0.2) < 1e-9)
        pub = VGroup(
            label(r"published, \ with real GPT-4 and GPT-3.5:", font_size=22, color=WHITE),
            label(r"upfront auditing: \ safety $15\%$", font_size=20, color=GREY_A),
            label(r"trusted monitoring: \ $62\%$ safe, \ $97\%$ useful", font_size=20, color=GREY_A),
            label(r"\ \dots deferring $10\%$ to T: \ $83\%$, \ $93\%$", font_size=20, color=GREY_A),
            label(r"untrusted monitoring: \ $79\%$, \ $96\%$", font_size=20, color=GREY_A),
            label(r"trusted editing ($20\%$): \ $92\%$, \ $94\%$", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.4, 0.9, 0])
        agent = history_card(2025, r"Ctrl-Z \ (Bhatt et al., April)", r"control for agents running shell commands: "
                             r"\ resampling suspicious steps cut attack success from $58\%$ to $7\%$, \ at a $5\%$ cost",
                             width=6.0, color=BLUE, font_size=19).move_to([3.4, -2.3, 0])
        tag = tagline(r"simulated curve; \ published numbers, \ Greenblatt et al.\ (2023)")
        with self.voiceover(
            "The blue team has one more move: defer to the trusted model. When code is suspicious, but not suspicious "
            "enough to audit, throw it away and use the weaker model's own solution. <bookmark mark='a'/> Each "
            f"threshold is a point on a frontier. Deferring the top ten percent raises safety from "
            f"{tm['safety'] * 100:.0f} to {r10['safety'] * 100:.0f} percent, at a cost of "
            f"{(1 - r10['usefulness']) * 100:.0f} percent of the useful work; the top twenty percent, to "
            f"{r20['safety'] * 100:.0f}. <bookmark mark='b'/> The real experiment, with GPT-4's own backdoors and "
            "GPT-3.5 as the monitor, found the same shape: sixty-two percent safe with monitoring alone, eighty-three "
            "deferring ten percent, ninety-two with the trusted model editing the suspicious code. "
            "<bookmark mark='c'/> Control has since moved to agents: in 2025, resampling an agent's suspicious steps "
            "cut the success of attacks in a system-administration benchmark from fifty-eight percent to seven. "
            "Control doesn't need the model to be aligned, only the protocol to be good."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), FadeIn(upd), FadeIn(upl))
            vo.wait_until("a")
            self.play(Create(fr), FadeIn(dots), FadeIn(tl), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in pub], lag_ratio=0.25))
            vo.wait_until("c")
            self.play(FadeIn(agent, shift=UP * 0.15))
        self.wait(0.4)
        self.clear_scene()
