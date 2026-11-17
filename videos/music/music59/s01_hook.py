from __future__ import annotations

from videos.music.music59.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.story()
        self.after()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.two")
        card = listen_card(r"Headphones on. \ A band heard from the stands of a stadium, \ over a screaming crowd, \ twice: \ once through a "
                           r"1965 stadium system, \ once through a modern one. \ Which was 1965?", width=10.0)
        with self.voiceover(
            "In August 1965 the Beatles played Shea Stadium in New York. Put on headphones and judge first. A band heard from the stands of a stadium, over a screaming crowd, "
            "twice: once through our simplified historical-system model, once through a modern-system model; neither is an archival recording. Which was 1965?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"a stadium, \ twice", kind="physical model", detail=r"our session, \ a simulated crowd", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        res = label(r"the first: \ horns for announcements, \ band-limited and overdriven, \ 6 dB under the crowd", font_size=20, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover(
            "The first. A system built for announcing baseball scores, horns with no bass and no treble, driven into "
            "distortion, and still six decibels under the crowd. The second puts the band clearly above it, full range."
        ):
            self.play(boxes[0][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def story(self):
        items = [
            (r"15 August 1965: \ the Beatles at Shea Stadium, \ New York: \ some 55,000 people, \ then a record for a concert", WHITE),
            (r"the band's amplifiers: \ 100-watt Vox stacks; \ the voices: \ through the stadium's announcement horns", WHITE),
            (r"the screaming crowd was louder than all of it; \ the band could not hear itself play", WHITE),
            (r"they stopped touring a year later", WHITE),
            (r"the modern concert system was built to solve that night: \ power, \ coverage, \ monitors, \ and control", TUNE),
        ]
        rows_scene(self, r"Shea Stadium", items,
                   "That first system is a fair picture of a night in 1965. <bookmark mark='b'/> On the fifteenth of August the "
                   "Beatles played Shea Stadium in New York to some fifty-five thousand people, then a record for a concert. "
                   "<bookmark mark='c'/> The band's amplifiers were hundred-watt Vox stacks; the voices went through the stadium's "
                   "announcement horns. <bookmark mark='d'/> The screaming crowd was louder than all of it; the band could not hear "
                   "itself play. <bookmark mark='e'/> They stopped touring a year later. "
                   "<bookmark mark='f'/> Modern concert sound developed through many events and innovations to address these problems: power, coverage, monitors for the "
                   "musicians, and control.", marks="bcdef")

    # ------------------------------------------------------------------
    def after(self):
        items = [
            (r"1969, \ Woodstock: \ a purpose-built system of stacked horns and bass bins, \ hung on towers", WHITE),
            (r"1974: \ the Grateful Dead's Wall of Sound: \ hundreds of loudspeakers behind the band, \ a separate system for each instrument", WHITE),
            (r"1980s: \ standard boxes, \ flown in clusters; \ 1992: \ L-Acoustics' V-DOSC, \ the line array as a product", WHITE),
            (r"today: \ curved line arrays, \ subwoofer arrays, \ delay towers, \ in-ear monitors, \ all on a network", TUNE),
        ]
        rows_scene(self, r"after Shea", items,
                   "The answer was built in steps. <bookmark mark='b'/> At Woodstock in 1969, a purpose-built system of stacked horns "
                   "and bass bins, hung on towers. <bookmark mark='c'/> In 1974 the Grateful Dead's Wall of Sound: hundreds of "
                   "loudspeakers behind the band, a separate system for each instrument, and no monitors needed. "
                   "<bookmark mark='d'/> In the 1980s, standard boxes flown in clusters; and in 1992 L-Acoustics' V-DOSC made the "
                   "line array a product. <bookmark mark='e'/> Today: curved line arrays, subwoofer arrays, delay towers, in-ear "
                   "monitors, all on a network.", marks="bcde")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"why a microphone howls, \ predicted from the loop",
            r"ringing out, \ and monitors",
            r"point and line sources, \ arrays and their curvature",
            r"subwoofer arrays, \ delay towers, \ air and weather",
            r"measuring a system; \ wireless and networks",
            r"intelligibility, \ and how loud is too loud",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. Why a microphone howls, and how to predict the note. <bookmark mark='b'/> Ringing a system out, "
            "and monitors. <bookmark mark='c'/> Point and line sources, arrays, and why they are hung in curves. "
            "<bookmark mark='d'/> Subwoofer arrays, delay towers, and what air and weather do. <bookmark mark='e'/> Measuring a "
            "system, and wireless microphones and networks. <bookmark mark='f'/> And intelligibility, and how loud is too loud."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
