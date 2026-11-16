from __future__ import annotations

from videos.psychology.psych38.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.products()
        self.alignment()

    def card(self):
        card = chapter_card(13, r"In practice: \ products, \ surveys and machines", r"Whose values get built in?",
                            lit=(), part=PART, scale=("group", "culture"), marr=("what",))
        with self.voiceover("Chapter thirteen. In practice: products, surveys and machines."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def products(self):
        head = heading(r"Taking a test or a product abroad")
        items = [
            (r"localization", r"a product tested on one country's users is tested on one country's users; \ "
                              r"repeat the key tests where it will ship", WEST),
            (r"global surveys", r"translate, \ back-translate, \ check invariance, \ and beware the reference "
                                r"group: \ compare behaviour where you can", MODEL),
            (r"tests and hiring", r"a test validated in one population needs evidence in the next; \ norms and "
                                  r"predictive validity both move", WORLD),
            (r"teams", r"directness, \ hierarchy and feedback norms differ; \ say the norms out loud instead of "
                       r"assuming yours", GOOD),
        ]
        rows = VGroup()
        for what, how, c in items:
            rows.add(VGroup(word_chip(what, color=c, font_size=19, width=3.2), wrapped_label(how, 8.6, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, -0.2, 0])
        with self.voiceover(
            "Industry meets this problem every time it crosses a border. <bookmark mark='a'/> Localization: a "
            "product tested on one country's users has been tested on one country's users. Repeat the key tests "
            "where it will ship. <bookmark mark='b'/> Global surveys: translate, translate back, check invariance, "
            "and beware the reference group. Compare behaviour where you can. <bookmark mark='c'/> Tests and hiring: "
            "a test validated in one population needs fresh evidence in the next. Both norms and predictive "
            "validity can move. <bookmark mark='d'/> And teams: norms of directness, hierarchy and feedback differ. "
            "Say them out loud, instead of assuming yours."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def alignment(self):
        head = heading(r"Aligning machines to whom?")
        A = axes([0, 1], [0, 1], x_length=4.4, y_length=3.2, xticks=None, yticks=None,
                 xlabel=r"cultural distance from the United States", ylabel=r"similarity to the model's answers",
                 center=[-3.6, -0.1, 0], font_size=14)
        rng = np.random.default_rng(65)
        x = rng.uniform(0.02, 0.95, 65)
        y = 0.9 - 0.65 * x + rng.normal(0, 0.08, 65)
        pts = scatter(A.ax, x, y, WORLD, radius=0.05)
        note = label(r"schematic: \ 65 countries", font_size=13, color=GREY_B).next_to(A, DOWN, buff=0.35)
        rows = rows_of([
            (r"a language model answers survey questions in a voice; \ whose?", WHITE),
            (r"Atari and colleagues, \ 2023: \ a model's answers to the World Values Survey sat closest to those of "
             r"WEIRD countries, \ and grew less similar the further a country was culturally from the United States",
             WORLD),
            (r"training text and human feedback both come mostly from WEIRD sources", AUTH),
            (r"alignment is a question this part has been asking all along: \ which population, \ measured how, \ "
             r"stands in for ``people''?", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Atari et al.\ (2023), \ preprint")
        with self.voiceover(
            "The newest version of the problem is in machines. <bookmark mark='a'/> A language model answers "
            "questions in a voice. Whose? <bookmark mark='b'/> In 2023 Mohammad Atari and colleagues gave a model "
            "the World Values Survey. Its answers sat closest to those of WEIRD countries, and grew less similar "
            "the further a country was, culturally, from the United States. <bookmark mark='c'/> Both the training "
            "text and the human feedback come mostly from WEIRD sources. <bookmark mark='d'/> Aligning a model to "
            "human values asks the question this whole part has been asking: which population, measured how, "
            "stands in for people?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[FadeIn(p, scale=1.4) for p in pts], lag_ratio=0.03))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
