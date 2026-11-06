from __future__ import annotations

from videos.philosophy.philosophy37.common import *  # noqa: F403


class Hume(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Hume's law", r"Can an ought follow from an is?", lit=(1739, 1960, 1997), part=PART)
        with self.voiceover("Chapter one. Hume's law."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.hume()
        self.prior()
        self.searle()
        self.oic()
        self.models()
        self.schurz()
        self.wall_brick()

    def hume(self):
        q = quote_card(r"In every system of morality, \ which I have hitherto met with, \ I have always remark'd, \ that "
                       r"the author proceeds for some time in the ordinary way of reasoning \dots\ when all of a sudden "
                       r"I am surpriz'd to find, \ that instead of the usual copulations of propositions, \ \textit{is}, "
                       r"\ and \textit{is not}, \ I meet with no proposition that is not connected with an "
                       r"\textit{ought}, \ or an \textit{ought not}.", r"David Hume",
                       r"\textit{A Treatise of Human Nature} \ (1739), \ 3.1.1", width=10.8, font_size=26).move_to(
            [0, 0.6, 0])
        foot = label(r"`this ought \dots\ expresses some new relation': \ how can it be a deduction from others which "
                     r"are entirely different from it?", font_size=19, color=OUGHT).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "David Hume noticed something in 1739, in a famous paragraph of the Treatise. <bookmark mark='a'/>In every "
            "system of morality he had met with, the author reasons for a while in the ordinary way, about God or "
            "human affairs, when all of a sudden, instead of the usual is and is not, every proposition is connected "
            "with an ought or an ought not. <bookmark mark='b'/>This ought, Hume wrote, expresses some new relation, "
            "and a reason should be given for how it can be a deduction from others that are entirely different from "
            "it. The thesis read into the paragraph, that no ought follows from premises containing only is, came to "
            "be called Hume's law."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def prior(self):
        hc = history_card(1960, r"Arthur Prior", r"``The Autonomy of Ethics''", width=5.2, color=HIST).to_corner(
            UL, buff=0.3)
        rows = [(r"tea", r"tea-drinking is common in England; \ so, \ tea-drinking is common in England \textit{or} all "
                         r"New Zealanders ought to be shot", OUGHT),
                (r"the dilemma", r"if the conclusion is normative, \ an ought follows from an is; \ if it is not, \ "
                                 r"add `tea-drinking is not common in England': \ the ought clause then follows from "
                                 r"two premises, \ neither of them normative", BAD),
                (r"the lesson", r"Hume's law needs care: \ the trouble is ought-parts that do no work", GOAL)]
        g = rows_table(rows, top=1.2, gap=0.5, width=8.2, x_text=-2.2, label_size=21, text_size=19)
        with self.voiceover(
            "In 1960 Arthur Prior showed that the law, stated naively, is false. <bookmark mark='a'/>From tea-drinking "
            "is common in England, it follows by logic alone that tea-drinking is common in England, or all New "
            "Zealanders ought to be shot. <bookmark mark='b'/>Is that conclusion normative? If so, an ought has "
            "followed from an is. If not, then combine it with the premise that tea-drinking is not common in England, "
            "and the ought clause follows, from two premises neither of which is normative. "
            "<bookmark mark='c'/>The lesson is that the law needs a careful statement: what is objectionable is an "
            "ought that does real work in the conclusion."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def searle(self):
        head = label(r"Searle's derivation \ (1964)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        steps = VGroup(*[label(t, font_size=22, color=c) for t, c in [
            (r"1. \ Jones uttered the words `I hereby promise to pay you, \ Smith, \ five dollars.'", IS),
            (r"2. \ Jones promised to pay Smith five dollars.", IS),
            (r"3. \ Jones placed himself under an obligation to pay Smith five dollars.", IS),
            (r"4. \ Jones is under an obligation to pay Smith five dollars.", OUGHT),
            (r"5. \ Jones ought to pay Smith five dollars.", OUGHT)]]).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        steps.move_to([0, 1.0, 0])
        foot = stack([(r"each step looks like a matter of fact, \ given the institution of promising", GREY_A),
                      (r"Hare's reply: \ the step from 2 to 3 uses the institution's constitutive rule, \ "
                       r"`one ought to keep one's promises': \ a normative premise, \ hidden", BAD),
                      (r"institutional facts are facts; \ but taking part in an institution is already a commitment",
                       GOAL)],
                     font_size=19, buff=0.18).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "In 1964 John Searle claimed to derive an ought from an is. <bookmark mark='a'/>Jones uttered the words, I "
            "hereby promise to pay you, Smith, five dollars. So Jones promised to pay Smith five dollars. So he placed "
            "himself under an obligation to pay. So he is under an obligation to pay. So he ought to pay Smith five "
            "dollars. <bookmark mark='b'/>Each step looks like a matter of fact, given the institution of promising, "
            "which is a social fact like money or marriage. <bookmark mark='c'/>R. M. Hare replied that the step from "
            "promising to obligation uses the institution's constitutive rule, that one ought to keep one's "
            "promises: a normative premise, hidden in the word promise. <bookmark mark='d'/>Institutional facts are "
            "facts; but to take part in an institution, to speak of obligations from inside it, is already to accept "
            "its norms. Schurz's theorem says why the ought could not have come from nowhere."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in steps], lag_ratio=0.5), run_time=4)
            for mk, r in zip("bcd", foot):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def oic(self):
        head = label(r"Ought implies can", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the principle", r"if you ought to do something, \ you can do it: \ often credited to Kant", OUGHT),
                (r"a bridge", r"contraposed, \ `cannot' implies `not ought': \ a fact about ability settles a norm", IS),
                (r"in the logic", r"ideal worlds must be possible worlds: \ a bridge principle added, \ not derived", GOAL),
                (r"the data", r"Chituc et al. \ (2016): \ people often say an agent still ought to keep a promise she has become unable to keep, \ when she is to blame", MIND)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The best-known bridge between is and ought runs the other way. <bookmark mark='a'/>Ought implies can: if "
            "you ought to do something, you are able to do it, a principle usually credited to Kant. <bookmark "
            "mark='b'/>Contraposed, it says that cannot implies not ought, so a plain fact about ability settles a "
            "normative question. <bookmark mark='c'/>In the logic, it holds only if the deontically ideal worlds are "
            "among the possible ones, a bridge principle we add to the system rather than derive. <bookmark "
            "mark='d'/>And it may not match ordinary judgment: Vladimir Chituc and colleagues found in 2016 that "
            "people often say an agent still ought to keep a promise she has made herself unable to keep, when she is "
            "to blame for the inability."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def models(self):
        d = load("schurz")
        head = label(r"A logic of ought, \ and its models", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        assert d["models_checked"] == 175616
        w0 = VGroup(Circle(radius=0.45, color=IS, stroke_width=3), label(r"$w$: \ $p$", font_size=20, color=IS))
        w1 = VGroup(Circle(radius=0.45, color=OUGHT, stroke_width=3), label(r"$\neg p$", font_size=20, color=OUGHT))
        w0.move_to([-4.6, 0.4, 0])
        w1.move_to([-2.0, 0.4, 0])
        arr = Arrow(w0.get_right(), w1.get_left(), buff=0.1, color=OUGHT, stroke_width=3)
        al = label(r"ideal", font_size=18, color=OUGHT).next_to(arr, UP, buff=0.08)
        cap = label(r"a countermodel to $p \vdash Op$: \ $p$ is true, \ but not in the ideal world", font_size=18,
                    color=GREY_A).next_to(VGroup(w0, w1), DOWN, buff=0.4)
        side = stack([(r"worlds, \ and an arrow to the worlds that are deontically ideal from each", GREY_A),
                      (r"$O\varphi$: \ $\varphi$ holds in every ideal world; \ $P\varphi$: \ in some", OUGHT),
                      (r"KD: \ every world has an ideal world, \ so ought implies may", GOAL),
                      (r"the Reasoner: \ every model of up to 3 worlds over the atoms used: \ 175,616 models", IS)],
                     font_size=19, aligned_edge=LEFT, width=5.6, buff=0.32).move_to([3.4, 0.2, 0])
        with self.voiceover(
            "To test the law properly, the Reasoner builds a logic of ought. <bookmark mark='a'/>A model is a set of "
            "worlds, with arrows from each world to the worlds that are deontically ideal from its point of view: "
            "the worlds where everything that ought to be, is. <bookmark mark='b'/>Ought phi is true at a world if "
            "phi holds in every ideal world; may phi, if it holds in some. <bookmark mark='c'/>In the standard system "
            "called KD, every world has at least one ideal world, so whatever ought to be may be. "
            "<bookmark mark='d'/>Here is a countermodel to the inference from p to ought p: p is true, but not in the "
            "ideal world. <bookmark mark='e'/>The Reasoner checks an inference by examining every model of up to "
            "three worlds over the atoms it uses: a hundred and seventy five thousand, six hundred and sixteen models."
        ) as vo:
            self.play(FadeIn(head), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(w0), FadeIn(w1), GrowArrow(arr), FadeIn(al), FadeIn(cap))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def schurz(self):
        d = load("schurz")
        head = label(r"Schurz's pattern, \ checked", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows = d["rows"]
        assert d["hume_pattern_holds"] and len(rows) == 8
        expect = [(True, True, False, True), (True, True, False, True), (True, False, False, None),
                  (True, False, False, None), (True, True, True, False), (False, True, False, False),
                  (False, True, False, False), (False, False, False, None)]
        assert [(r["descriptive"], r["valid"], r["theorem"], r["idle"]) for r in rows] == expect
        hd = [r"\text{premises}", r"\text{conclusion}", r"\text{is-only}", r"\text{valid}", r"\text{ought idle?}"]

        def tex(s):
            return MathTex(s if s else r"\varnothing", font_size=24)
        cells = []
        for r in rows:
            prem = ", ".join(r["premises"])
            idle = r"logical truth" if r["theorem"] else (r"idle" if r["idle"] else (r"does work" if r["valid"] else
                                                                                         r"--"))
            col = GOAL if r["idle"] or r["theorem"] else (BAD if r["valid"] and r["descriptive"] else GREY_A)
            cells.append([tex(prem), tex(r["conclusion"]), mark(r["descriptive"], 20), mark(r["valid"], 20),
                          label(idle, font_size=16, color=col if r["valid"] else GREY_A)])
        grid = ValueGrid(hd, cells, col_w=[3.2, 3.4, 1.6, 1.4, 2.6], cell_h=0.46, font_size=16).move_to([0, -0.15, 0])
        foot = label(r"every valid inference from is-only premises to an ought: \ a logical truth, \ or an ought "
                     r"that can be swapped for anything", font_size=18, color=GOAL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Gerhard Schurz proved in 1997 the version of Hume's law that survives Prior. The Reasoner runs his "
            "pattern on eight inferences. <bookmark mark='a'/>Prior's tea inference is valid, and so is his second, "
            "from p to: if not p, then ought q. But in both the ought is idle: replace it with a fresh sentence, about "
            "anything at all, and the inference stays valid. <bookmark mark='b'/>From p to ought p, and from p and q "
            "to ought p and q, the inferences are invalid; each has a countermodel. <bookmark mark='c'/>From nothing "
            "at all, it follows that it ought to be that q or not q: a logical truth of the system, which follows "
            "from any premises whatever. <bookmark mark='d'/>Add a normative premise, if p then ought q, and the "
            "ought does real work; but then the premises were not purely descriptive. Ought implies may, and ought p "
            "does not imply p. <bookmark mark='e'/>So every valid inference from premises that only say what is, to a "
            "conclusion with an ought in it, is either a logical truth or carries an ought that does no work. That is "
            "Schurz's theorem, for a broad class of alethic-deontic logics."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, ks in zip("abcde", ([0, 1], [2, 3], [4], [5, 6, 7], [])):
                vo.wait_until(mk)
                if ks:
                    self.play(*[FadeIn(c) for k in ks for c in grid.cell[k]])
                else:
                    self.play(FadeIn(foot))
        self.clear_scene()

    def wall_brick(self):
        w = wall(upto=37, current=37).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(37, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "This is the thirty seventh brick in the Wall. <bookmark mark='a'/>The dream was to derive ought from is: "
            "to read morality off the facts, by logic alone. Schurz's theorem shows that no such derivation does any "
            "work, and the Frege-Geach problem of chapter six shows that the simplest alternative, treating ought "
            "claims as not stating facts at all, has a logic problem of its own. <bookmark mark='b'/>What it forces is "
            "a choice: accept bridge principles that connect is and ought as extra premises, or give ought a "
            "non-factual meaning and then rebuild its logic."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(FadeIn(card), Indicate(w.brick[37], color=P.CONCL, scale_factor=1.06))
            vo.wait_until("b")
            self.wait(0.5)
        self.clear_scene()
