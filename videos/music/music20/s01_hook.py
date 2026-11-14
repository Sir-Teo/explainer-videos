from __future__ import annotations

import numpy as np

from videos.music.music20.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.potsdam()
        self.offering()
        self.plan()

    # ------------------------------------------------------------------
    def potsdam(self):
        d = load("hook")
        c = clip("hook.royal")
        card = history_card(1747, r"Potsdam, \ 7 May", r"Frederick the Great hands Bach a theme, \ and asks for a fugue", width=10.0, font_size=26).to_edge(UP, buff=0.4)
        g = voices_roll([d["theme"]], width=11.0, height=2.6, total=26.0).move_to(DOWN * 0.9)
        with self.voiceover(
            "On the evening of the seventh of May, 1747, at the palace in Potsdam, King Frederick the Great of "
            "Prussia, a keen flautist, had a visitor: Johann Sebastian Bach, sixty-two years old. "
            "<bookmark mark='a'/> The king played him a theme, and asked him to improvise a fugue on it. Here it is, "
            "with its rhythm simplified: a minor triad climbing, a plunge of a diminished seventh, and then a slow "
            "chromatic slide."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(g))
        with self.listen(c) as snd:
            window(snd, r"the royal theme, \ rhythm simplified", detail=r"a plucked string", corner=DL, tag_corner=DR)
            sing_voices(snd, g, [d["theme"]], beat=0.36)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def offering(self):
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"Bach improvised a fugue in three voices on it, \ there and then", WHITE),
            (r"asked for six voices, \ he chose a theme of his own", WHITE),
            (r"two months later he sent the king the \textit{Musical Offering}", WHITE),
            (r"a six-voice fugue on the king's theme, \ and canons set as riddles", TUNE),
            (r"one played against itself backwards; \ one that rises a tone each time round", EAR))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"the \textit{Musical Offering}", font_size=32, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The theme seems made to resist being combined with itself: that chromatic slide is hard to set against "
            "its own copies. <bookmark mark='a'/> Bach improvised a fugue in three voices on it on the spot. "
            "<bookmark mark='b'/> When the king asked for six voices, he chose a theme of his own. "
            "<bookmark mark='c'/> Two months later he sent the king a printed answer, the Musical Offering. "
            "<bookmark mark='d'/> It holds a fugue in six voices on the king's theme, and a set of canons written as "
            "riddles: only one line is printed, and the reader must find how the other voices enter. "
            "<bookmark mark='e'/> One canon is played against itself backwards. Another rises a whole tone each time "
            "round, and its inscription hopes that the king's glory rises with it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        head = label(r"Part 20: \ Canon and Fugue", font_size=36, color=TUNE).to_edge(UP, buff=0.5)
        steps = VGroup(*[label(t, font_size=27, color=c_) for t, c_ in (
            (r"rounds, \ and canons at every interval, \ counted", WHITE),
            (r"the four forms of a line, \ and the group they make", WHITE),
            (r"invertible counterpoint, \ augmentation, \ riddle canons", WHITE),
            (r"the crab canon and the endless canon, \ solved and heard", EAR),
            (r"the fugue: \ subject, \ answer, \ countersubject, \ stretto", WHITE),
            (r"\textit{The Art of Fugue}, \ and fugues by machine", TUNE))]).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(DOWN * 0.1)
        with self.voiceover(
            "This part asks one question in many forms: which melodies can be combined with themselves? "
            "<bookmark mark='a'/> It starts with rounds, and counts the canons a computer can find at every "
            "interval. <bookmark mark='b'/> Then the four forms of a line, forwards, upside down and backwards, and "
            "the small group they make. <bookmark mark='c'/> Then lines that can swap places, lines against "
            "themselves slowed down, and canons set as riddles. <bookmark mark='d'/> Then the two canons of the "
            "Musical Offering, the crab and the endless climb, solved and heard. <bookmark mark='e'/> Then the "
            "fugue, built from its parts on the Tune. <bookmark mark='f'/> And at the end, The Art of Fugue, and what "
            "machines can do with all this."
        ) as vo:
            self.play(FadeIn(head), FadeIn(steps[0]))
            for mark, s in zip("bcdef", steps[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(s))
        self.wait(0.4)
        self.clear_scene()
