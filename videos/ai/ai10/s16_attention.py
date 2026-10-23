from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai10.common import (ATT, CELLC, HIST, LSTMC, MONO, PART, img_heat, load, pct, seed_band)
from videos.ai.ai10.specs import BAHDANAU

ENC, DEC = C.TRUE_P, LSTMC
COLORS = {r"e_{ij}": ATT, r"\alpha_{ij}": ATT, r"c_i": CELLC, r"h_j": ENC, r"s_{i-1}": DEC}


class Attention(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.step()
        self.lengths()
        self.replay()
        self.paper()
        self.after()

    def card(self):
        card = chapter_card(15, r"The birth of attention", r"What if the decoder could look back at the input?",
                            lit=(2017,), part=PART)
        with self.voiceover("Chapter fifteen. The birth of attention."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def idea(self):
        hc = history_card(2014, r"Dzmitry Bahdanau, Kyunghyun Cho \& Yoshua Bengio",
                          r"\textit{Neural Machine Translation by Jointly Learning to Align and Translate}",
                          width=6.6, color=HIST).to_edge(UP, buff=0.3)
        rows = VGroup(
            cmath(r"e_{ij}", r"=", r"v^\top \tanh\big(W", r"s_{i-1}", r"+ U", r"h_j", r"\big)", colors=COLORS,
                  font_size=38),
            cmath(r"\alpha_{ij}", r"=", r"\frac{\exp e_{ij}}{\sum_{k} \exp e_{ik}}", colors=COLORS, font_size=38),
            cmath(r"c_i", r"=", r"\sum_j", r"\alpha_{ij}", r"h_j", colors=COLORS, font_size=38),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([-2.4, -0.9, 0])
        rows[1][2].set_color(ATT)
        notes_ = VGroup(why(r"how well input $j$ fits what output $i$ needs"),
                        why(r"a softmax over the input positions"),
                        why(r"the context: \ a weighted average of the encoder's states"))
        for n, r in zip(notes_, rows):
            n.next_to(r, RIGHT, buff=0.5)
            if n.get_right()[0] > 6.9:
                n.shift(LEFT * (n.get_right()[0] - 6.9))
        key = VGroup(label(r"$h_j$: \ the encoder's state at input $j$", font_size=20, color=ENC),
                     label(r"$s_{i-1}$: \ the decoder's state before output $i$", font_size=20, color=DEC))
        key.arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In September 2014 Dzmitry Bahdanau, a student visiting Bengio's lab, with Cho and Bengio, proposed "
            "to drop the single vector. <bookmark mark='a'/> Keep all of the encoder's states, one per input "
            "position, and at every step of the decoder score each one: how well does input j fit what the "
            "decoder needs next? The score is a tiny network, learned with everything else. "
            "<bookmark mark='b'/> A softmax turns the scores into weights that sum to one. <bookmark mark='c'/> "
            "And the decoder gets their weighted average, a context vector made fresh for each output. "
            "<bookmark mark='d'/> They called the weights an alignment. We call it attention."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(key))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(notes_[0]))
            vo.wait_until("b")
            self.play(Write(rows[1]), FadeIn(notes_[1]))
            vo.wait_until("c")
            self.play(Write(rows[2]), FadeIn(notes_[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def step(self):
        s = load("seq2seq")
        word = s["show"]
        al = np.asarray(s["runs"]["1-0"]["show_alpha"])
        out = s["runs"]["1-0"]["show_out"]
        n = len(word)
        i = 4  # the fifth letter written
        a = al[i, :n]
        hs = VGroup(*[Circle(radius=0.25, stroke_color=ENC, stroke_width=2, fill_color=ENC, fill_opacity=0.15)
                      for _ in range(n)]).arrange(RIGHT, buff=0.42).move_to([0, -2.0, 0])
        ls = VGroup(*[data_text(c, font=MONO, font_size=22, color=GREY_A).next_to(h, DOWN, buff=0.15)
                      for c, h in zip(word, hs)])
        bars = VGroup(*[Rectangle(width=0.38, height=max(2.4 * w, 0.02), stroke_width=0, fill_color=ATT,
                                  fill_opacity=0.9).move_to(h.get_top() + UP * (0.1 + max(2.4 * w, 0.02) / 2))
                        for w, h in zip(a, hs)])
        vals = VGroup(*[MathTex(f"{w:.2f}", font_size=18, color=ATT).next_to(b, UP, buff=0.05)
                        for w, b in zip(a, bars) if w > 0.08])
        ctx = VGroup(*[Square(0.26, stroke_width=0, fill_color=CELLC, fill_opacity=0.35 + 0.1 * k)
                       for k in range(5)]).arrange(RIGHT, buff=0.04).move_to([0, 2.4, 0])
        cl = MathTex(r"c_i = \sum_j \alpha_{ij} h_j", font_size=30, color=CELLC).next_to(ctx, RIGHT, buff=0.3)
        lines = VGroup(*[Line(h.get_top(), ctx.get_bottom(), stroke_width=0.5 + 6 * w, color=ATT,
                              stroke_opacity=0.3 + 0.7 * w) for w, h in zip(a, hs)])
        so_far = data_text(out[:i] + "_", font=MONO, font_size=28, color=DEC).to_corner(UL, buff=0.5)
        sl = label(rf"written so far; \ next: \ the letter ``{out[i]}''", font_size=22, color=DEC)
        sl.next_to(so_far, DOWN, buff=0.15).align_to(so_far, LEFT)
        tag = note(r"computed: \ our model's weights at this step").to_corner(DR, buff=0.25)
        top = int(np.argmax(a))
        with self.voiceover(
            f"Here is one step of our own model, reversing the word {word}. It has written {out[:i]}, and is "
            "about to write the next letter. <bookmark mark='a'/> It scores every position of the input, and "
            f"the softmax puts {pct(a[top], 0)} percent of the weight on one letter, the {word[top]} at position "
            f"{top + 1}: exactly the one it must copy. <bookmark mark='b'/> The context is that mixture of the "
            "encoder's states, mostly that one. Nothing had to squeeze through a single vector: the decoder "
            "reached back for what it needed."
        ) as vo:
            self.play(FadeIn(hs), FadeIn(ls), FadeIn(so_far), FadeIn(sl), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), FadeIn(vals))
            vo.wait_until("b")
            self.play(Create(lines), FadeIn(ctx), FadeIn(cl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lengths(self):
        s = load("seq2seq")
        tests = np.asarray(s["test"])
        lo, hi = s["train"]
        runs = s["runs"]
        ax = axes([tests[0], tests[-1]], [0, 1.0], x_length=7.4, y_length=4.2, xlabel=r"length of the string",
                  ylabel=r"reversed exactly", xticks=[5, 10, 15, 20, 25, 30], yticks=[0, 0.5, 1.0],
                  yfmt=lambda v: f"{int(100 * v)}\\%", center=[-1.4, -0.4, 0])
        A = ax.ax
        shade = Rectangle(width=A.c2p(hi, 0)[0] - A.c2p(lo, 0)[0], height=A.c2p(0, 1)[1] - A.c2p(0, 0)[1],
                          stroke_width=0, fill_color=GREY_D, fill_opacity=0.25)
        shade.move_to([(A.c2p(lo, 0)[0] + A.c2p(hi, 0)[0]) / 2, (A.c2p(0, 0)[1] + A.c2p(0, 1)[1]) / 2, 0])
        sl = label(r"trained on these lengths", font_size=20, color=GREY_B).next_to(shade, UP, buff=0.08)
        sl.align_to(shade, RIGHT)
        plain = seed_band(A, tests, [runs[f"0-{k}"]["exact"] for k in (0, 1, 2)], ENC)
        att = seed_band(A, tests, [runs[f"1-{k}"]["exact"] for k in (0, 1, 2)], ATT)
        leg = legend([(ENC, r"one vector"), (ATT, r"with attention")], font_size=22).to_corner(UR, buff=0.5)
        pa = runs["1-0"]["params"], runs["0-0"]["params"]
        pl = label(rf"weights: \ ${pa[1]:,}$ and ${pa[0]:,}$; \ the same steps".replace(",", "{,}"), font_size=20,
                   color=GREY_B).next_to(leg, DOWN, buff=0.25).align_to(leg, LEFT)
        keep_in_frame(pl)
        tag = note(r"computed: \ three seeds each, \ min--max").to_corner(DR, buff=0.2)
        ma = np.mean([runs[f"1-{k}"]["exact"] for k in (0, 1, 2)], 0)
        mp = np.mean([runs[f"0-{k}"]["exact"] for k in (0, 1, 2)], 0)
        ih = list(tests).index(hi)
        out_ = [i for i, n in enumerate(tests) if n > hi]
        extra = float(np.mean(ma[out_])) if out_ else float("nan")
        v = (f"With attention, {pct(ma[ih], 0)} percent of the {hi}-letter strings come out exactly right, "
             f"against {pct(mp[ih], 0)} percent with one vector.")
        if out_:
            if extra > 0.5:
                v2 = (f"And beyond the lengths it trained on, it keeps going: {pct(extra, 0)} percent on average, "
                      "because the rule it learned, look one place further back, doesn't depend on the length.")
            else:
                v2 = (f"Beyond the lengths it trained on, it too fails, at {pct(extra, 0)} percent on average: it "
                      "has never had to keep count that far.")
        else:
            v2 = ""
        with self.voiceover(
            "Now the fair comparison: the same encoder and decoder, the same training, with and without "
            f"attention, three times each. <bookmark mark='a'/> {v} <bookmark mark='b'/> {v2}"
        ) as vo:
            self.play(Create(ax), FadeIn(shade), FadeIn(sl), FadeIn(leg), FadeIn(pl), FadeIn(tag), FadeIn(plain))
            vo.wait_until("a")
            self.play(FadeIn(att), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        s = load("seq2seq")
        word = s["show"]
        r0 = s["runs"]["1-0"]
        steps = [int(x) for x in s["snap_steps"]]
        mats = [np.asarray(r0["snaps"][str(t)]) for t in steps]
        n = len(word)
        size = 3.9
        top = max(float(m_[:n + 1, :n].max()) for m_ in mats)  # one colour scale for every checkpoint

        def heat(i):
            m = mats[i][:n + 1, :n]
            return img_heat(m, size, sym=False, pos=ATT, height=size * m.shape[0] / m.shape[1],
                            vmax=top).move_to([-2.2, -0.4, 0])

        cur = heat(0)
        cw = cur.width / n
        xs = VGroup(*[data_text(c, font=MONO, font_size=20, color=GREY_A).move_to(
            cur.get_corner(UL) + np.array([cw * (k + 0.5), 0.25, 0])) for k, c in enumerate(word)])
        il = label(r"input", font_size=20, color=GREY_B).next_to(xs, UP, buff=0.1)
        ol = label(r"output step", font_size=20, color=DEC).rotate(PI / 2).next_to(cur, LEFT, buff=0.15)
        frame = SurroundingRectangle(cur, buff=0, color=GREY_D, stroke_width=1.2)
        cv = np.asarray(r0["curve"])
        ax = axes([0, steps[-1]], [0, 1.0], x_length=4.2, y_length=2.6, xlabel=r"training steps",
                  ylabel=r"20-letter strings right", xticks=[0, steps[-1]], yticks=[0, 1.0],
                  yfmt=lambda v: f"{int(100 * v)}\\%", center=[4.1, 0.6, 0])
        A = ax.ax
        k = ValueTracker(0)

        def path():
            t = steps[int(k.get_value())]
            m_ = cv[cv[:, 0] <= t]
            if len(m_) < 2:
                m_ = cv[:2]
            return VMobject(color=ATT, stroke_width=3.5).set_points_as_corners([A.c2p(a, b) for a, _, b in m_])

        live = always_redraw(path)
        clock = always_redraw(lambda: MathTex(rf"\text{{step }}{steps[int(k.get_value())]:,}".replace(",", "{,}"),
                                              font_size=28).move_to([4.1, -1.6, 0]))
        tag = note(r"computed: \ seed $0$, \ alignments at checkpoints").to_corner(DR, buff=0.2)
        # attention on the anti-diagonal (output letter r copies input letter n-1-r), at each checkpoint
        diag = [float(np.mean([mt[r_, n - 1 - r_] for r_ in range(n)])) for mt in mats]
        mass = diag[-1]
        i_b = next((i for i, d_ in enumerate(diag) if d_ > 0.5), None)
        t_diag = steps[i_b] if i_b is not None else steps[-1]
        if diag[0] < 0.3:
            early = "At first it looks everywhere a little, and learns nothing."
        else:
            early = "Even at first its attention leans toward the letters it needs."
        if i_b is not None:
            late = (f"Then a diagonal appears, running from the top right to the bottom left: the first letter "
                    f"written attends to the last one read, the second to the one before. By step {t_diag:,}, "
                    f"more than half its attention sits on that diagonal; by the end, {pct(mass, 0)} percent.")
        else:
            late = f"The diagonal stays faint: by the end only {pct(mass, 0)} percent of its attention is on it."
        long0, long1 = float(cv[0, 2]), float(cv[-1, 2])
        if long1 > long0 + 0.3:
            climb = "As the alignment sharpens, the accuracy on long strings climbs with it."
        else:
            climb = f"Yet the accuracy on long strings stays near {pct(long1, 0)} percent."
        i_b = 2 if i_b is None else max(1, min(i_b, len(mats) - 2))
        with self.voiceover(
            "Watch the alignment form during training. <bookmark mark='a'/> Rows are the letters it writes, "
            f"columns the letters it reads; bright is where it looks. {early} <bookmark mark='b'/> {late} "
            f"<bookmark mark='c'/> {climb} Bahdanau's translations showed the same picture: mostly diagonal, "
            "with the word order of French and English, and jumps where the two disagree."
        ) as vo:
            self.play(FadeIn(cur), Create(frame), FadeIn(xs), FadeIn(il), FadeIn(ol), Create(ax), FadeIn(tag))
            self.add(live, clock)
            vo.wait_until("a")
            for i in range(1, len(mats)):
                if i == i_b:
                    vo.wait_until("b")
                if i == len(mats) - 1:
                    vo.wait_until("c")
                nxt = heat(i)
                self.play(k.animate.set_value(i), FadeTransform(cur, nxt), run_time=1.0)
                cur = nxt
        for m in (live, clock):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def paper(self):
        B = BAHDANAU
        rows = [(r"RNNencdec-50 \ (one vector)", B["encdec"], B["encdec_nounk"], ENC),
                (r"RNNsearch-50 \ (attention)", B["search"], B["search_nounk"], ATT),
                (r"RNNsearch-50, \ trained longer", B["search_long"], B["search_long_nounk"], ATT),
                (r"Moses \ (phrase-based)", B["moses"], B["moses_nounk"], GREY_B)]
        tab = VGroup(VGroup(VectorizedPoint(), label(r"all sentences", font_size=22, color=GREY_A),
                            label(r"no unknown words", font_size=22, color=GREY_A)))
        for nm, a, b, c in rows:
            tab.add(VGroup(label(nm, font_size=22, color=c), MathTex(f"{a:.2f}", font_size=30, color=c),
                           MathTex(f"{b:.2f}", font_size=30, color=c)))
        colx = [-5.6, 1.0, 3.8]
        for ri, r in enumerate(tab):
            y = 1.4 - 0.7 * ri
            r[0].move_to([colx[0] + r[0].width / 2, y, 0])
            r[1].move_to([colx[1], y, 0])
            r[2].move_to([colx[2], y, 0])
        head = label(r"English to French, \ BLEU \ (Bahdanau et al., Table 1)", font_size=28).to_edge(UP, buff=0.5)
        foot = label(r"and on long sentences, \ no decline with length: \ their Figure 2", font_size=22,
                     color=GREY_A).to_edge(DOWN, buff=0.7)
        cite_ = cite(r"Bahdanau, Cho \& Bengio (2014)", corner=DR)
        with self.voiceover(
            "On real translation the gain was large. <bookmark mark='a'/> Bahdanau's encoder-decoder without "
            f"attention scored {B['encdec']} BLEU on English to French; with attention, {B['search']}. "
            "<bookmark mark='b'/> Trained longer, and counting only sentences without rare words, it reached "
            f"{B['search_long_nounk']}, past the phrase-based Moses system's {B['moses_nounk']}. And where the "
            "one-vector model fell apart on long sentences, the attention model held up at fifty words and more."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_), FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1], shift=RIGHT * 0.1), FadeIn(tab[2], shift=RIGHT * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(tab[3], shift=RIGHT * 0.1), FadeIn(tab[4], shift=RIGHT * 0.1), FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def after(self):
        items = [
            (2014, r"Graves, Wayne \& Danihelka; \ Weston, Chopra \& Bordes",
             r"neural Turing machines, \ memory networks: \ reading memory by content", HIST),
            (2015, r"Luong, Pham \& Manning; \ Xu et al.", r"dot-product scores; \ attention over the parts of an "
             r"image, \ to write captions", HIST),
            (2016, r"GNMT", r"attention in production translation", LSTMC),
            (2017, r"Vaswani et al., \ \textit{Attention Is All You Need}", r"drop the recurrence: \ attention "
             r"alone, \ everywhere: \ Parts 13 and 14", ATT),
        ]
        cards = VGroup(*[history_card(y, w, t, width=6.2, color=c, font_size=21) for y, w, t, c in items])
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.4)).move_to(DOWN * 0.15)
        head = label(r"a soft lookup: \ query, keys, values", font_size=34, color=ATT).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Attention is a soft lookup: a query, the decoder's state, compared with keys, the encoder's states, "
            "to fetch a mixture of values. <bookmark mark='a'/> The same year, neural Turing machines and memory "
            "networks used it to read memories. <bookmark mark='b'/> In 2015 Thang Luong and "
            "colleagues replaced Bahdanau's little scoring network with a dot product, and Kelvin Xu and "
            "colleagues pointed attention at the parts of a picture to write its caption. <bookmark mark='c'/> By "
            "2016 it was inside Google Translate. <bookmark mark='d'/> And in 2017 a team at Google asked what "
            "would happen if they dropped the recurrence altogether and kept only attention. That is the "
            "Transformer, and Parts 13 and 14."
        ) as vo:
            self.play(FadeIn(head))
            ghosts = cards.copy().set_opacity(0.25)
            self.play(FadeIn(ghosts))
            for i, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeOut(ghosts[i]), FadeIn(cards[i], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()
