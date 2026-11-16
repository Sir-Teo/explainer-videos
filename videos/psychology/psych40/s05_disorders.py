from __future__ import annotations

from videos.psychology.psych40.common import *  # noqa: F403


class Disorders(VoiceoverScene):
    def construct(self):
        self.card()
        self.frame()
        self.panic()
        self.habit()

    def card(self):
        card = chapter_card(4, r"The anxiety disorders in one frame", r"What do phobia, \ panic, \ worry and "
                            r"compulsion share?", lit={1986: r"Clark"}, part=PART, scale=("person",),
                            marr=("what", "how"))
        with self.voiceover("Chapter four. The anxiety disorders in one frame."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def frame(self):
        head = heading(r"What is feared, \ and what keeps it going")
        data = (
            (r"specific phobia", r"an object or situation", r"avoiding it", SYMP),
            (r"panic disorder", r"the body's own sensations", r"misreading them as catastrophe", AUTH),
            (r"social anxiety", r"others' judgment", r"safety behaviours, \ self-focus", PERSON),
            (r"generalized anxiety", r"many possible futures", r"worry as a way to feel prepared", MODEL),
            (r"OCD", r"intrusive thoughts", r"compulsions that bring relief, \ and become habits (Part 17)", GOOD),
            (r"PTSD", r"reminders of a trauma", r"avoiding the memory, \ so it is never reprocessed (Part 21)", WHITE),
        )
        hdr = VGroup(label(r"what is feared", font_size=16, color=GREY_B).move_to([-1.3, 2.3, 0], aligned_edge=LEFT),
                     label(r"what maintains it", font_size=16, color=GREY_B).move_to([2.4, 2.3, 0], aligned_edge=LEFT))
        rows = VGroup()
        for k, (name, feared, keeps, c) in enumerate(data):
            y = 1.6 - 0.72 * k
            cells = VGroup(word_chip(name, color=c, font_size=17, width=3.2).move_to([-6.4, y, 0], aligned_edge=LEFT),
                           wrapped_label(feared, 3.4, 17, WHITE).move_to([-1.3, y, 0], aligned_edge=LEFT),
                           wrapped_label(keeps, 4.4, 17, c).move_to([2.4, y, 0], aligned_edge=LEFT))
            rows.add(cells)
        with self.voiceover(
            "The anxiety disorders share one frame: something feared, and something that keeps the fear going. "
            "<bookmark mark='a'/> In a specific phobia, an object or situation is feared, and avoiding it keeps the "
            "fear alive. <bookmark mark='b'/> In panic disorder, what's feared is the body's own sensations, read as "
            "catastrophe. <bookmark mark='c'/> In social anxiety, others' judgment, kept going by safety behaviours "
            "and self-focus. <bookmark mark='d'/> In generalized anxiety, many possible futures, with worry felt as a "
            "way to be prepared. <bookmark mark='e'/> In obsessive-compulsive disorder, intrusive thoughts, with "
            "compulsions that bring relief and become habits, the goal-to-habit shift of Part 17. "
            "<bookmark mark='f'/> And in post-traumatic stress disorder, reminders of a trauma, with avoidance of "
            "the memory, so it's never reprocessed, the memory of Part 21."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr))
            for m, r in zip("abcdef", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def panic(self):
        head = heading(r"The panic spiral")
        names = [r"a body sensation", r"read as danger", r"anxiety", r"more sensations"]
        cols = [SYMP, AUTH, PERSON, SYMP]
        circ = VGroup()
        for k, (n, c) in enumerate(zip(names, cols)):
            a = PI / 2 - TAU * k / 4
            circ.add(word_chip(n, color=c, font_size=17, width=2.8).move_to([-3.6 + 1.9 * np.cos(a),
                                                                            0.1 + 1.5 * np.sin(a), 0]))
        arrows = VGroup(*[CurvedArrow(circ[k].get_center() + 0.4 * (circ[(k + 1) % 4].get_center() -
                                                                    circ[k].get_center()) / 2,
                                      circ[(k + 1) % 4].get_center() - 0.4 * (circ[(k + 1) % 4].get_center() -
                                                                              circ[k].get_center()) / 2,
                                      angle=-0.6, color=GREY_B) for k in range(4)])
        rows = rows_of([
            (r"Clark, \ 1986: \ a racing heart, \ breathlessness or dizziness is misread as a sign of a heart "
             r"attack, \ suffocation or madness", WHITE),
            (r"the misreading raises anxiety, \ which raises the sensations, \ which confirm the misreading", AUTH),
            (r"cognitive therapy tests the misreadings, \ for example by bringing on the sensations deliberately "
             r"and seeing that nothing happens", GOOD),
            (r"it is exposure aimed at a belief", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.2, 0])
        tag = historical_tag(r"Clark (1986)")
        with self.voiceover(
            "Panic shows how a belief closes the loop. <bookmark mark='a'/> In 1986 David Clark proposed that in "
            "panic disorder, a racing heart, breathlessness or dizziness is misread as a sign of a heart attack, "
            "suffocation, or going mad. <bookmark mark='b'/> The misreading raises anxiety, which raises the "
            "sensations, which confirm the misreading. <bookmark mark='c'/> Cognitive therapy tests the misreadings, "
            "for example by bringing on the sensations deliberately, and seeing that nothing happens. "
            "<bookmark mark='d'/> It's exposure, aimed at a belief."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(circ))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.4), run_time=2.0)
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def habit(self):
        head = heading(r"Compulsion as habit")
        goal = VGroup(word_chip(r"goal-directed", color=GOOD, font_size=20, width=3.4),
                      wrapped_label(r"act because of what the action brings; \ stop when the outcome stops being "
                                    r"wanted", 4.4, 18, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        habit = VGroup(word_chip(r"habit", color=AUTH, font_size=20, width=3.4),
                       wrapped_label(r"act because the cue is there; \ carry on even when the outcome is worthless",
                                     4.4, 18, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        VGroup(goal, habit).arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to([0, 1.3, 0])
        rows = rows_of([
            (r"Part 17: \ two systems control action, \ and practice shifts control from goals to habits", WHITE),
            (r"Gillan and colleagues, \ 2011: \ people with OCD kept responding for outcomes that had been made "
             r"worthless, \ more than controls did: \ a tilt toward habit", AUTH),
            (r"Gillan and colleagues, \ 2016: \ in large online samples, \ weaker goal-directed planning went with a "
             r"dimension of compulsivity found across diagnoses, \ not with OCD alone", MODEL),
            (r"so a compulsion may be a habit that has slipped free of its goal, \ and exposure with response "
             r"prevention retrains it", YOU),
        ], 12.4, 21, 0.36).move_to([0, -1.55, 0])
        tag = published_tag(r"Gillan et al.\ (2011); \ Gillan et al.\ (2016)")
        with self.voiceover(
            "Compulsions add a twist. <bookmark mark='a'/> In Part 17, two systems controlled action: goal-directed "
            "control, which acts for what the action brings, and habit, which acts because the cue is there. "
            "Practice shifts control from one to the other. <bookmark mark='b'/> In 2011 Claire Gillan and colleagues "
            "found that people with obsessive-compulsive disorder kept responding for outcomes that had been made "
            "worthless, more than controls did: a tilt toward habit. <bookmark mark='c'/> In 2016, in large online "
            "samples, Gillan and colleagues found that weaker goal-directed planning went with a dimension of "
            "compulsivity that cuts across diagnoses, not with OCD alone. <bookmark mark='d'/> So a compulsion may be "
            "a habit that has slipped free of its goal, and exposure with response prevention retrains it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(goal), FadeIn(habit))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
