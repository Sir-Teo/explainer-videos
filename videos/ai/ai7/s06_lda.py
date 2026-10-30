from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai7.common import BOUND, HIDDEN, MONO, PART, SEEN, TOPIC_COLORS, card_in, edge, load, node


def word_col(words, color, font_size=20, buff=0.08) -> VGroup:
    return VGroup(*[data_text(w, font=MONO, font_size=font_size, color=color) for w in words]).arrange(DOWN, buff=buff)


class Topics(VoiceoverScene):
    def construct(self):
        card_in(self, 5, r"Topic models", r"What is a book about, if nobody tells us the themes?",
                "Chapter five. Topic models.")
        self.story()
        self.train()
        self.result()

    # ------------------------------------------------------------------
    def story(self):
        l = load("lda")
        a = node(r"\alpha", [-5.6, 0.6, 0], hidden=True, r=0.3)
        a[0].set_stroke(GREY_B)
        th = node(r"\theta_d", [-3.9, 0.6, 0])
        z = node(r"z_{dn}", [-2.2, 0.6, 0])
        w = node(r"w_{dn}", [-0.5, 0.6, 0], hidden=False)
        b = node(r"\beta_k", [-0.5, 2.6, 0])
        arrows = VGroup(edge(a, th), edge(th, z), edge(z, w), edge(b, w))
        pn = SurroundingRectangle(VGroup(z, w), color=GREY_C, buff=0.25, corner_radius=0.1)
        pd = SurroundingRectangle(VGroup(th, z, w, pn), color=GREY_C, buff=0.25, corner_radius=0.1)
        pk = SurroundingRectangle(b, color=GREY_C, buff=0.2, corner_radius=0.1)
        tags = VGroup(MathTex(r"N", font_size=26, color=GREY_B).next_to(pn.get_corner(DR), UL, buff=0.06),
                      MathTex(r"D", font_size=26, color=GREY_B).next_to(pd.get_corner(DR), UL, buff=0.06),
                      MathTex(r"K", font_size=26, color=GREY_B).next_to(pk.get_corner(DR), UL, buff=0.06))
        graph = VGroup(a, th, z, w, b, arrows, pn, pd, pk, tags).move_to([-3.0, 0.2, 0])
        story = VGroup(
            label(r"1. \ each topic $k$: \ a distribution $\beta_k$ over words", font_size=24, color=HIDDEN),
            label(r"2. \ each section $d$: \ a mix of topics, \ $\theta_d \sim \mathrm{Dirichlet}(\alpha)$", font_size=24,
                  color=HIDDEN),
            label(r"3. \ each word: \ pick a topic $z \sim \theta_d$, \ then a word $w \sim \beta_z$", font_size=24,
                  color=SEEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, 0.6, 0])
        h = history_card(2003, r"D.~Blei, A.~Ng \& M.~Jordan", r"latent Dirichlet allocation \ (after T.~Hofmann's "
                         r"probabilistic latent semantic analysis, 1999)", width=6.0).to_edge(DOWN, buff=0.35)
        not6 = note(r"not Part 6's LDA \ (Fisher's discriminant): \ the same initials, \ a different idea",
                    font_size=20).to_corner(UR, buff=0.3)
        with self.voiceover(
            "A mixture model gives each page one hidden source. But a book is about several things at once. In "
            "2003 David Blei, Andrew Ng and Michael Jordan wrote down a model for that: latent Dirichlet allocation, "
            "the topic model. <bookmark mark='a'/> The story goes like this. There are K topics, each a distribution "
            "over words. <bookmark mark='b'/> Each section of text has its own mix of topics, drawn from a Dirichlet "
            "distribution, which prefers mixes of only a few. <bookmark mark='c'/> And each word is made in two "
            "steps: pick a topic from the section's mix, then a word from that topic. <bookmark mark='d'/> Only the "
            "words are observed. The topics, the mixes and every word's topic are hidden, and we infer them all."
        ) as vo:
            self.play(FadeIn(h, shift=UP * 0.2), FadeIn(not6), FadeIn(graph))
            vo.wait_until("a")
            self.play(Circumscribe(b, color=HIDDEN), FadeIn(story[0]))
            vo.wait_until("b")
            self.play(Circumscribe(th, color=HIDDEN), FadeIn(story[1]))
            vo.wait_until("c")
            self.play(Circumscribe(VGroup(z, w), color=SEEN), FadeIn(story[2]))
            vo.wait_until("d")
            self.play(Circumscribe(w, color=SEEN), *[Circumscribe(m, color=HIDDEN) for m in (th, z, b)])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def train(self):
        l = load("lda")
        bounds = np.asarray(l["bounds"])
        share = np.asarray(l["main_share"])
        show = sorted(np.argsort(-share)[:6].tolist())
        snaps = l["snaps"]
        keys = sorted(snaps, key=int)
        cols = VGroup()
        for j, k in enumerate(show):
            cols.add(word_col(snaps[keys[0]][k][:6], TOPIC_COLORS[k], font_size=22))
        cols.arrange(RIGHT, buff=0.35)
        w0 = cols.width
        if cols.width > 8.6:
            cols.width = 8.6
        fscale = cols.width / w0
        cols.move_to([0, 0.5, 0]).to_edge(LEFT, buff=0.4)
        heads = VGroup(*[label(rf"topic {j + 1}", font_size=22, color=TOPIC_COLORS[k]).next_to(c, UP, buff=0.2)
                         for j, (k, c) in enumerate(zip(show, cols))])
        g = axes([0, len(bounds), 10], [float(bounds.min()) - 0.05, float(bounds.max()) + 0.05, 0.2], x_length=3.6,
                 y_length=2.4, xlabel=r"round of variational EM", ylabel=r"bound per word (nats)", center=[4.9, -1.3, 0])
        it = ValueTracker(1)
        bc = always_redraw(lambda: curve(g.ax, np.arange(1, int(it.get_value()) + 1), bounds[:int(it.get_value())], BOUND, 3)
                           if it.get_value() >= 2 else VMobject())
        rv = Integer(0, font_size=34)
        rl = VGroup(label(r"round", font_size=26, color=GREY_A), rv).arrange(RIGHT, buff=0.15).move_to([4.9, 1.6, 0])
        info = label(rf"${l['D']:,}$ sections of ${l['seg']:,}$ words \ $\cdot$ \ the ${l['V']:,}$ commonest content words "
                     rf"\ $\cdot$ \ $K = {l['K']}$ topics".replace(",", "{,}"), font_size=22, color=GREY_A).to_edge(DOWN, buff=0.3)
        mono = bool(l["monotone"])
        rise = ("and, like every EM, it never falls" if mono else "though, with the smoothing we add, not on every round")
        with self.voiceover(
            f"We cut the thirty novels into {l['D']:,} sections of {l['seg']:,} words, keep the {l['V']:,} commonest "
            "words that aren't names or little function words, and ask for twelve topics. "
            "<bookmark mark='a'/> The topics start as the words of a few random sections: noise. Blei's original "
            "method fits them by variational EM, which chapter sixteen will explain: an E step that guesses each "
            "section's mix, and an M step that rebuilds each topic from the words assigned to it. "
            f"<bookmark mark='b'/> Watch six of the topics take shape. The bound on the likelihood climbs, {rise}."
        ) as vo:
            self.play(FadeIn(info), FadeIn(g), FadeIn(rl), FadeIn(cols), FadeIn(heads))
            vo.wait_until("a")
            self.play(Indicate(cols, color=GREY_B, scale_factor=1.02))
            vo.wait_until("b")
            self.add(bc)
            for key in keys[1:]:
                new = VGroup()
                for c, k in zip(cols, show):
                    nc = word_col(snaps[key][k][:6], TOPIC_COLORS[k], font_size=22)
                    nc.scale(fscale).move_to(c)
                    new.add(nc)
                self.play(*[Transform(c, n_) for c, n_ in zip(cols, new)], it.animate.set_value(max(int(key), 1)),
                          ChangeDecimalToValue(rv, int(key)), run_time=1.4)
        bc.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def result(self):
        l = load("lda")
        K = l["K"]
        tiles = VGroup()
        for k in range(K):
            ws = word_col(l["top"][k][:4], TOPIC_COLORS[k], font_size=19, buff=0.05)
            bk = label(rf"\textit{{{l['main'][k]}}}", font_size=16, color=GREY_B)
            if bk.width > 2.0:
                bk.width = 2.0
            t = VGroup(ws, bk).arrange(DOWN, buff=0.12)
            box = RoundedRectangle(width=2.2, height=t.height + 0.3, corner_radius=0.1, stroke_color=TOPIC_COLORS[k],
                                   stroke_width=1.5)
            tiles.add(VGroup(box, t.move_to(box)))
        tiles.arrange_in_grid(rows=2, cols=6, buff=(0.15, 0.25)).to_edge(UP, buff=0.35)
        cap = note(r"each topic's top words, \ and the novel where it is commonest", font_size=20).next_to(tiles, DOWN, buff=0.1)
        # one section, its words coloured by their likeliest topic, and its mixture
        words, tops = l["ex_words"][:60], l["ex_topic"][:60]
        lines, row = VGroup(), VGroup()
        for w_, t_ in zip(words, tops):
            m = data_text(w_, font=MONO, font_size=20, color=TOPIC_COLORS[t_] if t_ >= 0 else GREY_D)
            row.add(m)
            if len(row) == 10:
                lines.add(row.arrange(RIGHT, buff=0.12))
                row = VGroup()
        if len(row):
            lines.add(row.arrange(RIGHT, buff=0.12))
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        if lines.width > 8.6:
            lines.width = 8.6
        lines.move_to([-2.2, -1.9, 0])
        th = np.asarray(l["ex_theta"])
        bx = VGroup(*[Rectangle(width=0.2, height=max(2.2 * v, 0.01), stroke_width=0, fill_color=TOPIC_COLORS[k],
                                fill_opacity=0.9).move_to([3.3 + 0.28 * k, -3.2 + 1.1 * v, 0]) for k, v in enumerate(th)])
        bl = label(rf"this section's mix: \ \textit{{{l['ex_title']}}}", font_size=20, color=GREY_A).next_to(bx, UP, buff=0.15)
        top2 = np.argsort(-th)[:2]
        c3 = np.argsort(-np.asarray(l["main_share"]))[:3]
        with self.voiceover(
            "Here are all twelve topics after forty rounds, each with its commonest words and the novel where it "
            f"turns up most. <bookmark mark='a'/> Nobody named them, but you can read them. The topic most at home in "
            f"{l['main'][c3[0]]} leads with '{l['top'][c3[0]][0]}', the one in {l['main'][c3[1]]} with "
            f"'{l['top'][c3[1]][0]}', and the one in {l['main'][c3[2]]} with '{l['top'][c3[2]][0]}'. Others are harder "
            "to name. <bookmark mark='b'/> And here is one "
            f"section of {l['ex_title']}, with each word coloured by its likeliest topic. Its mix is "
            f"{100 * th[top2[0]]:.0f} percent one topic and {100 * th[top2[1]]:.0f} percent another. "
            "<bookmark mark='c'/> For a decade, topic models were how historians and social scientists read archives "
            "too large to read. Today embeddings do much of that work, but the idea, a document as a mix of hidden "
            "themes, is the same picture."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tiles], lag_ratio=0.1), FadeIn(cap), run_time=2.5)
            vo.wait_until("a")
            self.play(*[Indicate(tiles[k], scale_factor=1.06, color=TOPIC_COLORS[k]) for k in c3], run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(lines), run_time=1.5)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bx], lag_ratio=0.05), FadeIn(bl))
            vo.wait_until("c")
            self.play(*[Indicate(tiles[k], scale_factor=1.06, color=TOPIC_COLORS[k]) for k in top2])
        self.wait(0.3)
        self.clear_scene()
