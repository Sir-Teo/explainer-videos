from __future__ import annotations

from videos.philosophy.philosophy28.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.puzzle()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"For a \textit{large} class of cases \dots\ the meaning of a word is its use in the language.",
                       r"Ludwig Wittgenstein", r"\textit{Philosophical Investigations} \ (1953), \ \S 43", width=9.6,
                       font_size=28).next_to(t, DOWN, buff=0.45)
        with self.voiceover(
            "Part 27 built meaning out of reference: names and their bearers, sentences and their truth conditions, "
            "a parser that computes them. This part asks whether that is the right foundation. "
            "<bookmark mark='a'/>Ludwig Wittgenstein, who had built the most austere version of the reference "
            "picture, came to reject it. For a large class of cases, he wrote in the Investigations, the meaning of a "
            "word is its use in the language. <bookmark mark='b'/>Use: what speakers do with words, in context, "
            "with each other, for purposes. This part follows that idea from Wittgenstein through Quine, Austin and "
            "Grice to the mathematics of conversation, and to the question of whether machines trained on text can "
            "mean anything."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=USE, scale_factor=1.03))
        self.clear_scene()

    def puzzle(self):
        head = label(r"Four questions about use", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"rules", r"what fact about me makes it true that by `plus' I meant addition, \ and not something else?",
             RULE_C),
            (r"translation", r"could two translations fit every fact about a language, \ and disagree?", WORLD),
            (r"what is meant", r"`some of the students passed' usually conveys `not all': \ how, \ if it does not say "
                               r"so?", USE),
            (r"machines", r"a model that has only ever seen text: \ do its words mean anything?", HEAR),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "Four questions run through it. <bookmark mark='a'/>Rules: what fact about me makes it true that by "
            "plus I have always meant addition, and not some other function that agrees with it on every sum I have "
            "done? <bookmark mark='b'/>Translation: could two translations of a language fit every fact about its "
            "speakers, and still disagree? <bookmark mark='c'/>What is meant: some of the students passed usually "
            "conveys that not all did. How, if the words do not say it? <bookmark mark='d'/>And machines: a model "
            "that has only ever seen text. Do its words mean anything at all?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"the \textit{Tractatus}: \ pictures, \ truth tables, \ every truth function from one operation",
            r"the \textit{Investigations}: \ language games; \ family resemblance, \ computed",
            r"rule-following: \ plus and quus, \ built \ (the Wall); \ the private language argument",
            r"Quine's gavagai and proxy functions; \ Davidson's charity, \ computed",
            r"Austin and Searle: \ speech acts; \ Grice: \ implicature; \ `some, \ not all'",
            r"the Rational Speech Acts model, \ built: \ listeners and speakers reasoning about each other",
            r"Lewis's conventions: \ signalling games learned from nothing; \ word vectors",
            r"do language models mean? \ a Price List; \ a probe; \ pragmatics in machines",
        ], font_size=22)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>Wittgenstein's early picture theory, with every truth function built from "
            "a single operation. <bookmark mark='b'/>His later language games and family resemblance. "
            "<bookmark mark='c'/>Kripke's sceptical paradox about rules, built with plus and quus, this part's brick "
            "in the Wall, and the private language argument. <bookmark mark='d'/>Quine's indeterminacy of "
            "translation, and Davidson's principle of charity, computed. <bookmark mark='e'/>Speech acts, Grice's "
            "theory of implicature, and why some means not all. <bookmark mark='f'/>A working model of conversation "
            "as recursive reasoning, the Rational Speech Acts model. <bookmark mark='g'/>Conventions that emerge from "
            "nothing in signalling games, and meaning as distribution in word vectors. <bookmark mark='h'/>And "
            "whether language models mean anything, priced, probed, and tested."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
