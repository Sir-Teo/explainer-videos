from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai28.common import CHAIN, DIRECT, KLC, LEN, PART, PASS, POLICY, RIGHT_C, VOTE, WRONG_C, load


class TestTime(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_ways()
        self.s1()
        self.budget()
        self.bon_kl()
        self.bon_plot()

    def card(self):
        card = chapter_card(10, r"Thinking at answer time", r"Think longer, or think more often?", lit=(2024, 2025),
                            part=PART)
        with self.voiceover("Chapter ten. Thinking at answer time."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def two_ways(self):
        def chain(n, col, w=0.34):
            return VGroup(*[RoundedRectangle(width=w, height=0.3, corner_radius=0.05, stroke_width=1.5, stroke_color=col,
                                             fill_color=col, fill_opacity=0.25) for _ in range(n)]).arrange(RIGHT, buff=0.05)

        par = VGroup(*[chain(4, VOTE) for _ in range(5)]).arrange(DOWN, buff=0.12).move_to([-3.6, 0.0, 0])
        seq = chain(20, CHAIN, 0.28).move_to([3.2, 0.0, 0])
        if seq.width > 6.0:
            seq.width = 6.0
        pl = label(r"parallel: \ many tries, \ then pick \\ (vote, \ best-of-$N$, \ a checker)", font_size=24, color=VOTE)
        pl.next_to(par, UP, buff=0.4)
        sl = label(r"sequential: \ one longer chain \\ (re-check, \ revise, \ go on)", font_size=24, color=CHAIN)
        sl.next_to(seq, UP, buff=0.4)
        eq = label(r"the same $20$ tokens", font_size=22, color=GREY_A).to_edge(DOWN, buff=1.2)
        sch = note(r"schematic").to_corner(DR, buff=0.3)
        hc = history_card(2024, r"C.~Snell et al., \ Berkeley and Google DeepMind", r"choose the strategy per question: "
                          r"\ $4\times$ more efficient than best-of-$N$; \ a small model plus test-time compute can beat "
                          r"a $14\times$ larger one, \ on questions it can sometimes solve", width=8.6,
                          color=POLICY).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "There are two ways to spend more computation once the question is asked. <bookmark mark='a'/> In "
            "parallel: sample many answers, and pick one, by a vote, a grader, or a checker. <bookmark mark='b'/> Or "
            "in sequence: one longer chain that re-checks, revises and goes on. <bookmark mark='c'/> Which is better? "
            "In 2024, Charlie Snell and colleagues at Berkeley and Google DeepMind found that it depends on the "
            "question: easy ones gain from revising, hard ones from searching wider. Choosing per question beat "
            "best-of-N four times over, and a small model given test-time compute could beat one fourteen times "
            "larger, on questions it could sometimes solve."
        ) as vo:
            self.play(FadeIn(sch))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_, shift=RIGHT * 0.1) for c_ in par], lag_ratio=0.15), FadeIn(pl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.05) for t in seq], lag_ratio=0.05), FadeIn(sl))
            self.play(FadeIn(eq))
            vo.wait_until("c")
            self.play(FadeOut(eq), FadeIn(hc, shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def s1(self):
        trace = VGroup(label(r"\dots so the answer is 34.", font_size=26, color=GREY_A),
                       label(r"\textbf{Wait}", font_size=30, color=LEN),
                       label(r", let me check the second step again \dots", font_size=26, color=GREY_A)).arrange(RIGHT, buff=0.1)
        trace.move_to(UP * 0.6)
        sch = note(r"illustrative").next_to(trace, DOWN, buff=0.2)
        hc = history_card(2025, r"N.~Muennighoff et al., \ Stanford: \ \textit{s1: Simple test-time scaling}",
                          r"fine-tune on $1{,}000$ worked questions; \ to think longer, append ``Wait'' when it tries to "
                          r"stop; \ to think less, cut it off. \ AIME 2024: \ $50\% \to 57\%$", width=8.6,
                          color=LEN).move_to(UP * 2.2)
        dials = VGroup(label(r"budget forcing: \ a cap, \ and a nudge", font_size=26, color=LEN),
                       label(r"beat o1-preview on competition maths \ by up to $27\%$", font_size=24, color=GREY_A))
        dials.arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "The sequential dial can be very simple. In January 2025, Niklas Muennighoff and colleagues at Stanford "
            "fine-tuned a model on just a thousand worked questions, and then controlled its thinking at answer time. "
            "<bookmark mark='a'/> To make it think longer, when it tried to stop they appended one word: wait. The "
            "model went back over its work, and sometimes fixed a mistake. To make it think less, they cut it off and made it answer. "
            "<bookmark mark='b'/> With more thinking forced, AIME scores rose from 50 to 57 percent, and the model "
            "beat o1-preview on competition maths by up to twenty-seven percent. They called it budget forcing."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.15))
            vo.wait_until("a")
            self.play(FadeIn(trace[0]), FadeIn(sch))
            self.play(FadeIn(trace[1], scale=1.4))
            self.play(FadeIn(trace[2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_, shift=UP * 0.1) for d_ in dials], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def budget(self):
        b = load("think_budget")
        n = int(b["n"])
        res = {}
        for name in ("sft", "rl"):
            res[name] = (np.asarray(b[f"{name}_seq_tokens"]), np.asarray(b[f"{name}_seq"]),
                         np.asarray(b[f"{name}_vote_tokens"]), np.asarray(b[f"{name}_vote"]))
        tmax = int(max(max(r_[0].max(), r_[2].max()) for r_ in res.values()))
        g = axes([0, tmax], [0, 1], x_length=7.2, y_length=4.2, xlabel=r"tokens written per question",
                 ylabel=rf"right, \ ${n}$-digit lists", xticks=[0, tmax // 2, tmax], yticks=[0, 0.5, 1],
                 yfmt=lambda v: rf"{int(100 * v)}\%", center=[-1.4, -0.3, 0])
        cols = {("sft", "seq"): CHAIN, ("sft", "vote"): VOTE, ("rl", "seq"): POLICY, ("rl", "vote"): C.SURPRISE}
        lines, dots = {}, {}
        for name, (st, sa, vt, va) in res.items():
            for kind, xs, ys in (("seq", st, sa), ("vote", vt, va)):
                col = cols[(name, kind)]
                lines[(name, kind)] = curve(g.ax, xs, ys, col, 3.5 if name == "sft" else 3)
                dots[(name, kind)] = VGroup(*[Dot(g.ax.c2p(x, y), radius=0.045, color=col) for x, y in zip(xs, ys)])
        lg = legend([(CHAIN, r"think at most $m$ steps, \ then answer"), (VOTE, r"vote over $N$ answers at once"),
                     (POLICY, r"after RL: \ think at most $m$"), (C.SURPRISE, r"after RL: \ vote")], font_size=18)
        lg.next_to(g, RIGHT, buff=0.3).shift(UP * 0.9)
        if lg.get_right()[0] > 6.9:
            lg.shift(LEFT * (lg.get_right()[0] - 6.9))
        tag = note(rf"computed: \ ${int(b['nq'])}$ lists of ${n}$ digits; \ the model before RL and after RL "
                   r"(no cost on thought)").to_corner(DR, buff=0.2)
        st, sa, vt, va = res["sft"]
        full = float(sa[-1])
        at0 = float(sa[0])
        v_best = float(va.max())
        # at the token count of the full chain, how does the vote do?
        t_full = int(st[-1])
        v_at = float(np.interp(t_full, vt, va))
        if full > v_best + 0.05:
            verdict = (f"Thinking all {n} steps reaches {100 * full:.0f} percent with {t_full} tokens. A vote over "
                       f"answers given at once, at the same budget, manages {100 * v_at:.0f}, and with every token we "
                       f"allowed, {100 * v_best:.0f}. On a problem that is a chain of small steps, the chain wins: votes "
                       "can't add up digits that no single try added correctly.")
        else:
            verdict = (f"Thinking all {n} steps reaches {100 * full:.0f} percent with {t_full} tokens, and a vote over "
                       f"answers given at once reaches {100 * v_best:.0f} with the tokens we allowed.")
        rs, ra = res["rl"][1], res["rl"][3]
        mono = bool(np.all(np.diff(sa) > -0.03))
        if mono:
            first = (f"With no thought at all it gets {n}-digit lists right {100 * at0:.0f} percent of the time; each "
                     "extra step of thought buys more.")
        else:
            first = (f"With no thought at all it gets {n}-digit lists right {100 * at0:.0f} percent of the time, and "
                     f"{100 * full:.0f} with the whole chain, though not every extra step helps.")
        if rs[-1] > full + 0.02:
            after = (f"After reinforcement learning, thinking fully reaches {100 * rs[-1]:.0f} percent. Training and "
                     "test-time compute are two ways of buying the same thing.")
        else:
            after = (f"After reinforcement learning, thinking fully reaches {100 * rs[-1]:.0f} percent: what RL changed "
                     "is mostly the choice to think, not how well it adds.")
        with self.voiceover(
            "Our adding model can be given a budget too. Make it think, and force it to answer after at most m steps, "
            f"the way s1 cuts a model off. <bookmark mark='a'/> {first} <bookmark mark='b'/> The parallel "
            f"alternative: answer at once N times, and vote. <bookmark mark='c'/> {verdict} <bookmark mark='d'/> "
            f"{after}"
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lines[("sft", "seq")]), FadeIn(dots[("sft", "seq")]), FadeIn(lg[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(lines[("sft", "vote")]), FadeIn(dots[("sft", "vote")]), FadeIn(lg[1]), run_time=2.0)
            vo.wait_until("d")
            self.play(Create(lines[("rl", "seq")]), FadeIn(dots[("rl", "seq")]), FadeIn(lg[2]),
                      Create(lines[("rl", "vote")]), FadeIn(dots[("rl", "vote")]), FadeIn(lg[3]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bon_kl(self):
        colors = {r"p": RIGHT_C, r"q": WRONG_C, r"N": PASS}
        rows = [
            cmath(r"P(\text{best-of-}N \text{ is right})", r"=", r"1 - (1 - p)^N", font_size=34),
            cmath(r"\pi_N(y)", r"=", r"\begin{cases} \pi(y)\, \frac{1 - q}{p} & y \text{ right} \\ \pi(y)\, "
                  r"\frac{q}{1 - p} & y \text{ wrong} \end{cases}, \qquad q = (1 - p)^N", font_size=32),
            cmath(r"\mathrm{KL}(\pi_N \,\|\, \pi)", r"=", r"(1 - q) \log \frac{1 - q}{p} + q \log \frac{q}{1 - p}",
                  font_size=34),
            cmath(r"\mathrm{KL}(\pi_N \,\|\, \pi)", r"\xrightarrow{\ N \to \infty\ }", r"\log \frac{1}{p}\ \ \le\ \ "
                  r"\log N - \frac{N - 1}{N}", font_size=34),
        ]
        rows[2][2].set_color(KLC)
        whys = [why(r"draw $N$, \ keep a right one if there is one"),
                why(r"which right answer: \ in proportion to $\pi$"),
                why(r"the KL between two coins: \ right with $1 - q$, \ or with $p$"),
                why(r"bounded, \ however large $N$; \ Part 27's formula is an upper bound")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.4, buff=0.5, edge=6.9)
        cite_ = cite(r"A.~Beirami et al., \textit{Theoretical guarantees on the best-of-$n$ alignment policy} (2024)",
                     corner=DL)
        with self.voiceover(
            "The simplest parallel strategy with a checker is best-of-N: draw N answers and keep a right one. Part 27 "
            "showed that best-of-N moves a model log N minus N minus one over N nats away from where it started, when "
            "the reward has no ties. A checker's reward is all ties: right or wrong. So let's redo it. "
            "<bookmark mark='a'/> If one try is right with probability p, best-of-N is right with probability one "
            "minus one minus p to the N. <bookmark mark='b'/> Given that, which right answer it returns is in "
            "proportion to the model's own probabilities; the same for wrong ones. <bookmark mark='c'/> So the KL "
            "is just the divergence between two coins: one right with probability one minus q, the other with p. "
            "<bookmark mark='d'/> As N grows it levels off at log one over p, however many answers you draw, far "
            "below Part 27's formula, which in general is only an upper bound, as Ahmad Beirami and colleagues "
            "showed in 2024."
        ) as vo:
            self.play(FadeIn(cite_))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bon_plot(self):
        d = load("bon")
        Ns = [int(n) for n in d["Ns"]]
        lN = np.log2(Ns)
        kl, bound, acc = np.asarray(d["kl"]), np.asarray(d["bound"]), np.asarray(d["acc"])
        top = math.ceil(max(bound.max(), kl.max()))
        g = axes([0, lN[-1]], [0, top], x_length=5.6, y_length=3.6, xlabel=r"$N$", ylabel=r"KL from the model, \ nats",
                 xticks=list(lN[::2]), xfmt=lambda x: f"{int(2 ** x)}", yticks=[0, top], center=[-3.4, -0.4, 0])
        cb = curve(g.ax, lN, bound, GREY_B, 3)
        ck = curve(g.ax, lN, kl, KLC, 4)
        lb = label(r"$\log N - \frac{N-1}{N}$", font_size=20, color=GREY_B).next_to(g.ax.c2p(lN[-1], bound[-1]), UP, buff=0.1)
        lb.shift(LEFT * 0.6)
        lk = label(r"exact, \ with a checker", font_size=20, color=KLC).next_to(g.ax.c2p(lN[-1], kl[-1]), DOWN, buff=0.15)
        lk.shift(LEFT * 0.8)
        h = axes([0, lN[-1]], [0, 1], x_length=4.6, y_length=3.6, xlabel=r"$N$", ylabel=r"right",
                 xticks=list(lN[::2]), xfmt=lambda x: f"{int(2 ** x)}", yticks=[0, 0.5, 1],
                 yfmt=lambda v: rf"{int(100 * v)}\%", center=[3.6, -0.4, 0])
        ca = curve(h.ax, lN, acc, PASS, 4)
        r = load("rl")
        rl1 = float(r["after"])
        rline = DashedLine(h.ax.c2p(0, rl1), h.ax.c2p(lN[-1], rl1), color=POLICY, dash_length=0.08)
        rl_ = label(r"one try, \ after RL", font_size=18, color=POLICY).next_to(rline, DOWN, buff=0.08).align_to(rline, RIGHT)
        Nmatch = next((n for n, a in zip(Ns, acc) if a >= rl1), None)
        tag = note(r"computed: \ the addition model before RL, \ $200$ questions, \ exact").to_corner(DR, buff=0.2)
        if Nmatch:
            match = (f"best-of-N needs about {Nmatch} tries to match what one try of the model after reinforcement "
                     "learning gets right. RL moves into a single try what used to need many. o1's numbers had the same "
                     "shape: 74 percent with one try, 93 when a learned scorer picked from a thousand.")
        else:
            match = ("even best-of-N with every try we allowed falls short of one try of the model after reinforcement "
                     "learning.")
        with self.voiceover(
            "On our addition model, exactly. <bookmark mark='a'/> The KL of best-of-N with a checker levels off at "
            f"{kl[-1]:.2f} nats, while the formula for untied rewards would reach {bound[-1]:.2f} at {Ns[-1]} tries. "
            f"<bookmark mark='b'/> And accuracy: {match}"
        ) as vo:
            self.play(FadeIn(g), FadeIn(h), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(cb), FadeIn(lb), Create(ck), FadeIn(lk), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(ca), Create(rline), FadeIn(rl_), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
