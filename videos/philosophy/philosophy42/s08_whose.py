from __future__ import annotations

from videos.philosophy.philosophy42.common import *  # noqa: F403


class Whose(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Whose values?", r"If a machine could have any values, which should it have?", lit=(2004, 2020), part=PART)
        with self.voiceover("Chapter seven. Whose values?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.gabriel()
        self.plural()
        self.practice()
        self.reflect()

    def gabriel(self):
        head = history_card(2020, r"Iason Gabriel", r"``Artificial Intelligence, \ Values, \ and Alignment''", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"aligned with what?", r"instructions, \ intentions, \ revealed preferences, \ informed preferences, \ interests, \ or values", HUMAN),
                (r"the problem", r"people disagree reasonably: \ there is no single set of values to install", RISK),
                (r"fair principles", r"seek principles endorsed despite disagreement: \ overlapping consensus, \ the veil of ignorance \ (Part 38)", TRUEV),
                (r"social choice", r"or aggregate: \ but Arrow's theorem applies \ (Part 39)", PROXYC)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Suppose the technical problems were solved. Whose values would the machine have? <bookmark "
            "mark='a'/>Iason Gabriel distinguished what a system might be aligned with: our instructions, our "
            "intentions, our revealed preferences, our informed preferences, our interests, or our values. They come "
            "apart: what I ask for, what I mean, what I would want if I knew more, and what is good for me are "
            "different things. <bookmark mark='b'/>And people disagree, reasonably, about values. There is no single "
            "correct set to install. <bookmark mark='c'/>Gabriel's proposal is political: seek principles that people "
            "with different values can endorse, as Rawls sought an overlapping consensus, or principles chosen behind "
            "a veil of ignorance, the experiment of Part 38. <bookmark mark='d'/>The alternative is to aggregate, and "
            "Part 39 has shown that every aggregation rule has a price."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def plural(self):
        head = label(r"Many values in one model", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"pluralistic alignment", r"Sorensen et al. \ (2024): \ present the range of reasonable views, \ be steerable among them, \ or match a population's spread", HUMAN),
                (r"collective constitutions", r"about 1,000 Americans drafted principles for a model, \ with Polis \ (2023; \ Part 39)", TRUEV),
                (r"moral uncertainty", r"MacAskill, \ Bykvist and Ord \ (2020): \ act on credences over moral theories \ (Part 35)", PROXYC),
                (r"the moral parliament", r"Bostrom \ (2009); \ Newberry and Ord \ (2021): \ theories as delegates who bargain, \ in proportion to credence", ROBOT)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Several proposals take disagreement seriously. <bookmark mark='a'/>Taylor Sorensen and colleagues "
            "distinguished three kinds of pluralistic alignment: a model that presents the range of reasonable views, "
            "one that can be steered to any of them, and one whose answers match the spread of views in a population. "
            "<bookmark mark='b'/>The collective constitution of Part 39 asked about a thousand Americans to draft a "
            "model's principles together. <bookmark mark='c'/>Within a single model, the problem becomes Part 35's "
            "moral uncertainty: William MacAskill, Krister Bykvist and Toby Ord propose acting on one's credences "
            "over moral theories, which requires comparing their stakes. <bookmark mark='d'/>Nick Bostrom's moral "
            "parliament, developed by Toby Newberry and Ord, seats each theory as a delegate who bargains in "
            "proportion to the credence it has. Each proposal is a social choice rule in disguise, and each pays one "
            "of the prices of Part 39."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def reflect(self):
        head = label(r"Values that change", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"reflective equilibrium", r"Part 37: \ adjust principles and judgments until they fit; \ a process, \ not a list", TRUEV),
                (r"extrapolation", r"Yudkowsky \ (2004): \ what we would want if we knew more, \ thought faster, \ were more the people we wish we were", PROXYC),
                (r"lock-in", r"a powerful system that fixes today's values could prevent the moral progress Part 37 described", RISK),
                (r"constitutions", r"principles written in words and applied by the model: \ rule following again \ (Part 28)", HUMAN)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Values are not fixed. <bookmark mark='a'/>Part 37 described reflective equilibrium: we adjust principles "
            "and judgments against each other until they fit, and the fit keeps changing. Our values are a process, "
            "not a list. <bookmark mark='b'/>Eliezer Yudkowsky proposed aligning a system with our extrapolated "
            "volition: what we would want if we knew more, thought faster, and were more the people we wish we were. "
            "Whose extrapolation, and by what method, is the question. <bookmark mark='c'/>The danger on the other "
            "side is lock-in. A powerful system that fixed today's values could prevent the moral change that "
            "abolished slavery and extended the vote. <bookmark mark='d'/>Written constitutions, principles in words "
            "that a model applies to new cases, are one practical answer, and they bring back Part 28: no finite set "
            "of words fixes how to go on. Somebody, or something, must judge."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def practice(self):
        head = label(r"Choosing principles together, \ in practice", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"behind the veil", r"Weidinger et al. \ (2023): \ people choosing principles for an AI behind a veil of ignorance favoured helping the worst off \ (Part 38)", TRUEV),
                (r"bridging", r"Wojcik et al. \ (2022): \ Community Notes shows a note only if people who usually disagree both rate it helpful", HUMAN),
                (r"democratic inputs", r"2023: \ grants for experiments in deciding model behaviour democratically", PROXYC),
                (r"the open question", r"who participates, \ and who decides how their inputs are combined", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Some of this has been tried. <bookmark mark='a'/>Laura Weidinger and colleagues asked people to choose "
            "principles for an AI assistant from behind a veil of ignorance, not knowing whether they would be "
            "advantaged; they tended to favour principles that help the worst off, as in Part 38. <bookmark "
            "mark='b'/>The Community Notes system, described by Stefan Wojcik and colleagues, shows a fact-checking "
            "note only when people who usually disagree with each other both rate it helpful: an aggregation rule "
            "designed to find bridging consensus rather than a majority. <bookmark mark='c'/>In 2023 one developer "
            "funded experiments in deciding model behaviour democratically. <bookmark mark='d'/>The open questions "
            "are the ones Part 39 asked: who participates, and who decides how their inputs are combined."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
