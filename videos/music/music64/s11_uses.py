from __future__ import annotations

from videos.music.music64.common import *  # noqa: F403


class Uses(SoundScene):
    def construct(self):
        chapter(self, 10, r"What separation is for", r"Who needs a mix un-mixed?")
        self.uses()
        self.rights()
        self.listeners()

    # ------------------------------------------------------------------
    def uses(self):
        items = [
            (r"restoration: \ a voice lifted from a demo cassette; \ old mono recordings remixed in stereo", WHITE),
            (r"karaoke and practice: \ the voice removed, \ or the drums, \ so you can play along", WHITE),
            (r"remixing and sampling: \ a single stem from a finished record \ (Part 60's licences still apply)", WHITE),
            (r"upmixing: \ stereo spread to surround and Part 55's immersive formats", WHITE),
            (r"analysis: \ cleaner input for Part 61's transcribers and Part 62's chord recognizers", TUNE),
        ]
        rows_scene(self, r"uses", items,
                   "Who needs a mix un-mixed? <bookmark mark='b'/> Restorers: a voice lifted from a demo cassette, old mono "
                   "recordings remixed in stereo. <bookmark mark='c'/> Karaoke and practice: the voice removed, or the drums, so "
                   "you can play along. <bookmark mark='d'/> Remixers and samplers, taking a single stem from a finished record, "
                   "though Part 60's licences still apply. <bookmark mark='e'/> Upmixing: stereo spread to surround and to Part "
                   "55's immersive formats. <bookmark mark='f'/> And analysis: cleaner input for Part 61's transcribers and Part "
                   "62's chord recognizers.", marks="bcdef")

    # ------------------------------------------------------------------
    def rights(self):
        items = [
            (r"a separated stem is still a copy of the recording: \ the master's rights travel with it", WHITE),
            (r"the vocal of a famous singer, \ separated, \ is the raw material of voice cloning \ (Part 66)", WHITE),
            (r"services now separate on the phone, \ in real time: \ every record has become a multitrack", WHITE),
            (r"what used to be impossible is now a button, \ and the law has not caught up \ (dated)", TUNE),
        ]
        rows_scene(self, r"rights", items,
                   "Separation also raises questions. <bookmark mark='b'/> A separated stem is still a copy of the recording, and "
                   "the master's rights travel with it. <bookmark mark='c'/> The separated vocal of a famous singer is the raw "
                   "material of voice cloning, the subject of Part 66. <bookmark mark='d'/> Apps now separate on a phone, in real "
                   "time: every record has become a multitrack. <bookmark mark='e'/> What used to be impossible is now a button, "
                   "and the law has not caught up.", marks="bcde")

    # ------------------------------------------------------------------
    def listeners(self):
        items = [
            (r"the cocktail-party problem: \ Cherry \ (1953) \ asked how people follow one voice among many", WHITE),
            (r"people do not separate signals; \ they attend to streams \ (Bregman, \ 1990: \ auditory scene analysis)", WHITE),
            (r"cues: \ a common onset, \ harmonicity, \ a common location, \ continuity", WHITE),
            (r"the methods of this part borrow each cue: \ panning, \ harmonic templates, \ continuity in time", TUNE),
        ]
        rows_scene(self, r"how listeners do it", items,
                   "And how do listeners do it? <bookmark mark='b'/> Colin Cherry named the cocktail-party problem in 1953: how do "
                   "people follow one voice among many? <bookmark mark='c'/> People do not separate signals; they attend to streams, "
                   "as Albert Bregman's auditory scene analysis of 1990 described. <bookmark mark='d'/> Their cues: a common onset, "
                   "harmonicity, a common location, continuity. <bookmark mark='e'/> The methods of this part borrow each cue: "
                   "panning, harmonic templates, continuity in time.", marks="bcde")
