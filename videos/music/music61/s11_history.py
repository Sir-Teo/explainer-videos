from __future__ import annotations

from videos.music.music61.common import *  # noqa: F403


class History(SoundScene):
    def construct(self):
        chapter(self, 10, r"Fifty years of transcription", r"How did machines learn to write down what they hear?")
        self.early()
        self.data()
        self.ear()

    # ------------------------------------------------------------------
    def early(self):
        items = [
            (r"1975 to 1977: \ James Moorer at Stanford transcribes duets, \ if neither voice's pitch is a harmonic of the other's", WHITE),
            (r"the 1990s and 2000s: \ blackboards of rules, \ then statistics: \ Klapuri's harmonicity and spectral smoothness \ (2003)", WHITE),
            (r"2003: \ Smaragdis and Brown factorize a piano's spectrogram into notes: \ NMF", WHITE),
            (r"one voice: \ YIN \ (2002), \ SWIPE \ (2008), \ probabilistic YIN \ (2014), \ then CREPE, \ a network \ (2018)", WHITE),
            (r"2016: \ Sigtia, \ Benetos and Dixon: \ a network for polyphonic piano, \ end to end", TUNE),
        ]
        rows_scene(self, r"from rules to factors", items,
                   "The field is fifty years old. <bookmark mark='b'/> Between 1975 and 1977 James Moorer at Stanford had a program "
                   "transcribe duets, provided neither voice's pitch was a harmonic of the other's. <bookmark mark='c'/> Through the 1990s "
                   "and 2000s, systems of rules gave way to statistics: Anssi Klapuri's multiple-pitch estimator of 2003 used "
                   "harmonicity and the smoothness of real spectra. <bookmark mark='d'/> In 2003 Paris Smaragdis and Judith Brown "
                   "factorized a piano's spectrogram into notes, the method of Chapter 5. <bookmark mark='e'/> For a single voice, "
                   "YIN in 2002, then SWIPE, a probabilistic YIN in 2014, and in 2018 CREPE, a network. "
                   "<bookmark mark='f'/> And in 2016 Siddharth Sigtia, Emmanouil Benetos and Simon Dixon trained a network to "
                   "transcribe polyphonic piano end to end.", marks="bcdef")

    # ------------------------------------------------------------------
    def data(self):
        items = [
            (r"2010: \ MAPS, \ a piano dataset: \ a Disklavier records its own playing, \ so the answer key is exact", WHITE),
            (r"2018: \ Onsets and Frames \ (Hawthorne et al.): \ one network finds onsets, \ another sustains, \ each helps the other", WHITE),
            (r"2019: \ MAESTRO: \ about 200 hours of competition pianists on Disklaviers, \ notes aligned to a few milliseconds", WHITE),
            (r"with that much data, \ piano note F-measures rose above 0.9 on recordings like the training set", WHITE),
            (r"the lesson Monochord also teaches: \ transcription is limited by its answer keys", TUNE),
        ]
        rows_scene(self, r"data with answers", items,
                   "What changed most was data with answers. <bookmark mark='b'/> In 2010 MAPS recorded a Disklavier, a piano that "
                   "records the keys it plays, so the answer key was exact. <bookmark mark='c'/> In 2018 Curtis Hawthorne and "
                   "colleagues' Onsets and Frames used one network to find where notes begin and another for how long they last, "
                   "each helping the other. <bookmark mark='d'/> In 2019 they released MAESTRO: about two hundred hours of "
                   "competition pianists on Disklaviers, notes aligned to a few milliseconds. <bookmark mark='e'/> With that much "
                   "data, piano note F-measures rose above nine tenths on recordings like the training set. "
                   "<bookmark mark='f'/> The lesson is the one Monochord teaches too: transcription is limited by its answer keys.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def ear(self):
        items = [
            (r"Mozart, \ fourteen, \ wrote out Allegri's Miserere after hearing it in the Sistine Chapel, \ his father wrote \ (1770)", WHITE),
            (r"he knew the style, \ the harmony and the voices' ranges: \ a strong prior over what was likely", WHITE),
            (r"trained musicians transcribe by expectation as much as by hearing: \ they hear what fits, \ and check", WHITE),
            (r"a model of music, \ like Chapter 9's grid or Part 14's melodies, \ is how a machine gets such a prior", TUNE),
        ]
        rows_scene(self, r"how people do it", items,
                   "And how do people do it? <bookmark mark='b'/> In 1770, his father wrote, the fourteen-year-old Mozart wrote out "
                   "Allegri's Miserere after hearing it in the Sistine Chapel. <bookmark mark='c'/> He knew the style, the harmony "
                   "and the voices' ranges: a strong prior over what was likely. <bookmark mark='d'/> Trained musicians transcribe "
                   "by expectation as much as by hearing: they hear what fits, and check. <bookmark mark='e'/> A model of music, "
                   "like Chapter 9's grid or Part 14's melodies, is how a machine gets such a prior.", marks="bcde")
