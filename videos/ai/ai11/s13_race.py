from __future__ import annotations

import math
import unicodedata

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import OPT_COLORS, OPT_NAMES, PART, SAY, band, bits_axes, growing, lag, load, lr_tex, \
    step_counter, takeaway_card


def standings(r):
    """Optimizers by mean final bits over the seeds, with each one's min and max."""
    rows = []
    for o in r["opts"]:
        f = np.asarray(r[f"finals_{o}"], float)
        rows.append((o, float(np.nanmean(f)), float(np.nanmin(f)), float(np.nanmax(f))))
    return sorted(rows, key=lambda x: x[1])


class Race(VoiceoverScene):
    def construct(self):
        self.card()
        self.rules()
        self.sweeps()
        self.replay()
        self.reading()
        self.cost()
        self.takeaway()

    def card(self):
        c = chapter_card(12, r"The race, \ run fairly", r"Which optimizer trains our model fastest?", part=PART)
        with self.voiceover("Chapter twelve. The race, run fairly."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def rules(self):
        r = load("race")
        opts = list(r["opts"])
        n_lr = min(len(r[f"lrs_{o}"]) for o in opts)
        rules = VGroup(
            label(r"the same model, \ the same data in the same order, \ the same $3{,}000$ steps", font_size=24),
            label(r"the same schedule: \ $60$ steps of warmup, \ then a cosine to zero", font_size=24),
            label(rf"each optimizer at ${n_lr}$ learning rates or more, \ a factor of $2$ apart, \\ extended until the best "
                  r"is inside; \ the best kept", font_size=24),
            label(r"the best one run again from $2$ more seeds: \ the spread is shown", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        for r_ in rules:
            r_.scale(1.15)
        rules.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 1.3, 0])
        keep_in_frame(rules)
        head = label(r"the rules", font_size=34, color=C.BITS).next_to(rules, UP, buff=0.35)
        roster = VGroup(*[label(OPT_NAMES[o], font_size=26, color=OPT_COLORS[o]) for o in opts]).arrange(RIGHT, buff=0.55)
        roster.to_edge(DOWN, buff=1.6)
        notes = VGroup(*[label(t_, font_size=18, color=GREY_A).next_to(roster[i], DOWN, buff=0.12) for i, t_ in enumerate(
            [r"Nesterov, \ $0.9$", r"decay $0.1$", r"decay $1.0$", r"grafted", r"basis every $10$", r"$5$ rounds"])])
        sub = label(r"Shampoo, SOAP and Muon on the two hidden matrices; \ AdamW on the rest", font_size=20, color=GREY_B)
        sub.next_to(notes, DOWN, buff=0.3)
        tag = note(r"the character model: \ $8$ characters of context, \ $256$ units, \ Part 1's books").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Now a race between the optimizers of this part, on our character model, under rules that make it fair. "
            "<bookmark mark='a'/> The same model, the same batches in the same order, the same three thousand steps "
            "and the same schedule, a short warmup and a cosine. <bookmark mark='b'/> Each optimizer gets "
            f"{n_lr} learning rates, a factor of two apart, more if its best is at the end of the range, and keeps "
            "its best: a method can look bad just because it was run at the wrong rate. <bookmark mark='c'/> Then the best setting is run again from two "
            "more seeds, so we can see how much of any difference is luck. <bookmark mark='d'/> The contestants: SGD "
            "with momentum, AdamW, Lion, Shampoo, SOAP and Muon."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(roster.copy().set_opacity(0.25)))
            vo.wait_until("a")
            self.play(FadeIn(rules[0], shift=RIGHT * 0.2))
            self.play(FadeIn(rules[1], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rules[2], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(rules[3], shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(lag([FadeIn(x, shift=UP * 0.1) for x in roster], lag_ratio=0.2), FadeIn(notes), FadeIn(sub))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sweeps(self):
        r = load("race")
        opts = list(r["opts"])
        allf = np.concatenate([np.asarray(r[f"sweep_{o}"], float) for o in opts])
        ok = allf[np.isfinite(allf)]
        lo = math.floor((float(ok.min()) - 0.05) * 10) / 10
        hi = math.ceil((float(min(ok.max(), ok.min() + 1.6)) + 0.05) * 10) / 10
        n_lr = max(len(r[f"lrs_{o}"]) for o in opts)
        g = bits_axes([0, n_lr - 1], [lo, hi], x_length=6.6, y_length=4.4, center=[-2.8, -0.4, 0], x_step=1,
                      xlabel=r"learning rate, \ in steps of $\times 2$ from each grid's smallest",
                      ylabel=r"held-out bits after $3{,}000$ steps, \ seed $0$", y_step=round((hi - lo) / 4, 1) or 0.1,
                      xfmt=lambda v: rf"\times{2 ** int(v)}", yfmt=lambda v: f"{v:.2f}")
        ax = g.ax
        lines, best_dots = VGroup(), VGroup()
        for o in opts:
            f = np.asarray(r[f"sweep_{o}"], float)
            xs = np.arange(len(f))
            k = np.isfinite(f) & (f < hi)
            lines.add(VGroup(curve(ax, xs[k], f[k], OPT_COLORS[o], 3),
                             *[Dot(ax.c2p(x, y), radius=0.05, color=OPT_COLORS[o]) for x, y in zip(xs[k], f[k])]))
            i = int(np.nanargmin(f))
            best_dots.add(Circle(radius=0.11, color=OPT_COLORS[o], stroke_width=3).move_to(ax.c2p(i, f[i])))
        rows = VGroup(*[label(rf"{OPT_NAMES[o]}: \ best $\eta = {lr_tex(float(r[f'best_{o}']))}$", font_size=20,
                              color=OPT_COLORS[o]) for o in opts]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        rows.move_to([4.6, 0.6, 0])
        keep_in_frame(rows)
        edges = [o for o in opts if bool(r[f"edge_{o}"])]
        etxt = (f" One caution: {SAY[edges[0]]}'s best rate is at the end of its grid, so it might do a little better "
                "still." if len(edges) == 1 else
                (f" One caution: {len(edges)} of them have their best rate at the end of the grid." if edges else
                 " Every best rate is inside its grid, so the grids were wide enough."))
        with self.voiceover(
            "First the learning-rate sweeps. <bookmark mark='a'/> Each optimizer's held-out loss against its "
            "learning rates: too small and it crawls, too large and it overshoots, and in between a valley. "
            "<bookmark mark='b'/> Its lowest point is the rate it races at." + etxt
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(lag([Create(l_) for l_ in lines], lag_ratio=0.2), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(best_dots), FadeIn(rows))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        r = load("race")
        opts = list(r["opts"])
        cur = {o: np.asarray(r[f"curves_{o}"], float) for o in opts}  # seed x point x (step, bits)
        xs = cur[opts[0]][0, :, 0]
        S = float(xs[-1])
        lo = float(min(np.nanmin(c[:, -1, 1]) for c in cur.values())) - 0.08
        hi = lo + 1.6
        g = bits_axes([0, S], [lo, hi], x_length=7.2, y_length=4.6, center=[-2.5, -0.4, 0], x_step=1000,
                      y_step=0.4, yfmt=lambda v: f"{v:.1f}")
        ax = g.ax
        t = ValueTracker(0)
        live, bands = [], VGroup()
        for o in opts:
            c = cur[o]
            med = np.clip(np.median(c[:, :, 1], 0), lo, hi)
            live.append(growing(ax, xs, med, t, OPT_COLORS[o], 3))
            bands.add(band(ax, xs[1:], np.clip(c[:, 1:, 1].min(0), lo, hi), np.clip(c[:, 1:, 1].max(0), lo, hi),
                           OPT_COLORS[o], 0.2))
        cnt = step_counter(t, ax.get_corner(UR), DL)
        st = standings(r)
        rows = VGroup(label(r"held-out bits, \ $3$ seeds: \ mean \ (min--max)", font_size=20, color=GREY_A))
        for o, m, a, b in st:
            rows.add(label(rf"{OPT_NAMES[o]}: \ ${m:.3f}$ \ (${a:.3f}$--${b:.3f}$)", font_size=21, color=OPT_COLORS[o]))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.4, 0.4, 0])
        keep_in_frame(rows)
        tag = note(r"each at its best rate; \ line: \ median of $3$ seeds; \ band: \ min to max").to_corner(DL, buff=0.2)
        (w, wm, _, wb), (s2, _, sa, _) = st[0], st[1]
        last = st[-1]
        aw = next(x for x in st if x[0] == "adamw")
        sep = wb < sa  # the winner's worst seed beats the runner-up's best
        if sep:
            verdict = (f"{SAY[w]} wins, at {wm:.3f} bits, and its worst seed beats {SAY[s2]}'s best: the difference is "
                       "bigger than the luck of the seeds.")
        else:
            verdict = (f"{SAY[w]} is ahead on average, at {wm:.3f} bits, but its seeds overlap with {SAY[s2]}'s: on "
                       "this model the top two are not clearly separated.")
        rel = (f"AdamW, the baseline, finishes {aw[1] - wm:.3f} bits behind the winner. " if w != "adamw" else
               "The baseline, AdamW, is the winner here. ")
        with self.voiceover(
            "Now the race itself, replayed: each optimizer at its best rate, the line the median of three seeds, "
            "the band their spread. <bookmark mark='a'/> " + verdict + " <bookmark mark='b'/> " + rel
            + f"Last comes {SAY[last[0]]}, at {last[1]:.3f}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            self.add(*live, cnt)
            self.play(t.animate.set_value(S), run_time=7.0, rate_func=linear)
            for m_ in live + [cnt]:
                m_.clear_updaters()
            self.play(FadeIn(bands))
            vo.wait_until("a")
            self.play(lag([FadeIn(r_) for r_ in rows[:3]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(lag([FadeIn(r_) for r_ in rows[3:]], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reading(self):
        r = load("race")
        st = standings(r)
        names = ["sgdm", st[0][0] if st[0][0] != "sgdm" else st[1][0]]
        steps = [int(s_) for s_ in r["write_at"]]
        bits_at = {}
        for n in names:
            c = np.asarray(r[f"curves_{n}"], float)[0]
            bits_at[n] = [float(np.interp(k, c[:, 0], c[:, 1])) for k in steps]

        def clean(t):
            t = "".join(ch for ch in t if unicodedata.category(ch) not in ("Cc", "Cf", "Mn") or ch == "\n")
            return t.replace("\n", "↵")

        def block(name, k):
            t = clean(r[f"writes_{name}"][k])
            kw = dict(font="DejaVu Sans Mono", font_size=27)
            p_ = data_text("It was a", color=WHITE, **kw)
            n1 = len(t) // 2
            sp = t.rfind(" ", 0, n1 + 1)
            n1 = sp if sp > n1 - 10 else n1
            l1 = data_text(t[:n1].strip() or ".", color=OPT_COLORS[name], **kw).next_to(p_, RIGHT, buff=0.18)
            l1.align_to(p_, DOWN)
            l2 = data_text(t[n1:].strip() or ".", color=OPT_COLORS[name], **kw).next_to(VGroup(p_, l1), DOWN, buff=0.16)
            l2.align_to(p_, LEFT)
            return VGroup(p_, l1, l2)

        heads = {n: label(OPT_NAMES[n], font_size=24, color=OPT_COLORS[n]) for n in names}
        ys = {names[0]: 1.5, names[1]: -0.6}

        def place(name, k):
            g_ = block(name, k)
            if g_.width > 10.0:
                g_.scale_to_fit_width(10.0)
            return g_.shift([-3.7 - g_[0].get_left()[0], ys[name] - g_.get_center()[1], 0])

        for n in names:
            heads[n].move_to([-5.6, ys[n], 0])
        t = ValueTracker(0)
        bits = {n: always_redraw(lambda n=n: MathTex(
            rf"{float(np.interp(t.get_value(), steps, bits_at[n])):.2f}\ \text{{bits}}", font_size=22,
            color=OPT_COLORS[n]).next_to(heads[n], DOWN, buff=0.1)) for n in names}
        prompt = label(r"both continue ``It was a'' \ with the same random draws", font_size=22, color=GREY_A).to_edge(UP, buff=0.25)
        cnt = always_redraw(lambda: MathTex(rf"\text{{step }}{int(t.get_value()):,}".replace(",", "{,}"), font_size=28,
                                            color=WHITE).move_to([4.8, -2.6, 0]))
        cur = {n: place(n, 0) for n in names}
        b0, b1 = bits_at[names[0]], bits_at[names[1]]
        ahead = all(b < a for a, b in zip(b0[1:], b1[1:]))
        said1 = (f"{SAY[names[1]]}, there is punctuation and the rhythm of sentences. It is ahead at every checkpoint."
            if ahead else
            f"{SAY[names[1]]}, there is punctuation and the rhythm of sentences.")
        with self.voiceover(
            f"What do these numbers read like? Here SGD with momentum and the winner, {SAY[names[1]]}, continue the "
            "same three words with the same random draws, at checkpoints of their runs. <bookmark mark='a'/> Before "
            f"training, every character is equally likely, {b0[0]:.1f} bits each: noise from the whole alphabet. "
            f"<bookmark mark='b'/> After {steps[1]} steps, spaces and short words. <bookmark mark='c'/> By step "
            f"{steps[3]:,}, most of it is word-shaped, <bookmark mark='d'/> and by the end, at {b1[-1]:.2f} bits for "
            + said1
        ) as vo:
            self.play(FadeIn(prompt), *[FadeIn(h) for h in heads.values()])
            self.add(*bits.values(), cnt)
            vo.wait_until("a")
            self.play(*[FadeIn(cur[n][0]) for n in names])
            self.play(*[AddTextLetterByLetter(line_) for n in names for line_ in cur[n][1:]], run_time=1.5)
            for k, mk in zip(range(1, len(steps)), ("b", None, "c", "d")):
                if mk:
                    vo.wait_until(mk)
                nxt = {n: place(n, k) for n in names}
                self.play(*[FadeTransform(cur[n], nxt[n]) for n in names], t.animate.set_value(steps[k]), run_time=1.4)
                cur = nxt
        for m_ in list(bits.values()) + [cnt]:
            m_.clear_updaters()
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cost(self):
        r = load("race")
        opts = list(r["opts"])
        ms = {o: float(r[f"ms_{o}"]) for o in opts}
        base = ms["adamw"]
        top = max(ms.values()) * 1.15
        ax = CornerAxes(x_range=[0, len(opts), 1], y_range=[0, top, top / 4], x_length=7.0, y_length=3.8, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-2.4, -0.3, 0])
        bars, labs = VGroup(), VGroup()
        for i, o in enumerate(opts):
            h = ax.c2p(0, ms[o])[1] - ax.c2p(0, 0)[1]
            b = Rectangle(width=0.7, height=max(h, 0.01), stroke_width=0, fill_color=OPT_COLORS[o], fill_opacity=0.9)
            b.move_to(ax.c2p(i + 0.5, ms[o] / 2))
            bars.add(b)
            nm = r"SGD $+$ \\ momentum" if o == "sgdm" else OPT_NAMES[o]
            labs.add(VGroup(label(nm, font_size=18, color=OPT_COLORS[o]).next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.12),
                            label(rf"${ms[o] / base:.1f}\times$", font_size=20, color=WHITE).next_to(b, UP, buff=0.08)))
        yn = label(r"time per training step, \ relative to AdamW", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.4).align_to(ax, LEFT)
        caveat = label(r"one CPU thread, \ shared with other jobs; \ a tiny model, \ where the extra matrix work is a big "
                       r"share. \\ On GPUs, \ at scale, \ Muon's extra arithmetic is estimated at under $1\%$.", font_size=20,
                       color=GREY_B).to_edge(DOWN, buff=0.35)
        mu, sh = ms["muon"] / base, ms["shampoo"] / base
        with self.voiceover(
            "Steps are not free, though. <bookmark mark='a'/> Here is the time each optimizer took per step, "
            f"relative to AdamW, on this computer: Muon {mu:.1f} times, Shampoo {sh:.1f} times. "
            "<bookmark mark='b'/> Take that with care: one shared processor thread, and a model so small that the "
            "extra matrix work is a large share of each step. For large language models on GPUs, Muon's author "
            "estimates its extra arithmetic at under one percent, and AlgoPerf scores optimizers by wall-clock time for exactly this reason."
        ) as vo:
            self.play(Create(ax), FadeIn(yn))
            vo.wait_until("a")
            self.play(lag([GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15), FadeIn(labs), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(caveat))
        self.wait(0.3)
        self.clear_scene()

    def takeaway(self):
        r = load("race")
        st = standings(r)
        w = st[0][0]
        t = takeaway_card(r"A fair race: \ tune everyone, \ show the spread",
                          rf"On our model, \ at equal steps, \ each at its best rate: \ {OPT_NAMES[w]} first, \ "
                          rf"${st[0][1]:.3f}$ bits; \ {OPT_NAMES[st[-1][0]]} last, \ ${st[-1][1]:.3f}$.",
                          r"Next: \ how the learning rate should change over a run")
        with self.voiceover(
            f"So on our model, with every optimizer at its own best rate and equal steps, {SAY[w]} came first. The "
            "rate was tuned for each, and the schedule fixed for all. Next: how that schedule should be shaped."
        ):
            self.play(FadeIn(t[0], shift=UP * 0.2))
            self.play(FadeIn(t[1]))
        self.wait(0.3)
        self.clear_scene()
