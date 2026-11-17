from __future__ import annotations

from videos.psychology.psych41.common import *  # noqa: F403


class Autism(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.vaccines()
        self.priors()
        self.prevalence()
        self.facilitated()

    def card(self):
        card = chapter_card(10, r"Autism", r"Histories, \ myths, \ models and evidence",
                            lit={1943: r"Kanner", 1998: r"Wakefield et al.", 2012: r"Pellicano \& Burr"}, part=PART,
                            scale=("person", "society"), marr=("what",))
        with self.voiceover("Chapter ten. Autism."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def history(self):
        head = heading(r"Two first descriptions")
        steps = VGroup()
        for yr, txt, c in (
                (r"1943", r"Kanner in Baltimore describes eleven children with a powerful wish for sameness and "
                          r"little interest in other people", SYMP),
                (r"1944", r"Asperger in Vienna describes boys with intense interests and social difficulty; \ "
                          r"historians have since documented his part in the Nazi-era system that sent some disabled "
                          r"children to their deaths", AUTH),
                (r"1967", r"Bettelheim's \emph{The Empty Fortress} blames cold ``refrigerator mothers'': \ the "
                          r"schizophrenogenic mother again", AUTH),
                (r"since", r"twin studies show high heritability; \ autism is developmental, \ not caused by "
                           r"parenting", GOOD)):
            steps.add(VGroup(word_chip(yr, color=c, font_size=20, width=1.6), wrapped_label(txt, 10.0, 20, WHITE))
                      .arrange(RIGHT, buff=0.35))
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([0, -0.2, 0])
        tag = historical_tag(r"Kanner (1943); \ Asperger (1944)")
        with self.voiceover(
            "Autism has two first descriptions. <bookmark mark='a'/> In 1943 Leo Kanner in Baltimore described eleven "
            "children with a powerful wish for sameness and little interest in other people. <bookmark mark='b'/> "
            "In 1944 Hans Asperger in Vienna described boys with intense interests and social difficulty. Historians "
            "have since documented his part in the Nazi-era system that sent some disabled children to their deaths. "
            "<bookmark mark='c'/> In 1967 Bruno Bettelheim's book The Empty Fortress blamed cold refrigerator "
            "mothers: the schizophrenogenic mother again. <bookmark mark='d'/> Since then, twin studies have shown high "
            "heritability. Autism is developmental. It isn't caused by parenting."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, s in zip("abcd", steps):
                vo.wait_until(m)
                self.play(FadeIn(s, shift=RIGHT * 0.15))
        self.clear_scene()

    def vaccines(self):
        head = heading(r"A fraud, \ and 657{,}461 children")
        rows = rows_of([
            (r"Wakefield and colleagues, \ 1998: \ a case series of 12 children suggested the measles, \ mumps and "
             r"rubella vaccine might cause autism", AUTH),
            (r"investigations found misconduct; \ the \emph{Lancet} retracted the paper in 2010, \ and Wakefield was "
             r"struck off the UK medical register", WHITE),
            (r"Hviid and colleagues, \ 2019: \ 657{,}461 Danish children followed for years: \ no higher rate of "
             r"autism after vaccination", GOOD),
            (r"meanwhile vaccination fell in several countries, \ and measles came back: \ Part 4's lesson, \ with "
             r"children paying for it", YOU),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        tag = published_tag(r"Wakefield et al.\ (1998), \ retracted; \ Hviid et al.\ (2019)")
        with self.voiceover(
            "Then came a fraud. <bookmark mark='a'/> In 1998 Andrew Wakefield and colleagues published a case series "
            "of twelve children that suggested the measles, mumps and rubella vaccine might cause autism. "
            "<bookmark mark='b'/> Investigations found misconduct. The Lancet retracted the paper in 2010, and "
            "Wakefield was struck off the UK medical register. <bookmark mark='c'/> In 2019 Anders Hviid and "
            "colleagues followed six hundred and fifty-seven thousand, four hundred and sixty-one Danish children for "
            "years. There was no higher rate of autism after vaccination. <bookmark mark='d'/> Meanwhile vaccination "
            "fell in several countries, and measles came back. It's Part 4's lesson, with children paying for it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def priors(self):
        d = load("mask")
        head = heading(r"A world too real?")
        A = axes([0, 20], [0, 1.2], x_length=5.6, y_length=3.0, xticks=[0, 5, 10, 15, 20], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"precision of the prior",
                 ylabel=r"expected error", center=[-3.3, 0.5, 0], font_size=13)
        typ = curve(A.ax, d["grid"], d["mse95"], GOOD, stroke_width=3)
        odd = curve(A.ax, d["grid"], d["mse60"], AUTH, stroke_width=3)
        b1 = Dot(A.ax.c2p(d["best95"], float(np.min(d["mse95"]))), radius=0.07, color=GOOD)
        b2 = Dot(A.ax.c2p(d["best60"], float(np.min(d["mse60"]))), radius=0.07, color=AUTH)
        key = VGroup(label(r"the world matches the prior 95\% of the time", font_size=13, color=GOOD),
                     label(r"only 60\% of the time", font_size=13, color=AUTH)).arrange(DOWN, aligned_edge=LEFT,
                                                                                      buff=0.08)
        key.next_to(A, DOWN, buff=0.3)
        rows = rows_of([
            (r"Part 30: \ autistic children often find false-belief tasks harder; \ that account explains the social "
             r"side, \ not the senses", WHITE),
            (r"Pellicano and Burr, \ 2012: \ perception in autism leans less on priors, \ so the world arrives "
             r"``too real'': \ fewer illusions, \ more detail, \ more overload", SYMP),
            (rf"Psyche: \ how strong a prior should be depends on the world; \ the best precision is "
             rf"{d['best95']:.1f} when the world is typical, \ {d['best60']:.1f} when it is not", MODEL),
            (r"a weaker prior is a different trade-off, \ not simply a deficit", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Pellicano \& Burr (2012)")
        with self.voiceover(
            "What models describe autism? <bookmark mark='a'/> In Part 30, autistic children often found "
            "false-belief tasks harder. That account explains the social side, not the senses. "
            "<bookmark mark='b'/> In 2012 Elizabeth Pellicano and David Burr proposed that perception in autism "
            "leans less on priors, so the world arrives too real: fewer illusions, more detail, more overload. "
            "<bookmark mark='c'/> Psyche shows why that's a trade-off. How strong a prior should be depends on the "
            "world. When the world matches the prior ninety-five percent of the time, the best prior is strong. When "
            "it matches only sixty percent of the time, the best prior is weak. <bookmark mark='d'/> A weaker prior "
            "is a different trade-off, not simply a deficit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(typ), Create(odd), FadeIn(b1), FadeIn(b2), FadeIn(key), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def prevalence(self):
        head = heading(r"More diagnoses")
        A = axes([1998, 2022], [0, 32], x_length=5.4, y_length=2.8, xticks=[2000, 2010, 2020], yticks=[0, 10, 20, 30],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"surveillance year",
                 ylabel=r"per 1{,}000 children aged 8", center=[-3.4, 0.6, 0], font_size=13)
        yrs = np.array([2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020])
        rate = np.array([6.7, 6.6, 8.0, 9.0, 11.3, 14.7, 14.5, 16.8, 18.5, 23.0, 27.6])
        line = curve(A.ax, yrs, rate, PERSON, stroke_width=3)
        dots = scatter(A.ax, yrs, rate, PERSON, radius=0.06)
        lm = label(r"CDC's network, \ reported rates", font_size=13, color=GREY_B).next_to(A, DOWN, buff=0.3)
        rows = rows_of([
            (r"the US surveillance network found about 1 in 150 eight-year-olds in 2000, \ and about 1 in 36 in 2020", WHITE),
            (r"most of the rise is in diagnosis: \ broader criteria, \ the single autism spectrum of 2013, \ "
             r"awareness, \ services, \ and children once given other labels", MODEL),
            (r"whether the true rate has risen at all, \ and by how much, \ is debated", GREY_A),
            (r"neurodiversity: \ autism as a difference with both disabilities and strengths; \ many autistic adults "
             r"prefer ``autistic person'', \ and this part follows them", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"CDC ADDM (2023)")
        with self.voiceover(
            "Diagnoses have risen sharply. <bookmark mark='a'/> The American surveillance network found about one in "
            "a hundred and fifty eight-year-olds in 2000, and about one in thirty-six in 2020. "
            "<bookmark mark='b'/> Most of the rise is in diagnosis: broader criteria, the single autism spectrum of "
            "2013, awareness, services, and children who once received other labels. <bookmark mark='c'/> Whether "
            "the true rate has risen at all, and by how much, is debated. <bookmark mark='d'/> Neurodiversity "
            "describes autism as a difference with both disabilities and strengths. Many autistic adults prefer to "
            "be called autistic people, and this part follows them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(lm))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(line), FadeIn(dots), run_time=2.0)
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def facilitated(self):
        head = heading(r"Whose words?")
        tf = VGroup(little_person(0.8, color=PERSON), little_person(0.8, color=SYMP)).arrange(RIGHT, buff=0.25)
        tf.move_to([-4.6, 0.7, 0])
        p1 = VGroup(Square(0.6, color=GOOD), label(r"key", font_size=14, color=GOOD)).arrange(DOWN, buff=0.1)
        p2 = VGroup(Square(0.6, color=AUTH), label(r"cup", font_size=14, color=AUTH)).arrange(DOWN, buff=0.1)
        p1.next_to(tf[0], UP, buff=0.3)
        p2.next_to(tf[1], UP, buff=0.3)
        lab = VGroup(label(r"typist sees", font_size=13, color=GREY_A).next_to(p1, LEFT, buff=0.1),
                     label(r"facilitator sees", font_size=13, color=GREY_A).next_to(p2, RIGHT, buff=0.1))
        typed = label(r"typed: \ CUP", font_size=20, color=AUTH).next_to(tf, DOWN, buff=0.35)
        rows = rows_of([
            (r"facilitated communication: \ a helper steadies the hand of a non-speaking person, \ who types "
             r"fluent messages; \ Biklen, \ 1990, \ brought it to the US", WHITE),
            (r"Wheeler and colleagues, \ 1993: \ show the typist and the helper different pictures; \ the answers "
             r"named what the helper saw", AUTH),
            (r"the helpers were moving the hands without knowing it, \ the ideomotor effect; \ false allegations of "
             r"abuse had followed", SYMP),
            (r"the Ledger: \ failed; \ a blind test settles what sincere conviction cannot", YOU),
        ], 6.4, 19, 0.36).move_to([3.2, -0.2, 0])
        tag = published_tag(r"Biklen (1990); \ Wheeler et al.\ (1993)")
        with self.voiceover(
            "Last, a method that failed a simple test. <bookmark mark='a'/> In facilitated communication, a helper "
            "steadies the hand of a non-speaking person, who types fluent messages. Douglas Biklen brought it to the "
            "United States in 1990, and families welcomed it. <bookmark mark='b'/> In 1993 Douglas Wheeler and "
            "colleagues showed the typist and the helper different pictures. The answers named what the helper "
            "saw. <bookmark mark='c'/> The helpers were moving the hands without knowing it, the ideomotor effect. "
            "False allegations of abuse had already followed. <bookmark mark='d'/> The Ledger marks it failed. A "
            "blind test settles what sincere conviction can't."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tf))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(p1), FadeIn(p2), FadeIn(lab))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(typed))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
