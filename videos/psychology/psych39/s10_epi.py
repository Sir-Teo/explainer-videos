from __future__ import annotations

from videos.psychology.psych39.common import *  # noqa: F403


class Epi(VoiceoverScene):
    def construct(self):
        self.card()
        self.prevalence()
        self.manual()
        self.eating()
        self.personality()
        self.gap()

    def card(self):
        card = chapter_card(9, r"How common?", r"How many people, \ and how many treated?",
                            lit={2004: r"Kohn et al.", 2005: r"Kessler et al.", 2017: r"Jorm et al."}, part=PART,
                            scale=("group",), marr=("what",))
        with self.voiceover("Chapter nine. How common?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def prevalence(self):
        head = heading(r"Nearly half, \ starting young")
        A = axes([0, 75], [0, 11], x_length=5.0, y_length=2.6, xticks=[0, 15, 30, 45, 60, 75], yticks=None,
                 xfmt=lambda v: f"{v:.0f}", xlabel=r"age", center=[-3.4, -0.6, 0], font_size=14)
        meds = [(r"anxiety", 11, SYMP), (r"impulse control", 11, PERSON), (r"substance use", 20, AUTH),
                (r"mood", 30, MODEL)]
        marks = VGroup()
        for k, (n, age, c) in enumerate(meds):
            y = 9 - 2.4 * k
            marks.add(VGroup(Dot(A.ax.c2p(age, y), radius=0.09, color=c),
                             label(rf"{n}: \ {age}", font_size=14, color=c).next_to(A.ax.c2p(age, y), RIGHT,
                                                                                     buff=0.12)))
        half = DashedLine(A.ax.c2p(14, 0), A.ax.c2p(14, 10.5), color=GREY_B)
        lh = label(r"half of all cases by 14", font_size=13, color=GREY_B).next_to(A.ax.c2p(14, 10.5), UP,
                                                                                  buff=0.05)
        ml = label(r"median age at onset", font_size=14, color=GREY_A).next_to(A, UP, buff=0.55)
        rows = rows_of([
            (r"Kessler and colleagues, \ 2005: \ the National Comorbidity Survey Replication, \ a representative "
             r"sample of US adults interviewed in person", WHITE),
            (r"46.4\% had met the criteria for at least one disorder at some point in their lives", PERSON),
            (r"half of all lifetime cases had begun by age 14, \ three quarters by 24", SYMP),
            (r"lifetime prevalence depends on the thresholds of chapter six, \ and on remembering: \ follow-up "
             r"studies that ask repeatedly find even higher rates", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Kessler et al.\ (2005)")
        with self.voiceover(
            "How common are disorders? <bookmark mark='a'/> In 2005 Ronald Kessler and colleagues reported the "
            "National Comorbidity Survey Replication, a representative sample of American adults interviewed in "
            "person. <bookmark mark='b'/> Forty-six percent had met the criteria for at least one disorder at some "
            "point in their lives. <bookmark mark='c'/> Half of all lifetime cases had begun by age fourteen, three "
            "quarters by twenty-four. Anxiety typically starts in childhood, mood disorders around thirty. "
            "<bookmark mark='d'/> Lifetime prevalence depends on the thresholds of chapter six, and on remembering. "
            "Studies that follow people and ask repeatedly find even higher rates."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(ml))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), LaggedStart(*[FadeIn(m_) for m_ in marks], lag_ratio=0.4), Create(half),
                      FadeIn(lh))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def manual(self):
        head = heading(r"A map of the manual")
        groups = [
            (r"neurodevelopmental", r"Part 41", CROWD), (r"schizophrenia spectrum", r"Part 41", CROWD),
            (r"bipolar", r"Part 40", MODEL), (r"depressive", r"Part 40", MODEL), (r"anxiety", r"Part 40", MODEL),
            (r"obsessive-compulsive", r"Part 40", MODEL), (r"trauma- and stressor-related", r"Part 40", MODEL),
            (r"dissociative", r"in passing", None), (r"somatic symptom", r"in passing", None),
            (r"feeding and eating", r"this chapter", GOOD), (r"sleep-wake", r"Part 10", SYMP),
            (r"substance-related and addictive", r"Part 41", CROWD), (r"neurocognitive", r"Part 31: \ dementia", SYMP),
            (r"personality", r"this chapter; \ Part 42", GOOD),
        ]
        w, h, gx, gy, cols = 2.42, 1.12, 0.14, 0.16, 5
        cards = VGroup()
        for k, (name, where, c) in enumerate(groups):
            r, j = divmod(k, cols)
            n_row = cols if r < len(groups) // cols else len(groups) - cols * (len(groups) // cols)
            x0 = -(n_row * w + (n_row - 1) * gx) / 2 + w / 2
            box = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=GREY_D, stroke_width=1.8,
                                   fill_color=GREY_E, fill_opacity=0.25)
            nm = wrapped_label(name, w - 0.25, 19, WHITE)
            wh = label(where, font_size=17, color=c or GREY_B)
            inner = VGroup(nm, wh).arrange(DOWN, buff=0.1)
            if inner.height > h - 0.12:
                inner.height = h - 0.12
            card_ = VGroup(box, inner.move_to(box))
            card_.move_to([x0 + j * (w + gx), 1.55 - r * (h + gy), 0])
            card_.box, card_.where, card_.accent = box, wh, c
            cards.add(card_)
        src = label(r"the major groups of DSM-5-TR and ICD-11, \ both 2022", font_size=19, color=GREY_A)
        src.next_to(cards, DOWN, buff=0.35)
        treated = [cd for cd in cards if cd.accent is not None]
        passing = [cd for cd in cards if cd.accent is None]
        for cd in cards:
            cd.where.set_opacity(0)
        tag = published_tag(r"APA, \ DSM-5-TR (2022); \ WHO, \ ICD-11 (2022)")
        with self.voiceover(
            "Forty-six percent with a disorder; but which disorders? <bookmark mark='a'/> The two manuals in use, the "
            "American DSM-5-TR and the World Health Organization's ICD-11, both from 2022, sort mental disorders into "
            "about twenty groups, and their main groups largely match. Here are the major ones. "
            "<bookmark mark='b'/> This series treats many of them in depth. Anxiety, obsessive-compulsive and "
            "trauma-related disorders, depression and bipolar disorder are Part 40. Psychosis, addiction, autism "
            "and ADHD are Part 41. Dementia is in Part 31, and sleep in Part 10. <bookmark mark='c'/> Some it "
            "touches only in passing, the dissociative and somatic symptom disorders among them. Saying so is part "
            "of the map. <bookmark mark='d'/> And two groups get their own pages in this chapter: the eating "
            "disorders, and the personality disorders."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(cd, shift=UP * 0.1) for cd in cards], lag_ratio=0.08), FadeIn(src),
                      run_time=2.2)
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(cd.box.animate.set_stroke(cd.accent, width=2.4)
                                                   .set_fill(cd.accent, opacity=0.14),
                                                   cd.where.animate.set_opacity(1))
                                    for cd in treated if cd.accent != GOOD], lag_ratio=0.15), run_time=2.4)
            vo.wait_until("c")
            self.play(*[cd.where.animate.set_opacity(1) for cd in passing],
                      *[cd.box.animate.set_stroke(GREY_C, width=1.8).set_fill(opacity=0.05) for cd in passing])
            vo.wait_until("d")
            good = [cd for cd in treated if cd.accent == GOOD]
            self.play(*[cd.box.animate.set_stroke(GOOD, width=3).set_fill(GOOD, opacity=0.18) for cd in good],
                      *[cd.where.animate.set_opacity(1) for cd in good])
            self.play(*[Indicate(cd, color=GOOD, scale_factor=1.06) for cd in good])
        self.clear_scene()

    def eating(self):
        head = heading(r"The eating disorders")
        A = axes([-0.6, 2.6], [0, 7], x_length=4.4, y_length=3.0, xticks=None, yticks=[0, 1, 2, 4, 6],
                 yfmt=lambda v: f"{v:g}", ylabel=r"deaths, \ relative to others of the same age and sex",
                 center=[-3.5, -0.3, 0], font_size=17)
        vals = [1.0, 1.93, 5.86]
        cols = [GREY_B, SYMP, AUTH]
        b = bars(A.ax, [0, 1, 2], vals, cols, width=0.6)
        names = VGroup(*[wrapped_label(t, 1.35, 17, c).next_to(A.ax.c2p(x, 0), DOWN, buff=0.15)
                         for x, t, c in zip([0, 1, 2], [r"same age and sex", r"bulimia nervosa", r"anorexia nervosa"],
                                            cols)])
        tops = VGroup(*[label(rf"{v:.2f}".rstrip("0").rstrip("."), font_size=19, color=c)
                        .next_to(A.ax.c2p(x, v), UP, buff=0.08) for x, v, c in zip([0, 1, 2], vals, cols)])
        ref = DashedLine(A.ax.c2p(-0.6, 1), A.ax.c2p(2.6, 1), color=GREY_C, stroke_width=1.5)
        cards = point_cards([
            (r"Less common than depression", r"lifetime: \ anorexia under 1\% of women, \ binge-eating disorder "
             r"about 3.5\%; \ lower in men \ (Hudson et al., \ 2007)", SYMP),
            (r"Treatments with trials", r"adolescents with anorexia: \ family-based treatment beat individual "
             r"therapy at follow-up \ (Lock et al., \ 2010); \ adults with bulimia or binge eating: \ CBT, \ "
             r"and Fairburn's CBT-E", GOOD),
        ], width=6.3, cols=1, font_size=19)
        cards.move_to([3.45, -0.25, 0])
        tag = published_tag(r"Hudson et al.\ (2007); \ Arcelus et al.\ (2011); \ Lock et al.\ (2010)")
        with self.voiceover(
            "The eating disorders first. <bookmark mark='a'/> Anorexia nervosa, bulimia nervosa and binge-eating "
            "disorder are less common than depression or anxiety. In the American comorbidity survey, James Hudson "
            "and colleagues put the lifetime prevalence of anorexia at under one percent of women, and of "
            "binge-eating disorder at about three and a half percent, with lower rates in men. "
            "<bookmark mark='b'/> But anorexia is among the most dangerous of all mental disorders. In 2011 Jon "
            "Arcelus and colleagues pooled thirty-six studies. People with anorexia died at almost six times the "
            "rate expected for their age and sex, and about one death in five was by suicide. "
            "<bookmark mark='c'/> There are treatments with trial evidence. For adolescents with anorexia, in a "
            "trial reported by James Lock and colleagues in 2010, family-based treatment, in which parents are "
            "helped to take charge of meals, led to more full remissions at follow-up than individual therapy did. "
            "For adults with bulimia or binge-eating disorder, cognitive behavioural therapy has the most support, "
            "and Christopher Fairburn's enhanced version, CBT-E, was built to treat the eating disorders together. "
            "<bookmark mark='d'/> Early help matters, and many people recover. The personality disorders raise a "
            "different question: what enduring means."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cards.cards[0], shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(A), Create(ref), FadeIn(names), *[GrowFromEdge(x, DOWN) for x in b], FadeIn(tops),
                      run_time=1.8)
            vo.wait_until("c")
            self.play(FadeIn(cards.cards[1], shift=UP * 0.15))
            vo.wait_until("d")
            self.play(Indicate(cards.cards[1].title, color=GOOD))
        self.clear_scene()

    def personality(self):
        head = heading(r"The personality disorders")
        steps = [(r"none", GREY_C), (r"difficulty", SYMP), (r"mild", PERSON), (r"moderate", AUTH),
                 (r"severe", LOST)]
        sev = VGroup()
        for k, (t, c) in enumerate(steps):
            r = Rectangle(width=1.12, height=0.62, stroke_width=1.5, stroke_color=c, fill_color=c,
                          fill_opacity=0.12 + 0.12 * k)
            sev.add(VGroup(r, label(t, font_size=18, color=WHITE).move_to(r)))
        sev.arrange(RIGHT, buff=0.04).move_to([-3.5, 1.35, 0])
        sev_l = label(r"ICD-11: \ one diagnosis, \ graded by severity", font_size=19, color=GREY_A)
        sev_l.next_to(sev, UP, buff=0.18)
        doms = VGroup(*[word_chip(t, color=MODEL, font_size=17, width=2.6) for t in
                        [r"negative affectivity", r"detachment", r"dissociality", r"disinhibition", r"anankastia"]])
        doms.arrange_in_grid(rows=3, cols=2, buff=(0.15, 0.14)).next_to(sev, DOWN, buff=0.45)
        doms_l = label(r"five trait domains, \ and a borderline pattern", font_size=19, color=GREY_A)
        doms_l.next_to(doms, DOWN, buff=0.2)
        dsm = label(r"DSM-5-TR still lists ten types", font_size=19, color=GREY_B).move_to([-3.5, -2.85, 0])
        A = axes([0, 100], [-0.6, 1.6], x_length=4.6, y_length=1.8, xticks=[0, 50, 100], yticks=None,
                 xfmt=lambda v: f"{v:.0f}\\%", center=[3.5, 0.2, 0], font_size=17)
        hb = VGroup()
        for y, v, c, t in [(1, 93, GOOD, r"a remission lasting 2 years or more"),
                           (0, 50, PERSON, r"also good work and social lives")]:
            lo_, hi_ = A.ax.c2p(0, y), A.ax.c2p(v, y)
            bar = Rectangle(width=hi_[0] - lo_[0], height=0.42, stroke_width=0, fill_color=c, fill_opacity=0.85)
            bar.move_to([(lo_[0] + hi_[0]) / 2, lo_[1], 0])
            hb.add(VGroup(bar, label(rf"{v}\%", font_size=19, color=c).next_to(bar, RIGHT, buff=0.1),
                          label(t, font_size=18, color=WHITE).next_to(bar, UP, buff=0.08).align_to(bar, LEFT)))
        al = wrapped_label(r"borderline personality disorder, \ followed for ten years \ (Zanarini et al., \ 2010)",
                           5.6, 19, GREY_A).next_to(A, UP, buff=0.5)
        foot = wrapped_label(r"the therapy built for it: \ Part 42", 5.6, 19, CARE).next_to(A, DOWN, buff=0.45)
        tag = published_tag(r"WHO, \ ICD-11 (2022); \ Zanarini et al.\ (2010)")
        with self.voiceover(
            "The personality disorders are the other group. <bookmark mark='a'/> The manuals define them as "
            "enduring patterns of experience and behaviour that depart from what a person's culture expects, begin "
            "by early adulthood, and cause distress or impairment. The American manual still lists ten types. "
            "<bookmark mark='b'/> ICD-11 dropped the types. It keeps one diagnosis, graded by severity, described by "
            "five trait domains, with a borderline pattern that can be noted. It's chapter six's dimensions, adopted "
            "by a manual. <bookmark mark='c'/> And enduring proved too strong a word. Mary Zanarini and colleagues "
            "followed patients with borderline personality disorder for ten years. Ninety-three percent had a "
            "remission of symptoms that lasted at least two years. <bookmark mark='d'/> Only about half also "
            "recovered good working and social lives. <bookmark mark='e'/> The therapy built for borderline "
            "personality disorder comes in Part 42. And like most disorders on the map, these often go untreated."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(dsm))
            vo.wait_until("b")
            self.play(FadeIn(sev_l), LaggedStart(*[FadeIn(x, shift=RIGHT * 0.1) for x in sev], lag_ratio=0.2),
                      run_time=1.4)
            self.play(LaggedStart(*[FadeIn(x) for x in doms], lag_ratio=0.15), FadeIn(doms_l), run_time=1.4)
            vo.wait_until("c")
            self.play(FadeIn(al), FadeIn(A), GrowFromEdge(hb[0][0], LEFT), FadeIn(hb[0][1:]))
            vo.wait_until("d")
            self.play(GrowFromEdge(hb[1][0], LEFT), FadeIn(hb[1][1:]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def gap(self):
        head = heading(r"The treatment gap, \ and a paradox")
        A = axes([-0.6, 1.6], [0, 100], x_length=3.6, y_length=2.6, xticks=None, yticks=[0, 50, 100],
                 yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"untreated", center=[-4.0, -0.4, 0], font_size=14)
        b = bars(A.ax, [0, 1], [56.3, 78.1], [MODEL, AUTH], width=0.6)
        names = VGroup(wrapped_label(r"major depression", 1.6, 14, MODEL).next_to(A.ax.c2p(0, 0), DOWN, buff=0.15),
                       wrapped_label(r"alcohol use disorders", 1.6, 14, AUTH).next_to(A.ax.c2p(1, 0), DOWN,
                                                                                       buff=0.15))
        tops = VGroup(label(r"56\%", font_size=16, color=MODEL).next_to(A.ax.c2p(0, 56.3), UP, buff=0.08),
                      label(r"78\%", font_size=16, color=AUTH).next_to(A.ax.c2p(1, 78.1), UP, buff=0.08))
        rows = rows_of([
            (r"Kohn and colleagues, \ 2004: \ across studies worldwide, \ 56\% of people with major depression and "
             r"78\% with alcohol use disorders had received no treatment", WHITE),
            (r"the gap is widest in low- and middle-income countries", PERSON),
            (r"Jorm, \ Patten, \ Brugha and Mojtabai, \ 2017: \ in Australia, \ Canada, \ England and the US, \ "
             r"treatment rose sharply, \ especially antidepressants, \ but the prevalence of anxiety and "
             r"depression did not fall", AUTH),
            (r"possible reasons: \ treatment that reaches the wrong people, \ or works less well in practice than "
             r"in trials; \ Part 42 weighs the evidence", YOU),
        ], 6.4, 19, 0.36).move_to([3.2, -0.2, 0])
        tag = published_tag(r"Kohn et al.\ (2004); \ Jorm et al.\ (2017)")
        with self.voiceover(
            "Most people with a disorder are never treated. <bookmark mark='a'/> In 2004 Robert Kohn and colleagues "
            "pooled studies worldwide. Fifty-six percent of people with major depression, and seventy-eight percent "
            "with alcohol use disorders, had received no treatment. <bookmark mark='b'/> The gap is widest in low- "
            "and middle-income countries. <bookmark mark='c'/> But here's a paradox. In 2017 Anthony Jorm and "
            "colleagues looked at Australia, Canada, England and the United States. Treatment had risen sharply, "
            "antidepressants especially, but the prevalence of anxiety and depression hadn't fallen. "
            "<bookmark mark='d'/> Possible reasons: treatment that reaches the wrong people, or works less well in "
            "practice than in trials. Part 42 weighs the evidence."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), *[GrowFromEdge(x, DOWN) for x in b], FadeIn(tops))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
