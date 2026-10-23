from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai18.common import (DUP, F, KEPT, MONO, PAGE, PART, REMOVED, load, node_box, said, spoken_int, stat,
                                   take_away)


def url_text(u: str, n: int = 60, font_size: int = 17, color=PAGE):
    """A web address on screen: data, never translated."""
    u = u.replace("https://", "").replace("http://", "")
    return data_text(u if len(u) <= n else u[:n - 3] + "...", font=MONO, font_size=font_size, color=color)


class Dedup(VoiceoverScene):
    def construct(self):
        self.card()
        self.why_dedup()
        self.minhash()
        self.bands()
        self.found()

    def card(self):
        card = chapter_card(3, r"Near-duplicates: \ MinHash and LSH", r"How do you find copies among billions of "
                            r"pages, without comparing every pair?", part=PART)
        with self.voiceover("Chapter three. Near-duplicates: MinHash and locality-sensitive hashing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def why_dedup(self):
        D = load("dedup")
        ex = next((e for e in D["examples"] if "dollargeneral" in e["url_a"]), D["examples"][0])
        pair = VGroup(
            url_text(ex["url_a"]),
            url_text(ex["url_b"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        pj = label(rf"two pages of our sample: \ ${100 * ex['jaccard']:.0f}\%$ of their five-word phrases shared",
                   font_size=22, color=DUP)
        top = VGroup(pj, pair).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(UP, buff=0.5)
        # shingles: a sentence and its overlapping five-word pieces
        words = "the quick brown fox jumps over the lazy dog".split()
        row = VGroup(*[label(w, font_size=24, color=WHITE) for w in words]).arrange(RIGHT, buff=0.18)
        row.move_to([0, 0.6, 0])
        braces = VGroup()
        for i in range(len(words) - 4):
            br = Line(row[i].get_bottom() + DOWN * (0.15 + 0.12 * i), row[i + 4].get_bottom() + DOWN * (0.15 + 0.12 * i),
                      color=DUP, stroke_width=3)
            braces.add(br)
        sl = label(r"a document's shingles: \ its overlapping five-word phrases", font_size=20, color=DUP)
        sl.next_to(braces, DOWN, buff=0.2)
        jac = definition_card(r"Jaccard similarity", cmath(r"J(A, B)", r"=", r"\frac{|A \cap B|}{|A \cup B|}",
                                                           font_size=34), color=DUP, width=5.4)
        jac.move_to([-3.4, -2.2, 0])
        cost = VGroup(label(r"every pair of $n$ pages: \ $n^2/2$ comparisons", font_size=22, color=GREY_A),
                      label(r"$n = 10^{10}$: \ $5 \times 10^{19}$", font_size=26, color=REMOVED)).arrange(DOWN, buff=0.15)
        cost.move_to([3.4, -2.2, 0])
        src = cite(r"Lee et al., \textit{Deduplicating training data makes language models better} (2022)",
                   corner=DR, font_size=17)
        heads = VGroup()
        if ex.get("head_a"):
            heads = VGroup(said(ex["head_a"], chars=46, font_size=15, max_lines=5, box_color=DUP),
                           said(ex["head_b"], chars=46, font_size=15, max_lines=5, box_color=DUP)).arrange(RIGHT, buff=0.4)
            heads.scale_to_fit_width(min(heads.width, 12.6)).next_to(top, DOWN, buff=0.35)
        ten = stat(r"$10\times$", r"less memorized training text emitted, \ after deduplication \ (Lee et al., 2022)",
                   color=DUP, font_size=52, cap_size=20).move_to([0, -2.1, 0])
        with self.voiceover(
            "The web repeats itself. Mirrors, templates, the same product page with another price. "
            f"<bookmark mark='a'/> These two pages from our sample come from one site: "
            f"{100 * ex['jaccard']:.0f} percent of their phrases are the same. <bookmark mark='b'/> Duplicates waste "
            "compute, and they get memorized: Lee and colleagues found in 2022 that models trained on deduplicated "
            "data reproduce their training text ten times less often. <bookmark mark='c'/> To compare documents, "
            "cut each into shingles, its overlapping five-word phrases, as FineWeb does. <bookmark mark='d'/> Two "
            "documents are similar if their sets of shingles overlap: the Jaccard similarity, the size of the "
            "intersection over the size of the union. <bookmark mark='e'/> But comparing every pair of ten billion "
            "pages is five times ten to the nineteen comparisons. We need a shortcut."
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("a")
            self.play(Indicate(pair, color=DUP, scale_factor=1.02), FadeIn(heads, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(src), FadeIn(ten, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeOut(heads), FadeOut(ten))
            self.play(FadeIn(row), LaggedStart(*[Create(b) for b in braces], lag_ratio=0.3), FadeIn(sl), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(jac, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(cost, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def minhash(self):
        D = load("dedup")
        s, a = np.asarray(D["pair_s"]), np.asarray(D["pair_agree"])
        th = theorem_card(r"MinHash", r"For a random hash $h$: \ $\Pr\big[\min_{x \in A} h(x) = \min_{x \in B} h(x)\big]"
                          r" = J(A, B)$", who=r"Andrei Broder, 1997 (AltaVista)", color=DUP, width=7.4, font_size=22)
        th.to_edge(UP, buff=0.35)
        colors = {r"J": DUP}
        rows = [
            cmath(r"\text{smallest } h \text{ over } A \cup B", r"=", r"\text{any element, equally likely}", font_size=28),
            cmath(r"\min_A h = \min_B h", r"\iff", r"\text{that element} \in A \cap B", font_size=28),
            cmath(r"\Pr[\text{agree}]", r"=", r"\frac{|A \cap B|}{|A \cup B|}", r"=", r"J", colors=colors, font_size=30),
        ]
        whys = [why(r"$h$ is random: \ symmetry", font_size=20), why(r"the minimum of $A \cup B$ sits in both", font_size=20),
                why(r"count the favourable cases", font_size=20)]
        step = ladder(self, rows, whys, keep=3, top=1.3, x=-3.2, buff=0.45, edge=6.9)
        g = axes([0, 1], [0, 1], x_length=3.6, y_length=3.0, xlabel=r"true $J$", ylabel=r"share of $112$ minhashes equal",
                 xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], center=[4.4, -1.6, 0], font_size=18)
        idx = np.random.default_rng(0).choice(len(s), 500, replace=False)
        pts = VGroup(*[Dot(g.ax.c2p(s[i], a[i]), radius=0.022, color=DUP, fill_opacity=0.6) for i in idx])
        diag = DashedLine(g.ax.c2p(0, 0), g.ax.c2p(1, 1), color=GREY_B, dash_length=0.05)
        mtag = note(rf"computed: \ ${len(s):,}$ page pairs; \ mean gap ${D['agree_err']:.3f}$".replace(",", "{,}"),
                    font_size=18).next_to(g, DOWN, buff=0.1)
        # the two sets of shingles, each shingle with its hash (schematic numbers)
        ea = Ellipse(width=3.6, height=1.9, stroke_color=PAGE, stroke_width=2.5).move_to([-4.0, -2.45, 0])
        eb = Ellipse(width=3.6, height=1.9, stroke_color=DUP, stroke_width=2.5).move_to([-2.0, -2.45, 0])
        la = label(r"$A$", font_size=24, color=PAGE).next_to(ea, LEFT, buff=0.1)
        lb = label(r"$B$", font_size=24, color=DUP).next_to(eb, RIGHT, buff=0.1)
        spots = {"a": [(-5.2, -2.1), (-5.0, -2.85), (-4.5, -2.45)], "ab": [(-3.3, -2.0), (-2.7, -2.0), (-3.0, -2.6),
                                                                          (-3.3, -3.0), (-2.7, -3.0)],
                 "b": [(-1.5, -2.1), (-1.0, -2.6), (-1.5, -2.95)]}
        hv = {"a": [71, 38, 90], "ab": [44, 12, 63, 57, 29], "b": [85, 23, 66]}
        hashes = VGroup()
        for k in ("a", "ab", "b"):
            for (x_, y_), v in zip(spots[k], hv[k]):
                hashes.add(label(rf"${v}$", font_size=22, color=GREY_A).move_to([x_, y_, 0]))
        lowest = hashes[3 + 1]  # 12, in both sets
        ring = Circle(radius=0.26, color=YELLOW, stroke_width=3).move_to(lowest)
        venn = VGroup(ea, eb, la, lb, hashes)
        vnote = note(r"each shingle's hash \ (schematic)", font_size=17).next_to(venn, DOWN, buff=0.06)
        vmin = label(r"smallest over $A \cup B$: \ $12$, \ in both \ $\Rightarrow$ \ $\min_A h = \min_B h$",
                     font_size=20, color=YELLOW).next_to(venn, RIGHT, buff=0.35).shift(DOWN * 0.1)
        with self.voiceover(
            "The shortcut is a beautiful fact from 1997, found by Andrei Broder at AltaVista to spot duplicate web "
            "pages. Give every shingle a random number, with a random hash function. <bookmark mark='a'/> "
            "Over the union of the two sets, the shingle with the smallest hash is equally likely to be any of "
            "them. <bookmark mark='b'/> The two documents' minimum hashes agree exactly when that shingle is in "
            "both, in the intersection. <bookmark mark='c'/> So the chance that they agree is the size of the "
            "intersection over the size of the union: the Jaccard similarity itself. <bookmark mark='d'/> Keep 112 "
            "such minimums per document, as FineWeb does: a signature, and the share of positions where two signatures "
            f"agree estimates the similarity. We checked it on {spoken_int(len(s))} pairs of our pages, one of each pair "
            f"with some words replaced: <bookmark mark='e'/> the estimate sits on the diagonal, off by "
            f"{D['agree_err']:.3f} on average."
        ) as vo:
            self.play(FadeIn(th, shift=UP * 0.1), FadeIn(venn), FadeIn(vnote))
            vo.wait_until("a")
            step(0)
            self.play(Create(ring), lowest.animate.set_color(YELLOW))
            vo.wait_until("b")
            step(1)
            self.play(FadeIn(vmin, shift=RIGHT * 0.1))
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(*[FadeOut(w) for w in whys], FadeOut(vmin))
            self.play(FadeIn(g), Create(diag))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.004), FadeIn(mtag), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bands(self):
        D = load("dedup")
        b, r = D["bands"], D["rows"]
        sig = VGroup(*[Rectangle(width=0.085, height=0.42, stroke_width=0, fill_color=DUP,
                                 fill_opacity=0.35 + 0.5 * ((k // r) % 2)) for k in range(b * r)]).arrange(RIGHT, buff=0.01)
        sig.to_edge(UP, buff=0.55)
        sl = label(rf"a signature of ${b * r}$ minhashes, \ cut into ${b}$ bands of ${r}$", font_size=22, color=DUP)
        sl.next_to(sig, DOWN, buff=0.15)
        colors = {r"s": DUP, r"r": GREY_A, r"b": GREY_A}
        rows = [
            cmath(r"\Pr[\text{one band all equal}]", r"=", r"s^{r}", colors=colors, font_size=28),
            cmath(r"\Pr[\text{no band equal}]", r"=", r"(1 - s^{r})^{b}", colors=colors, font_size=28),
            cmath(r"\Pr[\text{candidates}]", r"=", r"1 - (1 - s^{r})^{b}", colors=colors, font_size=30),
        ]
        whys = [why(r"$r$ independent agreements", font_size=20), why(r"$b$ independent bands", font_size=20),
                why(r"compare only pairs that share a band", font_size=20)]
        step = ladder(self, rows, whys, keep=3, top=1.35, x=-3.6, buff=0.4, edge=6.9)
        g = axes([0, 1], [0, 1], x_length=5.0, y_length=3.0, xlabel=r"Jaccard similarity $s$",
                 ylabel=r"chance of becoming a candidate", xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.5, 1],
                 center=[3.3, -1.75, 0], font_size=18)
        ss = np.linspace(0, 1, 200)
        pc = curve(g.ax, ss, 1 - (1 - ss ** r) ** b, DUP, 3)
        bins = D["bins"]
        meas = VGroup(*[Dot(g.ax.c2p(bn["s"], bn["measured"]), radius=0.06, color=WHITE) for bn in bins])
        half = DashedLine(g.ax.c2p(D["s_half"], 0), g.ax.c2p(D["s_half"], 0.5), color=GREY_B, dash_length=0.05)
        hl = label(rf"$s = {D['s_half']:.2f}$", font_size=18, color=GREY_A).next_to(g.ax.c2p(D["s_half"], 0.5), LEFT,
                                                                                buff=0.12)
        lg = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.4, color=DUP, stroke_width=4),
                           label(rf"predicted, \ $b = {b}$, $r = {r}$", font_size=18, color=DUP)).arrange(RIGHT, buff=0.1),
                    VGroup(Dot(radius=0.06, color=WHITE), label(r"measured, \ our page pairs", font_size=18))
                    .arrange(RIGHT, buff=0.1)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        lg.move_to(g.ax.c2p(0.03, 0.88), aligned_edge=UL)
        worst = max(abs(bn["measured"] - bn["predicted"]) for bn in bins)
        src = cite(r"Indyk \& Motwani (1998); \ Broder (1997); \ FineWeb (2024), App.\ E", corner=DL, font_size=17)
        with self.voiceover(
            "One signature per document still leaves every pair to compare. Locality-sensitive hashing avoids "
            f"that: cut the {b * r} minhashes into {b} bands of {r}. <bookmark mark='a'/> For two documents with "
            "similarity s, each minhash agrees with probability s, so a whole band of r agrees with probability s to "
            "the r. <bookmark mark='b'/> The chance that no band agrees is one minus s to the r, to the power b. "
            "<bookmark mark='c'/> And the chance that at least one does, making the pair a candidate, is one minus "
            "that. <bookmark mark='d'/> Now only documents that share a bucket in some band get compared, and the "
            "curve is an S: pairs below about 0.5 almost never collide, pairs above 0.8 almost always do, with the "
            f"halfway point at {D['s_half']:.2f}. <bookmark mark='e'/> And here are our measured pairs, binned by "
            f"similarity: they follow the formula, at most {worst:.2f} away in any bin."
        ) as vo:
            self.play(FadeIn(sig), FadeIn(sl))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(*[FadeOut(w) for w in whys])
            self.play(FadeIn(g), FadeIn(src))
            self.play(Create(pc), run_time=1.5)
            self.play(Create(half), FadeIn(hl), FadeIn(lg[0]))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(m, scale=1.5) for m in meas], lag_ratio=0.1), FadeIn(lg[1]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def found(self):
        D = load("dedup")
        O = F.OLMO3
        left = VGroup(
            label(r"our sample", font_size=28, color=PAGE),
            label(rf"${D['n']:,}$ English pages".replace(",", "{,}"), font_size=24, color=WHITE),
            label(rf"${D['exact']}$ exact copies, \ ${D['removed']}$ near-duplicates", font_size=24, color=DUP),
            label(rf"${100 * D['removed_share']:.1f}\%$ removed", font_size=24, color=REMOVED),
            label(r"the thirty Gutenberg files", font_size=28, color=PAGE),
            label(rf"licence pages: \ ${D['foot_caught']}$ of ${D['foot_pairs']}$ pairs caught \ "
                  rf"($J \ge {D['foot_jaccard'][0]:.2f}$)", font_size=24, color=DUP),
            label(rf"the novels themselves: \ ${D['body_caught']}$ of ${D['body_pairs']}$ pairs", font_size=24,
                  color=KEPT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-3.4, 0.4, 0])
        left[4].shift(DOWN * 0.25)
        left[5:].shift(DOWN * 0.25)
        # Olmo 3's pipeline at the scale of the whole web
        steps = [(r"$38.7$B documents", O["docs"][0]), (rf"exact: \ $-{O['exact']}\%$", O["docs"][1]),
                 (rf"MinHash: \ $-{O['fuzzy']}\%$ of the pool", O["docs"][2]),
                 (rf"substrings: \ $-{O['substring']}\%$ of bytes", O["docs"][3])]
        bars = VGroup()
        for i, (t, n) in enumerate(steps):
            w = 5.0 * n / O["docs"][0]
            bar = Rectangle(width=w, height=0.42, stroke_width=0, fill_color=PAGE if i == 0 else KEPT, fill_opacity=0.85)
            bar.move_to([1.2 + w / 2, 1.3 - 0.75 * i, 0])
            bars.add(VGroup(bar, label(t, font_size=20, color=WHITE).next_to(bar, UP, buff=0.06).align_to(bar, LEFT)))
        bh = label(r"Olmo 3's web pool, \ at scale", font_size=26, color=PAGE).next_to(bars, UP, buff=0.3).align_to(bars, LEFT)
        fw = label(r"FineWeb: \ deduplicating each crawl alone \\ beat deduplicating all $96$ together", font_size=22,
                   color=GREY_A).next_to(bars, DOWN, buff=0.45).align_to(bars, LEFT)
        src = cite(r"Team OLMo, Olmo 3 (2025), Sec.\ 3.4; \ Penedo et al.\ (2024); \ computed here", corner=DL,
                   font_size=17)
        lic = VGroup()
        if D.get("foot_head"):
            lic = VGroup(label(r"the last page of two of the books", font_size=20, color=GREY_A),
                         *[said(h, chars=40, font_size=15, max_lines=4, box_color=DUP) for h in D["foot_head"][:2]])
            lic.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.4, 0.3, 0])
        share = D["removed_share"]
        if share < 0.05:
            found = (f"In our {spoken_int(D['n'])} English pages, {D['exact']} exact copies and "
                     f"{D['removed']} near-duplicates: {100 * share:.1f} percent. Common Crawl already avoids fetching "
                     "the same address twice in a crawl, and our sample is tiny.")
        else:
            found = (f"In our {spoken_int(D['n'])} English pages, {D['exact']} exact copies and "
                     f"{D['removed']} near-duplicates: {100 * share:.1f} percent of the pages.")
        if D["foot_caught"] == D["foot_pairs"] and D["body_caught"] == 0:
            books = (f"Each ends with the same licence, with the book's title changed: LSH catches all "
                     f"{D['foot_pairs']} pairs of licences, and none of the {D['body_pairs']} pairs of novels.")
        else:
            books = (f"Each ends with the same licence, with the book's title changed: LSH catches "
                     f"{D['foot_caught']} of the {D['foot_pairs']} pairs of licences, and {D['body_caught']} of the "
                     f"{D['body_pairs']} pairs of novels.")
        with self.voiceover(
            "What did we find? " + found + " <bookmark mark='a'/> The thirty Gutenberg files of Part 1 are a "
            "clearer test. " + books +
            " <bookmark mark='b'/> At the scale of the whole web the numbers are dramatic. For Olmo 3, removing exact "
            f"copies cut the pool by {O['exact']} percent, MinHash removed another {O['fuzzy']} percent, and repeated "
            f"substrings {O['substring']} percent of the remaining bytes: 38.7 billion documents became 9.7 billion. "
            "<bookmark mark='c'/> And one surprise. FineWeb first deduplicated all 96 crawls against each other, and "
            "the models got worse: in the oldest crawls, what survived was the junk that nobody had copied. "
            "Deduplicating each crawl on its own worked better."
        ) as vo:
            self.play(FadeIn(left[:4]), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(left[4:], shift=UP * 0.1), FadeIn(lic, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeOut(lic))
            self.play(FadeIn(bh), LaggedStart(*[GrowFromEdge(b_[0], LEFT) for b_ in bars], lag_ratio=0.4),
                      LaggedStart(*[FadeIn(b_[1]) for b_ in bars], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(fw, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
