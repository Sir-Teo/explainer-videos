from __future__ import annotations

from videos.philosophy.philosophy28.common import *  # noqa: F403


class Private(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"A private language?", r"Could a word mean what only I can know?", lit=(1953,),
                            part=PART)
        with self.voiceover("Chapter four. A private language?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.diary()
        self.beetle()
        self.readings()

    def diary(self):
        head = label(r"The diary \ (\S 258)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        page = RoundedRectangle(width=3.6, height=3.4, corner_radius=0.1, color=GREY_B, fill_color="#141a24",
                                fill_opacity=1).move_to([-3.8, -0.2, 0])
        entries = VGroup(*[label(t, font_size=20, color=WORD) for t in (r"Mon: \ S", r"Tue: \ ---", r"Wed: \ S",
                                                                         r"Thu: \ S?", r"Fri: \ ---")]).arrange(
            DOWN, buff=0.3, aligned_edge=LEFT).move_to(page)
        rows = stack([(r"I have a sensation, \ and write `S' in my diary whenever I have it", WHITE),
                      (r"`S' is defined privately: \ I concentrate my attention on the sensation", WORD),
                      (r"next time, \ how do I know I am using `S' correctly?", BAD),
                      (r"`whatever is going to seem right to me is right. \ And that only means that here we can't talk "
                       r"about \textit{right}'", RULE_C),
                      (r"no criterion of correctness: \ so no rule, \ so no meaning", GOAL)], font_size=21,
                     aligned_edge=LEFT, width=6.4, buff=0.28).move_to([3.0, -0.2, 0])
        with self.voiceover(
            "The rule-following argument has a famous corollary. <bookmark mark='a'/>Suppose I keep a diary about a "
            "certain sensation, and write S on every day I have it. <bookmark mark='b'/>S is defined by me alone: I "
            "concentrate my attention on the sensation and say to myself, this is S. <bookmark mark='c'/>Next time, how "
            "do I know I am using S correctly, for the same kind of sensation? <bookmark mark='d'/>Only by its seeming "
            "the same to me. But then, Wittgenstein writes, whatever is going to seem right to me is right, and that "
            "only means that here we can't talk about right. <bookmark mark='e'/>Without a criterion of correctness "
            "there is no rule, and without a rule, no meaning. A language whose words refer to what only its speaker "
            "can know is impossible."
        ) as vo:
            self.play(FadeIn(head), FadeIn(page))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(e) for e in entries], lag_ratio=0.3))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def beetle(self):
        head = label(r"The beetle in the box \ (\S 293)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        boxes = VGroup()
        contents = [Dot(radius=0.12, color=TRUTH), Star(n=5, outer_radius=0.16, color=USE, fill_opacity=1),
                    VGroup(), Square(0.22, color=HEAR, fill_opacity=1)]
        for i, c in enumerate(contents):
            b = Square(1.2, color=GREY_B, stroke_width=3).move_to([-4.8 + 2.2 * i, 0.7, 0])
            lid = Line(b.get_corner(UL), b.get_corner(UR), color=GREY_A, stroke_width=6)
            if len(c):
                c.move_to(b)
            who = label(rf"person {i + 1}", font_size=17, color=GREY_A).next_to(b, DOWN, buff=0.12)
            boxes.add(VGroup(b, c, lid, who))
        tag = label(r"everyone calls what is in their own box `beetle'", font_size=22, color=WORD).next_to(boxes, UP,
                                                                                                     buff=0.35)
        rows = stack([(r"no one can look into anyone else's box", WHITE),
                      (r"the boxes might hold different things, \ or something always changing, \ or nothing", BAD),
                      (r"`the thing in the box has no place in the language-game at all': \ it drops out", RULE_C),
                      (r"so if `pain' worked like `beetle', \ the private object would be irrelevant to its meaning",
                       GOAL)], font_size=21, aligned_edge=LEFT, width=12.0, buff=0.25).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Wittgenstein's second image is a game with boxes. <bookmark mark='a'/>Suppose everyone has a box with "
            "something in it, which we call a beetle. <bookmark mark='b'/>No one can look into anyone else's box, and "
            "everyone says he knows what a beetle is only by looking at his own. <bookmark mark='c'/>It would be quite "
            "possible for everyone to have something different in his box, or for the thing to be constantly "
            "changing, or for a box to be empty. <bookmark mark='d'/>The thing in the box, he concludes, has no place "
            "in the language game at all. It cancels out, whatever it is. <bookmark mark='e'/>So if a word like pain "
            "worked like beetle, the private object would be irrelevant to what the word means."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.2), FadeIn(tag))
            for mk, r in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def readings(self):
        head = label(r"What the argument shows", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"not behaviourism", r"Wittgenstein denies that sensations are nothing; \ `a nothing would serve just as "
                                  r"well as a something about which nothing could be said'", RULE_C),
            (r"the target", r"the picture of an inner object named by a private ostensive definition", BAD),
            (r"Robinson Crusoe", r"Ayer \ (1954): \ a solitary person could still keep rules; \ the debate is over "
                                 r"\textit{possible} sharing, \ not actual company", HIST),
            (r"where it returns", r"qualia, \ and the hard problem of consciousness, \ in Part 31", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "What does the argument show? <bookmark mark='a'/>Not that sensations are nothing, as a behaviourist "
            "might say. Wittgenstein's interlocutor asks if he is a behaviourist in disguise, and he replies that the "
            "conclusion is only that a nothing would serve just as well as a something about which nothing could be "
            "said. <bookmark mark='b'/>The target is a picture: an inner object, named by a private act of pointing. "
            "<bookmark mark='c'/>Critics such as A. J. Ayer, in 1954, asked about Robinson Crusoe, alone on his island: "
            "surely he could keep records. Defenders reply that what matters is whether the rules could be shared and "
            "checked, not whether anyone else is around. <bookmark mark='d'/>The argument returns when Part 31 asks "
            "about qualia and the hard problem of consciousness."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
