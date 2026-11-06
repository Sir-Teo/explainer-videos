from __future__ import annotations

from videos.philosophy.philosophy41.common import *  # noqa: F403


class Context(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"What privacy is", r"What does privacy protect, and why?", lit=(2010,), part=PART)
        with self.voiceover("Chapter nine. What privacy is."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.nissenbaum()
        self.census()
        self.philosophy()
        self.memory()
        self.consent()

    def nissenbaum(self):
        head = history_card(2010, r"Helen Nissenbaum", r"\textit{Privacy in Context}", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"contextual integrity", r"information flows carry norms of their context: \ medical, \ friendship, \ commerce", PRIV),
                (r"a violation", r"a flow that breaks its context's norms, \ even of `public' data \ (Nissenbaum, \ 2010)", BAD),
                (r"what DP misses", r"inference about groups: \ a model can learn that you are likely pregnant from others' data", RESP),
                (r"what DP gives", r"a guarantee about you, \ not about what can be learned about people like you", FAIRC)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "What is privacy? Differential privacy answers one precise question. Helen Nissenbaum's Privacy in "
            "Context, of 2010, answers a broader one. <bookmark mark='a'/>Information flows, she argues, carry the "
            "norms of their contexts: medical information flows to doctors, gossip among friends, purchases to "
            "sellers. <bookmark mark='b'/>Privacy is violated when a flow breaks those norms, even if the information "
            "was public. <bookmark mark='c'/>Differential privacy does not stop inferences from patterns in other "
            "people's data: a retailer's model can infer that a customer is likely pregnant from what similar "
            "customers bought. <bookmark mark='d'/>What it guarantees is about you, not about what can be learned "
            "about people like you."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def census(self):
        head = label(r"Privacy in practice", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the 2020 US census", r"the first major release protected by differential privacy, \ with a total budget set by policy", PRIV),
                (r"the controversy", r"small-area counts got noisier; \ demographers and states objected; \ the trade-off became public", BAD),
                (r"industry", r"Google's RAPPOR \ (2014) \ and Apple's local DP use randomized response at scale", FAIRC),
                (r"the choice of $\varepsilon$", r"a value judgment: \ how much accuracy to give up for how much protection", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Differential privacy is now policy. <bookmark mark='a'/>The 2020 United States census was the first "
            "major release protected by it, with a total privacy budget set by officials. <bookmark "
            "mark='b'/>Small-area counts became noisier, demographers and some states objected, and the trade-off "
            "between accuracy and privacy became a public argument. <bookmark mark='c'/>Google's RAPPOR, from 2014, "
            "and Apple's on-device systems use randomized response at scale. <bookmark mark='d'/>The choice of "
            "epsilon is a value judgment, not a technical one: how much accuracy to give up for how much protection."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def philosophy(self):
        head = label(r"Why privacy matters", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Warren and Brandeis \ (1890)", r"`the right to be let alone'", PRIV),
                (r"Rachels \ (1975)", r"privacy lets us maintain different relationships with different people", FAIRC),
                (r"Solove \ (2008)", r"a family of problems: \ surveillance, \ aggregation, \ exclusion, \ exposure", EXPL),
                (r"power", r"Zuboff \ (2019): \ surveillance capitalism; \ information as leverage over behaviour", RESP)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Why does privacy matter at all? <bookmark mark='a'/>Samuel Warren and Louis Brandeis, in 1890, called it "
            "the right to be let alone. <bookmark mark='b'/>James Rachels argued in 1975 that privacy lets us "
            "maintain different kinds of relationship with different people, which would be impossible if everyone "
            "knew everything. <bookmark mark='c'/>Daniel Solove's Understanding Privacy, of 2008, treated it as a "
            "family of problems: surveillance, aggregation, exclusion and exposure. <bookmark mark='d'/>And Shoshana "
            "Zuboff's The Age of Surveillance Capitalism, of 2019, emphasized power: information about behaviour as "
            "leverage over behaviour."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def memory(self):
        head = history_card(2021, r"Carlini et al.", r"``Extracting Training Data from Large Language Models''", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"memorization", r"GPT-2 could be prompted to emit verbatim training text, \ including names, \ phone numbers and addresses", RESP),
                (r"images too", r"Carlini et al. \ (2023): \ diffusion models can regenerate some training images almost exactly", BAD),
                (r"the right to be forgotten", r"\textit{Google Spain} \ (2014); \ GDPR Article 17: \ people may ask for data about them to be erased", EXPL),
                (r"machine unlearning", r"Bourtoule et al. \ (2021): \ train on separate shards, \ so that forgetting one person retrains only one shard", FAIRC)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Large models make privacy concrete again. <bookmark mark='a'/>In 2021 Nicholas Carlini and colleagues "
            "showed that a language model, GPT-2, could be prompted to emit text it had memorized from its training "
            "data, verbatim, including people's names, phone numbers and addresses. <bookmark mark='b'/>Two years "
            "later, Carlini's group showed that image generators can regenerate some of their training images almost "
            "exactly. A model trained on personal data is, in part, a store of it. <bookmark mark='c'/>The law has a "
            "right that now applies to models. In the Google Spain case of 2014, Europe's highest court held that "
            "people can ask search engines to delist information about them, and the General Data Protection "
            "Regulation's Article seventeen gives a right to erasure. <bookmark mark='d'/>But erasing a person from a "
            "trained model is hard. Lucas Bourtoule and colleagues proposed training on separate shards of data, so "
            "that forgetting one person means retraining only one shard. Differential privacy offers the deeper "
            "answer: a model that never depended much on anyone has little to forget."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def consent(self):
        head = label(r"Notice and consent", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"McDonald and Cranor \ (2008)", r"reading every privacy policy one meets would take about 200 hours a year", EXPL),
                (r"Solove \ (2013)", r"`privacy self-management' fails: \ no one can foresee the downstream uses of their data", BAD),
                (r"contextual integrity", r"a click cannot make appropriate a flow that breaks its context's norms", PRIV),
                (r"information fiduciaries", r"Balkin \ (2016): \ those who hold our data owe us duties of care and loyalty, \ like doctors and lawyers", FAIRC)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The usual legal answer to all this is consent: tell people what will happen to their data, and let them "
            "agree. <bookmark mark='a'/>Aleecia McDonald and Lorrie Cranor estimated in 2008 that reading every "
            "privacy policy an American meets online would take about two hundred hours a year. No one does it. "
            "<bookmark mark='b'/>Daniel Solove argued that the problem is deeper than time. Privacy self-management "
            "asks each person to judge uses of their data that no one can foresee, by aggregation with other data, "
            "years later. <bookmark mark='c'/>Contextual integrity explains why consent is not enough: a click on a "
            "box cannot make a flow appropriate when it breaks the norms of the context the data came from. <bookmark "
            "mark='d'/>Jack Balkin proposed another model, borrowed from the professions. Those who hold our data "
            "would be information fiduciaries, owing us duties of care and loyalty, as doctors and lawyers do. The "
            "burden then falls on those with the knowledge, not on the user with a checkbox."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
