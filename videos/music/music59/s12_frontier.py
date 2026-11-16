from __future__ import annotations

from videos.music.music59.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 11, r"Frontier: \ immersive stages and quiet neighbours", r"Can a festival be loud inside and quiet outside?")
        self.immersive()
        self.zones()
        self.problem()

    # ------------------------------------------------------------------
    def immersive(self):
        items = [
            (r"left-right stereo works for a strip of seats down the middle; \ everyone else hears the nearer side", WHITE),
            (r"object-based live systems: \ five or more arrays across the stage, \ each source placed by delays and levels", WHITE),
            (r"the voice comes from the singer for most of the audience, \ not only those in the centre", WHITE),
            (r"Part 55's precedence effect and wave fields, \ scaled up to an arena", WHITE),
            (r"open questions: \ how many arrays, \ how far the image holds, \ and what the room's reflections do to it", TUNE),
        ]
        rows_scene(self, r"immersive live sound", items,
                   "Two frontiers. The first is space. <bookmark mark='b'/> Left-right stereo works only for a strip of seats down "
                   "the middle of a venue; everyone else hears the nearer side. <bookmark mark='c'/> Object-based live systems hang "
                   "five or more arrays across the stage and place each source among them by delays and levels. "
                   "<bookmark mark='d'/> The voice then comes from the singer for most of the audience, not only those in the "
                   "centre. <bookmark mark='e'/> It is Part 55's precedence effect and wave fields, scaled up to an arena. "
                   "<bookmark mark='f'/> And the questions are open: how many arrays, how far across the audience the image holds, "
                   "and what the room's reflections do to it.", marks="bcdef")

    # ------------------------------------------------------------------
    def zones(self):
        items = [
            (r"outdoor events carry noise limits at the nearest houses, \ often for the bass, \ which no barrier stops", WHITE),
            (r"bass carries kilometres, \ and the weather of Chapter 6 bends it down at night", WHITE),
            (r"cardioid and end-fire subwoofers aim it; \ optimized arrays can trade a little audience level for much less off site", WHITE),
            (r"sound zones: \ arrays driven so that one region is loud and another quiet, \ by the arithmetic of Chapter 5, \ in a room or a car", WHITE),
            (r"active control: \ loudspeakers at the edge of the field that cancel the bass beyond it \ (trials, \ not yet routine)", TUNE),
        ]
        rows_scene(self, r"quiet neighbours", items,
                   "The second is silence. <bookmark mark='b'/> Outdoor events carry noise limits at the nearest houses, usually "
                   "hardest on the bass, which ordinary small barriers attenuate less effectively than higher frequencies. <bookmark mark='c'/> Bass carries kilometres, and Chapter 6's weather "
                   "bends it down at night. <bookmark mark='d'/> Cardioid and end-fire subwoofers aim it, and optimized arrays can "
                   "trade a little level in the audience for much less off site. <bookmark mark='e'/> Sound zones push the idea "
                   "further: arrays driven so that one region is loud and another quiet, by Chapter 5's arithmetic, in a car or a "
                   "living room as well as a field. <bookmark mark='f'/> And active control puts loudspeakers at the edge of the "
                   "field to cancel the bass beyond it, so far in trials rather than routine use.", marks="bcdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"model a festival: \ arrays, \ subwoofers, \ the field, \ and houses a kilometre away", WHITE),
            (r"let the weather vary: \ wind and temperature profiles drawn from a year of measurements", WHITE),
            (r"choose every delay and filter to keep the audience even, \ and the houses under their limit", WHITE),
            (r"$\bigstar$ \ research problem: \ what settings hold the limit with 95\% confidence over the weather, \ and what do they cost the audience?", EAR),
            (r"an answer would turn a night of guessing at the desk into a plan", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A research problem to end on. <bookmark mark='a'/> Model a festival: its arrays and subwoofers, the field, and "
            "houses a kilometre away. <bookmark mark='b'/> Let the weather vary, with wind and temperature profiles drawn from a "
            "year of measurements. <bookmark mark='c'/> Choose every delay and filter to keep the audience even and the houses "
            "under their limit. <bookmark mark='d'/> The question: what settings hold the limit with ninety-five percent "
            "confidence over the weather, and what do they cost the audience? <bookmark mark='e'/> An answer would turn a night "
            "of guessing at the desk into a plan."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
