from __future__ import annotations

from videos.psychology.psych23.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.readability()
        self.fields()

    def card(self):
        card = chapter_card(13, r"In practice: \ speech, \ reading, \ aphasia", r"Where does the psychology of "
                            r"language do work?", lit={1948: r"Flesch", 2000: r"National Reading Panel",
                                                       2017: r"Breitenstein et al."},
                            part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter thirteen. In practice: speech, reading and aphasia."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def readability(self):
        d = load("readability")
        head = heading(r"Readability formulas")
        eq = MathTex(r"\text{ease} = 206.835 - 1.015\,\frac{\text{words}}{\text{sentences}} - 84.6\,"
                     r"\frac{\text{syllables}}{\text{words}}", font_size=34, color=WORD).move_to([0, 2.2, 0])
        A = axes([0, 4], [0, 100], x_length=5.2, y_length=2.8, xticks=[], yticks=[0, 50, 100],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"Flesch reading ease", center=[-3.4, -0.3, 0], font_size=16)
        vals = [(r"Natural Stories 1", d["story1"], STAT), (r"Natural Stories 5", d["story5"], STAT),
                (r"\emph{The Maltese Falcon}, \ ch.\ 2", d["falcon"], WORD)]
        bs = VGroup(*[bars(A.ax, [k + 1], [v], c, 0.6) for k, (_, v, c) in enumerate(vals)])
        names = VGroup(*[label(t, font_size=15, color=GREY_A).next_to(A.ax.c2p(k + 1, 0), DOWN, buff=0.12 + 0.22 * (k % 2))
                         for k, (t, _, _) in enumerate(vals)])
        nums = VGroup(*[label(f"{v:.0f}", font_size=17).next_to(A.ax.c2p(k + 1, v), UP, buff=0.05)
                        for k, (_, v, _) in enumerate(vals)])
        rows = rows_of([
            (r"Flesch, \ 1948: \ longer sentences and longer words make text harder; \ still built into word "
             r"processors and required by some laws on plain language", WHITE),
            (r"the Natural Stories were written to be full of rare constructions, \ and they score as easy as "
             r"Hammett", STAT),
            (r"the formula sees only lengths: \ not structure, \ not surprisal, \ not what the reader knows", LOST),
            (r"better: \ measure the reader \ (Part 52), \ or use a language model's surprisal", MODEL),
        ], 5.6, 22, 0.33).move_to([3.6, -0.4, 0])
        ptag = psyche_tag(r"\texttt{language.flesch} \ (a rough syllable count)")
        with self.voiceover(
            "The most widely used piece of reading research is a formula. <bookmark mark='a'/> In 1948 Rudolf Flesch "
            "proposed that longer sentences and longer words make text harder to read, and weighted the two. "
            "Versions are still built into word processors, and some laws on plain language require them. "
            "<bookmark mark='b'/> Here it is on two of the Natural Stories and a chapter of The Maltese Falcon. The "
            "stories were written to be full of rare and difficult constructions, and they score just as easy as "
            "Hammett. <bookmark mark='c'/> The formula sees only lengths: not structure, not surprisal, not what the "
            "reader already knows. <bookmark mark='d'/> Better to measure readers directly, which is Part 52, or use "
            "the surprisal of a language model, which at least sees the words."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag), Write(eq))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(A), *[GrowFromEdge(b, DOWN) for b in bs], FadeIn(names), FadeIn(nums), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def fields(self):
        head = heading(r"Where the work is")
        cols = VGroup()
        items = [
            (r"reading", WORD, [r"the National Reading Panel, \ 2000: \ systematic phonics instruction helps "
                                r"children learn to read, \ especially early",
                                r"the reading wars are Part 54's"]),
            (r"aphasia", RULE, [r"Breitenstein and colleagues, \ 2017: \ in chronic aphasia after stroke, \ three "
                                r"weeks of intensive therapy improved everyday communication against waiting",
                                r"intensity, \ not only kind, \ matters"]),
            (r"speech recognition", SOUND, [r"systems learnt from thousands of hours of speech now match "
                                            r"professional transcribers on some benchmarks",
                                            r"accents, \ noise and children's voices are still harder"]),
        ]
        for k, (t, c, lines) in enumerate(items):
            body = VGroup(label(t, font_size=32, color=c),
                          rows_of([(lines[0], WHITE), (lines[1], GREY_A)], 3.6, 24, 0.4)).arrange(DOWN, buff=0.4,
                                                                                                aligned_edge=LEFT)
            box = RoundedRectangle(corner_radius=0.15, width=4.1, height=3.7, stroke_color=c, stroke_width=2,
                                   fill_color=c, fill_opacity=0.06).move_to([-4.35 + 4.35 * k, 0.6, 0])
            body.move_to(box.get_top() + DOWN * 0.3, aligned_edge=UP).align_to(box, LEFT).shift(RIGHT * 0.25)
            cols.add(VGroup(box, body))
        rows = rows_of([
            (r"and second languages: \ spacing and testing from Part 21, \ and a great deal of input", MODEL)],
            12.6, 26, 0.3).to_edge(DOWN, buff=0.65)
        tag = published_tag(r"National Reading Panel (2000); \ Breitenstein et al. (2017), \ \emph{Lancet}")
        with self.voiceover(
            "Three more places where this work is used. <bookmark mark='a'/> Teaching reading. In 2000 the National "
            "Reading Panel in the United States reviewed the experiments and found that systematic phonics, "
            "teaching how letters map to sounds, helps children learn to read, especially early on. The long "
            "argument over how to teach reading is Part 54's. <bookmark mark='b'/> Aphasia. In 2017 Caterina "
            "Breitenstein and colleagues ran a large trial in people with long-standing aphasia after a stroke. "
            "Three weeks of intensive therapy improved everyday communication compared with waiting. Intensity "
            "matters, not only the kind of therapy. <bookmark mark='c'/> And speech recognition. Systems trained "
            "on thousands of hours of speech now match professional transcribers on some benchmarks, though "
            "accents, noise and children's voices are still harder. <bookmark mark='d'/> For second languages, the "
            "best advice is Part 21's spacing and testing, and a great deal of input."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, c in zip("abc", cols):
                vo.wait_until(m)
                self.play(FadeIn(c, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]))
        self.clear_scene()
