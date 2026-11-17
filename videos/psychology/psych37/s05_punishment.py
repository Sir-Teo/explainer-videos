from __future__ import annotations

from videos.psychology.psych37.common import *  # noqa: F403


class Punishment(VoiceoverScene):
    def construct(self):
        self.card()
        self.decay()
        self.antisocial()

    def card(self):
        card = chapter_card(4, r"Public goods and punishment", r"Why does cooperation decay, \ and what holds it up?",
                            lit={2002: r"Fehr \& G\"achter", 2008: r"Herrmann et al."}, part=PART, scale=("group",),
                            marr=("what",))
        with self.voiceover("Chapter four. Public goods and punishment."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def decay(self):
        d = load("goods")
        head = heading(r"Ten rounds of a public good")
        A = axes([1, 10], [0, 1.0], x_length=5.6, y_length=3.6, xticks=[1, 4, 7, 10], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"round",
                 ylabel=r"average contribution", center=[-3.2, -0.3, 0], font_size=15)
        r = np.arange(1, 11)
        plain = curve(A.ax, r, d["plain"], CROWD)
        pun = curve(A.ax, r, d["punish"], GOOD)
        key = legend([(CROWD, r"no punishment"), (GOOD, r"punishment allowed")], font_size=15).move_to(
            A.ax.c2p(6.5, 0.9))
        rows = rows_of([
            (r"Psyche: \ 200 groups of four; \ most players are conditional cooperators, \ who give a little less "
             r"than the others gave last round; \ a quarter are free riders", WHITE),
            (rf"contributions fall from {pct(d['plain'][0])} to {pct(d['plain'][-1])}: \ each disappointment "
             r"teaches cooperators to give less", CROWD),
            (r"Fehr and G\"achter, \ 2002: \ with the chance to punish, \ at a cost to themselves and with no "
             r"gain, \ people punished free riders, \ and cooperation flourished; \ without it, \ it broke down",
             GOOD),
            (rf"in Psyche, \ punished free riders move toward the group's average, \ and contributions rise to "
             rf"{pct(d['punish'][-1])}", YOU),
        ], 6.0, 20, 0.34).move_to([3.4, -0.3, 0])
        tag = psyche_tag(r"\texttt{social.public\_goods}; \ Fehr \& G\"achter (2002)")
        with self.voiceover(
            "Public goods show cooperation decaying, round by round. <bookmark mark='a'/> In Psyche's version, two "
            "hundred groups of four play ten rounds. Most players are conditional cooperators: they give a little "
            "less than the others gave last round. A quarter are free riders. <bookmark mark='b'/> Contributions "
            f"fall from {spct(d['plain'][0])} to {spct(d['plain'][-1])}. Each disappointment teaches the "
            "cooperators to give less. <bookmark mark='c'/> In 2002 Ernst Fehr and Simon Gächter gave players the "
            "chance to punish others, at a cost to themselves and with no gain. People punished free riders, and "
            "cooperation flourished. Without punishment, it broke down. <bookmark mark='d'/> In Psyche, punished "
            f"free riders move toward the group's average, and contributions rise to {spct(d['punish'][-1])}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(plain), FadeIn(rows[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(pun), FadeIn(key), FadeIn(rows[3]), run_time=2)
        self.clear_scene()

    def antisocial(self):
        head = heading(r"Punishing the cooperators")
        cities_hi = VGroup(*[label(t, font_size=17, color=AUTH) for t in (
            r"Muscat", r"Athens", r"Riyadh", r"Samara", r"Minsk", r"Istanbul", r"Seoul")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12)
        cities_lo = VGroup(*[label(t, font_size=17, color=GOOD) for t in (r"Boston", r"Bonn", r"Copenhagen")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12)
        g = VGroup(VGroup(label(r"more antisocial punishment", font_size=16, color=AUTH), cities_hi).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2),
            VGroup(label(r"less", font_size=16, color=GOOD), cities_lo).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        ).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to([-3.6, 0.0, 0])
        rows = rows_of([
            (r"Herrmann, \ Th\"oni and G\"achter, \ 2008: \ the same game in 16 participant pools around the world",
             WHITE),
            (r"in some, \ people also punished those who contributed more than they did: \ antisocial punishment",
             AUTH),
            (r"where it was common, \ it removed punishment's benefit to cooperation", PERSON),
            (r"it was predicted by weak norms of civic cooperation and a weak rule of law: \ punishment helps where "
             r"it is trusted to target cheats", YOU),
        ], 6.2, 20, 0.36).move_to([3.2, -0.2, 0])
        tag = published_tag(r"Herrmann, \ Th\"oni \& G\"achter (2008)")
        with self.voiceover(
            "But punishment isn't always aimed at cheats. <bookmark mark='a'/> In 2008 Herrmann, Thöni and "
            "Gächter ran the same game in sixteen participant pools around the world. "
            "<bookmark mark='b'/> In some, people also punished those who contributed more than they did. It's "
            "called antisocial punishment. <bookmark mark='c'/> Where it was common, it removed punishment's "
            "benefit to cooperation. <bookmark mark='d'/> It was predicted by weak norms of civic cooperation and a "
            "weak rule of law. Punishment helps where it's trusted to target cheats."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(g), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
