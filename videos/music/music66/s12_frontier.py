from __future__ import annotations

from videos.music.music66.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 11, r"Frontier: \ data, \ consent and what is unsolved", r"Whose music did the machines learn from?")
        self.data()
        self.courts()
        self.musicians()
        self.unsolved()
        self.honest()
        self.problem()

    # ------------------------------------------------------------------
    def data(self):
        items = [
            (r"MusicGen was trained on 20,000 hours of music licensed for the purpose \ (its paper says so)", WHITE),
            (r"for several commercial song generators, \ the training data was not disclosed", WHITE),
            (r"Monochord's generators learnt only from sounds Monochord made: \ the honest version is the small one", WHITE),
            (r"what a model learnt from cannot be read off its weights; \ it must be disclosed, \ or found by tests like Part 65's", TUNE),
        ]
        rows_scene(self, r"data", items,
                   "The first frontier is data. <bookmark mark='b'/> MusicGen's authors say it was trained on twenty thousand hours "
                   "of music licensed for the purpose. <bookmark mark='c'/> For several commercial song generators, the training "
                   "data was not disclosed. <bookmark mark='d'/> Monochord's generators learnt only from sounds Monochord made, "
                   "which is why they are small: the honest version is the small one. <bookmark mark='e'/> What a model learnt from "
                   "cannot be read off its weights. It must be disclosed, or found by tests like Part 65's.", marks="bcde")

    # ------------------------------------------------------------------
    def courts(self):
        items = [
            (r"June 2024: \ the major labels sue Suno and Udio for training on their recordings without licence", WHITE),
            (r"2025: \ settlements and licensing deals between labels and both companies are announced \ (dated)", WHITE),
            (r"elsewhere: \ collecting societies sue over lyrics and compositions; \ courts weigh `fair use' and text-and-data-mining exceptions", WHITE),
            (r"the outcome will decide who is paid when music is learnt from \ (Part 60's money, \ again)", TUNE),
        ]
        rows_scene(self, r"the courts \ (dated: \ verify the latest)", items,
                   "The second is the courts, and everything here is dated. <bookmark mark='b'/> In June 2024 the major record "
                   "labels sued Suno and Udio, two song generators, for training on their recordings without a licence. "
                   "<bookmark mark='c'/> In 2025 settlements and licensing deals between labels and both companies were announced. "
                   "<bookmark mark='d'/> Elsewhere, collecting societies have sued over lyrics and compositions, and courts are "
                   "weighing fair use and exceptions for text and data mining. <bookmark mark='e'/> The outcome will decide who is "
                   "paid when music is learnt from: Part 60's money, again.", marks="bcde")

    # ------------------------------------------------------------------
    def unsolved(self):
        items = [
            (r"form: \ generated songs drift; \ verses, \ choruses and returns are imitated, \ not planned", WHITE),
            (r"control: \ a sentence is a blunt instrument; \ musicians want to edit a bar, \ a part, \ a mix \ (Part 64's stems)", WHITE),
            (r"attribution: \ which training recordings made this output likely?", WHITE),
            (r"evaluation: \ no metric yet tracks what listeners value", TUNE),
        ]
        rows_scene(self, r"unsolved", items,
                   "And what is unsolved. <bookmark mark='b'/> Form: generated songs drift; verses, choruses and returns are "
                   "imitated rather than planned. <bookmark mark='c'/> Control: a sentence is a blunt instrument, and musicians want "
                   "to edit a bar, a part or a mix, the stems of Part 64. <bookmark mark='d'/> Attribution: which training "
                   "recordings made this output likely? <bookmark mark='e'/> And evaluation: no metric yet tracks what listeners "
                   "value.", marks="bcde")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"render a corpus whose every recording is known, \ with Monochord, \ in several styles", WHITE),
            (r"train a token model and a diffusion model on it, \ at several sizes", WHITE),
            (r"for each output, \ estimate which training recordings it draws on, \ and check against the truth", WHITE),
            (r"$\bigstar$ \ research problem: \ can training-data attribution for generated audio be made accurate enough to pay on?", EAR),
            (r"an answer would turn Part 60's royalty waterfall into something a generator could run", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A research problem to end on. <bookmark mark='a'/> Render a corpus whose every recording is known, with Monochord, "
            "in several styles. <bookmark mark='b'/> Train a token model and a diffusion model on it, at several sizes. "
            "<bookmark mark='c'/> For each output, estimate which training recordings it draws on, and check against the truth, "
            "which here is known. <bookmark mark='d'/> Can attribution be made accurate enough to pay on? "
            "<bookmark mark='e'/> An answer would turn Part 60's royalty waterfall into something a generator could run."
        ) as vo:
            self.play(FadeIn(head))
            for mark, rr in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(rr))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def musicians(self):
        items = [
            (r"inside the tools: \ separation, \ generated fills and stems, \ timbre transfer, \ in ordinary music software", WHITE),
            (r"for stock and background music, \ generated tracks now compete with commissioned ones", WHITE),
            (r"streaming services have reported floods of generated uploads, \ and changed how they label and pay for them \ (dated)", WHITE),
            (r"the work most at risk is the most routine; \ the work least at risk is the most particular \ (an argument, \ not a measurement)", TUNE),
        ]
        rows_scene(self, r"what changed for musicians", items,
                   "What has changed for musicians already? <bookmark mark='b'/> Inside ordinary music software: separation, "
                   "generated fills and stems, timbre transfer. <bookmark mark='c'/> For stock and background music, generated "
                   "tracks now compete with commissioned ones. <bookmark mark='d'/> Streaming services have reported floods of "
                   "generated uploads, and changed how they label them and pay for them. <bookmark mark='e'/> A common argument is "
                   "that the work most at risk is the most routine and the work least at risk the most particular; it is an "
                   "argument, not yet a measurement.", marks="bcde")

    # ------------------------------------------------------------------
    def honest(self):
        items = [
            (r"every generator in this part learnt only from sounds Monochord made, \ in minutes, \ on one computer", WHITE),
            (r"so each is small and each falls short: \ a sample-level net that memorized, \ a token model with forty minutes of music", WHITE),
            (r"but every number is checkable: \ the training data is known, \ so copying and quality can be measured exactly", WHITE),
            (r"the large systems do the same things at a scale of data that no outsider can inspect", TUNE),
        ]
        rows_scene(self, r"the smallest honest versions", items,
                   "A word about this part's own machines. <bookmark mark='b'/> Every one learnt only from sounds Monochord made, in "
                   "minutes, on one computer. <bookmark mark='c'/> So each is small and each falls short: a sample-level network "
                   "that memorized its notes, a token model that heard forty minutes of piano, a thirty-thousandth of MusicGen's "
                   "twenty thousand hours. <bookmark mark='d'/> But "
                   "every number they produced can be checked, because the training data is known, and so copying and quality can "
                   "be measured exactly. <bookmark mark='e'/> The large systems do the same things at a scale of data that no "
                   "outsider can inspect, which is the frontier's real problem.", marks="bcde")
