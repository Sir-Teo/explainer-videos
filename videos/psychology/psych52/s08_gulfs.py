from __future__ import annotations

from videos.psychology.psych52.common import *  # noqa: F403


class Gulfs(VoiceoverScene):
    def construct(self):
        card_section(self, 7, r"Gulfs, \ affordances and signifiers", r"Why can't I open this door?",
                     marr=("what",))
        self.gulfs()
        self.affordances()

    def gulfs(self):
        head = heading(r"Norman's two gulfs")
        user = VGroup(little_person(1.2, PERSON), label(r"the user's goal", font_size=18, color=PERSON))
        user.arrange(DOWN, buff=0.15).move_to([-4.6, 0.9, 0])
        world = VGroup(RoundedRectangle(width=2.4, height=1.5, corner_radius=0.15, color=MODEL, fill_opacity=0.15),
                       label(r"the system's state", font_size=18, color=MODEL))
        world[1].move_to(world[0])
        world.move_to([4.6, 0.9, 0])
        ex = CurvedArrow(user.get_right() + UP * 0.3, world.get_left() + UP * 0.3, angle=-0.5, color=GOOD)
        ev = CurvedArrow(world.get_left() + DOWN * 0.3, user.get_right() + DOWN * 0.3, angle=-0.5, color=AUTH)
        le = label(r"execution: \ how do I do it?", font_size=18, color=GOOD).next_to(ex, UP, buff=0.1)
        lv = label(r"evaluation: \ did it work?", font_size=18, color=AUTH).next_to(ev, DOWN, buff=0.1)
        rows = rows_of([
            (r"the gulf of execution: \ the distance between what I want and the actions the system offers", GOOD),
            (r"the gulf of evaluation: \ the distance between what the system shows and what I need to know", AUTH),
            (r"Part 51's Three Mile Island light was a gulf of evaluation; \ a hidden menu command is a gulf of "
             r"execution", PERSON),
            (r"design narrows both: \ visible actions, \ immediate feedback, \ a clear mapping between them", YOU),
        ], 12.4, 20, 0.3).move_to([0, -2.3, 0])
        with self.voiceover(
            "Donald Norman described what goes wrong between a person and a device as two gulfs. "
            "<bookmark mark='a'/> The gulf of execution is the distance between what I want and the actions the system "
            "offers. How do I do it? <bookmark mark='b'/> The gulf of evaluation is the distance between what the "
            "system shows and what I need to know. Did it work? <bookmark mark='c'/> Part 51's light at Three Mile "
            "Island was a gulf of evaluation. A command hidden three menus deep is a gulf of execution. "
            "<bookmark mark='d'/> Design narrows both: visible actions, immediate feedback, and a clear mapping "
            "between them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(user), FadeIn(world))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(ex), FadeIn(le))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(ev), FadeIn(lv))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def affordances(self):
        chips_section(self, r"Affordances and signifiers", [
            (r"affordance", r"what an object allows a person to do: \ a flat plate affords pushing, \ a handle "
                            r"pulling (Gibson's word, \ Norman's use)", GOOD),
            (r"signifier", r"what tells the person the affordance is there: \ the plate, \ an underline, \ a raised "
                           r"button", MODEL),
            (r"the Norman door", r"a handle on a door that must be pushed: \ a signifier that lies", AUTH),
            (r"the flat screen", r"a screen affords touching everywhere: \ so every action needs a signifier, \ and "
                                 r"flat design that removes them hides the actions", PERSON),
        ], "Norman borrowed a word from James Gibson. <bookmark mark='a'/> An affordance is what an object allows a "
           "person to do. A flat plate affords pushing, and a handle affords pulling. <bookmark mark='b'/> A "
           "signifier is what tells the person the affordance is there: the plate, an underline, a raised button. "
           "<bookmark mark='c'/> A door with a handle that has to be pushed has a signifier that lies. People call it "
           "a Norman door. <bookmark mark='d'/> A screen affords touching everywhere, so every action needs a "
           "signifier, and flat designs that remove them hide the actions.", chip_w=3.4, text_w=8.8)
