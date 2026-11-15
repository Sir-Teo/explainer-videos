from __future__ import annotations

import numpy as np

from videos.music.music44.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.story()
        self.silent()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.two")
        card = listen_card(r"A short animated scene, \ twice, \ with the same music. \ "
                           r"In one the music was cut to the picture; \ in the other it starts a little late. \ Which fits?", width=10.4)
        with self.voiceover(
            "A question for your eyes and ears together. A short animated scene, shown twice, with the same music both "
            "times. Once the music was cut to the picture; the other time it starts a little late. Which one fits?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        st = stage()
        set_stage(st, 0.0)
        sp = strip()
        tag = label(r"first", font_size=24, color=GREY_A).to_corner(UR, buff=0.5)
        self.play(FadeOut(card), FadeIn(st), FadeIn(sp))
        s1, s2 = d["starts"]["first"], d["starts"]["second"]
        with self.listen(c) as snd:
            window(snd, r"the scene, \ twice", kind="synthesized", detail=r"piano, \ bass, \ a glide, \ a drum", corner=DL, tag_corner=DR)
            snd.drive(st.fig, lambda m, now: set_stage(st, now - (s1 if now < s2 else s2)))
            snd.drive(sp.head, lambda m, now: m.move_to([sp.x0 + sp.width * min(max(now - (s1 if now < s2 else s2), 0), sp.length) / sp.length, sp.y, 0]))
            t2 = label(r"second", font_size=24, color=GREY_A).to_corner(UR, buff=0.5)
            snd.show(tag)
            snd.drive(tag, lambda m, now: m.set_opacity(1.0 if now < s2 else 0.0))
            snd.show(t2)
            snd.drive(t2, lambda m, now: m.set_opacity(1.0 if now >= s2 else 0.0))
        ans = label(rf"the first: \ in the second the music starts {d['offset']:.1f} s late, \ and every hit misses its action", font_size=20, color=TUNE).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"The first. In the second the music starts {say(d['offset'], 1)} seconds late, so the door creaks after it has "
            "opened, the trill teeters over empty ground, and the thump lands after the figure. The same music, moved by "
            "a fraction of a second, stops belonging to the picture. Film composers spend much of their craft on exactly "
            "these fractions."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def story(self):
        items = [
            (r"one scene, \ three scores, \ three different films: \ music decides much of what a picture means", WHITE),
            (r"film music is written to picture: \ timed to the frame, \ hitting actions and cuts on the beat", WHITE),
            (r"games broke that: \ nobody knows how long a scene will last, \ or what the player will do next", WHITE),
            (r"so game scores are systems: \ pieces that rearrange themselves as the game runs", TUNE),
            (r"this part works the arithmetic of hitting a cut, \ and builds a score that adapts", GREY_A),
        ]
        rows_scene(self, r"music for picture and play", items,
                   "Music decides much of what a picture means: one scene with three scores is three different films. "
                   "<bookmark mark='b'/> Film music is written to the picture, timed to the frame, with actions and cuts landing "
                   "on the beat. <bookmark mark='c'/> Games broke that: nobody knows how long a scene will last, or what the "
                   "player will do next. <bookmark mark='d'/> So game scores are systems: pieces that rearrange themselves as "
                   "the game runs. <bookmark mark='e'/> This part works the arithmetic of hitting a cut on the beat, and builds a "
                   "score that adapts.", marks="bcde")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"what music does to an image; \ leitmotifs",
            r"spotting, \ hit points, \ and the click track's arithmetic",
            r"a tempo that hits three actions",
            r"harmony on screen; \ music under dialogue",
            r"game music: \ an adaptive score driven by a game",
            r"a sound chip, \ and what its limits did to music",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. What music does to an image, and leitmotifs. <bookmark mark='b'/> Spotting, hit points and "
            "the click track's arithmetic. <bookmark mark='c'/> A tempo that hits three actions. <bookmark mark='d'/> "
            "Harmony on screen, and music under dialogue. <bookmark mark='e'/> Game music: an adaptive score driven by a "
            "simulated game. <bookmark mark='f'/> And a sound chip, and what its limits did to music."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def silent(self):
        items = [
            (r"`silent' films were never silent: \ a pianist, \ an organist or an orchestra played in every cinema", WHITE),
            (r"studios sent cue sheets: \ lists of scenes with suggested music and timings, \ from the 1910s", WHITE),
            (r"from 1926 the Vitaphone system put the score on a disc synchronised with the film", WHITE),
            (r"with sound film, \ the score became part of the film itself, \ timed to the frame", TUNE),
            (r"games, \ fifty years later, \ undid the fixed timing again", GREY_A),
        ]
        rows_scene(self, r"a short history", items,
                   "A short history. <bookmark mark='b'/> So-called silent films were never silent: a pianist, an organist or an "
                   "orchestra played in every cinema. <bookmark mark='c'/> From the 1910s studios sent cue sheets, lists of scenes "
                   "with suggested music and timings. <bookmark mark='d'/> From 1926 the Vitaphone system put a score on a disc "
                   "synchronised with the film, <bookmark mark='e'/> and with sound film the score became part of the film "
                   "itself, timed to the frame. <bookmark mark='f'/> Games, fifty years later, undid the fixed timing again.",
                   marks="bcdef")
