from __future__ import annotations

import numpy as np

from videos.music.music42.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.beethoven()
        self.ode()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.two")
        card = listen_card(r"Two eight-bar melodies, \ built from the same four-note idea over the same chords. \ "
                           r"A program wrote both, \ then threw one away. \ Which did it keep: \ the first or the second?", width=10.4)
        with self.voiceover(
            "Beethoven's sketchbooks of 1822 to 1824 show one tune approached in draft after draft. Now a program's drafts. Two eight-bar melodies, built from the same four-note idea over the same chords. A "
            "program wrote both, and then threw one of them away. Which did it keep, the first or the second?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        a = scored(d["first"]["melody"], load("search")["chords"], width=5.6, height=1.6, lo=57, hi=81, size=14)
        b = scored(d["kept"]["melody"], load("search")["chords"], width=5.6, height=1.6, lo=57, hi=81, size=14)
        pair = VGroup(VGroup(a, label(r"first", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.3),
                      VGroup(b, label(r"second", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.3)).arrange(RIGHT, buff=0.8).move_to(UP * 0.4)
        self.play(FadeOut(card), FadeIn(pair))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two drafts", detail=r"Part 7's piano, \ a plucked bass", corner=DL, tag_corner=DR)
            cursor(snd, a, st["first"], 0.42)
            cursor(snd, b, st["kept"], 0.42)
            pulse(snd, pair[0], st["first"], st["kept"] - 0.5, buff=0.1)
            pulse(snd, pair[1], st["kept"], c.duration, buff=0.1)
        ans = VGroup(label(r"first: \ draft 1, \ rejected: \ " + WHY[d['first']['why']], font_size=20, color=GREY_A),
                     label(rf"second: \ draft {d['kept']['draft']:,} of {d['drafts']:,}, \ the best the critics scored", font_size=20, color=TUNE)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            f"It kept the second. The first was its very first draft, rejected at once for {WHY_SAID[d['first']['why']]}. The "
            f"second was draft {say(d['kept']['draft'])} of {say(d['drafts'])}: {say(d['rejected'])} drafts were thrown away, "
            "and of the rest, this one scored best. By the end of this part you will know what the critics listen for, and "
            "you will have built them."
        ):
            self.play(FadeIn(ans), pair[1][0].frame.animate.set_stroke(TUNE, 2, opacity=1))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def beethoven(self):
        items = [
            (r"Beethoven planned to set Schiller's ode \textit{An die Freude} \ from 1793, \ thirty years before the Ninth", WHITE),
            (r"his sketchbooks of 1822 to 1824 show the tune approached in draft after draft", WHITE),
            (r"what survives is the search: \ ideas tried, \ varied, \ crossed out, \ tried again", WHITE),
            (r"composing as search under constraints: \ generate, \ judge, \ keep the best", TUNE),
            (r"this part builds the generators and the judges", GREY_A),
        ]
        rows_scene(self, r"a tune found by search", items,
                   "Composers have always searched. <bookmark mark='b'/> Beethoven planned to set Schiller's ode to joy from 1793, "
                   "thirty years before the Ninth Symphony. <bookmark mark='c'/> His sketchbooks of 1822 to 1824 show the tune "
                   "approached in draft after draft, <bookmark mark='d'/> and what survives on those pages is the search itself: "
                   "ideas tried, varied, crossed out and tried again. <bookmark mark='e'/> Composing, seen this way, is search "
                   "under constraints: generate, judge, keep the best. <bookmark mark='f'/> This part builds the generators and "
                   "the judges.", marks="cdef")

    # ------------------------------------------------------------------
    def ode(self):
        d = load("ode")
        c = clip("ode.theme")
        mel = d["melody"]
        g = scored(mel, None, width=11.0, height=1.8, lo=57, hi=70)
        g.move_to(UP * 0.6)
        stats = VGroup(label(rf"{d['moves']} moves: \ {d['steps']} steps, \ {d['repeats']} repeated notes, \ {d['leaps']} leaps", font_size=22, color=TUNE),
                       label(r"the plainest material: \ a scale, \ walked, \ with one rhythmic surprise at each phrase end", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=1.0)
        head = label(r"what the search found: \ the theme's first two phrases", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "And what did Beethoven's search find? Hear the theme's first two phrases, as the series' corpus has them."
        ):
            self.play(FadeIn(head), FadeIn(g))
        with self.listen(c) as snd:
            window(snd, r"the Ode to Joy", detail=r"Beethoven, \ 1824; \ Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, g.roll.notes, [n[1] * 0.45 for n in mel], hot=WHITE, base=TUNE)
        with self.voiceover(
            f"Count its moves. Of {say(d['moves'])}, {say(d['steps'])} are steps to a neighbouring note and "
            f"{say(d['repeats'])} repeat a note. There is not a single leap. Years of search ended at the plainest material "
            "there is: a scale, walked, with one rhythmic surprise at the end of each phrase. Search does not mean "
            "complication; the hard part is the judging."
        ):
            self.play(FadeIn(stats))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"the motive and its operations; \ developing variation",
            r"kinds of variation; \ planning tension",
            r"constraints counted; \ the dice games of the 1750s",
            r"generate and test: \ the \textit{Illiac Suite}, \ chains and evolution",
            r"a searcher with critics, \ and the drafts it threw away",
            r"what creativity might mean, \ and how to judge a machine's",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. The motive, the operations composers apply to it, and developing variation. "
            "<bookmark mark='b'/> The kinds of variation, and planning tension across a phrase. <bookmark mark='c'/> "
            "Constraints, counted exactly, and the dice games of the 1750s. <bookmark mark='d'/> Generate and test: the "
            "Illiac Suite, Markov chains, and evolution. <bookmark mark='e'/> A searcher with critics, and the drafts it threw "
            "away. <bookmark mark='f'/> And what creativity might mean, and how to judge a machine's."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
