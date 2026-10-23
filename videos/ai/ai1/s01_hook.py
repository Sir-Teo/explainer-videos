from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import MONO, PART, letter, letter_row, load, wrap_words

ERA0, ERA1, EX0, EX1 = 1830, 2030, -6.5, 6.5


def era_x(y: float) -> float:
    return EX0 + (EX1 - EX0) * (y - ERA0) / (ERA1 - ERA0)


def sentence_block(sentence: str, ranks, width_chars=36, font_size=28, max_width=12.4):
    """The sentence in monospace lines, each letter with its guess count underneath."""
    lines = wrap_words(sentence, width_chars)
    rows, counts, k = VGroup(), VGroup(), 0
    for ln in lines:
        t = letter_row(ln, font_size=font_size)
        rows.add(t)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.75)
    if rows.width > max_width:
        rows.scale(max_width / rows.width)
    rows.move_to(UP * 0.3)
    for t, ln in zip(rows, lines):
        y = t.get_bottom()[1] - 0.2  # one baseline for the counts of a line, below the descenders
        for i, ch in enumerate(ln):
            r = int(ranks[k])
            col = GREY_C if r == 1 else interpolate_color(ManimColor(C.GUESS), ManimColor(C.SURPRISE), min(1, (r - 2) / 10))
            n = Text(str(r), font=MONO, font_size=15, color=col)
            n.move_to([t[i].get_x(), y - n.height / 2, 0])
            n.rank = r
            counts.add(n)
            k += 1
    return rows, counts, lines


def token_kind(toks: list[str], i: int) -> str:
    """word, piece of a word, or punctuation mark: how a token sits in the text."""
    t = toks[i]
    if not t.strip().isalnum():
        return "mark"
    nxt = toks[i + 1] if i + 1 < len(toks) else " "
    starts = t.startswith(" ") or i == 0 or not toks[i - 1].strip()[-1:].isalnum()
    ends = nxt.startswith(" ") or not nxt.strip()[:1].isalnum()
    return "word" if starts and ends else "piece"


class Hook(VoiceoverScene):
    def construct(self):
        self.shannon()
        self.era()
        self.modern()
        self.question()
        self.plan()
        self.board()

    # ------------------------------------------------------------------
    def shannon(self):
        g = load("game")
        sent = g["sentence"]
        ranks = [int(r) for r in g["sentence_ranks"]]
        assert len(ranks) == len(sent)
        rows, counts, lines = sentence_block(sent, ranks)
        letters = [m for t in rows for m in t]
        who = label(r"Claude Shannon, \ Bell Labs, \ 1951", font_size=30, color=GREY_A).to_corner(UL, buff=0.45)
        src = cite(r"C.~E.~Shannon, \textit{Prediction and Entropy of Printed English}, Bell System Technical Journal (1951)")
        tag = note(r"the guesser here: a simple counting program (Chapter 9), playing Shannon's game; \ computed",
                   font_size=20).next_to(rows, DOWN, buff=0.75)
        guesses = g["sentence_guesses"]
        assert [len(x) for x in guesses] == ranks  # the guesses up to the right one, for every letter
        slots = VGroup(*[Rectangle(width=m.width + 0.06, height=0.04, stroke_width=0, fill_color=GREY_D,
                                   fill_opacity=1).next_to(m, DOWN, buff=0.04) for m in letters])
        n_slow = 12  # "there is no ": guessed one try at a time; the rest of the sentence fills in quickly
        with self.voiceover(
            "In 1951, Claude Shannon played a game with English. He took a sentence, hid it, and asked a person "
            "to guess it, one letter at a time. <bookmark mark='a'/> A wrong guess, and they guessed again, until "
            "they got it. Under each letter, he wrote down how many guesses it took."
        ) as vo:
            cursor = SurroundingRectangle(slots[0], color=C.GUESS, buff=0.12, corner_radius=0.04)
            ask = label(r"guess the next letter", font_size=26, color=C.GUESS).next_to(rows, DOWN, buff=0.75)
            self.play(FadeIn(who), FadeIn(src), LaggedStart(*[FadeIn(sl_) for sl_ in slots], lag_ratio=0.01),
                      run_time=1.5)
            self.play(Create(cursor), FadeIn(ask))
            self.play(Indicate(cursor, color=C.GUESS, scale_factor=1.3), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeOut(cursor), FadeOut(ask), run_time=0.4)
            for k in range(n_slow):
                for wrong in guesses[k][:-1]:
                    t = letter(wrong, font_size=28, color=C.SURPRISE).move_to(letters[k])
                    self.play(FadeIn(t, scale=1.2), run_time=0.15)
                    self.play(FadeOut(t, shift=DOWN * 0.15), run_time=0.15)
                self.play(FadeIn(letters[k], scale=1.2), FadeIn(counts[k]), run_time=0.2)
            self.play(LaggedStart(*[AnimationGroup(FadeIn(m), FadeIn(c))
                                                          for m, c in zip(letters[n_slow:], counts[n_slow:])],
                                                        lag_ratio=0.12), run_time=max(3.0, vo.remaining() - 0.5))
            self.play(FadeOut(slots), run_time=0.4)
        self.add(tag)
        ones = [c for c in counts if c.rank == 1]
        many = [c for c in counts if c.rank >= 5]
        frac1 = len(ones) / len(counts)
        most = ("Most letters fall on the first guess." if frac1 > 0.5 else
                f"{100 * frac1:.0f} percent of the letters fall on the first guess.")
        # "motorcycle": after its first few letters, how much of it comes free (first guesses to the end)?
        i0 = sent.index("motorcycle")
        j = 10
        while j > 0 and ranks[i0 + j - 1] == 1:
            j -= 1
        seen = ", ".join(sent[i0:i0 + j])
        moto_said = (f"Once you've seen {seen}, the rest of motorcycle is free."
                     if 0 < j < 10 else "Even inside a word like motorcycle, the letters take guesses.")
        moto = VGroup(*[letters[i] for i in range(i0, i0 + 10)])
        moto_box = SurroundingRectangle(moto, color=C.GUESS, buff=0.08, corner_radius=0.06)
        with self.voiceover(
            f"{most} <bookmark mark='a'/> {moto_said} <bookmark mark='b'/> The guesses pile up at a few places, "
            "mostly where a new word begins. That is where the information is."
        ) as vo:
            self.play(FadeIn(tag))
            self.play(*[c.animate.set_opacity(0.35) for c in ones], run_time=0.8)
            vo.wait_until("a")
            self.play(Create(moto_box))
            vo.wait_until("b")
            self.play(FadeOut(moto_box), *[Indicate(c, color=C.SURPRISE, scale_factor=1.8) for c in many],
                      run_time=1.5)
        lo_h, hi_h = (float(x) for x in g["shannon_human"])
        blind = math.log2(27)
        est = label(rf"Shannon's estimate: \ about $1$ bit per letter \quad (${lo_h:.1f}$ to ${hi_h:.1f}$)",
                    font_size=32, color=C.BITS).to_edge(DOWN, buff=1.05)
        vs = label(rf"versus $\log_2 27 = {blind:.2f}$ bits for a letter guessed blindly", font_size=26, color=GREY_A)
        vs.next_to(est, DOWN, buff=0.18)
        with self.voiceover(
            "From counts like these, Shannon estimated that English carries about one bit per letter, a bit being "
            f"the answer to one yes-or-no question: between {lo_h:.1f} and {hi_h:.1f}, <bookmark mark='a'/> when a "
            f"letter guessed blindly could carry {blind:.2f}. Most of what we write is predictable."
        ) as vo:
            self.play(FadeOut(tag), FadeIn(est))
            vo.wait_until("a")
            self.play(FadeIn(vs))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def era(self):
        """How we got here: from telegraph codes to the guessing machines of today, on one strip."""
        y0 = -0.35
        axis = Line([EX0, y0, 0], [EX1, y0, 0], color=GREY_C, stroke_width=3)
        ticks = VGroup()
        for yr in range(1850, 2030, 25):
            ticks.add(Line([era_x(yr), y0 - 0.07, 0], [era_x(yr), y0 + 0.07, 0], color=GREY_C, stroke_width=2))
            ticks.add(Text(str(yr), font_size=20, color=GREY_B).next_to([era_x(yr), y0, 0], DOWN, buff=0.14))
        events = [  # year, text, above?, level
            (1844, r"Morse code: \\ \texttt{e} $=$ one dot", True, 1),
            (1928, r"Hartley: information \\ $=$ a logarithm", False, 1),
            (1948, r"Shannon: \\ entropy, the bit", True, 1),
            (1951, r"the guessing \\ game", False, 2),
            (1952, r"Huffman's \\ code", True, 2),
            (1976, r"arithmetic \\ coding", False, 1),
            (2003, r"a neural \\ language model", True, 1),
            (2019, r"GPT-2", False, 2),
            (2025, r"Qwen3", True, 2),
        ]
        marks = []
        for yr, txt, up, lev in events:
            x = era_x(yr)
            h = 0.75 if lev == 1 else 1.85
            stem = Line([x, y0, 0], [x, y0 + (h if up else -h), 0], color=C.HUMAN, stroke_width=2.5)
            dot = Dot([x, y0, 0], radius=0.08, color=C.HUMAN)
            words_ = VGroup(label(rf"{yr}", font_size=26, color=C.HUMAN), label(txt, font_size=22, color=WHITE))
            words_.arrange(DOWN, buff=0.04).next_to(stem.get_end(), UP if up else DOWN, buff=0.06)
            if yr == 1948:  # Huffman's stem (1952) rises just to its right
                words_.align_to([x + 0.12, 0, 0], RIGHT)
            elif yr == 1952:
                words_.align_to([x - 0.12, 0, 0], LEFT)
            keep_in_frame(words_, margin=0.15)
            marks.append(VGroup(stem, dot, words_))
        head = label(r"How we got here", font_size=42).to_edge(UP, buff=0.3)
        this = Rectangle(width=era_x(1977) - era_x(1838), height=0.32, stroke_width=0, fill_color=C.BITS,
                         fill_opacity=0.18).move_to([(era_x(1977) + era_x(1838)) / 2, y0, 0])
        that = Rectangle(width=era_x(2028) - era_x(1998), height=0.32, stroke_width=0, fill_color=C.NEURAL,
                         fill_opacity=0.18).move_to([(era_x(2028) + era_x(1998)) / 2, y0, 0])
        tl = label(r"this part", font_size=22, color=C.BITS).next_to(this, DOWN, buff=0.45).set_x(era_x(1880))
        tr = label(r"the rest of the series", font_size=22, color=C.NEURAL).next_to(that, DOWN, buff=0.45)
        tr.align_to([era_x(2016), 0, 0], RIGHT)  # clear of GPT-2's stem
        keep_in_frame(tr, margin=0.15)
        with self.voiceover(
            "Shannon didn't start from nothing. <bookmark mark='a'/> Telegraphers knew that common letters deserve "
            "short codes: Morse gives e a single dot. <bookmark mark='b'/> In 1928 Ralph Hartley, at Bell Labs, "
            "measured information by the logarithm of the number of possible messages. <bookmark mark='c'/> In "
            "1948 Shannon made it a theory: entropy, the bit, and the limits of compression. <bookmark mark='d'/> "
            "The guessing game, Huffman's code and arithmetic coding followed. <bookmark mark='e'/> Half a century "
            "later, the same game became how machines learn language: a network guessing the next word, in 2003, "
            "then GPT-2, and today's models."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(ticks), FadeIn(this), FadeIn(tl), FadeIn(that), FadeIn(tr))
            vo.wait_until("a")
            self.play(FadeIn(marks[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(marks[1], shift=DOWN * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(marks[2], shift=UP * 0.2))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(m) for m in marks[3:6]], lag_ratio=0.4))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(m) for m in marks[6:]], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def modern(self):
        pr = load("probes")
        prompt = "The Eiffel Tower is located in the city of"
        a = next(r for r in pr["GPT-2 small"] if r["prompt"] == prompt)
        b = next(r for r in pr["Qwen3-4B"] if r["prompt"] == prompt)
        pa, pb = dict(zip(a["tokens"], a["probs"])).get(" Paris"), dict(zip(b["tokens"], b["probs"])).get(" Paris")
        ptext = data_text(prompt, font=MONO, font_size=30, color=C.TOKEN).to_edge(UP, buff=0.8)
        blank = Rectangle(width=1.4, height=0.5, stroke_color=C.MODEL_Q, stroke_width=2.5).next_to(ptext, RIGHT, buff=0.2)
        q = Text("?", font=MONO, font_size=30, color=C.MODEL_Q).move_to(blank)

        def panel(res, name, year, x):
            head = label(rf"{name} \ ({year})", font_size=28, color=C.NEURAL).move_to([x, 1.8, 0])
            bars = VGroup()
            for k in range(5):
                tok = res["tokens"][k].replace(" ", "␣")
                p = res["probs"][k]
                t = data_text(tok, font=MONO, font_size=22, color=WHITE if k == 0 else GREY_A)
                t.move_to([x - 1.4, 1.0 - 0.6 * k, 0], aligned_edge=RIGHT)
                r = Rectangle(width=max(0.02, 6.0 * p), height=0.34, stroke_width=0, fill_color=C.PROB,
                              fill_opacity=0.9 if k == 0 else 0.55)
                r.move_to([x - 1.2, t.get_y(), 0], aligned_edge=LEFT)
                v = MathTex(f"{p:.3f}", font_size=24, color=GREY_A).next_to(r, RIGHT, buff=0.12)
                bars.add(VGroup(t, r, v))
            return VGroup(head, bars)

        left = panel(a, r"GPT-2 small, $124$M parameters", 2019, -3.4)
        right = panel(b, r"Qwen3-4B, $4$B parameters", 2025, 3.6)
        cap = label(r"the probability each model gives to every possible next token (top five shown)", font_size=24,
                    color=GREY_B).to_edge(DOWN, buff=0.5)
        tag = note(r"computed").to_corner(DR, buff=0.3)

        def says(p):
            return f"gives the word Paris {100 * p:.0f} percent" if p is not None else "doesn't put Paris in its top five"

        with self.voiceover(
            "Seventy-five years on, Shannon's game is exactly what large language models are trained to play. "
            "Give one the start of a sentence, <bookmark mark='a'/> and it returns a probability for every "
            "possible next word. <bookmark mark='b'/> GPT-2, from 2019, with a hundred and twenty-four million "
            f"parameters, the adjustable numbers inside it, {says(pa)}. <bookmark mark='c'/> Qwen3, a 2025 model "
            f"with four billion, {says(pb)}."
        ) as vo:
            self.play(FadeIn(ptext), Create(blank), FadeIn(q))
            vo.wait_until("a")
            self.play(FadeIn(cap), FadeIn(tag), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in left[1]],
                                                           lag_ratio=0.15))
            vo.wait_until("b")
            self.play(FadeIn(left[0]), Indicate(left[1], color=C.PROB, scale_factor=1.03))
            vo.wait_until("c")
            self.play(FadeIn(right[0]), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in right[1]], lag_ratio=0.15))
        self.play(Indicate(left[1][0], color=C.PROB), Indicate(right[1][0], color=C.PROB), run_time=1.5)
        # what a token is: a line of the Falcon passage, cut the way GPT-2 cuts it
        all_toks = load("lms")["surprise"]["GPT-2 small"]["tokens"]
        start = next((i for i in range(len(all_toks) - 1) if all_toks[i] == " Sp" and all_toks[i + 1] == "ade"), 24) - 2
        start = max(0, min(start, len(all_toks) - 9))
        toks = all_toks[start:start + 9]
        kinds = [token_kind(all_toks, start + i) for i in range(len(toks))]
        tiles = VGroup()
        for k, (tk, kind) in enumerate(zip(toks, kinds)):
            t = data_text(tk.replace(" ", "␣"), font=MONO, font_size=26, color=WHITE)
            r = RoundedRectangle(width=t.width + 0.24, height=0.5, corner_radius=0.06, stroke_width=0,
                                 fill_color=[C.EMBED, C.MLP, C.KEY][k % 3], fill_opacity=0.5).move_to(t)
            kl = label({"word": r"word", "mark": r"mark", "piece": r"piece"}[kind], font_size=22, color=GREY_B)
            kl.next_to(r, DOWN, buff=0.12)
            tiles.add(VGroup(r, t, kl))
        tiles.arrange(RIGHT, buff=0.08, aligned_edge=UP)
        tok_card = gloss(r"token", r"the chunk of text a model guesses at one time:\\ a whole word, a piece of a word, "
                         r"or a punctuation mark", picture=tiles, width=8.4, color=C.NEURAL)
        tok_card.scale(1.35).move_to(DOWN * 0.6)
        with self.voiceover(
            "Strictly, a model guesses the next token. <bookmark mark='a'/> A token is the chunk of text it "
            "guesses at one time: a word, a piece of a word, or a punctuation mark. Here is a line of a 1930 "
            "novel, cut the way GPT-2 cuts it."
        ) as vo:
            self.play(FadeOut(left), FadeOut(right), FadeOut(cap), FadeOut(tag))
            vo.wait_until("a")
            self.play(FadeIn(tok_card, shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def question(self):
        q = label(r"What do you have to know \\ to guess well?", font_size=56).shift(UP * 0.5)
        ptext = data_text("The Eiffel Tower is located in the city of", font=MONO, font_size=26, color=GREY_B)
        box = Rectangle(width=1.2, height=0.45, stroke_color=C.MODEL_Q, stroke_width=2.5).next_to(ptext, RIGHT,
                                                                                               buff=0.15)
        echo = VGroup(ptext, box, Text("?", font=MONO, font_size=26, color=C.MODEL_Q).move_to(box))
        echo.next_to(q, DOWN, buff=0.9)
        with self.voiceover(
            "Which raises the question this whole series is about. What do you have to know, to guess well?"
        ):
            self.play(Write(q), FadeIn(echo, shift=UP * 0.1), run_time=2.0)
        m = series_map(current=PART).shift(DOWN * 0.2)
        title = label(SERIES_ZH if zh() else SERIES_EN, font_size=44).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Over thirty-one parts, we'll build the answer from the ground up: <bookmark mark='a'/> foundations, "
            "<bookmark mark='b'/> learning from data, <bookmark mark='c'/> transformers, <bookmark mark='d'/> "
            "generation and perception, <bookmark mark='e'/> agency and reasoning, <bookmark mark='f'/> and finally, "
            "looking inside, and whether we can trust it."
        ) as vo:
            self.play(q.animate.scale(0.5).to_edge(UP, buff=0.3).set_opacity(0), FadeOut(echo), FadeIn(title),
                      LaggedStart(*[FadeIn(col.head) for col in m.cols], lag_ratio=0.15), run_time=1.5)
            self.remove(q)
            for k, mark in enumerate("abcdef"):
                vo.wait_until(mark)
                col = m.cols[k]
                self.play(Indicate(col.head, color=WHITE, scale_factor=1.05),
                          LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in col.rows], lag_ratio=0.15), run_time=1.2)
            self.play(Create(m.box))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ The Guessing Game", font_size=44).to_edge(UP, buff=0.4)
        obj = objectives_card([
            r"probability, surprise and entropy: \ what information is, \ and why it is unique",
            r"codes: \ Kraft--McMillan, \ Huffman's optimal code, \ typical sequences and Shannon's source coding "
            r"theorem",
            r"cross-entropy and KL divergence: \ the price of a wrong model",
            r"arithmetic coding: \ prediction is compression",
            r"learning: \ counting, \ Laplace's rule, \ maximum likelihood, \ the softmax gradient",
            r"mutual information, \ and what it takes to guess well",
            r"bits per character, \ bits per token, \ and the scoreboard: \ from gzip to Qwen3",
        ], font_size=24).next_to(title, DOWN, buff=0.4)
        if obj.get_bottom()[1] < -3.75:
            obj.scale((obj.get_top()[1] + 3.75) / obj.height, about_edge=UP)
        with self.voiceover(
            "Part one starts where Shannon did. <bookmark mark='a'/> What information is, and why it's measured in "
            "bits; the best codes, and Shannon's limit; the price of a wrong model; a code that turns any guesser "
            "into a compressor; how a model learns to guess; and how far guessing has come. Guessing well and "
            "compressing well, we'll see, are the same thing."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(FadeIn(obj.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in obj.rows], lag_ratio=0.3),
                      run_time=max(2.5, vo.remaining() - 0.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def board(self):
        sb = load("scoreboard")
        corpus = load("corpus")
        rows = sb["rows"]
        head = label(r"The scoreboard", font_size=40).to_edge(UP, buff=0.3)
        para = corpus["passage_head"].split("\n")[0]
        quote = wrapped_label(r"``" + para[:178].rsplit(" ", 1)[0] + r"\ldots''", 12.4, font_size=26,
                              color=GREY_A).next_to(head, DOWN, buff=0.3)
        src = note(rf"Dashiell Hammett, \textit{{The Maltese Falcon}} (1930), chapter 2: \ ${sb['chars']:,}$ "
                   r"characters. \ Public domain, and on Project Gutenberg, since 1 January 2026".replace(",", "{,}"),
                   font_size=20).next_to(quote, DOWN, buff=0.2)
        board = scoreboard(rows, shown=1, row_h=0.36, font_size=20).scale(0.92).to_edge(DOWN, buff=0.25)
        low = min(r["bits"] for r in rows if "bits" in r)
        goal = "to below one" if low < 1 else f"to {low:.2f} bits per character, and beyond"
        with self.voiceover(
            "And we'll keep score. Here is a page of The Maltese Falcon, from 1930. It entered the public domain "
            "on the first of January 2026, after every model in this part was trained, so none can have learned "
            "it by heart. <bookmark mark='a'/> As plain text, it takes eight bits per character. "
            f"<bookmark mark='b'/> The series explains how the numbers on this board come down: from eight, {goal}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(quote), FadeIn(src), FadeIn(board))
            vo.wait_until("a")
            self.play(Indicate(board.rows[0], color=WHITE, scale_factor=1.04))
            vo.wait_until("b")
            self.play(*[r.name.animate.set_color(GREY_B) for r in board.rows[1:]], run_time=1.0)
        self.wait(0.5)
        self.clear_scene()
