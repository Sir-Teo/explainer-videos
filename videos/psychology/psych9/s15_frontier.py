from __future__ import annotations

import math

import numpy as np

from videos.psychology.psych9.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.strata()
        self.siblings()
        self.whose()
        self.open()

    def card(self):
        card = chapter_card(14, r"Frontier: inside the family", r"How do you tell a gene's effect from its company?",
                            lit={2022: r"178{,}086 siblings"}, part=PART, scale=("molecule", "person", "culture"),
                            marr=("how",))
        with self.voiceover(
            "Chapter fourteen. Frontier: inside the family."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def strata(self):
        d = load("strata")
        expo = round(-math.log10(d["pooled_p"]))
        head = heading(r"Why comparing strangers can mislead")
        g = np.random.default_rng(7)

        def crowd(x0, freq, col, name, habit):
            dots = VGroup(*[Dot(radius=0.085, color=GENE if g.random() < freq else OWN) for _ in range(60)])
            dots.arrange_in_grid(rows=6, buff=0.13).move_to([x0, 1.1, 0])
            t = VGroup(label(name, font_size=31, color=col),
                       label(rf"the variant: \ {pct(freq)}", font_size=28, color=GENE),
                       label(habit, font_size=28, color=WHITE)).arrange(DOWN, buff=0.1)
            t.next_to(dots, DOWN, buff=0.2)
            return VGroup(dots, t)

        a = crowd(-5.0, d["f_a"], MZC, r"population A", r"few use chopsticks")
        b = crowd(-1.7, d["f_b"], DZC, r"population B", r"most use chopsticks")
        rows = rows_of([
            (r"the variant does nothing; \ the two populations differ in it, \ and in the habit, \ for separate reasons",
             WHITE),
            (rf"pool them: \ the variant ``predicts'' the habit, \ $p \approx 10^{{-{expo}}}$", BAD),
            (rf"within either population: \ nothing ($p = {d['within_a_p']:.2f}$ and ${d['within_b_p']:.2f}$)", MODEL),
            (r"corrections for ancestry help; \ they cannot be proved complete", GREY_A),
        ], 5.3, 29, 0.3).move_to([4.2, 0.0, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"simulated: 4{,}000 people, a variant with no effect")
        with self.voiceover(
            "The frontier of this part is the family, and here's why. <bookmark mark='a'/> Take two "
            "populations that differ, for reasons of ancestry, in how common a gene variant is. They also "
            "differ in a habit, for reasons that have nothing to do with the gene. Eating with chopsticks, "
            "in the classic teaching example. <bookmark mark='b'/> Pool the two, and the variant predicts "
            f"the habit, with a p-value near ten to the minus {expo}. A gene for chopsticks. "
            "<bookmark mark='c'/> Within either population, there's nothing. <bookmark mark='d'/> "
            "Statistical corrections for ancestry help a great deal, and they can't be proved complete. "
            "For traits like schooling, which follow geography and class as well as genes, that matters."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(a), FadeIn(b))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def siblings(self):
        d = load("strata")
        h = archive.HOWE_2022.data
        head = heading(r"Mendel's lottery: \ compare brothers and sisters")
        mum = VGroup(Square(side_length=0.5, stroke_width=0, fill_color=GENE, fill_opacity=0.9),
                     Square(side_length=0.5, stroke_width=0, fill_color=OWN, fill_opacity=0.6)).arrange(RIGHT, buff=0.06)
        dad = mum.copy()
        mum.move_to([-5.4, 1.7, 0])
        dad.move_to([-3.4, 1.7, 0])
        pl = label(r"each parent: \ two copies", font_size=28, color=GREY_A).move_to([-4.4, 2.4, 0])
        kids = VGroup()
        for i, (m, f_) in enumerate(((GENE, GENE), (OWN, GENE), (OWN, OWN))):
            k = VGroup(Square(side_length=0.5, stroke_width=0, fill_color=m, fill_opacity=0.9 if m == GENE else 0.6),
                       Square(side_length=0.5, stroke_width=0, fill_color=f_, fill_opacity=0.9 if f_ == GENE else 0.6))
            k.arrange(RIGHT, buff=0.06).move_to([-5.9 + 1.5 * i, -0.4, 0])
            kids.add(k)
        arrows = VGroup(*[Arrow([-4.4, 1.3, 0], k.get_top(), buff=0.1, color=GREY_B, stroke_width=3,
                                max_tip_length_to_length_ratio=0.12) for k in kids])
        kl = wrapped_label(r"each child gets one copy from each parent, by a coin flip: \ same parents, same home, same "
                           r"ancestry", 4.6, 28, WHITE).move_to([-4.4, -1.75, 0])
        keep_in_frame(kl)
        rows = rows_of([
            (rf"2022: \ a genome-wide study \emph{{within}} families, \ {num(h['siblings'])} siblings", DATA),
            (r"smaller effects within families for: \ schooling, \ test scores, \ height, \ depressive symptoms, \ smoking", HOME),
            (r"about the same for bodily measures such as cholesterol", GENE),
            (rf"our simulation with two strata: \ ${d['population']:.2f}$ between strangers, \ ${d['within']:.2f}$ between "
             r"siblings, \ and the second is the truth", MODEL),
        ], 6.4, 29, 0.3).move_to([3.5, -0.2, 0])
        keep_in_frame(rows)
        src = published_tag(archive.HOWE_2022.cite)
        tag = note(r"the family: schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "But brothers and sisters can't differ in ancestry. They have the same parents. "
            "<bookmark mark='a'/> And which of a parent's two copies each child receives is a coin flip. "
            "It's Mendel's lottery, and it's as fair an experiment as nature offers: same parents, same "
            "home, and a random draw of genes. <bookmark mark='b'/> So the newest studies run the "
            f"genome-wide scan between siblings. In 2022, with {h['siblings']:,} siblings, the effects "
            "estimated inside families came out smaller than the usual estimates for schooling, test "
            "scores, height, depressive symptoms and smoking. <bookmark mark='c'/> For bodily measures "
            "such as cholesterol, they were about the same. <bookmark mark='d'/> The traits where the "
            "home has a say are the ones where comparing strangers had overstated what genes do. In our "
            f"own simulation with two strata, the effect looks like {d['population']:.2f} between "
            f"strangers and {d['within']:.2f} between siblings, and the second is the one we planted."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(mum), FadeIn(dad), FadeIn(pl))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a_), FadeIn(k)) for a_, k in zip(arrows, kids)], lag_ratio=0.5),
                      FadeIn(kl), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def whose(self):
        m = archive.MARTIN_2019.data
        head = heading(r"Whose genomes?")
        full = 9.0
        bars = VGroup()
        items = [(r"European ancestry (where the scores were built)", 1.0, GENE),
                 (r"East Asian ancestry", 1 / m["fold_lower_east_asian"], THRESH),
                 (r"African ancestry", 1 / m["fold_lower_african"], BAD)]
        for i, (name, v, col) in enumerate(items):
            y = 1.25 - 1.0 * i
            bar = Rectangle(width=full * v, height=0.45, stroke_width=0, fill_color=col, fill_opacity=0.9)
            bar.move_to([-6.2 + full * v / 2, y, 0])
            nm = label(name, font_size=29, color=col).next_to(bar, UP, buff=0.08).align_to(bar, LEFT)
            bars.add(VGroup(bar, nm))
        bl = label(r"how well a score predicts, \ relative to the people it was built on", font_size=29, color=GREY_A)
        bl.move_to([0, 2.5, 0]).align_to(np.array([-6.2, 0, 0]), LEFT)
        rows = rows_of([
            (rf"about {pct(m['european_share'])} of the people in genome-wide studies have been of European ancestry", DATA),
            (r"the positions on a chip are markers, not causes; \ which marker travels with which cause depends on a "
             r"population's history", WHITE),
            (r"The tools work best for the people already best served. \ The remedy is to study everyone.", P.ACCENT),
        ], 12.4, 30, 0.2).to_edge(DOWN, buff=0.8)
        src = published_tag(archive.MARTIN_2019.cite)
        with self.voiceover(
            "A second frontier: whose genomes? <bookmark mark='a'/> About four fifths of the people in "
            "genome-wide studies have been of European ancestry. <bookmark mark='b'/> A score built on "
            "them predicts about half as well in people of East Asian ancestry, and several times worse "
            "in people of African ancestry. <bookmark mark='c'/> That isn't because the biology differs. "
            "The positions on a chip are markers, not causes, and which marker travels with which cause "
            "depends on a population's history. <bookmark mark='d'/> So today the tools of this field "
            "work best for the people who were already best served. The remedy is to study everyone."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(bl), FadeIn(bars[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[1], shift=RIGHT * 0.15), FadeIn(bars[2], shift=RIGHT * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2], shift=UP * 0.1))
        self.clear_scene()

    def open(self):
        head = heading(r"What is not settled")
        items = [
            (r"What is in the missing heritability?", r"Rarer variants, read by sequencing whole genomes; \ or twin "
                                                       r"estimates that were too high to begin with.", GENE),
            (r"How does genetic nurture work?", r"Which parts of a home do parents' genes shape, \ and could those parts "
                                                 r"be given to any child?", HOME),
            (r"From a position to a behaviour?", r"A variant, a gene, a cell type, a circuit, a habit: \ for almost no "
                                                 r"behavioural trait has that path been traced.", MODEL),
            (r"What should a score be used for?", r"Research on groups, \ or decisions about one child or one embryo? \ "
                                                  r"The arithmetic says which it can bear.", THRESH),
        ]
        rows = VGroup(*[VGroup(label(q, font_size=34, color=c), wrapped_label(a, 12.2, 29, WHITE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08) for q, a, c in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.34)
        rows.move_to([0, 0.35, 0])
        star = wrapped_label(r"$\star$ \ Problem 7: \ design the study that would tell a direct effect of a child's genes "
                             r"from an effect of the home their parents' genes made.", 12.4, 29,
                             P.ACCENT).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "So here's what isn't settled. <bookmark mark='a'/> What's in the missing heritability? Rarer "
            "variants, which need whole genomes to be read. Or twin estimates that were too high to begin "
            "with. Probably some of each. <bookmark mark='b'/> How does genetic nurture work? Which parts "
            "of a home do parents' genes shape, and could those parts be given to any child? That would "
            "turn a genetic finding into an environmental one. <bookmark mark='c'/> How do you get from a "
            "position in the genome to a behaviour? Through a gene, a kind of cell, a circuit and a "
            "habit. For almost no behavioural trait has that path been traced. <bookmark mark='d'/> And "
            "what should a score be used for? Research on groups, or decisions about one child, or one "
            "embryo? The arithmetic in this part says which of those it can bear. <bookmark mark='e'/> "
            "The starred problem asks you to design the study that separates a child's own genes from "
            "the home that their parents' genes made."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0][0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0][1]))
            for mark_, r in zip("bcd", rows[1:]):
                vo.wait_until(mark_)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(star, shift=UP * 0.1))
        self.clear_scene()
