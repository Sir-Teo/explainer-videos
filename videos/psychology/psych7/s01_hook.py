from __future__ import annotations

import numpy as np

from videos.psychology.psych7.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.accident()
        self.afterwards()
        self.question()
        self.objectives()

    def accident(self):
        g = archive.HARLOW_1868.data
        head = heading(r"Vermont, 13 September 1848")
        hd = head_outline(5.4).move_to([-3.6, -0.4, 0])
        c = hd.get_center()
        # the rod: in under the left cheekbone, out through the top of the head, toward the front
        a, b = c + np.array([1.15, -1.45, 0]), c + np.array([0.3, 3.0, 0])
        rod = Line(a, a, color=THRESH, stroke_width=9)
        rod_l = label(r"the tamping iron", font_size=24, color=THRESH).next_to(b, RIGHT, buff=0.15)
        facts = VGroup(
            wrapped_label(r"Phineas Gage, 25, \ foreman of a gang blasting rock for a railway", 5.6, 29, WHITE),
            wrapped_label(r"an iron rod more than a metre long, \ as thick as a broom handle, \ about six "
                          r"kilograms", 5.6, 29, THRESH),
            wrapped_label(r"in under the left cheekbone, \ out through the top of the head", 5.6, 29, WHITE),
            wrapped_label(r"He is talking within minutes. \ He rides into town sitting up.", 5.6, 29, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to([3.3, -0.2, 0])
        src = historical_tag(archive.HARLOW_1868.cite)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "On the thirteenth of September 1848, near Cavendish in Vermont, a gang of men was blasting rock "
            "to lay a railway. <bookmark mark='a'/> Their foreman was Phineas Gage, twenty-five years old, "
            "and by his employers' account the most capable man they had. His job was to pack gunpowder into "
            "a hole drilled in the rock, using an iron rod. <bookmark mark='b'/> The rod was more than a "
            "metre long, as thick as a broom handle, and weighed about six kilograms. That afternoon the "
            "powder went off while he was packing it. <bookmark mark='c'/> The rod went in under his left "
            "cheekbone, passed behind the eye, and came out through the top of his head. It landed some "
            "distance behind him. <bookmark mark='d'/> Gage was thrown onto his back. Within minutes he was "
            "talking. He rode into town sitting upright in a cart, and when the doctor arrived, the accounts "
            "say, Gage told him there was business enough here for him. He lived for about twelve more "
            "years."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(hd))
            vo.wait_until("a")
            self.play(FadeIn(facts[0], shift=RIGHT * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(facts[1], shift=RIGHT * 0.15))
            vo.wait_until("c")
            self.play(rod.animate.put_start_and_end_on(a, b), FadeIn(rod_l), FadeIn(facts[2]), run_time=0.5)
            vo.wait_until("d")
            self.play(FadeIn(facts[3], shift=UP * 0.1))
        self.clear_scene()

    def afterwards(self):
        head = heading(r"What happened to him afterwards? \ Two versions")
        story = VGroup(
            label(r"the story", font_size=36, color=LESION),
            wrapped_label(r"A sober, careful foreman becomes a foul-mouthed drifter who can never hold a job "
                          r"again.", 6.0, 30, WHITE),
            wrapped_label(r"So the frontal lobes hold a person's character.", 6.0, 30, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        record = VGroup(
            label(r"the record", font_size=36, color=SPARED),
            wrapped_label(r"1848: \ his doctor's short report of the injury and the recovery", 6.0, 30, WHITE),
            wrapped_label(r"1868: \ a second report, twenty years on, with a few sentences on his character: \ "
                          r"to his friends he was ``no longer Gage''", 6.0, 30, WHITE),
            wrapped_label(r"and in between: \ years driving a stagecoach in Chile", 6.0, 30, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        cols = VGroup(story, record).arrange(RIGHT, buff=0.7, aligned_edge=UP).move_to([0, 0.2, 0])
        if cols.width > 13.4:
            cols.width = 13.4
        end = wrapped_label(r"He survived, and something changed. \ How much, and for how long, the record does "
                            r"not say.", 12.6, 30, GREY_A).to_edge(DOWN, buff=0.7)
        src = historical_tag(archive.HARLOW_1868.cite)
        with self.voiceover(
            "What happened to him afterwards is one of the most often told stories in psychology, and you may "
            "have heard it. <bookmark mark='a'/> The careful, sober foreman turned into a foul-mouthed "
            "drifter, who could never hold a job again. And so, the story goes, we learned that the frontal "
            "lobes hold a person's character. <bookmark mark='b'/> Now the record. Gage's doctor, John "
            "Harlow, published a short report at the time, about the wound and the recovery. "
            "<bookmark mark='c'/> Twenty years later, after Gage had died, Harlow wrote a second one, and it "
            "has a few sentences on his character. He had become fitful and irreverent, Harlow wrote, and to "
            "his friends he was no longer Gage. That's nearly all there is. <bookmark mark='d'/> And there's "
            "one more fact in the record. For years in between, Gage drove a stagecoach in Chile. That's a "
            "job with a timetable, passengers, a team of horses and bad roads. A man who can't plan or "
            "control himself doesn't keep it. <bookmark mark='e'/> So he survived, and something in him "
            "changed. How much, for how long, and whether he got better, the record doesn't say. Most of what "
            "the textbooks add isn't in it. We'll put this on the Ledger, and you can guess the verdict."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in story], lag_ratio=0.7), run_time=5.0)
            vo.wait_until("b")
            self.play(FadeIn(record[0]), FadeIn(record[1], shift=RIGHT * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(record[2], shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(record[3], shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def question(self):
        head = heading(r"Is the mind in one place, or everywhere?")
        left = brain_side(4.6).move_to([-4.0, 0.6, 0])
        g = np.random.default_rng(7)
        names = [r"speech", r"memory", r"sight", r"caution", r"number", r"music"]
        spots = [(-0.55, 0.15), (0.05, -0.2), (0.72, 0.05), (-0.75, 0.3), (0.25, 0.4), (-0.25, -0.25)]
        tags = VGroup(*[label(n, font_size=20, color=BLACK).move_to(at(left, x, y)) for n, (x, y) in zip(names, spots)])
        left_l = VGroup(label(r"a place for each faculty", font_size=30, color=THRESH),
                        wrapped_label(r"remove the place, \ lose the faculty", 4.4, 26, WHITE)).arrange(
            DOWN, buff=0.1).next_to(left, DOWN, buff=0.3)
        right = brain_side(4.6, fill=0.0).move_to([4.0, 0.6, 0])
        for piece in right.lobe.values():
            piece.set_fill(GREY_B, opacity=0.35)
        right_l = VGroup(label(r"all of it, for everything", font_size=30, color=THRESH),
                         wrapped_label(r"remove any part, \ lose a little of everything", 4.4, 26, WHITE)).arrange(
            DOWN, buff=0.1).next_to(right, DOWN, buff=0.3)
        mid = label(r"or", font_size=40, color=GREY_B).move_to([0, 0.6, 0])
        end = wrapped_label(r"Damage is psychology's oldest experiment. \ This part is about how to read it, \ "
                            r"and how it misleads.", 12.6, 30, P.ACCENT).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Behind Gage's story is an old question. Is the mind in one place, or everywhere? "
            "<bookmark mark='a'/> One answer: each faculty has its own piece of brain. Speech here, memory "
            "there. Remove the piece, and you lose that faculty and nothing else. <bookmark mark='b'/> The "
            "other answer: the brain works as a whole. Remove any part of it, and you lose a little of "
            "everything. <bookmark mark='c'/> For most of history there was one way to find out, and it "
            "wasn't an experiment anyone would choose to run. You waited for an accident, a stroke, a wound, "
            "or a surgeon's knife, and then you looked at what the person could no longer do. Damage is "
            "psychology's oldest experiment. It's also one of the easiest to misread. This part is about how "
            "to read it, what it has shown, and how it misleads."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left), FadeIn(tags, lag_ratio=0.1), FadeIn(left_l))
            vo.wait_until("b")
            self.play(FadeIn(mid), FadeIn(right), FadeIn(right_l))
            vo.wait_until("c")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 7", font_size=34, color=GREY_B), label(r"The Brain", font_size=64))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the parts of a brain, \ and one line on what each is for",
            r"speech lost two ways, \ and a diagram that predicted a third",
            r"the logic of dissociation, \ and how one damaged system can fake two",
            r"maps: \ the body and the visual field laid out on the cortex, \ and your own blind spot",
            r"the man who could not make new memories, \ and the brain cut in two",
            r"a brain that rewires, \ and today's answer to ``one place or everywhere?''",
        ], color=P.ACCENT, font_size=32, width=13.2)
        with self.voiceover(
            "Part seven: the brain. <bookmark mark='a'/> We'll tour its parts, with one line on what each is "
            "for. <bookmark mark='b'/> We'll meet two patients who lost speech in two different ways, and a "
            "diagram that predicted a third way before anyone had seen it. <bookmark mark='c'/> We'll work "
            "out the logic that lets damage test a theory, the double dissociation, and we'll show how a "
            "single damaged system can fake one. <bookmark mark='d'/> We'll look at the maps on the cortex, "
            "compute how much of yours is spent on the centre of your gaze, and find the hole in your own "
            "field of view. <bookmark mark='e'/> We'll meet the man who could no longer make new memories, "
            "and the patients whose brains were cut in two. <bookmark mark='f'/> And we'll end with a brain "
            "that rewires itself, and with today's answer to the old question."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mark_, r in zip("bcdef", obj.rows[1:]):
                vo.wait_until(mark_)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
