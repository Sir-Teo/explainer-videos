from __future__ import annotations

from videos.psychology.psych2.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.unblinded()
        self.balanced()
        self.open_questions()

    def card(self):
        card = chapter_card(14, r"Frontier: \ when the blind cannot be kept", r"What do you do when the subject can "
                            r"tell which group they are in?", lit=(), part=PART, scale=("person", "group"),
                            marr=("what",))
        with self.voiceover(
            "Chapter fourteen. The frontier: when the blind can't be kept."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def unblinded(self):
        m = archive.MITCHELL_2021.data
        head = heading(r"A double-blind trial in which most people knew")
        drug_wrong, plac_wrong = m["drug_believed_placebo_at_least"], m["placebo_believed_drug_at_least"]

        def arm(n, wrong, color, name):
            cols = [color] * (n - wrong) + [GREY_C] * wrong
            crowd = people_row(n, cols, height=0.42, buff=0.09, per_row=23)
            t = label(name, font_size=28, color=color).next_to(crowd, UP, buff=0.15).align_to(crowd, LEFT)
            w = label(rf"at least {wrong} guessed wrong", font_size=24, color=GREY_B)
            w.next_to(crowd, DOWN, buff=0.12).align_to(crowd, LEFT)
            return VGroup(crowd, t, w)

        a = arm(m["n_drug"], drug_wrong, TREAT, rf"the drug: \ {m['n_drug']} people")
        b = arm(m["n_placebo"], plac_wrong, CTRL, rf"the placebo: \ {m['n_placebo']} people")
        arms = VGroup(a, b).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to([-1.3, 0.35, 0])
        key = VGroup(label(r"coloured: \ did not guess wrong", font_size=24, color=WHITE),
                     label(r"grey: \ guessed the other arm", font_size=24, color=GREY_B))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([5.0, 0.6, 0])
        if key.get_right()[0] > 6.95:
            key.shift(LEFT * (key.get_right()[0] - 6.95))
        q = wrapped_label(r"The drug group improved more. \ How much of that is the drug, and how much is knowing "
                          r"you got it?", 12.4, 30, P.ACCENT).to_edge(DOWN, buff=0.9)
        src = published_tag(archive.MITCHELL_2021.cite + r"; \ the authors' own count, which they call anecdotal")
        with self.voiceover(
            "Everything today leaned on the blind. So here's the open problem: sometimes it can't be kept. "
            "<bookmark mark='a'/> Take a real trial from 2021, of a drug with strong and unmistakable effects, "
            f"given alongside psychotherapy for post-traumatic stress. {m['n']} people, randomized, placebo "
            "controlled, double blind on paper. <bookmark mark='b'/> When the participants were told at the end "
            f"which arm they'd been in, at least {drug_wrong} of the {m['n_drug']} who had the drug had guessed "
            f"wrong. <bookmark mark='c'/> And at least {plac_wrong} of the {m['n_placebo']} on placebo. The "
            "authors reported this themselves, and call the count informal. Even so, it leaves a large majority "
            "who had worked out what they were given. <bookmark mark='d'/> The group on the drug improved more. Now you can "
            "see the difficulty. Expecting to get better is a treatment too. If people can tell what they got, "
            "the trial has randomized two things at once, the drug and the belief, and can't separate them. The "
            "same holds for any talking therapy, where no one can be blind to having had it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(a[1]), FadeIn(b[1]))
            vo.wait_until("b")
            self.play(FadeIn(a[0], lag_ratio=0.02), FadeIn(a[2]), FadeIn(key))
            vo.wait_until("c")
            self.play(FadeIn(b[0], lag_ratio=0.02), FadeIn(b[2]))
            vo.wait_until("d")
            self.play(FadeIn(q, shift=UP * 0.15))
        self.clear_scene()

    def balanced(self):
        head = heading(r"One answer: \ randomize the belief as well")
        cell = 2.2
        grid = VGroup()
        labels_top = [r"given the drug", r"given a placebo"]
        labels_left = [r"told: \ drug", r"told: \ placebo"]
        text = [[r"drug + belief", r"belief alone"], [r"drug alone", r"neither"]]
        colors = [[P.ACCENT, CTRL], [TREAT, GREY_C]]
        for i in range(2):
            for j in range(2):
                sq = RoundedRectangle(width=cell * 1.5, height=cell * 0.75, corner_radius=0.12, stroke_color=colors[i][j],
                                      stroke_width=2.5, fill_color=CARD_FILL, fill_opacity=1)
                sq.move_to([(j - 0.5) * cell * 1.6, (0.5 - i) * cell * 0.85, 0])
                grid.add(VGroup(sq, label(text[i][j], font_size=30, color=colors[i][j]).move_to(sq)))
        top = VGroup(*[label(t, font_size=26, color=WHITE).next_to(grid[j], UP, buff=0.2) for j, t in
                       enumerate(labels_top)])
        left = VGroup(*[label(t, font_size=26, color=WHITE).next_to(grid[2 * i], LEFT, buff=0.3) for i, t in
                        enumerate(labels_left)])
        table = VGroup(grid, top, left).move_to([0, 0.25, 0])
        note_ = wrapped_label(r"The balanced placebo design: \ a factorial, as in chapter 8. \ Its price is "
                              r"chapter 10: \ half the people are told something false.", 12.4, 28, GREY_A)
        note_.to_edge(DOWN, buff=0.85)
        others = VGroup(*[label(t, font_size=26, color=WHITE) for t in (
            r"an active placebo, with side effects of its own", r"ask everyone to guess their arm, and report it",
            r"several doses: \ does more drug do more?")])
        others.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        with self.voiceover(
            "What can a designer do? You have the tools already. <bookmark mark='a'/> If two things are "
            "tangled, cross them. Give the drug or a placebo, and separately, tell people they're getting the "
            "drug or a placebo. Four cells. <bookmark mark='b'/> One cell has the drug without the belief, and "
            "one has the belief without the drug, and the factorial pulls the two effects apart. It's called "
            "the balanced placebo design. <bookmark mark='c'/> And you can see its price at once. Half the "
            "participants are told something false about what's in their bodies, which is the chapter on ethics "
            "meeting the chapter on design head on. So in practice trials use weaker tools: a placebo with "
            "noticeable effects of its own, a routine question asking everyone to guess their group, a range "
            "of doses. None of them fully solves it. It's an open problem with large consequences, since "
            "several treatments now being tested are ones nobody could mistake for a sugar pill."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(top), FadeIn(left), LaggedStart(*[FadeIn(g) for g in grid], lag_ratio=0.3),
                      run_time=3.0)
            vo.wait_until("b")
            self.play(Indicate(grid[2], color=TREAT, scale_factor=1.06), Indicate(grid[1], color=CTRL,
                                                                                  scale_factor=1.06))
            vo.wait_until("c")
            self.play(FadeIn(note_, shift=UP * 0.15))
        self.clear_scene()

    def open_questions(self):
        head = heading(r"What is open")
        items = (
            (r"How big is the experimenter's footprint, study by study?",
             r"Demand can now be measured by hinting at the hypothesis on purpose (de Quidt et al.\ 2018). \ Few "
             r"studies do it."),
            (r"Can a design recover the effect when the blind fails?",
             r"Guesses of one's arm are rarely collected, and there is no agreed way to use them."),
            (r"Does a finding from one population hold in another?",
             r"Most samples still come from a small part of humanity. \ Large multi-site studies are the current "
             r"answer (Part 43)."),
        )
        rows = VGroup()
        for i, (q, a) in enumerate(items, 1):
            num = label(rf"{i}", font_size=52, color=P.ACCENT)
            body = VGroup(label(q, font_size=36, color=WHITE), wrapped_label(a, 11.6, 27, GREY_A))
            body.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            rows.add(VGroup(num, body).arrange(RIGHT, buff=0.4, aligned_edge=UP))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(head, DOWN, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        star = VGroup(label(r"$\star$ \ Research problem", font_size=28, color=P.ACCENT),
                      wrapped_label(r"A trial's participants can tell which arm they are in. \ Design a study, "
                                    r"acceptable to an ethics board, that separates the treatment's effect from "
                                    r"the effect of knowing. \ Say what it assumes.", 12.4, 27, WHITE))
        star.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        box = SurroundingRectangle(star, color=P.ACCENT, buff=0.22, corner_radius=0.12, stroke_width=2)
        sp = VGroup(box, star).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Three things are open. <bookmark mark='a'/> One. How large is the experimenter's footprint in an "
            "ordinary study? It can be measured now, by hinting at the hypothesis deliberately and seeing how "
            "far behaviour moves. Hardly anyone does. <bookmark mark='b'/> Two. When a blind fails, can the "
            "design still recover the effect? Participants' guesses are rarely even collected, and there's no "
            "agreed way to use them. <bookmark mark='c'/> Three. Does a finding from one kind of people hold "
            "for another? The current answer is to run the same study in many countries at once, and Part 43 "
            "does exactly that. <bookmark mark='d'/> And this part's research problem is the second of those. "
            "Participants can tell which arm they're in. Design a study that an ethics board would pass, and "
            "that separates the treatment from the knowing."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abc", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r, shift=LEFT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(sp, shift=UP * 0.2))
        self.clear_scene()
