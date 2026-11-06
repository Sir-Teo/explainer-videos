from __future__ import annotations

from videos.philosophy.philosophy38.common import *  # noqa: F403


class Plato(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"The interest of the stronger", r"Is justice more than power?", lit=(-380,), part=PART)
        with self.voiceover("Chapter one. The interest of the stronger."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.thrasymachus()
        self.gyges()
        self.city()
        self.aristotle()

    def thrasymachus(self):
        head = label(r"Thrasymachus", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the claim", r"justice is nothing but the advantage of the stronger: \ each ruling group makes laws in its own interest, \ and calls obeying them just", POW),
                (r"Socrates's reply", r"a ruler as such, \ like a doctor or a ship's captain, \ aims at the good of those in his care, \ not his own", FAIR),
                (r"the challenge", r"the unjust man does better than the just, \ in money, \ office and friends", POW),
                (r"why it matters", r"political philosophy must answer the cynic: \ show that justice is more than power dressed up", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Political philosophy begins with a provocation. <bookmark mark='a'/>In the first book of Plato's "
            "Republic, the sophist Thrasymachus says justice is nothing but the advantage of the stronger: each "
            "ruling group makes laws in its own interest, and calls obedience to them just. <bookmark "
            "mark='b'/>Socrates replies that a ruler, as a ruler, is like a doctor or a ship's captain, whose craft "
            "aims at the good of those in his care. <bookmark mark='c'/>Thrasymachus is not impressed: look at life, "
            "he says, and the unjust man does better than the just, in money, office and friends. <bookmark "
            "mark='d'/>Every theory in this part is an attempt to answer him, to show that justice is more than power "
            "dressed up as principle."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def gyges(self):
        head = label(r"The ring of Gyges", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the story", r"a shepherd finds a ring that makes him invisible; \ he seduces the queen, \ kills the king, \ and takes the throne", POW),
                (r"Glaucon's point", r"no one is just willingly: \ give the just man the ring, \ and he would act as the unjust one does", BAD),
                (r"the contract", r"justice is a compromise: \ we agree not to wrong each other because we fear being wronged", COM),
                (r"the demand", r"show that justice is good in itself, \ for the just person, \ even unseen", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "In the second book Glaucon sharpens the challenge. <bookmark mark='a'/>A shepherd named Gyges finds a "
            "ring that makes him invisible; he seduces the queen, kills the king and takes the throne. <bookmark "
            "mark='b'/>No one, Glaucon says, is just willingly: give the just man such a ring, and he would act as "
            "the unjust man does. <bookmark mark='c'/>Justice is a compromise: we agree not to wrong each other "
            "because each of us fears being wronged more than we enjoy wronging. That is the first social contract "
            "theory, two thousand years before Hobbes. <bookmark mark='d'/>Socrates must show that justice is good in "
            "itself, for the just person, even when no one is watching."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def city(self):
        head = label(r"Justice in the city and the soul", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the method", r"look for justice writ large, \ in a city, \ to see it in the individual", COM),
                (r"the city", r"rulers, \ auxiliaries, \ producers: \ justice is each class doing its own work and not meddling with another's", FAIR),
                (r"the soul", r"reason, \ spirit, \ appetite: \ a just person is one whose reason rules, \ with spirit as its ally", FAIR),
                (r"the verdict", r"injustice is a disorder of the soul, \ a kind of sickness: \ so justice pays, \ seen or unseen", GOAL),
                (r"the price", r"philosopher-kings, \ a noble lie, \ censorship: \ Popper's charge of totalitarianism \ (1945)", BAD)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Plato's answer runs through an analogy. <bookmark mark='a'/>Look first for justice writ large, in a "
            "city, and then find it in the individual. <bookmark mark='b'/>The ideal city has three classes, rulers, "
            "auxiliaries and producers; it is just when each does its own work and does not meddle with another's. "
            "<bookmark mark='c'/>The soul has three parts too, reason, spirit and appetite; a person is just when "
            "reason rules, with spirit as its ally. <bookmark mark='d'/>Injustice is a disorder of the soul, a kind "
            "of sickness, so justice pays, seen or unseen. <bookmark mark='e'/>The price of the ideal city was "
            "philosopher-kings, a noble lie about the origins of the classes, and censorship of the poets; Karl "
            "Popper, in 1945, called Plato an enemy of the open society."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def aristotle(self):
        head = label(r"Aristotle: \ justice as proportion", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"distributive", r"shares in proportion to merit: \ $\frac{\text{A's share}}{\text{B's share}} = \frac{\text{A's merit}}{\text{B's merit}}$, \ a geometric proportion", FAIR),
                (r"the dispute", r"democrats count free birth, \ oligarchs wealth, \ aristocrats virtue: \ all agree on proportion, \ and disagree about merit", POW),
                (r"corrective", r"in transactions, \ restore the equal: \ take the gain from the wrongdoer and return it, \ an arithmetic proportion", LIB),
                (r"the flute", r"\textit{Politics} III.12: \ the best flutes should go to the best players, \ not the best born: \ Anne's claim", MKT)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Plato's pupil Aristotle gave justice its first precise analysis, in Book Five of the Nicomachean Ethics. "
            "<bookmark mark='a'/>Distributive justice is a proportion: A's share is to B's share as A's merit is to "
            "B's merit. Divide a hundred and twenty among merits of one, two and three, and the just shares are "
            "twenty, forty and sixty. <bookmark mark='b'/>Everyone agrees on the proportion; they disagree about "
            "merit. Democrats count free birth, oligarchs wealth, aristocrats virtue. <bookmark mark='c'/>Corrective "
            "justice, in transactions, is arithmetic: if one party has gained by wronging another, the judge takes "
            "away the gain and restores the equal. <bookmark mark='d'/>And in the Politics, Aristotle asks who should "
            "get the best flutes, and answers: the best players, not the best born, because flutes are for playing. "
            "Anne's claim, in Sen's story, is Aristotle's."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
