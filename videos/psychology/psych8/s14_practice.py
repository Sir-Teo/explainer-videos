from __future__ import annotations

import numpy as np

from videos.psychology.psych8.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.works()
        self.detector()
        self.sold()
        self.questions()

    def card(self):
        card = chapter_card(13, r"In practice: what is sold, and what works", r"Which uses of a brain measure have earned their place?",
                            lit=(), part=PART, scale=("brain", "person"), marr=("why",))
        with self.voiceover(
            "Chapter thirteen. In practice: what is sold, and what works."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def works(self):
        head = heading(r"Where these instruments are everyday tools")
        items = [
            (r"epilepsy", r"the EEG shows a seizure as it happens, \ and often where it starts", EEGC),
            (r"sleep", r"the stages of sleep are defined by the EEG's rhythms (Part 10)", EEGC),
            (r"before brain surgery", r"a functional scan finds one patient's language and movement areas; \ "
                                      r"the surgeon checks them by stimulation", BLOOD),
            (r"anatomy", r"a structural scan shows a stroke, a tumour, \ the loss of tissue in dementia", VOLT),
        ]
        rows = VGroup()
        for name, what, col in items:
            rows.add(VGroup(label(name, font_size=34, color=col), wrapped_label(what, 12.2, 29, WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.06))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to([0, 0.2, 0])
        end = wrapped_label(r"What they share: \ one person, \ a large effect, \ a question about that person's "
                            r"brain, \ and an independent check.", 12.6, 30, P.ACCENT).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Outside the laboratory, where have these instruments earned a place? <bookmark mark='a'/> In "
            "epilepsy. A seizure is the largest electrical event a brain produces, and the EEG shows it as "
            "it happens. <bookmark mark='b'/> In sleep medicine. The stages of sleep are defined by the "
            "rhythms of the EEG, which is Part 10. <bookmark mark='c'/> Before brain surgery. A functional "
            "scan can find where one patient's language and hand movements live, and the surgeon then "
            "checks by stimulating the cortex directly, as Penfield did. <bookmark mark='d'/> And "
            "everywhere, the structural scan, which shows a stroke or a tumour. <bookmark mark='e'/> Look "
            "at what those have in common. One person. A large effect. A question about that person's "
            "brain, not their character. And an independent way to check the answer. Now look at what's "
            "sold beyond that."
        ) as vo:
            self.play(FadeIn(head))
            for k, mark_ in enumerate("abcd"):
                vo.wait_until(mark_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def detector(self):
        d = load("detector")
        g = archive.GANIS_2011.data
        head = heading(r"A lie detector that is right nine times in ten")
        n = d["people"] // 10  # one figure for every ten people
        people = VGroup()
        for k in range(n):
            liar = k < d["liars"] // 10
            flagged = (liar and k < d["caught"] // 10) or (not liar and k >= n - d["false_alarms"] // 10)
            body = Circle(radius=0.15, stroke_width=3.5 if flagged else 0, stroke_color=THRESH,
                          fill_color=BAD if liar else NOISE, fill_opacity=0.9)
            people.add(body)
        people.arrange_in_grid(rows=10, buff=0.15).move_to([-4.3, 0.0, 0])
        cap = VGroup(
            VGroup(Circle(radius=0.12, stroke_width=0, fill_color=BAD, fill_opacity=0.9),
                   label(r"lying", font_size=24, color=BAD)).arrange(RIGHT, buff=0.12),
            VGroup(Circle(radius=0.12, stroke_width=0, fill_color=NOISE, fill_opacity=0.9),
                   label(r"truthful", font_size=24, color=NOISE)).arrange(RIGHT, buff=0.12),
            VGroup(Circle(radius=0.12, stroke_width=3, stroke_color=THRESH, fill_opacity=0),
                   label(r"flagged by the scan", font_size=24, color=THRESH)).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.35).next_to(people, DOWN, buff=0.25)
        keep_in_frame(cap)
        pl = label(rf"{fmt_int(d['people'])} people; \ each figure is ten", font_size=24, color=GREY_A).next_to(people, UP, buff=0.2)
        rows = rows_of([
            (rf"{d['liars']} are lying: \ the scan flags {d['caught']} of them", BAD),
            (rf"{d['people'] - d['liars']} are truthful: \ it flags {d['false_alarms']} of them too", NOISE),
            (rf"of those it flags, \ {pct(d['at_tenth'])} are telling the truth", THRESH),
            (rf"and with a rehearsed twitch of a toe: \ {pct(g['without'])} caught became {pct(g['with'])}", DATA),
        ], 5.8, 31, 0.34).move_to([3.9, -0.1, 0])
        keep_in_frame(rows)
        src = published_tag(archive.GANIS_2011.cite)
        tag = note(r"the first three lines: arithmetic on assumed rates").to_corner(DR, buff=0.15)
        with self.voiceover(
            "Take lie detection by brain scan, which has been offered to courts and to employers. Be "
            "generous. Suppose it's right nine times in ten, on liars and on honest people alike. "
            f"<bookmark mark='a'/> Test {d['people']:,} people, of whom one in ten is lying. Of the "
            f"{d['liars']} liars, it flags {d['caught']}. <bookmark mark='b'/> Of the "
            f"{d['people'] - d['liars']} honest people, it wrongly flags one in ten: {d['false_alarms']}. "
            "<bookmark mark='c'/> So of the people it calls liars, half are telling the truth. That's "
            "Bayes' rule again, the same sum as reverse inference, and no improvement in the scanner "
            "changes it. Only a better base rate does. <bookmark mark='d'/> And nine in ten is a "
            "laboratory figure, from volunteers with nothing at stake who weren't trying to beat it. "
            "When volunteers in one study were taught to move a toe at chosen moments, detection fell "
            f"from {100 * g['without']:.0f} percent to {100 * g['with']:.0f}. That's today's third Ledger "
            "row, and it's why courts have kept it out."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(people, lag_ratio=0.01), FadeIn(pl), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def sold(self):
        o = archive.OWEN_2010.data
        head = heading(r"Brain training: \ the product and the test")
        left = VGroup(
            label(r"the promise", font_size=40, color=BLOOD),
            wrapped_label(r"play these games for minutes a day: \ sharper memory, \ better at work and school, \ "
                          r"protection against decline", 6.0, 33, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        right = VGroup(
            label(r"the test", font_size=40, color=MODEL),
            wrapped_label(rf"{fmt_int(o['completed'])} adults, \ {o['weeks']} weeks, \ assigned at random", 6.0, 33, WHITE),
            wrapped_label(r"better at every game they practised", 6.0, 33, MODEL),
            wrapped_label(r"no better at anything they had not practised", 6.0, 33, BAD),
            wrapped_label(rf"{o['settlement_year']}: \ one company pays 2 million dollars to settle a charge of "
                          r"deceptive advertising", 6.0, 33, DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        cols = VGroup(left, right).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to([0, -0.2, 0])
        if cols.width > 13.2:
            cols.width = 13.2
        src = published_tag(archive.OWEN_2010.cite)
        with self.voiceover(
            "The second product has nothing to do with scanners, and everything to do with the word "
            "brain. <bookmark mark='a'/> Brain-training games promised that a few minutes a day would "
            "sharpen memory and attention in general, at work, at school, and into old age. "
            f"<bookmark mark='b'/> In 2010 that was tested on {o['completed']:,} adults, assigned at "
            f"random to different kinds of training for {o['weeks']} weeks. <bookmark mark='c'/> They "
            "improved at every game they practised. <bookmark mark='d'/> On tests of things they hadn't "
            "practised, even closely related things, they improved no more than a comparison group that "
            f"hadn't trained on such games. <bookmark mark='e'/> In {o['settlement_year']} one well-known "
            "company in the business paid two million dollars to settle a charge of deceptive "
            "advertising, without admitting fault. This one is also on the Ledger. It teaches something "
            "about the mind, too. Skills are narrower than we'd like, and that comes back in Part 54."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(left, lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(right[0]), FadeIn(right[1]))
            vo.wait_until("c")
            self.play(FadeIn(right[2]))
            vo.wait_until("d")
            self.play(FadeIn(right[3]))
            vo.wait_until("e")
            self.play(FadeIn(right[4], shift=UP * 0.1))
        self.clear_scene()

    def questions(self):
        head = heading(r"Six questions for any claim that comes with a picture of a brain")
        items = [
            (r"How many tests are in the picture, \ and how was the threshold set?", THRESH),
            (r"Were the voxels chosen with the same data that the number comes from?", THRESH),
            (r"How many people? \ And how reliable is the measure, \ person by person?", EEGC),
            (r"Does the claim run forward, from task to brain, \ or backward, from brain to mind?", BLOOD),
            (r"Was the prediction tested on people the model had never seen?", MODEL),
            (r"What would the same study have shown without the scanner?", P.ACCENT),
        ]
        rows = VGroup(*[wrapped_label(rf"{k + 1}. \ {t}", 12.6, 32, col) for k, (t, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.55)
        keep_in_frame(rows)
        with self.voiceover(
            "So here's what to carry out of this part: six questions for any claim that arrives with a "
            "picture of a brain. <bookmark mark='a'/> How many tests are in the picture, and how was the "
            "line drawn? <bookmark mark='b'/> Were the voxels chosen with the same data the number comes "
            "from? <bookmark mark='c'/> How many people, and how reliable is the measure in each of them? "
            "<bookmark mark='d'/> Does the claim run forward, from task to brain, or backward, from brain "
            "to mind? <bookmark mark='e'/> Was the prediction tested on people the model had never seen? "
            "<bookmark mark='f'/> And the one that's asked least: what would the same study have shown "
            "without the scanner? A picture of a brain makes an explanation feel more solid. Often the "
            "behaviour already told you everything the picture does."
        ) as vo:
            self.play(FadeIn(head))
            for k, mark_ in enumerate("abcdef"):
                vo.wait_until(mark_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
        self.clear_scene()
