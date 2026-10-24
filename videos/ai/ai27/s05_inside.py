from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai27.common import (ASSIST, GOLD, PART, PENALTY, PROXY, REWARD, bubble, line_clip, load, node_box,
                                   said, ticks)
from videos.ai.ai27.compute import (CONCISE, NEGATIVE, PER_WORD, POSITIVE, REPEAT_FREE, REPEAT_W, WORD, _demean,
                                    gold_parts)

# gold's terms: one colour each, and how the narration names them
TERM_COL = [C.ENTROPY, C.LENGTH, C.LAMBDA, C.PATHOLOGY]
TERM_TEX = [r"mood", r"length", r"repetition", r"too short"]
TERM_SAY = {"mood": "mood", "length": "length", "repetition": "repetition", "too short": "lines that are too short"}


def kind(w: str) -> str:
    return "pos" if w in POSITIVE else "neg" if w in NEGATIVE else ""


KIND_COL = {"pos": REWARD, "neg": PENALTY, "": GREY_B}


class Inside(VoiceoverScene):
    def construct(self):
        self.d = load("inside")
        self.card()
        self.opening()
        self.scatter()
        self.terms()
        self.length()
        self.words()
        self.disagree()
        self.select()

    def card(self):
        card = chapter_card(5, r"Inside our reward model", r"What did it actually learn?", lit=(2022,), part=PART)
        with self.voiceover("Chapter five. Inside our reward model."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def opening(self):
        d = self.d
        acc = float(load("rm")["acc"][-1])
        text, top = d["text"], d["topic"]
        g, s = np.asarray(d["gold"]), np.asarray(d["large_score"])
        n, per, T = len(text), int(d["per_topic"]), len(set(top))
        nw = np.asarray(d["words"])
        sea = [i for i in range(n) if top[i] == top[0] and 6 <= nw[i] <= 14] or [0]
        i0 = sea[0]
        q = said(f"Write a line about the {top[i0]}.", "user", chars=40, font_size=20).move_to([-3.7, 3.0, 0])
        model = node_box(r"our fine-tuned model", ASSIST, font_size=22).move_to([-3.7, 1.95, 0])
        line = said(text[i0], chars=34, font_size=18, max_lines=2).move_to([-3.7, 0.75, 0])
        rmb = node_box(r"reward model", PROXY, font_size=22).move_to([-5.3, -0.75, 0])
        gb = node_box(r"gold", GOLD, font_size=22).move_to([-2.1, -0.75, 0])
        arr = lambda a, b, c=GREY_B: Arrow(a, b, buff=0.08, color=c, stroke_width=2.5, max_tip_length_to_length_ratio=0.2)
        a1, a2 = arr(q.get_bottom(), model.get_top()), arr(model.get_bottom(), line.get_top())
        a3, a4 = arr(line.get_bottom(), rmb.get_top(), PROXY), arr(line.get_bottom(), gb.get_top(), GOLD)
        ch4 = label(rf"chapter 4: \ right on ${100 * acc:.0f}\%$ \\ of held-out comparisons", font_size=20,
                    color=GREY_A).next_to(rmb, DOWN, buff=0.25)
        hid = label(r"hidden from \\ every model", font_size=20, color=GREY_A).next_to(gb, DOWN, buff=0.25)
        sv = label(rf"score ${s[i0]:+.2f}$", font_size=24, color=PROXY).next_to(ch4, DOWN, buff=0.3)
        gv = label(rf"gold ${g[i0]:+.2f}$", font_size=24, color=GOLD).next_to(hid, DOWN, buff=0.3).match_y(sv)
        # a few more lines, each with both scores
        pick = []
        for t in dict.fromkeys(top):
            js = [i for i in range(n) if top[i] == t and len(text[i]) <= 62 and nw[i] >= 4 and i != i0]
            if js:
                pick.append(js[0])
            if len(pick) == 5:
                break
        head = VGroup(label(r"a line", font_size=20, color=GREY_A).move_to([2.0, 3.0, 0]),
                      label(r"reward \\ model", font_size=20, color=PROXY).move_to([4.9, 3.0, 0]),
                      label(r"gold", font_size=20, color=GOLD).move_to([6.2, 3.0, 0]))
        rows = VGroup()
        for k, i in enumerate(pick):
            y = 2.05 - 0.95 * k
            rows.add(VGroup(said(text[i], chars=28, font_size=16, max_lines=2).move_to([2.0, y, 0]),
                            MathTex(rf"{s[i]:+.2f}", font_size=26, color=PROXY).move_to([4.9, y, 0]),
                            MathTex(rf"{g[i]:+.2f}", font_size=26, color=GOLD).move_to([6.2, y, 0])))
        tag = note(rf"computed: \ ${n}$ new lines from our fine-tuned model, \ ${per}$ for each of ${T}$ questions; \ "
                   r"none was in any comparison", font_size=20).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Chapter four measured our reward model from the outside: on comparisons it had never seen, it agreed "
            f"with the simulated people {100 * acc:.0f} percent of the time. A real lab can't do much more; it can't "
            "see inside its labellers' heads. <bookmark mark='a'/> We can, because we wrote gold. So let's open the "
            f"reward model up. Our fine-tuned model writes {n:d} new lines, {per:d} for each of the {T:d} questions, "
            "none of them in any comparison. <bookmark mark='b'/> The reward model scores every line, and so does "
            "gold. "
            "Here are a few, side by side."
        ) as vo:
            # centred while it is alone on screen; it moves aside when gold and the table arrive
            first = VGroup(q, a1, model, a2, line, a3, rmb, ch4)
            first.shift(RIGHT * 3.7)
            self.play(FadeIn(q), GrowArrow(a1), FadeIn(model), GrowArrow(a2), FadeIn(line))
            self.play(GrowArrow(a3), FadeIn(rmb), FadeIn(ch4))
            vo.wait_until("a")
            self.play(first.animate.shift(LEFT * 3.7), run_time=1.0)
            self.play(GrowArrow(a4), FadeIn(gb), FadeIn(hid), FadeIn(tag))
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_[0], shift=LEFT * 0.1) for r_ in rows], lag_ratio=0.3),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(sv), FadeIn(gv))
            self.play(LaggedStart(*[FadeIn(VGroup(r_[1], r_[2])) for r_ in rows], lag_ratio=0.3), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def scatter(self):
        d = self.d
        top = d["topic"]
        g, s = np.asarray(d["gold"]), np.asarray(d["large_score"])
        gc, sc = _demean(g, top), _demean(s, top)
        xlo, xhi = float(min(g.min(), gc.min())), float(max(g.max(), gc.max()))
        ylo, yhi = float(min(s.min(), sc.min())), float(max(s.max(), sc.max()))
        xp, yp = 0.05 * (xhi - xlo), 0.05 * (yhi - ylo)
        xlo, xhi, ylo, yhi = xlo - xp, xhi + xp, ylo - yp, yhi + yp
        gax = axes([xlo, xhi], [ylo, yhi], x_length=6.6, y_length=4.9, xlabel=r"gold",
                   ylabel=r"the reward model's score", xticks=ticks(xlo, xhi), yticks=ticks(ylo, yhi),
                   center=[-2.9, -0.35, 0])
        ax = gax.ax
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.03, color=PROXY, fill_opacity=0.7) for x, y in zip(g, s)])
        r_raw, r_in, slope = float(d["large_r_raw"]), float(d["large_r_within"]), float(d["large_slope"])
        agree, people = float(d["large_pair_agree"]), float(d["people_pair_agree"])
        tau = float(d["tau"])
        ideal = 1 / tau
        T = len(set(top))
        il = DashedLine(*line_clip(ax, ideal, xlo, xhi, ylo, yhi), color=GOLD, dash_length=0.08, stroke_width=3)
        fl = Line(*line_clip(ax, slope, xlo, xhi, ylo, yhi), color=PROXY, stroke_width=4)
        X = 1.9
        stats = VGroup(
            label(rf"correlation, \ all lines: \ ${r_raw:.2f}$", font_size=24),
            label(rf"each question's average taken out: \ ${r_in:.2f}$", font_size=24),
            VGroup(label(rf"slope: \ ${slope:.1f}$", font_size=24, color=PROXY),
                   label(rf"a perfect learner of our people: \ $1/\tau = {ideal:g}$", font_size=22, color=GOLD))
            .arrange(DOWN, aligned_edge=LEFT, buff=0.12),
            VGroup(label(rf"pairs it orders as gold does: \ ${100 * agree:.0f}\%$", font_size=24),
                   label(rf"one simulated person: \ ${100 * people:.0f}\%$", font_size=22, color=GREY_A))
            .arrange(DOWN, aligned_edge=LEFT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        stats.move_to([X, 0.4, 0], aligned_edge=LEFT)
        if stats.get_right()[0] > 6.9:
            stats.scale((6.9 - X) / stats.width, about_edge=LEFT)
        tag = note(rf"computed: \ ${len(g)}$ lines, \ ${int(d['n_pairs']):,}$ pairs".replace(",", "{,}"))
        tag.to_corner(DR, buff=0.2)
        if r_in > r_raw + 0.02:
            tight = f"The cloud tightens: the correlation rises to {r_in:.2f}."
        elif r_in < r_raw - 0.02:
            tight = f"The correlation falls, to {r_in:.2f}: across questions, the shifts happened to line up with gold."
        else:
            tight = f"The correlation hardly changes: {r_in:.2f}. The shifts were small next to the spread."
        if slope < 0.75 * ideal:
            slope_said = (f"Ours rises only {slope:.1f} for each point of gold: it is less sure than the people "
                          "are, as a model fitted to a few thousand noisy comparisons tends to be.")
        elif slope > 1.25 * ideal:
            slope_said = f"Ours rises {slope:.1f} for each point of gold: it is more confident than the people are."
        else:
            slope_said = f"Ours rises {slope:.1f} for each point of gold, close to that."
        if agree > people + 0.01:
            judge = (f"One simulated person, judging the same pairs, would agree with gold {100 * people:.0f} percent "
                     "of the time. The reward model is a better judge of gold than any one of the people it learned "
                     "from: it pools thousands of their noisy judgments.")
        elif agree < people - 0.01:
            judge = (f"One simulated person would agree with gold {100 * people:.0f} percent of the time: the reward "
                     "model is a worse judge of gold than one of the people it learned from.")
        else:
            judge = f"About as often as one simulated person would: {100 * people:.0f} percent."
        with self.voiceover(
            "Each dot is one line: across, what gold thinks of it; up, the reward model's score. "
            f"<bookmark mark='a'/> They go together, with a correlation of {r_raw:.2f}. <bookmark mark='b'/> But "
            "remember chapter four: the scores are only defined up to a shift for each question, so comparing lines "
            f"across questions mixes in {T:d} arbitrary shifts. Take each question's average out of both. {tight} "
            f"<bookmark mark='c'/> How steep should the cloud be? Our simulated people choose with a noise of {tau:g}, "
            f"so a reward model that learned them perfectly would score {ideal:g} times gold: the dashed line. "
            f"{slope_said} <bookmark mark='d'/> Over all {int(d['n_pairs']):,} pairs of lines to the same question "
            f"that gold doesn't tie, the reward model orders {100 * agree:.0f} percent as gold does. {judge}"
        ) as vo:
            self.play(FadeIn(gax), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(p_) for p_ in dots], lag_ratio=0.002), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(stats[0]))
            vo.wait_until("b")
            self.play(*[p_.animate.move_to(ax.c2p(x, y)) for p_, x, y in zip(dots, gc, sc)], run_time=2.5)
            self.play(FadeIn(stats[1]))
            vo.wait_until("c")
            self.play(Create(il), FadeIn(stats[2][1]))
            self.play(Create(fl), FadeIn(stats[2][0]))
            vo.wait_until("d")
            self.play(FadeIn(stats[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def terms(self):
        d = self.d
        slope = float(d["large_slope"])
        formula = cmath(r"\mathrm{gold}(y)", r"=", r"\tanh\frac{c - g}{2}", r"-",
                        rf"{PER_WORD:g}\,(n - {CONCISE:d})_+", r"-", rf"{REPEAT_W:g}\,(\rho - {REPEAT_FREE:g})_+",
                        font_size=36).move_to([0, 2.75, 0])
        for k, idx in enumerate((2, 4, 6)):
            formula[idx].set_color(TERM_COL[k])
        braces = VGroup(*[brace_note(formula[idx], t, color=TERM_COL[k], font_size=20)
                          for k, (idx, t) in enumerate(((2, r"mood: \ $c$ cheerful, $g$ gloomy words"),
                                                        (4, r"length: \ $n$ words"),
                                                        (6, r"repetition: \ $\rho$ repeated share")))])
        short = label(r"and $-1$ for a line of fewer than four words", font_size=22, color=TERM_COL[3])
        short.next_to(braces, DOWN, buff=0.2)
        names = list(d["part_names"])
        wl, ws = d["large_weights"], d["small_weights"]
        gold_w = [1.0, 1.0, 1.0, -1.0]
        live = [k for k in range(4) if wl[k] is not None]
        share_l = {k: wl[k] / gold_w[k] for k in live}
        share_s = {k: ws[k] / gold_w[k] for k in live if ws[k] is not None}
        vals = list(share_l.values()) + list(share_s.values()) + [0.0, 1.2]
        lo, hi = min(vals), max(vals)
        pad = 0.15 * (hi - lo)
        gax = axes([0, len(live)], [lo - pad if lo < 0 else 0, hi + pad], x_length=5.8, y_length=3.0,
                   ylabel=r"share of gold's weight it learned", yticks=[0, 1], center=[-3.1, -1.5, 0])
        ax = gax.ax
        one = DashedLine(ax.c2p(0, 1), ax.c2p(len(live), 1), color=GOLD, dash_length=0.08)
        onel = label(r"gold", font_size=20, color=GOLD).next_to(one, RIGHT, buff=0.1)
        zero = Line(ax.c2p(0, 0), ax.c2p(len(live), 0), color=GREY_C, stroke_width=1.5)
        ymin = ax.y_range[0]
        bars, small, labs = VGroup(), VGroup(), VGroup()
        for j, k in enumerate(live):
            for v, dx, op, dest in ((share_s.get(k), -0.17, 0.35, small), (share_l[k], 0.17, 0.9, bars)):
                if v is None:
                    continue
                b0, b1 = ax.c2p(j + 0.5 + dx, 0), ax.c2p(j + 0.5 + dx, v)
                dest.add(Rectangle(width=0.3, height=max(abs(b1[1] - b0[1]), 0.01), stroke_width=0,
                                   fill_color=TERM_COL[k], fill_opacity=op).move_to((b0 + b1) / 2))
            labs.add(label(TERM_TEX[k], font_size=20, color=TERM_COL[k]).next_to(ax.c2p(j + 0.5, ymin), DOWN,
                                                                                    buff=0.2))
        vtxt = VGroup(*[MathTex(rf"{share_l[k]:.2f}", font_size=22, color=TERM_COL[k]).next_to(
            bars[j], UP if share_l[k] >= 0 else DOWN, buff=0.08) for j, k in enumerate(live)])
        key = VGroup(label(r"faint: \ from $100$ comparisons", font_size=18, color=GREY_B),
                     label(r"bold: \ from all of them", font_size=18, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT,
                                                                                             buff=0.08)
        key.next_to(gax, RIGHT, buff=0.6).shift(UP * 0.9)
        r2 = float(d["large_r2"])
        r2l = label(rf"gold's terms explain ${100 * r2:.0f}\%$ \\ of its score's variation", font_size=24)
        r2l.next_to(key, DOWN, buff=0.5, aligned_edge=LEFT)
        tag = note(r"computed: \ least squares within each question, \ score in gold units (divided by its slope)",
                   font_size=18).to_corner(DR, buff=0.2)
        fit = cmath(r"\frac{\text{score}}{\text{slope}}", r"\approx", r"w_1\,\text{mood}", r"+",
                    r"w_2\,\text{length}", r"+", r"w_3\,\text{repetition}", r"-", r"w_4\,\text{too short}",
                    r"+\ \text{the question's own constant}", font_size=28)
        for k, idx in enumerate((2, 4, 6, 8)):
            fit[idx].set_color(TERM_COL[k])
        fit.move_to([0, 0.95, 0])
        if fit.width > 13.0:
            fit.scale_to_fit_width(13.0)
        hi_k = max(live, key=lambda k: share_l[k])
        lo_k = min(live, key=lambda k: share_l[k])
        better = sum(abs(share_l[k] - 1) < abs(share_s[k] - 1) for k in share_s)
        w_said = (f"It weighs {TERM_SAY[names[hi_k]]} most, at {share_l[hi_k]:.2f} of gold's weight, and "
                  f"{TERM_SAY[names[lo_k]]} least, at {share_l[lo_k]:.2f}.")
        if better == len(share_s):
            small_said = "The reward model trained on a hundred comparisons, faint, is further from gold on every term."
        elif better:
            small_said = (f"The one trained on a hundred comparisons, faint, is further from gold on {better:d} of the "
                          f"{len(share_s):d} terms.")
        else:
            small_said = "More comparisons didn't bring these weights any closer to gold's: the faint bars are as close."
        if r2 > 0.9:
            r2_said = (f"Gold's terms explain {100 * r2:.0f} percent of the variation in its score: almost everything "
                       "it learned is something gold cares about.")
        else:
            r2_said = (f"Gold's terms explain {100 * r2:.0f} percent of the variation in its score. The other "
                       f"{100 - 100 * r2:.0f} percent is something gold doesn't care about at all, whatever else it "
                       "picked up from a few thousand noisy comparisons.")
        with self.voiceover(
            "What has it learned? Gold is a sum of three terms: the mood of the words, a penalty for every word past "
            f"{CONCISE:d}, and a penalty for repeating words; and a line under four words is the worst there is. "
            "<bookmark mark='a'/> Fit the reward model's score, divided by its slope so it is in gold's units, as a "
            "sum of the same terms. If it had learned gold exactly, every weight would be one. "
            f"<bookmark mark='b'/> {w_said} <bookmark mark='b2'/> {small_said} <bookmark mark='c'/> {r2_said}"
        ) as vo:
            self.play(Write(formula), run_time=1.5)
            self.play(FadeIn(braces), FadeIn(short))
            vo.wait_until("a")
            self.play(FadeIn(fit, shift=DOWN * 0.1))
            self.play(FadeIn(gax), FadeIn(labs), Create(zero), Create(one), FadeIn(onel), FadeIn(key), FadeIn(tag))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in small], lag_ratio=0.15),
                      LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.15), run_time=2.0)
            self.play(FadeIn(vtxt))
            vo.wait_until("c")
            self.play(FadeIn(r2l))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def length(self):
        d = self.d
        top = d["topic"]
        g, s, nw = np.asarray(d["gold"]), np.asarray(d["large_score"]), np.asarray(d["words"])
        slope = float(d["large_slope"])
        gc, sc = _demean(g, top), _demean(s, top) / slope
        ok = nw >= 4
        edges = list(range(4, int(nw.max()) + 4, 3))
        bins = [(a, b) for a, b in zip(edges, edges[1:]) if np.sum(ok & (nw >= a) & (nw < b)) >= 8]
        cx = [float(np.mean(nw[ok & (nw >= a) & (nw < b)])) for a, b in bins]
        mg = [float(np.mean(gc[ok & (nw >= a) & (nw < b)])) for a, b in bins]
        ms = [float(np.mean(sc[ok & (nw >= a) & (nw < b)])) for a, b in bins]
        xmax = float(max(nw[ok].max(), 20)) + 1
        ylo, yhi = float(np.percentile(np.r_[gc[ok], sc[ok]], 1)), float(np.percentile(np.r_[gc[ok], sc[ok]], 99))
        ylo, yhi = min(ylo, min(mg + ms) - 0.1), max(yhi, max(mg + ms) + 0.1)
        gax = axes([3, xmax], [ylo, yhi], x_length=7.6, y_length=4.4, xlabel=r"words in the line",
                   ylabel=r"score against the question's average \ (gold units)",
                   xticks=[v for v in (4, CONCISE, 20, 30, 40) if v <= xmax], yticks=ticks(ylo, yhi, 3),
                   center=[-1.9, -0.3, 0])
        ax = gax.ax
        inside = ok & (sc > ylo) & (sc < yhi)
        cloud = VGroup(*[Dot(ax.c2p(x, y), radius=0.022, color=PROXY, fill_opacity=0.25)
                         for x, y in zip(nw[inside], sc[inside])])
        cg, cs = curve(ax, cx, mg, GOLD, 5), curve(ax, cx, ms, PROXY, 5)
        dg = VGroup(*[Dot(ax.c2p(x, y), radius=0.06, color=GOLD) for x, y in zip(cx, mg)])
        ds = VGroup(*[Dot(ax.c2p(x, y), radius=0.06, color=PROXY) for x, y in zip(cx, ms)])
        mark = DashedLine(ax.c2p(CONCISE, ylo), ax.c2p(CONCISE, yhi), color=GREY_B, dash_length=0.06)
        ml = label(rf"gold minds \\ past ${CONCISE:d}$ words", font_size=18, color=GREY_B)
        ml.next_to(ax.c2p(CONCISE, yhi), RIGHT, buff=0.1).shift(DOWN * 0.3)
        lg = legend([(GOLD, r"gold, \ averaged by length"), (PROXY, r"the reward model, \ in gold units"),
                     (PROXY, r"faint dots: \ each line's score")], font_size=20)
        lg[2][0].set_stroke(opacity=0.3)
        lg.next_to(gax, RIGHT, buff=0.35).shift(UP * 1.0)
        # past the free dozen words: how fast does each fall, per word? (straight lines through every such line)
        far = ok & (nw > CONCISE)
        fit = lambda y: float(np.polyfit(nw[far], y[far], 1)[0]) if far.sum() > 5 else 0.0
        kg, ks = fit(gc), fit(sc)
        rates = VGroup(label(rf"past ${CONCISE:d}$ words, per word:", font_size=22, color=GREY_A),
                       label(rf"gold \ ${kg:+.3f}$", font_size=24, color=GOLD),
                       label(rf"reward model \ ${ks:+.3f}$", font_size=24, color=PROXY)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).next_to(lg, DOWN, buff=0.5, aligned_edge=LEFT)
        tag = note(r"computed: \ each question's average taken out; \ averages over bins of three words")
        tag.to_corner(DR, buff=0.2)
        if kg < 0 and ks < 0 and abs(ks - kg) <= 0.35 * abs(kg):
            len_said = (f"It learned the length rule: past {CONCISE:d} words its score falls {-ks:.3f} a word, and "
                        f"gold's {-kg:.3f}.")
        elif kg < 0 and ks < kg:
            len_said = (f"It learned the length rule and then some: past {CONCISE:d} words its score falls "
                        f"{-ks:.3f} a word, faster than gold's {-kg:.3f}, as its large weight on length said.")
        elif kg < 0 and ks < 0:
            len_said = (f"It learned the direction but not the size: past {CONCISE:d} words its score falls "
                        f"{-ks:.3f} a word, and gold's {-kg:.3f}.")
        else:
            len_said = (f"It didn't learn the length rule: past {CONCISE:d} words gold falls {-kg:.3f} a word, and the "
                        f"reward model's score changes by {ks:+.3f}.")
        with self.voiceover(
            f"Here is length on its own. Gold doesn't mind a line up to {CONCISE:d} words; after that it takes off "
            f"{PER_WORD:g} a word. <bookmark mark='a'/> Averaged by length, with all its other terms mixed in, gold "
            "looks like this. <bookmark mark='b'/> And the reward model, in gold's units, like this. "
            f"<bookmark mark='c'/> {len_said}"
        ) as vo:
            self.play(FadeIn(gax), Create(mark), FadeIn(ml), FadeIn(tag))
            self.play(FadeIn(cloud), FadeIn(lg[2]), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(cg), FadeIn(dg), FadeIn(lg[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(cs), FadeIn(ds), FadeIn(lg[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rates))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def words(self):
        d = self.d
        ex = d.get("example")
        n_show = min(8, len(d["words_up"]), len(d["words_down"]))
        up, down = d["words_up"][:n_show], d["words_down"][:n_show]
        n_lines = sum(1 for w in np.asarray(d["words"]) if w >= 6)
        # one line, word by word: each word's chip, the reward model's change (bar) and gold's (mark) when it goes
        ex_grp = VGroup()
        if ex:
            effs = ex["effects"]
            # the line as one text, so the words share a baseline; each token's glyphs picked out by position
            toks = ex["text"].split()
            line_t = data_text(" ".join(toks), font="DejaVu Sans Mono", font_size=22, color=WHITE)
            if line_t.width > 12.6:
                line_t.width = 12.6
            line_t.move_to([0, 1.75, 0])
            starts = np.cumsum([0] + [len(t) for t in toks])
            if len(line_t) == starts[-1]:  # one glyph per non-space character
                chips = VGroup(*[line_t[starts[j]:starts[j + 1]] for j, _, _, _ in effs])
            else:
                chips = VGroup(*[data_text(t, font="DejaVu Sans Mono", font_size=20, color=WHITE)
                                 for _, t, _, _ in effs]).arrange(RIGHT, buff=0.22).move_to([0, 1.75, 0])
                line_t = chips
            m = max(max(abs(e[2]), abs(e[3])) for e in effs) or 1.0
            H = 1.3 / m
            base = Line([-6.6, 0.0, 0], [6.6, 0.0, 0], color=GREY_C, stroke_width=1.5)
            bars, marks = VGroup(), VGroup()
            for c_, (_, w, er, eg) in zip(chips, effs):
                x = c_.get_x()
                bars.add(Rectangle(width=min(0.34, c_.width), height=max(abs(er) * H, 0.01), stroke_width=0,
                                   fill_color=PROXY, fill_opacity=0.85).move_to([x, er * H / 2, 0]))
                marks.add(Line([x - 0.24, eg * H, 0], [x + 0.24, eg * H, 0], color=GOLD, stroke_width=5))
                col = KIND_COL[kind("".join(WORD.findall(w.lower())))]
                c_.set_color(col)
            exq = said(f"Write a line about the {ex['topic']}.", "user", chars=40, font_size=20).move_to([0, 2.8, 0])
            ex_lg = legend([(PROXY, r"the reward model's loss when the word goes"),
                            (GOLD, r"gold's, \ for the same deletion")], font_size=18).to_corner(DL, buff=0.3)
            ex_grp = VGroup(exq, line_t, base, bars, marks, ex_lg)
        # every line: the words that raise the score most, and lower it most; each column a zero line with the words
        # to its left, the bars and marks scaled so the largest reaches 1.9 either way
        rows_up, rows_down = VGroup(), VGroup()
        big = max(max(abs(r_[2]), abs(r_[3])) for r_ in up + down) or 1.0
        Wd = 1.9 / big
        y0, dy = 1.75, 0.55
        y_end = y0 - dy * (n_show - 1) - 0.3
        cols = ((rows_up, up, -2.4), (rows_down, down, 4.6))
        for rows, items, z in cols:
            for k, (w, cnt, er, eg, kd) in enumerate(items):
                y = y0 - dy * k
                wt = data_text(w, font="DejaVu Sans Mono", font_size=20, color=KIND_COL[kd])
                wt.move_to([z - 2.2, y, 0], aligned_edge=RIGHT)
                bar = Rectangle(width=max(abs(er) * Wd, 0.01), height=0.3, stroke_width=0, fill_color=PROXY,
                                fill_opacity=0.85).move_to([z + er * Wd / 2, y, 0])
                mk = Line([z + eg * Wd, y - 0.2, 0], [z + eg * Wd, y + 0.2, 0], color=GOLD, stroke_width=5)
                rows.add(VGroup(wt, bar, mk))
        axis_up = Line([-2.4, y0 + 0.35, 0], [-2.4, y_end, 0], color=GREY_C, stroke_width=1.5)
        axis_dn = Line([4.6, y0 + 0.35, 0], [4.6, y_end, 0], color=GREY_C, stroke_width=1.5)
        hu = label(r"raise its score most", font_size=24, color=REWARD).move_to([-3.2, 2.7, 0])
        hd = label(r"lower its score most", font_size=24, color=PENALTY).move_to([3.8, 2.7, 0])
        key = VGroup(label(r"green: \ on gold's cheerful list", font_size=18, color=REWARD),
                     label(r"red: \ on its gloomy list", font_size=18, color=PENALTY),
                     label(r"grey: \ on neither", font_size=18, color=GREY_B),
                     label(r"bar: \ reward model, \ mark: \ gold \ (gold units)", font_size=18, color=GREY_A))
        key.arrange(RIGHT, buff=0.45).to_edge(DOWN, buff=0.7)
        if key.width > 12.0:
            key.width = 12.0
        tag = note(rf"computed: \ every word deleted in turn from ${n_lines:d}$ lines; \ words seen at least "
                   rf"${int(d['min_count'])}$ times", font_size=18).to_corner(DR, buff=0.2)
        k_up = sum(1 for r_ in up if r_[4] == "pos")
        k_dn = sum(1 for r_ in down if r_[4] == "neg")
        if k_up + k_dn == 0:
            lists_said = ("Not one of them is on gold's lists: the words that move the reward model most are words "
                          "gold ignores.")
        elif k_up + k_dn >= n_show:
            lists_said = (f"Of the top {n_show:d}, gold's cheerful list holds {k_up:d}, and of the bottom {n_show:d}, "
                          f"its gloomy list holds {k_dn:d}: it has found gold's words.")
        elif k_dn == 0:
            lists_said = (f"Of the top {n_show:d}, gold's cheerful list holds only {k_up:d}, and its gloomy list holds "
                          f"none of the bottom {n_show:d}; the rest are words gold ignores.")
        elif k_up == 0:
            lists_said = (f"None of the top {n_show:d} is on gold's cheerful list, and of the bottom {n_show:d}, its "
                          f"gloomy list holds only {k_dn:d}; the rest are words gold ignores.")
        else:
            lists_said = (f"Of the top {n_show:d}, gold's cheerful list holds only {k_up:d}, and of the bottom "
                          f"{n_show:d}, its gloomy list holds {k_dn:d}; the rest are words gold ignores.")
        (_, pr, pg), (_, nr, ng) = d["class_pos"], d["class_neg"]
        word_r = float(d["word_r"])
        class_said = (f"Gold's own words, on average: a cheerful one moves the reward model's score by {pr:+.2f}, "
                      f"where it moves gold by {pg:+.2f}; a gloomy one moves it by {nr:+.2f}, where it moves gold by "
                      f"{ng:+.2f}. Over all {int(d['n_words'])} words the two agree with a correlation of {word_r:.2f}.")
        # how often each of gold's terms speaks in the data: lines with a listed word, pairs that differ in length
        texts, tops, nwords = d["text"], d["topic"], np.asarray(d["words"])
        share = float(np.mean([any(kind(w) for w in WORD.findall(x.lower())) for x in texts]))
        lterm = np.where(nwords >= 4, -PER_WORD * np.maximum(0, nwords - CONCISE), np.nan)
        diff = []
        for t in dict.fromkeys(tops):
            idx = [k for k in range(len(tops)) if tops[k] == t]
            diff += [lterm[i] != lterm[j] for a_, i in enumerate(idx) for j in idx[a_ + 1:]]
        len_share = float(np.mean(diff))
        if pr < 0.5 * pg and nr > 0.5 * ng:
            why_said = (f"Why so little? Only {100 * share:.0f} percent of the lines have a word from either of "
                        f"gold's lists, while {100 * len_share:.0f} percent of the pairs of lines differ in length: in "
                        "the comparisons it learned from, length speaks far more often than mood.")
        else:
            why_said = (f"{100 * share:.0f} percent of the lines have a word from one of gold's lists, enough for it "
                        "to learn their mood.")
        cls = VGroup(
            label(rf"gold's cheerful words: \ reward model ${pr:+.2f}$, \ gold ${pg:+.2f}$", font_size=22, color=REWARD),
            label(rf"gold's gloomy words: \ reward model ${nr:+.2f}$, \ gold ${ng:+.2f}$", font_size=22, color=PENALTY),
        ).arrange(RIGHT, buff=0.8).move_to(key)
        if cls.width > 13.0:
            cls.width = 13.0
        ex_topic = ex["topic"] if ex else d["topic"][0]
        with self.voiceover(
            "Which words does it listen to? Delete one word at a time and score the line again: the drop is that "
            f"word's worth to the reward model. <bookmark mark='a'/> Here is a line about the {ex_topic}, word by "
            "word. Orange bars are the reward model's change, in gold's units; yellow marks are gold's own change "
            "for the same deletion. <bookmark mark='b'/> Now every word in every line. These are the "
            f"{n_show:d} words that raise its score most, and the {n_show:d} that lower it most. "
            f"<bookmark mark='c'/> {lists_said} <bookmark mark='d'/> {class_said} <bookmark mark='e'/> {why_said}"
        ) as vo:
            if ex:
                self.play(FadeIn(exq), FadeIn(line_t), Create(base))
            vo.wait_until("a")
            if ex:
                self.play(LaggedStart(*[GrowFromEdge(b_, DOWN if b_.get_y() > 0 else UP) for b_ in bars],
                                      lag_ratio=0.1), FadeIn(ex_lg), run_time=2.0)
                self.play(LaggedStart(*[Create(m_) for m_ in marks], lag_ratio=0.1), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeOut(ex_grp))
            self.play(FadeIn(hu), FadeIn(hd), Create(axis_up), Create(axis_dn), FadeIn(key), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in rows_up], lag_ratio=0.1),
                      LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in rows_down], lag_ratio=0.1), run_time=2.5)
            vo.wait_until("c")
            hits = [Indicate(r_[0], color=REWARD) for r_, it in zip(rows_up, up) if it[4] == "pos"]
            hits += [Indicate(r_[0], color=PENALTY) for r_, it in zip(rows_down, down) if it[4] == "neg"]
            self.play(*(hits or [Indicate(VGroup(*[r_[0] for r_ in rows_up], *[r_[0] for r_ in rows_down]),
                                          color=GREY_A, scale_factor=1.05)]))
            vo.wait_until("d")
            self.play(FadeOut(key), FadeIn(cls, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def disagree(self):
        d = self.d
        per = int(d["per_topic"])
        top, text = d["topic"], d["text"]
        g = np.asarray(d["gold"])
        parts = {}
        for i, x in enumerate(text):
            p = gold_parts(x)
            parts[i] = (0.0, 0.0, 0.0, -1.0) if p is None else (*p, 0.0)
        P_ = np.array([parts[i] for i in range(len(text))])
        Pc = np.stack([_demean(P_[:, c], top) for c in range(4)], 1)
        index = {(t_, x): i for i, (t_, x) in enumerate(zip(top, text))}
        o, u = d["over"][0], d["under"][0]
        # which of gold's terms, against the question's average line, moves each line's gold most: down for the line
        # the reward model overrates, up for the one it underrates
        io, iu = index[(o["topic"], o["text"])], index[(u["topic"], u["text"])]
        ko, ku = int(np.argmin(Pc[io])), int(np.argmax(Pc[iu]))
        no, nu = len(WORD.findall(o["text"].lower())), len(WORD.findall(u["text"].lower()))
        if ko == 0:
            o_why = "Gold marks it down mainly for its gloomy words."
        elif ko == 1:
            o_why = f"Gold marks it down mainly for its length: {no:d} words."
        elif ko == 2:
            o_why = "Gold marks it down mainly for repeating itself."
        else:
            o_why = "Gold marks it down mainly for being too short to count."
        if ku == 0:
            u_why = "Gold likes it mainly for its cheerful words."
        elif ku == 1:
            u_why = f"Gold likes it mainly for being short: {nu:d} words."
        elif ku == 2:
            u_why = "Gold likes it mainly for not repeating itself."
        else:
            u_why = "Gold likes it mainly for being a whole line."

        def card(e, head, col):
            box = said(e["text"], chars=38, font_size=20, max_lines=4)
            q = said(f"Write a line about the {e['topic']}.", "user", chars=40, font_size=18)
            r1 = label(rf"reward model: \ ranks it ${e['rank_rm']}$ of ${per}$", font_size=24, color=PROXY)
            r2 = label(rf"gold: \ ranks it ${e['rank_gold']}$ of ${per}$ \ (gold ${e['gold']:+.2f}$)", font_size=24,
                       color=GOLD)
            h = label(head, font_size=28, color=col)
            return VGroup(h, q, box, r1, r2).arrange(DOWN, buff=0.22)

        left = card(o, r"the reward model overrates", PENALTY).move_to([-3.5, 0.6, 0])
        right = card(u, r"the reward model underrates", REWARD).move_to([3.5, 0.6, 0])
        for c_ in (left, right):
            if c_.width > 6.6:
                c_.width = 6.6
        ow = wrapped_label(o_why, 6.2, font_size=24, color=GREY_A).next_to(left, DOWN, buff=0.4)
        uw = wrapped_label(u_why, 6.2, font_size=24, color=GREY_A).next_to(right, DOWN, buff=0.4)
        tag = note(r"computed: \ the largest gaps between the two scores, each standardized within its question")
        tag.to_corner(DR, buff=0.2)
        with self.voiceover(
            "Where do the two disagree most? <bookmark mark='a'/> This line about the "
            f"{o['topic']} is the reward model's number {int(o['rank_rm'])} of the {per:d} for its question; gold "
            f"ranks it {int(o['rank_gold'])}. {o_why} <bookmark mark='b'/> And this line about the {u['topic']} is "
            f"the other way round: the reward model ranks it {int(u['rank_rm'])}, gold {int(u['rank_gold'])}. {u_why} "
            "<bookmark mark='c'/> These are the errors that matter, because an optimizer goes looking for them."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(left[0]), FadeIn(right[0]))
            vo.wait_until("a")
            self.play(FadeIn(left[1:], shift=UP * 0.15))
            self.play(FadeIn(ow))
            vo.wait_until("b")
            self.play(FadeIn(right[1:], shift=UP * 0.15))
            self.play(FadeIn(uw))
            vo.wait_until("c")
            self.play(Indicate(left[0], color=PENALTY), Indicate(right[0], color=REWARD))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def select(self):
        d = self.d
        top = d["topic"]
        g, s = np.asarray(d["gold"]), np.asarray(d["large_score"])
        gc = _demean(g, top)
        qs = list(dict.fromkeys(top))
        lo, hi = float(gc.min()), float(gc.max())
        pad = 0.08 * (hi - lo)
        gax = axes([0, len(qs)], [lo - pad, hi + pad], x_length=6.4, y_length=4.4,
                   xlabel=rf"the ${len(qs)}$ questions, \ ${int(d['per_topic'])}$ lines each",
                   ylabel=r"gold, \ against the question's average line", yticks=ticks(lo, hi, 3),
                   center=[-3.4, -0.3, 0])
        ax = gax.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(len(qs), 0), color=GREY_C, dash_length=0.06)
        dots, rings_rm, rings_g = VGroup(), VGroup(), VGroup()
        for j, t in enumerate(qs):
            idx = [i for i in range(len(top)) if top[i] == t]
            for i in idx:
                dots.add(Dot(ax.c2p(j + 0.5, gc[i]), radius=0.028, color=GREY_B, fill_opacity=0.7))
            fav = idx[int(np.argmax(s[idx]))]
            best = idx[int(np.argmax(g[idx]))]
            rings_rm.add(Circle(radius=0.09, color=PROXY, stroke_width=3).move_to(ax.c2p(j + 0.5, gc[fav])))
            rings_g.add(Circle(radius=0.13, color=GOLD, stroke_width=2.5).move_to(ax.c2p(j + 0.5, gc[best])))
        believed, actual = float(d["large_pick_believed"]), float(d["large_pick_gold"])
        best_v, same = float(d["gold_pick"]), float(d["large_pick_same"])
        X = 0.7
        nums = VGroup(
            label(r"each question's favourite line", font_size=24, color=GREY_A),
            label(rf"by the reward model, \ as it sees it: \ ${believed:+.2f}$", font_size=24, color=PROXY),
            label(rf"by the reward model, \ as gold sees it: \ ${actual:+.2f}$", font_size=24, color=GOLD),
            label(rf"gold's own favourite: \ ${best_v:+.2f}$", font_size=24, color=GOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([X, 1.4, 0], aligned_edge=LEFT)
        if nums.get_right()[0] > 6.9:
            nums.scale((6.9 - X) / nums.width, about_edge=LEFT)
        kinds = definition_card(r"Goodhart, \ four ways", VGroup(
            label(r"regressional: \ choose by a noisy measure, \ and you choose its noise too", font_size=22,
                  color=GREY_A),
            label(r"extremal: \ far from its data, \ the measure stops tracking", font_size=22, color=GREY_A),
            label(r"causal, \ adversarial: \ the other two", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14), width=6.1, font_size=24, color=PROXY,
            kind=r"Manheim \& Garrabrant, 2018")
        kinds.move_to([X, -1.85, 0], aligned_edge=LEFT)
        ring_key = VGroup(
            VGroup(Circle(radius=0.09, color=PROXY, stroke_width=3),
                   label(r"the reward model's favourite", font_size=22, color=PROXY)).arrange(RIGHT, buff=0.2),
            VGroup(Circle(radius=0.13, color=GOLD, stroke_width=2.5),
                   label(r"gold's favourite", font_size=22, color=GOLD)).arrange(RIGHT, buff=0.16),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        ring_key.next_to(nums[0], DOWN, buff=0.35, aligned_edge=LEFT)
        if kinds.get_right()[0] > 6.9:
            kinds.scale((6.9 - X) / kinds.width, about_edge=LEFT)
        tag = note(r"computed: \ the larger reward model's favourite of each question's lines; \ gold units",
                   font_size=18).to_corner(DR, buff=0.15)
        if believed > actual + 0.02:
            verdict = (f"It overestimated its own picks by {believed - actual:.2f}, and it picked gold's favourite "
                       f"in {100 * same:.0f} percent of the questions.")
        else:
            verdict = (f"Here its picks are worth about what it thinks, and it picked gold's favourite in "
                       f"{100 * same:.0f} percent of the questions.")
        with self.voiceover(
            "Now use the reward model to choose. Each column is one question's lines, placed by gold; the orange "
            "ring is the line the reward model likes best, the yellow ring gold's own favourite. "
            f"<bookmark mark='a'/> By its own score, in gold's units, its favourites stand {believed:+.2f} above the "
            f"question's average line. <bookmark mark='b'/> Gold says {actual:+.2f}. <bookmark mark='c'/> Gold's own "
            f"favourites would have stood at {best_v:+.2f}. {verdict} <bookmark mark='d'/> Choosing by a noisy "
            "measure chooses the noise along with the signal: the winner tends to be a line the measure overrates. "
            "David Manheim and Scott Garrabrant called this regressional Goodhart. Push harder, with more "
            "candidates, or a policy trained against the score, and you reach lines unlike any it learned from, "
            "where its errors stop being random: extremal Goodhart. That is where the next two chapters go."
        ) as vo:
            self.play(FadeIn(gax), Create(zero), FadeIn(tag))
            self.play(FadeIn(dots), run_time=1.5)
            self.play(FadeIn(nums[0]), FadeIn(ring_key),
                      LaggedStart(*[Create(c_) for c_ in rings_rm], lag_ratio=0.05),
                      LaggedStart(*[Create(c_) for c_ in rings_g], lag_ratio=0.05), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeOut(ring_key), run_time=0.5)
            self.play(FadeIn(nums[1]))
            vo.wait_until("b")
            self.play(FadeIn(nums[2]))
            vo.wait_until("c")
            self.play(FadeIn(nums[3]))
            vo.wait_until("d")
            self.play(FadeIn(kinds, shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()
