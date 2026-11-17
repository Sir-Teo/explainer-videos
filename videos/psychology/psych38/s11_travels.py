from __future__ import annotations

from videos.psychology.psych38.common import *  # noqa: F403


class Travels(VoiceoverScene):
    def construct(self):
        self.card()
        self.manylabs()
        self.generality()

    def card(self):
        card = chapter_card(10, r"What travels", r"Which findings hold everywhere?",
                            lit={2017: r"Simons, \ Shoda \& Lindsay", 2018: r"Klein et al."}, part=PART,
                            scale=("person", "culture"), marr=("what",))
        with self.voiceover("Chapter ten. What travels."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def manylabs(self):
        head = heading(r"Twenty-eight findings, \ thirty-six countries")
        A = axes([0, 0.9], [-0.5, 27.5], x_length=4.6, y_length=4.4, xticks=[0, 0.2, 0.4, 0.6, 0.8], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"effect size, \ $d$", center=[-3.6, -0.3, 0], font_size=13)
        # schematic: originals spread around a median of 0.60, replications around 0.15
        rng = np.random.default_rng(28)
        orig = np.clip(np.sort(rng.gamma(4.0, 0.15, 28)), 0.05, 0.88)
        rep = np.clip(orig * 0.25 + rng.normal(0, 0.05, 28), 0.0, 0.88)
        ys = np.arange(28)
        o = scatter(A.ax, orig, ys, GREY_A, radius=0.045)
        r_ = scatter(A.ax, rep, ys, WEST, radius=0.05)
        links = VGroup(*[Line(A.ax.c2p(a, y), A.ax.c2p(b, y), color=GREY_D, stroke_width=1.2) for a, b, y in
                         zip(orig, rep, ys)])
        key = legend([(GREY_A, r"original"), (WEST, r"replication")], font_size=14).move_to(A.ax.c2p(0.7, 3))
        note = label(r"schematic: \ medians as reported", font_size=13, color=GREY_B).next_to(A, DOWN, buff=0.3)
        rows = rows_of([
            (r"Many Labs 2, \ 2018: \ 28 classic findings, \ 125 samples, \ 15{,}305 people in 36 countries and "
             r"territories", WHITE),
            (r"the median effect fell from $d = 0.60$ in the originals to $0.15$; \ 15 of the 28 were significant "
             r"in the original direction", WEST),
            (r"and effects varied little from sample to sample, \ including between WEIRD and less WEIRD samples", GOOD),
            (r"what mattered was the finding, \ not the place: \ effects that replicated did so nearly everywhere, \ "
             r"and those that failed failed nearly everywhere", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Klein et al.\ (2018), \ Many Labs 2")
        with self.voiceover(
            "If cultures differ so much, why do some findings travel? <bookmark mark='a'/> In 2018 Many Labs 2 "
            "tested twenty-eight classic findings in a hundred and twenty-five samples, fifteen thousand three "
            "hundred people in thirty-six countries and territories. <bookmark mark='b'/> The median effect fell "
            "from point six in the originals to point one five. Fifteen of the twenty-eight were significant in the "
            "original direction. <bookmark mark='c'/> And the effects varied little from sample to sample, including "
            "between WEIRD and less WEIRD samples. <bookmark mark='d'/> What mattered was the finding, not the place. "
            "Effects that replicated did so nearly everywhere, and those that failed, failed nearly everywhere."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(o), FadeIn(key))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(links), FadeIn(r_))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def generality(self):
        head = heading(r"What holds, \ and how to say so")
        left = VGroup(word_chip(r"travels well", color=GOOD, font_size=19, width=4.6),
                      wrapped_label(r"psychophysics: \ thresholds and Weber's law (Part 11); \ basic conditioning "
                                    r"(Part 16); \ much of memory (Parts 20 and 21); \ the switch-footbridge gap",
                                    4.6, 18, WHITE)).arrange(DOWN, buff=0.3)
        right = VGroup(word_chip(r"varies", color=WORLD, font_size=19, width=4.6),
                       wrapped_label(r"how much people conform, \ give, \ punish and trust strangers; \ how they "
                                     r"describe themselves; \ some perceptual habits; \ the level of moral "
                                     r"approval", 4.6, 18, WHITE)).arrange(DOWN, buff=0.3)
        VGroup(left, right).arrange(RIGHT, buff=0.6, aligned_edge=UP).move_to([-0.2, 1.0, 0])
        rows = rows_of([
            (r"Simons, \ Shoda and Lindsay, \ 2017: \ end every paper with a constraints-on-generality statement: \ "
             r"the populations, \ materials and settings the authors expect the finding to hold for, \ and why",
             MODEL),
            (r"a finding without a stated population is a finding about the people who happened to be tested", YOU),
        ], 12.0, 20, 0.32).to_edge(DOWN, buff=0.8)
        tag = published_tag(r"Simons, \ Shoda \& Lindsay (2017)")
        with self.voiceover(
            "So what holds? <bookmark mark='a'/> Some things travel well: thresholds and Weber's law from Part 11, "
            "basic conditioning from Part 16, much of memory from Parts 20 and 21, and the gap between switching and "
            "pushing. <bookmark mark='b'/> Other things vary: how much people conform, give, punish and trust "
            "strangers, how they describe themselves, some perceptual habits, and the level of moral approval. "
            "<bookmark mark='c'/> In 2017 Daniel Simons, Yuichi Shoda and Stephen Lindsay proposed a habit: end "
            "every paper with a constraints-on-generality statement, naming the populations, materials and settings "
            "the authors expect the finding to hold for, and why. <bookmark mark='d'/> A finding without a stated "
            "population is a finding about the people who happened to be tested."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left, shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(right, shift=UP * 0.15))
            for m, r in zip("cd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
