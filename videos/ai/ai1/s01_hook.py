from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import MONO, letter, letter_row, load, wrap_words


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


class Hook(VoiceoverScene):
    def construct(self):
        self.shannon()
        self.modern()
        self.everywhere()
        self.question()
        self.board()

    # ------------------------------------------------------------------
    def shannon(self):
        g = load("game")
        sent = g["sentence"]
        ranks = g["sentence_ranks"]
        assert len(ranks) == len(sent) == 101
        rows, counts, lines = sentence_block(sent, ranks)
        letters = [m for t in rows for m in t]
        who = label(r"Claude Shannon, \ Bell Labs, \ 1951", font_size=30, color=GREY_A).to_corner(UL, buff=0.45)
        src = cite(r"C.~E.~Shannon, \textit{Prediction and Entropy of Printed English}, Bell System Technical Journal (1951)")
        tag = note(r"the guesser here: a simple counting program (Chapter 8), playing Shannon's game; \ computed",
                   font_size=20).next_to(rows, DOWN, buff=0.75)
        guesses = g["sentence_guesses"]
        assert [len(x) for x in guesses] == [int(r) for r in ranks] and guesses[3] == " yr"
        slots = VGroup(*[Rectangle(width=m.width + 0.06, height=0.04, stroke_width=0, fill_color=GREY_D,
                                   fill_opacity=1).next_to(m, DOWN, buff=0.04) for m in letters])
        n_slow = 12  # "there is no ": guessed one try at a time; the rest of the sentence fills in quickly
        with self.voiceover(
            "In 1951, Claude Shannon played a game with English. He took a sentence, hid it, and asked a person "
            "to guess it, one letter at a time. <bookmark mark='a'/> A wrong guess, and they guessed again, until "
            "they got it. Under each letter, he wrote down how many guesses it took."
        ) as vo:
            self.play(FadeIn(who), FadeIn(src), FadeIn(slots[:n_slow]))
            vo.wait_until("a")
            for k in range(n_slow):
                for wrong in guesses[k][:-1]:
                    t = letter(wrong, font_size=28, color=C.SURPRISE).move_to(letters[k])
                    self.play(FadeIn(t, scale=1.2), run_time=0.15)
                    self.play(FadeOut(t, shift=DOWN * 0.15), run_time=0.15)
                self.play(FadeIn(letters[k], scale=1.2), FadeIn(counts[k]), run_time=0.2)
            self.play(FadeIn(slots[n_slow:]), LaggedStart(*[AnimationGroup(FadeIn(m), FadeIn(c))
                                                          for m, c in zip(letters[n_slow:], counts[n_slow:])],
                                                        lag_ratio=0.12), run_time=max(3.0, vo.remaining() - 0.5))
            self.play(FadeOut(slots), run_time=0.4)
        self.add(tag)
        ones = [c for c in counts if c.rank == 1]
        many = [c for c in counts if c.rank >= 5]
        frac1 = len(ones) / len(counts)
        assert 0.5 < frac1 < 0.7, frac1
        # "motorcycle": after m, o, t, o, r, c, y, the rest comes for free
        i0 = sent.index("motorcycle")
        assert all(int(r) == 1 for r in ranks[i0 + 7:i0 + 10]) and int(ranks[i0 + 6]) > 1
        moto = VGroup(*[letters[i] for i in range(i0, i0 + 10)])
        moto_box = SurroundingRectangle(moto, color=C.GUESS, buff=0.08, corner_radius=0.06)
        with self.voiceover(
            "Most letters fall on the first guess. <bookmark mark='a'/> Once you've seen m, o, t, o, r, c, y, "
            "the rest of motorcycle is free. <bookmark mark='b'/> The guesses pile up at a few places, mostly where "
            "a new word begins. That is where the information is."
        ) as vo:
            self.play(FadeIn(tag))
            self.play(*[c.animate.set_opacity(0.35) for c in ones], run_time=0.8)
            vo.wait_until("a")
            self.play(Create(moto_box))
            vo.wait_until("b")
            self.play(FadeOut(moto_box), *[Indicate(c, color=C.SURPRISE, scale_factor=1.8) for c in many],
                      run_time=1.5)
        est = label(r"Shannon's estimate: \ about $1$ bit per letter \quad ($0.6$ to $1.3$)", font_size=32,
                    color=C.BITS).to_edge(DOWN, buff=1.05)
        vs = label(r"versus $\log_2 27 = 4.75$ bits for a letter guessed blindly", font_size=26, color=GREY_A)
        vs.next_to(est, DOWN, buff=0.18)
        with self.voiceover(
            "From counts like these, Shannon estimated how much information English really carries: about one "
            "bit per letter, somewhere between 0.6 and 1.3, <bookmark mark='a'/> when a single letter, guessed "
            "blindly, could carry 4.75. Most of what we write is predictable."
        ) as vo:
            self.play(FadeOut(tag), FadeIn(est))
            vo.wait_until("a")
            self.play(FadeIn(vs))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def modern(self):
        pr = load("probes")
        prompt = "The Eiffel Tower is located in the city of"
        a = next(r for r in pr["GPT-2 small"] if r["prompt"] == prompt)
        b = next(r for r in pr["Qwen3-4B"] if r["prompt"] == prompt)
        assert a["tokens"][0] == b["tokens"][0] == " Paris"
        assert abs(a["probs"][0] - 0.064) < 0.001 and abs(b["probs"][0] - 0.346) < 0.001
        ptext = Text(prompt, font=MONO, font_size=30, color=C.TOKEN).to_edge(UP, buff=0.8)
        blank = Rectangle(width=1.4, height=0.5, stroke_color=C.MODEL_Q, stroke_width=2.5).next_to(ptext, RIGHT, buff=0.2)
        q = Text("?", font=MONO, font_size=30, color=C.MODEL_Q).move_to(blank)

        def panel(res, name, year, x):
            head = label(rf"{name} \ ({year})", font_size=28, color=C.NEURAL).move_to([x, 1.8, 0])
            bars = VGroup()
            for k in range(5):
                tok = res["tokens"][k].replace(" ", "␣").replace("_", " _")
                p = res["probs"][k]
                t = Text(tok, font=MONO, font_size=22, color=WHITE if k == 0 else GREY_A)
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
        with self.voiceover(
            "Seventy-five years later, this guessing game is exactly what large language models are trained to "
            "play. Give one the start of a sentence, <bookmark mark='a'/> and it returns a probability for every "
            "possible next word. <bookmark mark='b'/> GPT-2, from 2019, gives Paris six percent. <bookmark mark='c'/> "
            "Qwen3, a 2025 model, gives it thirty-five."
        ) as vo:
            self.play(FadeIn(ptext), Create(blank), FadeIn(q))
            vo.wait_until("a")
            self.play(FadeIn(cap), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(left[0]), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in left[1]], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(FadeIn(right[0]), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in right[1]], lag_ratio=0.15))
        self.play(Indicate(left[1][0], color=C.PROB), Indicate(right[1][0], color=C.PROB), run_time=1.5)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def everywhere(self):
        r = np.random.default_rng(3)
        W, H = 3.0, 2.3
        centers = [np.array([-5.1, 0.2, 0]), np.array([-1.7, 0.2, 0]), np.array([1.7, 0.2, 0]),
                   np.array([5.1, 0.2, 0])]
        frames = VGroup(*[RoundedRectangle(width=W, height=H, corner_radius=0.12, stroke_color=GREY_C,
                                           stroke_width=1.5).move_to(c) for c in centers])
        # text: the next token
        t1 = Text("the cat sat", font=MONO, font_size=20, color=C.TOKEN).move_to(centers[0] + UP * 0.6)
        t2 = Text("on the", font=MONO, font_size=20, color=C.TOKEN).next_to(t1, DOWN, buff=0.15).align_to(t1, LEFT)
        box = Rectangle(width=0.8, height=0.32, stroke_color=C.MODEL_Q, stroke_width=2).next_to(t2, RIGHT, buff=0.12)
        bars1 = VGroup(*[Rectangle(width=0.22, height=h, stroke_width=0, fill_color=C.PROB, fill_opacity=0.85)
                         for h in (0.8, 0.45, 0.25, 0.15, 0.1)]).arrange(RIGHT, buff=0.08, aligned_edge=DOWN)
        bars1.move_to(centers[0] + DOWN * 0.55)
        text_p = VGroup(t1, t2, box, bars1)
        # images: the noise (a noisy patch and the clean one)
        n = 8
        clean = np.fromfunction(lambda i, j: np.exp(-((i - 3.5) ** 2 + (j - 3.5) ** 2) / 9.0), (n, n))
        noisy = np.clip(clean + r.normal(0, 0.35, (n, n)), 0, 1)

        def pix(a, c):
            g = VGroup()
            for i in range(n):
                for j in range(n):
                    g.add(Square(0.13, stroke_width=0, fill_opacity=1,
                                 fill_color=interpolate_color(ManimColor("#1A2230"), ManimColor(C.TRUE_P), float(a[i, j])))
                          .move_to(c + np.array([(j - 3.5) * 0.13, (3.5 - i) * 0.13, 0])))
            return g

        img_p = VGroup(pix(noisy, centers[1] + LEFT * 0.7), pix(clean, centers[1] + RIGHT * 0.7),
                       Arrow(centers[1] + LEFT * 0.1, centers[1] + RIGHT * 0.1, buff=0, color=C.MODEL_Q,
                             stroke_width=3, max_tip_length_to_length_ratio=0.5))
        # sound: the next stretch of waveform
        xs = np.linspace(-1.3, 0.5, 120)
        ys = 0.45 * np.sin(9 * xs) * np.cos(2.3 * xs) + 0.08 * np.sin(31 * xs)
        wave = VMobject(color=C.TRUE_P, stroke_width=2.5).set_points_smoothly(
            [centers[2] + np.array([x, y, 0]) for x, y in zip(xs, ys)])
        xs2 = np.linspace(0.5, 1.3, 50)
        ys2 = 0.45 * np.sin(9 * xs2) * np.cos(2.3 * xs2) + 0.08 * np.sin(31 * xs2)
        wave2 = DashedVMobject(VMobject(color=C.MODEL_Q, stroke_width=2.5).set_points_smoothly(
            [centers[2] + np.array([x, y, 0]) for x, y in zip(xs2, ys2)]), num_dashes=12)
        snd_p = VGroup(wave, wave2)
        # robots: the next action
        path_pts = [centers[3] + np.array([-1.1 + 0.25 * k, -0.6 + 0.9 * np.sin(0.35 * k) ** 2, 0]) for k in range(7)]
        dots = VGroup(*[Dot(p_, radius=0.06, color=C.TRUE_P) for p_ in path_pts])
        trail = VMobject(color=C.TRUE_P, stroke_width=2).set_points_as_corners(path_pts)
        nxt = Dot(path_pts[-1] + np.array([0.3, 0.25, 0]), radius=0.08, color=C.MODEL_Q)
        arm = VGroup(Line(centers[3] + np.array([-1.2, -0.95, 0]), path_pts[3], color=GREY_B, stroke_width=4),
                     Line(path_pts[3], path_pts[-1], color=GREY_B, stroke_width=4))
        act_p = VGroup(arm, trail, dots, DashedLine(path_pts[-1], nxt.get_center(), color=C.MODEL_Q), nxt)
        caps = VGroup(*[label(t, font_size=22, color=GREY_A).next_to(f, DOWN, buff=0.2) for t, f in zip(
            [r"text: the next token", r"images: the noise", r"sound: the next sound token",
             r"robots: the next action"], frames)])
        head = label(r"the same game, everywhere", font_size=40).to_edge(UP, buff=0.6)
        tag = schematic_tag()
        with self.voiceover(
            "And it's not just text. <bookmark mark='a'/> Models that make images learn to guess the noise that "
            "was added to a picture. <bookmark mark='b'/> Speech models guess the next slice of sound. "
            "<bookmark mark='c'/> Robot controllers guess the next movement of an arm. Under the hood, nearly every "
            "frontier model plays some version of Shannon's game."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Create(frames[0]), FadeIn(text_p), FadeIn(caps[0]))
            vo.wait_until("a")
            self.play(Create(frames[1]), FadeIn(img_p), FadeIn(caps[1]))
            vo.wait_until("b")
            self.play(Create(frames[2]), Create(wave), FadeIn(wave2), FadeIn(caps[2]))
            vo.wait_until("c")
            self.play(Create(frames[3]), FadeIn(act_p), FadeIn(caps[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def question(self):
        q = label(r"What do you have to know \\ to guess well?", font_size=56)
        with self.voiceover(
            "Which raises the question this whole series is about. What do you have to know, to guess well?"
        ) as vo:
            self.play(Write(q), run_time=2.0)
        m = series_map(current=1).shift(DOWN * 0.2)
        title = label(SERIES_ZH if zh() else SERIES_EN, font_size=44).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Over twenty parts, we'll build the answer from the ground up. <bookmark mark='a'/> First, the "
            "foundations: probability and information, vectors, calculus, and randomness. <bookmark mark='b'/> "
            "Then learning, from classical statistics to neural networks and the mathematics of scale. "
            "<bookmark mark='c'/> Then the engines of today's models: attention, memory, sparsity, diffusion, and "
            "the many kinds of tokens. <bookmark mark='d'/> And finally, reasoning, agents, inference, and what we "
            "can see when we look inside."
        ) as vo:
            self.play(q.animate.scale(0.5).to_edge(UP, buff=0.3).set_opacity(0), FadeIn(title))
            self.remove(q)
            for k, mark in enumerate(["a", "b", "c", "d"]):
                vo.wait_until(mark)
                col = m.cols[k]
                self.play(FadeIn(col.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in col.rows],
                                                        lag_ratio=0.15), run_time=1.4)
            self.play(Create(m.box))
        with self.voiceover(
            "Part one starts where Shannon did: with surprise, entropy, codes and compression. By the end, we'll "
            "see why guessing well and compressing well are the same thing."
        ) as vo:
            self.play(Indicate(m.part[1], color=C.BITS, scale_factor=1.15), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def board(self):
        sb = load("scoreboard")
        corpus = load("corpus")
        rows = sb["rows"]
        head = label(r"The scoreboard", font_size=40).to_edge(UP, buff=0.3)
        para = corpus["passage_head"].split("\n")[0]
        assert para.startswith("A TELEPHONE-BELL rang in darkness.")
        quote = wrapped_label(r"``" + para[:178].rsplit(" ", 1)[0] + r"\ldots''", 12.4, font_size=26,
                              color=GREY_A).next_to(head, DOWN, buff=0.3)
        src = note(rf"Dashiell Hammett, \textit{{The Maltese Falcon}} (1930), chapter 2: \ ${sb['chars']:,}$ "
                   r"characters. \ Public domain, and on Project Gutenberg, since 1 January 2026".replace(",", "{,}"),
                   font_size=20).next_to(quote, DOWN, buff=0.2)
        board = scoreboard(rows, shown=1, row_h=0.36, font_size=20).scale(0.92).to_edge(DOWN, buff=0.25)
        assert rows[0]["bits"] == 8.0
        with self.voiceover(
            "And we'll keep score. Here is a page of a novel, The Maltese Falcon, from 1930. It entered the public "
            "domain, and Project Gutenberg, on the first of January 2026, after every model in this part was "
            "trained, so none of them can have learned it by heart. <bookmark mark='a'/> Stored as plain text, it "
            "takes eight bits per character. <bookmark mark='b'/> Our job, for the whole series, is to explain how "
            "the numbers on this board come down: from eight, to below one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(quote), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(board))
            vo.wait_until("b")
            self.play(*[r.name.animate.set_color(GREY_B) for r in board.rows[1:]], run_time=1.0)
        self.wait(0.5)
        self.clear_scene()
