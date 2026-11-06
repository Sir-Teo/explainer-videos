from __future__ import annotations

from videos.philosophy.philosophy40.common import *  # noqa: F403


class Art(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"What is art?", r"What makes a carton of soap pads a work of art?", lit=(1956, 1964), part=PART)
        with self.voiceover("Chapter nine. What is art?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.theories()
        self.brillo()
        self.institution()
        self.everyday()
        self.value()

    def theories(self):
        head = history_card(1956, r"Morris Weitz", r"``The Role of Theory in Aesthetics''", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"Tolstoy \ (1897)", r"\textit{What Is Art?}: \ art infects others with feelings the artist has lived through", ART),
                (r"Bell \ (1914)", r"significant form: \ lines and colours combined to move us aesthetically", FORM),
                (r"Collingwood \ (1938)", r"art proper is the expression of emotion, \ discovered in the making", TASTE),
                (r"Weitz \ (1956)", r"`art' is an open concept, \ held together by family resemblance: \ no definition is possible", BAD)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "What is art? Each answer of the early twentieth century was soon refuted by the art that followed it. "
            "<bookmark mark='a'/>Leo Tolstoy's What Is Art?, of 1897, held that art infects others with feelings the "
            "artist has lived through. <bookmark mark='b'/>Clive Bell, in 1914, called the essential quality "
            "significant form: lines and colours combined to move us aesthetically. <bookmark mark='c'/>R. G. "
            "Collingwood's The Principles of Art, of 1938, made art proper the expression of emotion, discovered in "
            "the making. <bookmark mark='d'/>Then Morris Weitz argued in 1956, with Wittgenstein's family resemblance "
            "from Part 28, that art is an open concept with no definition, because artists keep making new kinds of "
            "it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def brillo(self):
        head = label(r"Brillo boxes", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Duchamp \ (1917)", r"\textit{Fountain}: \ a urinal, \ signed R. Mutt, \ submitted to an exhibition", ART),
                (r"Warhol \ (1964)", r"\textit{Brillo Box}: \ indistinguishable from the cartons in a supermarket stockroom", TASTE),
                (r"Danto \ (1964)", r"``The Artworld'': \ what makes it art is no visible property, \ but an atmosphere of theory and history", FORM),
                (r"Danto \ (1981)", r"\textit{The Transfiguration of the Commonplace}: \ artworks are about something, \ and embody their meaning", SYM)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Two objects forced the question into a new form. <bookmark mark='a'/>In 1917 Marcel Duchamp submitted "
            "Fountain, a urinal signed R. Mutt, to an exhibition. <bookmark mark='b'/>In 1964 Andy Warhol exhibited "
            "Brillo Box, indistinguishable to the eye from the cartons in a supermarket stockroom. <bookmark "
            "mark='c'/>Arthur Danto's essay The Artworld, of the same year, argued that what makes one box art and "
            "the other not is no visible property, but an atmosphere of artistic theory and a knowledge of the "
            "history of art. <bookmark mark='d'/>His Transfiguration of the Commonplace, of 1981, added that artworks "
            "are about something and embody their meaning, which a carton does not."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def institution(self):
        head = label(r"The institutional theory, \ and after", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Dickie \ (1974)", r"an artwork is an artefact on which someone acting for the artworld has conferred the status of candidate for appreciation", ART),
                (r"the objection", r"circular, \ and it cannot say why the artworld's choices are reasons", BAD),
                (r"Levinson \ (1979)", r"historical definition: \ intended for regard in some way earlier art was regarded", TASTE),
                (r"cluster accounts", r"Gaut \ (2000): \ ten criteria, \ none necessary, \ enough of them sufficient", SYM)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Definitions came back, built on Danto's insight. <bookmark mark='a'/>George Dickie's institutional "
            "theory, of 1974, says an artwork is an artefact on which someone acting on behalf of the artworld has "
            "conferred the status of candidate for appreciation. <bookmark mark='b'/>Critics called it circular, and "
            "asked why the artworld's choices should be reasons for anyone. <bookmark mark='c'/>Jerrold Levinson's "
            "historical definition, of 1979, says a work is art if it is intended for regard in some way that earlier "
            "art was correctly regarded. <bookmark mark='d'/>And Berys Gaut's cluster account of 2000 lists ten "
            "criteria, among them expressing emotion, being skilful and belonging to an established art form, none "
            "necessary and enough of them sufficient: the open concept, tamed."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def everyday(self):
        head = label(r"Beyond the gallery", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"nature", r"Hepburn \ (1966): \ nature has no frame, \ and invites a different appreciation", SYM),
                (r"science", r"Carlson \ (1979): \ appreciate a landscape through the knowledge of what it is", FORM),
                (r"everyday aesthetics", r"Saito \ (2007): \ the look of laundry, \ the feel of tools, \ the taste of food", TASTE),
                (r"Sibley \ (1959)", r"aesthetic concepts: \ graceful, \ garish, \ balanced: \ applied by taste, \ never by rule", ART)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Aesthetics also looks beyond art. <bookmark mark='a'/>Ronald Hepburn argued in 1966 that nature has no "
            "frame and invites a different kind of appreciation, in which we are part of what we appreciate. "
            "<bookmark mark='b'/>Allen Carlson held in 1979 that we should appreciate a landscape through scientific "
            "knowledge of what it is, as we appreciate art through knowledge of its kind. <bookmark mark='c'/>Yuriko "
            "Saito's Everyday Aesthetics, of 2007, turned to the look of laundry on a line, the feel of tools and the "
            "taste of food. <bookmark mark='d'/>And Frank Sibley argued in 1959 that aesthetic concepts, such as "
            "graceful, garish and balanced, are applied by taste and never by rule: no list of features ever "
            "logically suffices for grace. That is the Wall again."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def value(self):
        head = label(r"What is art good for?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"hedonism", r"art's value is the pleasure of experiencing it", TASTE),
                (r"cognitivism", r"art yields knowledge: \ Nussbaum \ (1990): \ novels as moral philosophy", FORM),
                (r"Lopes \ (2018)", r"\textit{Being for Beauty}: \ aesthetic reasons are reasons for the practices of experts in a domain", SYM),
                (r"the open question", r"each theory fits some art, \ and some art defies each", BAD)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Why does art matter? <bookmark mark='a'/>Aesthetic hedonism says its value is the pleasure of "
            "experiencing it. <bookmark mark='b'/>Cognitivists say art yields knowledge: Martha Nussbaum's Love's "
            "Knowledge, of 1990, read novels as moral philosophy. <bookmark mark='c'/>Dominic McIver Lopes's Being "
            "for Beauty, of 2018, ties aesthetic reasons to the practices of people expert in a domain, such as "
            "dancers or potters, rather than to pleasure. <bookmark mark='d'/>Each theory fits some art, and some art "
            "seems designed to defy each."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
