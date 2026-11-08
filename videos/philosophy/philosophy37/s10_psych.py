from __future__ import annotations

from videos.philosophy.philosophy37.common import *  # noqa: F403


class Psych(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Moral psychology", r"Do we reason our way to moral judgments?", lit=(2001,),
                            part=PART)
        with self.voiceover("Chapter nine. Moral psychology."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.haidt()
        self.folk()
        self.foundations()
        self.greene()
        self.grammar()

    def haidt(self):
        head = label(r"The emotional dog and its rational tail \ (Haidt, \ 2001)", font_size=30, color=CONN).to_edge(
            UP, buff=0.35)
        rows = [(r"the vignette", r"Julie and Mark, \ adult siblings, \ make love once, \ with every precaution; \ no "
                                  r"one is harmed, \ and it brings them closer", MIND),
                (r"the verdict", r"most people say it was wrong at once, \ then search for reasons, \ and when each "
                                 r"reason is ruled out, \ keep the verdict: \ moral dumbfounding", BAD),
                (r"the model", r"social intuitionism: \ intuition first, \ reasoning after, \ mostly to persuade "
                               r"others", MIND),
                (r"the lesson for metaethics", r"if judgments come from intuitions, \ which theory of their content "
                                               r"fits best?", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.48, width=8.2, x_text=-1.9, label_size=20, text_size=20)
        with self.voiceover(
            "Psychologists have asked how moral judgments are actually made. <bookmark mark='a'/>Jonathan Haidt gave "
            "people a story. Julie and Mark, adult brother and sister on holiday, decide to make love once, with every "
            "precaution; no one is harmed, they keep it secret, and it brings them closer. <bookmark mark='b'/>Most "
            "people say at once that it was wrong, then search for reasons; when each reason is ruled out by the "
            "story, they keep the verdict anyway: moral dumbfounding. <bookmark mark='c'/>Haidt's social intuitionist "
            "model, of 2001, says intuition comes first and reasoning after, mostly to persuade others: the emotional "
            "dog wags its rational tail. <bookmark mark='d'/>For metaethics the question is which theory of moral "
            "content fits that psychology: expressivists find their attitudes in it, realists say intuitions can be "
            "perceptions of moral facts."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def folk(self):
        head = label(r"Are ordinary people realists?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the question", r"does ordinary moral talk presuppose objectivity, \ as Mackie claimed?", GREY_A),
                (r"Goodwin and Darley \ (2008)", r"people treat many moral claims as more objective than conventions, \ though less than plain facts", REAL),
                (r"variation", r"objectivity is attributed claim by claim, \ and varies between people and cultures", MIND),
                (r"for the theories", r"if folk morality is mixed, \ every metaethics will be partly revisionary", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Experimental philosophers have tested Mackie's premise, that ordinary moral talk presupposes "
            "objectivity. <bookmark mark='a'/>Does it? <bookmark mark='b'/>Geoffrey Goodwin and John Darley found in "
            "2008 that people treat many moral claims as more objective than social conventions, though less than "
            "plain matters of fact. <bookmark mark='c'/>And they attribute objectivity claim by claim: more to the "
            "wrongness of robbery than to the wrongness of abortion, with variation between people and cultures. "
            "<bookmark mark='d'/>If ordinary morality is mixed in this way, then every metaethical theory will be "
            "partly revisionary of it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def foundations(self):
        head = label(r"Moral foundations \ (Graham, \ Haidt and Nosek, \ 2009)", font_size=30, color=CONN).to_edge(
            UP, buff=0.35)
        names = [(r"care / harm", REAL), (r"fairness / cheating", IS), (r"loyalty / betrayal", OUGHT),
                 (r"authority / subversion", MIND), (r"sanctity / degradation", EXPR), (r"liberty / oppression", ANTI)]
        tiles = VGroup(*[VGroup(RoundedRectangle(width=3.6, height=0.8, corner_radius=0.1, stroke_color=c,
                                                 fill_color=c, fill_opacity=0.2), label(n, font_size=20, color=c))
                         for n, c in names]).arrange_in_grid(rows=2, cols=3, buff=0.3).move_to([0, 1.0, 0])
        foot = stack([(r"a handful of intuitive concerns, \ each with an evolutionary story", GREY_A),
                      (r"in their surveys, \ self-described liberals weighted care and fairness most; \ conservatives "
                       r"weighted all five more evenly", MIND),
                      (r"critics: \ the list is a hypothesis, \ the measures contested, \ and the step to `ought' "
                       r"is Hume's gap again", BAD)],
                     font_size=19, buff=0.2).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "Haidt and his colleagues went on to sort moral intuitions into foundations. <bookmark mark='a'/>Care and "
            "harm; fairness and cheating; loyalty and betrayal; authority and subversion; sanctity and degradation; "
            "and later, liberty and oppression. Each comes with an evolutionary story. <bookmark mark='b'/>In the "
            "surveys of Jesse Graham, Haidt and Brian Nosek, in 2009, self-described liberals weighted care and "
            "fairness most heavily, while conservatives weighted all five more evenly. <bookmark mark='c'/>Critics "
            "say the list is a hypothesis and the measures are contested; and whatever the description, the step from "
            "what people value to what they ought to value is Hume's gap again."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in tiles], lag_ratio=0.25), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def greene(self):
        head = label(r"Two systems, \ and the trolley in the scanner", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"Greene et al. \ (2001)", r"brain imaging: \ `personal' dilemmas like the footbridge engage "
                                            r"emotion-related regions more than `impersonal' ones like the switch", MIND),
                (r"dual process", r"fast emotional responses favour deontological verdicts; \ slower reasoning, \ "
                                  r"consequentialist ones \ (Greene, \ \textit{Moral Tribes}, \ 2013)", MIND),
                (r"the debate", r"McGuire et al. \ (2009): \ the effect was driven by a few items; \ later studies "
                                r"mixed", BAD),
                (r"Berker \ (2009)", r"`the normative insignificance of neuroscience': \ the data matter only through "
                                     r"a normative premise, \ which does all the work", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.45, width=8.4, x_text=-1.8, label_size=20, text_size=19)
        with self.voiceover(
            "Joshua Greene put the trolley problem of Part 35 in a brain scanner. <bookmark mark='a'/>In 2001 he and "
            "his colleagues reported that personal dilemmas like the footbridge engage regions associated with "
            "emotion more than impersonal ones like the switch. <bookmark mark='b'/>His dual-process theory says fast "
            "emotional responses drive deontological verdicts, and slower reasoning drives consequentialist ones; in "
            "Moral Tribes, of 2013, he argued that we should trust the slow system in unfamiliar cases. "
            "<bookmark mark='c'/>The data were disputed: a reanalysis by Jonathan McGuire and colleagues in 2009 found "
            "the effect driven by a handful of items, and later studies are mixed. <bookmark mark='d'/>Selim Berker "
            "argued in 2009 that neuroscience is normatively insignificant here: the data bear on what we ought to "
            "think only through a normative premise, such as that emotional responses are unreliable, and that "
            "premise does all the work."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def grammar(self):
        head = label(r"A moral grammar? \ (Mikhail, \ 2011)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"the analogy", r"Rawls's suggestion, \ made precise: \ moral judgment as a faculty like Chomsky's "
                                 r"grammar, \ with unconscious principles", MIND),
                (r"the evidence", r"people across cultures distinguish intended harm from foreseen harm, \ and doing "
                                  r"from allowing, \ without being able to say so", REAL),
                (r"the structure", r"parse an act into its means and its side effects, \ then apply something like "
                                   r"double effect: \ Part 35's doctrine, \ as a computation", OUGHT),
                (r"for metaethics", r"a universal grammar would be a fact about us, \ not about value: \ Hume's gap "
                                    r"stands", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "John Mikhail took up a suggestion of Rawls's and made it precise. <bookmark mark='a'/>Perhaps moral "
            "judgment is a faculty like Chomsky's grammar, governed by principles we use without being able to state "
            "them. <bookmark mark='b'/>The evidence: people in many cultures distinguish harm intended as a means "
            "from harm foreseen as a side effect, and doing from allowing, in judgments about trolley cases, while "
            "unable to explain the difference. <bookmark mark='c'/>Mikhail's theory parses each act into its means "
            "and its side effects, then applies something like the doctrine of double effect of Part 35, as a "
            "computation. <bookmark mark='d'/>But even a universal moral grammar would be a fact about us, not "
            "about value; whether its verdicts are correct is Hume's question again."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
