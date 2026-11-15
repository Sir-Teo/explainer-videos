from __future__ import annotations

from videos.psychology.psych22.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.rsa()
        self.language()
        self.machines()
        self.open_questions()

    def card(self):
        card = chapter_card(14, r"Frontier: \ concepts in minds and machines", r"Do machines have concepts like ours, "
                            r"and how would we tell?", lit={2008: r"Kriegeskorte et al.", 2015: r"Lake et al.",
                                                            2024: r"Marjieh et al."},
                            part=PART, scale=("mind", "world"), marr=("what", "how"))
        with self.voiceover("Chapter fourteen. Frontier: concepts in minds and machines."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def rsa(self):
        d = load("ekman")
        assert d["rsa_hue"] > d["rsa_wavelength"] > d["rsa_cones"], "the narration orders the three models"
        head = heading(r"Comparing spaces: \ representational similarity")
        eq = MathTex(r"\rho = \mathrm{Spearman}\big(\{D^{\text{people}}_{ij}\}_{i<j},\ "
                     r"\{D^{\text{model}}_{ij}\}_{i<j}\big)", font_size=36, color=MODEL).move_to([-3.0, 2.2, 0])
        vals = [(r"cone excitations", d["rsa_cones"], GREY_B), (r"wavelength", d["rsa_wavelength"], CAT_B),
                (r"hue angle, \ opponent channels", d["rsa_hue"], MODEL),
                (r"\dots with a fitted blue-yellow weight", float(np.max(d["rsa_hue_weights"])), PROTO)]
        A = axes([0, 1], [0, 4.6], x_length=4.6, y_length=3.4, xticks=[0, 0.5, 1.0], yticks=[],
                 xfmt=lambda v: f"{v:.1f}", xlabel=r"match to Ekman's people, \ $\rho$", center=[-2.0, -0.5, 0],
                 font_size=17)
        bs, names, nums = VGroup(), VGroup(), VGroup()
        for k, (t, v, c) in enumerate(vals):
            y = 3.9 - 1.05 * k
            lo, hi = A.ax.c2p(0, y), A.ax.c2p(v, y)
            bs.add(Rectangle(width=max(hi[0] - lo[0], 1e-3), height=0.42, stroke_width=0, fill_color=c,
                             fill_opacity=0.85).move_to([(lo[0] + hi[0]) / 2, lo[1], 0]))
            names.add(label(t, font_size=17, color=c).next_to(lo, LEFT, buff=0.15))
            nums.add(label(f"{v:.2f}", font_size=18).next_to(hi, RIGHT, buff=0.08))
        rows = rows_of([
            (r"turn any two systems into dissimilarity tables over the same items, \ and correlate them", WHITE),
            (r"Ekman's people against three models of the eye: \ the hue angle of Part 13's opponent channels "
             r"matches best", MODEL),
            (r"wavelength cannot close the circle; \ raw cone signals miss how hue is coded after the cones", CAT_B),
            (r"the same comparison is made between brains, \ people and networks: \ one currency for all three",
             PROTO),
        ], 5.0, 20, 0.3).move_to([4.2, -0.1, 0])
        ptag = psyche_tag(r"\texttt{concepts.rsa}, \ \texttt{hue\_angle\_distances}; \ Ekman via smacof")
        with self.voiceover(
            "How would we tell whether a machine, or a brain area, has concepts like ours? The frontier's main tool "
            "is simple. <bookmark mark='a'/> Turn each system into a table of dissimilarities over the same items, "
            "and correlate the tables. It's called representational similarity analysis. <bookmark mark='b'/> Here "
            "it is on Ekman's colours, against three models of the eye. The hue angle between lights, in the "
            f"opponent channels of Part 13, matches people best, rho {d['rsa_hue']:.2f}, and "
            f"{float(np.max(d['rsa_hue_weights'])):.2f} if we let one weight be fitted. <bookmark mark='c'/> "
            f"Wavelength gets {d['rsa_wavelength']:.2f}: it can't close the circle. Raw cone signals get "
            f"{d['rsa_cones']:.2f}: they miss how hue is coded after the cones. <bookmark mark='d'/> The same "
            "comparison is made between brain areas, people and artificial networks. It gives all three one currency."
        ) as vo:
            self.play(FadeIn(head), Write(eq), FadeIn(ptag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(A), *[GrowFromEdge(b, LEFT) for b in bs], FadeIn(names), FadeIn(nums), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def language(self):
        head = heading(r"What language knows about perception")
        doms = (("pitch", 0.92), ("colour", 0.89), ("loudness", 0.89), ("consonants", 0.57), ("taste", 0.54),
                ("timbre", 0.42))
        A = axes([0, 7], [0, 1], x_length=5.6, y_length=3.0, xticks=[], yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{v:.1f}", ylabel=r"correlation with people, \ $r$", center=[-3.0, -0.3, 0],
                 font_size=17)
        bs = VGroup(*[bars(A.ax, [k + 1], [v], MODEL if v > 0.8 else CAT_B, 0.7) for k, (_, v) in enumerate(doms)])
        names = VGroup(*[label(t, font_size=14, color=GREY_A).next_to(A.ax.c2p(k + 1, 0), DOWN,
                                                                    buff=0.12 + 0.2 * (k % 2))
                         for k, (t, _) in enumerate(doms)])
        nums = VGroup(*[label(f"{v:.2f}", font_size=16).next_to(A.ax.c2p(k + 1, v), UP, buff=0.05)
                        for k, (_, v) in enumerate(doms)])
        rows = rows_of([
            (r"Marjieh and colleagues, \ 2024: \ GPT models rated the similarity of pairs of stimuli given only as "
             r"text, \ such as Ekman's 14 colours as hex codes", WHITE),
            (r"their ratings tracked people's: \ $r = .89$ for the colours, \ and scaling them recovered the colour "
             r"wheel", MODEL),
            (r"weaker for taste and timbre, \ which language describes less well", CAT_B),
            (r"Firth's idea at scale: \ much of the structure of perception is written into how we talk about it",
             PROTO),
        ], 5.6, 20, 0.3).move_to([3.6, -0.1, 0])
        tag = published_tag(r"Marjieh, \ Sucholutsky, \ van Rijn, \ Jacoby \& Griffiths (2024)")
        with self.voiceover(
            "Now a surprise. <bookmark mark='a'/> In 2024 Raja Marjieh and colleagues asked large language models "
            "to rate the similarity of pairs of stimuli they could not see or hear: given only as text, like "
            "Ekman's fourteen colours written as hex codes. <bookmark mark='b'/> The ratings tracked people's. For "
            "Ekman's colours the correlation was point eight nine, and scaling the model's ratings recovered the "
            "colour wheel. Pitch did as well. <bookmark mark='c'/> It was weaker for taste and timbre, which "
            "language describes less well. <bookmark mark='d'/> That's Firth's idea at scale. Much of the structure "
            "of perception is written into how people talk about it, and a model of text can read it out, without "
            "an eye or an ear."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(A), *[GrowFromEdge(b, DOWN) for b in bs], FadeIn(names), FadeIn(nums), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def machines(self):
        head = heading(r"Learning concepts the way people do")
        cols = VGroup()
        items = [
            (r"one example", CAT_A, [r"Lake, \ Salakhutdinov \& Tenenbaum, \ 2015: \ handwritten characters from 50 "
                                     r"alphabets, \ learned from one example each",
                                     r"a model that infers how a character was drawn erred on 3.3\% of one-shot "
                                     r"tests; \ people on 4.5\%"]),
            (r"attention, \ again", MODEL, [r"Peterson, \ Abbott \& Griffiths, \ 2018: \ deep networks' image "
                                            r"features predict human similarity only moderately",
                                            r"reweighting the features, \ like ALCOVE's attention, \ brings them "
                                            r"much closer"]),
            (r"composition", PROTO, [r"Lake \& Baroni, \ 2023: \ a network trained on many small tasks learned to "
                                     r"combine new words the way people did",
                                     r"including people's typical errors"]),
        ]
        for k, (t, c, lines) in enumerate(items):
            col = VGroup(label(t, font_size=28, color=c),
                         rows_of([(lines[0], WHITE), (lines[1], GREY_A)], 3.7, 19, 0.3)).arrange(DOWN, buff=0.35,
                                                                                              aligned_edge=LEFT)
            col.move_to([-4.4 + 4.4 * k, 0.5, 0])
            cols.add(col)
        rows = rows_of([
            (r"the old theories return as engineering: \ the size principle, \ attention weights, \ structured "
             r"hypotheses", MODEL)], 12.4, 22, 0.3).to_edge(DOWN, buff=0.65)
        tag = published_tag(r"Lake et al. (2015); \ Peterson et al. (2018); \ Lake \& Baroni (2023)")
        with self.voiceover(
            "Can machines learn concepts the way people do? <bookmark mark='a'/> Brenden Lake, Ruslan Salakhutdinov "
            "and Joshua Tenenbaum gave a program handwritten characters from fifty alphabets, one example each. "
            "Their model inferred how each character had been drawn, stroke by stroke, a structured hypothesis like "
            "the number game's. On one-shot tests it erred on 3.3 percent, people on 4.5. "
            "<bookmark mark='b'/> Joshua Peterson, Joshua Abbott and Thomas Griffiths found that the image features "
            "of deep networks predict human similarity judgements only moderately, and that reweighting the features, "
            "much as ALCOVE's attention does, brings them much closer. <bookmark mark='c'/> And Lake and Marco "
            "Baroni trained a network on many small tasks until it learned to combine new words the way people did, "
            "including the errors people typically make. <bookmark mark='d'/> The old theories of this part keep "
            "coming back as engineering."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, c in zip("abc", cols):
                vo.wait_until(m)
                self.play(FadeIn(c, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]))
        self.clear_scene()

    def open_questions(self):
        head = heading(r"Open questions")
        rows = rows_of([
            (r"where are concepts in the brain? \ Huth and colleagues, \ 2016, \ mapped which cortex responds to "
             r"which meanings while people listened to stories: \ broad, \ bilateral maps, \ much alike from person "
             r"to person", WHITE),
            (r"is a concept one thing? \ prototypes, \ exemplars and theories may each describe a different use: \ "
             r"recognising, \ remembering, \ explaining", MODEL),
            (r"does a model that matches our similarities share our concepts? \ matching a table is not the same as "
             r"knowing why the members belong", CAT_A),
            (r"grounding: \ how text-trained systems, \ and children, \ tie words to the world", PROTO),
        ], 12.0, 22, 0.42).move_to([0, -0.1, 0])
        tag = published_tag(r"Huth, \ de Heer, \ Griffiths, \ Theunissen \& Gallant (2016)")
        with self.voiceover(
            "Four questions are open. <bookmark mark='a'/> Where are concepts in the brain? Alexander Huth and "
            "colleagues mapped which parts of the cortex respond to which meanings while people listened to stories "
            "for hours. The maps were broad, on both sides of the brain, and much alike from person to person. "
            "<bookmark mark='b'/> Is a concept one thing at all? Prototypes, exemplars and theories may each describe "
            "a different use of concepts: recognising, remembering, explaining. <bookmark mark='c'/> Does a model "
            "that matches our similarity tables share our concepts? Matching a table is not the same as knowing why "
            "the members belong, which was chapter nine's lesson. <bookmark mark='d'/> And grounding: how do "
            "systems trained on text, and children, come to tie their words to the world?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
