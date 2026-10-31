from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai10.common import (ATT, CELLC, HIST, LSTMC, MONO, PART, load, pct, seed_band)
from videos.ai.ai10.specs import GNMT, SEQ2SEQ

ENC, DEC = C.TRUE_P, LSTMC


def loops(text: str, n: int = 10, times: int = 3) -> bool:
    """Does some stretch of ``n`` characters occur ``times`` times or more?"""
    seen = {}
    for i in range(len(text) - n + 1):
        k = text[i:i + n]
        seen[k] = seen.get(k, 0) + 1
    return max(seen.values(), default=0) >= times


class Seq2Seq(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.architecture()
        self.forcing()
        self.beam()
        self.bottleneck()
        self.gnmt()

    def card(self):
        card = chapter_card(14, r"Sequence to sequence", r"How can a network read one sequence and write another?",
                            lit=(1997,), part=PART)
        with self.voiceover("Chapter fourteen. Sequence to sequence."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def history(self):
        S = SEQ2SEQ
        cards = VGroup(
            history_card(2003, r"Philipp Koehn, Franz Och \& Daniel Marcu", r"phrase-based statistical translation: "
                         r"\ tables of phrase pairs and their counts; \ Part 7", width=4.3, color=HIST,
                         font_size=20),
            history_card(2014, r"Ilya Sutskever, Oriol Vinyals \& Quoc Le, \ Google",
                         rf"one LSTM reads the sentence, \ another writes the translation: \ ${S['ensemble']}$ BLEU "
                         rf"against the phrase-based ${S['smt']}$", width=4.3, color=LSTMC, font_size=20),
            history_card(2014, r"Kyunghyun Cho and colleagues, \ Montreal", r"the RNN encoder--decoder, \ with the "
                         r"GRU", width=4.3, color=HIST, font_size=20),
        ).arrange(RIGHT, buff=0.25, aligned_edge=UP).move_to(UP * 0.6)
        if cards.width > 13.4:
            cards.width = 13.4
        bleu = label(r"BLEU (Papineni et al., 2002): \ how many words and phrases of the output appear in human "
                     r"translations, \ $0$ to $100$", font_size=20, color=GREY_B).to_edge(DOWN, buff=0.9)
        trick = label(rf"a trick: \ read the source sentence backwards: \ BLEU ${S['reverse_before']}$ $\to$ "
                      rf"${S['reverse_after']}$", font_size=22, color=CELLC).next_to(bleu, UP, buff=0.25)
        cite_ = cite(r"Koehn et al.\ (2003); \ Sutskever et al.\ (2014); \ Cho et al.\ (2014)", corner=DR)
        with self.voiceover(
            "By 2014 machine translation was statistical. <bookmark mark='a'/> The best systems, phrase-based, "
            "from Part 7, used huge tables of phrase pairs and a dozen separately tuned parts. "
            "<bookmark mark='b'/> In September 2014 Ilya Sutskever, Oriol Vinyals and Quoc Le at Google replaced it "
            "all with two LSTMs: one reads the English sentence into its memory, the other starts from that memory "
            f"and writes French. Five of them together scored {S['ensemble']} BLEU, beating the phrase-based "
            f"baseline's {S['smt']}. <bookmark mark='c'/> One trick mattered: reading the source backwards, so "
            "its first words, which the translation needs first, are the last ones read. <bookmark mark='d'/> "
            "Kyunghyun Cho's group in Montreal built the same design with the GRU."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(bleu))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(trick, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def architecture(self):
        src, tgt = "the cat sat".split(), "le chat était assis".split()
        enc = VGroup(*[Circle(radius=0.32, stroke_color=ENC, stroke_width=2.5, fill_color=ENC, fill_opacity=0.15)
                       for _ in src]).arrange(RIGHT, buff=0.8).move_to([-4.0, 0.2, 0])
        dec = VGroup(*[Circle(radius=0.32, stroke_color=DEC, stroke_width=2.5, fill_color=DEC, fill_opacity=0.15)
                       for _ in tgt]).arrange(RIGHT, buff=0.8).move_to([3.0, 0.2, 0])
        sw = VGroup(*[data_text(w, font=MONO, font_size=22, color=GREY_A).next_to(c, DOWN, buff=0.6)
                      for w, c in zip(src, enc)])
        tw = VGroup(*[data_text(w, font=MONO, font_size=22, color=DEC).next_to(c, UP, buff=0.6)
                      for w, c in zip(tgt, dec)])
        sa = VGroup(*[Arrow(w.get_top(), c.get_bottom(), buff=0.06, stroke_width=2, color=GREY_B) for w, c in
                      zip(sw, enc)])
        ta = VGroup(*[Arrow(c.get_top(), w.get_bottom(), buff=0.06, stroke_width=2, color=DEC) for w, c in
                      zip(tw, dec)])
        ea = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.05, stroke_width=2.5, color=ENC) for a, b in
                      zip(enc, enc[1:])])
        da = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.05, stroke_width=2.5, color=DEC) for a, b in
                      zip(dec, dec[1:])])
        vec = VGroup(*[Square(0.22, stroke_width=0, fill_color=CELLC, fill_opacity=0.3 + 0.1 * k) for k in range(6)])
        vec.arrange(DOWN, buff=0.03).move_to([-0.5, 0.2, 0])
        va = Arrow(enc[-1].get_right(), vec.get_left(), buff=0.06, stroke_width=3, color=CELLC)
        vb = Arrow(vec.get_right(), dec[0].get_left(), buff=0.06, stroke_width=3, color=CELLC)
        vl = label(r"one vector: \\ the whole sentence", font_size=20, color=CELLC).next_to(vec, UP, buff=0.25)
        fb = VGroup(*[CurvedArrow(w.get_right() + DOWN * 0.05, d.get_left() + DOWN * 0.15, angle=-0.8, color=GREY_C,
                                  stroke_width=1.5, tip_length=0.12) for w, d in zip(tw, dec[1:])])
        el = label(r"encoder", font_size=24, color=ENC).next_to(enc, DOWN, buff=1.4)
        dl = label(r"decoder", font_size=24, color=DEC).next_to(dec, DOWN, buff=1.4)
        fl = label(r"each word written is fed back in", font_size=20, color=GREY_B).next_to(tw, UP, buff=0.25)
        tag = note(r"schematic").to_corner(DR, buff=0.3)
        with self.voiceover(
            "The design has two halves. <bookmark mark='a'/> The encoder reads the input one symbol at a time, "
            "updating its state. <bookmark mark='b'/> Its last state is a single vector that has to stand for the "
            "whole sentence. <bookmark mark='c'/> The decoder starts from that vector and writes the output one "
            "symbol at a time, each step a softmax over the vocabulary, <bookmark mark='d'/> and each word it "
            "writes is fed back in as the next step's input, until it writes an end-of-sentence symbol."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(sw), LaggedStart(*[GrowArrow(a) for a in sa], lag_ratio=0.2), FadeIn(enc),
                      LaggedStart(*[GrowArrow(a) for a in ea], lag_ratio=0.3), FadeIn(el))
            vo.wait_until("b")
            self.play(GrowArrow(va), FadeIn(vec), FadeIn(vl))
            vo.wait_until("c")
            self.play(GrowArrow(vb), FadeIn(dec), LaggedStart(*[GrowArrow(a) for a in da], lag_ratio=0.3),
                      LaggedStart(*[GrowArrow(a) for a in ta], lag_ratio=0.3), FadeIn(tw), FadeIn(dl))
            vo.wait_until("d")
            self.play(LaggedStart(*[Create(f) for f in fb], lag_ratio=0.3), FadeIn(fl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def forcing(self):
        words = ["le", "chat", "est", "assis"]
        own = ["le", "chien", "a", "faim"]
        def row(ins, outs, y, col_in, title):
            cells = VGroup(*[RoundedRectangle(width=1.3, height=0.6, corner_radius=0.1, stroke_color=DEC,
                                              stroke_width=2) for _ in outs]).arrange(RIGHT, buff=0.35)
            cells.move_to([1.0, y, 0])
            i_t = VGroup(*[data_text(w, font=MONO, font_size=20, color=c).next_to(cl, DOWN, buff=0.35)
                           for w, cl, c in zip(ins, cells, col_in)])
            o_t = VGroup(*[data_text(w, font=MONO, font_size=20, color=DEC).next_to(cl, UP, buff=0.25)
                           for w, cl in zip(outs, cells)])
            t = label(title, font_size=22, color=GREY_A).next_to(cells, LEFT, buff=0.5)
            return VGroup(t, cells, i_t, o_t)

        top = row(["<s>"] + words[:-1], words, 1.5, [GREY_A] * 4, r"training: \\ teacher forcing")
        bot = row(["<s>"] + own[:-1], own, -1.4, [GREY_A] + [C.PENALTY] * 3, r"testing: \\ its own words")
        tl = label(r"fed the true previous word", font_size=20, color=GREY_A).next_to(top[2], DOWN, buff=0.15)
        bl = label(r"fed its own previous word: \ one slip, and it continues from the slip", font_size=20,
                   color=C.PENALTY).next_to(bot[2], DOWN, buff=0.15)
        cite_ = cite(r"Williams \& Zipser (1989); \ Bengio, Vinyals, Jaitly \& Shazeer (2015)", corner=DR)
        tag = note(r"illustrative").to_corner(UR, buff=0.3)
        with self.voiceover(
            "How is the decoder trained? <bookmark mark='a'/> By teacher forcing, from Ronald Williams and David "
            "Zipser in 1989: at every step, feed it the true previous word, and ask for the next. "
            "<bookmark mark='b'/> At test time there is no true history, only its own: one mistake, and every later "
            "step continues from a history it never saw in training."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(top), FadeIn(tl))
            vo.wait_until("b")
            self.play(FadeIn(bot), FadeIn(bl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def beam(self):
        m = load("charlstm")
        # a schematic tree: two beams kept at each depth
        root = Dot([-5.8, 0.6, 0], radius=0.08, color=WHITE)
        kept = []
        prev = [root]
        g = VGroup(root)
        edges = VGroup()
        for d in range(3):
            nxt = []
            for p in prev:
                for k in range(3):
                    y = p.get_y() + (1 - k) * (1.2 / (d + 1))
                    q = Dot([p.get_x() + 1.4, y, 0], radius=0.07, color=GREY_C)
                    edges.add(Line(p.get_center(), q.get_center(), color=GREY_D, stroke_width=1.5))
                    nxt.append(q)
            g.add(*nxt)
            keep = nxt[:2]
            for q in keep:
                q.set_color(ATT)
            kept.append(keep)
            prev = keep
        tl = label(r"beam search, \ width $2$: \ keep the two most probable prefixes", font_size=22,
                   color=ATT).next_to(g, UP, buff=0.3).align_to(g, LEFT)
        tag = note(r"schematic").next_to(g, DOWN, buff=0.3).align_to(g, LEFT)
        rows = VGroup()
        items = [(r"greedy", m["greedy"], m["greedy_bits"], GREY_A), (r"beam of $8$", m["beam"], m["beam_bits"], ATT),
                 (r"sampled", m["sampled"], m["sampled_bits"], LSTMC)]
        for name, txt, b, col in items:
            t = " ".join(txt.split())[:58]
            rows.add(VGroup(label(rf"{name}: \ ${b:.0f}$ bits", font_size=20, color=col),
                            data_text(t, font="DejaVu Serif", font_size=17, color=WHITE)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                 buff=0.08))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.6, -0.2, 0])
        for r in rows:
            if r.width > 7.4:
                r.width = 7.4
        keep_in_frame(rows)
        pr = data_text(m["prompt"].strip(), font="DejaVu Serif", font_size=18, color=GREY_B).next_to(rows, UP, buff=0.3)
        pr.align_to(rows, LEFT)
        pl = label(r"our character LSTM, \ $120$ characters after:", font_size=20, color=GREY_A).next_to(pr, UP,
                                                                                                    buff=0.1)
        pl.align_to(rows, LEFT)
        rep = loops(m["beam"]) or loops(m["greedy"])
        tail = ("But look at the most probable text: it goes round in circles, what Ari Holtzman and colleagues "
                "later called neural text degeneration; for open-ended writing, sampling is used instead." if rep else
                "For open-ended writing the most probable text is often dull, which is why language models sample "
                "instead; for translation, where the aim is a faithful rendering, beam search became common.")
        with self.voiceover(
            "Writing the most probable output exactly would mean searching every possible sequence. Greedy "
            "decoding takes the single best word at each step instead. <bookmark mark='a'/> Beam search keeps a "
            "few of the best partial outputs at every step, extends each, and keeps the best of those: a cheap "
            "compromise. <bookmark mark='b'/> On our character "
            "LSTM, from the same prompt: greedy decoding writes text that costs "
            f"{m['greedy_bits']:.0f} bits under the model, a beam of eight finds text costing {m['beam_bits']:.0f}, "
            f"and a random sample costs {m['sampled_bits']:.0f}. <bookmark mark='c'/> {tail}"
        ) as vo:
            self.play(FadeIn(root), FadeIn(tl))
            self.play(Create(edges), FadeIn(g[1:]), FadeIn(tag), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(pl), FadeIn(pr), LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in rows], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bottleneck(self):
        s = load("seq2seq")
        tests = np.asarray(s["test"])
        lo, hi = s["train"]
        runs = s["runs"]
        ax = axes([tests[0], tests[-1]], [0, 1.0], x_length=7.0, y_length=4.0, xlabel=r"length of the string",
                  ylabel=r"reversed exactly", xticks=[5, 10, 15, 20, 25, 30], yticks=[0, 0.5, 1.0],
                  yfmt=lambda v: f"{int(100 * v)}\\%", center=[-1.6, -0.4, 0])
        A = ax.ax
        shade = Rectangle(width=A.c2p(hi, 0)[0] - A.c2p(lo, 0)[0], height=A.c2p(0, 1)[1] - A.c2p(0, 0)[1],
                          stroke_width=0, fill_color=GREY_D, fill_opacity=0.25)
        shade.move_to([(A.c2p(lo, 0)[0] + A.c2p(hi, 0)[0]) / 2, (A.c2p(0, 0)[1] + A.c2p(0, 1)[1]) / 2, 0])
        sl = label(r"trained on these lengths", font_size=20, color=GREY_B).next_to(shade, UP, buff=0.08)
        sl.align_to(shade, RIGHT)  # clear of the axis label at the top left
        plain = seed_band(A, tests, [runs[f"0-{k}"]["exact"] for k in (0, 1, 2)], ENC)
        ex = data_text("attention → noitnetta", font=MONO, font_size=24, color=GREY_A).to_corner(UR, buff=0.5)
        leg = legend([(ENC, r"encoder--decoder, \ one vector")], font_size=22).next_to(ex, DOWN, buff=0.3)
        leg.align_to(ex, RIGHT)
        mean = np.mean([runs[f"0-{k}"]["exact"] for k in (0, 1, 2)], 0)
        half = next((int(n) for n, v in zip(tests, mean) if v < 0.5), None)
        b = runs["0-0"]["beam"]
        bt = VGroup(label(r"greedy against a beam of $4$:", font_size=20, color=GREY_A),
                    *[MathTex(rf"n = {n}:\ {100 * v[0]:.0f}\% \to {100 * v[1]:.0f}\%", font_size=24, color=ATT)
                      for n, v in sorted(b.items(), key=lambda kv: int(kv[0]))]).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.1)
        bt.next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        keep_in_frame(bt)
        tag = note(rf"computed: \ a bidirectional GRU encoder, \ a GRU decoder, \ ${s['steps']:,}$ steps, \ three "
                   rf"seeds".replace(",", "{,}")).to_corner(DR, buff=0.2)
        if half is not None:
            v = (f"Short strings come out right. Past about {half} letters, fewer than half do, and outside the "
                 "lengths it trained on, almost none: one vector can't hold them all.")
        else:
            v = "It reverses most strings, though less reliably as they grow."
        gains = [v_[1] - v_[0] for v_ in b.values()]
        bv = (f"A beam of four helps a little, by up to {100 * max(gains):.0f} points." if max(gains) > 0.02 else
              "A beam of four hardly helps: the information is simply not in the vector.")
        with self.voiceover(
            "We built a small encoder-decoder, and gave it a job with no ambiguity: write a string of letters "
            "backwards. <bookmark mark='a'/> It trained on strings of "
            f"{lo} to {hi} letters, three times from different starts. <bookmark mark='b'/> {v} "
            f"<bookmark mark='c'/> {bv} The whole input has to squeeze through the encoder's last state: "
            "a bottleneck, and the longer the input, the worse it gets."
        ) as vo:
            self.play(Create(ax), FadeIn(ex), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(shade), FadeIn(sl))
            vo.wait_until("b")
            self.play(FadeIn(plain), FadeIn(leg), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(bt))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gnmt(self):
        hc = history_card(2016, r"Yonghui Wu, Mike Schuster, Zhifeng Chen, Quoc Le and colleagues, \ Google",
                          rf"GNMT: \ ${GNMT['layers']}$-layer LSTMs, \ residual connections, \ attention; \ "
                          rf"in side-by-side ratings, \ ${GNMT['error_cut']}\%$ fewer translation errors than the "
                          r"phrase-based system", width=7.4, color=HIST).move_to(UP * 0.9)
        prod = label(r"September 2016: \ Google Translate's Chinese to English switches to it, \\ about "
                     r"$18$ million translations a day", font_size=24, color=WHITE).next_to(hc, DOWN, buff=0.5)
        nxt = label(r"one ingredient still to explain: \ attention", font_size=28, color=ATT).to_edge(DOWN, buff=0.6)
        cite_ = cite(r"Wu et al.\ (2016); \ Le \& Schuster, Google Research blog (2016)", corner=DR)
        with self.voiceover(
            "Two years later the idea was in production. <bookmark mark='a'/> Google's neural machine "
            "translation system of 2016 stacked eight layers of LSTMs on each side, and in side-by-side ratings by people it cut translation errors by "
            f"{GNMT['error_cut']} percent on average against Google's own phrase-based system. "
            "<bookmark mark='b'/> In September 2016 it took over Google Translate's Chinese to English, about "
            "eighteen million translations a day. "
            "<bookmark mark='c'/> But GNMT had one more ingredient, the one that removed the bottleneck."
        ) as vo:
            self.play(FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(prod, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(nxt))
        self.wait(0.3)
        self.clear_scene()


_ = pct
