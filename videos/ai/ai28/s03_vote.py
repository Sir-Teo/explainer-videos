from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai28.common import CHAIN, DIRECT, MONO, PART, PASS, RIGHT_C, VOTE, WRONG_C, chip, load


class Vote(VoiceoverScene):
    def construct(self):
        self.card()
        self.testbed()
        self.history()
        self.many()
        self.why_vote()
        self.curves()

    def card(self):
        card = chapter_card(2, r"Many chains, one vote", r"If one chain of thought can go wrong, why not ask for many?",
                            lit=(2022,), part=PART)
        with self.voiceover("Chapter two. Many chains, one vote."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def testbed(self):
        s = load("think_sft")
        fmt = VGroup(
            VGroup(*[chip(str(v), 0.42, GREY_B, 20) for v in (4, 7, 2, 9)]),
            chip("=", 0.42, GREY_C, 20, fill=0), chip("think", 0.42, CHAIN, 16, width=0.92, fill=0.25),
            VGroup(*[chip(str(v), 0.42, CHAIN, 20, width=0.52, fill=0.18) for v in (4, 11, 13, 22)]),
            chip("ans", 0.42, DIRECT, 16, width=0.76, fill=0.25), chip("22", 0.42, WHITE, 20, width=0.52, fill=0.3))
        for g_ in (fmt[0], fmt[3]):
            g_.arrange(RIGHT, buff=0.06)
        fmt.arrange(RIGHT, buff=0.1)
        bq = Brace(fmt[0], UP, color=GREY_B)
        lq = label(r"a list of $2$ to $9$ digits", font_size=20, color=GREY_B).next_to(bq, UP, buff=0.08)
        bt = Brace(fmt[3], UP, color=CHAIN)
        lt = label(r"thinking: \ the running total", font_size=20, color=CHAIN).next_to(bt, UP, buff=0.08)
        ba = Brace(fmt[5], DOWN, color=WHITE)
        la = label(r"the sum", font_size=20).next_to(ba, DOWN, buff=0.08)
        direct = VGroup(VGroup(*[chip(str(v), 0.42, GREY_B, 20) for v in (4, 7, 2, 9)]).arrange(RIGHT, buff=0.06),
                        chip("=", 0.42, GREY_C, 20, fill=0), chip("ans", 0.42, DIRECT, 16, width=0.76, fill=0.25),
                        chip("22", 0.42, WHITE, 20, width=0.52, fill=0.3)).arrange(RIGHT, buff=0.1)
        dl = label(r"or answer at once", font_size=20, color=DIRECT).next_to(direct, LEFT, buff=0.3)
        top = VGroup(fmt, bq, lq, bt, lt, ba, la).move_to([0.6, 2.0, 0])
        direct.next_to(top, DOWN, buff=0.35).align_to(fmt, LEFT)
        dl.next_to(direct, LEFT, buff=0.3)
        sch = note(r"schematic").next_to(direct, RIGHT, buff=0.4)
        ns = list(s["ns"])
        acc_d, acc_t, p_t = s["acc_direct"], s["acc_think"], s["p_think_free"]
        g = axes([ns[0] - 0.5, ns[-1] + 0.5], [0, 1], x_length=6.0, y_length=2.4, xlabel=r"digits in the list",
                 ylabel=r"right, \ one sample", xticks=ns, yticks=[0, 0.5, 1], yfmt=lambda v: rf"{int(100 * v)}\%",
                 center=[-2.6, -2.05, 0])
        cd, ct = curve(g.ax, ns, acc_d, DIRECT, 3.5), curve(g.ax, ns, acc_t, CHAIN, 3.5)
        dots = VGroup(*[Dot(g.ax.c2p(x, y), radius=0.05, color=c) for xs, ys, c in ((ns, acc_d, DIRECT), (ns, acc_t, CHAIN))
                        for x, y in zip(xs, ys)])
        lg = legend([(CHAIN, r"made to think"), (DIRECT, r"made to answer at once")], font_size=20)
        lg.next_to(g, RIGHT, buff=0.4).shift(UP * 0.3)
        free = label(rf"left to choose, \ it thinks ${100 * np.mean(p_t):.0f}\%$ of the time", font_size=20,
                     color=GREY_A).next_to(lg, DOWN, buff=0.3).align_to(lg, LEFT)
        tag = note(rf"computed: \ a $2$-layer transformer, \ ${int(s['sft_steps']):,}$ supervised steps".replace(",", "{,}"))
        tag.to_corner(DR, buff=0.2)
        with self.voiceover(
            "For the next chapters we need a model that can choose to think. Here is ours, trained on this computer. "
            "<bookmark mark='a'/> The question is a list of two to nine digits; the answer is their sum. "
            "<bookmark mark='b'/> The model may think first: it writes a think token, then the running total after "
            "each digit, then the answer. <bookmark mark='c'/> Or it may answer at once. Its training showed it both, "
            "and chains cut short, so it can stop thinking at any point. <bookmark mark='d'/> Sampled at temperature "
            f"one, made to answer at once, it gets two digits right {100 * acc_d[0]:.0f} percent of the time, and "
            f"nine digits {100 * acc_d[-1]:.0f}. Made to think, {100 * acc_t[0]:.0f} and {100 * acc_t[-1]:.0f}. "
            "Each step of thought is a small sum, but small sums still go wrong sometimes, and one wrong step spoils "
            "the chain."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(fmt[0]), FadeIn(bq), FadeIn(lq), FadeIn(fmt[1]))
            vo.wait_until("b")
            self.play(FadeIn(fmt[2:]), FadeIn(bt), FadeIn(lt), FadeIn(ba), FadeIn(la), FadeIn(sch))
            vo.wait_until("c")
            self.play(FadeIn(direct), FadeIn(dl))
            vo.wait_until("d")
            self.play(FadeIn(g), Create(ct), Create(cd), FadeIn(dots), FadeIn(lg), run_time=2.0)
            self.play(FadeIn(free))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        hc = history_card(2022, r"X.~Wang et al., \ Google: \ \textit{Self-consistency improves chain of thought "
                          r"reasoning}", r"sample many chains of thought, \ keep the answer they most often reach; \ "
                          r"on grade-school maths, \ $+17.9$ points over a single chain", width=8.4,
                          color=VOTE).move_to(UP * 1.6)
        idea = VGroup(
            label(r"different routes to the same answer: \ evidence it is right", font_size=26, color=RIGHT_C),
            label(r"errors scatter: \ wrong chains rarely agree on the same wrong answer", font_size=26,
                  color=WRONG_C),
            label(r"no checker needed: \ only the answers", font_size=26, color=VOTE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 1.3)
        with self.voiceover(
            "In March 2022, two months after chain-of-thought prompting, Xuezhi Wang and colleagues at Google asked: "
            "if one chain can go wrong, why not sample several and take a vote? They called it self-consistency, "
            "and on grade-school maths it added eighteen points over a single chain. <bookmark mark='a'/> The "
            "intuition: different routes that reach the same answer are evidence for it. <bookmark mark='b'/> "
            "Mistakes, on the other hand, tend to scatter: wrong chains rarely agree on the same wrong answer. "
            "<bookmark mark='c'/> And it needs no checker at all, only the answers."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(idea[k], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def many(self):
        v = load("think_vote")
        d, A, St, truth = np.asarray(v["ex_d"]), np.asarray(v["ex_answers"]), np.asarray(v["ex_steps"]), int(v["ex_truth"])
        digits = [int(x) for x in d if x < 10]
        run = np.cumsum(digits)
        q = VGroup(*[chip(str(x), 0.42, GREY_B, 20) for x in digits]).arrange(RIGHT, buff=0.06).to_edge(UP, buff=0.4)
        ql = label(rf"a {len(digits)}-digit list", font_size=22, color=GREY_A).next_to(q, LEFT, buff=0.3)
        rows = VGroup()
        for j in range(8):
            st = [int(x) for x in St[j] if x >= 0]
            ok = [s_ == run[i] if i < len(run) else False for i, s_ in enumerate(st)]
            r_ = VGroup(*[chip(str(x), 0.36, RIGHT_C if o else WRONG_C, 16, width=0.46, fill=0.18) for x, o in zip(st, ok)])
            r_.arrange(RIGHT, buff=0.04)
            a_ = chip(str(int(A[j])) if A[j] >= 0 else "?", 0.36, RIGHT_C if A[j] == truth else WRONG_C, 16,
                      width=0.5, fill=0.35)
            rows.add(VGroup(r_, MathTex(r"\to", font_size=24, color=GREY_C), a_).arrange(RIGHT, buff=0.12))
        for r_ in rows:
            r_[2].set_x(-1.0)
            r_[1].next_to(r_[2], LEFT, buff=0.12)
            r_[0].next_to(r_[1], LEFT, buff=0.12)
        rows.arrange(DOWN, buff=0.13).move_to([-3.6, -0.55, 0])
        for r_ in rows:
            r_[2].set_x(-0.9)
            r_[1].next_to(r_[2], LEFT, buff=0.12)
            r_[0].next_to(r_[1], LEFT, buff=0.12)
        rl = label(r"$8$ of its $64$ chains \ (steps checked)", font_size=20, color=CHAIN).next_to(rows, UP, buff=0.2)
        # the 64 answers, tallied
        vals, cnt = np.unique(A[A >= 0], return_counts=True)
        order = np.argsort(vals)
        vals, cnt = vals[order], cnt[order]
        H = 3.4 / cnt.max()
        bw = min(0.42, 5.2 / len(vals))
        bars = VGroup(*[Rectangle(width=bw * 0.85, height=max(H * c_, 0.02), stroke_width=0,
                                  fill_color=RIGHT_C if v_ == truth else WRONG_C, fill_opacity=0.85)
                        for v_, c_ in zip(vals, cnt)]).arrange(RIGHT, buff=bw * 0.15, aligned_edge=DOWN)
        bars.move_to([3.6, -0.6, 0]).align_to([0, -2.4, 0], DOWN)
        bl = VGroup(*[data_text(str(int(v_)), font=MONO, font_size=14, color=GREY_B).next_to(b, DOWN, buff=0.06)
                      for v_, b in zip(vals, bars)])
        if len(vals) > 10:
            for i, t in enumerate(bl):
                if vals[i] != truth and cnt[i] < cnt.max():
                    t.set_opacity(0)
        hl = label(r"all $64$ answers", font_size=22, color=GREY_A).next_to(bars, UP, buff=0.25)
        top = int(vals[np.argmax(cnt)])
        win = SurroundingRectangle(bars[int(np.argmax(cnt))], color=VOTE, buff=0.06, stroke_width=3)
        wl = label(rf"the vote: \ ${top}$", font_size=24, color=VOTE).next_to(win, UP, buff=0.1)
        p_right = float(np.mean(A == truth))
        n_ok = int(np.sum(A[:8] == truth))
        n_wrong_vals = int(len(np.unique(A[(A >= 0) & (A != truth)])))
        some = (f"{n_ok} of these eight end on the right sum. The others slipped somewhere, and a slip carries "
                "through to the end: every later total is off by the same amount." if n_ok < 8 else
                "All eight of these end on the right sum.")
        scatter = (f"the wrong ones scatter over {n_wrong_vals} different values." if n_wrong_vals > 3 else
                   f"the wrong ones fall on just {n_wrong_vals} values.")
        if top == truth:
            verdict = f"So the most common answer, the vote, is {top}: right."
        else:
            verdict = f"Here the most common answer is {top}, and the vote is wrong."
        with self.voiceover(
            f"Here is one {len(digits)}-digit list, and eight of the sixty-four chains our model wrote for it, made "
            "to think. Each step is coloured by whether it matches the true running total. "
            f"<bookmark mark='a'/> {some} <bookmark mark='b'/> Now tally all sixty-four answers. "
            f"{100 * p_right:.0f} percent of them are the right sum, {truth}; {scatter} <bookmark mark='c'/> {verdict}"
        ) as vo:
            self.play(FadeIn(q), FadeIn(ql), FadeIn(rl))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in rows], lag_ratio=0.15), run_time=2.5)
            vo.wait_until("a")
            self.play(*[Indicate(r_[2], scale_factor=1.3) for r_ in rows if True], run_time=1.0)
            vo.wait_until("b")
            self.play(FadeIn(hl), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), FadeIn(bl),
                      run_time=2.0)
            vo.wait_until("c")
            self.play(Create(win), FadeIn(wl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why_vote(self):
        colors = {r"y^*": RIGHT_C, r"p^*": RIGHT_C, r"y": WRONG_C, r"p_y": WRONG_C, r"k": VOTE}
        rows = [
            cmath(r"\text{the vote is right}", r"\iff", r"N_{y^*} > N_{y}\ \text{ for every wrong } y", font_size=32),
            cmath(r"N_{y^*} - N_{y}", r"=", r"\sum_{i=1}^{k} \big(\mathbf 1[Y_i = y^*] - \mathbf 1[Y_i = y]\big),\ \ "
                  r"\text{mean } k\,(p^* - p_y)", font_size=32),
            cmath(r"P\big(N_{y^*} \le N_y\big)", r"\le", r"e^{-k\,(p^* - p_y)^2 / 2}", font_size=34),
            cmath(r"\text{vote}_k \text{ right}", r"\xrightarrow{\ k \to \infty\ }",
                  r"\begin{cases} 1 & p^* > \max_y p_y \\ 0 & \text{some } p_y > p^* \end{cases}", font_size=32),
        ]
        whys = [why(r"$N$: \ how often each answer appears in $k$ samples"),
                why(r"$k$ independent draws, \ each in $\{-1, 0, 1\}$"),
                why(r"Hoeffding \ (Part 26): \ a range of $2$"),
                why(r"a union bound over the wrong answers")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.6, buff=0.5, edge=6.9)
        res = label(r"voting can only amplify \ what the model already prefers", font_size=28, color=VOTE)
        res.to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "When does voting work? Call the right answer y star, and its probability p star. <bookmark mark='a'/> "
            "The vote is right when the right answer appears more often than every wrong one. <bookmark mark='a2'/> "
            "Compare it with one wrong answer y: the difference in counts is a sum of k independent draws, each plus one, zero, or minus "
            "one, with mean k times p star minus p y. <bookmark mark='b'/> By Hoeffding's inequality, the chance "
            "that the wrong answer catches up falls exponentially in k. <bookmark mark='c'/> So as the votes grow, "
            "the vote is right with probability one if the right answer is the model's single most likely answer, "
            "and with probability zero if some wrong answer is more likely. <bookmark mark='d'/> Voting can only "
            "amplify what the model already prefers. It cannot rescue a question where the model's favourite answer "
            "is wrong."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("a2")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        v = load("think_vote")
        ks = [int(k) for k in v["ks"]]
        lk = np.log2(ks)
        tv, tp, dv = np.asarray(v["think_vote"]), np.asarray(v["think_pass"]), np.asarray(v["direct_vote"])
        lim = float(v["think_mode_right"])
        lo = float(np.floor(min(tv.min(), dv.min()) * 10) / 10)
        g = axes([0, lk[-1]], [lo, 1.0], x_length=7.2, y_length=4.4, xlabel=r"samples per question, \ $k$",
                 ylabel=r"questions answered right", xticks=list(lk), xfmt=lambda x: f"{int(2 ** x)}",
                 yticks=[lo, (lo + 1) / 2, 1.0], yfmt=lambda y: rf"{int(round(100 * y))}\%", center=[-1.6, -0.3, 0])
        ax = g.ax
        cp, cv, cdv = curve(ax, lk, tp, PASS, 4), curve(ax, lk, tv, VOTE, 4), curve(ax, lk, dv, DIRECT, 3)
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.05, color=c) for ys, c in ((tp, PASS), (tv, VOTE), (dv, DIRECT))
                        for x, y in zip(lk, ys)])
        limit = DashedLine(ax.c2p(0, lim), ax.c2p(lk[-1], lim), color=VOTE, dash_length=0.08, stroke_width=2)
        ll = label(rf"the limit: \ most frequent answer right \ (${100 * lim:.0f}\%$)", font_size=18, color=VOTE)
        ll.next_to(limit, DOWN, buff=0.08).align_to(limit, RIGHT)
        lg = legend([(PASS, r"any of $k$ right \ (needs a checker)"), (VOTE, r"vote over $k$ chains"),
                     (DIRECT, r"vote over $k$ answers given at once")], font_size=19)
        lg.next_to(g, RIGHT, buff=0.3).shift(UP * 1.0)
        if lg.get_right()[0] > 6.9:
            lg.shift(LEFT * (lg.get_right()[0] - 6.9))
        tag = note(r"computed: \ $300$ questions, \ $64$ samples each; \ subsets averaged").to_corner(DR, buff=0.2)
        dlim = float(v["direct_mode_right"])
        if dv[-1] < tv[-1] - 0.03:
            direct_said = (f"Voting over answers given at once reaches only {100 * dv[-1]:.0f}: for more of the "
                           "questions, the model's favourite answer at once is wrong, and voting cannot fix that. The "
                           "chains make the right answer the most likely one, and then the vote amplifies it.")
        else:
            direct_said = (f"Voting over answers given at once does about as well here, {100 * dv[-1]:.0f} percent: "
                           "on this task the model's favourite answer is often right either way.")
        with self.voiceover(
            "Here it is on three hundred questions. <bookmark mark='a'/> One chain is right "
            f"{100 * tv[0]:.0f} percent of the time. Voting over {ks[-1]} chains: {100 * tv[-1]:.0f} percent. "
            f"<bookmark mark='b'/> And the derivation predicted where it would level off: the share of questions "
            f"whose most frequent answer is right, {100 * lim:.0f} percent. <bookmark mark='c'/> If something could "
            f"check the answers, any of {ks[-1]} chains being right would count: {100 * tp[-1]:.0f} percent. The gap "
            "between the two curves is what a checker is worth. <bookmark mark='d'/> " + direct_said
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(cv), FadeIn(lg[1]), FadeIn(dots[len(ks):2 * len(ks)]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(limit), FadeIn(ll))
            vo.wait_until("c")
            self.play(Create(cp), FadeIn(lg[0]), FadeIn(dots[:len(ks)]), run_time=2.0)
            vo.wait_until("d")
            self.play(Create(cdv), FadeIn(lg[2]), FadeIn(dots[2 * len(ks):]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
