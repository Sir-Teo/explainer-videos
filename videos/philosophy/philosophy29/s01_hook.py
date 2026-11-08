from __future__ import annotations

from videos.philosophy.philosophy29.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.puzzle()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"We must go back to the `things themselves'.", r"Edmund Husserl",
                       r"\textit{Logical Investigations} \ (1900--1901)", width=8.0, font_size=30).next_to(t, DOWN,
                                                                                                     buff=0.45)
        with self.voiceover(
            "Part 28 ended with a question about machines that have only ever seen text: is there meaning without a "
            "world? This part turns from language to the world as it is lived: to experience itself, and to the "
            "tradition that made experience its subject. <bookmark mark='a'/>In 1900 Edmund Husserl gave that "
            "tradition its slogan. We must go back to the things themselves: not to theories about experience, but "
            "to what shows itself, exactly as it shows itself. <bookmark mark='b'/>From Husserl came phenomenology; "
            "from phenomenology, Heidegger and the existentialists, hermeneutics, and the critique of artificial "
            "intelligence that gave AI one of its hardest problems."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=ACT, scale_factor=1.03))
        self.clear_scene()

    def puzzle(self):
        head = label(r"Four questions about experience", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"aboutness", r"every thought is a thought \textit{of} something: \ even of something that does not "
                           r"exist. \ How?", ACT),
            (r"time", r"we hear a melody, \ though at each instant only one note sounds: \ where is the rest of it?",
             TIME),
            (r"world", r"is the world first a collection of objects, \ or a field of things to do with?", WORLD),
            (r"relevance", r"a robot must know what its actions change and what they leave alone: \ can any set of "
                           r"rules tell it?", BAD),
        ]
        g = rows_table(rows, top=1.6, gap=0.55)
        with self.voiceover(
            "Four questions run through it. <bookmark mark='a'/>Aboutness: every thought is a thought of something, "
            "every fear a fear of something, even when the thing does not exist. How can a state of mind be about "
            "anything? <bookmark mark='b'/>Time: we hear a melody, though at each instant only one note is sounding. "
            "Where, in the present, is the rest of the melody? <bookmark mark='c'/>World: is the world first of all "
            "a collection of objects with properties, as science describes it, or a field of things to do things "
            "with? <bookmark mark='d'/>And relevance: a robot that acts must know what its actions change and what "
            "they leave alone. Can any finite set of rules tell it? That last question, the frame problem, is this "
            "part's brick in the Wall."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Brentano: \ intentionality; \ Husserl: \ the reduction, \ noesis and noema, \ a cube's profiles, \ "
            r"computed",
            r"Husserl's time diagram, \ animated; \ a retentional present, \ built",
            r"Heidegger: \ being-in-the-world, \ the hammer, \ care; \ Dreyfus against symbolic AI",
            r"the frame problem: \ a planner and Dennett's robots, \ built \ (the Wall; \ a Price List)",
            r"Merleau-Ponty's body; \ 4E cognition; \ Braitenberg's vehicles, \ simulated",
            r"Kierkegaard, \ Nietzsche, \ Sartre, \ Beauvoir; \ the eternal return, \ computed",
            r"Gadamer's circle; \ Saussure and Derrida; \ word vectors under rotation, \ computed",
            r"Foucault's gaze and Goodhart's law; \ Habermas; \ the Kyoto school; \ bridges",
        ], font_size=22)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>Brentano's thesis that the mental is the intentional, and Husserl's method "
            "for describing experience, with a cube that is never seen whole. <bookmark mark='b'/>Husserl's analysis "
            "of the living present, with his own diagram animated, and a model of retention built. "
            "<bookmark mark='c'/>Heidegger's being-in-the-world and the hammer, and Hubert Dreyfus's attack on "
            "symbolic AI. <bookmark mark='d'/>The frame problem, with a planner and Daniel Dennett's three robots, "
            "this part's brick in the Wall and its Price List. <bookmark mark='e'/>Merleau-Ponty's lived body, "
            "embodied cognition, and vehicles that seem to have feelings. <bookmark mark='f'/>The existentialists, "
            "and Nietzsche's eternal return, tested on a reversible world. <bookmark mark='g'/>Interpretation, "
            "structure and difference, with word vectors rotated. <bookmark mark='h'/>And power, communication, the "
            "Kyoto school, and the bridges between continental and analytic philosophy."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
