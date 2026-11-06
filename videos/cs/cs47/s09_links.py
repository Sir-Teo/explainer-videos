from __future__ import annotations

import math
import random

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs47.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load, trace

# a small web for the pictures (illustrative)
TOY_POS = {0: (-4.9, 1.3), 1: (-2.5, 1.9), 2: (-3.4, -0.2), 3: (-5.6, -1.4), 4: (-1.3, -0.7), 5: (-2.6, -2.3)}
TOY_OUT = {0: [1, 2], 1: [2, 4], 2: [0], 3: [0, 2], 4: [2, 1], 5: [4, 2]}


def toy_pagerank(d=0.85, iters=100):
    n = len(TOY_POS)
    r = np.full(n, 1 / n)
    for _ in range(iters):
        nr = np.full(n, (1 - d) / n)
        for v, us in TOY_OUT.items():
            for u in us:
                nr[u] += d * r[v] / len(us)
        r = nr
    return r


class Links(VoiceoverScene):
    def construct(self):
        self.card()
        self.votes()
        self.surfer()
        self.power()
        self.hits()
        self.spam()

    def card(self):
        card = chapter_card(8, r"Links and the random surfer", r"Which pages does the web itself vouch for?",
                            lit=(1998, 1999),
                            extra=((1998, r"Brin and Page: \ PageRank"), (1999, r"Kleinberg: \ hubs and authorities")),
                            part=PART)
        with self.voiceover("Chapter eight. Links and the random surfer."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def votes(self):
        head = label(r"Links as votes", font_size=36).to_edge(UP, buff=0.3)
        nodes = {k: Circle(radius=0.28, color=DATA, stroke_width=2.5, fill_color=DATA, fill_opacity=0.2).move_to(
            [x, y, 0]) for k, (x, y) in TOY_POS.items()}
        edges = VGroup(*[Arrow(nodes[v].get_center(), nodes[u].get_center(), buff=0.32, stroke_width=2,
                               color=GREY_B, max_tip_length_to_length_ratio=0.1) for v, us in TOY_OUT.items()
                         for u in us])
        ill = label(r"illustrative", font_size=16, color=GREY_B).move_to([-1.0, -2.9, 0])
        surfer = Dot(radius=0.12, color=HEAD).move_to(nodes[3])
        rng = random.Random(5)
        walk, v = [], 3
        for _ in range(14):
            if rng.random() < 0.15:
                v, jump = rng.randrange(len(TOY_POS)), True
            else:
                v, jump = rng.choice(TOY_OUT[v]), False
            walk.append((v, jump))
        pr = toy_pagerank()
        notes = VGroup(
            wrapped_label(r"Brin and Page \ (1998): \ a link is a vote; \ a page is important if important pages "
                          r"link to it, \ and each page splits its vote among its links", 5.6, font_size=20,
                          color=WHITE),
            wrapped_label(r"the random surfer: \ follow a random link on each page; \ now and then, \ jump to a "
                          r"page chosen at random", 5.6, font_size=20, color=HEAD),
            wrapped_label(r"\textbf{PageRank} = \ the share of time the surfer spends on each page, \ in the long "
                          r"run \ (node size)", 5.6, font_size=20, color=YES),
            wrapped_label(r"a link's \textbf{anchor text} is indexed as words describing the page it points to",
                          5.6, font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, 0.0, 0])
        with self.voiceover(
            "Words say what a page is about, not whether it is any good. <bookmark mark='a'/> Sergey Brin and Larry "
            "Page, in 1998, read the links between pages as votes: a page is important if important pages link to it,"
            " and each page splits its vote among its links. <bookmark mark='b'/> The definition is circular, and a "
            "story resolves it. A surfer clicks a random link on every page, and now and then, bored, jumps to a "
            "random page. <bookmark mark='c'/> The fraction of time the surfer spends on each page, in the long run, "
            "is its PageRank. <bookmark mark='d'/> Brin and Page also indexed the text of each link as words "
            "describing its target."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(n) for n in nodes.values()], Create(edges), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(surfer), FadeIn(notes[1]))
            for u, jump in walk:
                if jump:
                    self.play(FadeOut(surfer, scale=0.3), run_time=0.2)
                    surfer.move_to(nodes[u])
                    self.play(FadeIn(surfer, scale=2), Flash(nodes[u], color=LAM, flash_radius=0.4), run_time=0.35)
                else:
                    self.play(surfer.animate.move_to(nodes[u]), run_time=0.45)
                self.play(nodes[u].animate.set_fill(DATA, opacity=min(0.9, nodes[u].get_fill_opacity() + 0.1)),
                          run_time=0.15)
            vo.wait_until("c")
            self.play(FadeOut(surfer), *[nodes[k].animate.scale(math.sqrt(pr[k] * len(pr)) * 0.95).set_fill(
                YES, opacity=0.35).set_stroke(YES) for k in nodes], FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def surfer(self):
        head = label(r"The random surfer, \ written down", font_size=36).to_edge(UP, buff=0.3)
        eq = label(r"$\mathrm{PR}(p) \;=\; \dfrac{1-d}{N} \;+\; d \displaystyle\sum_{q \to p} "
                   r"\dfrac{\mathrm{PR}(q)}{L(q)}$",
                   font_size=38).next_to(head, DOWN, buff=0.4)
        # a fragment: two pages linking to p, each sharing its rank among its links
        p = Circle(radius=0.32, color=YES, fill_color=YES, fill_opacity=0.25).move_to([-3.0, -0.9, 0])
        pl = label(r"$p$", font_size=24, color=YES).move_to(p)
        q1 = Circle(radius=0.3, color=DATA, fill_color=DATA, fill_opacity=0.2).move_to([-5.6, 0.2, 0])
        q2 = Circle(radius=0.3, color=DATA, fill_color=DATA, fill_opacity=0.2).move_to([-5.6, -2.0, 0])
        q1l = label(r"$q_1$", font_size=20, color=DATA).move_to(q1)
        q2l = label(r"$q_2$", font_size=20, color=DATA).move_to(q2)
        a1 = Arrow(q1.get_center(), p.get_center(), buff=0.34, color=DATA, stroke_width=3)
        a2 = Arrow(q2.get_center(), p.get_center(), buff=0.34, color=DATA, stroke_width=3)
        s1 = label(r"$\mathrm{PR}(q_1)/3$", font_size=18, color=DATA).next_to(a1.get_center(), UP, buff=0.12)
        s2 = label(r"$\mathrm{PR}(q_2)/2$", font_size=18, color=DATA).next_to(a2.get_center(), DOWN, buff=0.12)
        stubs = VGroup(
            Arrow(q1.get_center(), q1.get_center() + np.array([0.2, 1.1, 0]), buff=0.3, color=GREY_C, stroke_width=2),
            Arrow(q1.get_center(), q1.get_center() + np.array([1.1, 0.7, 0]), buff=0.3, color=GREY_C, stroke_width=2),
            Arrow(q2.get_center(), q2.get_center() + np.array([1.2, -0.6, 0]), buff=0.3, color=GREY_C,
                  stroke_width=2))
        tele = DashedLine([-1.2, 0.5, 0], p.get_center(), buff=0.34, color=LAM, stroke_width=2.5)
        tele_l = label(r"teleport: \ $(1-d)/N$", font_size=18, color=LAM).next_to([-1.2, 0.5, 0], UP, buff=0.08)
        notes = VGroup(
            wrapped_label(r"with probability $d$ follow a link, \ otherwise jump anywhere: \ Brin and Page suggest "
                          r"$d = 0.85$", 6.0, font_size=20, color=WHITE),
            wrapped_label(r"a page with no links shares its rank with every page", 6.0, font_size=20, color=GREY_A),
            wrapped_label(r"$\mathbf{r} = G\,\mathbf{r}$: \ the eigenvector of the Google matrix with eigenvalue 1, "
                          r"\ the stationary distribution of a Markov chain \ (Part 18)", 6.0, font_size=20,
                          color=YES),
            wrapped_label(r"teleporting makes every page reachable from every other: \ by Perron--Frobenius the "
                          r"vector exists and is unique", 6.0, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([3.5, -1.0, 0])
        with self.voiceover(
            "Write it down. <bookmark mark='a'/> With probability d the surfer follows a link; otherwise it teleports"
            " anywhere. So a page's rank is the teleport share, one minus d over the number of pages, plus d times "
            "the rank flowing in, each page giving an equal part of its rank to each of its links. Brin and Page "
            "suggested a d of zero point eight five. <bookmark mark='b'/> A page with no links passes its rank to "
            "everyone. <bookmark mark='c'/> In matrix form, the rank vector is the eigenvector of the Google matrix "
            "with eigenvalue one: the stationary distribution of a Markov chain, as in Part 18. <bookmark mark='d'/> "
            "Teleporting connects every page to every other, so by the Perron–Frobenius theorem that vector exists "
            "and is unique."       ) as vo:
            self.play(FadeIn(head), Write(eq))
            vo.wait_until("a")
            self.play(FadeIn(p), FadeIn(pl), FadeIn(q1), FadeIn(q2), FadeIn(q1l), FadeIn(q2l), Create(stubs))
            self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(s1), FadeIn(s2))
            self.play(Create(tele), FadeIn(tele_l), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def power(self):
        pr = load("pagerank")
        n_web = pr["target"] + 1                     # the preferential-attachment pages; the rest is the farm
        hist = pr["convergence"]
        head = label(r"Power iteration on a synthetic web", font_size=36).to_edge(UP, buff=0.3)
        lo = -7                                       # log10 values are drawn shifted up by 7, so the x-axis sits low
        g = axes([0, 40, 10], [0, 8, 1], x_length=6.0, y_length=4.0, x_label=r"iteration",
                 y_label=r"change in the rank vector \ (sum of absolute differences)",
                 xticks=[0, 10, 20, 30, 40], yticks=[1, 3, 5, 7], fy=lambda v: rf"$10^{{{int(v) + lo}}}$")
        g.move_to([-2.8, -0.35, 0])
        ax = g.ax
        obs = trace(ax, [(k + 1, math.log10(h) - lo) for k, h in enumerate(hist)], YES, width=3.5)
        bound = DashedVMobject(trace(ax, [(k + 1, math.log10(hist[0] * 0.85 ** k) - lo) for k in range(len(hist))],
                                     HEAD, width=2.5), num_dashes=40)
        man, ex = f"{hist[-1]:.1e}".split("e")
        ol = label(rf"ours: \ ${man} \times 10^{{{int(ex)}}}$ after {len(hist)} steps", font_size=17, color=YES)
        bl = label(r"guaranteed: \ at least a factor $d = 0.85$ a step", font_size=17, color=HEAD)
        legend = VGroup(bl, ol).arrange(DOWN, aligned_edge=RIGHT, buff=0.12)
        legend.move_to(ax.c2p(40, 7.6), aligned_edge=UR)
        rows = [[f"{i}", f"{v:.4f}"] for i, v in pr["top"][:5]]
        tab = grid_table([r"page", r"PageRank"], rows, widths=[1.3, 1.9], row_h=0.42, font_size=19, mono_cols=())
        tab.move_to([4.6, 1.3, 0])
        tl = label(r"the top five", font_size=18, color=GREY_A).next_to(tab, UP, buff=0.15)
        notes = VGroup(
            wrapped_label(rf"{n_web} pages added one at a time, \ each linking to up to four earlier pages chosen "
                          rf"in proportion to their links, \ plus a farm of {pr['pages'] - n_web}", 4.4,
                          font_size=19, color=WHITE),
            wrapped_label(r"the top pages are the oldest: \ preferential attachment made them hubs", 4.4,
                          font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.4).set_x(4.6)
        with self.voiceover(
            "To compute it, start from the uniform vector and multiply by the matrix, again and again. "
            "<bookmark mark='a'/> Our synthetic web has four hundred pages, each linking to up to four earlier ones, "
            "chosen in proportion to the links they already have, plus a farm of twenty. <bookmark mark='b'/> At each"
            " step the change shrinks by at least a factor d, and here faster: to one part in a million after forty "
            "steps. The bound does not depend on the number of pages, so a web of billions also needs only a few "
            "dozen passes. <bookmark mark='c'/> The top pages are the oldest, which preferential attachment made into"
            " hubs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), FadeIn(tl), FadeIn(tab))
            vo.wait_until("b")
            self.play(Create(obs), run_time=2.5)
            self.play(Create(bound), FadeIn(bl), FadeIn(ol))
            vo.wait_until("c")
            self.play(Indicate(VGroup(*[r[0] for r in tab.cells[1:]]), color=YES),
                      FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def hits(self):
        pr = load("pagerank")
        n_web = pr["target"] + 1
        head = label(r"Hubs and authorities", font_size=36).to_edge(UP, buff=0.3)
        A = np.array([[1, 1, 0], [1, 1, 1], [1, 0, 0]], dtype=float)       # hub i links to authority j
        hy = [1.6, 0.4, -0.8]
        hubs = [Circle(radius=0.26, color=LAM, fill_color=LAM, fill_opacity=0.2).move_to([-5.0, y, 0]) for y in hy]
        auths = [Circle(radius=0.26, color=KERN, fill_color=KERN, fill_opacity=0.2).move_to([-2.6, y, 0]) for y in hy]
        edges = VGroup(*[Arrow(hubs[i].get_center(), auths[j].get_center(), buff=0.28, stroke_width=2, color=GREY_B,
                               max_tip_length_to_length_ratio=0.08)
                         for i in range(3) for j in range(3) if A[i, j]])
        hl = label(r"hubs", font_size=19, color=LAM).next_to(hubs[0], UP, buff=0.2)
        al = label(r"authorities", font_size=19, color=KERN).next_to(auths[0], UP, buff=0.2)
        ill = label(r"illustrative", font_size=16, color=GREY_B).next_to(VGroup(hubs[2], auths[2]), DOWN, buff=0.3)

        def bars(h, a):
            g = VGroup()
            for i in range(3):
                g.add(Rectangle(width=max(0.02, 0.9 * h[i]), height=0.18, stroke_width=0, fill_color=LAM,
                                fill_opacity=0.85).next_to(hubs[i], LEFT, buff=0.1).align_to(hubs[i], DOWN))
                g.add(Rectangle(width=max(0.02, 0.9 * a[i]), height=0.18, stroke_width=0, fill_color=KERN,
                                fill_opacity=0.85).next_to(auths[i], RIGHT, buff=0.1).align_to(auths[i], DOWN))
            return g
        h, a = np.ones(3) / math.sqrt(3), np.ones(3) / math.sqrt(3)
        states = []
        for _ in range(3):
            a = A.T @ h
            a /= np.linalg.norm(a)
            h = A @ a
            h /= np.linalg.norm(h)
            states.append((h.copy(), a.copy()))
        bar = bars(np.ones(3) / math.sqrt(3), np.ones(3) / math.sqrt(3))
        eq = VGroup(label(r"$\mathbf{a} = A^{\mathsf T}\mathbf{h}$, \ $\mathbf{h} = A\,\mathbf{a}$, \ normalise, "
                          r"\ repeat", font_size=24, color=WHITE),
                    label(r"$\to$ leading eigenvectors of $A^{\mathsf T}\!A$ and $A A^{\mathsf T}$", font_size=22,
                          color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.2, 1.7, 0])
        notes = VGroup(
            wrapped_label(r"Kleinberg \ (1999): \ an \textbf{authority} is linked from good hubs; \ a \textbf{hub} "
                          r"links to good authorities", 6.0, font_size=20, color=WHITE),
            wrapped_label(r"run on the neighbourhood of a query's results, \ not on the whole web", 6.0,
                          font_size=20, color=GREY_A),
            wrapped_label(rf"on our synthetic web: \ the top authority is page {pr['hits_top_authority']}, \ the "
                          rf"farm's target; \ the top hub is page {pr['hits_top_hub']}, \ a farm page; \ "
                          rf"{pr['farm_in_top_hubs']} of the 20 best hubs are farm pages", 6.0, font_size=20,
                          color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(eq, DOWN, buff=0.4).align_to(eq, LEFT)
        farm_ok = pr["hits_top_authority"] == pr["target"] and pr["hits_top_hub"] >= n_web
        with self.voiceover(
            "Jon Kleinberg, at the same time, read links differently. <bookmark mark='a'/> Authorities are pages "
            "linked to by good hubs; hubs are pages that link to good authorities. Each score is the sum of the other"
            " kind over the links. <bookmark mark='b'/> Iterate and normalise, and the two vectors converge to the "
            "leading eigenvectors of A transpose A and A A transpose, the singular vectors of the link matrix. "
            "Kleinberg ran it on the neighbourhood of a query's results. <bookmark mark='c'/> On our web it is easily"
            " led. The top authority is the farm's target, the top hub is a farm page, and all twenty farm pages are "
            "among the twenty best hubs."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(c) for c in hubs + auths], Create(edges), FadeIn(hl), FadeIn(al),
                      FadeIn(ill), FadeIn(bar))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(eq))
            for hh, aa in states:
                self.play(Transform(bar, bars(hh, aa)), run_time=0.9)
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            if not farm_ok:
                self.play(Indicate(notes[2], color=NO))
        self.wait(0.4)
        self.clear_scene()

    def spam(self):
        pr = load("pagerank")
        n_web = pr["target"] + 1
        farm_n = pr["pages"] - n_web
        head = label(r"Link spam", font_size=36).to_edge(UP, buff=0.3)
        c = np.array([-3.6, 0.3, 0])
        target = Circle(radius=0.32, color=NO, fill_color=NO, fill_opacity=0.3).move_to(c)
        tl = label(rf"the target: \ page {pr['target']}", font_size=17, color=NO).move_to(c + np.array([0, 2.3, 0]))
        R = 1.9
        fpos = [c + R * np.array([math.cos(2 * math.pi * k / farm_n), math.sin(2 * math.pi * k / farm_n), 0])
                for k in range(farm_n)]
        farm = VGroup(*[Dot(p, radius=0.09, color=LAM) for p in fpos])
        spokes = VGroup(*[Line(p, c, buff=0.33, stroke_width=1.3, color=LAM, stroke_opacity=0.7) for p in fpos])
        chords = VGroup(*[Line(fpos[i], fpos[j], stroke_width=0.6, color=LAM, stroke_opacity=0.35)
                          for i in range(farm_n) for j in range(i + 1, farm_n)])
        fl = label(rf"a farm of {farm_n} pages: \ all link to the target and to one another", font_size=17,
                   color=LAM).next_to(VGroup(farm), DOWN, buff=0.2)
        # a rank ladder: 1 at the top
        y_top, y_bot, xl = 2.2, -2.0, 1.2

        def Y(rank):
            return y_top - (rank - 1) / (pr["pages"] - 1) * (y_top - y_bot)
        ladder = Line([xl, y_top, 0], [xl, y_bot, 0], color=GREY_C, stroke_width=2)
        lt = label(r"rank 1", font_size=16, color=GREY_A).next_to([xl, y_top, 0], LEFT, buff=0.15)
        lb = label(rf"rank {pr['pages']}", font_size=16, color=GREY_A).next_to([xl, y_bot, 0], LEFT, buff=0.15)
        mk = Triangle(color=NO, fill_opacity=1).scale(0.12).rotate(-math.pi / 2).move_to(
            [xl + 0.2, Y(pr["rank_without_farm"]), 0])
        before = label(rf"without the farm: \ {pr['rank_without_farm']}th of {n_web}", font_size=19,
                       color=GREY_A).next_to(mk, RIGHT, buff=0.15)
        after = label(rf"with it: \ {pr['rank_with_farm']}th of {pr['pages']}", font_size=19, color=NO)
        after.next_to([xl + 0.35, Y(pr["rank_with_farm"]), 0], RIGHT, buff=0.15)
        lines = VGroup(
            wrapped_label(r"\texttt{rel=\"nofollow\"} \ (2005): \ a site marks links it does not vouch for, \ such "
                          r"as those in comments", 12.4, font_size=19, color=WHITE),
            wrapped_label(r"TrustRank \ (Gy\"ongyi, Garcia-Molina and Pedersen, 2004): \ teleport only to pages "
                          r"people have checked, \ so rank flows from trusted seeds", 12.4, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "That farm is link spam: twenty pages linking to one target and to one another. <bookmark mark='a'/> "
            "Without it, the target, the newest page of our web, ranks three hundred and forty-sixth of four hundred."
            " <bookmark mark='b'/> With it, a hundred and fourteenth of four hundred and twenty: each farm page "
            "collects its teleport share and passes most of it on. <bookmark mark='c'/> Defences followed. In 2005 "
            "the major search engines agreed on a nofollow attribute, for links a site does not vouch for, such as "
            "those in comments. TrustRank, from Gyöngyi, Garcia-Molina and Pedersen in 2004, teleports only to pages "
            "people have checked. Today links are one signal among many, combined by learned rankers, as chapter "
            "twelve will show."
        ) as vo:
            self.play(FadeIn(head), FadeIn(target), FadeIn(tl), Create(ladder), FadeIn(lt), FadeIn(lb))
            vo.wait_until("a")
            self.play(FadeIn(mk), FadeIn(before))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d) for d in farm], lag_ratio=0.05), Create(spokes), FadeIn(fl))
            self.play(Create(chords), run_time=1.2)
            self.play(mk.animate.move_to([xl + 0.2, Y(pr["rank_with_farm"]), 0]), FadeIn(after),
                      before.animate.set_opacity(0.5), Flash(target, color=NO), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(lines[0]))
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA)
