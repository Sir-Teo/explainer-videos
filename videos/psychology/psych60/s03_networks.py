from __future__ import annotations

from videos.psychology.psych60.common import *  # noqa: F403


class Networks(VoiceoverScene):
    def construct(self):
        card_section(self, 2, r"Networks as models of the mind", r"When does a network explain a brain?",
                     scale=("brain",), marr=("how",))
        self.vision()
        self.language()
        self.lesson()

    def vision(self):
        rows_section(self, r"Vision", [
            (r"Yamins and DiCarlo, \ 2016: \ networks trained only to recognize objects predict the responses of "
             r"neurons along the ventral stream (Part 14) better than models built by hand", GOOD),
            (r"benchmarks now score many networks against many neural and behavioural data sets", MODEL),
            (r"but their errors differ from people's: \ texture over shape, \ and images altered imperceptibly that "
             r"change their answer", AUTH),
            (r"Bowers and colleagues, \ 2023: \ good prediction of neural data is not evidence of the same "
             r"mechanism; \ test them with psychology's controlled experiments", PERSON),
        ], "When does a network explain a brain? First, vision. <bookmark mark='a'/> In 2016 Daniel Yamins and James "
           "DiCarlo showed that networks trained only to recognize objects predict the responses of neurons along "
           "the ventral stream, Part 14's pathway, better than models built by hand. <bookmark mark='b'/> Benchmarks "
           "now score many networks against many neural and behavioural data sets. <bookmark mark='c'/> But their "
           "errors differ from people's. They weigh texture over shape, and images altered imperceptibly can change "
           "their answer. <bookmark mark='d'/> In 2023 Jeffrey Bowers and colleagues argued that predicting neural "
           "data well isn't evidence of the same mechanism, and that networks should be tested with psychology's "
           "controlled experiments.", tag=published_tag(r"Yamins \& DiCarlo (2016)"))

    def language(self):
        rows_section(self, r"Language", [
            (r"Part 23: \ a language model's surprisal predicts reading times and the N400", GOOD),
            (r"Mahowald and colleagues, \ 2024: \ separate formal competence (grammar, \ which models have) from "
             r"functional competence (reasoning, \ knowledge, \ social sense, \ which is uneven)", MODEL),
            (r"the data gap: \ children learn language from orders of magnitude fewer words than models are "
             r"trained on", AUTH),
            (r"so a model can be a good model of what is learnable from text, \ and a poor model of how a child "
             r"learns", YOU),
        ], "Second, language. <bookmark mark='a'/> Part 23 showed that a language model's surprisal predicts reading "
           "times and the N400. <bookmark mark='b'/> Kyle Mahowald and colleagues separate formal competence, "
           "grammar, which models have, from functional competence, reasoning, knowledge and social sense, which is "
           "uneven. <bookmark mark='c'/> And there's a data gap. Children learn language from orders of magnitude "
           "fewer words than models are trained on. <bookmark mark='d'/> So a model can be a good model of what's "
           "learnable from text, and a poor model of how a child learns.")

    def lesson(self):
        chips_section(self, r"Behaviour matched is not mechanism shared", [
            (r"Marr's levels", r"a network can match people at the level of what is computed and differ in how "
                               r"(Part 1)", MODEL),
            (r"error patterns", r"compare which items each gets wrong, \ not overall accuracy", PERSON),
            (r"controlled tests", r"the minimal pairs, \ dissociations and illusions of the previous parts", GOOD),
            (r"the payoff", r"a network that passes them is a candidate theory you can open and lesion, \ which "
                            r"brains rarely allow", YOU),
        ], "So, behaviour matched is not mechanism shared. <bookmark mark='a'/> A network can match people at "
           "Marr's level of what's computed and differ in how it's done, as Part 1 set out. <bookmark mark='b'/> "
           "Compare which items each one gets wrong, not overall accuracy. <bookmark mark='c'/> Use the controlled "
           "tests of the previous parts: minimal pairs, dissociations and illusions. <bookmark mark='d'/> And the "
           "payoff: a network that passes them is a candidate theory you can open and lesion, which brains rarely "
           "allow.")
