from __future__ import annotations

from videos.psychology.psych61.common import *  # noqa: F403


class Who(VoiceoverScene):
    def construct(self):
        card_section(self, 5, r"Who is sampled", r"A decade after WEIRD, \ who does psychology study?",
                     scale=("society",))
        self.weird()
        self.english()
        self.cog()

    def weird(self):
        rows_section(self, r"A decade after WEIRD", [
            (r"Part 38: \ Henrich, \ Heine and Norenzayan, \ 2010: \ most participants are Western, \ educated, \ "
             r"industrialized, \ rich and democratic", WHITE),
            (r"Thalmayer, \ Toscanelli and Arnett, \ 2021: \ in leading journals, \ samples from the United States "
             r"and Europe still made up the great majority; \ authors even more so", AUTH),
            (r"the cost: \ Part 38's illusions and fairness games varied across societies", MODEL),
            (r"the remedies: \ global networks, \ funding for local labs, \ and reporting who was sampled in every "
             r"paper's abstract", GOOD),
        ], "A decade after WEIRD, who does psychology study? <bookmark mark='a'/> In Part 38, Joseph Henrich, Steven "
           "Heine and Ara Norenzayan showed that most participants are Western, educated, industrialized, rich and "
           "democratic. <bookmark mark='b'/> In 2021 Amber Gayle Thalmayer, Cecilia Toscanelli and Jeffrey Arnett found "
           "that in leading journals, samples from the United States and Europe still made up the great majority, "
           "and authors even more so. <bookmark mark='c'/> The cost was Part 38's: illusions and fairness games "
           "varied across societies. <bookmark mark='d'/> The remedies are global networks, funding for local labs, "
           "and reporting who was sampled in every paper's abstract.",
           tag=published_tag(r"Thalmayer, \ Toscanelli \& Arnett (2021)"))

    def english(self):
        rows_section(self, r"English as the default", [
            (r"Blasi and colleagues, \ 2022: \ most of cognitive science's work on language and thought uses English "
             r"speakers", WHITE),
            (r"English is unusual: \ its spelling, \ its fixed word order, \ its few grammatical markers", MODEL),
            (r"claims about reading (Part 23), \ memory for words and categories rest on that one language", AUTH),
            (r"the test: \ does the finding hold in languages unlike English? \ often it has never been asked", YOU),
        ], "There's a second default: English. <bookmark mark='a'/> In 2022 Damian Blasi and colleagues showed that "
           "most of cognitive science's work on language and thought uses English speakers. <bookmark mark='b'/> "
           "English is unusual: its spelling, its fixed word order, its few grammatical markers. <bookmark mark='c'/> "
           "Claims about reading, Part 23's subject, and about memory for words and categories rest on that one "
           "language. <bookmark mark='d'/> The test is whether a finding holds in languages unlike English, and often "
           "it has never been asked.", tag=published_tag(r"Blasi et al.\ (2022)"))

    def cog(self):
        rows_section(self, r"Say whom the finding is about", [
            (r"Simons, \ Shoda and Lindsay, \ 2017: \ end every paper with a statement of the constraints on "
             r"generality: \ which people, \ stimuli, \ procedures and settings the authors expect the result to "
             r"hold for, \ and why", WHITE),
            (r"a claim about ``people'' from 120 undergraduates in one city becomes a claim about them, \ unless "
             r"the authors argue further", MODEL),
            (r"it turns unstated generality into a testable prediction: \ a replication outside the stated range is "
             r"a test, \ not a failure", GOOD),
            (r"and it makes sampling a design decision: \ to claim more, \ sample more widely, \ as the many-labs "
             r"projects did", YOU),
        ], "One remedy is to say whom the finding is about. <bookmark mark='a'/> In 2017 Daniel Simons, Yuichi Shoda "
           "and Stephen Lindsay proposed that every paper end with a statement of the constraints on generality: "
           "which people, stimuli, procedures and settings the authors expect the result to hold for, and why. "
           "<bookmark mark='b'/> A claim about people from a hundred and twenty undergraduates in one city becomes a "
           "claim about them, unless the authors argue further. <bookmark mark='c'/> It turns unstated generality "
           "into a testable prediction. A replication outside the stated range is a test, not a failure. "
           "<bookmark mark='d'/> And it makes sampling a design decision. To claim more, sample more widely, as the "
           "many-labs projects did.")
