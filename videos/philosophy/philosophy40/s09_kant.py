from __future__ import annotations

from videos.philosophy.philosophy40.common import *  # noqa: F403


class Kant(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Disinterested pleasure", r"How can a feeling claim everyone's agreement?", lit=(1790,), part=PART)
        with self.voiceover("Chapter eight. Disinterested pleasure."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.moments()
        self.free()
        self.sublime()
        self.after()
        self.bourdieu()

    def moments(self):
        head = history_card(1790, r"Immanuel Kant", r"\textit{Critique of the Power of Judgment}", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"disinterested", r"the pleasure in the beautiful is independent of any desire for the object's existence", TASTE),
                (r"universal", r"we speak as if beauty were a property, \ and demand everyone's agreement, \ though no concept proves it", SYM),
                (r"purposive", r"the form seems designed, \ though we can name no purpose: \ purposiveness without a purpose", FORM),
                (r"necessary", r"a common sense: \ the judgment presupposes a shared capacity of feeling", ART)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Immanuel Kant's Critique of the Power of Judgment, of 1790, gave the judgment of taste four moments. "
            "<bookmark mark='a'/>First, the pleasure is disinterested: it does not depend on wanting the object to "
            "exist, to own it or eat it. <bookmark mark='b'/>Second, it is universal without a concept: we speak as "
            "if beauty were a property of the thing, and demand everyone's agreement, though no argument can prove a "
            "rose beautiful. <bookmark mark='c'/>Third, the beautiful has the form of purposiveness without a "
            "purpose: it looks designed, though we can name nothing it is for. <bookmark mark='d'/>Fourth, the "
            "judgment is necessary, resting on a common sense, a capacity of feeling we presuppose all people share."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def free(self):
        head = label(r"Free play, \ free and dependent beauty", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"free play", r"imagination and understanding harmonize, \ without a concept fixing the result: \ that harmony is the pleasure", FORM),
                (r"free beauty", r"flowers, \ birds, \ designs \`a la grecque, \ music without words: \ judged without a concept of what they should be", SYM),
                (r"dependent beauty", r"a horse, \ a church, \ a human being: \ beauty measured against what the thing is for", TASTE),
                (r"the antinomy", r"taste is not based on concepts \ (no disputing it) \ and is \ (we argue about it): \ resolved by an indeterminate concept", ART)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The faculties explain the pleasure. <bookmark mark='a'/>In judging beauty, imagination and understanding "
            "fall into free play, a harmony that no concept fixes, and that harmony is what we feel. <bookmark "
            "mark='b'/>Free beauty, as in flowers, birds, ornamental patterns and music without words, is judged "
            "without any concept of what the thing should be. <bookmark mark='c'/>Dependent beauty, of a horse, a "
            "church or a human being, is judged against what the thing is for. <bookmark mark='d'/>And Kant states "
            "the paradox of taste as an antinomy: taste is not based on concepts, or we could dispute it by proof; "
            "and it is, or we could not even argue about it. His resolution is that it rests on an indeterminate "
            "concept, the supersensible ground of nature and of ourselves."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def sublime(self):
        head = label(r"The sublime", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"mathematical", r"the starry sky, \ the ocean: \ magnitude that imagination cannot take in, \ while reason thinks it as a whole", FORM),
                (r"dynamical", r"storms, \ volcanoes, \ waterfalls: \ might that could crush us, \ seen from safety", BAD),
                (r"the turn", r"what we finally admire is our own vocation as rational beings, \ superior to nature", TASTE),
                (r"genius", r"fine art is the art of genius: \ a talent that gives the rule to art, \ which no rule can teach", ART)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Kant also gave the sublime its classic analysis. <bookmark mark='a'/>The mathematical sublime is "
            "magnitude, the starry sky or the ocean, that imagination cannot take in, while reason thinks it as a "
            "whole. <bookmark mark='b'/>The dynamical sublime is might, storms, volcanoes and waterfalls, that could "
            "crush us, seen from safety. <bookmark mark='c'/>In both, what we finally admire is our own vocation as "
            "rational beings, superior to nature. <bookmark mark='d'/>And fine art is the art of genius, a talent "
            "that gives the rule to art, which no rule can teach: the Wall of this part, stated by Kant himself."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def after(self):
        head = label(r"After Kant", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Schiller \ (1795)", r"\textit{On the Aesthetic Education of Man}: \ in the play drive, \ sense and reason are reconciled", TASTE),
                (r"Hegel", r"art is the sensuous appearance of the Idea; \ in modern times it has been surpassed by philosophy", FORM),
                (r"Schopenhauer \ (1819)", r"music is a copy of the will itself, \ not of its appearances", SYM),
                (r"Nietzsche \ (1872)", r"\textit{The Birth of Tragedy}: \ the Apollonian and the Dionysian", ART)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Kant's successors made art the centre of philosophy. <bookmark mark='a'/>Friedrich Schiller's Letters on "
            "the Aesthetic Education of Man, of 1795, held that in the play drive, sense and reason are reconciled, "
            "and that people are fully human only when they play. <bookmark mark='b'/>Hegel called art the sensuous "
            "appearance of the Idea, and argued that in modern times it has been surpassed by philosophy, the thesis "
            "of the end of art. <bookmark mark='c'/>Arthur Schopenhauer, in 1819, held that music copies not the "
            "appearances of the world but the will itself. <bookmark mark='d'/>And Friedrich Nietzsche's The Birth of "
            "Tragedy, of 1872, found in Greek tragedy the union of two forces: the Apollonian, of form and dream, and "
            "the Dionysian, of intoxication."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def bourdieu(self):
        head = label(r"Whose taste?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Bourdieu \ (1979)", r"\textit{Distinction}: \ the `pure gaze' Kant describes is a class habit, \ which marks social position", BAD),
                (r"the data", r"surveys of 1960s France: \ taste in music and art follows education and class", TASTE),
                (r"Korsmeyer \ (2004)", r"\textit{Gender and Aesthetics}: \ the sublime gendered male, \ the beautiful female", ART),
                (r"the reply", r"that taste has social causes does not show that no taste is better: \ the genetic fallacy", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The sociology of taste challenged Kant's universality. <bookmark mark='a'/>Pierre Bourdieu's "
            "Distinction, of 1979, argued that the disinterested gaze Kant describes is a habit of the educated "
            "classes, and that taste marks social position. <bookmark mark='b'/>His surveys of 1960s France found "
            "taste in music and art following education and class closely. <bookmark mark='c'/>Carolyn Korsmeyer's "
            "Gender and Aesthetics, of 2004, traced how the sublime was gendered male and the beautiful female. "
            "<bookmark mark='d'/>The reply is that showing that a taste has social causes does not show that no taste "
            "is better than another; to think so is the genetic fallacy."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
