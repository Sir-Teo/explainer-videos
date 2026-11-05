from __future__ import annotations

import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs20.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class Lsh(VoiceoverScene):
    def construct(self):
        self.card()
        self.jaccard()
        self.minhash()
        self.bands()
        self.novels()

    def card(self):
        card = chapter_card(13, r"Near-duplicates: \ MinHash and LSH", r"Which of 600 million pairs are alike?",
                            lit=(1997, 1998), extra=((1997, r"Broder's MinHash"), (1998, r"Indyk--Motwani LSH")),
                            part=PART)
        with self.voiceover("Chapter thirteen. Near-duplicates: MinHash and locality-sensitive hashing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def jaccard(self):
        head = label(r"How alike are two paragraphs?", font_size=34).to_edge(UP, buff=0.35)
        a = r"the king's attorney is informed by a friend to the throne"
        b = r"the king's attorney is informed by a friend of the throne"
        ta = label(rf"\textit{{{a}}}", font_size=22, color=DATA)
        tb = label(rf"\textit{{{b}}}", font_size=22, color=LAM)
        VGroup(ta, tb).arrange(DOWN, buff=0.25).next_to(head, DOWN, buff=0.45)
        sh = VGroup(
            label(r"shingles: \ every run of 5 consecutive words", font_size=21, color=WHITE),
            label(r"\textit{the king's attorney is informed}, \ \textit{king's attorney is informed by}, \ \dots",
                  font_size=19, color=GREY_A),
            MathTex(r"J(A, B) = \frac{|A \cap B|}{|A \cup B|}", font_size=40, color=YES),
            label(r"here: \ 4 shared of 10, \ $J = 0.4$; \ one changed word breaks 5 shingles", font_size=21,
                  color=HEAD),
            label(r"comparing every pair of the novels' 34{,}525 long paragraphs: \ 596 million pairs", font_size=21,
                  color=NO),
        ).arrange(DOWN, buff=0.3).next_to(tb, DOWN, buff=0.45)
        with self.voiceover(
            "Search engines, plagiarism detectors and the people who clean training data for language models all "
            "need to find documents that are nearly the same. <bookmark mark='a'/> Represent a passage by its "
            "shingles, every run of five consecutive words. <bookmark mark='b'/> Two passages are as alike as the "
            "share of shingles they have in common: the Jaccard similarity, the size of the intersection over the "
            "size of the union. <bookmark mark='c'/> These two lines, from two versions of the same letter in "
            "The Count of Monte Cristo, share four of their ten distinct shingles, because changing one word breaks "
            "every shingle that contains it. <bookmark mark='d'/> The novels have thirty-four thousand paragraphs "
            "of forty words or more. Comparing every pair means almost six hundred million comparisons of sets."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ta), FadeIn(tb))
            vo.wait_until("a")
            self.play(FadeIn(sh[0]), FadeIn(sh[1]))
            vo.wait_until("b")
            self.play(FadeIn(sh[2]))
            vo.wait_until("c")
            self.play(FadeIn(sh[3]))
            vo.wait_until("d")
            self.play(FadeIn(sh[4]))
        self.wait(0.3)
        self.clear_scene()

    def minhash(self):
        head = label(r"MinHash: \ one number that agrees with probability $J$", font_size=34).to_edge(UP, buff=0.35)
        rng = random.Random(7)
        A = set(range(0, 14))
        B = set(range(6, 22))
        U = sorted(A | B)
        order = U[:]
        rng.shuffle(order)
        cells = VGroup()
        for x in order:
            col = YES if (x in A and x in B) else (DATA if x in A else LAM)
            cells.add(Square(side_length=0.42, stroke_width=1, stroke_color=GREY_C, fill_color=col, fill_opacity=0.7))
        cells.arrange(RIGHT, buff=0.04).move_to(UP * 1.0)
        leg = VGroup(label(r"only in $A$", font_size=18, color=DATA), label(r"in both", font_size=18, color=YES),
                     label(r"only in $B$", font_size=18, color=LAM)).arrange(RIGHT, buff=0.6).next_to(cells, UP,
                                                                                                  buff=0.3)
        arrow = Arrow(cells[0].get_bottom() + DOWN * 0.7, cells[0].get_bottom(), color=HEAD, buff=0.05)
        txt = label(r"a random order of all shingles: \ the first one belonging to $A \cup B$", font_size=20,
                    color=HEAD).next_to(arrow, DOWN, buff=0.1).align_to(cells, LEFT)
        lines = VGroup(
            label(r"$h_{\min}(A) = h_{\min}(B)$ \ exactly when that first shingle is in both \ (here it is only "
                  r"in $A$: \ they differ)", font_size=22, color=WHITE),
            MathTex(r"\Pr[h_{\min}(A) = h_{\min}(B)] = \frac{|A \cap B|}{|A \cup B|} = J", font_size=36, color=YES),
            label(r"100 hash functions: \ a signature of 100 numbers; \ the share that agree estimates $J$ \ "
                  r"($\pm 0.05$)", font_size=21, color=LAM),
            label(r"Broder (1997), \ for AltaVista's crawl of the Web", font_size=19, color=GREY_B),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Andrei Broder found a shortcut in 1997, at the search engine AltaVista. <bookmark mark='a'/> Put every "
            "shingle in a random order, using a hash function, and look at the first shingle of the union of two "
            "sets. <bookmark mark='b'/> Each set's minimum hash is the same exactly when that first shingle "
            "belongs to both; here it is only in A, so they differ. By symmetry, every shingle of the union is equally "
            "likely to be first. <bookmark "
            "mark='c'/> So the two minimums agree with probability exactly the Jaccard similarity. <bookmark "
            "mark='d'/> Repeat with a hundred hash functions, and each paragraph becomes a signature of a hundred "
            "numbers. The share of positions where two signatures agree estimates their similarity, to within "
            "about five hundredths."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(leg))
            vo.wait_until("a")
            self.play(GrowArrow(arrow), FadeIn(txt))
            vo.wait_until("b")
            self.play(FadeIn(lines[0]), Indicate(cells[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]), FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def bands(self):
        d = load("minhash")
        head = label(r"Banding: \ hash the signatures themselves", font_size=34).to_edge(UP, buff=0.35)
        pts = VGroup(
            label(r"cut each signature into $b = 20$ bands of $r = 5$ numbers", font_size=21, color=WHITE),
            label(r"two paragraphs become candidates if \textbf{some} band matches exactly", font_size=21,
                  color=WHITE),
            MathTex(r"\Pr[\text{candidates}] = 1 - (1 - J^{\,r})^{b}", font_size=36, color=YES),
            label(r"a step near $J = (1/b)^{1/r} \approx 0.55$", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.25).to_edge(LEFT, buff=0.5).shift(UP * 0.5)
        ax = Axes(x_range=[0, 1, 0.2], y_range=[0, 1, 0.25], x_length=5.0, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(RIGHT, buff=0.7).shift(DOWN * 0.4)
        curve = ax.plot(lambda s: 1 - (1 - s ** 5) ** 20, x_range=[0, 1], color=YES)
        dots = VGroup(*[Dot(ax.c2p(c["lo"] + 0.05, c["hit"]), radius=0.07, color=HEAD) for c in d["curve"]])
        xl = VGroup(*[label(f"{x:.1f}", font_size=16, color=GREY_B).next_to(ax.c2p(x, 0), DOWN, buff=0.1)
                      for x in (0, 0.2, 0.4, 0.6, 0.8, 1.0)])
        xt = label(r"similarity $J$", font_size=18, color=GREY_A).next_to(xl, DOWN, buff=0.1)
        yt = label(r"found", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        leg = label(r"dots: 600 planted copies with words changed at random", font_size=17, color=HEAD
                    ).next_to(ax, DOWN, buff=0.75)
        with self.voiceover(
            "Signatures are short, but there are still six hundred million pairs of them. <bookmark mark='a'/> The "
            "last trick, locality-sensitive hashing, from Piotr Indyk and Rajeev Motwani, hashes the signatures "
            "themselves. Cut each into twenty bands of five numbers, and put each band into a hash table. <bookmark "
            "mark='b'/> Two paragraphs become candidates only if some band matches exactly. <bookmark mark='c'/> A "
            "band matches with probability J to the fifth, so the chance of becoming candidates is one minus one "
            "minus J to the fifth, to the twentieth. <bookmark mark='d'/> That curve is a step: pairs below a "
            "similarity of about a half are almost never compared, and pairs above seven tenths almost always are. "
            "We planted six hundred edited copies of paragraphs, and the share found at each similarity follows "
            "the curve."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(xt), FadeIn(yt))
            for mk, p in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
                if mk == "c":
                    self.play(Create(curve))
            self.play(LaggedStart(*[GrowFromCenter(x) for x in dots], lag_ratio=0.15), FadeIn(leg))
        self.wait(0.3)
        self.clear_scene()

    def novels(self):
        d = load("minhash")
        head = label(r"Near-duplicates in thirty novels", font_size=34).to_edge(UP, buff=0.35)
        stats = VGroup(
            label(rf"{words(d['paragraphs'])} paragraphs, \ {big_m(d['shingles'])} shingles, \ "
                  rf"{big_m(d['pairs'])} pairs", font_size=22, color=GREY_A),
            label(rf"signatures: \ {d['t_sig']:.1f} s; \ banding: \ {d['t_band']:.1f} s; \ candidates: \ "
                  rf"{d['candidates']}", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.2).next_to(head, DOWN, buff=0.35)
        rows = []
        for t in d["truth"]:
            a, b = t["a"], t["b"]
            where = a if a == b else rf"{a} \ / \ {b}"
            rows.append([f"{t['j']:.2f}", where, r"\textit{" + tex_escape(t["text_a"][:44]) + r"...}",
                         r"found" if t["found"] else r"---"])
        tab = grid_table([r"$J$", r"where", r"begins", r"LSH"], rows, widths=[0.9, 5.0, 5.8, 1.0], row_h=0.42,
                         font_size=16, mono_cols=(),
                         colors=[[YES if t["found"] else GREY_A, WHITE, GREY_B, YES if t["found"] else GREY_D]
                                 for t in d["truth"]]).next_to(stats, DOWN, buff=0.4)
        note_ = VGroup(
            label(r"ground truth: \ every pair sharing even one rare shingle, \ found through an inverted index",
                  font_size=19, color=GREY_A),
            label(r"the two pairs above the threshold were both found; \ the others sit on the low side of the "
                  r"step", font_size=19, color=WHITE),
            label(r"in practice: \ Google's near-duplicate crawler \ (SimHash), \ dedup of LLM training data "
                  r"(MinHash)", font_size=19, color=LAM),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now the novels. <bookmark mark='a'/> Thirty-four thousand paragraphs, three and a half million "
            "shingles, six hundred million pairs. Computing every signature took two seconds, and the banding "
            f"three more. It produced just {d['candidates']} candidate pairs. <bookmark mark='b'/> To check, we found "
            "every pair of paragraphs that share even one uncommon shingle, with an inverted index, and computed "
            "their exact similarity. Only seven pairs in all thirty novels share a fifth of their phrases. "
            "<bookmark mark='c'/> The two above the threshold were both found: a table of contents in two editions, "
            "and the anonymous letter in The Count of Monte Cristo, which is quoted more than once, in different "
            "versions. The rest, a battle order repeated in War and Peace and a passage repeated in The Awakening, "
            "fall below the step, as the curve predicts. <bookmark mark='d'/> Novelists rarely repeat themselves; the Web does all "
            "the time. Google's crawler finds near-duplicate pages with a cousin of this idea, Moses Charikar's "
            "SimHash, and MinHash with banding is a standard step in cleaning the training data of language models."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(stats))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.2), FadeIn(note_[0]))
            vo.wait_until("c")
            self.play(FadeIn(note_[1]))
            vo.wait_until("d")
            self.play(FadeIn(note_[2]))
        self.wait(0.3)
        self.clear_scene()


def tex_escape(t):
    for a, b in (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"), ("_", r"\_"),
                 ("{", r"\{"), ("}", r"\}"), ("~", r"\~{}"), ("^", r"\^{}"), ('"', "")):
        t = t.replace(a, b)
    return t


def big_m(n):
    if n >= 1e8:
        return f"{n / 1e6:.0f} million"
    if n >= 1e6:
        return f"{n / 1e6:.1f} million"
    return words(n)
