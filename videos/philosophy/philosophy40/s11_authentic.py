from __future__ import annotations

from videos.philosophy.philosophy40.common import *  # noqa: F403


class Authentic(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Forgeries and machines", r"Does it matter who made it?", lit=(1968,), part=PART)
        with self.voiceover("Chapter ten. Forgeries and machines."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.forgery()
        self.value()
        self.restore()
        self.ai()
        self.predictors()

    def forgery(self):
        head = history_card(1968, r"Nelson Goodman", r"\textit{Languages of Art}", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"the problem", r"if a forgery cannot be told from the original, \ is it any less beautiful?", TASTE),
                (r"Goodman \ (1968)", r"\textit{Languages of Art}: \ knowing it is a forgery trains the eye to see differences it will later find", FORM),
                (r"autographic and allographic", r"a painting can be forged; \ a symphony cannot: \ any correct performance is the work", SYM),
                (r"van Meegeren", r"painted `Vermeers' that fooled experts; \ in 1945 he painted one under supervision to prove it", ART)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "If you cannot tell a forgery from the original, is it any less valuable? <bookmark mark='a'/>The "
            "question tests whether beauty is in what we see. <bookmark mark='b'/>Nelson Goodman's Languages of Art, "
            "of 1968, argued that knowing a picture is a forgery matters even now, because it trains the eye to look "
            "for differences it may later learn to see. <bookmark mark='c'/>He distinguished autographic arts, like "
            "painting, where the history of production matters and forgery is possible, from allographic arts, like "
            "music, where any correct performance of the score is the work. <bookmark mark='d'/>Han van Meegeren sold "
            "paintings as Vermeers that fooled the experts of the 1930s; accused in 1945 of selling a national "
            "treasure to Hermann Göring, he painted another under supervision to prove he was a forger, not a "
            "collaborator."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def value(self):
        head = label(r"Why provenance matters", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Dutton \ (1979)", r"art is a performance: \ a forgery misrepresents the achievement we admire", TASTE),
                (r"contagion", r"Newman and Bloom \ (2012): \ people value an original partly as a trace of the artist's touch", ART),
                (r"Walton \ (1970)", r"`Categories of Art': \ the same picture looks different as a Picasso and as a forgery", FORM),
                (r"the lesson", r"aesthetic value is not in the visible surface alone", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Why should provenance matter, if the surface is the same? <bookmark mark='a'/>Denis Dutton argued in "
            "1979 that art is a kind of performance, and a forgery misrepresents the achievement we admire. <bookmark "
            "mark='b'/>George Newman and Paul Bloom found in 2012 that people value an original partly as a physical "
            "trace of the artist, a kind of contagion. <bookmark mark='c'/>Kendall Walton's Categories of Art, of "
            "1970, argued that how a work looks depends on the category in which we see it, so the same canvas looks "
            "different as a Picasso and as a copy. <bookmark mark='d'/>Aesthetic value is not in the visible surface "
            "alone."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def ai(self):
        head = label(r"Art by machines", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the prize", r"2022: \ an image made with Midjourney won a prize at the Colorado State Fair", ART),
                (r"the law", r"US Copyright Office \ (2023): \ copyright requires human authorship; \ AI-generated material is excluded", BAD),
                (r"\textit{Thaler v. Perlmutter}", r"a federal court agreed in 2023, \ and the appeal court in 2025", TASTE),
                (r"the philosophy", r"if art needs intention and expression, \ a model's image is not art; \ if it needs only form, \ it may be", FORM)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Machines now make images that win prizes. <bookmark mark='a'/>In 2022 an image made with Midjourney, "
            "Théâtre D'opéra Spatial, won the digital art prize at the Colorado State Fair. <bookmark mark='b'/>The "
            "United States Copyright Office ruled in 2023 that copyright requires human authorship, and that material "
            "generated by AI must be excluded from a registration. <bookmark mark='c'/>In Thaler versus Perlmutter, a "
            "federal court agreed in 2023 that a work made autonomously by a machine cannot be copyrighted, and the "
            "appeals court affirmed in 2025. <bookmark mark='d'/>Philosophically, the answer depends on the theories "
            "of the last chapter: if art requires intention and expression, a model's image is not art, though its "
            "user's choices may be; if art needs only significant form, it may be."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def predictors(self):
        head = label(r"Machines that judge beauty", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"aesthetic predictors", r"models trained on people's ratings of images, \ such as LAION's \ (2022)", FORM),
                (r"and their use", r"used to filter the training images of image generators toward the `prettier'", TASTE),
                (r"the risk", r"a narrowing of taste: \ the averageness of faces, \ applied to all images", BAD),
                (r"Hume, \ again", r"whose ratings? \ a panel of the many, \ not of true judges; \ and no test of time", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Machines now also judge beauty. <bookmark mark='a'/>Aesthetic predictors are models trained on people's "
            "ratings of images, such as the predictor released with the LAION image collection in 2022. <bookmark "
            "mark='b'/>They have been used to filter the training images of image generators toward those rated "
            "prettier. <bookmark mark='c'/>The risk is a narrowing of taste: the averageness that makes composite "
            "faces attractive, applied to all images. <bookmark mark='d'/>And Hume's question returns: whose ratings? "
            "A large panel of the many, not of true judges, and with no test of time."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def restore(self):
        head = label(r"Restoration", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the Sistine Chapel", r"cleaned 1980--1994: \ bright colours appeared; \ critics feared the final layers were lost", ART),
                (r"the question", r"is the work what the artist made, \ or what centuries made of it?", TASTE),
                (r"Brandi \ (1963)", r"\textit{Theory of Restoration}: \ restore the unity of the work without faking history", FORM)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Authenticity also governs restoration. <bookmark mark='a'/>The cleaning of Michelangelo's Sistine Chapel "
            "ceiling, from 1980 to 1994, revealed brilliant colours; critics feared that the artist's final layers "
            "had been removed with the grime. <bookmark mark='b'/>Is the work what the artist made, or what the "
            "centuries made of it? <bookmark mark='c'/>Cesare Brandi's Theory of Restoration, of 1963, answered: "
            "restore the potential unity of the work, without faking history, and leave every intervention "
            "recognizable."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
