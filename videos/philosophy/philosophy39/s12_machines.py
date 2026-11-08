from __future__ import annotations

from videos.philosophy.philosophy39.common import *  # noqa: F403


class Machines(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Deliberation, \ delegation, \ and AI", r"Can talking, \ delegating or machines rescue the will of the people?", lit=(1992, 2023), part=PART)
        with self.voiceover("Chapter eleven. Deliberation, delegation, and AI."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.deliberation()
        self.liquid()
        self.sortition()
        self.bt()
        self.generative()
        self.alignment()

    def deliberation(self):
        head = history_card(1992, r"Jürgen Habermas", r"\textit{Between Facts and Norms}", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"Habermas \ (1992)", r"\textit{Between Facts and Norms}: \ legitimacy comes from public reasoning among equals, \ not from adding up votes", TRUTH),
                (r"deliberative polls", r"Fishkin: \ a random sample deliberates, \ then votes; \ opinions shift, \ and grow more single-peaked", MAJ),
                (r"citizens' assemblies", r"Ireland \ (2016--18): \ 99 randomly chosen citizens on abortion; \ a referendum followed", VOTE),
                (r"Polis and vTaiwan", r"online deliberation that maps opinion clusters and surfaces consensus statements", MACH)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Arrow's theorem treats preferences as given. Deliberative democracy treats them as something to be "
            "formed. <bookmark mark='a'/>Jürgen Habermas's Between Facts and Norms, of 1992, located legitimacy in "
            "public reasoning among equals rather than in the aggregation of votes. <bookmark mark='b'/>James "
            "Fishkin's deliberative polls bring a random sample of citizens together to deliberate before they vote; "
            "their opinions shift, and, as chapter seven noted, grow more single-peaked. <bookmark "
            "mark='c'/>Ireland's Citizens' Assembly of ninety nine randomly chosen citizens deliberated on abortion "
            "from 2016, and a referendum followed in 2018. <bookmark mark='d'/>Tools such as Polis, used in Taiwan's "
            "vTaiwan process, map clusters of opinion online and surface the statements that every cluster supports."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def liquid(self):
        head = label(r"Delegation: \ liquid democracy", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the idea", r"vote yourself on any issue, \ or delegate your vote to someone who can delegate it again \ (Ford, \ 2002)", VOTE),
                (r"in use", r"LiquidFeedback, \ in Germany's Pirate Party", MAJ),
                (r"the risk", r"Kahng, \ Mackenzie and Procaccia \ (2018): \ delegation can concentrate votes and make the majority less likely to be right", BAD),
                (r"the jury theorem again", r"delegation is correlation: \ the opinion leader of chapter nine", CYC)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Another reform changes who votes. <bookmark mark='a'/>In liquid democracy, proposed in this form by "
            "Bryan Ford in 2002, each person may vote on any issue or delegate their vote to someone else, who may "
            "delegate it again. <bookmark mark='b'/>Germany's Pirate Party used a version of it, LiquidFeedback. "
            "<bookmark mark='c'/>Anson Kahng, Simon Mackenzie and Ariel Procaccia showed in 2018 that no local "
            "delegation rule can guarantee better decisions than direct voting: delegation can concentrate votes in a "
            "few hands. <bookmark mark='d'/>In the language of chapter nine, delegation is correlation, and "
            "correlation is what undoes the jury theorem."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def alignment(self):
        head = label(r"Social choice for AI", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Conitzer et al. \ (2024)", r"``Social Choice Should Guide AI Alignment'': \ make the aggregation rule a deliberate choice", MACH),
                (r"Ge et al. \ (2024)", r"the standard reward-fitting rule violates basic axioms of social choice", BAD),
                (r"collective constitutions", r"Anthropic and the Collective Intelligence Project \ (2023): \ about 1,000 Americans drafted principles for a model, \ via Polis", VOTE),
                (r"ahead", r"Part 41: \ fairness criteria that cannot all hold; \ Part 42: \ whose values a machine should have", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Social choice theorists have taken notice. <bookmark mark='a'/>Vincent Conitzer and colleagues argued in "
            "2024 that social choice should guide AI alignment: the aggregation rule should be chosen deliberately, "
            "with its axioms in view. <bookmark mark='b'/>Luise Ge and colleagues showed the same year that the "
            "standard way of fitting reward models violates basic axioms of social choice. <bookmark mark='c'/>In "
            "2023 Anthropic and the Collective Intelligence Project asked about a thousand Americans to draft and "
            "vote on principles for a language model, using Polis. <bookmark mark='d'/>Part 41 turns to fairness "
            "criteria for machines that cannot all hold together, and Part 42 to the question of whose values a "
            "machine should have."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def bt(self):
        d = load("bt")
        assert d["bt_order"] == ["y", "x", "z"] and d["borda_order"] == ["y", "x", "z"] and d["condorcet_winner"] == "x"
        assert d["P"]["xy"] == 0.58 and d["P"]["yz"] == 0.9
        head = label(r"What preference learning aggregates", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        grp = stack([(r"60\% of annotators: \ $x \succ y \succ z$", VOTE), (r"40\%: \ $y \succ z \succ x$", MAJ),
                     (r"each picks her preferred answer 90\% of the time; \ the group is hidden", GREY_A)],
                    font_size=21, buff=0.16).move_to([0, 2.15, 0])
        hd = [r"\text{response}", r"\text{beats } x", r"\text{beats } y", r"\text{beats } z", r"\text{Borda}",
              r"\text{Bradley--Terry}"]
        cells = []
        for a in ("x", "y", "z"):
            row = [label(a, font_size=22, color=ALT[a])]
            for b in ("x", "y", "z"):
                row.append(label(r"--" if a == b else f"{d['P'][a + b]:.2f}", font_size=19,
                                 color=GREY_D if a == b else (MAJ if a != b and d["P"][a + b] > 0.5 else GREY_B)))
            row.append(label(f"{d['borda'][a]:.2f}", font_size=19, color=SCORE))
            row.append(label(f"{d['bt'][a]:+.2f}", font_size=19, color=MACH))
            cells.append(row)
        grid = ValueGrid(hd, cells, col_w=[1.8, 1.6, 1.6, 1.6, 1.6, 2.4], cell_h=0.55, font_size=18).move_to([0, -0.2, 0])
        foot = stack([(r"x beats both others head to head \ (58\%): \ the Condorcet winner", MAJ),
                      (r"the fitted reward ranks y first: \ y, \ x, \ z, \ exactly Borda's order", MACH),
                      (r"Siththaranjan, \ Laidlaw and Hadfield-Menell \ (2023): \ with hidden context, \ fitting a "
                       r"reward model is a Borda count", GOAL)],
                     font_size=20, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Today's language models are tuned on human preferences, and that is social choice in disguise. <bookmark "
            "mark='a'/>Suppose sixty percent of annotators rank three answers x, y, z, and forty percent rank them y, "
            "z, x; each picks her preferred answer ninety percent of the time, and which group an annotator belongs "
            "to is hidden. <bookmark mark='b'/>The table shows how often each answer beats each other. x beats y and "
            "z fifty eight percent of the time: x is the Condorcet winner. <bookmark mark='c'/>Standard training fits "
            "a Bradley-Terry model, a score for each answer, by maximum likelihood. The Reasoner fits it, and the "
            "scores rank y first, then x, then z: exactly the order of the Borda count. <bookmark mark='d'/>Anand "
            "Siththaranjan, Cassidy Laidlaw and Dylan Hadfield-Menell proved in 2023 that this is general: when the "
            "comparisons hide differences between people, fitting a reward model implicitly aggregates them by Borda "
            "count. The choice of aggregation rule was made without anyone deciding it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grp))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for row in grid.cell for c in row[:4]],
                      FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(*[FadeIn(row[4]) for row in grid.cell], *[FadeIn(row[5]) for row in grid.cell], FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def sortition(self):
        head = label(r"Choosing by lot", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Athens", r"most magistrates were chosen by lot, \ with the \textit{kleroterion}: \ election was thought aristocratic", HIST),
                (r"Guerrero \ (2014)", r"lottocracy: \ randomly chosen single-issue legislatures, \ informed by experts", VOTE),
                (r"Landemore \ (2020)", r"\textit{Open Democracy}: \ open mini-publics in place of elected elites", MAJ),
                (r"fair selection", r"Flanigan et al. \ (2021): \ algorithms that select representative panels while giving each volunteer a fair chance", MACH)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "An older device is returning. <bookmark mark='a'/>In classical Athens most magistrates were chosen by "
            "lot, with a stone allotment machine called the kleroterion, and election was regarded as aristocratic. "
            "<bookmark mark='b'/>Alexander Guerrero proposed in 2014 a lottocracy of randomly chosen single-issue "
            "legislatures, informed by experts. <bookmark mark='c'/>Hélène Landemore's Open Democracy, of 2020, "
            "argues for open mini-publics in place of elected elites. <bookmark mark='d'/>And Bailey Flanigan and "
            "colleagues published in Nature, in 2021, algorithms that select citizens' assemblies representative of "
            "the population while giving every volunteer as equal a chance of selection as possible; they are used to "
            "select real assemblies."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def generative(self):
        head = label(r"Language models in collective decisions", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"silicon samples", r"Argyle et al. \ (2023): \ language models can imitate the survey answers of demographic groups, \ imperfectly", MACH),
                (r"generative social choice", r"Fish et al. \ (2024): \ a model drafts statements; \ an algorithm picks a slate that represents every group, \ with guarantees", MAJ),
                (r"mediation", r"Tessler et al. \ (2024): \ an AI mediator wrote group statements that participants preferred to human-written ones", VOTE),
                (r"the worry", r"whoever writes the options, \ or the summaries, \ sets the agenda: \ chapter two's lesson", BAD)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Language models are entering collective decisions themselves. <bookmark mark='a'/>Lisa Argyle and "
            "colleagues found in 2023 that language models can imitate the survey answers of demographic groups, "
            "imperfectly. <bookmark mark='b'/>Sara Fish and colleagues proposed generative social choice in 2024: a "
            "model drafts statements, and an algorithm picks a slate that represents every group, with "
            "proportionality guarantees. <bookmark mark='c'/>Michael Henry Tessler and colleagues reported in 2024 "
            "that an AI mediator wrote group statements that participants preferred to statements by human mediators. "
            "<bookmark mark='d'/>The worry is chapter two's lesson again: whoever writes the options, or the "
            "summaries, sets the agenda."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
