from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai10.common import (CELLC, GATEC, LSTMC, MONO, PART, load, load_cached, read_cached_text, rgb)

LM_C = C.NEURAL


def board_rows():
    """The scoreboard so far: Part 1's rows (its cache; or, where Part 1's language-model rows haven't been computed,
    the rows its counting models and compressors give), Part 7's Kneser-Ney, Part 9's neural models, and ours."""
    try:
        rows = [dict(r) for r in load_cached("ai1", "scoreboard")["rows"]]
    except FileNotFoundError:
        raw = load_cached("ai1", "raw")
        rows = [
            dict(key="ascii", label="plain text file", bits=8 * raw["n_bytes"] / raw["n_chars"], part=1, kind="baseline"),
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
    k, n, me = load_cached("ai7", "kn"), load_cached("ai9", "lm"), load("charlstm")
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
        top = max(5.0, float(np.ceil(np.max(ev[:, 1]))))
        ax = axes([0, S], [1.5, top], x_length=6.6, y_length=3.4, xlabel=r"training steps",
                  ylabel=r"this run: passage bits per character", xticks=[0, S // 2, S],
                  yticks=list(range(2, int(top) + 1, 2)),
                  center=[-2.4, 0.9, 0])
        A = ax.ax
        references = VGroup(
            label(r"reference results", font_size=20, color=GREY_A),
            label(rf"Part 9 neural: \ ${n9:.2f}$; \ $21{{,}}382$ targets", font_size=19, color=GREY_B),
            label(rf"Part 7 Kneser--Ney: \ ${kn:.2f}$; \ $21{{,}}399$ targets", font_size=19, color=C.COUNTING),
            label(r"this LSTM: \ $21{,}405$ targets", font_size=19, color=LM_C),
            label(r"target spans and training differ", font_size=18, color=GREY_A),
        ).arrange(DOWN, buff=0.12).move_to([4.4, 0.0, 0])
        if references.width > 4.6:
            references.scale_to_fit_width(4.6)
        t = ValueTracker(0.0)

        def upto():
            n_ = int(np.searchsorted(ev[:, 0], t.get_value(), side="right"))
            pts = [A.c2p(x, y) for x, y in ev[:n_, :2]]
            if not pts:
                return VMobject(color=LM_C, stroke_width=4)
            if len(pts) == 1:
                pts.append(pts[0].copy())
            return VMobject(color=LM_C, stroke_width=4).set_points_as_corners(pts)

        live = always_redraw(upto)
        clock = always_redraw(lambda: VGroup(
            MathTex(rf"\text{{step }}{int(round(t.get_value())):,}".replace(",", "{,}"), font_size=28),
            MathTex(rf"{float(ev[max(0, int(np.searchsorted(ev[:, 0], t.get_value(), side="right")) - 1), 1]):.2f}\ \text{{bits/char (last logged)}}", font_size=24,
                    color=LM_C)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.8, 2.0, 0]))
        panel = RoundedRectangle(width=13.0, height=1.9, corner_radius=0.12, stroke_color=GREY_D, stroke_width=1.5,
                                 fill_color="#121722", fill_opacity=1).move_to([0, -2.6, 0])
        pl = label(r"what it writes now, \ from Part 9's prompt and the same random draws:", font_size=20,
                   color=GREY_A).next_to(panel.get_corner(UL), DR, buff=0.12)

        def sample_text(s):
            # Wrap the displayed excerpt without changing its generated characters.
            txt = " ".join(s.split())[:116]
            from textwrap import wrap
            generated = wrap(txt, width=58, break_long_words=True, break_on_hyphens=False,
                             replace_whitespace=False, drop_whitespace=False)
            rows = [data_text(m["prompt"].strip(), font="DejaVu Serif", font_size=19, color=GREY_B)]
            rows += [data_text(line, font="DejaVu Serif", font_size=19, color=WHITE) for line in generated]
            g = VGroup(*rows).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            if g.width > 12.4:
                g.scale_to_fit_width(12.4)
            return g.move_to(panel.get_center() + DOWN * 0.15)

        cur = sample_text(snaps[0][1])
        e0 = ev[0, 1]
        pb = float(m["passage_bits"])
        i_mid = next((i for i, (s, _) in enumerate(snaps) if s >= S // 6), 2)
        mid_bits = float(np.interp(snaps[i_mid][0], ev[:, 0], ev[:, 1]))
        end = (f"By the final step, this run records {pb:.2f} bits per character on its held-out target span. "
               "The reference results use different target spans and training settings.")
        words = " ".join(snaps[i_mid][1].split()).split(" ")
        wordy = 0.1 < (len(words) - 1) / max(len(snaps[i_mid][1]), 1) < 0.3 and np.mean([len(w) for w in words]) < 9
        if wordy:
            mid_s = (f"Within {snaps[i_mid][0]:,} steps it writes words and spaces, at {mid_bits:.2f} bits per "
                     "character.")
        else:
            mid_s = (f"After {snaps[i_mid][0]:,} steps it is at {mid_bits:.2f} bits per character, though what it "
                     "writes doesn't look like words yet.")
        with self.voiceover(
            "Here is its training, scored on the passage from The Maltese Falcon, which is not used for weight "
            f"updates. <bookmark mark='a'/> It starts at {e0:.1f} bits per character, a guess among "
            f"{m['K']} symbols, writing noise. <bookmark mark='b'/> {mid_s} <bookmark mark='c'/> {end}"
        ) as vo:
            self.play(Create(ax), FadeIn(references), FadeIn(panel), FadeIn(pl),
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
                self.play(FadeOut(cur), run_time=0.2)
                self.play(FadeIn(nxt), run_time=0.3)
                cur = nxt
        for mob in (live, clock):
            mob.clear_updaters()
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def board(self):
        rows, i, n9, kn9 = board_rows()
        board = scoreboard(rows, highlight=(i,), max_bits=8.0)
        board.scale_to_fit_height(min(board.height, 5.9)).move_to(DOWN * 0.45)
        protocol = label(r"historical reference scores: \ scoring protocols and training budgets differ",
                         font_size=23, color=GREY_A).to_edge(UP, buff=0.35)
        glow = SurroundingRectangle(board.rows[i], color=LM_C, buff=0.0, stroke_width=2.5)
        me = rows[i]["bits"]
        big = [j for j, r in enumerate(rows) if j > i and r.get("kind") == "lm" and "bits" in r]
        v = f"{me:.2f} bits per character under this run's evaluation."
        tail = (" The other rows retain their recorded reference values. Their target spans, contexts and "
                "training budgets differ; this board does not isolate the effect of recurrent memory.")
        with self.voiceover(
            "On the scoreboard, a new row. <bookmark mark='a'/> Our character LSTM: " + v + " <bookmark mark='b'/>"
            + tail
        ) as vo:
            self.play(FadeIn(board), FadeIn(protocol))
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
        ps = read_cached_text("ai1", "passage")
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
            f"average; a letter inside a word, {wi:.1f}; a capital letter, {cap:.1f}. The "
            "remaining letters cost less on average than its first letter in this run. That is Part 1's guessing "
            "game, played by a machine that remembers."
        ):
            self.play(FadeIn(head), FadeIn(scale), LaggedStart(*[FadeIn(r) for r in block], lag_ratio=0.2),
                      run_time=2.0)
        self.wait(0.6)
        self.clear_scene()


def load_nlm():
    return float(load_cached("ai9", "lm")["passage_bits"]), float(load_cached("ai7", "kn")["best_bits"])


_ = GATEC
