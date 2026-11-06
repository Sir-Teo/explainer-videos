from __future__ import annotations

from explainer.cs import *  # noqa: F403
from explainer.cs.algo import crypto as K
from videos.cs.cs29.common import (BG, DATA, HEAD, NO, PART, YES, fit_right, load, mono)

A2Z = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def chi2(col, shift):
    n = len(col)
    obs = [0] * 26
    for c in col:
        obs[(A2Z.index(c) - shift) % 26] += 1
    return sum((obs[i] - n * K.ENGLISH_FREQ[A2Z[i]]) ** 2 / (n * K.ENGLISH_FREQ[A2Z[i]]) for i in range(26))


class Vigenere(VoiceoverScene):
    def construct(self):
        self.card()
        self.many()
        self.coincidence()
        self.columns()

    def card(self):
        card = chapter_card(2, r"Vigen\`ere and the index of coincidence", r"What if every letter has its own shift?",
                            lit=(1854, 1863, 1922), extra=((1854, r"Babbage breaks Vigen\`ere"), (1863, r"Kasiski"),
                                                           (1922, r"Friedman: \ coincidence")), part=PART)
        with self.voiceover("Chapter two. Vigenère, and the index of coincidence."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def many(self):
        v = load("vigenere")
        head = label(r"Many shifts, \ by a keyword", font_size=34).to_edge(UP, buff=0.3)
        n = 28
        dx = 0.42
        pt = v["plain"][:n]
        key = (v["key"] * 5)[:n]
        ct = v["cipher60"][:n]

        def row(s, color):
            g = VGroup(*[mono(c, 21, color).move_to([dx * i, 0, 0]) for i, c in enumerate(s)])
            return g
        rp, rk, rc = row(pt, WHITE), row(key, HEAD), row(ct, DATA)
        grid = VGroup(rp, rk, rc).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.6)
        tags = VGroup(*[label(t, font_size=18, color=c).next_to(r, LEFT, buff=0.3) for t, c, r in
                        ((r"plain", GREY_A, rp), (r"key", HEAD, rk), (r"cipher", DATA, rc))])
        VGroup(grid, tags).move_to([0, grid.get_y(), 0])
        es = [i for i, c in enumerate(pt) if c == "E"]
        marks = VGroup(*[SurroundingRectangle(VGroup(rp[i], rc[i]), color=YES, buff=0.06, stroke_width=2) for i in es])
        lines = VGroup(
            label(r"Bellaso \ (1553), \ later credited to Vigen\`ere: \ shift each letter by the next letter of a "
                  r"keyword", font_size=22, color=WHITE),
            label(r"the same plain letter becomes different cipher letters: \ the counts flatten out", font_size=22,
                  color=YES),
            label(r"\textit{le chiffre ind\'echiffrable}: \ trusted for 300 years", font_size=22, color=HEAD),
            label(r"Babbage \ (1854, \ unpublished) \ and Kasiski \ (1863): \ find the keyword's \textbf{length}, "
                  r"\ and it falls apart", font_size=22, color=NO),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The defence against counting is to use many substitutions. <bookmark mark='a'/> Giovan Battista Bellaso "
            "described it in 1553, and it was later credited to Blaise de Vigenère: shift each letter by the next "
            "letter of a keyword, here BABBAGE, repeating. A shifts by zero, B by one, G by six. <bookmark mark='b'/> "
            "Now the same plaintext letter becomes different ciphertext letters. These five E's are enciphered as "
            "K, E, F, E and K. The letter counts flatten out, and al-Kindi's method has nothing to grip. <bookmark "
            "mark='c'/> It was called the indecipherable cipher, and trusted for three hundred years. <bookmark "
            "mark='d'/> Then Charles Babbage, in 1854, and Friedrich Kasiski, in 1863, saw the weakness: once you "
            "know the length of the keyword, the cipher falls apart into simple shifts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rp), FadeIn(tags[0]))
            vo.wait_until("a")
            self.play(FadeIn(rk), FadeIn(tags[1]), FadeIn(lines[0]))
            self.play(FadeIn(rc), FadeIn(tags[2]))
            vo.wait_until("b")
            self.play(Create(marks), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def coincidence(self):
        v = load("vigenere")
        head = label(r"The index of coincidence", font_size=34).to_edge(UP, buff=0.3)
        sc = {int(k): s for k, s in v["scores"].items()}
        ax = Axes(x_range=[0, 21, 1], y_range=[0.03, 0.075, 0.01], x_length=7.2, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.55).to_edge(
            LEFT, buff=0.9)
        bars = VGroup()
        for L, s in sc.items():
            top = ax.c2p(L, s)
            base = ax.c2p(L, 0.03)
            bars.add(Rectangle(width=0.22, height=top[1] - base[1], stroke_width=0,
                               fill_color=YES if s > 0.06 else DATA, fill_opacity=0.85).move_to(base, aligned_edge=DOWN))
        xt = VGroup(*[label(str(L), font_size=15, color=GREY_A).next_to(ax.c2p(L, 0.03), DOWN, buff=0.1)
                      for L in (1, 5, 7, 10, 14, 15, 20)])
        yt = VGroup(*[label(f"{y:.2f}", font_size=15, color=GREY_A).next_to(ax.c2p(0, y), LEFT, buff=0.1)
                      for y in (0.04, 0.05, 0.06, 0.07)])
        xl = label(r"guessed key length $L$", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.15)
        eng = DashedLine(ax.c2p(0, v["ioc_plain"]), ax.c2p(21, v["ioc_plain"]), color=YES, stroke_width=1.5)
        rnd = DashedLine(ax.c2p(0, v["ioc_random"]), ax.c2p(21, v["ioc_random"]), color=NO, stroke_width=1.5)
        el = label(rf"English: \ {v['ioc_plain']:.3f}", font_size=16, color=YES).next_to(eng, UP, buff=0.05).align_to(
            ax, RIGHT)
        rl = label(r"random: \ $1/26 = 0.038$", font_size=16, color=NO).next_to(rnd, UP, buff=0.05).align_to(ax, RIGHT)
        for t_ in (el, rl):
            t_.add_background_rectangle(color=BG, opacity=0.85, buff=0.04)
        notes = VGroup(
            label(r"IC: \ the chance that two letters \\ picked at random are equal", font_size=20, color=WHITE),
            label(r"$\mathrm{IC} = \sum_c p_c^2$: \ English is lumpy, \\ so it scores high", font_size=20,
                  color=GREY_A),
            label(rf"whole ciphertext: \ {v['ioc_cipher']:.3f}, \\ close to random", font_size=20, color=DATA),
            label(r"split into $L$ columns: \ if $L$ is right, \\ each column is one Caesar shift \\ of English",
                  font_size=20, color=HEAD),
            label(rf"peaks at $L$ = 7 and 14: \\ the key has 7 letters", font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).next_to(ax, RIGHT, buff=0.5).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "William Friedman gave the test its modern form in 1922. <bookmark mark='a'/> The index of coincidence "
            "is the chance that two letters picked at random from a text are the same. English is lumpy, with many "
            "E's and T's, so it scores about six and a half percent; letters spread evenly score one in twenty-six, "
            "under four percent. <bookmark mark='b'/> Our whole ciphertext scores four and a half: close to random, "
            "as the cipher intends. <bookmark mark='c'/> Now guess a key length, and split the ciphertext into that "
            "many columns: every first letter, every second letter, and so on. If the guess is right, each column was "
            "shifted by a single letter, and its index jumps back up to English. <bookmark mark='d'/> Try every "
            "length from one to twenty. Seven stands out, and fourteen, its double. The key has seven letters."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(FadeIn(notes[1]), Create(eng), FadeIn(el), Create(rnd), FadeIn(rl))
            vo.wait_until("b")
            self.play(FadeIn(notes[2]))
            vo.wait_until("c")
            self.play(FadeIn(notes[3]))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), run_time=2.5)
            self.bring_to_front(el, rl)
            self.play(FadeIn(notes[4]))
        self.wait(0.3)
        self.clear_scene()

    def columns(self):
        v = load("vigenere")
        head = label(r"Seven Caesar ciphers", font_size=34).to_edge(UP, buff=0.3)
        ct = v["cipher"]
        L = len(v["recovered"])
        col = ct[0::L]
        ch = [chi2(col, s) for s in range(26)]
        best = min(range(26), key=lambda s: ch[s])
        ax = Axes(x_range=[0, 26, 1], y_range=[0, 3.2, 1], x_length=6.4, y_length=2.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.7).to_edge(
            LEFT, buff=0.8)
        import math
        bars = VGroup()
        for s in range(26):
            y = math.log10(ch[s])
            base = ax.c2p(s + 0.5, 0)
            top = ax.c2p(s + 0.5, y)
            bars.add(Rectangle(width=0.18, height=top[1] - base[1], stroke_width=0,
                               fill_color=YES if s == best else DATA, fill_opacity=0.85).move_to(base,
                                                                                             aligned_edge=DOWN))
        letters = VGroup(*[mono(A2Z[s], 13, YES if s == best else GREY_A).next_to(ax.c2p(s + 0.5, 0), DOWN, buff=0.08)
                           for s in range(26)])
        yl = label(r"mismatch with English \ ($\chi^2$, \ log scale)", font_size=16, color=GREY_A).next_to(
            ax, UP, buff=0.3).align_to(ax, LEFT)
        xl = label(r"shift of column 1", font_size=16, color=GREY_A).next_to(letters, DOWN, buff=0.12)
        keyrow = VGroup(*[mono(c, 34, HEAD) for c in v["recovered"]]).arrange(RIGHT, buff=0.25)
        keyrow.next_to(ax, RIGHT, buff=0.9).align_to(ax, UP).shift(DOWN * 0.4)
        kl = label(r"the key, \ column by column", font_size=18, color=GREY_A).next_to(keyrow, UP, buff=0.2)
        dec = K.vigenere(ct, v["recovered"], decrypt=True)
        out = mono(dec[:40], 20, YES).next_to(VGroup(ax, letters, xl), DOWN, buff=0.45).to_edge(LEFT, buff=0.8)
        lines = VGroup(
            label(r"each column: \ try all 26 shifts, \ keep the one whose counts look most like English",
                  font_size=21, color=WHITE),
            label(rf"the key: \ \texttt{{{v['recovered']}}} \ (correct), \ and all 600 letters decrypt",
                  font_size=21, color=YES),
            label(r"the lesson: \ a short key, \ reused, \ leaves patterns; \ statistics find them", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "With the length known, each column is a Caesar cipher. <bookmark mark='a'/> For the first column, try "
            "all twenty-six shifts and measure how far each result's letter counts are from English. One shift, B, "
            "fits far better than any other. <bookmark mark='b'/> Repeat for each of the seven columns, and the "
            "keyword reads itself off: BABBAGE. All six hundred letters decrypt. <bookmark mark='c'/> The lesson "
            "outlives the cipher. A short key used over and over leaves patterns in the ciphertext, and statistics "
            "will find them. Every cipher in this part either uses its key once, like Shannon's, or stretches it "
            "into something that never repeats."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(letters), FadeIn(yl), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), FadeIn(lines[0]),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(kl), LaggedStart(*[FadeIn(k, shift=DOWN * 0.2) for k in keyrow], lag_ratio=0.3),
                      FadeIn(lines[1]))
            self.play(FadeIn(out))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()
