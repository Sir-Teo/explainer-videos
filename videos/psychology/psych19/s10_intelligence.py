from __future__ import annotations

from videos.psychology.psych19.common import *  # noqa: F403


class Intelligence(VoiceoverScene):
    def construct(self):
        self.card()
        self.complex_span()
        self.correlation()

    def card(self):
        card = chapter_card(9, r"Working memory and reasoning", r"Does holding more help you think better?",
                            lit={1980: r"Daneman \& Carpenter", 2005: r"Kane et al."}, part=PART,
                            scale=("mind", "person"), marr=("what",))
        with self.voiceover("Chapter nine. Working memory and reasoning."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def complex_span(self):
        p = archive.DANEMAN_CARPENTER_1980.data
        head = heading(r"Complex span: \ store while you process")
        strip = trial_strip([
            (r"is it true?", label(r"$(8 \div 2) - 1 = 1$", font_size=34), ""),
            (r"remember this letter", label(r"F", font_size=48, color=MEM), ""),
            (r"is it true?", label(r"$(3 \times 2) + 2 = 8$", font_size=34), ""),
            (r"remember this letter", label(r"Q", font_size=48, color=MEM), ""),
            (r"recall the letters", label(r"F \ Q \ ...", font_size=40, color=YOU), ""),
        ], frame_w=2.3, frame_h=1.2, font_size=18).move_to([0, 1.9, 0])
        rows = rows_of([
            (r"1980: \ Meredyth Daneman and Patricia Carpenter: \ read sentences aloud, \ keep each one's last word", WHITE),
            (r"reading span predicted reading comprehension and the verbal SAT; \ simple word span much less well", MEM),
            (rf"a 1996 meta-analysis: \ reading span and comprehension correlate about "
             rf"{p['meta_r_reading_span_comprehension']:.2f}", DATA),
            (r"operation span, \ above, \ is the version most used today: \ arithmetic instead of sentences", GREY_A),
            (r"Engle's view: \ what complex span measures is control of attention, \ keeping a goal against "
             r"interference", EXEC),
        ], 12.4, 25, 0.26).to_edge(DOWN, buff=0.8)
        tag = historical_tag(archive.DANEMAN_CARPENTER_1980.cite)
        with self.voiceover(
            "If working memory is a workspace for thinking, the capacity that matters should be the capacity to hold "
            "while doing something else. <bookmark mark='a'/> In 1980 Meredyth Daneman and Patricia Carpenter had "
            "students read sentences aloud and remember the last word of each, in sets of increasing size. "
            "<bookmark mark='b'/> This reading span predicted reading comprehension and verbal SAT scores much better than a "
            "plain word span did. <bookmark mark='c'/> A meta-analysis by Daneman and Philip Merikle in 1996 "
            f"put the correlation with comprehension at about {p['meta_r_reading_span_comprehension']:.2f}. "
            "<bookmark mark='d'/> The version on screen, operation span, alternates arithmetic with letters, and is "
            "the most used today. <bookmark mark='e'/> Randall Engle and his colleagues argue that what these tasks "
            "really measure is executive attention: the ability to keep a goal active while something else "
            "competes for it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(strip))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def correlation(self):
        p = archive.KANE_2005.data
        head = heading(r"Working memory capacity and fluid intelligence")
        wmc = Circle(1.1, color=MEM, fill_opacity=0.15).move_to([-5.1, 0.75, 0])
        gf = Circle(1.1, color=EXEC, fill_opacity=0.15).move_to([-0.9, 0.75, 0])
        wl = wrapped_label(r"working memory capacity", 1.8, 21, MEM).move_to(wmc)
        gl = wrapped_label(r"fluid intelligence", 1.8, 21, EXEC).move_to(gf)
        arrow = DoubleArrow(wmc.get_right(), gf.get_left(), buff=0.1, color=GREY_B)
        rl = label(rf"latent: \ about {p['latent_r']:.2f}", font_size=22, color=DATA).move_to([-3.0, 1.5, 0])
        tl = wrapped_label(rf"one task with one task: \ about {p['task_r']:.2f}", 2.4, 19, GREY_B).move_to(
            [-3.0, -0.05, 0])
        eq = MathTex(r"r_{\text{tasks}} = r_{\text{latent}}\,\sqrt{\rho_1 \rho_2}", font_size=38, color=GREY_A)
        eq.move_to([4.0, 0.9, 0])
        el = label(r"Part 3: \ unreliable tests attenuate a correlation", font_size=20, color=GREY_B).next_to(
            eq, DOWN, buff=0.2)
        rows = rows_of([
            (r"2005: \ Kane, \ Hambrick and Conway re-analyse 14 latent-variable studies", WHITE),
            (rf"working memory and fluid reasoning share a lot: \ a latent correlation near {p['latent_r']:.2f}", DATA),
            (rf"Ackerman, \ Beier and Boyle: \ task-level correlations nearer {p['task_r']:.2f}; \ related, \ not "
             r"the same thing", GREY_A),
            (r"a correlation across people is not a mechanism, \ and not a lever: \ Part 32", LOST),
        ], 12.4, 25, 0.26).to_edge(DOWN, buff=0.8)
        tag = published_tag(archive.KANE_2005.cite)
        with self.voiceover(
            "Complex span also predicts something broader. <bookmark mark='a'/> In 2005 Michael Kane, David Hambrick "
            "and Andrew Conway re-analysed fourteen studies that measured working memory capacity and fluid "
            "intelligence, the ability to solve new problems, each with several tasks. <bookmark mark='b'/> The "
            f"correlation between the two underlying factors was about {p['latent_r']:.2f}. "
            "<bookmark mark='c'/> Phillip Ackerman and his colleagues, looking at single tasks, put it nearer "
            f"{p['task_r']:.2f}. The two numbers are not in conflict: a single task is an unreliable measure of a "
            "factor, and Part 3 showed how unreliability attenuates a correlation. Both camps agreed the two are "
            "related but not the same thing. <bookmark mark='d'/> And a correlation across people says nothing "
            "about whether raising one would raise the other. That is an experiment, and an industry ran it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(wmc), FadeIn(gf), FadeIn(wl), FadeIn(gl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arrow), FadeIn(rl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(tl), FadeIn(eq), FadeIn(el), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
