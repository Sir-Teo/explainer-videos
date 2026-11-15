from __future__ import annotations

from videos.psychology.psych29.common import *  # noqa: F403


class Constructed(VoiceoverScene):
    def construct(self):
        self.card()
        self.theory()
        self.variation()
        self.cases()

    def card(self):
        card = chapter_card(5, r"Constructed emotion", r"Are anger, fear and joy natural kinds?",
                            lit={1980: r"Russell", 2003: r"core affect", 2017: r"Barrett"},
                            part=PART, scale=("brain", "mind", "culture"), marr=("what", "how"))
        with self.voiceover("Chapter five. Constructed emotion."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def theory(self):
        head = heading(r"Two ingredients and a concept")
        core = Circle(radius=1.3, color=BODY, fill_opacity=0.08).move_to([-4.2, 0.2, 0])
        ax_v = Arrow(core.get_left(), core.get_right(), buff=0, color=PLEAS, stroke_width=3)
        ax_a = Arrow(core.get_bottom(), core.get_top(), buff=0, color=BODY, stroke_width=3)
        cl = label(r"core affect", font_size=20, color=BODY).next_to(core, DOWN, buff=0.2)
        plus = label(r"$+$", font_size=48).move_to([-2.2, 0.2, 0])
        concept = word_chip(r"a concept: \ ``anger''", color=COG, font_size=22).move_to([-0.3, 0.2, 0])
        rows = rows_of([
            (r"core affect: \ a continuous feeling of pleasantness and arousal, \ always present, \ the map of "
             r"chapter four", BODY),
            (r"concepts, \ learned in a culture: \ the brain categorizes core affect in context, \ as it "
             r"categorizes colour or shape", COG),
            (r"anger is then not one circuit or one face, \ but a population of varied instances grouped by a "
             r"goal: \ like ``things to take on a picnic''", FACE),
            (r"Barrett, \ 2017: \ \emph{How Emotions Are Made}", WHITE),
        ], 5.0, 21, 0.32).move_to([4.0, -0.1, 0])
        tag = published_tag(r"Russell (2003); \ Barrett (2017)")
        with self.voiceover(
            "The strongest alternative to basic emotions is that they are built. <bookmark mark='a'/> On James "
            "Russell's and Lisa Feldman Barrett's account, the brain is always producing core affect, a continuous "
            "feeling of pleasantness and arousal: the map of chapter four. <bookmark mark='b'/> On top of it, the "
            "brain uses concepts learned in a culture to categorize that affect in context, the way it categorizes "
            "colours and shapes. <bookmark mark='c'/> Anger, then, is not one circuit or one face, but a population "
            "of varied instances, grouped by what they are for, like the category of things to take on a picnic. "
            "<bookmark mark='d'/> Barrett set this out in 2017 in How Emotions Are Made."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(core), GrowArrow(ax_v), GrowArrow(ax_a), FadeIn(cl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(plus), FadeIn(concept), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def variation(self):
        head = heading(r"Variation within a category")
        faces = VGroup(*[face(v, a, color=UNPL, radius=0.42) for v, a in
                         ((-0.9, 0.6), (-0.5, -0.3), (-0.2, 0.2), (0.3, 0.4), (-0.9, 0.95), (-0.4, -0.7))])
        faces.arrange_in_grid(rows=2, cols=3, buff=(0.45, 0.45)).move_to([-3.6, 0.3, 0])
        fl = wrapped_label(r"six faces of people who reported anger \ (schematic)", 4.4, 17, GREY_B).next_to(
            faces, DOWN, buff=0.25)
        rows = rows_of([
            (r"within a category, \ faces, \ bodily changes and brain activity vary widely", WHITE),
            (r"meta-analyses of the autonomic nervous system find heart rate and skin conductance patterns that "
             r"overlap between emotions more than they separate them", BODY),
            (r"meta-analyses of brain imaging find no region specific to one emotion; \ the amygdala responds to "
             r"many things that are novel or relevant", FEAR),
            (r"pattern classifiers can tell emotions apart above chance in a given study, \ with patterns that "
             r"spread across the brain and change between studies", MODEL),
        ], 5.8, 21, 0.32).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Siegel et al.\ (2018); \ Lindquist et al.\ (2012)")
        with self.voiceover(
            "The evidence for construction is variation. <bookmark mark='a'/> Within one emotion category, faces, "
            "bodily changes and brain activity vary widely. <bookmark mark='b'/> A 2018 meta-analysis of the "
            "autonomic nervous system, by Erika Siegel and colleagues, found patterns of heart rate and skin "
            "conductance that overlap between emotions more than they separate them. <bookmark mark='c'/> A 2012 "
            "meta-analysis of brain imaging by Kristen Lindquist and colleagues found no region specific to one "
            "emotion; the amygdala, for instance, responds to many things that are novel or relevant, not only "
            "to threats. <bookmark mark='d'/> Pattern classifiers can tell emotions apart above chance within a "
            "given study, but with patterns spread across the brain that change from study to study."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(faces), FadeIn(fl))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def cases(self):
        head = heading(r"The best case for each side")
        left = VGroup(label(r"basic emotions", font_size=26, color=FACE), rows_of([
            (r"some expressions are recognized above chance across very different cultures", WHITE),
            (r"some responses are fast, \ automatic, \ and shared with other mammals: \ startle, \ freezing, \ "
             r"disgust's gape", WHITE),
            (r"infants show distinct facial movements early", WHITE),
        ], 5.6, 21, 0.25)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        right = VGroup(label(r"constructed emotion", font_size=26, color=COG), rows_of([
            (r"variation within a category is the rule, \ not noise", WHITE),
            (r"agreement falls when the method stops supplying the categories", WHITE),
            (r"words and culture change what people perceive and report", WHITE),
        ], 5.6, 21, 0.25)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        VGroup(left, right).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to([0, 0.4, 0])
        foot = wrapped_label(r"a middle view: \ evolved families of responses, \ with large variation, \ categorized "
                             r"by concepts; \ the argument is now over how much of each", 12.2, 23, PLEAS).to_edge(
            DOWN, buff=0.75)
        with self.voiceover(
            "Here is the best case for each side. <bookmark mark='a'/> For basic emotions: some expressions are "
            "recognized above chance across very different cultures; some responses are fast, automatic and shared "
            "with other mammals, like the startle, freezing, and the gape of disgust; and infants show distinct "
            "facial movements early. <bookmark mark='b'/> For construction: variation within a category is the "
            "rule, not noise; agreement falls when the method stops supplying the categories; and words and culture "
            "change what people perceive and report. <bookmark mark='c'/> Many researchers now hold a middle view: "
            "evolved families of responses, with large variation, categorized by learned concepts. The argument is "
            "over how much of each."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
