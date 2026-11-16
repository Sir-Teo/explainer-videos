from __future__ import annotations

import numpy as np

from videos.music.music21.common import *  # noqa: F403

KEY_C = {"C major": "#F5C542", "G major": "#F472B6", "A minor": "#7DD3FC", "F major": "#A3E635", "D minor": "#C084FC", "E minor": "#94A3B8"}


def key_strip(keys, total, width=11.0, height=0.4):
    g = VGroup()
    step = keys[1]["t"] - keys[0]["t"] if len(keys) > 1 else 2
    for k in keys:
        w = width * step / total
        r = Rectangle(width=w, height=height, stroke_width=0, fill_color=KEY_C.get(k["key"], GREY_B), fill_opacity=0.9)
        r.move_to([-width / 2 + width * (k["t"] + step / 2) / total, 0, 0])
        g.add(r)
    return g


class Sonata(SoundScene):
    def construct(self):
        chapter(self, 6, r"Sonata: \ a drama of keys", r"Why does a sonata go away, \ and how does it come back?", extra=((2006, r"Hepokoski and Darcy's sonata theory"),))
        self.plan()
        self.keys()
        self.near()
        self.drama()

    # ------------------------------------------------------------------
    def plan(self):
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"exposition: \ a first theme at home; \ a transition; \ a second theme in another key \ (often the dominant in major, or the relative major in minor)", WHITE),
            (r"development: \ fragments of the themes, \ through several keys, \ then back to the dominant", WHITE),
            (r"recapitulation: \ both themes again, \ the second now at home", WHITE),
            (r"the second theme's return in the home key is the resolution of the whole", TUNE),
            (r"rounded binary grown large: \ the plan of most first movements from 1750 to 1900", GREY_A))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"sonata form", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Sonata form is the plan of most first movements of symphonies, sonatas and quartets from about 1750 to "
            "1900. <bookmark mark='a'/> The exposition states a first theme at home, travels through a transition, and "
            "states a second theme in another key, often the dominant in major, or the relative major in minor. <bookmark mark='b'/> The development breaks the "
            "themes into fragments and takes them through several keys, then works its way back to the dominant. "
            "<bookmark mark='c'/> The recapitulation states both themes again, the second one now in the home key. "
            "<bookmark mark='d'/> That is the drama: what was stated away from home must be restated at home. "
            "<bookmark mark='e'/> It is rounded binary grown large, with the return in the second half made into an "
            "event."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def keys(self):
        d = load("sonata")
        total = d["total"]
        big = d["big"]
        names = list(big)
        st = strip([big[n][0] for n in names], names, total, width=11.0, height=0.5, colors={"exposition": "#F5C542", "development": "#7DD3FC", "recapitulation": "#A3E635"}, font_size=22).move_to(UP * 2.0)
        ks = key_strip(d["keys"], total).move_to(UP * 0.9)
        kl = label(r"Part 15's key finder, \ eight beats at a time", font_size=20, color=GREY_B).next_to(ks, DOWN, buff=0.15)
        legend = VGroup(*[VGroup(Square(side_length=0.22, stroke_width=0, fill_color=c_, fill_opacity=0.9), label(tex(k), font_size=20, color=GREY_A)).arrange(RIGHT, buff=0.12)
                          for k, c_ in KEY_C.items() if any(x["key"] == k for x in d["keys"])]).arrange(RIGHT, buff=0.35).next_to(kl, DOWN, buff=0.3)
        secs = VGroup(*[label(t, font_size=21, color=c_) for t, c_ in (
            (r"first theme: \ the Tune's opening, \ in C", WHITE),
            (r"second theme: \ the same opening upside down, \ in G", EAR),
            (r"development: \ its head in A minor, \ F, \ D minor, \ then the dominant", BLUE),
            (r"recapitulation: \ both themes in C", TUNE))]).arrange(DOWN, buff=0.22, aligned_edge=LEFT).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Here is the plan of a miniature sonata built on the Tune, which ends this part as Variation 21. "
            "<bookmark mark='a'/> Below the sections, the key that Part 15's key finder hears, eight beats at a time. "
            "<bookmark mark='b'/> The first theme is the Tune's opening, in C. The second theme is the same opening "
            "turned upside down, in G. <bookmark mark='c'/> The development takes the Tune's first notes through A "
            "minor, F major and D minor, and arrives on the dominant. <bookmark mark='d'/> The recapitulation brings "
            "both themes back in C. The colours tell the story without a note being heard: home, away, far away, home."
        ) as vo:
            self.play(FadeIn(st))
            vo.wait_until("a")
            self.play(FadeIn(ks), FadeIn(kl), FadeIn(legend))
            vo.wait_until("b")
            self.play(FadeIn(secs[0]), FadeIn(secs[1]))
            vo.wait_until("c")
            self.play(FadeIn(secs[2]))
            vo.wait_until("d")
            self.play(FadeIn(secs[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def near(self):
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"the keys the development visits: \ A minor, \ F major, \ D minor, \ then G", WHITE),
            (r"Part 19's pathfinder: \ each is one pivot chord from C", WHITE),
            (r"the miniature never leaves C's neighbourhood", WHITE),
            (r"other developments explore remote tonal regions; \ Part 19's pivot graph has maximum distance two", TUNE),
            (r"tonal journeys can shape a return; \ graph distance is not a law of emotional strength", EAR))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"how far does the development go?", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "How far does the miniature travel? <bookmark mark='a'/> Its development visits A minor, F major and D minor before the dominant. <bookmark mark='b'/> Ask Part 19's pathfinder: every one of them is a single pivot chord away from C. <bookmark mark='c'/> The miniature never leaves C's neighbourhood. <bookmark mark='d'/> Other developments, including Beethoven’s, may explore more remote tonal regions; in Part 19’s particular pivot graph every key is at most two edges away. Enharmonic changes offer additional routes. <bookmark mark='e'/> A return can suggest homecoming, without a proven proportional law relating feeling to graph distance."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def drama(self):
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"Hepokoski and Darcy, \ 2006: \ the exposition is a journey with a goal", WHITE),
            (r"the medial caesura: \ a pause on the new dominant, \ the door to the second theme", WHITE),
            (r"the essential expositional closure: \ the first full cadence in the new key", WHITE),
            (r"the recapitulation must reach the same cadence at home: \ the essential structural closure", TUNE),
            (r"form as a set of expectations, \ which a composer meets, \ delays or defies", GREY_A))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"sonata theory", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "In 2006 James Hepokoski and Warren Darcy described the exposition as a journey with a goal. <bookmark mark='a'/> <bookmark mark='b'/> The transition ends with a pause on the new key's dominant, the medial caesura, a door through which the second theme enters. In the miniature sonata it is the transition's last chord, D major. <bookmark mark='c'/> In this theory, essential expositional closure is the first satisfactory perfect authentic cadence in the secondary-theme zone, with exclusions and exceptions. <bookmark mark='d'/> And the recapitulation must reach the same cadence at home, the moment the whole movement has been heading for. <bookmark mark='e'/> Seen this way, a form is a set of expectations that a composer can meet, delay or defy, and the drama is in which."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
