from __future__ import annotations

from explainer import *  # noqa: F403
from videos.llm.common import (
    PROMPT, Mono, TokenBox, data, display_token, label, piece_text, show_chapter_card, token_row,
)


class Tokens(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 1, "Text into tokens")
        self.d = data()
        self.split_sentence()
        self.second_sentence()
        self.granularity()
        self.bpe()
        self.wrap_up()

    # ------------------------------------------------------------------
    def split_sentence(self):
        sent = PROMPT + " Paris."
        tk = self.d["tokenize"][sent]
        pieces, ids = tk["pieces"], tk["ids"]
        assert pieces[1:4] == [" E", "iff", "el"]
        text = piece_text(pieces, font_size=30).move_to(UP * 2.2)
        row = token_row(pieces, show_space=True, font_size=30, buff=0.1).move_to(UP * 0.6)
        if row.width > 13.4:
            row.scale_to_fit_width(13.4)

        with self.voiceover(
            "Step one. A language model can't read letters. <bookmark mark='s'/> Text first gets chopped into pieces, "
            "called tokens."
        ) as vo:
            self.play(FadeIn(text))
            vo.wait_until("s")
            self.play(*[TransformFromCopy(text.pieces[i], row[i].text) for i in range(len(pieces))],
                      *[FadeIn(row[i].box) for i in range(len(pieces))], run_time=1.8)

        spaces = VGroup(*[r.text.glyphs[0] for r, p in zip(row, pieces) if p.startswith(" ")])
        eiffel = VGroup(*row[1:4])
        eb = Brace(eiffel, DOWN, buff=0.12, color=YELLOW)
        el = label(r"a rarer word: three tokens", font_size=32, color=YELLOW).next_to(eb, DOWN, buff=0.1)
        with self.voiceover(
            "Common words, like <bookmark mark='the'/> the, or <bookmark mark='city'/> city, get a single token each. "
            "And notice that <bookmark mark='sp'/> the space in front of a word is usually part of its token. "
            "A rarer word, like Eiffel, <bookmark mark='e'/> gets broken into smaller pieces: E, iff, el."
        ) as vo:
            vo.wait_until("the")
            self.play(Indicate(row[8], color=YELLOW))
            vo.wait_until("city")
            self.play(Indicate(row[9], color=YELLOW))
            vo.wait_until("sp")
            self.play(spaces.animate.set_color(YELLOW), run_time=0.6)
            self.play(spaces.animate.set_color(GREY_D), run_time=0.6)
            vo.wait_until("e")
            self.play(eiffel.animate.set_color(YELLOW), GrowFromCenter(eb), FadeIn(el))

        id_row = VGroup(*[MathTex(str(i), font_size=30, color=GREY_A).next_to(r, DOWN, buff=0.22) for i, r in zip(ids, row)])
        for m in id_row[1::2]:
            m.shift(DOWN * 0.38)
        vs = self.d["vocab_samples"]
        entries = [("0", vs["0"]), ("1", vs["1"]), ("2", vs["2"]), None, ("464", vs["464"]), None,
                   ("6342", vs["6342"]), None, ("50255", vs["50255"]), ("50256", vs["50256"])]
        table = VGroup()
        for e in entries:
            if e is None:
                table.add(MathTex(r"\vdots", font_size=30, color=GREY_B))
                continue
            i, s = e
            num = MathTex(i, font_size=30, color=GREY_A)
            tok = Mono(display_token(s, show_space=True), font_size=28)
            table.add(VGroup(num, tok).arrange(RIGHT, buff=0.3))
        table.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        for m in table:
            if isinstance(m, MathTex):
                m.shift(RIGHT * 0.25)
        table.scale_to_fit_height(3.3).to_corner(DR, buff=0.35)
        tbox = SurroundingRectangle(table, color=GREY_B, buff=0.2, corner_radius=0.08, stroke_width=1.5)
        ttitle = label(r"vocabulary:\\50{,}257 tokens", font_size=34, color=GREY_A).next_to(tbox, LEFT, buff=0.4)
        ttitle.align_to(tbox, UP)
        assert self.d["vocab_size"] == 50257
        with self.voiceover(
            "Each token is really just a number: <bookmark mark='n'/> its position in a fixed list, called the vocabulary. "
            "<bookmark mark='v'/> GPT-2's vocabulary has 50,257 entries. From here on, the model never sees letters again; "
            "only these numbers."
        ) as vo:
            self.play(FadeOut(VGroup(eb, el)), eiffel.animate.set_color(C.TOKEN))
            vo.wait_until("n")
            self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.15) for m in id_row], lag_ratio=0.06), run_time=1.5)
            vo.wait_until("v")
            self.play(FadeIn(tbox), FadeIn(table, lag_ratio=0.1), FadeIn(ttitle), FadeOut(text), run_time=1.5)
        self.ids_row = VGroup(row, id_row)
        self.clear_scene()

    # ------------------------------------------------------------------
    def second_sentence(self):
        sent = "Tokenization splits unbelievable words like ChatGPT into pieces."
        pieces = self.d["tokenize"][sent]["pieces"]
        assert " unbelievable" in pieces and pieces[6:9] == [" Chat", "G", "PT"]
        row = token_row(pieces, show_space=True, font_size=30, buff=0.1)
        if row.width > 13.4:
            row.scale_to_fit_width(13.4)
        row.move_to(UP * 0.4)
        u = pieces.index(" unbelievable")
        ub = Brace(row[u], DOWN, buff=0.12, color=GREEN)
        ul = label(r"long, but common:\\one token", font_size=32, color=GREEN).next_to(ub, DOWN, buff=0.1)
        cb = Brace(VGroup(*row[6:9]), DOWN, buff=0.12, color=YELLOW)
        cl = label(r"newer than the vocabulary:\\three tokens", font_size=32, color=YELLOW).next_to(cb, DOWN, buff=0.1)
        with self.voiceover(
            "Another example. <bookmark mark='u'/> A long but common word, like unbelievable, gets a token of its own. "
            "But ChatGPT didn't exist when this vocabulary was built, in 2019, <bookmark mark='c'/> so it gets split "
            "into three pieces."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in row], lag_ratio=0.05), run_time=1.5)
            vo.wait_until("u")
            self.play(row[u].animate.set_color(GREEN), GrowFromCenter(ub), FadeIn(ul))
            vo.wait_until("c")
            self.play(VGroup(*row[6:9]).animate.set_color(YELLOW), GrowFromCenter(cb), FadeIn(cl))
        self.clear_scene()

    # ------------------------------------------------------------------
    def granularity(self):
        g = self.d["granularity"]
        rows = VGroup(
            token_row(g["chars"], show_space=True, font_size=28, buff=0.06),
            token_row(g["words"], show_space=True, font_size=28, buff=0.06),
            token_row(g["subwords"], show_space=True, font_size=28, buff=0.06),
        ).arrange(DOWN, buff=1.0, aligned_edge=LEFT).shift(RIGHT * 0.6 + UP * 0.3)
        names = VGroup(*[label(t, font_size=36) for t in [r"characters", r"whole words", r"subwords"]])
        notes = VGroup(*[label(t, font_size=30, color=GREY_B) for t in [
            r"tiny vocabulary, but long sequences",
            r"short sequences, but every word, name and typo needs an entry",
            r"the compromise",
        ]])
        for n, r, t in zip(names, rows, notes):
            n.next_to(r, LEFT, buff=0.5).align_to(names, RIGHT)
            t.next_to(r, DOWN, buff=0.15).align_to(r, LEFT)
        names.arrange(DOWN, buff=1.0)
        for n, r in zip(names, rows):
            n.next_to(r, LEFT, buff=0.5)
            n.set_y(r.get_y())
        VGroup(names, rows, notes).move_to(ORIGIN)
        names.align_to(names[0], RIGHT)
        sub_box = SurroundingRectangle(VGroup(names[2], rows[2], notes[2]), color=GREEN, buff=0.2, corner_radius=0.1)

        with self.voiceover(
            "Why chop text up this way? You could use <bookmark mark='c'/> single characters. Then the vocabulary is tiny, "
            "but every sentence becomes a long sequence, and the model has to work harder just to see the words. "
            "<bookmark mark='w'/> Or you could use whole words. Sequences are short, but the vocabulary needs every word, "
            "name and typo ever written, and anything new is a dead end. <bookmark mark='s'/> Subword tokens are the "
            "compromise."
        ) as vo:
            vo.wait_until("c")
            self.play(FadeIn(names[0]), LaggedStart(*[FadeIn(t) for t in rows[0]], lag_ratio=0.04), run_time=1.2)
            self.play(FadeIn(notes[0]))
            vo.wait_until("w")
            self.play(FadeIn(names[1]), FadeIn(rows[1], lag_ratio=0.2), run_time=1.0)
            self.play(FadeIn(notes[1]))
            vo.wait_until("s")
            self.play(FadeIn(names[2]), FadeIn(rows[2], lag_ratio=0.15), FadeIn(notes[2]), run_time=1.0)
            self.play(Create(sub_box))
        self.clear_scene()

    # ------------------------------------------------------------------
    def bpe(self):
        steps = self.d["bpe"]
        words = list(steps[0]["segments"].keys())
        counts = {"low": 7, "lower": 4, "lowest": 3, "slow": 5, "slower": 2, "tower": 6, "towers": 3}
        assert steps[0]["merge"] == ["o", "w"] and steps[0]["pairs"][0][2] == 30
        title = label(r"Byte-pair encoding, on a tiny made-up corpus", font_size=36).to_edge(UP, buff=0.4)
        y0, dy = 2.0, 0.66
        x_count, x_row = -6.2, -4.9

        def make_row(segs, y):
            r = VGroup(*[TokenBox(s, font_size=28, pad=0.09, min_width=0.42) for s in segs]).arrange(RIGHT, buff=0.07)
            return r.move_to([x_row, y, 0], aligned_edge=LEFT)

        count_labels = VGroup(*[MathTex(rf"{counts[w]}\times", font_size=30, color=GREY_B).move_to([x_count, y0 - k * dy, 0])
                                for k, w in enumerate(words)])
        rows = [make_row(steps[0]["segments"][w], y0 - k * dy) for k, w in enumerate(words)]
        vocab_title = label(r"vocabulary", font_size=30, color=GREY_A).move_to([3.0, 2.1, 0])
        base_chars = sorted({c for w in words for c in w})
        vocab = VGroup(*[TokenBox(c, font_size=26, pad=0.08, min_width=0.4) for c in base_chars])
        vocab.arrange_in_grid(cols=7, buff=0.08).next_to(vocab_title, DOWN, buff=0.25)
        new_vocab = VGroup()
        pair_lab = VGroup()

        with self.voiceover(
            "The vocabulary itself is built by an algorithm called byte-pair encoding. Here it is on a tiny, made-up "
            "collection of words, <bookmark mark='c'/> each with a count of how often it appears. "
            "<bookmark mark='s'/> Start with single characters as the vocabulary."
        ) as vo:
            self.play(FadeIn(title))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.1), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(count_labels, lag_ratio=0.1))
            vo.wait_until("s")
            self.play(FadeIn(vocab_title), FadeIn(vocab, lag_ratio=0.1))

        def merge_step(k, narrate=None, fast=False):
            nonlocal rows, pair_lab
            a, b = steps[k]["merge"]
            n = steps[k]["pairs"][0][2]
            hits = []
            for wi, w in enumerate(words):
                segs = steps[k]["segments"][w]
                i = 0
                while i < len(segs) - 1:
                    if segs[i] == a and segs[i + 1] == b:
                        hits.append((wi, i))
                        i += 2
                    else:
                        i += 1
            new_pair = VGroup(
                label(r"most frequent pair:", font_size=28, color=GREY_A),
                TokenBox(a, font_size=26, pad=0.08), TokenBox(b, font_size=26, pad=0.08),
                MathTex(rf"({n}\times)", font_size=30, color=GREY_A),
            ).arrange(RIGHT, buff=0.15).move_to([3.0, -1.3, 0])
            new_pair[1:3].set_color(YELLOW)
            run = 0.5 if fast else 1.0
            self.play(FadeOut(pair_lab), FadeIn(new_pair), run_time=run * 0.6)
            pair_lab = new_pair
            boxes = VGroup(*[VGroup(rows[wi][i], rows[wi][i + 1]) for wi, i in hits])
            self.play(boxes.animate.set_color(YELLOW), run_time=run * 0.6)
            new_rows = [make_row(steps[k + 1]["segments"][w], y0 - wi * dy) for wi, w in enumerate(words)]
            anims = []
            for wi in range(len(words)):
                old, new = rows[wi], new_rows[wi]
                merged = {i for wj, i in hits if wj == wi}
                j, i = 0, 0
                while i < len(old):
                    if i in merged:
                        new[j].set_color(YELLOW)
                        anims.append(ReplacementTransform(VGroup(old[i], old[i + 1]), new[j]))
                        i += 2
                    else:
                        anims.append(ReplacementTransform(old[i], new[j]))
                        i += 1
                    j += 1
            entry = TokenBox(a + b, font_size=26, pad=0.08, color=YELLOW)
            if len(new_vocab):
                entry.next_to(new_vocab[-1], RIGHT, buff=0.1)
                if entry.get_right()[0] > 6.8:
                    entry.next_to(new_vocab[0], DOWN, buff=0.1, aligned_edge=LEFT)
            else:
                entry.next_to(vocab, DOWN, buff=0.35, aligned_edge=LEFT)
            new_vocab.add(entry)
            self.play(*anims, FadeIn(entry, shift=DOWN * 0.2), run_time=run)
            self.play(*[m.animate.set_color(C.TOKEN) for r in new_rows for m in r], entry.animate.set_color(C.TOKEN),
                      run_time=run * 0.5)
            rows = new_rows

        with self.voiceover(
            "Now count how often each pair of neighboring symbols appears, weighted by how common each word is. "
            "<bookmark mark='w'/> The winner is o followed by w, 30 times. <bookmark mark='m'/> Merge that pair into a new "
            "symbol, everywhere it occurs, and add it to the vocabulary."
        ) as vo:
            vo.wait_until("w")
            merge_step(0)

        with self.voiceover(
            "Then repeat. <bookmark mark='a'/> Now l and o w appear together 21 times, so they merge into low. "
            "<bookmark mark='b'/> Next, e and r become e r. <bookmark mark='c'/> Then tow, tower, <bookmark mark='d'/> "
            "and slow."
        ) as vo:
            vo.wait_until("a")
            merge_step(1)
            vo.wait_until("b")
            merge_step(2, fast=True)
            vo.wait_until("c")
            merge_step(3, fast=True)
            merge_step(4, fast=True)
            vo.wait_until("d")
            merge_step(5, fast=True)

        total = MathTex(r"256", r"+", r"50{,}000", r"+", r"1", r"=", r"50{,}257", font_size=40)
        notes = VGroup(*[label(t, font_size=28, color=GREY_B) for t in [r"bytes", r"merges", r"end of text"]])
        total.to_edge(DOWN, buff=0.75)
        for n, i in zip(notes, (0, 2, 4)):
            n.next_to(total[i], DOWN, buff=0.15)
        total[6].set_color(YELLOW)
        with self.voiceover(
            "Frequent chunks, like low, tower, and the ending e r, become single tokens, while rarer words get spelled "
            "out of smaller pieces. <bookmark mark='g'/> GPT-2's tokenizer starts from the 256 possible bytes and runs "
            "50,000 merges like this over a large body of text. Add one special token that marks the end of a document, "
            "<bookmark mark='t'/> and you get its 50,257 tokens."
        ) as vo:
            self.play(FadeOut(pair_lab))
            vo.wait_until("g")
            self.play(Write(total[:3]), FadeIn(notes[:2]))
            vo.wait_until("t")
            self.play(Write(total[3:]), FadeIn(notes[2]))
        self.clear_scene()

    # ------------------------------------------------------------------
    def wrap_up(self):
        row, id_row = self.ids_row
        grp = VGroup(row, id_row).move_to(UP * 0.5)
        paris = id_row[11]
        q = label(r"6342 = Paris\ldots\ but what \emph{is} Paris?", font_size=34, color=GREY_A).to_edge(DOWN, buff=1.2)
        with self.voiceover(
            "So our sentence has become a list of integers. But the number 6342 tells the model nothing about what Paris "
            "is. <bookmark mark='n'/> The next step is to give every token a much richer description."
        ) as vo:
            self.play(FadeIn(grp))
            self.play(Indicate(paris, color=YELLOW), Indicate(row[11], color=YELLOW))
            vo.wait_until("n")
            self.play(FadeIn(q, shift=UP * 0.2))
        self.clear_scene()


