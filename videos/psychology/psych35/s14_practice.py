from __future__ import annotations

from videos.psychology.psych35.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.judging()
        self.research()
        self.machines()

    def card(self):
        card = chapter_card(13, r"In practice: \ judging people, \ asking people", r"Where do these errors cost money?",
                            lit={2000: r"Ng \& Russell"}, part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter thirteen. In practice: judging people, and asking people."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def judging(self):
        head = heading(r"Judging people at work")
        items = [
            (r"interviews", r"first impressions form in a tenth of a second and agree across judges \ (chapter "
             r"six); \ structured interviews, \ the same questions scored the same way, \ predict job performance "
             r"better than conversation \ (Part 53)", PERSON),
            (r"performance reviews", r"a bad quarter reads as a bad employee: \ the correspondence bias \ (chapter "
             r"two); \ ask what the territory, \ the team and the year made easy or hard", AUTH),
            (r"self-assessment", r"almost everyone is above average \ (chapter five); \ calibrate against outcomes, "
             r"\ not against confidence", CROWD),
            (r"post-mortems", r"people explain their own decisions with plausible theories \ (chapter eleven); "
             r"\ keep records written at the time of the decision", MODEL),
        ]
        rows = VGroup()
        for what, how, c in items:
            rows.add(VGroup(word_chip(what, color=c, font_size=19, width=3.6), wrapped_label(how, 8.4, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to([0, -0.2, 0])
        with self.voiceover(
            "Every finding in this part has a price at work. <bookmark mark='a'/> In interviews, impressions form in "
            "a tenth of a second and judges agree on them. Structured interviews, with the same questions scored the "
            "same way, predict job performance better than a conversation does. Part 53 measures how much better. "
            "<bookmark mark='b'/> In performance reviews, a bad quarter reads as a bad employee. That's the "
            "correspondence bias. Ask what the territory, the team and the year made easy or hard. "
            "<bookmark mark='c'/> In self-assessment, almost everyone is above average. Calibrate against outcomes, "
            "not confidence. <bookmark mark='d'/> And in post-mortems, people explain their own decisions with "
            "plausible theories. Keep records written at the time the decision was made."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def research(self):
        head = heading(r"What users say, \ and what they do")
        left = VGroup(word_chip(r"ask", color=CROWD, font_size=24, width=5.2),
                      wrapped_label(r"``would you use this?'': \ LaPiere's letter; \ ``why did you choose that?'': "
                                    r"\ the stockings", 5.2, 20, WHITE),
                      wrapped_label(r"good for what people want, \ feel and understand", 5.2, 20, GOOD)
                      ).arrange(DOWN, buff=0.3)
        right = VGroup(word_chip(r"watch", color=PERSON, font_size=24, width=5.2),
                       wrapped_label(r"what they click, \ where they hesitate, \ what they come back to: \ LaPiere's "
                                     r"road trip", 5.2, 20, WHITE),
                       wrapped_label(r"good for what people do, \ and in which situation", 5.2, 20, GOOD)
                       ).arrange(DOWN, buff=0.3)
        VGroup(left, right).arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to([0, 0.6, 0])
        foot = wrapped_label(r"user research's oldest rule, \ ``watch what they do, \ not what they say'', \ is "
                             r"LaPiere's lesson with a match in kind: \ ask about the specific act, \ in the specific "
                             r"situation", 12.0, 21, YOU).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "User research meets chapter four every day. <bookmark mark='a'/> Asking people whether they'd use "
            "something is LaPiere's letter. Asking why they chose something is the stockings. Asking is good for "
            "what people want, feel and understand. <bookmark mark='b'/> Watching what they click, where they "
            "hesitate and what they come back to is LaPiere's road trip. It's good for what people do, and in which "
            "situation. <bookmark mark='c'/> The field's oldest rule, watch what they do, not what they say, is "
            "LaPiere's lesson. And when you do ask, ask about the specific act, in the specific situation."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def machines(self):
        head = heading(r"Machines that infer what you want")
        rows = rows_of([
            (r"Ng and Russell, \ 2000: \ inverse reinforcement learning: \ recover the reward an agent is pursuing "
             r"from its behaviour, \ chapter ten's idea as an algorithm", WHITE),
            (r"recommenders, \ assistants and robots that learn from demonstration all infer goals from actions", CROWD),
            (r"they inherit the observer's problems: \ a click forced by the layout read as a preference is the "
             r"correspondence bias, \ in software", AUTH),
            (r"and a system that assumes people are rational will misread them exactly where Parts 25 and 26 "
             r"showed they are not", YOU),
        ], 12.0, 22, 0.42).move_to([0, -0.3, 0])
        tag = historical_tag(r"Ng \& Russell (2000)")
        with self.voiceover(
            "Machines read minds too. <bookmark mark='a'/> In 2000 Andrew Ng and Stuart Russell described inverse "
            "reinforcement learning: recover the reward an agent is pursuing from its behaviour. It's chapter ten's "
            "idea as an algorithm. <bookmark mark='b'/> Recommenders, assistants and robots that learn from "
            "demonstration all infer goals from actions. <bookmark mark='c'/> And they inherit the observer's "
            "problems. A click forced by the layout, read as a preference, is the correspondence bias in software. "
            "<bookmark mark='d'/> A system that assumes people are rational will misread them exactly where Parts "
            "25 and 26 showed they aren't."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
