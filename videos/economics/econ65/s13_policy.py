from __future__ import annotations

from videos.economics.econ65.common import *  # noqa: F403


class Policy(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Policy", r"What can governments do about AI and work, \ and what is a value judgment?",
             "Chapter eleven. Policy.", lit={2022: "Guerreiro, Rebelo and Teles"}, scale=("nation",),
             horizon=("a decade",))
        self.called()
        self.robot_tax()
        self.levers()
        self.is_ought()

    def called(self):
        F = load("frey")
        c = calls.CALLS["frey_osborne_2013"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=18)
        cc.move_to(UP * 0.5)
        lesson = label(r"technically automatable is not automated: \ adoption, \ cost and new tasks decide",
                       font_size=21, color=E.ACCENT).next_to(cc, DOWN, buff=0.5)
        tag = data_tag(rf"BLS via FRED: \ PAYEMS \ (retrieved {F['retrieved']})", corner=DL, font_size=12)
        with self.voiceover(
            "Policy begins with fear, and fear begins with forecasts. Called it? <bookmark mark='a'/> In 2013 "
            "Carl Benedikt Frey and Michael Osborne classified seven hundred and two occupations by how easily "
            "their tasks could be computerised, and concluded that about forty-seven percent of American "
            "employment was at high risk, perhaps over a decade or two. It became one of the most cited numbers "
            "of the decade. <bookmark mark='b'/> Since September 2013, American payroll employment has risen by "
            f"about {100 * F['growth']:.0f} percent. But the paper rated what was technically possible, not what "
            "would be adopted or when, and its second decade is not over. <bookmark mark='c'/> Too early to say. "
            "<bookmark mark='d'/> The lesson of the task model holds: technically automatable is not automated. "
            "Cost, adoption and new tasks decide."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1][0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cc.left))
            vo.wait_until("b")
            self.play(FadeIn(cc.right))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.4))
            vo.wait_until("d")
            self.play(FadeIn(lesson))
        self.clear_scene()

    def robot_tax(self):
        ax = plane([0, 60], [0, 1], center=LEFT * 2.0 + DOWN * 0.4, x_length=7.6, y_length=4.2,
                   xticks=[0, 20, 40, 60], yticks=[], xlabel=r"years after automation arrives",
                   ylabel=r"the optimal tax on robots", xfmt=lambda v: f"{v:.0f}", font_size=14)
        xs = np.linspace(0, 60, 121)
        ys = np.where(xs < 40, 0.8 * (1 - xs / 40) ** 1.5, 0.0)
        tl = path(ax, xs, ys, MACH, 3.4)
        ret = vline(ax, 40, 0, 1, GREY_C)
        rlab = label(r"the last of today's \\ routine workers retire", font_size=15, color=GREY_B).next_to(
            ax.ax.c2p(40, 0.85), RIGHT, buff=0.1)
        side = VGroup(
            label(r"why tax robots at all?", font_size=20, color=E.ACCENT),
            label(r"not for revenue: \ automation raises output \\ and tax receipts", font_size=17, color=GREY_A),
            label(r"to raise the wages of workers \\ who are too far into their careers \\ to retrain", font_size=17,
                  color=WORK),
            label(r"a modest tax, \ falling to zero", font_size=17, color=MACH),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(ax.ax, RIGHT, buff=0.4)
        tag = published_tag(r"Guerreiro, \ Rebelo and Teles, \ Review of Economic Studies 89(1) (2022); \ the "
                            r"curve's shape only", corner=DL, font_size=12)
        with self.voiceover(
            "Should robots be taxed? Bill Gates suggested it in 2017, to replace the income tax lost when robots "
            "replace workers. <bookmark mark='a'/> Joao Guerreiro, Sergio Rebelo and Pedro Teles worked it out in "
            "a model with routine and non-routine workers. Automation does not shrink the tax base, they found; it "
            "raises output and revenue. <bookmark mark='b'/> The reason to tax robots is different: workers already "
            "in routine occupations, too far into their careers to retrain, lose; and a tax on robots raises their "
            "wages, which an income tax cannot target. <bookmark mark='c'/> So the optimal tax is modest, and "
            "falls to zero once the current generation of routine workers has retired. The curve here shows only "
            "its shape. The case is about distribution, and it is temporary."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[:2]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), Create(tl), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(ret), FadeIn(rlab), FadeIn(side[3]))
        self.clear_scene()

    def levers(self):
        cards = point_cards([
            (r"insure the losers", r"unemployment insurance, \ wage insurance, \ retraining: \ Part 42's tools, "
             r"\ sized for displacement that may come faster", WORK),
            (r"share the capital", r"if income moves to capital, \ who owns it matters: \ pensions, \ broad "
             r"ownership, \ the tax on capital \ (Parts 40 and 41)", GDP),
            (r"keep markets open", r"compute, \ data and customers as Part 44's bottlenecks: \ merger review, \ "
             r"interoperability, \ open models", MACH),
            (r"steer the technology", r"tax codes that favour machines over people, \ and research that could "
             r"aim at helping workers rather than replacing them", NEWT),
            (r"educate", r"the race between education and technology \ (Part 39): \ skills that complement the "
             r"machines", IDEA),
            (r"measure", r"usage, \ adoption and displacement, \ in time to act: \ the statistics lag", TEXT),
        ], width=12.6, cols=3, font_size=18).move_to(DOWN * 0.2)
        head = label(r"the levers", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Acemoglu, \ Manera and Restrepo, \ \emph{Does the US Tax Code Favor Automation?}, \ "
                            r"Brookings (2020); \ Acemoglu and Johnson, \ \emph{Power and Progress} (2023)",
                            corner=DL, font_size=12)
        with self.voiceover(
            "Beyond robot taxes, six levers. <bookmark mark='a'/> Insure the people who lose, with the tools of "
            "Part forty-two, sized for a displacement that may come faster than past ones. <bookmark mark='b'/> If "
            "income moves from work to capital, who owns the capital matters: pensions, broad ownership, the taxes "
            "of Parts forty and forty-one. <bookmark mark='c'/> Keep the markets of chapter ten open. <bookmark "
            "mark='d'/> Steer the technology: Daron Acemoglu, Andrea Manera and Pascual Restrepo argue that the "
            "American tax code taxes labour much more heavily than equipment and software, which tilts firms "
            "towards automating; and Acemoglu and Simon Johnson argue that research could aim at helping workers "
            "rather than replacing them. <bookmark mark='e'/> Educate for the tasks that complement machines, the "
            "race of Part thirty-nine. <bookmark mark='f'/> And measure: the statistics will lag the change."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcdef", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def is_ought(self):
        io = is_ought_card(r"AI that automates tasks can raise output while lowering some workers' wages and labour's "
                           r"share; policies can move income from the winners to the losers, at some cost.",
                           r"Governments should slow automation, or tax it, or let it run and compensate.",
                           r"How much a loss to displaced workers weighs against gains to everyone else; whether "
                           r"work has a value beyond its pay; and how much faster growth is worth against a fairer "
                           r"share of it.", width=12.0, font_size=22).move_to(UP * 0.1)
        tag = published_tag(r"Part 18", corner=DL, font_size=12)
        with self.voiceover(
            "And here, as always, the line between what economics can show and what it cannot. <bookmark "
            "mark='a'/> Economics can show that automation can raise output while lowering some workers' wages "
            "and labour's share, and that policy can move income from winners to losers, at some cost. <bookmark "
            "mark='b'/> Whether to slow automation, tax it, or let it run and compensate, needs value judgments: how "
            "much a displaced worker's loss weighs against everyone else's gain; whether work matters beyond its "
            "pay; how much faster growth is worth against a fairer share of it. <bookmark mark='c'/> Those are "
            "yours to make. The models tell you what each choice costs."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(io.card))
            vo.wait_until("a")
            self.play(FadeIn(io.is_row))
            vo.wait_until("b")
            self.play(FadeIn(io.judgment), FadeIn(io.ought))
            vo.wait_until("c")
            self.play(Indicate(io.judgment, color=E.OUGHT, scale_factor=1.02))
        self.clear_scene()
