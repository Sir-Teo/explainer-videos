from __future__ import annotations

from videos.psychology.psych41.common import *  # noqa: F403


class Causes(VoiceoverScene):
    def construct(self):
        self.card()
        self.genes()
        self.environment()
        self.mothers()

    def card(self):
        card = chapter_card(6, r"Causes", r"Genes, \ environments, \ and a theory that did harm",
                            lit={2003: r"Sullivan et al.", 2016: r"Sekar et al.", 2022: r"Trubetskoy et al."},
                            part=PART, scale=("molecule", "person", "society"), marr=("what",))
        with self.voiceover("Chapter six. Causes."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def genes(self):
        head = heading(r"Many genes, \ each tiny")
        A = axes([-4, 4], [0, 0.45], x_length=5.4, y_length=2.6, xticks=None, yticks=None,
                 xlabel=r"liability: \ genes plus environment", ylabel=r"people", center=[-3.4, 0.6, 0], font_size=13)
        x = np.linspace(-4, 4, 300)
        y = np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi)
        dens = curve(A.ax, x, y, PERSON, stroke_width=3)
        cut = DashedLine(A.ax.c2p(2.7, 0), A.ax.c2p(2.7, 0.42), color=AUTH, stroke_width=2)
        xt = np.linspace(2.7, 4, 40)
        tail = area_under(A.ax, xt, np.exp(-xt ** 2 / 2) / np.sqrt(2 * np.pi), AUTH, 0.6)
        c_l = label(r"threshold", font_size=13, color=AUTH).next_to(A.ax.c2p(2.7, 0.42), UP, buff=0.06)
        lm = label(r"schematic: \ Part 9's liability-threshold model", font_size=13, color=GREY_B).next_to(
            A, DOWN, buff=0.3)
        rows = rows_of([
            (r"Sullivan, \ Kendler and Neale, \ 2003: \ twin studies put the heritability of liability near 0.8", WHITE),
            (r"Trubetskoy and colleagues, \ 2022: \ 287 regions of the genome, \ each adding a tiny amount of risk", MODEL),
            (r"Sekar and colleagues, \ 2016: \ variants of the immune gene C4 raise risk, \ and C4 marks synapses for "
             r"pruning in adolescence, \ when onset begins", SYMP),
            (r"Part 9's lesson again: \ heritable does not mean fixed, \ and no single gene of large effect", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Sullivan, \ Kendler \& Neale (2003); \ Trubetskoy et al.\ (2022); \ Sekar et al.\ (2016)")
        with self.voiceover(
            "Start with genes. <bookmark mark='a'/> In 2003 Patrick Sullivan, Kenneth Kendler and Michael Neale "
            "pooled the twin studies. They put the heritability of liability to schizophrenia near eighty percent. "
            "<bookmark mark='b'/> The genes behind it are many. In 2022 a consortium led by Vassily Trubetskoy "
            "reported two hundred and eighty-seven regions of the genome, each adding a tiny amount of risk. "
            "<bookmark mark='c'/> One clue to mechanism: in 2016 Aswin Sekar and colleagues showed that variants of "
            "an immune gene, C4, raise risk, and that C4 marks synapses for pruning in adolescence, just when onset "
            "begins. <bookmark mark='d'/> It's Part 9's lesson again. Heritable doesn't mean fixed, and there's no "
            "single gene of large effect."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(lm), Create(dens))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(cut), FadeIn(tail), FadeIn(c_l))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def environment(self):
        head = heading(r"Environments that raise risk")
        data = (
            (r"heavy cannabis use", r"the heaviest users had about four times the odds of a psychotic disorder in a "
                                    r"2016 meta-analysis; \ whether cannabis causes it is debated", AUTH),
            (r"growing up in a city", r"higher rates in urban upbringing, \ in a dose-response pattern", SYMP),
            (r"migration", r"higher rates in migrants and their children, \ especially where they are a small, \ "
                           r"excluded minority", PERSON),
            (r"adversity", r"childhood trauma and social defeat go with higher risk", MODEL),
        )
        rows = VGroup()
        for what, how, c in data:
            rows.add(VGroup(word_chip(what, color=c, font_size=18, width=3.6), wrapped_label(how, 8.2, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.1, 0])
        foot = wrapped_label(r"all observational: \ confounding and reverse causation are live, \ and genes and "
                             r"environments are tangled together", 12.0, 20, YOU).move_to([0, -2.7, 0])
        tag = published_tag(r"Marconi et al.\ (2016)")
        with self.voiceover(
            "Environments matter too. <bookmark mark='a'/> Heavy cannabis use: in a 2016 meta-analysis led by Arianna "
            "Marconi, the heaviest users had about four times the odds of a psychotic disorder. Whether cannabis "
            "causes it is still debated. <bookmark mark='b'/> Growing up in a city: higher rates with urban "
            "upbringing, in a dose-response pattern. <bookmark mark='c'/> Migration: higher rates in migrants and "
            "their children, especially where they're a small, excluded minority. <bookmark mark='d'/> And "
            "adversity: childhood trauma and social defeat go with higher risk. <bookmark mark='e'/> All of this is "
            "observational. Confounding and reverse causation are live, and genes and environments are tangled "
            "together."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def mothers(self):
        head = heading(r"A theory that did harm")
        rows = rows_of([
            (r"Fromm-Reichmann, \ 1948: \ the ``schizophrenogenic mother'', \ cold and controlling, \ was said to cause "
             r"schizophrenia in her child", AUTH),
            (r"for decades families were blamed, \ and mothers were treated as the cause of their children's illness", WHITE),
            (r"no evidence supported it; \ twin and adoption studies pointed elsewhere", GOOD),
            (r"a theory is not harmless because it is only a theory: \ autism's ``refrigerator mother'' repeated the "
             r"mistake", YOU),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        tag = historical_tag(r"Fromm-Reichmann (1948)")
        with self.voiceover(
            "One theory of cause did real harm. <bookmark mark='a'/> In 1948 the psychoanalyst Frieda Fromm-Reichmann "
            "wrote of the schizophrenogenic mother, cold and controlling, who was said to cause schizophrenia in her "
            "child. <bookmark mark='b'/> For decades, families were blamed, and mothers treated as the cause of their "
            "children's illness. <bookmark mark='c'/> No evidence supported it. Twin and adoption studies pointed "
            "elsewhere. <bookmark mark='d'/> A theory isn't harmless because it's only a theory. Autism's refrigerator "
            "mother, later in this part, repeated the mistake."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
