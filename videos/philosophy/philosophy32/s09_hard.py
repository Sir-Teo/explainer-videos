from __future__ import annotations

from videos.philosophy.philosophy32.common import *  # noqa: F403


class Hard(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"No free will", r"What if neither determinism nor chance leaves room for desert?",
                            lit=(1994,), part=PART)
        with self.voiceover("Chapter eight. No free will."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.plum()
        self.basic()
        self.after()

    def plum(self):
        head = label(r"Pereboom's four cases", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"case 1", r"neuroscientists manipulate Professor Plum's brain moment by moment, \ so that he "
                            r"reasons his way to killing White", BAD),
                (r"case 2", r"they programmed him at the start of his life to reason that way", BAD),
                (r"case 3", r"his community trained him, \ by ordinary means, \ to reason that way", WILL),
                (r"case 4", r"ordinary determinism: \ the past and the laws produced him", LAW),
                (r"the argument", r"no relevant difference between neighbouring cases: \ if not responsible in 1, "
                                  r"\ not in 4", GOAL)]
        g = rows_table(rows, top=1.6, gap=0.42)
        with self.voiceover(
            "Derk Pereboom argues that the compatibilist conditions are not enough, with four cases. "
            "<bookmark mark='a'/>In the first, neuroscientists manipulate Professor Plum's brain moment by moment, "
            "so that he reasons his way to killing Ms White. He meets every compatibilist condition: he acts on "
            "desires he endorses, for reasons he responds to. Yet he is plainly not to blame. "
            "<bookmark mark='b'/>In the second, they programmed him at the start of his life to reason that way. "
            "<bookmark mark='c'/>In the third, his community trained him to, by ordinary means. "
            "<bookmark mark='d'/>In the fourth, there are no manipulators: the past and the laws of a deterministic "
            "world produced him. <bookmark mark='e'/>Pereboom argues there is no relevant difference between any "
            "case and the next. If Plum is not responsible in the first, he is not responsible in the fourth, and "
            "neither are we."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def basic(self):
        hc = history_card(1994, r"Galen Strawson", r"`The Impossibility of Moral Responsibility'", width=6.2,
                          color=HIST).to_corner(UL, buff=0.3)
        texts = [r"you do what you do because of how you are", r"to be responsible for that, \ you must be "
                                                                r"responsible for how you are",
                 r"so you must have made yourself that way, \ by acting on principles you already had",
                 r"and been responsible for those, \ so made yourself have them \dots"]
        boxes = VGroup()
        for k, t in enumerate(texts):
            b = VGroup(RoundedRectangle(width=6.4, height=0.75, corner_radius=0.15,
                                        color=[WILL, SELF, SELF, BAD][k], fill_opacity=0.08),
                       label(t, font_size=18, color=[WILL, SELF, SELF, BAD][k]))
            boxes.add(b.move_to([-2.8 + 0.5 * k, 1.1 - 1.0 * k, 0]))
        arrows = VGroup(*[Arrow(boxes[k].get_bottom() + LEFT * 2.0, boxes[k + 1].get_top() + LEFT * 2.0, buff=0.05,
                                color=GREY_B, stroke_width=2) for k in range(3)])
        conc = label(r"an infinite regress: \ no one can be the cause of himself, \ so no one is ultimately "
                     r"responsible", font_size=20, color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Galen Strawson's basic argument goes further: it says freedom of the kind desert needs is impossible, "
            "whether determinism is true or not. <bookmark mark='a'/>You do what you do because of how you are. "
            "<bookmark mark='b'/>So to be truly responsible for what you do, you must be responsible for how you "
            "are. <bookmark mark='c'/>But to be responsible for how you are, you must have made yourself that way, "
            "intentionally, acting on principles you already had. <bookmark mark='d'/>And to be responsible for "
            "those, you must have made yourself have them, and so on. <bookmark mark='e'/>The regress never ends. "
            "Since no one can be the cause of himself, Strawson concludes, no one is ultimately responsible for "
            "anything."
        ) as vo:
            self.play(FadeIn(hc))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(boxes[k]), *([GrowArrow(arrows[k - 1])] if k else []))
            vo.wait_until("e")
            self.play(FadeIn(conc))
        self.clear_scene()

    def after(self):
        head = label(r"Life without basic desert", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"what goes", r"basic desert: \ blame and punishment deserved just because of what one did", BAD),
                (r"what stays", r"forward-looking reasons: \ protection, \ moral formation, \ reconciliation", OK),
                (r"crime", r"Pereboom and Caruso: \ a public-health quarantine model in place of retribution", WILL),
                (r"meaning", r"love, \ gratitude and achievement, \ he argues, \ survive without it", SELF)]
        g = rows_table(rows, top=1.6, gap=0.5)
        with self.voiceover(
            "What would follow, if they were right? <bookmark mark='a'/>Pereboom's answer is that what goes is basic "
            "desert: the idea that someone deserves blame or punishment just because of what they did, regardless "
            "of any good it does. <bookmark mark='b'/>What stays are forward-looking reasons: protecting others, "
            "helping people become better, repairing relationships. <bookmark mark='c'/>For crime, he and Gregg "
            "Caruso propose a model like public-health quarantine: restraint where it protects, and no more harm "
            "than that requires. <bookmark mark='d'/>And love, gratitude and the sense of achievement, he argues, "
            "survive the loss. Whether they do is the question of the next chapter."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
