from __future__ import annotations

from videos.philosophy.philosophy38.common import *  # noqa: F403


class Global(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Justice beyond borders", r"Do we owe strangers abroad what we owe fellow citizens?", lit=(1979, 2002), part=PART)
        with self.voiceover("Chapter eleven. Justice beyond borders."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.cosmo()
        self.statism()
        self.borders()
        self.ai()

    def cosmo(self):
        head = history_card(2002, r"Thomas Pogge", r"\textit{World Poverty and Human Rights}", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"the arbitrariness of birthplace", r"if natural talents are morally arbitrary, \ so is the country one is born in", WORLD),
                (r"Beitz \ (1979)", r"\textit{Political Theory and International Relations}: \ a global original position", FAIR),
                (r"Pogge \ (2002)", r"\textit{World Poverty and Human Rights}: \ a negative duty not to impose an unjust global order", BAD),
                (r"privileges", r"the international resource and borrowing privileges: \ whoever holds power may sell a country's oil and borrow in its name", POW)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Rawls's argument travels further than he wanted. <bookmark mark='a'/>If natural talents are arbitrary "
            "from the moral point of view, so, surely, is the country one happens to be born in, which, by "
            "Branko Milanović's estimate, accounts for more than half of the variation in income across the world's "
            "people. <bookmark mark='b'/>Charles Beitz, in 1979, proposed a global "
            "original position, whose parties do not know their nationality. <bookmark mark='c'/>Thomas Pogge's World "
            "Poverty and Human Rights, of 2002, argued that the rich are not merely failing to help: they violate a "
            "negative duty, by imposing a global order that foreseeably reproduces poverty. <bookmark mark='d'/>His "
            "examples are the international resource and borrowing privileges: whoever holds power in a country, "
            "however they got it, may sell its oil and borrow in its name."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def statism(self):
        head = label(r"Does justice stop at the border?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Rawls \ (1999)", r"\textit{The Law of Peoples}: \ eight principles among peoples, \ and a duty of assistance to burdened societies", FAIR),
                (r"Nagel \ (2005)", r"``The Problem of Global Justice'': \ justice is owed only among those who share a sovereign", LIB),
                (r"Blake \ (2001)", r"coercion by a shared state triggers egalitarian justice", POW),
                (r"Cohen--Sabel \ (2006)", r"``Extra rempublicam nulla justitia?'': \ global institutions already create such ties", WORLD)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The statist reply. <bookmark mark='a'/>Rawls's The Law of Peoples, of 1999, offered eight principles "
            "among peoples, including human rights and a duty of assistance to burdened societies, but no global "
            "difference principle. <bookmark mark='b'/>Thomas Nagel's The Problem of Global Justice, of 2005, argued "
            "that justice, as opposed to humanitarian duty, is owed only among those who are jointly subject to a "
            "sovereign and in whose name it acts. <bookmark mark='c'/>Michael Blake located the trigger in coercion "
            "by a shared state. <bookmark mark='d'/>Joshua Cohen and Charles Sabel replied, under the title No "
            "Justice Outside the Republic?, that global institutions, from trade law to the World Health "
            "Organization, already create the kind of ties that matter."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def borders(self):
        head = label(r"Borders and generations", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Carens \ (1987)", r"``Aliens and Citizens'': \ citizenship in a rich country is like feudal privilege; \ borders should be open", WORLD),
                (r"Walzer; \ Wellman \ (2008)", r"communities may decide their own membership, \ as clubs and families do", COM),
                (r"Rawls's just savings", r"each generation saves for the next what it would have wished its predecessors to save", FAIR),
                (r"climate", r"Shue \ (1993): \ subsistence and luxury emissions; \ Gardiner \ (2011): \ \textit{A Perfect Moral Storm}", BAD)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Two more boundaries. <bookmark mark='a'/>Joseph Carens argued in 1987 that citizenship in a rich country "
            "is the modern equivalent of feudal privilege, an inherited status that greatly enhances life chances, "
            "and that borders should be largely open. <bookmark mark='b'/>Walzer and Christopher Heath Wellman "
            "replied that political communities, like clubs and families, may decide their own membership. <bookmark "
            "mark='c'/>Across time, Rawls proposed a just savings principle: each generation should save for the next "
            "what it would have wished its predecessors to save for it. <bookmark mark='d'/>Climate change sharpens "
            "this: Henry Shue distinguished subsistence emissions from luxury emissions, and Stephen Gardiner's A "
            "Perfect Moral Storm described a problem that is global, intergenerational and theoretically unresolved, "
            "which links back to Part 36's discounting."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def ai(self):
        head = label(r"Justice for machines that allocate", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Gabriel \ (2020)", r"``Artificial Intelligence, \ Values, \ and Alignment'': \ we need principles that people with different values can endorse", COM),
                (r"the veil, \ tested", r"Weidinger et al. \ (2023): \ choosing behind a veil, \ people more often chose to prioritize the worst off", FAIR),
                (r"algorithmic allocation", r"credit, \ bail, \ benefits and housing are increasingly decided by models", MKT),
                (r"ahead", r"Part 39: \ aggregating judgments; \ Part 41: \ fairness metrics that cannot all hold; \ Part 42: \ whose values to align to", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Justice now has to be designed into machines. <bookmark mark='a'/>Iason Gabriel's Artificial "
            "Intelligence, Values, and Alignment, of 2020, argued that since people disagree about values, AI systems "
            "need principles that people with different values can reasonably endorse, and suggested the veil of "
            "ignorance as one way to find them. <bookmark mark='b'/>Laura Weidinger and colleagues tested this in "
            "2023: participants who chose a principle for an AI assistant behind a veil, not knowing their own "
            "position, more often chose to prioritize the worst off. <bookmark mark='c'/>Credit, bail, welfare "
            "benefits and housing are increasingly allocated by models. <bookmark mark='d'/>The rest of the series "
            "follows this thread: Part 39 asks how to aggregate many people's judgments, Part 41 meets fairness "
            "measures that cannot all hold together, and Part 42 asks whose values a machine should be aligned to."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
