from __future__ import annotations

import numpy as np

from videos.music.music44.common import *  # noqa: F403


class Picture(SoundScene):
    def construct(self):
        chapter(self, 1, r"What music does to an image", r"Can music change what we see?")
        self.boltz()
        self.three()
        self.functions()
        self.theory()
        self.diegetic()
        self.mickey()

    # ------------------------------------------------------------------
    def boltz(self):
        items = [
            (r"Marilyn Boltz \ (2001): \ the same ambiguous film clips, \ with positive, \ negative or no music", WHITE),
            (r"viewers judged the characters' intentions by the music: \ a stranger was friendly or sinister", WHITE),
            (r"and they remembered objects that fitted the music's mood better than ones that did not", WHITE),
            (r"music does not decorate the picture: \ it tells the viewer how to read it", TUNE),
            (r"Annabel Cohen's model: \ music's associations attach to whatever on screen is congruent with it", GREY_A),
        ]
        rows_scene(self, r"music changes what we see", items,
                   "Does music change what we see? <bookmark mark='b'/> In 2001 Marilyn Boltz showed people the same ambiguous "
                   "film clips with positive music, negative music or none. <bookmark mark='c'/> They judged the characters' "
                   "intentions by the music: the same stranger was friendly or sinister. <bookmark mark='d'/> They even "
                   "remembered the objects that fitted the music's mood better. <bookmark mark='e'/> Music does not decorate a "
                   "picture; it tells the viewer how to read it. <bookmark mark='f'/> Annabel Cohen's model puts it this way: "
                   "music's associations attach to whatever on screen is congruent with it.", marks="bcdef")

    # ------------------------------------------------------------------
    def three(self):
        d = load("three")
        c = clip("three.three")
        st = stage()
        set_stage(st, 0.0)
        sp = strip()
        tags = {k: label(k, font_size=26, color=col).to_corner(UR, buff=0.5) for k, col in (("comic", TUNE), ("suspense", EAR), ("heroic", BLUE))}
        with self.voiceover(
            "Try it here. Our scene, three times, with three scores of ours, each written to the same three hit points: the "
            "door, the edge, and the landing. First comic, then suspense, then heroic. Watch the figure, and notice what "
            "you think it is."
        ):
            self.play(FadeIn(st), FadeIn(sp))
        st_ = d["starts"]
        keys = ["comic", "suspense", "heroic"]
        def t0(now):
            k = 0
            for i, kk in enumerate(keys):
                if now >= st_[kk]:
                    k = i
            return st_[keys[k]]
        with self.listen(c) as snd:
            window(snd, r"three scores", kind="synthesized", detail=r"piano, \ bass, \ additive orchestra, \ drums", corner=DL, tag_corner=DR)
            snd.drive(st.fig, lambda m, now: set_stage(st, now - t0(now)))
            snd.drive(sp.head, lambda m, now: m.move_to([sp.x0 + sp.width * min(max(now - t0(now), 0), sp.length) / sp.length, sp.y, 0]))
            for i, k in enumerate(keys):
                end = st_[keys[i + 1]] if i + 1 < 3 else c.duration + 1
                snd.show(tags[k])
                snd.drive(tags[k], lambda m, now, a=st_[k], b=end: m.set_opacity(1.0 if a <= now < b else 0.0))
        rows_ = text_rows([
            (r"comic: \ every footstep and action mirrored; \ a clumsy, \ harmless figure", TUNE),
            (r"suspense: \ low drones, \ a heartbeat, \ stabs at the hits; \ a figure in danger, \ or a dangerous one", EAR),
            (r"heroic: \ a horn motive, \ full chords; \ a brave figure, \ and a triumphant landing", BLUE),
        ], font_size=22)
        hd = label(r"one picture, \ three films", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        self.play(FadeOut(st), FadeOut(sp))
        with self.voiceover(
            "Three different films. <bookmark mark='a'/> The comic score mirrors every footstep and action, and the "
            "figure becomes clumsy and harmless. <bookmark mark='b'/> The suspense score, with low drones, a heartbeat and "
            "stabs at the hits, makes it a figure in danger, or a dangerous one. <bookmark mark='c'/> The heroic score gives "
            "it a horn motive and full chords, and the fall becomes a triumphant landing."
        ) as vo:
            self.play(FadeIn(hd), FadeIn(rows_.copy().set_opacity(0.15)))
            for mark, r in zip("abc", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def functions(self):
        items = [
            (r"set the place and period: \ a harpsichord, \ a synthesizer, \ a folk instrument", WHITE),
            (r"set the mood, \ and tell us what a character feels or hides", WHITE),
            (r"bind cuts together: \ music runs across shots and makes them one scene", WHITE),
            (r"point: \ a sting tells us where to look; \ a motif tells us who is near", TUNE),
            (r"and pace: \ the score's tempo becomes the scene's", GREY_A),
        ]
        rows_scene(self, r"what film music does", items,
                   "What does film music do? <bookmark mark='b'/> It sets the place and period, with a harpsichord, a "
                   "synthesizer or a folk instrument. <bookmark mark='c'/> It sets the mood, and tells us what a character feels "
                   "or hides. <bookmark mark='d'/> It binds cuts together: music running across shots makes them one scene. "
                   "<bookmark mark='e'/> It points: a sting tells us where to look, a motif who is near. <bookmark mark='f'/> And "
                   "it paces: the score's tempo becomes the scene's.", marks="bcdef")

    # ------------------------------------------------------------------
    def theory(self):
        items = [
            (r"Claudia Gorbman, \ \textit{Unheard Melodies} \ (1987): \ the classical score works unnoticed: \ it cues the story, \ "
             r"binds the shots and signals emotion", WHITE),
            (r"Michel Chion, \ \textit{Audio-Vision} \ (1990): \ sound and image are not added together, \ they are combined", WHITE),
            (r"added value: \ a sound makes us see something in the image, \ and we credit it to the image", WHITE),
            (r"synchresis: \ a sound and an image that coincide fuse into one event, \ whatever made them", TUNE),
            (r"why the late cut in the opening felt wrong, \ and why chapter 3 counts frames", GREY_A),
        ]
        rows_scene(self, r"two theories of the audiovisual", items,
                   "Two theories give names to what we have just heard. <bookmark mark='b'/> In 1987 Claudia Gorbman described "
                   "how the classical Hollywood score works: mostly unnoticed, cueing the story, binding the shots and "
                   "signalling emotion. <bookmark mark='c'/> Three years later the composer and critic Michel Chion argued "
                   "that sound and image are not added together, but combined. <bookmark mark='d'/> Sound adds value: it makes "
                   "us see something in the picture, and we credit what we saw to the picture. <bookmark mark='e'/> And a sound "
                   "and an image that coincide fuse into one event, whatever made them. Chion called that synchresis. "
                   "<bookmark mark='f'/> It is why the late cut in this part's opening felt wrong, and why chapter three counts "
                   "frames.", marks="bcdef")

    # ------------------------------------------------------------------
    def mickey(self):
        items = [
            (r"`Mickey-Mousing': \ music that mirrors every action, \ named after the Disney cartoons of the 1930s", WHITE),
            (r"Carl Stalling at Disney and Warner Bros. \ timed scores to the frame with click tracks", WHITE),
            (r"Max Steiner's \textit{King Kong} \ (1933) \ brought the technique into a feature film", WHITE),
            (r"used sparingly it is comic or emphatic; \ used everywhere it tires", TUNE),
            (r"chapter 2: \ music that follows characters rather than actions", GREY_A),
        ]
        rows_scene(self, r"Mickey-Mousing", items,
                   "Our comic score hit everything. <bookmark mark='b'/> That style is called Mickey-Mousing, after the Disney "
                   "cartoons of the 1930s, <bookmark mark='c'/> where composers such as Carl Stalling timed scores to the frame "
                   "with click tracks, later at Warner Brothers too. <bookmark mark='d'/> Max Steiner's King Kong of 1933 brought "
                   "the technique into a feature film. <bookmark mark='e'/> Used sparingly it is comic or emphatic; used "
                   "everywhere, it tires. <bookmark mark='f'/> Chapter two turns to music that follows characters rather than "
                   "actions.", marks="bcdef")

    # ------------------------------------------------------------------
    def diegetic(self):
        items = [
            (r"source music \ (diegetic): \ music the characters can hear \ --- \ a radio, \ a band in the scene", WHITE),
            (r"score \ (non-diegetic): \ music only the audience hears", WHITE),
            (r"films play with the line: \ a song on a radio swells into the score, \ or a character answers the score", WHITE),
            (r"games blur it further: \ the player's actions can make the music, \ inside the world", TUNE),
            (r"either way, \ the audience reads the scene through it", GREY_A),
        ]
        rows_scene(self, r"source and score", items,
                   "One more distinction. <bookmark mark='b'/> Source music, which film scholars call diegetic, is music the "
                   "characters can hear: a radio, a band in the scene. <bookmark mark='c'/> Score is music only the audience "
                   "hears. <bookmark mark='d'/> Films play with the line between them: a song on a radio swells into the score, "
                   "or a character seems to answer it. <bookmark mark='e'/> Games blur it further, when the player's actions make "
                   "the music inside the world. <bookmark mark='f'/> Either way, the audience reads the scene through it.",
                   marks="bcdef")
