from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import HIST, chapter, dots_on, load
from videos.ai.ai3.compute import ratings_world

GEN_COLORS = ["#F2A541", "#58A6FF", "#E85D75", "#D4A5FF", "#5BD17A", "#4FD1C5"]
TRC, TEC = C.TRUE_P, C.MODEL_Q
TT, POP = C.REWARD, GREY_B


def penalty_verdict(history, no_vector_penalty, tolerance=0.01):
    """Separate within-run rebound from the endpoint comparison; RMSE is in stars."""
    last = float(history[-1, 2])
    other = float(no_vector_penalty[-1, 2])
    best = float(np.min(no_vector_penalty[:, 2]))
    rebound = (f" With no vector penalty, held-out error rises from its minimum of {best:.3f} to {other:.3f}."
               if other > best + tolerance else
               f" With no vector penalty, held-out error finishes at {other:.3f}, without a clear late rebound.")
    gap = other - last
    comparison = ("higher than" if gap > tolerance else "lower than" if gap < -tolerance else "within 0.01 stars of")
    return (f"{rebound} Its final error is {comparison} the vector-penalized run's {last:.3f}. "
            "Both runs retain the same bias penalty.")


def retrieval_display_data(result):
    """Separate eligibility, finite measurements and displayable history per cohort."""
    history = np.asarray(result["curve"], float)
    cohorts = {}
    for key, suffix, column in (("warm", "warm", 2), ("cold", "cold", 3)):
        counts = result["evaluation"][key]
        users, targets = int(counts["evaluated_users"]), int(counts["eligible_targets"])
        eligible = users > 0 and targets > 0
        recall, popularity = float(result[f"recall_{suffix}"]), float(result[f"pop_{suffix}"])
        model_available = eligible and bool(np.isfinite(recall))
        baseline_available = eligible and bool(np.isfinite(popularity))
        steps, values = history[:, 0].copy(), history[:, column].copy()
        valid = np.isfinite(steps) & np.isfinite(values)
        values[~valid] = np.nan  # shared curve() preserves omitted runs as gaps
        cohorts[key] = dict(users=users, targets=targets, eligible=eligible, recall=recall,
                            popularity=popularity, model_available=model_available,
                            baseline_available=baseline_available, steps=steps, values=values,
                            show_curve=model_available and bool(valid.any()))
    return cohorts


def retrieval_cohort_summary(cohort, name):
    """Never compare unavailable recall with popularity or pronounce it a loss."""
    users, targets = cohort["users"], cohort["targets"]
    if not cohort["eligible"]:
        return (f"For {name}, recall is unavailable: {users} evaluated users have {targets} eligible held-out "
                "targets. Empty-target users are excluded, so there is no popularity comparison.")
    recall, popularity = cohort["recall"], cohort["popularity"]
    if not cohort["model_available"] and not cohort["baseline_available"]:
        return (f"For {name}, both recall measurements are unavailable despite {users} evaluated users and "
                f"{targets} eligible targets. No finite comparison is available.")
    if not cohort["model_available"]:
        return (f"For {name}, two-tower recall is unavailable on {users} users and {targets} eligible targets; "
                f"popularity recall is {popularity:.3f}. No comparison is available.")
    if not cohort["baseline_available"]:
        return (f"For {name}, two-tower recall is {recall:.3f} on {users} users and {targets} eligible targets, "
                "but popularity recall is unavailable. No comparison is available.")
    comparison = ("The two towers beat popularity for this cohort." if recall > popularity else
                  "The two towers do not beat popularity for this cohort.")
    return (f"For {name}, macro recall reaches {recall:.3f}, against popularity's {popularity:.3f}, on "
            f"{users} users and {targets} eligible targets. {comparison}")


class Netflix(VoiceoverScene):
    def construct(self):
        chapter(self, 17, r"Low rank in the wild", r"Can a mostly empty table be filled in?",
                "Chapter seventeen. Low rank in the wild: recommendations and retrieval.")
        self.prize()
        self.model()
        self.replay()
        self.ranks()
        self.towers()
        self.today()

    # ------------------------------------------------------------------
    def prize(self):
        m = load("mf")
        W = ratings_world()
        U, I = 160, 260
        R = np.zeros((U, I))
        sel = (W["users"] < U) & (W["items"] < I)
        R[W["users"][sel], W["items"][sel]] = W["r"][sel]
        rgb = np.zeros((U, I, 3))
        bg = np.array(ManimColor("#121722").to_rgb())
        rgb[:] = bg
        for s_ in range(1, 6):
            c = np.array(ManimColor(interpolate_color(ManimColor(C.PENALTY), ManimColor(C.REWARD), (s_ - 1) / 4)).to_rgb())
            rgb[R == s_] = c
        img = ImageMobject((np.concatenate([rgb, np.ones((U, I, 1))], -1) * 255).astype(np.uint8))
        img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        img.stretch_to_fit_width(5.6).stretch_to_fit_height(3.5).move_to([-3.1, -0.3, 0])
        frame = SurroundingRectangle(img, buff=0, color=GREY_D, stroke_width=1.2)
        xl = label(r"films", font_size=22, color=GREY_A).next_to(frame, UP, buff=0.1)
        yl = label(r"users", font_size=22, color=GREY_A).next_to(frame, LEFT, buff=0.1)
        tag = note(rf"a corner of our synthetic ratings: \ ${100 * m['density']:.1f}\%$ of cells filled; \\ red $1$ "
                   r"star, \ green $5$").next_to(frame, DOWN, buff=0.12)
        card = history_card(2006, r"the Netflix Prize",
                            r"$100{,}480{,}507$ ratings, \ $480{,}189$ users, \ $17{,}770$ films; \ \$1 million for "
                            r"predicting held-out ratings $10\%$ better than Netflix's Cinematch \ (test error "
                            r"$0.9525$)", color=HIST, width=5.6).move_to([3.5, 1.2, 0])
        won = history_card(2009, r"BellKor's Pragmatic Chaos",
                           r"test error $0.8567$, \ $10.06\%$ better; \ a rival team matched it twenty minutes too "
                           r"late", color=HIST, width=5.6).move_to([3.5, -1.8, 0])
        with self.voiceover(
            "Low rank's most famous test came from a DVD rental company. <bookmark mark='a'/> In October 2006 Netflix "
            "released a hundred million ratings, from 480,189 customers on 17,770 films, and offered a million dollars "
            "to predict held-out ratings ten percent better than its own system. <bookmark mark='b'/> The table was "
            "mostly empty: about two hundred ratings per customer. <bookmark mark='c'/> In December, a programmer "
            "writing as Simon Funk posted a short program that factorized it by gradient descent, and leapt up the "
            "leaderboard. In 2009 BellKor's Pragmatic Chaos won with a blend of hundreds of models, many of them "
            "refinements of that factorization."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(img), Create(frame), FadeIn(xl), FadeIn(yl))
            vo.wait_until("b")
            self.play(FadeIn(tag), Indicate(frame, color=WHITE))
            vo.wait_until("c")
            self.play(FadeIn(won, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def model(self):
        m = load("mf")
        colors = {r"\mathbf{p}_u^{\top}\mathbf{q}_i": C.BITS}
        rows = [
            cmath(r"\hat r_{ui}", "=", r"\mu + b_u + b_i +", r"\mathbf{p}_u^{\top}\mathbf{q}_i", font_size=38, colors=colors),
            cmath(r"\min", r"\textstyle\sum_{(u,i)\ \text{rated}}", r"\Big[(r_{ui} - \hat r_{ui})^2 + \lambda\big(|\mathbf{p}_u|^2 + "
                  r"|\mathbf{q}_i|^2\big) + 0.01(b_u^2+b_i^2)\Big]", font_size=32),
        ]
        whys = [why(r"an average, \ how generous the user is, \ how good the film is, \\ and a rank-$k$ taste match"),
                why(r"only the cells we have; \ $\lambda$ penalizes vectors; \ biases retain a $0.01$ penalty")]
        step = ladder(self, rows, whys, keep=2, top=2.9, x=-1.5, buff=0.6, edge=6.9)
        pts = VGroup(
            label(r"the best rank-$k$ copy of a \textit{full} table: \ the SVD (chapter eight)", font_size=28,
                  color=GREY_A),
            label(r"a table with holes: \ no formula; \ gradient descent, \ or alternating least squares", font_size=28,
                  color=C.BITS),
            label(rf"our world: \ ${m['users']:,}$ users, \ ${m['items']:,}$ films, \ ${m['n_ratings']:,}$ ratings, \ "
                  rf"six hidden genres \ (synthetic)".replace(",", "{,}"), font_size=26, color=GREY_B),
        ).arrange(DOWN, buff=0.35).move_to(DOWN * 1.6)
        with self.voiceover(
            "The model is a sum. <bookmark mark='a'/> An average, plus the user's generosity, plus the film's quality, "
            "plus a dot product of k numbers of taste each. <bookmark mark='b'/> Fit it to the ratings we have, keeping "
            "the vectors small, with a separate fixed penalty on user and film biases. <bookmark mark='c'/> A full table would have chapter eight's answer; with holes there is "
            "no formula, and we descend the gradient. <bookmark mark='d'/> We built a small world to test on: "
            f"{m['users']:,} users, {m['items']:,} films, {m['n_ratings']:,} ratings, from six hidden genres the method "
            "never sees."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(Indicate(rows[0][3], color=C.BITS))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            self.play(FadeIn(pts[0]))
            self.play(FadeIn(pts[1]))
            vo.wait_until("d")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        m = load("mf")
        rp = m["replay"]
        h, h0 = np.asarray(rp["hist"]), np.asarray(rp["hist_noreg"])
        E = int(h[-1, 0])
        lo = float(min(h[:, 1:].min(), h0[:, 1:].min())) - 0.03
        hi = float(max(h[:, 1:].max(), h0[:, 1:].max())) + 0.03
        ga = axes([0, E, 10], [lo, hi, 0.1], x_length=5.6, y_length=3.6, xticks=[0, 10, 20, 30, 40],
                  yticks=[round(v, 1) for v in np.arange(np.ceil(lo * 10) / 10, hi, 0.1)],
                  xlabel=r"pass over the ratings", ylabel=r"error (root mean square, stars)", center=[-3.5, -0.6, 0])
        ax = ga.ax
        ep = h[:, 0]
        leg = legend([(TRC, r"ratings it trained on"), (TEC, r"held-out ratings"),
                      (GREY_B, r"dashed: \ no vector penalty; \ bias penalty unchanged")], font_size=18).next_to(ga, UP, buff=0.1)
        Q = np.asarray(m["q_snaps"])
        gen = np.asarray(m["genre"])
        eps_ = [int(e) for e in m["q_snap_epochs"]]
        lim = float(np.percentile(np.abs(Q[-1]), 99)) * 1.1
        gb = Axes(x_range=[-lim, lim, lim], y_range=[-lim, lim, lim], x_length=4.2, y_length=4.2, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([3.6, -0.4, 0])
        sub = np.arange(0, Q.shape[1], 2)
        t = ValueTracker(0)

        def epoch():
            return float(np.interp(t.get_value(), np.arange(len(eps_)), eps_))

        def trace(values, color, dashed=False):
            end = epoch()
            xs = np.append(ep[ep < end], end)
            ys = np.interp(xs, ep, values)
            # At pass zero use a dot, then reveal the actual epoch coordinates.
            line = curve(ax, xs, ys, color, 2.5) if len(xs) > 1 else Dot(ax.c2p(xs[0], ys[0]), radius=0.03, color=color)
            return DashedVMobject(line, num_dashes=40) if dashed and len(xs) > 1 else line

        traces = VGroup(*[always_redraw(lambda values=values, color=color, dashed=dashed:
                                       trace(values, color, dashed))
                          for values, color, dashed in ((h[:, 1], TRC, False), (h[:, 2], TEC, False),
                                                        (h0[:, 1], TRC, True), (h0[:, 2], TEC, True))])
        cursor = always_redraw(lambda: Line(ax.c2p(epoch(), lo), ax.c2p(epoch(), hi), color=WHITE,
                                           stroke_width=1.5, stroke_opacity=0.6))

        def film_dots():
            v = t.get_value()
            i = int(min(np.floor(v), len(eps_) - 2))
            a = v - i
            P = (1 - a) * Q[i] + a * Q[i + 1]
            return VGroup(*[Dot(gb.c2p(*np.clip(P[j], -lim, lim)), radius=0.03, color=GEN_COLORS[gen[j]],
                                fill_opacity=0.8) for j in sub])

        def centroids():
            v = t.get_value()
            i = int(min(np.floor(v), len(eps_) - 2))
            a = v - i
            P = (1 - a) * Q[i] + a * Q[i + 1]
            g_ = VGroup()
            for k_ in range(len(m["genres"])):
                c_ = P[gen == k_].mean(0) * 2.5
                g_.add(Dot(gb.c2p(*np.clip(c_, -lim, lim)), radius=0.11, color=GEN_COLORS[k_], stroke_color=WHITE,
                           stroke_width=2))
            return g_

        fd = always_redraw(film_dots)
        cent = always_redraw(centroids)
        ep_read = always_redraw(lambda: label(rf"film vectors after {epoch():.0f} passes" if
                                              epoch() > 0 else r"film vectors at the start",
                                              font_size=22, color=GREY_A).next_to(gb, UP, buff=0.12))
        gl = VGroup(*[label(nm, font_size=18, color=c_) for nm, c_ in zip(m["genres"], GEN_COLORS)])
        gl.arrange_in_grid(rows=2, cols=3, buff=(0.2, 0.08)).next_to(gb, DOWN, buff=0.12)
        cn = note(r"2D PCA view; \ saved passes interpolated; \ outer points clipped \\ "
                  r"large dots: genre averages $\times 2.5$; \ RMSE clips predictions to $[1,5]$",
                  font_size=17).next_to(gl, DOWN, buff=0.08)
        tail = penalty_verdict(h, h0)
        genre_verdict = ("The final genre-neighbour agreement exceeds the without-self chance baseline."
                         if m["genre_nn"] > m["genre_chance"] else
                         "The final genre-neighbour agreement does not exceed the without-self chance baseline.")
        with self.voiceover(
            f"Training replayed, at rank {int(rp['rank'])}. <bookmark mark='a'/> The error falls on the ratings it "
            f"trains on, and on held-out ones: from {h[0, 2]:.2f} stars to {h[-1, 2]:.3f}.{tail} "
            "<bookmark mark='b'/> On the right, each film's vector, on its two strongest directions, coloured by the "
            "hidden genre, with each genre's average. <bookmark mark='c'/> Of each film's ten "
            "nearest films, "
            f"{100 * m['genre_nn']:.0f} percent share its genre, against {100 * m['genre_chance']:.0f} percent by "
            f"chance. {genre_verdict}"
        ) as vo:
            self.play(FadeIn(ga), FadeIn(leg), Create(gb), FadeIn(gl), FadeIn(cn))
            self.add(fd, cent, ep_read)
            vo.wait_until("a")
            self.add(traces, cursor)
            self.play(t.animate.set_value(1), run_time=2.0)
            vo.wait_until("b")
            self.play(t.animate.set_value(2), run_time=2.0)
            vo.wait_until("c")
            self.play(t.animate.set_value(len(eps_) - 1), run_time=3.0)
        fd.clear_updaters()
        cent.clear_updaters()
        ep_read.clear_updaters()
        traces.clear_updaters(recursive=True)
        cursor.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ranks(self):
        m = load("mf")
        ks = sorted(int(k) for k in m["test_rmse"])
        vals = {k: np.asarray(m["test_rmse"][str(k)]) for k in ks}
        lo = float(min(m["rmse_mean"], m["rmse_bias"], min(v.min() for v in vals.values()))) - 0.03
        hi = float(max(m["rmse_mean"], m["rmse_bias"], max(v.max() for v in vals.values()))) + 0.03
        lk = np.log2(ks)
        g = axes([-0.3, float(lk[-1]) + 0.3, 1], [lo, hi, 0.05], x_length=7.0, y_length=4.0, xticks=list(lk),
                 xfmt=lambda v: f"{2 ** v:.0f}", yticks=[round(v, 2) for v in np.arange(np.ceil(lo * 20) / 20, hi, 0.05)],
                 xlabel=r"rank $k$ \ (numbers of taste per user and per film)", ylabel=r"held-out error (stars)",
                 center=[-1.4, -0.5, 0])
        ax = g.ax
        mean_l = DashedLine(ax.c2p(-0.3, m["rmse_mean"]), ax.c2p(lk[-1] + 0.3, m["rmse_mean"]), color=GREY_B)
        bias_l = DashedLine(ax.c2p(-0.3, m["rmse_bias"]), ax.c2p(lk[-1] + 0.3, m["rmse_bias"]), color=GREY_A)
        ml = label(rf"the average rating: \ ${m['rmse_mean']:.3f}$", font_size=20, color=GREY_B)
        ml.next_to(ax.c2p(lk[-1] + 0.3, m["rmse_mean"]), DOWN, buff=0.06).align_to(ax.c2p(lk[-1] + 0.3, 0), RIGHT)
        bl = label(rf"plus user and film biases: \ ${m['rmse_bias']:.3f}$", font_size=20, color=GREY_A)
        bl.next_to(ax.c2p(lk[-1] + 0.3, m["rmse_bias"]), UP, buff=0.06).align_to(ax.c2p(lk[-1] + 0.3, 0), RIGHT)
        bars = VGroup(*[Line(ax.c2p(x, vals[k].min()), ax.c2p(x, vals[k].max()), color=C.BITS, stroke_width=6)
                        for x, k in zip(lk, ks)])
        mids = dots_on(ax, lk, [vals[k].mean() for k in ks], C.BITS, 0.07)
        cv = curve(ax, lk, [vals[k].mean() for k in ks], C.BITS, 3)
        best = min(ks, key=lambda k: vals[k].mean())
        cap = note(r"matched train+validation refit; \ common test ratings \\ three seeds per rank; \ $\lambda$ selected before refitting",
                   font_size=18).to_corner(DR, buff=0.25)
        why_best = (", near the six hidden genres in this synthetic world." if best in (4, 8) else ".")
        with self.voiceover(
            f"How much taste does it take? All methods are refitted on the same training plus validation ratings, "
            f"then measured on the same untouched test ratings. The average rating misses by {m['rmse_mean']:.3f} stars. "
            f"<bookmark mark='a'/> Adding generosity and quality: {m['rmse_bias']:.3f}. <bookmark mark='b'/> Then the "
            "taste vectors, rank one to thirty-two, three seeds each. The error is lowest at rank "
            f"{best}, {vals[best].mean():.3f}{why_best}"
        ) as vo:
            self.play(FadeIn(g), Create(mean_l), FadeIn(ml), FadeIn(cap))
            vo.wait_until("a")
            self.play(Create(bias_l), FadeIn(bl))
            vo.wait_until("b")
            self.play(Create(cv), LaggedStart(*[Create(b_) for b_ in bars], lag_ratio=0.2), FadeIn(mids), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def towers(self):
        t = load("twotower")
        curve_ = np.asarray(t["curve"])
        steps = curve_[:, 0]
        cohorts = retrieval_display_data(t)
        # the two towers, schematic
        def tower(title, inputs, col, x):
            box = RoundedRectangle(width=2.6, height=1.0, corner_radius=0.12, stroke_color=col, stroke_width=2,
                                   fill_color=col, fill_opacity=0.15)
            ins = VGroup(*[label(s, font_size=18, color=GREY_A) for s in inputs]).arrange(DOWN, buff=0.06)
            ins.next_to(box, DOWN, buff=0.25)
            nm = label(title, font_size=24, color=col).move_to(box)
            vec = Rectangle(width=0.25, height=1.0, stroke_color=col, fill_color=col, fill_opacity=0.6).next_to(box, UP,
                                                                                                         buff=0.3)
            return VGroup(box, nm, ins, vec, Arrow(box.get_top(), vec.get_bottom(), buff=0.05, color=GREY_B,
                                                   stroke_width=2)).shift(RIGHT * x)

        ut = tower(r"user tower", [r"films watched", r"age group, \ region"], C.TRUE_P, -4.6)
        it = tower(r"film tower", [r"film id", r"genre, \ year"], C.MODEL_Q, -1.8)
        both = VGroup(ut, it).move_to([-3.2, 0.2, 0])
        dot = MathTex(r"\text{score} = \mathbf{u}\cdot\mathbf{v}", font_size=32).next_to(both, UP, buff=0.3)
        tag = note(r"schematic; \ inference ranks by raw $s = \mathbf{u}\cdot\mathbf{v}/\tau$ \\ training candidate logits: $s-\log q(i)$",
                   font_size=18).next_to(both, DOWN, buff=0.2)
        available_values = [0.1]
        for cohort in cohorts.values():
            if cohort["show_curve"]:
                available_values.extend(cohort["values"][np.isfinite(cohort["values"])])
            if cohort["baseline_available"]:
                available_values.append(cohort["popularity"])
        ymax = min(1.0, max(available_values) * 1.15)
        g = axes([0, float(steps[-1]), 1000], [0, ymax, ymax / 4], x_length=5.4, y_length=3.4,
                 xticks=list(np.linspace(0, steps[-1], 4)), yticks=list(np.linspace(0, ymax, 5)),
                 yfmt=lambda v: f"{v:.2f}", xlabel=r"training step", ylabel=r"macro recall at $10$ \ (held-out films)",
                 center=[3.4, -0.5, 0])
        ax = g.ax
        def measured(cohort, color):
            if not cohort["show_curve"]:
                return VGroup()
            finite = np.isfinite(cohort["values"])
            if finite.sum() == 1:
                i = int(np.flatnonzero(finite)[0])
                return Dot(ax.c2p(cohort["steps"][i], cohort["values"][i]), radius=0.06, color=color)
            return curve(ax, cohort["steps"], cohort["values"], color, 3)

        warm, cold = cohorts["warm"], cohorts["cold"]
        cw, cc = measured(warm, TT), measured(cold, C.BITS)
        pw = (DashedLine(ax.c2p(0, warm["popularity"]), ax.c2p(steps[-1], warm["popularity"]), color=POP)
              if warm["baseline_available"] else VGroup())
        pc = (DashedLine(ax.c2p(0, cold["popularity"]), ax.c2p(steps[-1], cold["popularity"]),
                         color=GREY_A, dashed_ratio=0.3) if cold["baseline_available"] else VGroup())
        legend_rows = []
        for available, color, text in (
                (warm["show_curve"], TT, r"two towers: \ users it trained on"),
                (cold["show_curve"], C.BITS, r"two towers: \ new users, \ $5$ films each"),
                (warm["baseline_available"], POP, r"popular films: \ known users, dashed"),
                (cold["baseline_available"], GREY_A, r"popular films: \ new users, short dashes")):
            if available:
                legend_rows.append((color, text))
        leg = (legend(legend_rows, font_size=17) if legend_rows else VGroup()).move_to([-3.2, -2.9, 0])
        unavailable_rows = []
        for cohort, name in ((warm, r"known users"), (cold, r"new users")):
            if not cohort["eligible"]:
                reason = r"no eligible held-out targets"
                missing = r"recall unavailable"
            elif not cohort["model_available"] or not cohort["baseline_available"]:
                reason = r"a recall measurement is non-finite"
                missing = r"comparison unavailable"
            elif not cohort["show_curve"]:
                reason = r"no finite training-history samples"
                missing = r"history unavailable"
            else:
                continue
            unavailable_rows.append(note(rf"{name}: {missing} \\ {reason}", font_size=17))
        unavailable = VGroup(*unavailable_rows).arrange(DOWN, buff=0.12).move_to([3.4, 2.65, 0])
        ew, ec = t["evaluation"]["warm"], t["evaluation"]["cold"]
        metric = note(r"recall: hits / all eligible targets, averaged over users \\ "
                      rf"known: ${ew['evaluated_users']}$ users, ${fmt_int(ew['eligible_targets'])}$ targets; \ "
                      rf"new: ${ec['evaluated_users']}$ users, ${fmt_int(ec['eligible_targets'])}$ targets \\ "
                      r"empty-target users excluded; \ watched films filtered",
                      font_size=22).next_to(g, DOWN, buff=0.08)
        warm_summary = retrieval_cohort_summary(warm, "known users")
        cold_summary = retrieval_cohort_summary(cold, "new users")
        with self.voiceover(
            "Factorization has a weakness: a new user has no vector. Today's recommenders use two towers. "
            "<bookmark mark='a'/> One network turns a user's history into a vector, another a film's details; the score "
            "is their dot product. <bookmark mark='b'/> Trained so each user's real films outscore the batch, corrected "
            "for the negative sampling distribution. In the ideal candidate-classification calculation, the corrected "
            "logit carries a density ratio, while the raw score models the conditional log probability, up to a user "
            "constant. We rank by the raw score; adding a popularity prior again is a separate ablation, not a recovery "
            "step. Finite training need not reach that ideal. <bookmark mark='c'/> Macro recall averages each user's "
            "fraction of all eligible held-out favourites recovered in the top ten. New users start from five "
            f"films each. {warm_summary} Separately, {cold_summary}"
        ) as vo:
            self.play(FadeIn(both), FadeIn(tag), FadeIn(g), FadeIn(metric), FadeIn(unavailable))
            vo.wait_until("a")
            self.play(FadeIn(dot))
            vo.wait_until("b")
            self.play(Create(pw), Create(pc), FadeIn(leg))
            vo.wait_until("c")
            self.play(Create(cw), Create(cc), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def today(self):
        t = load("twotower")
        cards = VGroup(
            history_card(2016, r"P.~Covington, J.~Adams \& E.~Sargin, \ YouTube",
                         r"recommendations as a nearest-neighbour search \ among film vectors", color=HIST, width=4.3,
                         font_size=30),
            history_card(2017, r"J.~Johnson, M.~Douze \& H.~J\'egou, \ FAISS",
                         r"approximate search over a billion vectors, \ on GPUs", color=HIST, width=4.3, font_size=30),
            history_card(2020, r"V.~Karpukhin et al., \ dense passage retrieval",
                         r"questions and passages as vectors: \ search by dot product, \ the retrieval behind "
                         r"today's chatbots", color=HIST, width=4.3, font_size=30),
        ).arrange(RIGHT, buff=0.2, aligned_edge=UP).move_to(UP * 0.4)
        head = label(r"Retrieval is a matrix product", font_size=40).to_edge(UP, buff=0.35)
        tail = MathTex(rf"\text{{scores}} = U\,V^{{\top}}: \quad \text{{users}} \times {t['dim']} \ \cdot \ {t['dim']} "
                       rf"\times {fmt_int(t['items'])}\ \text{{films}}", font_size=34, color=C.BITS).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Retrieval is, at heart, one matrix product, and the art is not computing most of it. <bookmark mark='a'/> "
            "In 2016 YouTube described recommending as a nearest-neighbour search among video vectors. "
            "<bookmark mark='b'/> In 2017 Facebook's FAISS searched a billion vectors, on GPUs. <bookmark mark='c'/> In "
            "2020 dense passage retrieval put questions and passages in one space, the way assistants now find what to "
            "read before answering. Part 29 puts it to work."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tail))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
