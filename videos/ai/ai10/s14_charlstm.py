from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai10.common import (CELLC, GATEC, LSTMC, MONO, PART, load, rgb)

LM_C = C.NEURAL


def board_rows():
    """The scoreboard so far: Part 1's rows (its cache; or, where Part 1's language-model rows haven't been computed,
    the rows its counting models and compressors give), Part 7's Kneser-Ney, Part 9's neural models, and ours."""
    from videos.ai.ai1 import compute as c1
    from videos.ai.ai7 import compute as c7
    from videos.ai.ai9 import compute as c9

    try:
        rows = [dict(r) for r in c1.load("scoreboard")["rows"]]
    except FileNotFoundError:
        raw = c1.load("raw")
        rows = [
            dict(key="ascii", label="plain text file", bits=8.0, part=1, kind="baseline"),
            dict(key="uniform", label=f"uniform over its {raw['passage_symbols']} symbols", bits=raw["uniform"],
                 part=1, kind="count"),
            dict(key="order0", label="letter frequencies", bits=raw["rows"][0]["test"], part=1, kind="count"),
            dict(key="order1", label="the previous character", bits=raw["rows"][1]["test"], part=1, kind="count"),
            dict(key="gzip", label="gzip", bits=raw["compressors"]["gzip"], part=1, kind="compressor"),
            dict(key="xz", label="xz", bits=raw["compressors"]["xz"], part=1, kind="compressor"),
            dict(key="bzip2", label="bzip2", bits=raw["compressors"]["bzip2"], part=1, kind="compressor"),
            dict(key="best", label=f"the previous {raw['best']} characters", bits=raw["best_bits"], part=1,
                 kind="count"),
            dict(key="human", label="people (Shannon 1951, letters only)", lo=0.6, hi=1.3, part=1, kind="human"),
        ]
    k, n, me = c7.load("kn"), c9.load("lm"), load("charlstm")
    i = next(j for j, r in enumerate(rows) if r["key"] == "best") + 1
    rows.insert(i, dict(key="kn", label=rf"Kneser--Ney, \ ${k['best']}$ characters", bits=k["best_bits"], part=7,
                        kind="count"))
    rows.insert(i + 1, dict(key="nlm", label=rf"a neural model, \ ${n['n_ctx']}$ characters", bits=n["passage_bits"],
                            part=9, kind="lm"))
    rows.insert(i + 2, dict(key="mix", label=r"the neural model $+$ Kneser--Ney", bits=n["mix_bits"], part=9,
                            kind="lm"))
    rows.insert(i + 3, dict(key="lstm", label=rf"a character LSTM, \ ${me['hidden']}$ cells", bits=me["passage_bits"],
                            part=10, kind="lm"))
    return rows, i + 3, n, k


class CharLSTM(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.replay()
        self.board()
        self.quotes()
        self.surprise()

    def card(self):
        card = chapter_card(13, r"A character LSTM", r"How well does an LSTM play Shannon's guessing game?",
                            lit=(1997, 2003), part=PART)
        with self.voiceover("Chapter thirteen. A character LSTM."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def model(self):
        m = load("charlstm")
        n_read = int(m["batch"])
        streams = VGroup()
        for r in range(8):
            y = 1.9 - 0.42 * r
            line = Line([-6.2, y, 0], [1.0, y, 0], color=GREY_D, stroke_width=4)
            done = Line([-6.2, y, 0], [-6.2 + 7.2 * 0.38, y, 0], color=LM_C, stroke_width=4)
            win = Rectangle(width=0.5, height=0.26, stroke_color=CELLC, stroke_width=2).move_to(done.get_end() +
                                                                                                 RIGHT * 0.25)
            streams.add(VGroup(line, done, win))
        dots = MathTex(r"\vdots", font_size=30, color=GREY_B).next_to(streams, DOWN, buff=0.1)
        sl = label(rf"${n_read}$ readers, \ each through its own stretch of the novels", font_size=22, color=GREY_A)
        sl.next_to(streams, UP, buff=0.2).align_to(streams, LEFT)
        wl = label(rf"each step: \ the next ${m['bptt']}$ characters; \\ the memory carried on to the next step",
                   font_size=20, color=CELLC).next_to(dots, DOWN, buff=0.15).align_to(streams, LEFT)
        facts = VGroup(
            label(rf"a vector of ${m['emb']}$ numbers for each of ${m['K']}$ characters", font_size=22, color=GREY_A),
            label(rf"one LSTM layer, \ ${m['hidden']}$ cells", font_size=22, color=LSTMC),
            label(r"a softmax over the next character", font_size=22, color=GREY_A),
            label(rf"${m['params']:,}$ weights".replace(",", "{,}"), font_size=24, color=WHITE),
            label(rf"${m['chars_seen'] / 1e6:.1f}$ million characters read, \ "
                  rf"${100 * m['chars_seen'] / m['train_chars']:.0f}\%$ of the books", font_size=22, color=GREY_A),
            label(rf"${m['seconds'] / 60:.0f}$ minutes on this computer; \ gradient clipped on "
                  rf"${m['clipped']}$ of ${m['steps']:,}$ steps".replace(",", "{,}"), font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.4, 0.3, 0])
        if facts.width > 5.0:
            facts.width = 5.0
        cite_ = cite(r"after Karpathy (2015), \ \textit{The Unreasonable Effectiveness of Recurrent Neural Networks}",
                     corner=DL)
        mins = m["seconds"] / 60
        with self.voiceover(
            "Now the LSTM plays the series' game: guess the next character. <bookmark mark='a'/> Each character "
            f"becomes a learned vector; one layer of {m['hidden']} LSTM cells reads them in order; a softmax "
            f"guesses the next. {m['params']:,} weights in all. <bookmark mark='b'/> We train it as Andrej "
            "Karpathy's char-rnn did in 2015: cut the thirty novels into "
            f"{n_read} long stretches, one reader on each, {m['bptt']} characters per step, the memory carried "
            "on from step to step while the gradient is cut at each step's edge. <bookmark mark='c'/> It read "
            f"{m['chars_seen'] / 1e6:.1f} million characters, about "
            f"{100 * m['chars_seen'] / m['train_chars']:.0f} percent of the books, once, in {mins:.0f} minutes on "
            "this computer."
        ) as vo:
            big = facts[:4].copy().scale(1.45).move_to([0, 0.4, 0])
            self.play(FadeIn(big, lag_ratio=0.2), FadeIn(cite_))
            vo.wait_until("b")
            self.play(ReplacementTransform(big, facts[:4]))
            self.play(FadeIn(streams), FadeIn(dots), FadeIn(sl), FadeIn(wl))
            self.play(*[s[2].animate.shift(RIGHT * 1.2) for s in streams],
                      *[s[1].animate.put_start_and_end_on(s[1].get_start(), s[1].get_end() + RIGHT * 1.2)
                        for s in streams], run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(facts[4:], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        m = load("charlstm")
        ev = np.asarray(m["evals"], float)
        snaps = m["snaps"]
        n9, kn = load_nlm()
        S = int(m["steps"])
        top = 5.0
        ax = axes([0, S], [1.5, top], x_length=6.6, y_length=3.4, xlabel=r"training steps",
                  ylabel=r"bits per character on the passage", xticks=[0, S // 2, S], yticks=[2, 3, 4, 5],
                  center=[-2.4, 0.9, 0])
        A = ax.ax
        l9 = DashedLine(A.c2p(0, n9), A.c2p(S, n9), color=GREY_B, stroke_width=2)
        t9 = label(rf"Part 9's neural model: \ ${n9:.2f}$", font_size=20, color=GREY_B).next_to(l9, UP, buff=0.05)
        t9.align_to(l9, RIGHT)
        lk = DashedLine(A.c2p(0, kn), A.c2p(S, kn), color=C.COUNTING, stroke_width=2)
        tk = label(rf"Part 7's Kneser--Ney: \ ${kn:.2f}$", font_size=20, color=C.COUNTING).next_to(lk, DOWN, buff=0.05)
        tk.align_to(lk, RIGHT)
        t = ValueTracker(0.0)

        def clip(y):
            return float(np.clip(y, 1.5, top))

        def upto():
            n_ = max(2, int(np.searchsorted(ev[:, 0], t.get_value(), side="right")))
            pts = [A.c2p(x, clip(y)) for x, y in ev[:n_, :2]]
            if n_ < len(ev):
                x = t.get_value()
                pts.append(A.c2p(x, clip(np.interp(x, ev[:, 0], ev[:, 1]))))
            return VMobject(color=LM_C, stroke_width=4).set_points_as_corners(pts)

        live = always_redraw(upto)
        clock = always_redraw(lambda: VGroup(
            MathTex(rf"\text{{step }}{int(round(t.get_value())):,}".replace(",", "{,}"), font_size=28),
            MathTex(rf"{float(np.interp(t.get_value(), ev[:, 0], ev[:, 1])):.2f}\ \text{{bits/char}}", font_size=28,
                    color=LM_C)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.8, 2.0, 0]))
        panel = RoundedRectangle(width=13.0, height=1.9, corner_radius=0.12, stroke_color=GREY_D, stroke_width=1.5,
                                 fill_color="#121722", fill_opacity=1).move_to([0, -2.6, 0])
        pl = label(r"what it writes now, \ from Part 9's prompt and the same random draws:", font_size=20,
                   color=GREY_A).next_to(panel.get_corner(UL), DR, buff=0.12)

        def sample_text(s):
            txt = " ".join(s.split())[:116]
            g = VGroup(data_text(m["prompt"].strip(), font="DejaVu Serif", font_size=19, color=GREY_B),
                       data_text(txt, font="DejaVu Serif", font_size=19, color=WHITE)).arrange(RIGHT, buff=0.12,
                                                                                            aligned_edge=DOWN)
            if g.width > 12.4:
                g.scale_to_fit_width(12.4)
            return g.move_to(panel.get_center() + DOWN * 0.2)

        cur = sample_text(snaps[0][1])
        e0 = ev[0, 1]
        pb = float(m["passage_bits"])
        i_mid = next((i for i, (s, _) in enumerate(snaps) if s >= S // 6), 2)
        mid_bits = float(np.interp(snaps[i_mid][0], ev[:, 0], ev[:, 1]))
        if pb < kn and pb < n9:
            end = (f"By the end, {pb:.2f} bits per character on the passage: below Part 9's neural model, and below "
                   f"Kneser-Ney's {kn:.2f}.")
        elif pb < n9:
            end = (f"By the end, {pb:.2f} bits per character on the passage: below Part 9's neural model, but not "
                   f"yet Kneser-Ney's {kn:.2f}.")
        else:
            end = (f"By the end, {pb:.2f} bits per character on the passage, against Part 9's {n9:.2f} and "
                   f"Kneser-Ney's {kn:.2f}.")
        words = " ".join(snaps[i_mid][1].split()).split(" ")
        wordy = 0.1 < (len(words) - 1) / max(len(snaps[i_mid][1]), 1) < 0.3 and np.mean([len(w) for w in words]) < 9
        if wordy:
            mid_s = (f"Within {snaps[i_mid][0]:,} steps it writes words and spaces, at {mid_bits:.2f} bits per "
                     "character.")
        else:
            mid_s = (f"After {snaps[i_mid][0]:,} steps it is at {mid_bits:.2f} bits per character, though what it "
                     "writes doesn't look like words yet.")
        with self.voiceover(
            "Here is its training, scored as always on the scoreboard's passage from The Maltese Falcon, which it "
            f"never sees. <bookmark mark='a'/> It starts at {e0:.1f} bits per character, a guess among "
            f"{m['K']} symbols, writing noise. <bookmark mark='b'/> {mid_s} <bookmark mark='c'/> {end}"
        ) as vo:
            self.play(Create(ax), Create(l9), FadeIn(t9), Create(lk), FadeIn(tk), FadeIn(panel), FadeIn(pl),
                      FadeIn(cur))
            self.add(live, clock)
            vo.wait_until("a")
            for i in range(1, len(snaps)):
                if i == 1:
                    vo.wait_until("b")
                if i == len(snaps) - 1:
                    vo.wait_until("c")
                s_ = int(snaps[i][0])
                self.play(t.animate.set_value(s_), run_time=0.6 + 1.4 * (s_ - int(snaps[i - 1][0])) / S)
                nxt = sample_text(snaps[i][1])
                self.play(FadeOut(cur), FadeIn(nxt), run_time=0.5)
                cur = nxt
        for mob in (live, clock):
            mob.clear_updaters()
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def board(self):
        rows, i, n9, kn9 = board_rows()
        board = scoreboard(rows, highlight=(i,), max_bits=8.0)
        board.scale_to_fit_height(min(board.height, 6.6)).move_to(DOWN * 0.1)
        glow = SurroundingRectangle(board.rows[i], color=LM_C, buff=0.0, stroke_width=2.5)
        me = rows[i]["bits"]
        above = [r for r in rows[:i] if "bits" in r]
        best_above = min(r["bits"] for r in above)
        big = [j for j, r in enumerate(rows) if j > i and r.get("kind") == "lm" and "bits" in r]
        lm_best = min((rows[j]["bits"] for j in big), default=None)
        if me < best_above:
            v = (f"{me:.2f} bits per character, better than every row above it, by {best_above - me:.2f} bits. "
                 "The memory pays.")
        else:
            v = (f"{me:.2f} bits per character, {me - best_above:.2f} behind the best row above it: with the "
                 "training we could afford here, the LSTM hasn't caught up.")
        if lm_best is not None and lm_best < me:
            tail = (f" The pretrained language models below it are still far ahead, down to {lm_best:.2f} bits: "
                    "more text, more computing, and a different architecture, which is the next act's story."
                    if me - lm_best > 0.5 else
                    f" The pretrained language models below it are still ahead, down to {lm_best:.2f} bits, with "
                    "far more text and computing, and a different architecture: the next act's story.")
        else:
            tail = " The large models of Part 1, still to be filled in on this board, show how far there is to go."
        with self.voiceover(
            "On the scoreboard, a new row. <bookmark mark='a'/> Our character LSTM: " + v + " <bookmark mark='b'/>"
            + tail
        ) as vo:
            self.play(FadeIn(board))
            vo.wait_until("a")
            self.play(Create(glow))
            vo.wait_until("b")
            if big:
                self.play(Indicate(VGroup(*[board.rows[j] for j in big]), color=C.NEURAL))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def colored_text(self, text, values, lo, hi, width_chars=60, font_size=20, cmap=("#0B0F17", LM_C)):
        lines, cur, vals, cv = [], "", [], []
        for ch, v in zip(text, values):
            if ch == "\n":
                ch = " "
            cur += ch
            cv.append(v)
            if len(cur) >= width_chars and ch == " ":
                lines.append(cur)
                vals.append(cv)
                cur, cv = "", []
        if cur:
            lines.append(cur)
            vals.append(cv)
        rows = VGroup()
        cw = Text("M", font=MONO, font_size=font_size).width * 1.0
        a, b = rgb(cmap[0]), rgb(cmap[1])
        for li, (ln, vs) in enumerate(list(zip(lines, vals))[:6]):
            row = VGroup()
            for k, (ch, v) in enumerate(zip(ln, vs)):
                t = float(np.clip((v - lo) / max(hi - lo, 1e-9), 0, 1))
                bg = Rectangle(width=cw * 1.02, height=cw * 1.75, stroke_width=0,
                               fill_color=ManimColor(a * (1 - t) + b * t), fill_opacity=1)
                bg.move_to([k * cw, 0, 0])
                row.add(bg)
                if ch != " ":
                    row.add(data_text(ch, font=MONO, font_size=font_size, color=WHITE).move_to(bg))
            row.shift(DOWN * li * cw * 2.0)
            rows.add(row)
        return rows

    def quotes(self):
        m = load("charlstm")
        txt = m["quote_text"]
        tr = np.asarray(m["quote_trace"])
        if m["quote_corr"] < 0:
            tr = -tr
        lo, hi = float(np.quantile(tr, 0.05)), float(np.quantile(tr, 0.95))
        block = self.colored_text(txt, tr, lo, hi, cmap=("#0B0F17", CELLC))
        block.move_to(DOWN * 0.4)
        if block.width > 13.2:
            block.width = 13.2
        head = label(rf"one cell's value, \ character by character: \ cell ${m['quote_cell']}$ of "
                     rf"${m['hidden']}$", font_size=26, color=CELLC).to_edge(UP, buff=0.5)
        sub = label(rf"correlation with ``inside a quotation'' over the passage: \ ${abs(m['quote_corr']):.2f}$ \ "
                    rf"(the next best cell: \ ${m['quote_corr_next']:.2f}$)", font_size=22, color=GREY_A)
        sub.next_to(head, DOWN, buff=0.15)
        cite_ = cite(r"Karpathy, Johnson \& Fei-Fei (2015); \ Radford, J\'ozefowicz \& Sutskever (2017)", corner=DR)
        strong = abs(m["quote_corr"]) > 0.5
        v = (f"One of its {m['hidden']} cells does something nobody asked for: it switches on at an opening "
             "quotation mark and off at the closing one. Over the whole passage its value follows "
             f"\"inside a quotation\" with a correlation of {abs(m['quote_corr']):.2f}." if strong else
             f"The cell that best follows \"inside a quotation\" does so only loosely: a correlation of "
             f"{abs(m['quote_corr']):.2f}. Our small model hasn't dedicated a cell to it.")
        with self.voiceover(
            "What has it learned to remember? Look at single cells, as Karpathy, Justin Johnson and Fei-Fei Li did "
            "in 2015. <bookmark mark='a'/> " + v + " <bookmark mark='b'/> To close the quotation it must "
            "remember that one is open, maybe for lines. In 2017 Alec Radford and colleagues at OpenAI trained "
            "a bigger one on Amazon reviews and found a single cell that tracked whether a review was positive."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_), LaggedStart(*[FadeIn(r) for r in block], lag_ratio=0.2),
                      run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(sub))
        self.wait(0.3)
        self.clear_scene()

    def surprise(self):
        m = load("charlstm")
        from videos.ai.ai1 import compute as c1

        ps = c1.text("passage")
        sp = np.asarray(m["surprise"])  # bits for each character after the first
        n = 300
        block = self.colored_text(ps[1:1 + n], sp[:n], 0.0, 8.0, cmap=("#0B0F17", C.SURPRISE))
        block.move_to(DOWN * 0.3)
        if block.width > 13.2:
            block.width = 13.2
        head = label(r"the surprise of each character, \ in bits: \ the passage's opening", font_size=26,
                     color=C.SURPRISE).to_edge(UP, buff=0.5)
        scale = VGroup(label(r"0 bits", font_size=20, color=GREY_B),
                       Rectangle(width=2.6, height=0.22, stroke_width=0).set_fill(
                           color=[ManimColor("#0B0F17"), ManimColor(C.SURPRISE)], opacity=1),
                       label(r"8 bits", font_size=20, color=GREY_B)).arrange(RIGHT, buff=0.15)
        scale.to_edge(DOWN, buff=0.5)
        ws, wi, cap = m["word_start_bits"], m["word_inside_bits"], m["capital_bits"]
        with self.voiceover(
            "And where is it surprised? Colour each character of the passage's opening by the bits it cost. "
            f"<bookmark mark='a'/> Over the whole passage, the first letter of a word costs {ws:.1f} bits on "
            f"average; a letter inside a word, {wi:.1f}; a capital letter, {cap:.1f}. Once a word has begun, the "
            "rest of it is nearly free. That is Part 1's guessing game, played by a machine that remembers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(scale), LaggedStart(*[FadeIn(r) for r in block], lag_ratio=0.2),
                      run_time=2.0)
        self.wait(0.6)
        self.clear_scene()


def load_nlm():
    from videos.ai.ai7 import compute as c7
    from videos.ai.ai9 import compute as c9

    return float(c9.load("lm")["passage_bits"]), float(c7.load("kn")["best_bits"])


_ = GATEC
