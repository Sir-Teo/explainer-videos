from __future__ import annotations

from videos.music.music65.common import *  # noqa: F403


class Tokens(SoundScene):
    def construct(self):
        chapter(self, 6, r"Music as tokens", r"How do you turn a score into words for a language model?")
        self.three()
        self.choices()
        self.keys()

    # ------------------------------------------------------------------
    def three(self):
        d = load("corpus")
        reps, enc = d["reps"], d["encodings"]
        def row(name, toks, rep, col):
            seq = label(r"\ ".join(t.replace("<", r"$\langle$").replace(">", r"$\rangle$").replace("_", r"\_") for t in toks[:12]), font_size=15, color=col)
            stat = label(rf"{rep['vocab']} symbols; \ {rep['mean_length']:.0f} per tune", font_size=16, color=GREY_A)
            return VGroup(label(name, font_size=19, color=col), seq, stat)
        g = VGroup(row(r"one token a note", enc["note"], reps["note"], TUNE),
                   row(r"pitch, \ then length", enc["split"], reps["split"], BLUE),
                   row(r"a grid of sixteenths", enc["grid"], reps["grid"], EAR))
        for r in g:
            r.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        g.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(DOWN * 0.2)
        head = label(rf"the opening of {bwv(d['example'])}, \ three ways", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "A language model reads tokens, so music must become tokens, and the choice matters. Here is a chorale's opening "
            "three ways. <bookmark mark='a'/> One token a note, pitch, length and phrase end together: "
            f"{say(reps['note']['vocab'])} different symbols, about {say(round(reps['note']['mean_length']))} tokens a tune. "
            "<bookmark mark='b'/> Pitch, then length, as separate tokens, the way MIDI-like encodings do: only "
            f"{say(reps['split']['vocab'])} symbols, but {say(round(reps['split']['mean_length']))} tokens a tune. "
            "<bookmark mark='c'/> Or a grid, one token every sixteenth note, with a symbol for holding, as DeepBach did: "
            f"{say(reps['grid']['vocab'])} symbols, and {say(round(reps['grid']['mean_length']))} tokens a tune."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abc", g):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def choices(self):
        items = [
            (r"fewer symbols, \ longer sequences: \ each symbol is seen more often, \ but the model must look further back", WHITE),
            (r"a grid makes time explicit and simultaneity easy \ (four voices on one grid); \ events make long notes cheap", WHITE),
            (r"for many instruments: \ REMI \ (bars and positions as tokens, \ 2020), \ or the notes of each instrument interleaved", WHITE),
            (r"or skip symbols: \ tokens from a neural codec of the audio itself \ (Part 66)", WHITE),
            (r"Monochord's transformer reads pitch, \ then length, \ then a fermata: \ 61 symbols, \ room for every key", TUNE),
        ]
        rows_scene(self, r"what the choice trades", items,
                   "What does the choice trade? <bookmark mark='b'/> Fewer symbols make longer sequences: each symbol is seen more "
                   "often, but the model must look further back. <bookmark mark='c'/> A grid makes time explicit and simultaneous "
                   "notes easy, four voices on one grid; events make long notes cheap. <bookmark mark='d'/> For many instruments "
                   "there are encodings with bars and positions as tokens, like REMI in 2020, or each instrument's notes "
                   "interleaved. <bookmark mark='e'/> Or skip symbols altogether, and use tokens from a neural codec of the audio "
                   "itself, the subject of Part 66. <bookmark mark='f'/> Monochord's transformer reads a pitch, then a length, then "
                   "a fermata if the phrase ends: sixty-one symbols, with room for every pitch in every key.", marks="bcdef")

    # ------------------------------------------------------------------
    def keys(self):
        items = [
            (r"every tune here is in C: \ a model that sees only C learns C's pitches, \ not the tune's intervals", WHITE),
            (r"the same tune a tone higher is, \ to a listener, \ the same tune: \ transposition is a free example", WHITE),
            (r"so a model can learn from each tune in twelve keys, \ as Chapter 7's transformer will", WHITE),
            (r"not quite free: \ the voice's range, \ and an instrument's open strings, \ make some keys rarer and some sounds unlike others", WHITE),
            (r"pitch-relative tokens \ (intervals) \ build the symmetry in instead of teaching it", TUNE),
        ]
        rows_scene(self, r"twelve keys", items,
                   "One more choice concerns keys. <bookmark mark='b'/> Every tune here is in C, so a model that sees only C "
                   "learns C's pitches, not the tune's intervals. <bookmark mark='c'/> But the same tune a tone higher is, to a "
                   "listener, the same tune: transposition makes a free example. <bookmark mark='d'/> So a model can learn from "
                   "each tune in twelve keys, as the transformer of the next chapter will. <bookmark mark='e'/> It is not quite "
                   "free: a voice's range, or an instrument's open strings, make some keys rarer and some sounds unlike the "
                   "others. <bookmark mark='f'/> Tokens that are themselves intervals build the symmetry in, instead of "
                   "teaching it by example.", marks="bcdef")
