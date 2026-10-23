from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai24.common import (COLOR, NAME, PART, PIX, RAND, SPOKEN, SUP, axes, load, pct, place_labels, tag,
                                   take_away, take_away_in)

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
        self.caveats()

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
                 r"\ three seeds", corner=UR).next_to(head, DOWN, buff=0.08)
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
        crow = load("compare")["rows"]
        names = [n for n in ORDER if n in acc] + ["scratch"]
        rows = {n: {"ft": [float(np.mean(acc[n])), float(np.min(acc[n])), float(np.max(acc[n]))]} for n in names}
        order = sorted([n for n in names if n != "scratch"], key=lambda n: -rows[n]["ft"][0]) + ["scratch"]
        COLOR["scratch"], NAME["scratch"] = RAND, r"from scratch"
        fewp = {n: crow[n]["few"][0] for n in order if n in crow}
        lo = min([rows[n]["ft"][1] for n in order] + list(fewp.values()))
        vmin = float(np.floor((lo - 0.02) * 10) / 10)
        g = hbars(rows, "ft", order, vmin=vmin)
        X = lambda v: -1.2 + 6.6 * (v - vmin) / (1.0 - vmin)  # noqa: E731  (hbars' default x0 and W)
        ticks = VGroup()
        for i, n in enumerate(order):
            if n in fewp:
                y = g[i].bar.get_y()
                ticks.add(Line([X(fewp[n]), y - 0.16, 0], [X(fewp[n]), y + 0.16, 0], color=YELLOW, stroke_width=4))
                if X(fewp[n]) + 0.05 > g[i].val.get_left()[0]:  # keep the value clear of the tick
                    g[i].val.next_to([X(fewp[n]), y, 0], RIGHT, buff=0.12)
        head = label(rf"Fine-tune the whole network \ from $10$ labels per digit", font_size=30).to_edge(UP, buff=0.3)
        axl = label(rf"test accuracy, \% \ (axis from ${pct(vmin, 0)}$); \ ${int(f['steps'])}$ updates, \ three draws "
                    r"of the labels; \\ yellow tick: \ the frozen network's probe from the same $100$ labels",
                    font_size=18, color=GREY_B).to_edge(DOWN, buff=0.25)
        sc = rows["scratch"]["ft"][0]
        ssl = [n for n in order if n not in ("scratch", "supervised")]
        best = ssl[0]
        mae, ij = rows["mae"]["ft"][0], rows["ijepa"]["ft"][0]
        gain = {n: rows[n]["ft"][0] - fewp[n] for n in ssl}
        top3 = sorted(ssl, key=lambda n: -gain[n])[:3]
        if "mae" in top3 and "ijepa" in top3:
            mv = (f"The masked models gain the most from it: MAE goes from {pct(fewp['mae'])} percent with a frozen "
                  f"network to {pct(mae)} fine-tuned, I-JEPA from {pct(fewp['ijepa'])} to {pct(ij)}.")
        else:
            mv = (f"Fine-tuning helps the masked models less than the literature would suggest: MAE ends at {pct(mae)} "
                  f"percent, I-JEPA at {pct(ij)}.")
        if mae < sc + 0.01:
            mv2 = (f"But that only brings MAE back to where training from scratch gets, {pct(sc)} percent: its "
                   "pre-training gave no head start.")
        else:
            mv2 = f"MAE ends {pct(mae - sc)} points above training from scratch."
        bf = max(ssl, key=lambda n: fewp[n])
        if gain[bf] < -0.005:
            keep = (f"And for the best networks, the frozen probe was the better use of the hundred labels: "
                    f"{SPOKEN.get(bf, bf)} scores {pct(fewp[bf])} percent frozen and {pct(rows[bf]['ft'][0])} "
                    "fine-tuned. With so few labels, moving every weight can undo part of what was learned.")
        else:
            keep = (f"{SPOKEN.get(bf, bf)}, the best frozen network, goes from {pct(fewp[bf])} percent frozen to "
                    f"{pct(rows[bf]['ft'][0])} fine-tuned.")
        n_up = sum(rows[n]["ft"][0] > sc for n in ssl)
        with self.voiceover(
            "A frozen network is one test. The other common one lets the whole network change, starting from what "
            "it learned, with the same hundred labels. <bookmark mark='a'/> Trained from scratch on a hundred "
            f"digits, our network reaches {pct(sc)} percent. <bookmark mark='b'/> Of the {len(ssl)} self-supervised "
            f"starts, {n_up} beat that; the best is {SPOKEN.get(best, best)}, at {pct(rows[best]['ft'][0])}. "
            f"<bookmark mark='c'/> {mv} <bookmark mark='d'/> {mv2} <bookmark mark='e'/> {keep}"
        ) as vo:
            self.play(FadeIn(head), FadeIn(axl), FadeIn(g[-1]))
            vo.wait_until("a")
            self.play(Indicate(g[-1], color=RAND, scale_factor=1.02))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g[:-1]], lag_ratio=0.12), run_time=3.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.05), run_time=1.5)
            idx = [order.index(n) for n in ("mae", "ijepa") if n in order]
            self.play(*[Indicate(g[i], scale_factor=1.03) for i in idx])
            vo.wait_until("d")
            self.play(Indicate(g[-1], color=RAND, scale_factor=1.03))
            vo.wait_until("e")
            self.play(Indicate(g[order.index(bf)], color=COLOR[bf], scale_factor=1.03))
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
            dots.add(VGroup(d, label(NAME[n], font_size=16, color=COLOR[n])))
        place_labels([g_[0] for g_ in dots], [g_[1] for g_ in dots])
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
            dots.add(VGroup(d, label(NAME[n], font_size=16, color=COLOR[n])))
        place_labels([g_[0] for g_ in dots], [g_[1] for g_ in dots])
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
            self.play(*take_away_in(self, tk))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def caveats(self):
        c = load("compare")
        rows = c["rows"]
        ssl = [n for n in ORDER if n not in ("supervised", "random_cnn", "pixels")]
        un = rows["random_cnn"]["few"][0]
        good = [n for n in ssl if rows[n]["few"][0] > un + 0.01]
        pts = VGroup(
            label(r"one small network, \ 800 updates, \ ten kinds of digit", font_size=26),
            label(r"methods whose recipes train far longer \ (DINO, \ masked models) \ may be at a disadvantage here",
                  font_size=26),
            label(r"at ImageNet scale, \ with vision transformers, \ the order differs: \\ DINOv2 and DINOv3 lead "
                  r"self-supervised frozen probes; \ masked models do well after fine-tuning", font_size=26),
            label(rf"here: \ ${len(good)}$ of ${len(ssl)}$ methods beat the untrained network \ with ten labels per "
                  r"digit", font_size=26, color=C.BITS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(UP * 0.2)
        head = label(r"How to read this scoreboard", font_size=34).to_edge(UP, buff=0.5)
        with self.voiceover(
            "How far should this scoreboard be trusted? It is one small network, eight hundred updates, ten kinds of "
            "digit. <bookmark mark='a'/> Methods whose published recipes train for hundreds of passes over the data, "
            "DINO and the masked models, may be at a disadvantage on a budget this short. <bookmark mark='b'/> At ImageNet scale, with vision "
            "transformers, the order is different: the DINO line leads the self-supervised methods on frozen features, and masked "
            "models do well "
            f"once fine-tuned. <bookmark mark='c'/> Here, {len(good)} of the {len(ssl)} methods learned enough about "
            "digits, without a single label, to beat the untrained network when only ten labels per digit are given."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pts[0]))
            vo.wait_until("a")
            self.play(FadeIn(pts[1]))
            vo.wait_until("b")
            self.play(FadeIn(pts[2]))
            vo.wait_until("c")
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()
