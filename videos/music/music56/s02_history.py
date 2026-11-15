from __future__ import annotations

import math

from videos.music.music56.common import *  # noqa: F403


class History(SoundScene):
    def construct(self):
        chapter(self, 1, r"From the horn to the workstation", r"How did a record stop being a performance?")
        self.timeline()
        self.tape()
        self.bounce()
        self.daw()

    # ------------------------------------------------------------------
    def timeline(self):
        d = load("history")
        rows = d["rows"]
        ax = frame_axes(width=10.4, height=3.2, xlo=1870, xhi=2025, ylo=0, yhi=math.log10(300), center=DOWN * 0.5)
        dots = VGroup()
        tags = VGroup()
        for i, r in enumerate(rows):
            p = ax.to(r["year"], math.log10(r["tracks"]))
            dots.add(Dot(p, radius=0.08, color=TUNE if r["year"] < 1990 else EAR))
            tags.add(label(rf"{r['year']}: \ {r['tracks']}", font_size=13, color=GREY_A).next_to(p, UP if i % 2 == 0 else DOWN, buff=0.12))
        steps = VMobject(stroke_color=GREY_B, stroke_width=2).set_points_as_corners([ax.to(r["year"], math.log10(r["tracks"])) for r in rows])
        yt = VGroup(*[label(f"{v}", font_size=14, color=GREY_A).next_to(ax.to(1870, math.log10(v)), LEFT, buff=0.12) for v in (1, 4, 24, 256)])
        xt = VGroup(*[label(f"{v}", font_size=14, color=GREY_A).next_to(ax.to(v, 0), DOWN, buff=0.12) for v in (1880, 1920, 1960, 2000)])
        yl = label(r"tracks \ (log scale)", font_size=15, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        note = label(r"one horn, \ one groove, \ one take \ $\to$ \ hundreds of tracks, \ every one editable", font_size=18, color=WHITE).to_edge(DOWN, buff=0.35)
        head = label(r"tracks against years", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Count the tracks a studio could record separately, year by year. <bookmark mark='a'/> From Edison's tinfoil in "
            "1877 to the 1940s, one: a horn or a microphone, cutting one groove, in one take. <bookmark mark='b'/> Magnetic "
            "tape arrived after the war, and Les Paul had an eight-track machine by 1957. The Beatles made Sergeant Pepper "
            "in 1967 on four tracks, bouncing them together to free more; by 1974 machines had twenty-four. "
            "<bookmark mark='c'/> Then digital tape, and in 1991 a computer with four tracks, Pro Tools, whose descendants "
            "hold as many as the computer can. A record stopped being a performance and became an object built in layers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yt), FadeIn(xt), FadeIn(yl), FadeIn(ghost(VGroup(steps, dots), 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(dots[:3]), FadeIn(tags[:3]))
            vo.wait_until("b")
            self.play(FadeIn(dots[3:6]), FadeIn(tags[3:6]), Create(steps), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(dots[6:]), FadeIn(tags[6:]), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tape(self):
        items = [
            (r"1947 to 1948: \ magnetic tape, \ from German Magnetophons; \ Bing Crosby records his radio shows on it", WHITE),
            (r"tape can be cut with a razor blade and spliced: \ the best of several takes, \ joined at a 45-degree angle", WHITE),
            (r"Les Paul's sound on sound: \ play along with yourself, \ again and again", WHITE),
            (r"multitrack: \ several parallel tracks on one tape, \ each recorded and re-recorded on its own", WHITE),
            (r"from then on, \ a performance could be assembled, \ not just captured", TUNE),
        ]
        rows_scene(self, r"tape", items,
                   "Tape changed everything. <bookmark mark='b'/> Magnetic tape came to America from captured German Magnetophons, "
                   "and in 1947 and 1948 Bing Crosby began recording his radio shows on it. <bookmark mark='c'/> Tape can be cut "
                   "with a razor blade and spliced, so the best parts of several takes can be joined, at a forty-five degree angle "
                   "to soften the join. <bookmark mark='d'/> Les Paul played along with himself, layer on layer, sound on sound. "
                   "<bookmark mark='e'/> Then multitrack: several parallel tracks on one tape, each recorded and re-recorded on its "
                   "own. <bookmark mark='f'/> From then on a performance could be assembled, not just captured.", marks="bcdef")

    # ------------------------------------------------------------------
    def bounce(self):
        items = [
            (r"four tracks are not many: \ record three, \ mix them onto the fourth, \ and erase the three", WHITE),
            (r"each bounce commits the balance for good, \ and adds a generation of tape hiss and loss", WHITE),
            (r"so engineers mixed as they went: \ decisions made early, \ and lived with", WHITE),
            (r"more tracks moved the decisions later, \ to the mix; \ the mix became a craft of its own", TUNE),
        ]
        rows_scene(self, r"bouncing", items,
                   "Four tracks are not many. <bookmark mark='b'/> To get more, record three, mix them onto the fourth, and erase "
                   "the three for new parts: bouncing. <bookmark mark='c'/> But each bounce commits a balance for good, and adds a "
                   "generation of tape hiss and loss. <bookmark mark='d'/> So engineers mixed as they went, making decisions early "
                   "and living with them. <bookmark mark='e'/> More tracks moved the decisions later, to the end, to the mix, which "
                   "became a craft of its own.", marks="bcde")

    # ------------------------------------------------------------------
    def daw(self):
        items = [
            (r"the workstation \ (Part 53): \ every track a file, \ every edit undoable, \ every setting saved", WHITE),
            (r"the console became software: \ faders, \ equalizers, \ compressors, \ reverberators as plug-ins", WHITE),
            (r"nothing need be decided until the end, \ and many decisions never are", WHITE),
            (r"what stayed the same is what this part is about: \ microphones, \ gain, \ balance, \ masking, \ space, \ the ear", TUNE),
        ]
        rows_scene(self, r"the workstation", items,
                   "Then the computer. <bookmark mark='b'/> In the workstation of Part 53 every track is a file, every edit can be "
                   "undone, every setting is saved. <bookmark mark='c'/> The console became software, its faders, equalizers, "
                   "compressors and reverberators plug-ins. <bookmark mark='d'/> Nothing need be decided until the end, and many "
                   "decisions never are. <bookmark mark='e'/> What stayed the same is what this part is about: microphones, gain, "
                   "balance, masking, space, and the ear.", marks="bcde")
