from __future__ import annotations

import numpy as np

from videos.music.music14.common import *  # noqa: F403


class Leaps(SoundScene):
    def construct(self):
        chapter(self, 5, r"The rule that chance obeys", r"Why do leaps turn back?", extra=((2000, r"von Hippel and Huron"),))
        self.urn()
        self.dice()
        self.test()
        self.moral()

    # ------------------------------------------------------------------
    def urn(self):
        d = load("leaps")
        c = clip("leaps.urn")
        u = d["urn_melody"]
        r = roll(u, width=11.0, height=3.0, lo=-1, hi=13, lines=(), color=CHANCE_C).move_to(UP * 0.5)
        med = DashedLine([r.x(0), r.y(d["median"]), 0], [r.x(r.total), r.y(d["median"]), 0], color=WHITE, stroke_width=2)
        ml = label(r"the middle", font_size=22, color=WHITE).next_to(med, RIGHT, buff=0.1)
        head = label(r"twenty-four notes drawn from an urn: \ no memory, \ no composer", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Back to the leap rule. Why would shuffled notes obey it? Forget music for a moment. Here "
            "is an urn full of notes: many from the middle of an octave, fewer from the edges, as in a "
            "real tune. Draw twenty-four of them, each with no memory of the one before."
        ):
            self.play(FadeIn(head), FadeIn(r), Create(med), FadeIn(ml))
        with self.listen(c) as snd:
            window(snd, r"notes from an urn", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            sing(snd, r, d["urn_times"])
        # the first big leap away from the middle, and the note after it
        k = next(i for i in range(len(u) - 2) if abs(u[i + 1] - u[i]) >= 5 and abs(u[i + 1] - d["median"]) > abs(u[i] - d["median"]))
        box = SurroundingRectangle(VGroup(r.notes[k], r.notes[k + 1], r.notes[k + 2]), color=EAR, buff=0.12)
        cap = VGroup(label(r"a leap away from the middle lands near an edge;", font_size=28, color=WHITE), label(r"most of the urn lies back the way it came", font_size=28, color=WHITE),
                     label(r"regression to the mean", font_size=34, color=TUNE)).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Look at a leap in that. <bookmark mark='a'/> A big leap away from the middle has to land "
            "near an edge of the range. And from out there, where is the next note likely to be? Back "
            "toward the middle, because that is where most of the notes in the urn are. Not because of "
            "the leap. <bookmark mark='b'/> Statisticians call this regression to the mean: after an "
            "extreme value, the next is probably less extreme. Francis Galton found it in the heights of "
            "parents and children. Here it is in a melody that nobody wrote."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(box), FadeIn(cap[0]), FadeIn(cap[1]))
            vo.wait_until("b")
            self.play(FadeIn(cap[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def test(self):
        d = load("leaps")["kinds"]
        card = pause_card(r"A leap that lands \textit{nearer} the middle of the tune's range than it began. \ Does the next note turn back, \ or carry on?", width=9.0).move_to(UP * 0.3)
        with self.voiceover(
            "That gives a way to tell the two explanations apart. If composers turn back after leaps "
            "as a matter of craft, they should do it wherever the leap lands. If it is only regression "
            "to the mean, it should depend on where the leap lands. So, a prediction. Take a leap that "
            "lands nearer the middle of the tune's range than it started. Does the next note turn back, "
            "or carry on?"
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        rows = [(r"away from the middle", 100 * d["departing"]["real"], 100 * d["departing"]["shuffled"]), (r"across the middle", 100 * d["crossing"]["real"], 100 * d["crossing"]["shuffled"]),
                (r"toward the middle", 100 * d["approaching"]["real"], 100 * d["approaching"]["shuffled"])]
        pb = pair_bars(rows, width=10.0, height=2.6, names=(r"the 54 tunes", r"the same tunes, \ shuffled")).move_to(DOWN * 1.1)
        pb.legend.next_to(pb, UP, buff=0.35)
        head = label(r"how often the note after a leap turns back, \ in a hundred, \ by where the leap lands", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "It carries on: four times in five. <bookmark mark='a'/> When a leap heads away from the "
            f"middle, the tune turns back {say(100 * d['departing']['real'])} times in a hundred. "
            f"<bookmark mark='b'/> When it heads toward the middle, only "
            f"{say(100 * d['approaching']['real'])}. And shuffled notes show exactly the same pattern. "
            "<bookmark mark='c'/> In the year 2000, Paul von Hippel and David Huron showed this in "
            "hundreds of melodies from Europe, Africa, China and native America. The textbook rule is "
            "true as a description. As advice it is unnecessary: any melody in a limited range will "
            "follow it without being told."
        ) as vo:
            self.play(FadeOut(card), FadeIn(head), FadeIn(pb[0]), FadeIn(pb.legend), FadeIn(pb.groups[2]))
            vo.wait_until("a")
            self.play(FadeIn(pb.groups[0]))
            vo.wait_until("b")
            self.play(Indicate(pb.groups[2], color=WHITE, scale_factor=1.05), FadeIn(pb.groups[1]))
            vo.wait_until("c")
            self.play(FadeIn(label(r"P. von Hippel and D. Huron, \ \textit{Music Perception} \ (2000)", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.35)))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def moral(self):
        d = load("leaps")["kinds"]["all"]
        pb = pair_bars([(r"all leaps", 100 * d["real"], 100 * d["shuffled"])], width=3.6, height=2.6, names=(r"the tunes", r"by chance")).move_to(LEFT * 4.0 + DOWN * 0.6)
        pb.legend.next_to(pb, UP, buff=0.3)
        steps = VGroup(label(r"1. \ find a regularity", font_size=30, color=WHITE), label(r"2. \ ask what chance would do, \ under the same constraints", font_size=30, color=WHITE),
                       label(r"3. \ what is left over is the craft", font_size=32, color=TUNE)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 2.3 + UP * 0.2)
        with self.voiceover(
            "Notice what just happened, because it is the method of this whole part. A regularity in "
            "music is not yet a fact about composers. <bookmark mark='a'/> First ask what chance would "
            "do, under the same constraints. <bookmark mark='b'/> What is left over after that is the "
            f"craft. And here the leftover points the other way: real tunes turn back "
            f"{say(100 * d['real'])} times in a hundred, chance {say(100 * d['shuffled'])}. If "
            "anything, composers resist the rule. A real melody holds its direction longer than a "
            "shuffled one would."
        ) as vo:
            self.play(FadeIn(steps[0]), FadeIn(pb), FadeIn(pb.legend))
            vo.wait_until("a")
            self.play(FadeIn(steps[1]))
            vo.wait_until("b")
            self.play(FadeIn(steps[2]), Indicate(pb.groups[0], color=WHITE, scale_factor=1.05))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dice(self):
        d = load("more")["dice"]

        def die(n, color=WHITE):
            sq = RoundedRectangle(width=1.0, height=1.0, corner_radius=0.15, stroke_color=color, stroke_width=3)
            return VGroup(sq, label(str(n), font_size=44, color=color).move_to(sq))

        rolls3 = VGroup(die(2), die(5, EAR), die("?", GREY_B)).arrange(RIGHT, buff=0.6).move_to(UP * 1.6)
        arrow = label(r"a leap up", font_size=24, color=EAR).next_to(VGroup(rolls3[0], rolls3[1]), DOWN, buff=0.2)
        rows = VGroup(label(rf"rolls where the second die beats the first by two or more: \ {d['cases']}", font_size=26, color=WHITE),
                      label(rf"the third roll is lower: \ {d['fall']} \quad higher: \ {d['rise']} \quad the same: \ {d['same']}", font_size=26, color=WHITE),
                      label(rf"it turns back {100 * d['share']:.0f} times in a hundred", font_size=34, color=TUNE)).arrange(DOWN, buff=0.3).move_to(DOWN * 1.2)
        with self.voiceover(
            "You can check the argument with a die, and no music at all. Roll it three times. Suppose "
            "the second roll is higher than the first by two or more: a leap up. <bookmark mark='a'/> "
            f"There are {say(d['cases'])} ways that can happen, and on average the second roll is then a "
            f"{say(d['mean_landing'])}. Now the third roll. <bookmark mark='b'/> It is lower in "
            f"{say(d['fall'])} of those cases, and higher in only {say(d['rise'])}. The die turns back "
            f"{say(100 * d['share'])} times in a hundred. A die has no taste and no training. It has a "
            "range, from one to six, and that is enough."
        ) as vo:
            self.play(FadeIn(rolls3), FadeIn(arrow))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            self.play(FadeIn(rows[2]))
        self.wait(0.4)
        self.clear_scene()
