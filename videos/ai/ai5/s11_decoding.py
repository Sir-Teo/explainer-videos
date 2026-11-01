from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.decoding_contract import comparison, judge_verdict
from videos.ai.ai5.common import DATA, MODEL, MONO, PART, curve, load, printable

TEMP = "#FF6B8B"  # the temperature dial
RULES = {"temp": TEMP, "topk": C.INTERVAL, "topp": C.BITS, "minp": "#7FD3FF"}
RULE_NAMES = {"temp": r"temperature", "topk": r"top-$k$", "topp": r"top-$p$", "minp": r"min-$p$"}
SPOKEN = {"temp": "temperature alone", "topk": "top-k", "topp": "top-p", "minp": "min-p"}


def softmax_T(z, T):
    a = (z - z.max()) / T
    p = np.exp(a)
    return p / p.sum()


def kept(p, kind, v):
    """How many tokens a truncation rule keeps from the distribution p."""
    s = np.sort(p)[::-1]
    if kind == "topk":
        return int(v)
    if kind == "topp":
        return int(np.searchsorted(np.cumsum(s), v) + 1)
    return int((s >= v * s[0]).sum())


def comparison_verdict(result, spoken):
    """Do not call an observed subset a comparison of all four rules."""
    at, best = result["at"], result["best"]
    if not at:
        return "No rule covers this target diversity; no interpolation or ranking is available here."
    scope = ("All four rules cover this target diversity." if result["all_rules"] else
             f"Only {len(at)} of the four rules cover this target diversity; the others are not ranked here.")
    if len(at) == 1:
        return f"At the target diversity, {scope} One value alone cannot establish a winner."
    if result["spread"] < 0.02:
        return f"At the target diversity, {scope} Their interpolated surprises differ by only {result['spread']:.3f} nats per character."
    return f"At the target diversity, {scope} Among the covered rules, {spoken[best]} has the lowest interpolated surprise, {at[best]:.3f} nats per character."



class Decoding(VoiceoverScene):
    def construct(self):
        self.card()
        self.temperature()
        self.truncate()
        self.experiment()

    def card(self):
        card = chapter_card(9, r"How a language model chooses", r"How adventurous should the next token be?", lit=(2019,),
                            part=PART)
        with self.voiceover("Chapter nine. How a language model chooses."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def temperature(self):
        d = load("temperature")
        z = np.asarray(d["logits"], float)
        top = [int(i) for i in d["top"]]
        toks = [t.strip() for t in d["top_tokens"]]
        for T in (0.5, 1.0, 2.0):
            assert np.allclose(softmax_T(z, T)[top], np.asarray(d[f"p{T}"]), atol=1e-6)
        n_vocab = len(z)
        Tt = ValueTracker(1.0)
        p1 = softmax_T(z, 1.0)[top]
        bars = LiveBars(p1, max_value=0.24, height=3.4, bar_width=0.62, gap=0.22, colors=MODEL,
                        label_mobs=[data_text(t, font=MONO, font_size=22, color=GREY_A) for t in toks])
        bars.place(-1.9, x=-2.4)
        for i, lab in enumerate(bars.labels):  # every other word one line lower, so long ones don't collide
            if i % 2:
                lab.shift(DOWN * 0.32)
        for i, tr in enumerate(bars.trackers):
            tr.add_updater(lambda m, i=i: m.set_value(float(softmax_T(z, Tt.get_value())[top[i]])))
        prompt = data_text(d["prompt"] + " …", font="DejaVu Serif", font_size=26, color=WHITE).to_edge(UP, buff=0.4)
        prompt.set_x(-2.0)
        sub = label(r"GPT-2's ten favourite next tokens, \ out of $50{,}257$", font_size=24, color=GREY_A)
        sub.next_to(prompt, DOWN, buff=0.2).align_to(prompt, LEFT)
        colors = {r"T": TEMP, r"z_i": MODEL, r"z_j": MODEL}
        f = cmath(r"q_i \;\propto\; \exp\!\big(", r"z_i", r"\,/\,", r"T", r"\big)", colors=colors, font_size=44)
        f.move_to([4.4, 1.6, 0])
        tv = DecimalNumber(1.0, num_decimal_places=2, font_size=40, color=TEMP)
        tv.add_updater(lambda m: m.set_value(Tt.get_value()))
        trd = VGroup(MathTex(r"T =", font_size=40, color=TEMP), tv).arrange(RIGHT, buff=0.15).next_to(f, DOWN, buff=0.45)

        def ent():
            q = softmax_T(z, Tt.get_value())
            q = q[q > 0]
            return float(-(q * np.log2(q)).sum())

        hv = DecimalNumber(ent(), num_decimal_places=1, font_size=34, color=C.SURPRISE)
        hv.add_updater(lambda m: m.set_value(ent()))
        hrd = VGroup(label(r"entropy:", font_size=30), hv, label(r"bits", font_size=30)).arrange(RIGHT, buff=0.15)
        hrd.next_to(trd, DOWN, buff=0.3)
        rv = DecimalNumber(100 * (1 - p1.sum()), num_decimal_places=0, font_size=30, color=GREY_A, unit=r"\%")
        rv.add_updater(lambda m: m.set_value(100 * (1 - softmax_T(z, Tt.get_value())[top].sum())))
        rest = VGroup(label(rf"the other ${n_vocab - 10:,}$:".replace(",", "{,}"), font_size=26, color=GREY_A), rv)
        rest.arrange(RIGHT, buff=0.15).next_to(hrd, DOWN, buff=0.3)
        with self.voiceover(
            "A language model ends every step with a distribution over its vocabulary, and decoding picks from it. "
            "<bookmark mark='a'/> Here's GPT-2's distribution for the token after: Spade sat down in the armchair, "
            f"and. Its favourite gets only {100 * p1[0]:.0f} percent. <bookmark mark='b'/> The first dial is "
            "temperature: divide the scores by T before the softmax, the Gibbs distribution of chapter six."
        ) as vo:
            self.play(FadeIn(prompt), FadeIn(sub))
            vo.wait_until("a")
            self.add(*bars.trackers)  # their updaters follow the temperature
            self.play(FadeIn(bars), FadeIn(rest))
            vo.wait_until("b")
            self.play(Write(f), FadeIn(trd), FadeIn(hrd))
        with self.voiceover(
            "Turn it down, below one, and the distribution sharpens toward the favourites. <bookmark mark='a'/> Turn "
            "it up, and it flattens, until any token at all might come next. <bookmark mark='b'/> The entropy follows "
            f"the dial: {d['H0.5']:.1f} bits at a half, {d['H1.0']:.1f} at one, {d['H2.0']:.1f} at two."
        ) as vo:
            self.play(Tt.animate.set_value(0.5), run_time=2.5)
            vo.wait_until("a")
            self.play(Tt.animate.set_value(2.0), run_time=3.0)
            vo.wait_until("b")
            self.play(Tt.animate.set_value(1.0), run_time=1.5)
        for tr in bars.trackers:
            tr.clear_updaters()
        for m in (tv, hv, rv):
            m.clear_updaters()
        bars.freeze()
        self.wait(0.2)
        self.clear_scene()
        # what comes out
        samples = d["samples"]
        rows = VGroup()
        for T, name in (("0.0", r"$T \to 0$: \ always the favourite"), ("0.5", r"$T = 0.5$"), ("1.0", r"$T = 1$"),
                        ("2.0", r"$T = 2$")):
            tag = label(name, font_size=28, color=TEMP)
            words = ("… " + printable(samples[T])).split()
            lines, cur = [], ""
            for w in words:  # wrap at 12.6 units
                trial = (cur + " " + w).strip()
                if cur and data_text(trial, font="DejaVu Serif", font_size=22).width > 12.6:
                    lines.append(cur)
                    cur = w
                else:
                    cur = trial
            lines.append(cur)
            txt = VGroup(*[data_text(l_, font="DejaVu Serif", font_size=22, color=WHITE) for l_ in lines])
            txt.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            rows.add(VGroup(tag, txt).arrange(DOWN, aligned_edge=LEFT, buff=0.12))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.36).move_to(DOWN * 0.3)
        ph = data_text(d["prompt"], font="DejaVu Serif", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here's what comes out. <bookmark mark='a'/> Always taking the favourite is safe and flat. "
            "<bookmark mark='b'/> At a half, still sensible. <bookmark mark='c'/> At one, sampling the model's own "
            "distribution, it's stranger and more varied. <bookmark mark='d'/> At two, it falls apart: the tail of "
            "fifty thousand unlikely tokens, each tiny, together wins too often."
        ) as vo:
            self.play(FadeIn(ph))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k], shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def truncate(self):
        d = load("temperature")
        ctx = []
        for zk, pk in (("logits", "prompt"), ("logits2", "prompt2")):
            z = np.asarray(d[zk], float)
            p = softmax_T(z, 1.0)
            ctx.append((np.sort(p)[::-1], str(d[pk])))
        N = 40
        panels, cuts, counts = VGroup(), [], []
        rule = ValueTracker(0.5)  # top-p's p
        for j, (s, prompt) in enumerate(ctx):
            ax = Axes(x_range=[0, N, 10], y_range=[0, 1, 0.5], x_length=5.8, y_length=3.2, tips=False,
                      axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.4 + 6.8 * j, -0.4, 0])
            hmax = 0.25 if j == 0 else 1.0
            bars = VGroup(*[Rectangle(width=5.8 / N * 0.8, height=max(3.2 * min(v / hmax, 1.0), 0.004), stroke_width=0,
                                      fill_color=MODEL, fill_opacity=0.85).move_to(ax.c2p(i + 0.5, 0), aligned_edge=DOWN)
                            for i, v in enumerate(s[:N])])
            cum = curve(ax, np.arange(N + 1), np.concatenate([[0], np.cumsum(s[:N])]), color=C.BITS, stroke_width=2.5)
            pt = data_text(prompt + " …", font="DejaVu Serif", font_size=20, color=WHITE).next_to(ax, UP, buff=0.55)
            if pt.width > 6.2:
                pt.width = 6.2
            sc = label(rf"bars: \ the {N} likeliest tokens, \ largest ${100 * s[0]:.0f}\%$", font_size=18, color=GREY_A)
            sc.next_to(ax, UP, buff=0.12)
            cl = label(r"running total", font_size=18, color=C.BITS).next_to(ax.c2p(N, float(np.cumsum(s[:N])[-1])), DOWN, buff=0.12).shift(LEFT * 0.7)
            panels.add(VGroup(ax, bars, cum, pt, sc, cl))

            def cutline(ax=ax, s=s):
                k = kept(s, "topp", rule.get_value())
                x = min(k, N)
                return VGroup(DashedLine(ax.c2p(x, 0), ax.c2p(x, 1.05), color=C.BITS, stroke_width=3),
                              label(rf"keeps ${k:,}$".replace(",", "{,}"), font_size=22, color=C.BITS)
                              .next_to(ax.c2p(x, 1.05), DL if x > 0.7 * N else UP, buff=0.08))

            cuts.append(always_redraw(cutline))
        pv = DecimalNumber(0.5, num_decimal_places=2, font_size=36, color=C.BITS)
        pv.add_updater(lambda m: m.set_value(rule.get_value()))
        pl = VGroup(label(r"top-$p$, \ $p =$", font_size=32, color=C.BITS), pv).arrange(RIGHT, buff=0.15).to_edge(UP, buff=0.35)
        rules = VGroup(
            label(r"top-$k$: \ keep the $k$ likeliest \ (Fan et al., 2018)", font_size=22, color=RULES["topk"]),
            label(r"top-$p$, \ nucleus: \ the fewest whose total reaches $p$ \ (Holtzman et al., 2020)", font_size=22,
                  color=RULES["topp"]),
            label(r"min-$p$: \ keep those at least $p_{\min}$ times the likeliest \ (Nguyen et al., 2024)", font_size=22,
                  color=RULES["minp"])).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_edge(DOWN, buff=0.3)
        s0, s1 = ctx[0][0], ctx[1][0]
        k09 = (kept(s0, "topp", 0.9), kept(s1, "topp", 0.9))
        m01 = (kept(s0, "minp", 0.1), kept(s1, "minp", 0.1))
        with self.voiceover(
            "Temperature reshapes the distribution, but the long tail of unlikely tokens is always there. The other "
            "dials cut it off. <bookmark mark='a'/> Two real moments for GPT-2: an open one, where the favourite has "
            f"{100 * s0[0]:.0f} percent, and a nearly certain one, where it has {100 * s1[0]:.0f}. <bookmark "
            "mark='b'/> Top-k keeps a fixed number of tokens: too many in the second case, too few in the first. "
            "<bookmark mark='c'/> Top-p, nucleus sampling, keeps the fewest tokens whose probabilities add up to p, so "
            f"the cut adapts: at nine tenths it keeps {k09[0]:,} tokens in the open case and {k09[1]} in the certain "
            "one. <bookmark mark='d'/> Min-p keeps every token at least a fraction as likely as the favourite: at a "
            f"tenth, {m01[0]} and {m01[1]}."
        ) as vo:
            self.play(FadeIn(panels[0][:3]), FadeIn(panels[0][3:]), FadeIn(panels[1]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(rules[0]))
            vo.wait_until("c")
            self.play(FadeIn(rules[1]), FadeIn(pl), FadeIn(cuts[0]), FadeIn(cuts[1]))
            self.play(rule.animate.set_value(0.95), run_time=3.0, rate_func=linear)
            self.play(rule.animate.set_value(0.9), run_time=0.8)
            vo.wait_until("d")
            self.play(FadeIn(rules[2]))
        for m in cuts + [pv]:
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def experiment(self):
        d = load("decoding")
        kinds, vals = [str(k) for k in d["kinds"]], [float(v) for v in d["values"]]
        human, greedy = d["human"], d["greedy0.0"]
        hn = float(human["nll"])
        n_settings = len(d["settings"])
        n_prompts, n_samples = int(d["prompt_count"]), int(d["stochastic_samples"])
        pts = {k: sorted([(float(d[s]["div"]), float(d[s]["nll"]), v) for s, kk, v in zip(d["settings"], kinds, vals)
                          if kk == k]) for k in RULES}
        # Show actual finite coordinates, with no clipping to an old measured run.
        summary = comparison([(k, d[key]) for key, k in zip(d["settings"], kinds) if k in RULES], RULES)
        xlo = max(0.0, math.floor(min(0.85, *(a for P in pts.values() for a, _, _ in P)) * 10) / 10 - 0.02)
        xhi = min(1.02, math.ceil(max(0.85, *(a for P in pts.values() for a, _, _ in P)) * 10) / 10 + 0.02)
        ylo = max(0.0, math.floor(min(hn, float(greedy["nll"]), *(b for P in pts.values() for _, b, _ in P)) * 4) / 4 - 0.05)
        yhi = math.ceil(max(hn, float(greedy["nll"]), *(b for P in pts.values() for _, b, _ in P)) * 4) / 4 + 0.1
        ax = Axes(x_range=[xlo, xhi, 0.1], y_range=[ylo, yhi, 0.25], x_length=7.0, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-2.0, -0.4, 0])
        xt = VGroup(*[MathTex(f"{v:.1f}", font_size=22, color=GREY_B).next_to(ax.c2p(v, ylo), DOWN, buff=0.1) for v in np.arange(math.ceil(xlo * 10) / 10, xhi + 1e-8, 0.1)])
        yt = VGroup(*[MathTex(f"{v:.2f}", font_size=22, color=GREY_B).next_to(ax.c2p(xlo, v), LEFT, buff=0.1) for v in np.linspace(ylo, yhi, 4)])
        xl = label(r"diversity: \ distinct token pairs across $8$ sampled continuations", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"GPT-2's surprise at the text \ (nats per character; \ lower: likelier)", font_size=22,
                   color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        hline = DashedLine(ax.c2p(xlo, hn), ax.c2p(xhi, hn), color=WHITE, stroke_width=2.5)
        hl = label(rf"the novels' own text: \ ${hn:.2f}$", font_size=20, color=WHITE).next_to(ax.c2p(xlo, hn), UR, buff=0.08)
        lines = VGroup()
        for k, P in pts.items():
            P_ = [(a, b) for a, b, _ in P]
            lines.add(VGroup(VMobject(color=RULES[k], stroke_width=3).set_points_as_corners([ax.c2p(a, b) for a, b in P_]),
                             *[Dot(ax.c2p(a, b), radius=0.06, color=RULES[k]) for a, b in P_]))
        leg = VGroup(*[label(RULE_NAMES[k], font_size=22, color=RULES[k]) for k in RULES]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        leg.next_to(ax, RIGHT, buff=0.25).align_to(ax, UP)
        # quality at a common diversity, for each rule
        dstar = 0.85
        at = summary["at"]
        vline = DashedLine(ax.c2p(dstar, ylo), ax.c2p(dstar, yhi), color=GREY_B, stroke_width=1.5)
        tbl = VGroup(label(rf"at diversity ${dstar}$:", font_size=20, color=GREY_A),
                     *[label(rf"{RULE_NAMES[k]}: \ ${at[k]:.3f}$", font_size=20, color=RULES[k]) for k in at])
        tbl.arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        rep_g = float(greedy["rep"])
        rep_s = max(float(d[s]["rep"]) for s, k in zip(d["settings"], kinds) if k != "greedy")
        mean_se = float(np.mean([np.std(d[s_]["nll_prompt"], ddof=1) / math.sqrt(len(d[s_]["nll_prompt"]))
                            for s_ in d["settings"]]))
        sel = note(rf"mean standard error of setting means: ${mean_se:.2f}$ nats/character \ (not passage SD or CI)", font_size=20).to_edge(DOWN, buff=0.15)
        gl = label(rf"greedy: \ surprise ${float(greedy['nll']):.2f}$, \\ but ${100 * rep_g:.0f}\%$ of its 4-token runs repeat",
                   font_size=20, color=TEMP).next_to(tbl, DOWN, buff=0.35).align_to(tbl, LEFT)
        # Rank only settings actually observed at the target; never extrapolate.
        v1 = comparison_verdict(summary, SPOKEN)
        gn = float(greedy["nll"])
        g_judge = judge_verdict(gn, [float(d[key]["nll"]) for key, k in zip(d["settings"], kinds) if k != "greedy"])
        tp = [(v, float(d[s]["nll"])) for s, k, v in zip(d["settings"], kinds, vals) if k == "temp"]
        tp.sort()
        Th = (float(np.interp(hn, [b for _, b in tp], [a for a, _ in tp]))
              if all(tp[i][1] < tp[i+1][1] for i in range(len(tp)-1)) and tp[0][1] <= hn <= tp[-1][1] else None)
        mono = all(np.corrcoef([a for a, _, _ in P], [b for _, b, _ in P])[0, 1] > 0.5 for P in pts.values() if len(P) > 2)
        v0 = ("In this run, higher diversity tends to accompany higher surprise within each rule." if mono else
              "The rules do not all show the same predictability-diversity trend in this run.")
        v2 = (f"Human prose sits between: as surprising to the judge as our model's text at a temperature of about "
              f"{Th:.1f}." if Th is not None else "")
        with self.voiceover(
            "Which rule writes best? We tested them on the series' own small model, trained on the thirty novels: "
            f"{n_prompts} held-out passages, {n_samples} sampled continuations per passage for each stochastic "
            f"setting, and one greedy continuation per passage: {n_settings} settings total. A larger model, GPT-2, "
            f"scores separately tokenized continuations in nats per continuation character. <bookmark mark='a'/> {v0} <bookmark mark='b'/> "
            f"{v1} <bookmark mark='c'/> {g_judge}; {100 * rep_g:.0f} percent of "
            f"its four-token runs repeat, against at most {100 * rep_s:.1f} percent for any sampled setting. "
            f"{v2} Likelihood alone does not measure text quality."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), Create(hline), FadeIn(hl))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3), FadeIn(leg), run_time=2.5)
            vo.wait_until("a")
            self.play(*[Indicate(l_, scale_factor=1.0) for l_ in lines], run_time=1.2)
            vo.wait_until("b")
            self.play(Create(vline), FadeIn(tbl), FadeIn(sel))
            vo.wait_until("c")
            self.play(FadeIn(gl))
        self.wait(0.3)
        self.clear_scene()
        self.samples_(d)

    def samples_(self, d):
        rows = VGroup()
        picks = [("greedy0.0", r"greedy", TEMP), ("temp1.0", r"temperature $1$", TEMP), ("topp0.9", r"top-$p$ $0.9$",
                                                                                         RULES["topp"]),
                 ("minp0.1", r"min-$p$ $0.1$", RULES["minp"])]
        for key, name, col in picks:
            txt = printable(str(d[key]["ex_prompt"][0]))
            words = txt.split()
            lines, cur = [], ""
            for w in words:
                trial = (cur + " " + w).strip()
                if cur and data_text(trial, font="DejaVu Serif", font_size=20).width > 12.4:
                    lines.append(cur)
                    cur = w
                else:
                    cur = trial
            lines.append(cur)
            body = VGroup(*[data_text(l_, font="DejaVu Serif", font_size=20, color=WHITE) for l_ in lines[:2]])
            body.arrange(DOWN, aligned_edge=LEFT, buff=0.06)
            rows.add(VGroup(label(name, font_size=22, color=col), body).arrange(DOWN, aligned_edge=LEFT, buff=0.08))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 0.35)
        tail_ = printable(str(d["prompt3"]))[-90:]
        tail_ = tail_[tail_.find(" ") + 1:] if " " in tail_ else tail_
        ph = data_text("… " + tail_ + " …", font="DejaVu Serif", font_size=22, color=GREY_A)
        ph.to_edge(UP, buff=0.4)
        if ph.width > 12.6:
            ph.width = 12.6
        tag = note(r"the series' novels model, \ one of its continuations under each rule").to_edge(DOWN, buff=0.2)
        loops = float(d["greedy0.0"]["rep"]) > 0
        g_line = ("In this run, greedy decoding repeats some four-token sequences." if loops else
                  "In this run, greedy decoding has no repeated four-token sequences.")
        with self.voiceover(
            "Here is one passage, continued four ways. <bookmark mark='a'/> " + g_line + " <bookmark mark='b'/> Pure "
            "sampling uses the untruncated distribution. <bookmark mark='c'/> The other examples restrict its tail. Min-p, proposed in 2024 "
            "to allow higher temperatures, was challenged by a 2025 re-analysis that found its evidence weaker than "
            "reported. Part nineteen adds the other half of decoding: constraining what may be written at all."
        ) as vo:
            self.play(FadeIn(ph), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
        self.wait(0.3)
        self.clear_scene()
