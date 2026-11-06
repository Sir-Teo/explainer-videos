from __future__ import annotations

from videos.philosophy.philosophy40.common import *  # noqa: F403


class Greeks(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Beauty and imitation", r"Is beauty a Form, \ and art a copy of a copy?", lit=(-380, -335), part=PART)
        with self.voiceover("Chapter one. Beauty and imitation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.plato()
        self.aristotle()
        self.later()
        self.rasa()

    def plato(self):
        head = history_card(-380, r"Plato", r"\textit{Symposium}; \ \textit{Republic}", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"the ladder", r"\textit{Symposium}: \ from one beautiful body, \ to all bodies, \ souls, \ laws, \ knowledge, \ and Beauty itself", FORM),
                (r"the critique of art", r"\textit{Republic} X: \ a painting copies a bed, \ which copies the Form: \ twice removed from truth", BAD),
                (r"the danger", r"poetry feeds the passions: \ the poets are banished from the ideal city", ART),
                (r"\textit{Hippias Major}", r"`the beautiful is difficult': \ every definition of beauty fails", TASTE)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Western aesthetics begins with Plato's ambivalence. <bookmark mark='a'/>In the Symposium, Diotima "
            "teaches Socrates a ladder of love: from one beautiful body to all bodies, then to beautiful souls, laws, "
            "kinds of knowledge, and finally to Beauty itself, eternal and unchanging. <bookmark mark='b'/>But in the "
            "tenth book of the Republic, art is imitation: a painter copies a bed, which a carpenter copied from the "
            "Form of the bed, so the painting is twice removed from truth. <bookmark mark='c'/>Poetry feeds the "
            "passions it should tame, and the poets are banished from the ideal city. <bookmark mark='d'/>And the "
            "Hippias Major tests one definition of beauty after another, the appropriate, the useful, the pleasant to "
            "sight and hearing, and ends: the beautiful is difficult."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def aristotle(self):
        head = label(r"Aristotle's \textit{Poetics}", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"mimesis", r"imitation is natural to us, \ and we learn and take pleasure in it: \ even in images of corpses", ART),
                (r"the plot", r"tragedy imitates an action with a beginning, \ middle and end, \ whose parts are necessary or probable", FORM),
                (r"catharsis", r"through pity and fear, \ tragedy accomplishes the catharsis of such emotions", TASTE),
                (r"beauty", r"order, \ symmetry and definiteness, \ in something of a size that can be taken in at once", SYM)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Aristotle answered Plato's charge. <bookmark mark='a'/>Imitation is natural to human beings, and we "
            "learn and take pleasure in it: we enjoy exact images even of things painful to see, such as corpses. "
            "<bookmark mark='b'/>A tragedy imitates a single action with a beginning, a middle and an end, whose "
            "parts follow by necessity or probability. <bookmark mark='c'/>Through pity and fear it accomplishes the "
            "catharsis of such emotions, a word read as purgation, purification or clarification. <bookmark "
            "mark='d'/>And beauty, in the Metaphysics and the Poetics, is order, symmetry and definiteness, in "
            "something of a size that can be taken in at once."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def later(self):
        head = label(r"From Plotinus to Burke", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Plotinus", r"third century: \ beauty is not symmetry alone, \ or a simple colour could not be beautiful: \ it is form shining through", FORM),
                (r"Aquinas", r"integrity, \ proportion and clarity: \ the beautiful is what pleases when seen", SYM),
                (r"Hutcheson \ (1725)", r"an inner sense of beauty, \ responding to uniformity amidst variety", TASTE),
                (r"Burke \ (1757)", r"the sublime, \ born of terror at a safe distance, \ against the beautiful, \ small and smooth", ART)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The tradition developed in two directions. <bookmark mark='a'/>Plotinus, in the third century, objected "
            "that if beauty were symmetry, a simple colour or a single note could not be beautiful; beauty is form "
            "shining through matter. <bookmark mark='b'/>Thomas Aquinas named three conditions: integrity, proportion "
            "and clarity; the beautiful is what pleases when it is seen. <bookmark mark='c'/>Francis Hutcheson, in "
            "1725, posited an inner sense of beauty that responds to uniformity amidst variety. <bookmark "
            "mark='d'/>And Edmund Burke's Enquiry, of 1757, set against the beautiful, small and smooth, the sublime: "
            "the delight of terror felt at a safe distance."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def rasa(self):
        head = label(r"Rasa", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the \textit{Natyashastra}", r"Bharata's treatise on drama: \ a play produces \textit{rasa}, \ an aesthetic flavour", EAST),
                (r"eight rasas", r"the erotic, \ comic, \ pathetic, \ furious, \ heroic, \ terrible, \ odious, \ marvellous", TASTE),
                (r"Abhinavagupta \ (c. 1000)", r"rasa is not the character's emotion, \ nor the spectator's, \ but a universalized savouring", FORM),
                (r"the parallel", r"like Kant's disinterest: \ emotion freed from personal stake", SYM)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "India developed an aesthetics of its own. <bookmark mark='a'/>The Natyashastra, Bharata's ancient "
            "treatise on drama, holds that a play produces rasa, an aesthetic flavour savoured by the audience. "
            "<bookmark mark='b'/>It lists eight: the erotic, comic, pathetic, furious, heroic, terrible, odious and "
            "marvellous; later writers added peace as a ninth. <bookmark mark='c'/>The philosopher Abhinavagupta, "
            "around the year one thousand, argued that rasa is neither the character's emotion nor the spectator's "
            "own, but a universalized savouring of emotion. <bookmark mark='d'/>That is close to Kant's disinterested "
            "pleasure: emotion freed from personal stake."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
