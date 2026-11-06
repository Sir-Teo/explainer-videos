from __future__ import annotations

from videos.philosophy.philosophy41.common import *  # noqa: F403


class Responsibility(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Opacity and responsibility", r"Who answers for a machine's decision?", lit=(2004, 2019), part=PART)
        with self.voiceover("Chapter eleven. Opacity and responsibility."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.opacity()
        self.gaps()
        self.crumple()
        self.accountability()
        self.standards()

    def opacity(self):
        head = history_card(2016, r"Jenna Burrell", r"``How the Machine Thinks''", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"three opacities", r"secrecy, \ technical illiteracy, \ and the scale of the model itself", PRIV),
                (r"reliabilism", r"Durán and Formanek \ (2018): \ trust a process with a verified track record, \ as we trust instruments", FAIRC),
                (r"testimony", r"Part 12: \ we rely on experts we cannot check; \ are models experts?", EXPL),
                (r"the worry", r"track records are measured on yesterday's data; \ the world shifts", BAD)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Can we trust what we cannot understand? <bookmark mark='a'/>Jenna Burrell distinguished in 2016 three "
            "kinds of opacity: corporate secrecy, the public's technical illiteracy, and the sheer scale of the model "
            "itself. <bookmark mark='b'/>Juan Durán and Nico Formanek proposed computational reliabilism in 2018: "
            "trust a process with a verified track record, as we trust instruments we do not understand. <bookmark "
            "mark='c'/>Part 12 asked when we may rely on experts we cannot check; the question now is whether models "
            "are experts. <bookmark mark='d'/>The worry is that track records are measured on yesterday's data, and "
            "the world shifts."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def gaps(self):
        head = label(r"Responsibility gaps", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Matthias \ (2004)", r"learning machines act in ways no one could predict: \ who is responsible?", RESP),
                (r"many hands", r"Thompson \ (1980); \ Nissenbaum \ (1996): \ when many contribute, \ no one seems to blame", EXPL),
                (r"Part 32", r"responsibility needs control and knowledge: \ both are spread thin", FAIRC),
                (r"replies", r"Santoni de Sio and Mecacci \ (2021): \ design for meaningful human control; \ assign responsibility in advance", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "When a machine errs, who is responsible? <bookmark mark='a'/>Andreas Matthias argued in 2004 that "
            "learning machines act in ways their makers could not predict, opening a gap between harm and blame. "
            "<bookmark mark='b'/>Dennis Thompson in 1980, and Helen Nissenbaum in 1996, described the problem of many "
            "hands: when many people each contribute a little, no one seems to blame. <bookmark mark='c'/>Part 32 "
            "found that responsibility needs control and knowledge, and in machine learning both are spread thin. "
            "<bookmark mark='d'/>Filippo Santoni de Sio and Giulio Mecacci replied in 2021 that we must design for "
            "meaningful human control and assign responsibility in advance, before anything goes wrong."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def accountability(self):
        head = label(r"Accountability in practice", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"model cards", r"Mitchell et al. \ (2019): \ a short report on what a model is for, \ and how it performs on each group", FAIRC),
                (r"datasheets", r"Gebru et al. \ (2021): \ where the data came from, \ who is in it, \ and what it should not be used for", EXPL),
                (r"audits", r"Raji and Buolamwini \ (2019): \ external audits changed vendors' behaviour", PRIV),
                (r"incidents", r"the AI Incident Database \ (2020): \ failures recorded, \ as aviation records near-misses", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Institutions have begun to respond. <bookmark mark='a'/>Margaret Mitchell and colleagues proposed model "
            "cards in 2019: a short report on what a model is for and how it performs on each group. <bookmark "
            "mark='b'/>Timnit Gebru and colleagues proposed datasheets for datasets: where the data came from, who is "
            "in it, and what it should not be used for. <bookmark mark='c'/>Inioluwa Deborah Raji and Joy Buolamwini "
            "showed in 2019 that public external audits changed vendors' behaviour. <bookmark mark='d'/>And the AI "
            "Incident Database, begun in 2020, records failures as aviation records near-misses, so that others can "
            "learn from them."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def crumple(self):
        head = history_card(2019, r"Madeleine Clare Elish", r"``Moral Crumple Zones''", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"the crumple zone", r"in a complex automated system, \ blame collapses onto the nearest human operator", RESP),
                (r"Tempe \ (2018)", r"a self-driving test car killed a pedestrian; \ the safety driver was charged, \ the company was not", BAD),
                (r"automation bias", r"Skitka, \ Mosier and Burdick \ (1999): \ people follow automated advice, \ even when it is wrong", EXPL),
                (r"Green and Chen \ (2019)", r"`Disparate Interactions': \ in an experiment, \ people used the same risk scores differently for Black and white defendants", FAIRC)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "A common answer to responsibility gaps is to keep a human in the loop. <bookmark mark='a'/>Madeleine "
            "Clare Elish warned that the human can become a moral crumple zone. In a car, the crumple zone absorbs "
            "the force of a crash; in a complex automated system, blame collapses onto the nearest human operator, "
            "who had the least control over its design. <bookmark mark='b'/>In 2018 in Tempe, Arizona, a self-driving "
            "test car killed a pedestrian. The safety driver was charged; the company was not. <bookmark "
            "mark='c'/>And the human in the loop is not independent. Linda Skitka and colleagues documented "
            "automation bias: people follow automated advice, even when it is wrong and they have evidence it is "
            "wrong. <bookmark mark='d'/>Ben Green and Yiling Chen gave people pretrial risk scores in an experiment. "
            "The scores did not make their predictions much better, and people deviated from them differently for "
            "Black and for white defendants. A human in the loop can add a bias as well as remove one."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def standards(self):
        head = label(r"Governance, \ in practice", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"NIST \ (2023)", r"the AI Risk Management Framework: \ govern, \ map, \ measure, \ manage", EXPL),
                (r"ISO/IEC 42001 \ (2023)", r"a certifiable management-system standard for organizations that build or use AI", PRIV),
                (r"impact assessments", r"Canada's Directive on Automated Decision-Making \ (2019): \ assess a system's impact before government deploys it", FAIRC),
                (r"the limit", r"process standards ask whether you checked, \ not whether the outcome is just: \ the philosophy is still needed", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Accountability is now being written into standards. <bookmark mark='a'/>The United States National "
            "Institute of Standards and Technology published its AI Risk Management Framework in 2023, organized "
            "around four functions: govern, map, measure and manage. <bookmark mark='b'/>The same year, ISO and the "
            "IEC published 42001, a management-system standard that an organization building or using AI can be "
            "certified against, as it can for quality or information security. <bookmark mark='c'/>Canada's Directive "
            "on Automated Decision-Making, from 2019, requires government departments to assess a system's impact "
            "before deploying it, with more review for higher impact. <bookmark mark='d'/>These are real gains: they "
            "make someone responsible for asking the questions of this part. But a process standard asks whether you "
            "checked, not whether the result is just. Which error rates to equalize, how much privacy to buy, which "
            "explanation is owed: the standards leave these to judgment, and that judgment is philosophy."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
