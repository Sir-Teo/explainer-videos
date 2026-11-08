from __future__ import annotations

from videos.philosophy.philosophy38.common import *  # noqa: F403


class Liberty(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Liberty", r"Freedom from what, \ and to do what?", lit=(1958, 1997), part=PART)
        with self.voiceover("Chapter eight. Liberty."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.berlin()
        self.maccallum()
        self.measure()
        self.pettit()
        self.constant()

    def berlin(self):
        head = history_card(1958, r"Isaiah Berlin", r"``Two Concepts of Liberty''", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"negative liberty", r"freedom from interference: \ the area within which I can act unobstructed by others", LIB),
                (r"positive liberty", r"freedom to be one's own master: \ self-government, \ by a person or a people", COM),
                (r"Berlin's warning", r"positive liberty can be inverted: \ a `true self' to be forced to be free, \ by those who claim to know it", BAD),
                (r"pluralism", r"values are many and can conflict: \ no final harmony in which all goods coexist", GOAL)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Isaiah Berlin's lecture Two Concepts of Liberty, of 1958, set the terms of the modern debate. <bookmark "
            "mark='a'/>Negative liberty is freedom from interference: the area within which I can act unobstructed by "
            "others. <bookmark mark='b'/>Positive liberty is freedom to be one's own master: self-government, by a "
            "person or a people. <bookmark mark='c'/>Berlin warned that the positive idea can be inverted: once there "
            "is a true self, distinct from the empirical one, those who claim to know it may force people to be free, "
            "in Rousseau's phrase. <bookmark mark='d'/>Behind the warning was value pluralism: goods are many and can "
            "conflict, and there is no final harmony in which all of them coexist."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def maccallum(self):
        head = label(r"One concept, \ three places \ (MacCallum, \ 1967)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the triad", r"$x$ is free from $y$ to do or become $z$: \ every claim about liberty fills three places", LIB),
                (r"negative views", r"fix $y$ as other people's deliberate interference", MKT),
                (r"positive views", r"widen $y$ to include ignorance, \ compulsion or lack of means, \ and $z$ to self-realization", COM),
                (r"G. A. Cohen", r"money is a ticket: \ without it, \ you will be stopped at the door, \ so poverty is unfreedom", FAIR)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Gerald MacCallum argued in 1967 that there is really one concept of liberty. <bookmark mark='a'/>Every "
            "claim about freedom fills three places: an agent x is free from some obstacle y to do or become z. "
            "<bookmark mark='b'/>Negative theorists fix y as deliberate interference by other people. <bookmark "
            "mark='c'/>Positive theorists widen y to include ignorance, compulsion or lack of means, and z to "
            "self-realization. <bookmark mark='d'/>G. A. Cohen added that money is like a ticket: someone without it "
            "who tries to board the train will be physically stopped, so poverty is a lack of freedom even on the "
            "negative view."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def pettit(self):
        head = label(r"Freedom as non-domination \ (Pettit, \ 1997)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the slave of a kind master", r"never interfered with, \ yet unfree: \ he lives at another's mercy", BAD),
                (r"domination", r"the capacity to interfere arbitrarily, \ whether or not it is used", POW),
                (r"the republican tradition", r"Cicero; \ Machiavelli; \ Harrington; \ the Commonwealthmen; \ Skinner \ (1998)", HIST),
                (r"the eyeball test", r"can you look others in the eye, \ with no reason for fear or deference?", FAIR)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Philip Pettit's Republicanism, of 1997, revived a third idea. <bookmark mark='a'/>Consider the slave of "
            "a kind master: never interfered with, yet plainly unfree, because he lives at another's mercy. <bookmark "
            "mark='b'/>Freedom is the absence of domination, the capacity of someone to interfere arbitrarily, "
            "whether or not it is used. <bookmark mark='c'/>Pettit and the historian Quentin Skinner traced the idea "
            "through Cicero, Machiavelli and the English Commonwealthmen. <bookmark mark='d'/>Pettit's eyeball test "
            "asks whether you can look others in the eye without reason for fear or deference."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def constant(self):
        head = label(r"Liberty, \ ancient and modern", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Constant \ (1819)", r"the liberty of the ancients, \ sharing in collective rule; \ of the moderns, \ peaceful enjoyment of private independence", HIST),
                (r"Mill \ (1859)", r"the harm principle: \ power may be exercised against one's will only to prevent harm to others", LIB),
                (r"Hart; \ Feinberg", r"legal moralism and paternalism: \ when may the law enforce morality, \ or protect us from ourselves?", MKT),
                (r"Thaler--Sunstein \ (2008)", r"libertarian paternalism: \ a default changes choices without removing any", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The distinction is older than Berlin. <bookmark mark='a'/>Benjamin Constant's lecture of 1819 contrasted "
            "the liberty of the ancients, sharing in collective rule, with the liberty of the moderns, the peaceful "
            "enjoyment of private independence. <bookmark mark='b'/>John Stuart Mill's On Liberty, of 1859, stated "
            "the harm principle: power may rightly be exercised over a person against their will only to prevent harm "
            "to others. <bookmark mark='c'/>H. L. A. Hart and Joel Feinberg asked when, if ever, the law may enforce "
            "morality, or protect us from ourselves. <bookmark mark='d'/>And Richard Thaler and Cass Sunstein's "
            "libertarian paternalism, of 2008, proposed defaults and nudges that change choices without removing any, "
            "which recommender systems now apply at enormous scale."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def measure(self):
        head = label(r"Measuring freedom", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Pattanaik--Xu \ (1990)", r"three axioms on menus: \ all single options are equal; \ $\{x, y\} \succ \{x\}$; \ adding a new option to two menus preserves their order", LIB),
                (r"the theorem", r"they force ranking by size alone: \ $A \succeq B \iff |A| \ge |B|$", GOAL),
                (r"Sen \ (1991)", r"a choice among three bad options is not more freedom than one good one: \ preferences must enter", BAD),
                (r"Carter \ (1999); \ Kramer \ (2003)", r"freedom has non-specific value, \ and can be measured; \ \textit{The Quality of Freedom}", COM)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Can freedom be measured? <bookmark mark='a'/>Prasanta Pattanaik and Yongsheng Xu proposed, in 1990, "
            "three axioms for ranking menus of options by the freedom they offer: all menus with a single option are "
            "equally free; a menu of two options is freer than either option alone; and adding the same new option to "
            "two menus preserves their order. <bookmark mark='b'/>They proved that these force the simplest possible "
            "measure: count the options. <bookmark mark='c'/>Sen replied that a choice among three bad options is not "
            "more freedom than a single good one, so preferences, or reasons to value options, must enter the "
            "measure. <bookmark mark='d'/>Ian Carter argued that freedom also has non-specific value, beyond the "
            "value of what it lets us do, and Matthew Kramer's The Quality of Freedom built a detailed measure on "
            "that idea."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
