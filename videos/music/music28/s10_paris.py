from __future__ import annotations

import numpy as np

from videos.music.music28.common import *  # noqa: F403


class Paris(SoundScene):
    def construct(self):
        chapter(self, 9, r"1913, \ and after", r"Was there really a riot?", extra=((1913, r"the Théâtre des Champs-Élysées opens"),))
        self.premiere()
        self.impression()
        self.legend()
        self.after()
        self.others()

    # ------------------------------------------------------------------
    def premiere(self):
        items = [
            (r"29 May 1913: \ the Ballets Russes, \ Diaghilev's company, \ at the new Théâtre des Champs-Élysées", WHITE),
            (r"choreography by Vaslav Nijinsky: \ dancers stamping, \ feet turned in, \ no ballet grace", WHITE),
            (r"Pierre Monteux conducts; \ the audience laughs, \ whistles, \ shouts back", WHITE),
            (r"the noise drowns the orchestra; \ Nijinsky calls the counts to the dancers from the wings", TUNE),
            (r"within a year, \ in concert without the dancing, \ the score was cheered", GREY_A),
        ]
        rows_scene(self, r"the first night", items,
                   "The Rite's first night has become a legend. <bookmark mark='b'/> On the twenty-ninth of May 1913 "
                   "Sergei Diaghilev's Ballets Russes danced it at the new Théâtre des Champs-Élysées, "
                   "<bookmark mark='c'/> in choreography by Vaslav Nijinsky: dancers stamping, feet turned inwards, none of "
                   "ballet's grace. <bookmark mark='d'/> Pierre Monteux conducted, and parts of the audience laughed, "
                   "whistled and shouted back at each other, <bookmark mark='e'/> so loudly, by several accounts, that "
                   "Nijinsky stood on a chair in the wings calling out the counts to the dancers. <bookmark mark='f'/> Less "
                   "than a year later the score was played in concert, without the dancing, and cheered.", marks="cdef")

    # ------------------------------------------------------------------
    def legend(self):
        rows_ = text_rows([
            (r"the accounts were written down later, \ some decades later, \ and they disagree", WHITE),
            (r"much of the uproar may have been about the dancing, \ not the music", WHITE),
            (r"the `riot' grew in the retelling: \ a founding myth of musical modernism", WHITE),
            (r"a historian's question: \ how many independent witnesses, \ written how soon?", TUNE),
            (r"the same question as Part 23's chant legends, \ and Part 26's metronome", GREY_A),
        ], font_size=24)
        head = label(r"how much of the legend is true?", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "How much of the legend is true? <bookmark mark='a'/> The accounts we have were mostly written down later, some "
            "of them decades later, and they disagree with each other. <bookmark mark='b'/> Much of the uproar may have "
            "been provoked by the dancing rather than the music. <bookmark mark='c'/> And the riot grew in the retelling "
            "into a founding myth of musical modernism. <bookmark mark='d'/> It is a historian's question, of how many "
            "independent witnesses there are and how soon they wrote, <bookmark mark='e'/> the same question the series "
            "asked of the chant legends in Part 23 and of Beethoven's metronome in Part 26."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def after(self):
        items = [
            (r"1914--1918: \ the war ends the Paris of the Ballets Russes' first seasons", WHITE),
            (r"Stravinsky turns to `neoclassicism': \ Baroque forms, \ dry textures \ (\textit{Pulcinella}, \ 1920)", WHITE),
            (r"Bartók's string quartets: \ symmetry, \ folk rhythm and counterpoint together", WHITE),
            (r"the new scales enter film, \ jazz and popular song", TUNE),
            (r"in Vienna, \ a different answer: \ give up the key entirely \ (Part 29)", EAR),
        ]
        rows_scene(self, r"after the Rite", items,
                   "What came after? <bookmark mark='b'/> The war of 1914 to 1918 ended the world of the Ballets Russes' "
                   "first seasons. <bookmark mark='c'/> Stravinsky turned to what was called neoclassicism, Baroque forms in "
                   "dry textures, beginning with Pulcinella in 1920. <bookmark mark='d'/> Bartók's six string quartets combine "
                   "symmetry, folk rhythm and strict counterpoint. <bookmark mark='e'/> The new scales passed into film "
                   "scores, jazz and popular song. <bookmark mark='f'/> And in Vienna, Schoenberg's circle gave a different "
                   "answer: give up the key entirely. That is the next part.", marks="cdef")

    # ------------------------------------------------------------------
    def others(self):
        items = [
            (r"Lili Boulanger \ (1893--1918): \ first woman to win the Prix de Rome for composition, \ 1913", WHITE),
            (r"Nadia Boulanger: \ teacher of a century of composers, \ from Copland to Glass", WHITE),
            (r"Germaine Tailleferre, \ the one woman of Les Six", WHITE),
            (r"Ruth Crawford Seeger \ (1901--1953): \ dissonant counterpoint, \ then American folk song", TUNE),
            (r"the period's history is still being widened", GREY_A),
        ]
        rows_scene(self, r"others in the room", items,
                   "The usual story leaves people out. <bookmark mark='b'/> Lili Boulanger, in 1913, the year of the Rite, "
                   "became the first woman to win the Prix de Rome for composition; she died at twenty-four. "
                   "<bookmark mark='c'/> Her sister Nadia taught a century of composers, from Aaron Copland to Philip Glass. "
                   "<bookmark mark='d'/> Germaine Tailleferre was the one woman of Les Six. <bookmark mark='e'/> In America, "
                   "Ruth Crawford Seeger wrote dissonant counterpoint and then devoted herself to transcribing American folk "
                   "song. <bookmark mark='f'/> The period's history is still being widened.", marks="cdef")

    # ------------------------------------------------------------------
    def impression(self):
        items = [
            (r"`Impressionism': \ a painters' word, \ applied to Debussy against his wishes", WHITE),
            (r"his allies were poets: \ Mallarmé, \ Verlaine, \ the Symbolists", WHITE),
            (r"\textit{Prélude à l'après-midi d'un faune} \ (1894), \ after Mallarmé's poem", WHITE),
            (r"suggestion rather than statement: \ a harmony that does not resolve, \ a form that does not announce itself", TUNE),
            (r"labels are later; \ the music was argued about as it appeared", GREY_A),
        ]
        rows_scene(self, r"not impressionism", items,
                   "Before the Rite, a word about labels. <bookmark mark='b'/> Debussy's music is often called impressionist, after the painters, a word he disliked. <bookmark mark='c'/> His allies were poets, Mallarmé and Verlaine and the Symbolists, <bookmark mark='d'/> and his Prelude to the Afternoon of a Faun, of 1894, follows a poem by Mallarmé. <bookmark mark='e'/> Their ideal was suggestion rather than statement: a harmony that does not resolve, a form that does not announce itself. <bookmark mark='f'/> Such labels come later; the music was argued about as it appeared.", marks="cdef")
