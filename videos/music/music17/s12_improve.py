from __future__ import annotations

import numpy as np

from videos.music.music17.common import *  # noqa: F403


class Improve(SoundScene):
    def construct(self):
        chapter(self, 11, r"Where we lose", r"What does the search not know?")
        self.missing()
        self.decorate()
        self.gap()

    # ------------------------------------------------------------------
    def missing(self):
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"it looks one chord back: \ no plan for a phrase, \ or for a whole chorale", WHITE),
            (r"it cannot tell a phrase's end from the piece's end", WHITE),
            (r"it never puts a note between the beats", WHITE),
            (r"it is paid for stillness: \ moving costs, \ and nothing rewards a line", WHITE),
            (r"it hears no words", GREY_A))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"what the search does not know", font_size=32, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Why does the search fall short? List what it does not know. <bookmark mark='a'/> It looks one "
            "chord back, so it has no plan: Bach's minor chorales travel to the relative major in the "
            "middle and come home at the end, and nothing in a table of pairs can arrange that. "
            "<bookmark mark='b'/> It cannot tell the end of a phrase from the end of the piece. "
            "<bookmark mark='c'/> It never writes a note between the beats. <bookmark mark='d'/> Its "
            "costs pay it for stillness: motion is penalized, and nothing rewards a good line. "
            "<bookmark mark='e'/> And it hears no words, while Bach sometimes chose a chord for a word."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def decorate(self):
        d = load("improve")
        c = clip("improve.decorated")
        g = choir_roll(d["voices"], width=10.0, height=3.4, lo=38, hi=80, thick=0.11).move_to(DOWN * 0.3)
        rule = label(r"a rule: \ where an alto, \ tenor or bass note moves a third, \ fill the third with a passing note, \ unless that makes a parallel", font_size=22, color=WHITE).to_edge(UP, buff=0.5)
        rule.scale_to_fit_width(min(rule.width, 12.6))
        with self.voiceover(
            "The third of these can be patched by a rule. Where an inner voice or the bass moves by a "
            "third from one beat to the next, split its note in two and put a passing note in the gap, "
            "unless that would make parallel fifths or octaves with another voice. Here is the search's "
            "harmonization of the third and fourth phrases again, with that rule applied."
        ):
            self.play(FadeIn(rule), FadeIn(g))
        with self.listen(c) as snd:
            window(snd, r"the search, \ with passing notes by rule", kind="synthesized", detail=r"a model choir", corner=DL, tag_corner=DR)
            sing_roll(snd, g, d["times"])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gap(self):
        d = load("improve")["notes_per_beat"]
        ch = columns([d["ours"], d["decorated"], d["bach"]], [r"the search", r"with passing notes", r"Bach"], width=6.0, height=2.6, color=WEAK, hot=(2,), hot_color=TUNE, fmt="{:.2f}", font_size=24).move_to(LEFT * 2.2 + DOWN * 0.5)
        t = label(r"notes a beat, \ alto, \ tenor and bass, \ on test chorales", font_size=24, color=GREY_A).next_to(ch, UP, buff=0.35)
        side = VGroup(label(r"a rule closes a little of the gap", font_size=26, color=WHITE),
                      label(r"the rest is planning lines over many beats", font_size=26, color=TUNE)).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(RIGHT * 4.0 + DOWN * 0.3)
        side.scale_to_fit_width(min(side.width, 5.4))
        side.move_to(RIGHT * 4.0 + DOWN * 0.3)
        with self.voiceover(
            "Count the notes in the lower three voices, per beat, across the test chorales. "
            f"<bookmark mark='a'/> The search writes {say(d['ours'], 2)} a beat: fewer than one, because it "
            f"holds notes. With the rule, {say(d['decorated'], 2)}. Bach writes {say(d['bach'], 2)}. "
            "<bookmark mark='b'/> A rule closes a little of the gap, and the passing notes help the sound. "
            "The rest is not a matter of decoration. It is the plan of each line over many beats, which "
            "is what composers mean by voice leading and what machines took decades to learn. That is the "
            "frontier."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(ch), FadeIn(t))
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()
