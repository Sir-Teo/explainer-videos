from __future__ import annotations

import numpy as np

from videos.psychology.psych9.common import *  # noqa: F403


class Candidate(VoiceoverScene):
    def construct(self):
        self.card()
        self.story()
        self.power()
        self.flexible()
        self.collapse()

    def card(self):
        card = chapter_card(8, r"The candidate-gene decade", r"Which genes? And why were the first answers wrong?",
                            lit={2003: r"a gene for depression?"}, part=PART, scale=("molecule", "person"), marr=("tissue",))
        with self.voiceover(
            "Chapter eight. The candidate-gene decade."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def story(self):
        c = archive.CASPI_2003.data
        head = heading(r"Pick a gene with a good story, \ and test it")
        steps = chain([r"a candidate gene, \ in a short and a long version", r"a few hundred people, genotyped",
                       r"do the versions differ in the trait?"], [GENE, VOLT, THRESH], width=12.6, font_size=29, height=1.3)
        steps.move_to([0, 1.7, 0])
        rows = rows_of([
            (r"the serotonin transporter: \ serotonin is what common antidepressants act on", WHITE),
            (rf"2003, {c['cohort']}: \ people with the short version were more often depressed after stressful events", DATA),
            (r"a gene, \ an environment, \ and an interaction between them", GENE),
            (r"one of the most celebrated findings of its decade; \ hundreds of studies of the same kind followed", GREY_A),
        ], 12.4, 30, 0.26).move_to([0, -1.35, 0])
        src = published_tag(archive.CASPI_2003.cite)
        with self.voiceover(
            "Twin studies say that genes matter. They don't say which genes. In the nineteen-nineties it "
            "became cheap to read a person's version of one particular gene, and a new kind of study took "
            "off. <bookmark mark='a'/> Pick a candidate: a gene with a good story. The serotonin "
            "transporter, for instance. Serotonin is what the common antidepressants act on, and the gene "
            "comes in a short version and a long one. Read it in a few hundred people, and test whether "
            "the versions differ in the trait. <bookmark mark='b'/> The most famous result came in 2003, "
            "from a study that had followed people in Dunedin, New Zealand, since their birth. People "
            "with the short version, it reported, were more likely to become depressed after stressful "
            "events in their lives. <bookmark mark='c'/> A gene, an environment, and an interaction "
            "between the two. <bookmark mark='d'/> It was one of the most celebrated findings of its "
            "decade, and hundreds of studies of the same kind followed it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(steps.boxes[0]))
            vo.wait_until("a")
            self.play(GrowArrow(steps.arrows[0]), FadeIn(steps.boxes[1]), GrowArrow(steps.arrows[1]), FadeIn(steps.boxes[2]),
                      FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def power(self):
        d = load("candidate")
        head = heading(r"The arithmetic that was missing")
        lx = np.log10(d["ns"])
        A = axes([2, 6], [0, 1.05], x_length=6.4, y_length=4.2, xticks=[2, 3, 4, 5, 6], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: rf"10^{{{int(v)}}}", yfmt=lambda v: pct(v), xlabel=r"people in the study",
                 ylabel=r"chance of detecting the gene", center=[-3.3, -0.45, 0])
        ax = A.ax
        cv = curve(ax, lx, d["power"], GENE, stroke_width=4)
        floor = DashedLine(ax.c2p(2, 0.05), ax.c2p(6, 0.05), color=BAD, stroke_width=2)
        fl = label(r"5\%: \ what nothing gives", font_size=26, color=BAD).next_to(ax.c2p(6, 0.05), UL, buff=0.08)
        p1 = VGroup(Dot(ax.c2p(3, d["power_1000"]), radius=0.1, color=WHITE),
                    label(rf"1{{,}}000 people: \ {pct(d['power_1000'])}", font_size=28).next_to(ax.c2p(3, d["power_1000"]), UP,
                                                                                               buff=0.45))
        p2 = VGroup(Dot(ax.c2p(np.log10(d["need"]), 0.8), radius=0.1, color=WHITE),
                    label(rf"{d['need']:,}".replace(",", "{,}") + r" people: \ 80\%", font_size=28).next_to(
                        ax.c2p(np.log10(d["need"]), 0.8), LEFT, buff=0.2))
        rows = rows_of([
            (rf"the largest effect of one common variant on years of schooling: \ {100 * d['r2']:.2f}\% of the differences",
             DATA),
            (r"a study of a few hundred could not have seen an effect of that size", WHITE),
            (r"and yet such studies kept reporting hits", BAD),
        ], 4.9, 30, 0.32).move_to([4.4, -0.3, 0])
        keep_in_frame(rows)
        src = published_tag(archive.RIETVELD_2013.cite)
        tag = psyche_tag(r"computed: a test at the 5\% level")
        with self.voiceover(
            "Here's the trouble, and it's arithmetic. When very large studies finally measured the effect "
            "of single common gene variants on a trait like years of schooling, the largest one explained "
            "about two hundredths of one percent of the differences between people. "
            "<bookmark mark='a'/> How many people does it take to detect an effect of that size? For an "
            f"eighty percent chance, at the usual threshold: {d['need']:,}. <bookmark mark='b'/> A study "
            f"of a thousand people has a {100 * d['power_1000']:.0f} percent chance, when five percent is "
            "what you'd get from nothing at all. <bookmark mark='c'/> So a candidate-gene study of a few "
            "hundred people couldn't have detected a real effect of realistic size. And yet such studies "
            "reported hits, year after year. You know from Part 4 what that means."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(A), Create(floor), FadeIn(fl), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Create(cv), run_time=2.0)
            self.play(FadeIn(p2))
            vo.wait_until("b")
            self.play(FadeIn(p1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2], shift=UP * 0.1))
        self.clear_scene()

    def flexible(self):
        d = load("candidate")
        head = heading(r"A gene that does nothing, \ studied 2{,}000 times")
        A = axes([0, 1], [0, float(d["p_hist"].max()) * 1.1], x_length=6.0, y_length=3.6, xticks=[0, 0.5, 1.0], yticks=[],
                 xfmt=lambda v: f"{v:.1f}", xlabel=r"the smallest $p$ among a laboratory's 18 analyses", ylabel=r"",
                 center=[-3.5, -0.6, 0])
        edges = np.linspace(0, 1, 21)
        bars = hist(A.ax, edges, d["p_hist"], OWN)
        first = hist(A.ax, edges[:2], d["p_hist"][:1], BAD, opacity=0.9)
        fl = label(rf"$p < .05$: \ {pct(d['rate_any'])}", font_size=30, color=BAD).next_to(
            A.ax.c2p(0.06, float(d["p_hist"][0])), RIGHT, buff=0.2)
        choices = rows_of([
            (rf"the planned analysis only: \ {pct(d['rate_planned'])} of laboratories find something", MODEL),
            (r"the choices: \ count copies, \ or ``any short'', \ or ``two short''; \ everyone, \ men, \ women; \ two "
             r"measures of the trait", WHITE),
            (rf"report the best of the {d['analyses']}: \ {pct(d['rate_any'])} find a significant effect", BAD),
            (r"add journals that prefer positive results, \ and that is a literature", GREY_A),
        ], 5.2, 30, 0.3).move_to([4.2, -0.3, 0])
        keep_in_frame(choices)
        tag = psyche_tag(rf"simulated: {d['n_each']} people in each study; \ the gene has no effect")
        with self.voiceover(
            "So here's a gene that does nothing, studied by two thousand laboratories, with "
            f"{d['n_each']} people each. <bookmark mark='a'/> If every laboratory runs the one analysis "
            f"it planned, {100 * d['rate_planned']:.0f} percent find something, as they should. "
            "<bookmark mark='b'/> But there are choices. Count the copies of the short version, or lump "
            "people into 'any short' or 'two short'. Analyse everyone, or men and women separately. Use "
            f"one measure of depression, or another. That's {d['analyses']} analyses, every one of them "
            f"defensible. <bookmark mark='c'/> Let each laboratory report its best, and "
            f"{100 * d['rate_any']:.0f} percent find a significant effect of a gene that does nothing. "
            "<bookmark mark='d'/> Add journals that prefer positive results, and you have a literature."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(bars))
            vo.wait_until("a")
            self.play(FadeIn(choices[0]))
            vo.wait_until("b")
            self.play(FadeIn(choices[1]))
            vo.wait_until("c")
            self.play(FadeIn(first), FadeIn(fl), FadeIn(choices[2]))
            vo.wait_until("d")
            self.play(FadeIn(choices[3], shift=UP * 0.1))
        self.clear_scene()

    def collapse(self):
        c, ch, b = archive.CASPI_2003.data, archive.CHABRIS_2012.data, archive.BORDER_2019.data
        head = heading(r"Then the tests arrived")
        items = [
            (r"2009", rf"the serotonin gene and depression, \ pooled: \ {c['risch_studies']} studies, \ more than "
                      rf"{num(c['risch_people'])} people", r"no association, \ with stress or without", BAD),
            (r"2012", rf"{ch['variants']} published variants for intelligence, \ retested in three large samples",
             rf"{ch['significant']} of {ch['tests']} tests significant; \ {ch['expected'][0]} to {ch['expected'][1]} expected "
             r"if the effects were real", BAD),
            (r"2019", rf"the {b['genes']} most-studied genes for depression, \ a plan registered in advance, \ up to "
                      rf"{num(b['n_max'])} people", r"none held up; \ no better than genes picked at random",
             BAD),
        ]
        rows = VGroup()
        for i, (year, what, found, col) in enumerate(items):
            y = 2.1 - 1.4 * i
            yr = label(year, font_size=44, color=DATA).move_to([-5.7, y, 0])
            txt = VGroup(wrapped_label(what, 10.2, 29, WHITE), wrapped_label(found, 10.2, 30, col)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08)
            txt.move_to([0, y, 0]).align_to(np.array([-4.6, 0, 0]), LEFT)
            rows.add(VGroup(yr, txt))
        end = wrapped_label(r"Genes do matter for behaviour: \ the twin studies stand. \ Each gene matters so little that "
                            r"this method could not see it.", 12.4, 31, P.ACCENT).to_edge(DOWN, buff=0.85)
        src = published_tag(archive.BORDER_2019.cite + r"; \ " + archive.CHABRIS_2012.cite)
        with self.voiceover(
            "And then the tests arrived. <bookmark mark='a'/> In 2009, a pooled analysis of "
            f"{c['risch_studies']} studies, more than {c['risch_people']:,} people, found no association "
            "between the serotonin gene and depression, with stress or without. <bookmark mark='b'/> In "
            f"2012, {ch['variants']} published gene variants for intelligence were retested in three "
            f"large samples. Of {ch['tests']} tests, {ch['significant']} was significant, where "
            f"{ch['expected'][0]} to {ch['expected'][1]} were expected if the published effects were "
            f"real. <bookmark mark='c'/> And in 2019 a team took the {b['genes']} most-studied candidate "
            "genes for depression and tested each one, with a plan registered in advance, in samples of "
            f"up to {b['n_max']:,} people. None held up. As a set, the famous genes did no better than "
            "genes picked at random. <bookmark mark='d'/> A decade of findings, hundreds of papers, and "
            "almost nothing there. It goes on the Ledger today. The lesson isn't that genes don't matter "
            "for behaviour. The twin studies stand. It's that each gene matters so little that this "
            "method couldn't see it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(rows[0][0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0][1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()
