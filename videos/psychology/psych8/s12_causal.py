from __future__ import annotations

import numpy as np

from videos.psychology.psych8.common import *  # noqa: F403
from videos.psychology.psych7.common import brain_side, at, lesion_mark  # the series' brain drawing


class Causal(VoiceoverScene):
    def construct(self):
        self.card()
        self.watching()
        self.ladder()
        self.settled()

    def card(self):
        card = chapter_card(11, r"From watching to intervening", r"Is the active region doing the work?",
                            lit={1985: r"TMS"}, part=PART, scale=("circuit", "brain"), marr=("tissue",))
        with self.voiceover(
            "Chapter eleven. From watching to intervening."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def watching(self):
        head = heading(r"A scan is an observation")
        brain = brain_side(5.0, fill=0.2).move_to([-4.2, -0.2, 0])
        spot = Dot(at(brain, -0.35, 0.1), radius=0.32, color=THRESH, fill_opacity=0.85)
        rows = rows_of([
            (r"the region is more active \emph{while} the task is done", WHITE),
            (r"it might be doing the work", MODEL),
            (r"it might be listening in, \ or bracing, \ or tidying up afterwards", NOISE),
            (r"activity goes \emph{with} the task. \ Whether the task \emph{needs} it is a different question, \ "
             r"and Part 2 said how to ask it: \ intervene.", P.ACCENT),
        ], 6.2, 30, 0.32).move_to([3.4, -0.2, 0])
        keep_in_frame(rows)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Suppose every warning so far has been heeded. The threshold is honest, the voxels were chosen "
            "independently, and the claim runs forward. <bookmark mark='a'/> What you have is this: a "
            "region is more active while people do the task. <bookmark mark='b'/> It may be doing the "
            "work. <bookmark mark='c'/> It may also be listening in on a region that does the work, or "
            "preparing for a response that never has to be made, or clearing up afterwards. All of those "
            "light up. <bookmark mark='d'/> Activity that goes with a task is a correlation, measured "
            "inside one head. You know from Part 2 what it takes to go further. You have to intervene: "
            "change the region, and see what happens to the task."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(brain))
            vo.wait_until("a")
            self.play(FadeIn(spot, scale=0.5), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def ladder(self):
        head = heading(r"Four ways to intervene")
        items = [
            (r"damage", r"Part 7: \ a region is lost; \ nature chooses where", r"needed?", NOISE),
            (r"a magnetic pulse", r"1985: \ a coil on the scalp disturbs a patch of cortex for a fraction of a "
                                  r"second, \ in healthy people, \ where and when you choose", r"needed, and when?", EEGC),
            (r"a current, during surgery", r"Penfield's method: \ switch a spot on or off in an awake patient",
             r"needed? \ enough?", DATA),
            (r"light, in animals", r"cells made sensitive to light can be switched on or off by type, \ to the "
                                   r"millisecond", r"enough?", MODEL),
        ]
        rows = VGroup()
        for name, what, asks, col in items:
            left = VGroup(label(name, font_size=36, color=col), wrapped_label(what, 9.0, 30, WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.06)
            right = label(asks, font_size=31, color=col)
            rows.add(VGroup(left, right).arrange(RIGHT, buff=0.45))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to([0, 0.45, 0])
        for r in rows:
            r[1].align_to(rows[1][1], LEFT)
        keep_in_frame(rows)
        end = wrapped_label(r"Remove it and the task fails: \ necessary. \ \ Switch it on and the behaviour "
                            r"appears: \ sufficient. \ \ A scan shows neither.", 12.6, 29, P.ACCENT).to_edge(DOWN, buff=0.8)
        src = historical_tag(archive.BARKER_1985.cite)
        with self.voiceover(
            "There are four ways to do it. <bookmark mark='a'/> Damage, the subject of Part 7. It tests "
            "whether a region is needed, but nature picks the place. <bookmark mark='b'/> In 1985 Anthony "
            "Barker and his colleagues in Sheffield held a coil of wire against a volunteer's head and "
            "sent a brief, strong current through it. The magnetic pulse passed through the skull, and "
            "the volunteer's opposite hand twitched. A pulse like that disturbs a patch of cortex for a "
            "fraction of a second and leaves no trace. So you can ask, in a healthy person, whether a "
            "region is needed, and at what moment. <bookmark mark='c'/> During surgery, as Penfield did, a "
            "small current can switch a spot on or off while the patient talks. <bookmark mark='d'/> And "
            "in animals, cells can be made sensitive to light, and then switched on or off, one cell type "
            "at a time, to the millisecond. Part 6's memory experiment was done that way. "
            "<bookmark mark='e'/> Two words sort these out. Take a region away and the task fails: it was "
            "necessary. Switch it on and the behaviour appears: it was sufficient. A scan, by itself, "
            "shows neither."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for k, mark_ in enumerate("abcd"):
                vo.wait_until(mark_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def settled(self):
        head = heading(r"What scanning has settled, \ and what it has not")
        yes = VGroup(
            label(r"settled", font_size=36, color=MODEL),
            wrapped_label(r"the maps: \ vision, touch, movement and hearing laid out on the cortex, \ in the "
                          r"living human brain", 6.2, 31, WHITE),
            wrapped_label(r"that the same regions respond to the same kind of task, \ person after person: \ a "
                          r"patch that prefers faces, 1997", 6.2, 31, WHITE),
            wrapped_label(r"where a surgeon must not cut: \ language and movement, \ mapped in one patient", 6.2, 31, WHITE),
            wrapped_label(r"networks of regions that rise and fall together, \ even at rest", 6.2, 31, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        no = VGroup(
            label(r"not settled, or not so", font_size=36, color=BAD),
            wrapped_label(r"what one person is thinking, \ without their help and hours of their own data", 6.2, 31, WHITE),
            wrapped_label(r"a diagnosis of a mental disorder from one person's scan", 6.2, 31, WHITE),
            wrapped_label(r"``the centre'' for love, \ religion, \ or a brand of cola", 6.2, 31, WHITE),
            wrapped_label(r"how the activity computes anything: \ a map says where, \ not how", 6.2, 31, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        cols = VGroup(yes, no).arrange(RIGHT, buff=0.6, aligned_edge=UP).move_to([0, -0.35, 0])
        if cols.width > 13.4:
            cols.width = 13.4
        src = published_tag(archive.KANWISHER_1997.cite)
        with self.voiceover(
            "So here's a short, plain list. What has thirty years of scanning settled? "
            "<bookmark mark='a'/> The maps. The layouts of vision, touch, movement and hearing, which Part "
            "7 knew from wounds and surgery, have been charted in living, healthy people. "
            "<bookmark mark='b'/> That brains are alike: the same regions answer to the same kind of task "
            "in person after person. The best-known is a patch on the underside of the brain that "
            "responds more to faces than to anything else, reported in 1997 and found again ever since. "
            "What it's for is still argued, and that's Part 14. That one patient's language and movement areas can be found before an "
            "operation, so the surgeon can avoid them. And that regions form networks which rise and fall "
            "together even when a person is doing nothing. <bookmark mark='c'/> And what hasn't it "
            "delivered? Reading what one person is thinking, without their cooperation and hours of their "
            "own data. Diagnosing a mental disorder from an individual's scan. A centre for love, or "
            "religion, or a favourite brand. <bookmark mark='d'/> And the deepest gap: a map says where. "
            "It doesn't say how. Knowing which patch of cortex is busy during arithmetic tells you about "
            "as much about arithmetic as knowing which building a company is in tells you about its "
            "business."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(yes[0]), FadeIn(no[0]))
            vo.wait_until("a")
            self.play(FadeIn(yes[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in yes[2:]], lag_ratio=0.9), run_time=9.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in no[1:4]], lag_ratio=0.9), run_time=8.0)
            vo.wait_until("d")
            self.play(FadeIn(no[4], shift=UP * 0.1))
        self.clear_scene()
