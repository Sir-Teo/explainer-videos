from __future__ import annotations

from videos.psychology.psych2.common import *  # noqa: F403

AB, TRIAL, UX = "#7EC8F5", "#7BD88F", "#F2C14E"


def tile(title: str, lines, color, width=4.25) -> VGroup:
    t = label(title, font_size=34, color=color)
    body = VGroup(*[wrapped_label(ln, width - 0.6, 24, WHITE) for ln in lines]).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.2)
    inner = VGroup(t, body).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    box = RoundedRectangle(width=width, height=inner.height + 0.6, corner_radius=0.14, stroke_color=color,
                           stroke_width=2, fill_color=CARD_FILL, fill_opacity=0.95)
    inner.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.3)
    return VGroup(box, inner)


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.uses()
        self.in_practice()

    def card(self):
        card = chapter_card(13, r"In practice: \ who is blind?", r"Where are these designs earning a living today?",
                            lit=(), part=PART, scale=("group",), marr=("what",))
        with self.voiceover(
            "Chapter thirteen. In practice: who is blind?"
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def uses(self):
        head = heading(r"The same designs, under other names")
        tiles = VGroup(
            tile(r"A/B test", [r"a website shows version A or B by the toss of a coin",
                               r"the control group is the old page",
                               r"users do not know they are in it: \ a blind, for free"], AB),
            tile(r"clinical trial", [r"randomized, placebo-controlled, double-blind",
                                     r"everyone randomized is analysed, including those who dropped out",
                                     r"the answer to attrition has a name: \ intention to treat"], TRIAL),
            tile(r"user study", [r"each tester tries every design: \ within-person",
                                 r"the order is counterbalanced",
                                 r"the person running the session did not build the design"], UX),
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP).next_to(head, DOWN, buff=0.45)
        if tiles.width > 13.6:
            tiles.width = 13.6
        with self.voiceover(
            "None of this stayed in psychology. <bookmark mark='a'/> When a website tests a new button, it "
            "shows the new page to a random half of its visitors and the old page to the rest. That's a "
            "randomized experiment with a control group, and since the visitors don't know, it's blind as "
            "well. Large companies run thousands of them a year. <bookmark mark='b'/> A drug is approved on "
            "randomized, placebo-controlled, double-blind trials, every word of which you now know the reason "
            "for. And trials have their own answer to attrition: analyse everyone as they were randomized, "
            "including the people who dropped out. <bookmark mark='c'/> And when a design team watches people "
            "use two versions of a product, a good one has every tester try both, in a balanced order, with a "
            "session leader who didn't build either. Chapter six, and chapter seven."
        ) as vo:
            self.play(FadeIn(head))
            for mark, t in zip("abc", tiles):
                vo.wait_until(mark)
                self.play(FadeIn(t, shift=UP * 0.15))
        self.clear_scene()

    def in_practice(self):
        head = label(r"In practice", font_size=48, color=P.ACCENT)
        qs = VGroup(*[label(t, font_size=36, color=WHITE) for t in (
            r"1. \ Compared with what?",
            r"2. \ Who decided who got what?",
            r"3. \ Who knew?",
            r"4. \ Who dropped out?",
            r"5. \ Who was studied?",
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        who = wrapped_label(r"Who uses this: \ experimenters of every kind, product and data teams, clinical "
                            r"researchers, policy evaluators, and anyone reading a headline that says ``study "
                            r"finds''.", 12.4, 28, GREY_A)
        g = VGroup(head, qs, who).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(ORIGIN)
        with self.voiceover(
            "So here is this part's practice card, and it's five questions long. You can put them to any study, "
            "in any field, including the ones in the news tomorrow. <bookmark mark='a'/> Compared with what? "
            "<bookmark mark='b'/> Who decided who got what? <bookmark mark='c'/> Who knew? "
            "<bookmark mark='d'/> Who dropped out? <bookmark mark='e'/> And who was studied? "
            "<bookmark mark='f'/> A study that can answer all five has earned a hearing. It hasn't yet earned "
            "belief. That takes the next two parts."
        ) as vo:
            self.play(FadeIn(head))
            for mark, q in zip("abcde", qs):
                vo.wait_until(mark)
                self.play(FadeIn(q, shift=RIGHT * 0.2))
            vo.wait_until("f")
            self.play(FadeIn(who, shift=UP * 0.15))
        self.clear_scene()
