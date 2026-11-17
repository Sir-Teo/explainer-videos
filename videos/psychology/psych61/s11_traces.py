from __future__ import annotations

from videos.psychology.psych61.common import *  # noqa: F403


class Traces(VoiceoverScene):
    def construct(self):
        card_section(self, 10, r"Digital traces", r"Can language online measure a population's health?",
                     scale=("society",))
        self.twitter()
        self.ecological()
        self.lessons()

    def twitter(self):
        rows_section(self, r"Tweets and the heart", [
            (r"Eichstaedt and colleagues, \ 2015: \ the language of tweets from US counties predicted deaths from "
             r"heart disease better than a model of demographic and health factors", WHITE),
            (r"angry and hostile words went with more deaths; \ words of engagement and optimism with fewer", MODEL),
            (r"Brown and Coyne, \ 2018: \ the tweeters were not the people who died; \ results changed with the "
             r"counties included and the analysis chosen", AUTH),
            (r"Part 47's warning: \ a county-level association says little about individuals", PERSON),
        ], "Can language online measure a population's health? <bookmark mark='a'/> In 2015 Johannes Eichstaedt and "
           "colleagues reported that the language of tweets from American counties predicted deaths from heart "
           "disease better than a model of demographic and health factors. <bookmark mark='b'/> Angry and hostile "
           "words went with more deaths, and words of engagement and optimism with fewer. <bookmark mark='c'/> In "
           "2018 Nicholas Brown and James Coyne pointed out that the people tweeting were not the people who died, "
           "and that results changed with the counties included and the analysis chosen. <bookmark mark='d'/> It's "
           "Part 47's warning: a county-level association says little about individuals.",
           tag=published_tag(r"Eichstaedt et al.\ (2015)"))

    def lessons(self):
        chips_section(self, r"What digital traces need", [
            (r"validity", r"a word count is not a feeling: \ check the measure against people (Part 3)", MODEL),
            (r"the right level", r"population claims from population data; \ individual claims need individuals",
             PERSON),
            (r"held-out tests", r"prediction scored on regions or people not used to build the model", GOOD),
            (r"consent and harm", r"traces were not given for research; \ inferring health or traits can harm the "
                                  r"people inferred about", AUTH),
        ], "What do digital traces need? <bookmark mark='a'/> Validity: a word count is not a feeling, so check the "
           "measure against people, as in Part 3. <bookmark mark='b'/> The right level: population claims from "
           "population data, and individual claims need individuals. <bookmark mark='c'/> Held-out tests: "
           "prediction scored on regions or people not used to build the model. <bookmark mark='d'/> And consent and "
           "harm: traces weren't given for research, and inferring health or traits can harm the people inferred "
           "about.")

    def ecological(self):
        d = load("ecological")
        head = heading(r"Counties are not people")
        lo, hi = float(min(d["cx"].min(), d["cy"].min())), float(max(d["cx"].max(), d["cy"].max()))
        A = axes([lo - 0.2, hi + 0.2], [lo - 0.2, hi + 0.2], x_length=4.2, y_length=3.4, xticks=None, yticks=None,
                 xlabel=r"county: \ hostile words (mean)", ylabel=r"county: \ heart disease (mean)",
                 center=[-3.6, 0.2, 0], font_size=12)
        pts = scatter(A.ax, d["cx"], d["cy"], AUTH, radius=0.035)
        rows = rows_of([
            (r"Psyche: \ 3{,}000 counties of 1{,}000 people; \ a county's income lowers both its people's hostile "
             r"posting and their heart risk", WHITE),
            (rf"across counties, \ language and heart disease correlate {d['county_r']:.2f}", AUTH),
            (rf"across people, \ {d['person_r']:.2f}; \ within a county, \ {abs(d['within_r']):.2f}: \ a person's words "
             r"say nothing about their own heart", MODEL),
            (r"the county correlation is real and can still be useful for mapping; \ reading it as a fact about "
             r"individuals is the ecological fallacy", GOOD),
            (r"so a trace study must say at which level its claim lives, \ and what else differs between the units", YOU),
        ], 6.4, 18, 0.32).move_to([3.2, -0.2, 0])
        tag = psyche_tag(r"simulated counties, \ truth known")
        with self.voiceover(
            "Here's the trap in that study's design, simulated. <bookmark mark='a'/> Psyche has three thousand "
            "counties of a thousand people. A county's income lowers both its people's hostile posting and their "
            "heart risk. <bookmark mark='b'/> Across counties, language and heart disease correlate about zero point "
            "six. <bookmark mark='c'/> Across people, about zero point zero six, and within a county, zero. A person's "
            "words say nothing about their own heart. <bookmark mark='d'/> The county correlation is real, and can "
            "still be useful for mapping. Reading it as a fact about individuals is the ecological fallacy. "
            "<bookmark mark='e'/> So a trace study has to say at which level its claim lives, and what else differs "
            "between the units."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.002), run_time=2)
            for m, r in zip("cde", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
