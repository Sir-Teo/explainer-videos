from __future__ import annotations

from videos.music.music65.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 11, r"Frontier: \ form, \ control and attribution", r"What do composing machines still not do?")
        self.form()
        self.control()
        self.attribution()
        self.problem()

    # ------------------------------------------------------------------
    def form(self):
        items = [
            (r"the Music Transformer \ (Huang et al., \ 2018): \ attention by relative distance, \ so a motive can return in another place and key", WHITE),
            (r"a minute of coherent piano music from performances; \ but a sonata's plan over twenty minutes is still hard", WHITE),
            (r"hierarchy helps: \ plan sections, \ then phrases, \ then notes \ (Part 21's forms)", WHITE),
            (r"Monochord's tunes end where their phrases end; \ none of them knows where it is in a piece", TUNE),
        ]
        rows_scene(self, r"long-range form", items,
                   "Three frontiers. The first is form. <bookmark mark='b'/> The Music Transformer of 2018, from Cheng-Zhi Anna "
                   "Huang and colleagues, attends by relative distance, so a motive can come back somewhere else and in another "
                   "key. <bookmark mark='c'/> It wrote a minute of coherent piano music, learnt from performances; but the plan of "
                   "a sonata across twenty minutes is still hard. <bookmark mark='d'/> Hierarchy helps: plan the sections, then "
                   "the phrases, then the notes, as in Part 21's forms. <bookmark mark='e'/> Monochord's tunes end where their "
                   "phrases end, and none of them knows where it is in a piece.", marks="bcde")

    # ------------------------------------------------------------------
    def control(self):
        items = [
            (r"control: \ condition on a key, \ a tempo, \ chords, \ a style, \ a sentence; \ or fill in a gap \ (infilling)", WHITE),
            (r"tools for composers rather than replacements: \ suggest the next bar, \ harmonize a line, \ vary a motive", WHITE),
            (r"and constraints, \ as in Chapter 4: \ say what must be true, \ and sample everything else", TUNE),
        ]
        rows_scene(self, r"control", items,
                   "The second is control. <bookmark mark='b'/> Condition the model on a key, a tempo, chords, a style or a "
                   "sentence, or ask it to fill a gap in the middle of a piece. <bookmark mark='c'/> Many of the most useful "
                   "systems are tools for composers rather than replacements: suggest the next bar, harmonize a line, vary a "
                   "motive. <bookmark mark='d'/> And constraints, as in Chapter 4: say what must be true, and sample everything "
                   "else.", marks="bcd")

    # ------------------------------------------------------------------
    def attribution(self):
        items = [
            (r"whose music is in a model's output? \ copying can be measured, \ as here, \ but only against data one has", WHITE),
            (r"influence is subtler than copying: \ which training pieces made this phrase likely?", WHITE),
            (r"Bach is out of copyright; \ most music a large model learns from is not \ (Part 60's rights; \ Part 66's courts)", WHITE),
            (r"attribution and licensing for training data are being argued now \ (dated)", TUNE),
        ]
        rows_scene(self, r"attribution", items,
                   "The third is attribution. <bookmark mark='b'/> Whose music is in a model's output? Copying can be measured, as "
                   "this part measured it, but only against data one has. <bookmark mark='c'/> And influence is subtler than "
                   "copying: which training pieces made this phrase likely? <bookmark mark='d'/> Bach is long out of copyright; "
                   "most music a large model learns from is not, as Part 60's rights and Part 66's courts make clear. "
                   "<bookmark mark='e'/> How training data should be attributed and licensed is being argued now.", marks="bcde")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"train generators of many sizes on a corpus whose every piece is known", WHITE),
            (r"measure, \ for each, \ likelihood on unseen music and how much it copies, \ by exact runs and by near matches", WHITE),
            (r"ask listeners which outputs they prefer, \ blind", WHITE),
            (r"$\bigstar$ \ research problem: \ is there a frontier of novelty against quality, \ and can a model be moved along it, \ or past it?", EAR),
            (r"an answer would tell us what to ask of composing machines, \ and of their training data", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A research problem to end on. <bookmark mark='a'/> Train generators of many sizes on a corpus whose every piece "
            "is known. <bookmark mark='b'/> Measure, for each, its likelihood on unseen music and how much it copies, by exact "
            "runs and by near matches. <bookmark mark='c'/> Ask listeners which outputs they prefer, without telling them "
            "which is which. <bookmark mark='d'/> Is there a frontier of novelty against quality, and can a model be moved "
            "along it, or past it? <bookmark mark='e'/> The answer would tell us what to ask of composing machines, and of "
            "their training data."
        ) as vo:
            self.play(FadeIn(head))
            for mark, rr in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(rr))
        self.wait(0.6)
        self.clear_scene()
