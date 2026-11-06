from __future__ import annotations

from videos.philosophy.philosophy27.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.puzzle()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"$a = a$ and $a = b$ are obviously statements of differing cognitive value.",
                       r"Gottlob Frege", r"`On Sense and Reference' \ (1892)", width=9.0, font_size=28).next_to(
            t, DOWN, buff=0.45)
        with self.voiceover(
            "Part 26 ended a long walk through physics with a question about what a theory's words refer to. This "
            "part, the first of a new act on mind and meaning, asks that question about all words. "
            "<bookmark mark='a'/>Gottlob Frege opened the subject in 1892 with a sentence that looks too simple to "
            "matter: a equals a, and a equals b, are obviously statements of differing cognitive value. "
            "<bookmark mark='b'/>The first is trivial. The second, if true, can be a discovery. Yet if a really is "
            "b, they seem to say the same thing. Explaining the difference, and what words contribute to what we "
            "say, is the work of this part."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=SENSE, scale_factor=1.03))
        self.clear_scene()

    def puzzle(self):
        head = label(r"Four questions about words", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"names", r"does `Hesperus' mean just the planet it names? \ then why is `Hesperus is Phosphorus' news?",
             NAME),
            (r"descriptions", r"what does `the present king of France' contribute, \ when there is no such king?",
             REF),
            (r"context", r"`I am here now' cannot be false when I say it; \ yet I might have been elsewhere", WORLD),
            (r"composition", r"we understand sentences we have never heard: \ meanings must be built from parts, "
                             r"\ by rules a machine could run", SENSE),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "Four questions run through it. <bookmark mark='a'/>Names: if a name means just the thing it names, why "
            "is it news that Hesperus is Phosphorus? <bookmark mark='b'/>Descriptions: what does the phrase the "
            "present king of France contribute to a sentence, when there is no king? <bookmark mark='c'/>Context: "
            "the sentence I am here now cannot be false when I say it, and yet I might have been somewhere else. "
            "<bookmark mark='d'/>And composition: we understand sentences we have never heard before, so their "
            "meanings must be built from the meanings of their parts, by rules precise enough for a machine. This "
            "part builds that machine."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"the School of Names: \ a white horse, \ identity and inclusion",
            r"Frege: \ sense and reference; \ three descriptions of one point, \ computed",
            r"Russell's descriptions, \ Strawson's gaps, \ Donnellan's two uses",
            r"Kripke: \ rigid names across worlds; \ Twin Earth and the social mind",
            r"Kaplan's indexicals and the two-dimensional matrix",
            r"Tarski and Davidson; \ Montague's $\lambda$-calculus; \ a semantic parser, \ built",
            r"generalized quantifiers; \ `most' is not first-order, \ by a game",
            r"intensions; \ belief reports \ (a Price List; \ the Wall); \ donkeys; \ meaning in machines",
        ], font_size=22)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>An ancient puzzle about a white horse, from the Chinese School of Names. "
            "<bookmark mark='b'/>Frege's distinction between sense and reference, with his own geometric example "
            "computed. <bookmark mark='c'/>Russell's theory of descriptions, and the replies of Strawson and "
            "Donnellan. <bookmark mark='d'/>Kripke's revolution in the theory of names, and Putnam's Twin Earth. "
            "<bookmark mark='e'/>Kaplan's logic of indexicals, and the two-dimensional picture. "
            "<bookmark mark='f'/>Truth-conditional semantics, from Tarski and Davidson to Montague, ending in a "
            "working semantic parser. <bookmark mark='g'/>Quantifiers as relations between sets, and a proof, by a "
            "game, that most cannot be said in first-order logic. <bookmark mark='h'/>And intensions; belief "
            "reports, where Frege's puzzle becomes this part's brick in the Wall; donkey sentences; and what all of "
            "this means for machines that use language."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
