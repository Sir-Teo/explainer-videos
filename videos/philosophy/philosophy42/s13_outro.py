from __future__ import annotations

from videos.philosophy.philosophy42.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.reading()
        self.references()
        self.farewell()

    def recap(self):
        g, q, o = load("goodhart"), load("quantilize"), load("offswitch")
        p, lob = load("power"), load("lob")
        items = [
            rf"Goodhart: \ {g['light']['true'][-1]:.2f} with Gaussian error; \ peak {g['heavy']['peak']:.2f}, \ then "
            rf"{abs(g['heavy']['last']):.2f}, \ with heavy tails",
            rf"a quantilizer: \ the top quarter {q['best_true']:.2f}, \ the argmax {q['rows'][0]['true']:.2f}",
            r"specification gaming: \ boats, \ blocks, \ Tetris, \ sycophancy, \ tests",
            r"no free lunch for preferences: \ four planners, \ one behaviour \ (the Wall)",
            rf"the off switch: \ wait {o['example']['wait']:.2f} against act {o['example']['act']:.2f}; \ a noisy "
            rf"human, \ {o['example_noisy']['wait']:.2f}",
            rf"power: \ {p['to_hub'] * 100:.0f}\% avoid shutdown; \ $k/(k+1)$",
            r"Löb: \ " + r", \ ".join(str(r["lob_valid"]) for r in lob["rows"]) + r" frames; \ FairBot cooperates "
            r"with FairBot",
            r"whose values; \ honesty; \ moral status; \ the Wall complete; \ calculemus",
        ]
        card = objectives_card(items, title=r"What we built", font_size=22)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Goodhart's law, computed: with Gaussian error more "
            "pressure helps; with heavy tails the true value peaks and falls back to nothing. <bookmark "
            "mark='b'/>A quantilizer that keeps most of the real gain. <bookmark mark='c'/>A catalogue of "
            "specification gaming, from boats to language models. <bookmark mark='d'/>The no-free-lunch theorem for "
            "preferences, the first half of the last brick in the Wall. <bookmark mark='e'/>The off-switch game, "
            "solved: uncertainty makes a robot defer, and a noisy human undoes it. <bookmark mark='f'/>Power-seeking, "
            "counted. <bookmark mark='g'/>Löb's axiom checked on every small frame, and proof-based agents that "
            "cooperate. <bookmark mark='h'/>And whose values, honesty, moral status, the Wall complete, and Leibniz "
            "again."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, \ complete", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{alignment.goodhart, quantilize}", r"proxies under pressure"),
                (r"\texttt{alignment.no\_free\_lunch}", r"behaviour does not fix values"),
                (r"\texttt{alignment.off\_switch}", r"the incentive to defer"),
                (r"\texttt{alignment.power\_seeking}", r"options and POWER on a small MDP"),
                (r"\texttt{alignment.lob\_frames}", r"Löb's axiom on every small frame"),
                (r"\texttt{alignment.modal\_combat}", r"proof-based agents"),
                (r"\texttt{prop}, \ \texttt{modal}, \ \dots, \ \texttt{fairness}", r"Parts 1--41")]
        lefts = [label(a, font_size=20, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=20, color=GREY_A) for _, b in mods]
        x0, y0 = -6.4, head.get_bottom()[1] - 0.6
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.55
            if a.width > 7.4:
                a.width = 7.4
            a.move_to([x0 + a.width / 2, y, 0])
            if b.width > 4.6:
                b.width = 4.6
            b.move_to([1.6 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_alignment.py}", font_size=22,
                      color=GREY_B).to_corner(DL, buff=0.4)
        w = wall(upto=42, current=42).scale(0.36).to_corner(DR, buff=0.3)
        with self.voiceover(
            "The Reasoner's last module is alignment. <bookmark mark='a'/>It puts proxies under pressure, shows that "
            "behaviour does not fix values, solves the off-switch game, counts power on a small world, checks Löb's "
            "axiom on every small frame, and plays proof-based agents against each other. <bookmark mark='b'/>And "
            "the Wall is complete, with forty two bricks."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[42], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"With Gaussian $V$ and $E$ of equal variance, \ show that $\mathbb{E}[V \mid U] = U/2$.",
            r"For $u \sim N(\mu, \sigma^2)$, \ show that $\mathbb{E}[\max(u, 0)] \ge \max(\mu, 0)$, \ with equality "
            r"only if $\sigma = 0$.",
            r"Give two planner--reward pairs that explain a person who always picks the cheaper of two items.",
            r"Why does the share of reward functions that avoid shutdown approach $k/(k+1)$?",
            r"Use Löb's theorem to show that FairBot cooperates with FairBot.",
            r"Show that Löb's axiom fails on a single world that sees itself.",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Why the Gaussian proxy "
            "overstates by half; why waiting is never worse with a rational human; two explanations of a frugal "
            "shopper; the arithmetic of power; FairBot's handshake; and Löb's axiom on a world that sees itself. "
            "Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def reading(self):
        card = objectives_card([
            r"logic: \ Enderton, \textit{A Mathematical Introduction to Logic}; \ Boolos, \ Burgess and Jeffrey, "
            r"\textit{Computability and Logic}",
            r"knowledge and probability: \ Williamson, \textit{Knowledge and Its Limits}; \ Hacking, \textit{An "
            r"Introduction to Probability and Inductive Logic}",
            r"science and causation: \ Godfrey-Smith, \textit{Theory and Reality}; \ Pearl, \textit{Causality}",
            r"metaphysics and mind: \ Sider, \textit{Writing the Book of the World}; \ Chalmers, \textit{The "
            r"Conscious Mind}",
            r"ethics and justice: \ Kagan, \textit{Normative Ethics}; \ Kymlicka, \textit{Contemporary Political "
            r"Philosophy}",
            r"choice: \ Peterson, \textit{An Introduction to Decision Theory}; \ Sen, \textit{Collective Choice and "
            r"Social Welfare}",
            r"alignment: \ Russell, \textit{Human Compatible}; \ Christian, \textit{The Alignment Problem}",
            r"and the beginning: \ Leibniz, \textit{Philosophical Papers and Letters} \ (ed.\ Loemker)",
        ], title=r"What to read next", font_size=20)
        with self.voiceover(
            "Where to go from here. <bookmark mark='a'/>For logic, Enderton, and Boolos, Burgess and Jeffrey. "
            "<bookmark mark='b'/>For knowledge and probability, Williamson and Hacking. <bookmark mark='c'/>For "
            "science and causation, Godfrey-Smith and Pearl. <bookmark mark='d'/>For metaphysics and mind, Sider and "
            "Chalmers. <bookmark mark='e'/>For ethics and justice, Kagan and Kymlicka. <bookmark mark='f'/>For "
            "choice, Peterson and Sen. <bookmark mark='g'/>For alignment, Russell and Brian Christian. <bookmark "
            "mark='h'/>And for the beginning of it all, Leibniz himself."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Russell, \textit{Human Compatible} (2019); \ Christian, \textit{The Alignment Problem} (2020)",
             r"Gabriel, `Artificial Intelligence, Values, and Alignment' (2020)",
             r"Hadfield-Menell et al., `The Off-Switch Game' (2017); \ Turner et al. (2021)",
             r"Armstrong and Mindermann (2018); \ Demski and Garrabrant, \textit{Embedded Agency} (2019)"],
            [r"Löb 1955; Wiener 1960; Goodhart 1975; Campbell 1976; Solovay 1976; Strathern 1997; Ng and Russell 2000",
             r"Yudkowsky 2004; Omohundro 2008; Bostrom 2012, 2014; Yudkowsky and Herreshoff 2013; Barasz et al. 2014",
             r"Soares et al. 2015; Amodei et al. 2016; Hadfield-Menell et al. 2016; Garrabrant et al. 2016; Taylor 2016",
             r"Christiano et al. 2017; Carey 2018; Manheim and Garrabrant 2018; Critch 2019; Hadfield-Menell and Hadfield 2019",
             r"Krakovna et al. 2020; Lehman et al. 2020; Evans et al. 2021; Lin, Hilton and Evans 2021; Christiano, Cotra and Xu 2021",
             r"Bai et al. 2022; Burns et al. 2022; Ouyang et al. 2022; Perez et al. 2022; Turner and Tadepalli 2022",
             r"Butlin, Long et al. 2023; Gao, Schulman and Hilton 2023; Marks and Tegmark 2023; Scheurer et al. 2023",
             r"Sharma et al. 2023; Turpin et al. 2023; Birch 2024; Denison et al. 2024; Greenblatt et al. 2024",
             r"Hubinger et al. 2024; Kwa et al. 2024; Long, Sebo et al. 2024; Sorensen et al. 2024; Baker et al. 2025"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()

    def farewell(self):
        w = wall(upto=42).scale(0.5).move_to([0, 1.2, 0])
        cal = label(r"\textit{calculemus}", font_size=60, color=GOAL).next_to(w, DOWN, buff=0.5)
        thanks = label(r"Thank you for watching \textit{Philosophy, Built}", font_size=28, color=GREY_A).next_to(
            cal, DOWN, buff=0.35)
        with self.voiceover(
            "Forty two parts ago, the series promised to take Leibniz's dream literally, and see how far calculation "
            "could carry philosophy. It carried us further than he could have hoped, and it stopped, every time, at a "
            "wall that showed us exactly where thinking must take over. <bookmark mark='a'/>Let us calculate. And "
            "then, let us judge. <bookmark mark='b'/>Thank you for watching Philosophy, Built."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(FadeIn(cal, scale=1.2))
            vo.wait_until("b")
            self.play(FadeIn(thanks))
            self.wait(2)
        self.clear_scene()
