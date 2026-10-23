from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai24.common import COLOR, NAME, PART, PIX, RAND, SPOKEN, SUP, axes, load, pct, take_away

ORDER = ["supervised", "simclr", "moco", "byol", "simsiam", "barlow", "vicreg", "dino", "matryoshka", "rotation", "mae",
         "beit", "ijepa", "random_cnn", "pixels"]


def hbars(rows, field, names, x0=-1.2, W=6.6, vmin=0.5, vmax=1.0, row_h=0.36, font_size=20):
    """Horizontal bars, one per method, with the spread of seeds as a whisker."""
    g = VGroup()
    X = lambda v: x0 + W * (v - vmin) / (vmax - vmin)  # noqa: E731
    for i, n in enumerate(names):
        r = rows[n]
        m, lo, hi = r[field]
        y = 2.6 - i * row_h
        col = COLOR[n]
        b = Rectangle(width=max(X(m) - x0, 0.02), height=row_h * 0.7, stroke_width=0, fill_color=col,
                      fill_opacity=0.85).move_to([x0 + max(X(m) - x0, 0.02) / 2, y, 0])
        w = Line([X(lo), y, 0], [X(hi), y, 0], color=WHITE, stroke_width=1.5)
        nm = label(NAME[n], font_size=font_size, color=col).next_to([x0, y, 0], LEFT, buff=0.15)
        v = MathTex(pct(m), font_size=font_size + 2, color=col).next_to([max(X(hi), X(m)), y, 0], RIGHT, buff=0.12)
        row = VGroup(b, w, nm, v)
        row.bar, row.whisk, row.name_, row.val = b, w, nm, v
        g.add(row)
    return g


class Budget(VoiceoverScene):
    def construct(self):
        self.card()
        self.linear()
        self.few()
        self.finetune()
        self.geometry()
        self.rank()

    def card(self):
        card = chapter_card(13, r"Every method, one budget", r"Which way of learning without labels learned the most?",
                            lit=(), part=PART)
        with self.voiceover("Chapter thirteen. Every method, one budget."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def sorted_names(self, rows, field):
        learned = [n for n in ORDER if n not in ("supervised", "random_cnn", "pixels")]
        learned.sort(key=lambda n: -rows[n][field][0])
        return ["supervised"] + learned + ["random_cnn", "pixels"]

    def linear(self):
        c = load("compare")
        rows = c["rows"]
        names = self.sorted_names(rows, "linear")
        lo = min(rows[n]["linear"][1] for n in names)
        vmin = float(np.floor((lo - 0.02) * 20) / 20)
        g = hbars(rows, "linear", names, vmin=vmin)
        head = label(r"Linear probe, \ all $60{,}000$ labels", font_size=30).to_edge(UP, buff=0.3)
        axl = label(rf"test accuracy, \% \ (axis from ${pct(vmin, 0)}$); \ whiskers: lowest and highest seed",
                    font_size=18, color=GREY_B).to_edge(DOWN, buff=0.25)
        tg = tag(r"computed: \ the same network, \ " + rf"${int(c['steps'])}$ updates of ${int(c['batch'])}$ digits, "
                 r"\ three seeds", corner=UR)
        best = names[1]
        b, s_ = rows[best]["linear"][0], rows["supervised"]["linear"][0]
        worst = names[-3]
        un = rows["random_cnn"]["linear"][0]
        below = [n for n in names[1:-2] if rows[n]["linear"][0] < un]
        if len(below) > 1:
            below_s = f"{len(below)} of the learned methods score below the untrained network."
        elif below:
            below_s = f"One learned method scores below the untrained network: {SPOKEN.get(below[0], below[0])}."
        else:
            below_s = "Every learned method beats the untrained network."
        with self.voiceover(
            "Here is every method, trained on the same network for the same number of steps, from three random "
            "starts, judged by a linear probe with all the labels. <bookmark mark='a'/> At the top, for "
            f"reference, the supervised network: {pct(s_)} percent. <bookmark mark='b'/> The best method without "
            f"labels is {SPOKEN.get(best, best)}, at {pct(b)} percent, {pct(s_ - b)} points behind. <bookmark "
            f"mark='c'/> At the bottom of the learned methods, {SPOKEN.get(worst, worst)}, with "
            f"{pct(rows[worst]['linear'][0])}; the untrained network scores {pct(un)}, and the raw pixels "
            f"{pct(rows['pixels']['linear'][0])}. <bookmark mark='d'/> {below_s}"
        ) as vo:
            self.play(FadeIn(head), FadeIn(axl), FadeIn(tg))
            self.play(FadeIn(g[0]))
            vo.wait_until("a")
            self.play(Indicate(g[0], color=SUP, scale_factor=1.02))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g[1:-2]], lag_ratio=0.15), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(g[-2:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def few(self):
        c = load("compare")
        rows = c["rows"]
        names = self.sorted_names(rows, "few")
        lo = min(rows[n]["few"][1] for n in names)
        vmin = float(np.floor((lo - 0.02) * 10) / 10)
        g = hbars(rows, "few", names, vmin=vmin)
        head = label(r"The harder test: \ only $10$ labels per digit", font_size=30).to_edge(UP, buff=0.3)
        axl = label(rf"test accuracy, \% \ (axis from ${pct(vmin, 0)}$); \ five draws of the $100$ labels per run",
                    font_size=18, color=GREY_B).to_edge(DOWN, buff=0.25)
        best = names[1]
        b = rows[best]["few"][0]
        s_ = rows["supervised"]["few"][0]
        px = rows["pixels"]["few"][0]
        lin_best = self.sorted_names(rows, "linear")[1]
        same = best == lin_best
        lead = SPOKEN.get(best, best)
        v = (f"The leader is the same: {lead}, with {pct(b)} percent from a hundred labels." if same else
             f"The order changes: {SPOKEN.get(best, best)} leads here, with {pct(b)} percent from a hundred labels, "
             f"while {SPOKEN.get(lin_best, lin_best)}, the best on the full probe, gets "
             f"{pct(rows[lin_best]['few'][0])}.")
        with self.voiceover(
            "The full probe flatters everyone: with sixty thousand labels, even raw pixels do well. The question "
            "self-supervised learning was invented for is what you can do with very few labels. <bookmark "
            "mark='a'/> So: a linear classifier from ten labelled digits of each kind. <bookmark mark='b'/> "
            f"{v} <bookmark mark='c'/> The raw pixels manage {pct(px)}; the supervised network, which was trained "
            f"with all sixty thousand labels before its ten-per-digit probe, {pct(s_)}. That gap, between "
            f"{pct(px)} and {pct(b)}, is what the unlabelled digits taught."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.1), run_time=3.0)
            vo.wait_until("b")
            self.play(Indicate(g[1], color=COLOR[best], scale_factor=1.03))
            vo.wait_until("c")
            self.play(Indicate(g[-1], color=PIX, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def finetune(self):
        f = load("finetune")
        acc = f["acc"]
        names = [n for n in ORDER if n in acc] + ["scratch"]
        rows = {n: {"ft": [float(np.mean(acc[n])), float(np.min(acc[n])), float(np.max(acc[n]))]} for n in names}
        order = sorted([n for n in names if n != "scratch"], key=lambda n: -rows[n]["ft"][0]) + ["scratch"]
        COLOR["scratch"], NAME["scratch"] = RAND, r"from scratch"
        lo = min(rows[n]["ft"][1] for n in order)
        vmin = float(np.floor((lo - 0.02) * 10) / 10)
        g = hbars(rows, "ft", order, vmin=vmin)
        head = label(rf"Fine-tune the whole network \ from $10$ labels per digit", font_size=30).to_edge(UP, buff=0.3)
        axl = label(rf"test accuracy, \% \ (axis from ${pct(vmin, 0)}$); \ ${int(f['steps'])}$ updates, \ three draws "
                    r"of the labels", font_size=18, color=GREY_B).to_edge(DOWN, buff=0.25)
        sc = rows["scratch"]["ft"][0]
        best = [n for n in order if n not in ("scratch", "supervised")][0]
        mae, ij = rows["mae"]["ft"][0], rows["ijepa"]["ft"][0]
        lin = {n: load("compare")["rows"][n]["few"][0] for n in ("mae", "ijepa") if n in load("compare")["rows"]}
        mv = (f"The masked models gain the most from it: MAE goes from {pct(lin['mae'])} percent with a frozen "
              f"network to {pct(mae)} fine-tuned, I-JEPA from {pct(lin['ijepa'])} to {pct(ij)}." if
              mae - lin.get("mae", mae) > 0.05 else
              f"Fine-tuning helps the masked models less than the literature would suggest: MAE ends at {pct(mae)} "
              f"percent, I-JEPA at {pct(ij)}.")
        ssl = [n for n in order if n not in ("scratch", "supervised")]
        n_up = sum(rows[n]["ft"][0] > sc for n in ssl)
        with self.voiceover(
            "A frozen network is one test. The other common one lets the whole network change, starting from what "
            "it learned, with the same hundred labels. <bookmark mark='a'/> Trained from scratch on a hundred "
            f"digits, our network reaches {pct(sc)} percent. <bookmark mark='b'/> Of the {len(ssl)} self-supervised "
            f"starts, {n_up} beat that; the best is {SPOKEN.get(best, best)}, at {pct(rows[best]['ft'][0])}. "
            f"<bookmark mark='c'/> {mv}"
        ) as vo:
            self.play(FadeIn(head), FadeIn(axl), FadeIn(g[-1]))
            vo.wait_until("a")
            self.play(Indicate(g[-1], color=RAND, scale_factor=1.02))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g[:-1]], lag_ratio=0.12), run_time=3.0)
            vo.wait_until("c")
            idx = [order.index(n) for n in ("mae", "ijepa") if n in order]
            self.play(*[Indicate(g[i], scale_factor=1.03) for i in idx])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def geometry(self):
        from scipy.stats import spearmanr

        c = load("compare")
        rows = c["rows"]
        names = [n for n in ORDER if n not in ("random_cnn", "pixels") and "align_h" in rows[n]]
        al = np.array([rows[n]["align_h"][0] for n in names])
        un = np.array([rows[n]["unif_h"][0] for n in names])
        ac = np.array([rows[n]["linear"][0] for n in names])
        ax = axes([float(un.min()) - 0.1, float(un.max()) + 0.1], [0, float(al.max()) * 1.2], x_length=7.0,
                  y_length=4.2, xlabel=r"$\mathcal L_{\rm uniform}$ of $h$ \ (lower: more spread)",
                  ylabel=r"$\mathcal L_{\rm align}$ of $h$", center=[-1.4, -0.3, 0])
        dots = VGroup()
        for n, x, y in zip(names, un, al):
            d = Dot(ax.ax.c2p(x, y), radius=0.08, color=COLOR[n])
            dots.add(VGroup(d, label(NAME[n], font_size=16, color=COLOR[n]).next_to(d, UR, buff=0.04)))
        ru = float(spearmanr(un, ac).correlation)
        ra = float(spearmanr(al, ac).correlation)
        res = VGroup(label(r"rank correlation with the linear probe", font_size=20, color=GREY_A),
                     label(rf"uniformity: \ ${ru:+.2f}$", font_size=24, color="#58A6FF"),
                     label(rf"alignment: \ ${ra:+.2f}$", font_size=24, color="#5BD17A")).arrange(DOWN,
                                                                                               aligned_edge=LEFT,
                                                                                               buff=0.12)
        res.to_corner(DR, buff=0.5)
        if ru < -0.5 and ra < -0.5:
            v = (f"Lower is better for both, so Wang and Isola predict negative correlations, and both are: "
                 f"{ru:.2f} for uniformity, {ra:.2f} for alignment.")
        elif ru < -0.5:
            v = (f"Lower is better for both, so Wang and Isola predict negative correlations. Uniformity's is strong, "
                 f"{ru:.2f}; alignment's is only {ra:.2f}: methods that keep their points spread do better, however "
                 "tightly they hold the views together.")
        elif ra < -0.5:
            v = (f"Lower is better for both, so Wang and Isola predict negative correlations. Alignment's is strong, "
                 f"{ra:.2f}; uniformity's is only {ru:.2f}.")
        else:
            v = (f"Lower is better for both, so Wang and Isola predict negative correlations; across our methods both "
                 f"are weak: {ru:.2f} for uniformity, {ra:.2f} for alignment.")
        tg = tag(r"computed: \ every method's encoder output $h$, \ mean of three seeds", corner=UR)
        with self.voiceover(
            "Chapter five's two numbers can be measured on every method's representation, not just SimCLR's. "
            "<bookmark mark='a'/> Here each method sits at its uniformity and alignment. <bookmark mark='b'/> " + v
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rank(self):
        c = load("compare")
        rows = c["rows"]
        names = [n for n in ORDER if n not in ("random_cnn", "pixels")]
        rk = np.array([rows[n]["rank"][0] for n in names])
        ac = np.array([rows[n]["few"][0] for n in names])
        from scipy.stats import spearmanr

        rho = float(spearmanr(rk, ac).correlation)
        ax = axes([0, max(rk) * 1.15], [float(np.floor(ac.min() * 10) / 10), 1.0], x_length=7.0, y_length=4.2,
                  xlabel=r"effective rank of $h$ \ (2{,}000 test digits)", ylabel=r"10 labels per digit",
                  center=[-1.0, -0.3, 0])
        dots = VGroup()
        for n, x, y in zip(names, rk, ac):
            d = Dot(ax.ax.c2p(x, y), radius=0.08, color=COLOR[n])
            dots.add(VGroup(d, label(NAME[n], font_size=16, color=COLOR[n]).next_to(d, UR, buff=0.04)))
        src = cite(r"RankMe: \ Garrido, Balestriero, Najman \& LeCun (2023)", corner=UR)
        res = label(rf"Spearman's rank correlation: \ ${rho:+.2f}$".replace("+", r"+"), font_size=26,
                    color=C.BITS).to_corner(DR, buff=0.5)
        if rho > 0.5:
            v = (f"Across our methods, the rank correlation is {rho:.2f}: a fuller representation usually means a "
                 "better one, as RankMe found.")
        elif rho > 0.2:
            v = f"Across our methods, the rank correlation is only {rho:.2f}: a hint, not a rule."
        else:
            v = (f"Across our methods, the rank correlation is {rho:.2f}: no useful relation. Filling the dimensions "
                 "does not, by itself, make them useful.")
        tk = take_away(r"judge a representation on the task you care about: \ here, \ learning from ten labels")
        with self.voiceover(
            "Can you tell which representation is good without any labels at all? Quentin Garrido and colleagues "
            "proposed the effective rank: in their experiments, the methods whose vectors filled more dimensions "
            "did better downstream. <bookmark mark='a'/> Here is the effective rank of each of our methods against "
            f"its ten-label accuracy. <bookmark mark='b'/> {v}"
        ) as vo:
            self.play(FadeIn(ax), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(res))
            self.play(FadeIn(tk, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
