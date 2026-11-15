from __future__ import annotations

from videos.psychology.psych27.common import *  # noqa: F403


class Adversarial(VoiceoverScene):
    def construct(self):
        self.card()
        self.design()
        self.results()

    def card(self):
        card = chapter_card(9, r"An adversarial collaboration", r"Can rival theories agree on how to lose?",
                            lit={2021: r"Melloni et al.", 2023: r"first results", 2025: r"Cogitate Consortium"},
                            part=PART, scale=("mind", "brain"), marr=("what",))
        with self.voiceover("Chapter nine. An adversarial collaboration."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def design(self):
        head = heading(r"Agreeing in advance on how to lose")
        rows = rows_of([
            (r"the theories' own authors agreed on experiments, \ and on which results would count against each "
             r"theory, \ before any data", WHITE),
            (r"visual stimuli \ (faces, \ objects, \ letters, \ false fonts) \ shown for half a second to a second "
             r"and a half, \ some relevant to the task, \ some not", SEEN),
            (r"three methods in several laboratories: \ fMRI, \ MEG, \ and recordings from electrodes in epilepsy "
             r"patients", MODEL),
        ], 12.0, 24, 0.36).move_to([0, 1.3, 0])
        gnw = VGroup(label(r"the workspace predicted", font_size=24, color=GNW),
                     wrapped_label(r"ignition in prefrontal cortex at the stimulus's onset and again at its offset; \ "
                                   r"the stimulus's content decodable there", 5.4, 21, WHITE)).arrange(DOWN, buff=0.2)
        iit = VGroup(label(r"integrated information predicted", font_size=24, color=IIT),
                     wrapped_label(r"activity in posterior cortex sustained for as long as the stimulus is seen, \ "
                                   r"and sustained synchrony within it", 5.4, 21, WHITE)).arrange(DOWN, buff=0.2)
        VGroup(gnw, iit).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to([0, -1.7, 0])
        tag = published_tag(r"Melloni et al.\ (2021); \ Cogitate Consortium (2025)")
        with self.voiceover(
            "In 2019 the Templeton World Charity Foundation funded something unusual. <bookmark mark='a'/> The "
            "authors of the workspace and integrated information theories agreed, in advance and in writing, on a "
            "set of experiments and on which results would count against each theory. Lucia Melloni and colleagues "
            "published the plan in 2021. <bookmark mark='b'/> People watched faces, objects, letters and meaningless "
            "symbols, shown for half a second up to a second and a half, some relevant to their task and some not. "
            "<bookmark mark='c'/> Several laboratories recorded them with fMRI, with MEG, and with electrodes "
            "implanted in patients being treated for epilepsy. <bookmark mark='d'/> The workspace predicted ignition "
            "in prefrontal cortex when a stimulus appeared and again when it disappeared, with its content readable "
            "there. Integrated information predicted activity in the back of the brain sustained for as long as the "
            "stimulus was seen, and sustained synchrony within it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(gnw), FadeIn(iit))
        self.clear_scene()

    def results(self):
        head = heading(r"What each theory got wrong")
        g = VGroup(label(r"global workspace", font_size=26, color=GNW),
                   wrapped_label(r"no ignition in prefrontal cortex when the stimulus went off; \ some content "
                                 r"\ (category) \ was readable there, \ some \ (orientation) \ was not", 5.6, 22,
                                 WHITE)).arrange(DOWN, buff=0.25)
        i = VGroup(label(r"integrated information", font_size=26, color=IIT),
                   wrapped_label(r"content was sustained in posterior cortex, \ as predicted; \ but the sustained "
                                 r"synchrony within it was not found", 5.6, 22, WHITE)).arrange(DOWN, buff=0.25)
        VGroup(g, i).arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to([0, 1.0, 0])
        rows = rows_of([
            (r"first results announced in 2023; \ published in \emph{Nature} in 2025", GREY_A),
            (r"neither theory won; \ both lost something they had staked in advance", LOST),
            (r"the method is the result: \ theories made to risk being wrong, \ on terms they set themselves", MODEL),
        ], 12.0, 24, 0.32).move_to([0, -1.9, 0])
        tag = published_tag(r"Cogitate Consortium (2025)")
        with self.voiceover(
            "The first results were announced in 2023, and the full paper appeared in Nature in 2025. "
            "<bookmark mark='a'/> For the workspace, there was no burst of ignition in prefrontal cortex when the "
            "stimulus went off, and while some of its content, like its category, could be read out there, some, "
            "like its orientation, could not. <bookmark mark='b'/> For integrated information, content was sustained "
            "in the back of the brain, as predicted, but the sustained synchrony within it was not found. "
            "<bookmark mark='c'/> So neither theory won, and each lost something it had staked in advance. "
            "<bookmark mark='d'/> The lasting result may be the method itself: theories made to risk being wrong, on "
            "terms they set themselves. More such collaborations are under way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(g))
            vo.wait_until("b")
            self.play(FadeIn(i))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
