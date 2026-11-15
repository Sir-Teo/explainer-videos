from __future__ import annotations

from videos.psychology.psych23.common import *  # noqa: F403


class Critical(VoiceoverScene):
    def construct(self):
        self.card()
        self.cases()
        self.age()

    def card(self):
        card = chapter_card(9, r"A critical period?", r"Is there an age after which a language cannot be fully "
                            r"learned?", lit={1977: r"Curtiss", 1989: r"Johnson \& Newport",
                                              2018: r"Hartshorne et al."},
                            part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter nine. A critical period?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def cases(self):
        head = heading(r"First languages, \ learnt late")
        cols = VGroup()
        items = [
            (r"Genie", LOST, [r"found in 1970, \ aged 13, \ after a childhood of extreme isolation and abuse",
                              r"she learnt many words, \ but never the grammar of a native speaker \ (Curtiss, \ "
                              r"1977)",
                              r"one child, \ and a deprived one: \ the language cannot be separated from the rest"]),
            (r"late first signers", SOUND, [r"deaf children of hearing parents sometimes meet a sign language only "
                                            r"at school or later",
                                            r"Mayberry and colleagues, \ 2002: \ deaf adults with no language "
                                            r"early learnt English less well than those who signed from infancy",
                                            r"early exposure to \emph{some} language seems to matter most"]),
        ]
        for k, (t, c, lines) in enumerate(items):
            body = VGroup(label(t, font_size=32, color=c),
                          rows_of([(lines[0], WHITE), (lines[1], c), (lines[2], GREY_A)], 5.5, 25, 0.4)
                          ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
            box = RoundedRectangle(corner_radius=0.15, width=6.2, height=4.2, stroke_color=c, stroke_width=2,
                                   fill_color=c, fill_opacity=0.06).move_to([-3.35 + 6.7 * k, 0.4, 0])
            body.move_to(box.get_top() + DOWN * 0.3, aligned_edge=UP).align_to(box, LEFT).shift(RIGHT * 0.3)
            cols.add(VGroup(box, body))
        tag = published_tag(r"Curtiss (1977); \ Mayberry, \ Lock \& Kazmi (2002)")
        with self.voiceover(
            "Is there an age after which a language can't be fully learned? The evidence comes in uneasy kinds. "
            "<bookmark mark='a'/> Genie was found in 1970, aged thirteen, after a childhood of extreme isolation and "
            "abuse. She learned many words, but never the grammar of a native speaker. But she is one child, and a "
            "badly deprived one, so the language can't be separated from everything else that happened to her. "
            "<bookmark mark='b'/> A cleaner case: deaf children of hearing parents sometimes meet a sign language "
            "only at school or later. Rachel Mayberry and colleagues found that deaf adults who had met no language "
            "early learned English less well than deaf adults who had signed from infancy, or than people who had "
            "heard another language early. Early exposure to some language, "
            "any language, seems to matter most."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, c in zip("ab", cols):
                vo.wait_until(m)
                self.play(FadeIn(c, shift=UP * 0.15))
        self.clear_scene()

    def age(self):
        head = heading(r"Second languages: \ the age of starting")
        A = axes([0, 40], [0, 1], x_length=5.6, y_length=3.4, xticks=[0, 10, 17.4, 30, 40], yticks=[],
                 xfmt=lambda v: f"{v:g}", xlabel=r"age, \ years", ylabel=r"grammar", center=[-3.2, 0.5, 0],
                 font_size=16)
        x = np.linspace(0, 40, 200)
        y = np.where(x < 17.4, 0.95, 0.95 - 0.03 * (x - 17.4))  # the ability to learn, by current age
        c = curve(A.ax, x, np.clip(y, 0.05, 1), WORD, 3)
        # eventual grammar by the age of starting falls earlier: a late starter has less time before the decline
        y2 = np.where(x < 10, 0.9, 0.9 - 0.022 * (x - 10))
        c2 = DashedVMobject(curve(A.ax, x, np.clip(y2, 0.05, 1), STAT, 2.5), num_dashes=40)
        key = legend([(WORD, r"ability to learn, \ by age"), (STAT, r"eventual grammar, \ by age of starting")],
                     font_size=18).next_to(A, DOWN, buff=0.3)
        mark = DashedLine(A.ax.c2p(17.4, 0), A.ax.c2p(17.4, 1), color=LOST)
        sl = label(r"schematic of the shapes reported, \ not data", font_size=18, color=GREY_B).next_to(key, DOWN,
                                                                                                      buff=0.15)
        rows = rows_of([
            (r"Johnson \& Newport, \ 1989: \ 46 Chinese and Korean speakers who moved to the United States at ages 3 "
             r"to 39: \ the later they arrived, \ the lower their scores on English grammar", WHITE),
            (r"but age of arrival travels with schooling, \ motivation, \ years of use and identity", GREY_A),
            (r"Hartshorne, \ Tenenbaum \& Pinker, \ 2018: \ 669{,}498 people took an online grammar quiz; \ a model "
             r"separating age, \ age of starting and years of experience", MODEL),
            (r"the ability to learn grammar stays near its peak until about 17.4 years, \ then declines: \ a "
             r"critical period, \ later than thought, \ with its cause unknown", WORD),
        ], 5.6, 22, 0.33).move_to([3.6, 0.0, 0])
        tag = published_tag(r"Johnson \& Newport (1989); \ Hartshorne, \ Tenenbaum \& Pinker (2018)")
        with self.voiceover(
            "For second languages, the question is about the age of starting. <bookmark mark='a'/> In 1989 Jacqueline "
            "Johnson and Elissa Newport tested forty-six native speakers of Chinese and Korean who had moved to the "
            "United States between the ages of three and thirty-nine. The later they had arrived, the lower their "
            "scores on English grammar. <bookmark mark='b'/> But age of arrival travels with schooling, motivation, "
            "years of use and identity, so a correlation can't settle it. <bookmark mark='c'/> In 2018 Joshua "
            "Hartshorne, Joshua Tenenbaum and Steven Pinker had six hundred and seventy thousand people take an "
            "online grammar quiz, and fitted a model that separates current age, age of starting and years of "
            "experience. <bookmark mark='d'/> They estimated that the ability to learn grammar stays near its peak "
            "until about seventeen and a half, then declines: a critical period, but much later than people had "
            "thought, and its cause, biological or social, is unknown. A late starter has less time to learn before "
            "the decline, so the grammar people end up with falls off from a much earlier age of starting. The "
            "curves drawn here are schematics of those shapes, not their data."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(sl))
            vo.wait_until("a")
            self.play(Create(c2), FadeIn(key[1]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(c), FadeIn(key[0]), Create(mark), FadeIn(rows[3]))
        self.clear_scene()
