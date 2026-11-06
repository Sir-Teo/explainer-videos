from __future__ import annotations

from videos.philosophy.philosophy38.common import *  # noqa: F403


class Community(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Community and role", r"Is justice the first virtue of every society?", lit=(1982, 1983), part=PART)
        with self.voiceover("Chapter ten. Community and role."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.sandel()
        self.walzer()
        self.critique()
        self.confucian()

    def sandel(self):
        head = history_card(1982, r"Michael Sandel", r"\textit{Liberalism and the Limits of Justice}", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"the unencumbered self", r"Rawls's parties choose ends from nowhere: \ but some attachments constitute who we are", COM),
                (r"MacIntyre \ (1981)", r"\textit{After Virtue}: \ justice is intelligible only within a tradition and its practices", HIST),
                (r"Taylor \ (1979)", r"``Atomism'': \ the capacities rights protect develop only within a society", LIB),
                (r"Rawls \ (1993)", r"\textit{Political Liberalism}: \ justice as fairness is political, \ not metaphysical; \ an overlapping consensus among reasonable doctrines", FAIR)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "In 1982 Michael Sandel's Liberalism and the Limits of Justice began the communitarian critique. "
            "<bookmark mark='a'/>Rawls's parties, Sandel argued, are unencumbered selves who choose their ends from "
            "nowhere; but some attachments, to family, community or faith, are not chosen and constitute who we are. "
            "<bookmark mark='b'/>Alasdair MacIntyre's After Virtue, of 1981, held that justice is intelligible only "
            "within a tradition and its practices, and that modern moral argument is the debris of lost ones. "
            "<bookmark mark='c'/>Charles Taylor's essay Atomism argued that the capacities which rights protect "
            "develop only within a society that sustains them. <bookmark mark='d'/>Rawls's Political Liberalism, of "
            "1993, partly conceded: justice as fairness is political, not metaphysical, and aims at an overlapping "
            "consensus among reasonable doctrines that disagree about the good."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def walzer(self):
        head = label(r"Spheres of justice \ (Walzer, \ 1983)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"social meanings", r"goods mean different things in different spheres: \ medicine, \ office, \ love, \ money", COM),
                (r"complex equality", r"no good should convert into dominance over others: \ wealth may not buy office or verdicts", FAIR),
                (r"blocked exchanges", r"votes, \ exemption from military service, \ criminal justice, \ love: \ not for sale", BAD),
                (r"Sandel \ (2012)", r"\textit{What Money Can't Buy}: \ markets crowd out norms \ (the Haifa day-care fines)", MKT)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Michael Walzer's Spheres of Justice, of 1983, gave the critique a positive theory. <bookmark "
            "mark='a'/>Goods mean different things in different spheres, medicine, office, love, money, and each "
            "sphere's meaning fixes its principle of distribution: need, merit, free exchange. <bookmark "
            "mark='b'/>Complex equality forbids converting success in one sphere into dominance in another: wealth "
            "may not buy office, verdicts or grace. <bookmark mark='c'/>Hence blocked exchanges: votes, exemption "
            "from military service, criminal justice, love. <bookmark mark='d'/>Sandel's What Money Can't Buy, of "
            "2012, extended the point with evidence that markets can crowd out norms, as when the Israeli day-care "
            "centres studied by Uri Gneezy and Aldo Rustichini fined parents for lateness, and lateness rose."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def critique(self):
        head = label(r"Who was left out of the contract?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Okin \ (1989)", r"\textit{Justice, \ Gender, \ and the Family}: \ the family is a school of justice, \ and it is unjust", FAIR),
                (r"Pateman \ (1988)", r"\textit{The Sexual Contract}: \ the social contract presupposed a prior contract over women", POW),
                (r"Mills \ (1997)", r"\textit{The Racial Contract}: \ the real contract excluded the non-white from its terms", BAD),
                (r"Young \ (1990)", r"five faces of oppression: \ exploitation, \ marginalization, \ powerlessness, \ cultural imperialism, \ violence", COM)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Others asked who the contract had left out. <bookmark mark='a'/>Susan Moller Okin's Justice, Gender, and "
            "the Family, of 1989, argued that the family, where we first learn justice, distributes work and power "
            "unjustly, and that Rawls's heads of household hid it. <bookmark mark='b'/>Carole Pateman's The Sexual "
            "Contract, of 1988, argued that the social contract presupposed a prior contract over women. <bookmark "
            "mark='c'/>Charles Mills's The Racial Contract, of 1997, argued that the actual contract of modern "
            "European states excluded the non-white from its terms, and that ideal theory hides this. <bookmark "
            "mark='d'/>Iris Marion Young's Justice and the Politics of Difference, of 1990, moved from distribution "
            "to oppression, which has five faces: exploitation, marginalization, powerlessness, cultural imperialism "
            "and violence."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def confucian(self):
        head = label(r"Ritual, \ role and merit", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Xunzi \ (c. \ 250 BCE)", r"desires without limit lead to strife; \ the former kings set up ritual and duty to divide, \ so that goods and desires sustain each other", HIST),
                (r"Mencius", r"the people are most important, \ the state next, \ the ruler least; \ a tyrant may be removed", COM),
                (r"Chan \ (2014)", r"\textit{Confucian Perfectionism}: \ the state may promote the good life, \ moderately", FAIR),
                (r"Bai \ (2019)", r"\textit{Against Political Equality}: \ a hybrid regime, \ votes for all and offices by merit", MKT),
                (r"Bell \ (2015)", r"\textit{The China Model}: \ political meritocracy, \ and its problems of corruption and legitimacy", BAD)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The Confucian tradition approaches justice through ritual and role. <bookmark mark='a'/>Xunzi's chapter "
            "on ritual begins: people are born with desires; if desires are not met they seek, and if seeking has no "
            "measure or limit there is strife. The former kings hated disorder and set up ritual and duty to divide "
            "things, so that goods and desires would sustain each other. <bookmark mark='b'/>Mencius held that the "
            "people are most important, the altars of the state next, and the ruler least, and that killing a tyrant "
            "is not regicide. <bookmark mark='c'/>Joseph Chan's Confucian Perfectionism, of 2014, defends a state "
            "that moderately promotes the good life. <bookmark mark='d'/>Bai Tongdong's Against Political Equality, "
            "of 2019, proposes a hybrid regime: votes for all, and offices partly by merit. <bookmark "
            "mark='e'/>Daniel Bell's The China Model, of 2015, defends political meritocracy and takes seriously its "
            "problems of corruption and legitimacy."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
