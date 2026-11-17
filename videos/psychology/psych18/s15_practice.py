from __future__ import annotations

from videos.psychology.psych18.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.radiology()
        self.alarms()
        self.screens()

    def card(self):
        card = chapter_card(14, r"In practice: \ alarms, \ radiology, \ roads, \ screens",
                            r"Where does the limit on attention cost lives or money?",
                            lit={2005: r"Wolfe et al.", 2013: r"Drew et al."}, part=PART, scale=("person", "group"),
                            marr=("what",))
        with self.voiceover("Chapter fourteen. In practice: alarms, radiology, roads, screens."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def radiology(self):
        head = heading(r"Searching for a living")
        rows = rows_of([
            (r"radiologists, \ baggage screeners, \ pathologists: \ professional searchers for rare targets", WHITE),
            (r"satisfaction of search: \ after finding one abnormality, \ readers miss a second more often", BAD),
            (r"prevalence: \ rare targets are missed more; \ screeners now see inserted test targets", ATT),
            (r"double reading by a second expert catches a share of misses; \ so do checklists", GOOD),
            (r"and an algorithm as second reader works only if people neither ignore it nor defer to it", CONTROL),
        ], 12.4, 27, 0.36).move_to([0, -0.1, 0])
        tag = published_tag(archive.WOLFE_2005.cite)
        with self.voiceover(
            "Attention research has direct customers. <bookmark mark='a'/> Radiologists, airport baggage screeners "
            "and pathologists are professional searchers, and their targets are rare. <bookmark mark='b'/> One "
            "well-known error is called satisfaction of search: after finding one abnormality on an image, readers "
            "are more likely to miss a second. It is the search ending too soon, in the terms of guided search. "
            "<bookmark mark='c'/> The prevalence effect is another. Airport screening systems now insert images of "
            "threats into real bag images now and then, which keeps the effective prevalence up and measures "
            "screeners' performance at the same time. <bookmark mark='d'/> Having a second expert read the same "
            "images catches a share of the misses, and so do checklists that force a full search. "
            "<bookmark mark='e'/> Algorithms are increasingly the second reader. They help only if people neither "
            "ignore their prompts nor stop searching once a prompt appears, which is an attention problem too."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def alarms(self):
        head = heading(r"Alarms that are not heard")
        rows = rows_of([
            (r"a hospital ward: \ monitors sound hundreds of alarms a day, \ most of them needing no action", WHITE),
            (r"alarm fatigue: \ staff learn, \ correctly, \ that an alarm usually means nothing", BAD),
            (r"a learned criterion, \ as in Chapter eleven: \ the rare true alarm pays for it", CONTROL),
            (r"fixes: \ fewer, \ smarter alarms; \ distinct sounds for distinct urgencies; \ delays for self-correcting "
             r"blips", GOOD),
            (r"cockpits and control rooms learned this first: \ every warning competes for the same bottleneck", ATT),
        ], 12.4, 27, 0.36).move_to([0, -0.1, 0])
        with self.voiceover(
            "Alarms are the vigilance problem turned round. <bookmark mark='a'/> On a hospital ward, patient monitors "
            "can sound hundreds of alarms a day, and most require no action. <bookmark mark='b'/> Staff learn, "
            "correctly, that an alarm usually means nothing, and respond more slowly or silence it: alarm fatigue, "
            "which patient-safety bodies have listed among the leading hazards of medical technology. "
            "<bookmark mark='c'/> It's the criterion from chapter eleven, set by the base rate, and the rare true "
            "alarm pays for it. <bookmark mark='d'/> The fixes are design: fewer and smarter alarms, distinct sounds "
            "for distinct levels of urgency, and short delays so that brief blips which correct themselves never "
            "sound. <bookmark mark='e'/> Aviation and process control learned this first. In a cockpit every warning "
            "competes for the same limited channel, so warnings are ranked, and the most urgent silences the rest."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def screens(self):
        head = heading(r"Roads and screens")
        rows = rows_of([
            (r"driving: \ laws ban holding a phone; \ the evidence says the conversation is the problem", BAD),
            (r"in-car touchscreens and voice assistants are tested for how long they take the eyes and the mind", ATT),
            (r"advertising sells attention: \ an ad counts as viewable if half of it is on screen for a second", CONTROL),
            (r"on screen is not attended: \ eye tracking and recall show how much of that is never seen", GREY_A),
            (r"design for attention, \ and design against it: \ Part 52 returns to both", YOU),
        ], 12.4, 27, 0.36).move_to([0, -0.1, 0])
        tag = published_tag(archive.STRAYER_2001.cite)
        with self.voiceover(
            "Two more places. <bookmark mark='a'/> On the road, many laws ban holding a phone while driving and allow "
            "hands-free calls, but the evidence says the cost is in the conversation. <bookmark mark='b'/> Car "
            "makers now test touchscreens and voice assistants for how long they take the eyes off the road and the "
            "mind off driving. <bookmark mark='c'/> On screens, attention is the product being sold. An online display "
            "ad is counted as viewable, by an industry standard, if half its pixels are on screen for one second. "
            "<bookmark mark='d'/> Being on screen is not the same as being attended, as eye-tracking and recall "
            "studies show, and buyers increasingly pay for measures of attention rather than exposure. "
            "<bookmark mark='e'/> Designing for attention, and designing to capture it against people's own "
            "interests, return in Part 52."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
