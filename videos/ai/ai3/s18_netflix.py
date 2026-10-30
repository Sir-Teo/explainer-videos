from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import HIST, chapter, dots_on, load
from videos.ai.ai3.compute import ratings_world

GEN_COLORS = ["#F2A541", "#58A6FF", "#E85D75", "#D4A5FF", "#5BD17A", "#4FD1C5"]
TRC, TEC = C.TRUE_P, C.MODEL_Q
TT, POP = C.REWARD, GREY_B


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
        img.stretch_to_fit_width(6.0).stretch_to_fit_height(3.7).move_to([-3.5, -0.6, 0])
        frame = SurroundingRectangle(img, buff=0, color=GREY_D, stroke_width=1.2)
        xl = label(r"films", font_size=22, color=GREY_A).next_to(frame, UP, buff=0.1)
        yl = label(r"users", font_size=22, color=GREY_A).next_to(frame, LEFT, buff=0.1)
        tag = note(rf"a corner of our synthetic ratings: \ ${100 * m['density']:.1f}\%$ of cells filled; \ red $1$ "
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
            vo.wait_until("b")
            self.play(FadeIn(img), Create(frame), FadeIn(xl), FadeIn(yl), FadeIn(tag))
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
            cmath(r"\min", r"\textstyle\sum_{(u,i)\ \text{rated}}", r"(r_{ui} - \hat r_{ui})^2 + \lambda\big(|\mathbf{p}_u|^2 + "
                  r"|\mathbf{q}_i|^2\big)", font_size=36),
        ]
        whys = [why(r"an average, \ how generous the user is, \ how good the film is, \\ and a rank-$k$ taste match"),
                why(r"only the cells we have; \ $\lambda$ keeps the vectors small")]
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
            "the vectors small. <bookmark mark='c'/> A full table would have chapter eight's answer; with holes there is "
            "no formula, and we descend the gradient. <bookmark mark='d'/> We built a small world to test on: "
            f"{m['users']:,} users, {m['items']:,} films, {m['n_ratings']:,} ratings, from six hidden genres the method "
            "never sees."
        ) as vo:
            vo.wait_until("a")
            step(0)
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
        lo = float(min(h[:, 1].min(), h0[:, 1].min())) - 0.03
        hi = float(min(1.3, max(h[:, 2].max(), h0[:, 2].max()))) + 0.03
        ga = axes([0, E, 10], [lo, hi, 0.1], x_length=5.6, y_length=3.6, xticks=[0, 10, 20, 30, 40],
                  yticks=[round(v, 1) for v in np.arange(np.ceil(lo * 10) / 10, hi, 0.1)],
                  xlabel=r"pass over the ratings", ylabel=r"error (root mean square, stars)", center=[-3.5, -0.6, 0])
        ax = ga.ax
        ep = h[:, 0]
        tr, te = curve(ax, ep, np.clip(h[:, 1], lo, hi), TRC, 3), curve(ax, ep, np.clip(h[:, 2], lo, hi), TEC, 3)
        tr0 = DashedVMobject(curve(ax, ep, np.clip(h0[:, 1], lo, hi), TRC, 2), num_dashes=40)
        te0 = DashedVMobject(curve(ax, ep, np.clip(h0[:, 2], lo, hi), TEC, 2), num_dashes=40)
        leg = legend([(TRC, r"ratings it trained on"), (TEC, r"held-out ratings"),
                      (GREY_B, rf"dashed: \ no penalty, \ $\lambda = 0$")], font_size=20).next_to(ga, UP, buff=0.1)
        Q = np.asarray(m["q_snaps"])
        gen = np.asarray(m["genre"])
        eps_ = [int(e) for e in m["q_snap_epochs"]]
        lim = float(np.percentile(np.abs(Q[-1]), 99)) * 1.1
        gb = Axes(x_range=[-lim, lim, lim], y_range=[-lim, lim, lim], x_length=4.2, y_length=4.2, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([3.6, -0.4, 0])
        sub = np.arange(0, Q.shape[1], 2)
        t = ValueTracker(0)

        def film_dots():
            v = t.get_value()
            i = int(min(np.floor(v), len(eps_) - 2))
            a = v - i
            P = (1 - a) * Q[i] + a * Q[i + 1]
            return VGroup(*[Dot(gb.c2p(*np.clip(P[j], -lim, lim)), radius=0.03, color=GEN_COLORS[gen[j]],
                                fill_opacity=0.8) for j in sub])

        fd = always_redraw(film_dots)
        ep_read = always_redraw(lambda: label(rf"film vectors after {eps_[int(round(t.get_value()))]} passes" if
                                              t.get_value() > 0.01 else r"film vectors at the start", font_size=22,
                                              color=GREY_A).next_to(gb, UP, buff=0.12))
        gl = VGroup(*[label(nm, font_size=18, color=c_) for nm, c_ in zip(m["genres"], GEN_COLORS)])
        gl.arrange_in_grid(rows=2, cols=3, buff=(0.2, 0.08)).next_to(gb, DOWN, buff=0.12)
        best, worst0 = float(h[:, 2].min()), float(h0[:, 2].min())
        last0 = float(h0[-1, 2])
        overfit = last0 > worst0 + 0.01
        tail = (f" Without the penalty the held-out error bottoms out at {worst0:.3f} and climbs back to {last0:.3f}: "
                "the vectors memorize the training ratings." if overfit else
                " Without the penalty it ends a little worse.")
        with self.voiceover(
            f"Training replayed, at rank {int(rp['rank'])}. <bookmark mark='a'/> The error falls on the ratings it "
            f"trains on, and on held-out ones: from {h[0, 2]:.2f} stars to {h[-1, 2]:.3f}.{tail} "
            "<bookmark mark='b'/> On the right, each film's vector, on its two strongest directions, coloured by the "
            "hidden genre. <bookmark mark='c'/> The genres pull apart. Of each film's ten nearest films, "
            f"{100 * m['genre_nn']:.0f} percent share its genre, against {100 * m['genre_chance']:.0f} percent by "
            "chance."
        ) as vo:
            self.play(FadeIn(ga), FadeIn(leg), Create(gb), FadeIn(gl))
            self.add(fd, ep_read)
            vo.wait_until("a")
            self.play(Create(tr), Create(te), run_time=2.0)
            self.play(Create(tr0), Create(te0), run_time=1.5)
            vo.wait_until("b")
            self.play(t.animate.set_value(2), run_time=2.0)
            vo.wait_until("c")
            self.play(t.animate.set_value(len(eps_) - 1), run_time=3.0)
        fd.clear_updaters()
        ep_read.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ranks(self):
        m = load("mf")
        ks = sorted(int(k) for k in m["test_rmse"])
        vals = {k: np.asarray(m["test_rmse"][str(k)]) for k in ks}
        lo = float(min(v.min() for v in vals.values())) - 0.03
        hi = float(m["rmse_mean"]) + 0.03
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
        cap = note(r"three seeds per rank; \ $\lambda$ chosen on separate validation ratings").to_corner(DR, buff=0.25)
        why_best = (", near the six genres we hid; beyond that, extra directions fit noise." if best in (4, 8) else ".")
        with self.voiceover(
            f"How much taste does it take? The average rating misses by {m['rmse_mean']:.3f} stars. "
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
        tag = note(r"schematic").next_to(both, DOWN, buff=0.2)
        g = axes([0, float(steps[-1]), 1000], [0, 0.3, 0.1], x_length=5.4, y_length=3.4, xticks=[0, 1000, 2000, 3000],
                 yticks=[0, 0.1, 0.2, 0.3], xlabel=r"training step", ylabel=r"recall at $10$ \ (held-out films)",
                 center=[3.4, -0.5, 0])
        ax = g.ax
        cw = curve(ax, steps, curve_[:, 4], TT, 3)
        cc = curve(ax, steps, curve_[:, 5], C.BITS, 3)
        pw = DashedLine(ax.c2p(0, t["pop_warm"]), ax.c2p(steps[-1], t["pop_warm"]), color=POP)
        pc = DashedLine(ax.c2p(0, t["pop_cold"]), ax.c2p(steps[-1], t["pop_cold"]), color=POP)
        leg = legend([(TT, r"two towers: \ users it trained on"), (C.BITS, r"two towers: \ new users, \ $5$ films each"),
                      (POP, r"dashed: \ most popular films")], font_size=18).next_to(g, UP, buff=0.1)
        rw, rc = t["recall_warm_prior"], t["recall_cold_prior"]
        bw = rw > t["pop_warm"]
        bc = rc > t["pop_cold"]
        if bw and bc:
            verdict = "Both beat recommending the most popular films."
        elif bw:
            verdict = "For users it trained on it beats popularity; for brand-new users it does not, yet."
        elif bc:
            verdict = "It beats popularity for new users, but not for the users it trained on."
        else:
            verdict = "Neither beats simply recommending the most popular films: in this world popularity is a strong signal."
        with self.voiceover(
            "Factorization has a weakness: a new user has no vector. Today's recommenders use two towers. "
            "<bookmark mark='a'/> One network turns a user's history into a vector, another a film's details; the score "
            "is their dot product. <bookmark mark='b'/> Trained so each user's real films outscore the batch, corrected "
            "for popularity, the score learns a pointwise mutual information, chapter twelve's quantity; popularity is "
            "added back to recommend. <bookmark mark='c'/> The share of held-out favourites in the top ten reaches "
            f"{rw:.2f} for known users and {rc:.2f} for new ones, from five films each; popularity alone gets "
            f"{t['pop_warm']:.2f} and {t['pop_cold']:.2f}. {verdict}"
        ) as vo:
            self.play(FadeIn(both), FadeIn(tag), FadeIn(g))
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
