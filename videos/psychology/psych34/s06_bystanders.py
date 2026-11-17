from __future__ import annotations

from videos.psychology.psych34.common import *  # noqa: F403


class Bystanders(VoiceoverScene):
    def construct(self):
        self.card()
        self.parable()
        self.laboratory()
        self.model()
        self.street()

    def card(self):
        card = chapter_card(5, r"Bystanders", r"Does a crowd make help less likely?",
                            lit={1964: r"the 38 witnesses", 1968: r"Darley \& Latan\'e", 2011: r"Fischer et al.",
                                 2020: r"Philpot et al."}, part=PART, scale=("group",), marr=("what",))
        with self.voiceover("Chapter five. Bystanders."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def parable(self):
        head = heading(r"Thirty-eight witnesses")
        headline = VGroup(Rectangle(width=6.4, height=1.3, stroke_color=GREY_B, fill_color="#E8E4D8", fill_opacity=1),
                          label(r"37 WHO SAW MURDER DIDN'T CALL THE POLICE", font_size=22, color=BLACK))
        headline[1].move_to(headline[0])
        headline.move_to([0, 2.0, 0])
        cap = label(r"\emph{The New York Times}, \ front page, \ 27 March 1964", font_size=18, color=GREY_A)
        cap.next_to(headline, DOWN, buff=0.12)
        rows = rows_of([
            (r"two weeks after Kitty Genovese was murdered in Queens, \ the \emph{Times} reported that 38 neighbours "
             r"had watched and done nothing", AUTH),
            (r"it became the founding story of a field: \ apathy in the city, \ and a crowd that does not help", CROWD),
            (r"later inquiries found about a dozen people who heard or saw parts of the attack, \ and at least one "
             r"who called the police", GOOD),
            (r"Manning, \ Levine and Collins, \ 2007: \ ``the parable of the 38 witnesses''; \ in 2016 the "
             r"\emph{Times} itself called its reporting flawed", YOU),
        ], 12.4, 21, 0.3).move_to([0, -1.25, 0])
        tag = historical_tag(r"Gansberg (1964); \ Manning, \ Levine \& Collins (2007)")
        with self.voiceover(
            "The study of bystanders began with a newspaper story. <bookmark mark='a'/> In March 1964 Kitty Genovese "
            "was murdered in Queens, New York. Two weeks later the New York Times reported, on its front "
            "page, that thirty-eight of her neighbours had watched and done nothing. <bookmark mark='b'/> It became "
            "the founding story of a field: apathy in the city, and a crowd that does not help. "
            "<bookmark mark='c'/> Later inquiries found about a dozen people who had heard or seen parts of the "
            "attack, and at least one who called the police. <bookmark mark='d'/> In 2007 "
            "Manning, Levine and Collins called it the parable of the thirty-eight witnesses. In "
            "2016 the Times itself called its reporting flawed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(headline), FadeIn(cap))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def laboratory(self):
        head = heading(r"The effect in the laboratory")
        panels = VGroup()
        for k, (title, xs, ys, names) in enumerate((
                (r"a seizure over the intercom: \ helped", [0, 1, 2], [85, 62, 31],
                 [r"alone", r"one other", r"four others"]),
                (r"smoke in the room: \ reported it", [0, 1, 2], [75, 38, 10],
                 [r"alone", r"three strangers", r"two who ignore it"]))):
            A = axes([-0.6, 2.6], [0, 100], x_length=4.2, y_length=3.0, xticks=None, yticks=[0, 50, 100],
                     yfmt=lambda v: f"{v:.0f}\\%", center=[-4.4 + 4.6 * k, 0.5, 0], font_size=14)
            b = bars(A.ax, xs, ys, [GOOD, CROWD, AUTH], width=0.6)
            nm = VGroup(*[label(n, font_size=14, color=GREY_A).next_to(A.ax.c2p(x, 0), DOWN, buff=0.15)
                          for x, n in zip(xs, names)])
            tops = VGroup(*[label(rf"{y}\%", font_size=15, color=WHITE).next_to(A.ax.c2p(x, y), UP, buff=0.06)
                            for x, y in zip(xs, ys)])
            t = label(title, font_size=18, color=WHITE).next_to(A, UP, buff=0.15)
            panels.add(VGroup(A, b, nm, tops, t))
        rows = rows_of([
            (r"Darley and Latan\'e, \ 1968: \ students talking over an intercom heard another apparently have a "
             r"seizure", WHITE),
            (r"Latan\'e and Darley, \ 1968: \ smoke poured into a room where students filled in questionnaires", WHITE),
            (r"the more people who could help, \ the less likely each one was to do anything: \ diffusion of "
             r"responsibility, \ and others' calm read as a sign nothing was wrong", CROWD),
        ], 4.0, 18, 0.3).move_to([4.9, -0.2, 0])
        tag = historical_tag(r"Darley \& Latan\'e (1968); \ Latan\'e \& Darley (1968)")
        with self.voiceover(
            "Two young psychologists, John Darley and Bibb Latané, took the story into the laboratory. "
            "<bookmark mark='a'/> In one study, students talking over an intercom heard another student apparently "
            "have a seizure. Alone, eighty-five percent went for help before the fit was over. When they believed "
            "four others could hear it too, thirty-one percent did. <bookmark mark='b'/> In another, smoke poured "
            "into a room where students were filling in questionnaires. Three quarters of those alone reported it. "
            "With two confederates who ignored the smoke, one in ten did. <bookmark mark='c'/> The more people who "
            "could help, the less likely each one was to do anything. They called it diffusion of responsibility, "
            "and added that other people's calm is read as a sign that nothing is wrong."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), *[FadeIn(p[0]) for p in panels], *[FadeIn(p[2]) for p in panels],
                      *[FadeIn(p[4]) for p in panels])
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), *[GrowFromEdge(b_, DOWN) for b_ in panels[0][1]], FadeIn(panels[0][3]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), *[GrowFromEdge(b_, DOWN) for b_ in panels[1][1]], FadeIn(panels[1][3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def model(self):
        d = load("bystanders")
        head = heading(r"Each helps less; \ does anyone help less?")
        A = axes([0.5, 20.5], [0, 1.0], x_length=6.2, y_length=3.8, xticks=[1, 5, 10, 15, 20],
                 yticks=[0, 0.25, 0.5, 0.75, 1.0], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}",
                 xlabel=r"bystanders", ylabel=r"chance that at least one helps", center=[-2.9, -0.4, 0], font_size=15)
        N = np.asarray(d["N"])
        cs = VGroup(*[curve(A.ax, N, d[f"any_{k}"], c, stroke_width=4) for k, c in ((5, GOOD), (10, CROWD),
                                                                                     (15, AUTH))])
        key = legend([(GOOD, r"each one's chance falls slowly"), (CROWD, r"falls as $1/N$"),
                      (AUTH, r"falls faster than $1/N$")], font_size=15)
        key.move_to(A.ax.c2p(13.0, 0.42))
        rows = rows_of([
            (r"suppose one person alone helps with chance 0.85, \ and each of $N$ bystanders with chance "
             r"$0.85\,N^{-\beta}$", WHITE),
            (r"the chance that anyone helps is $1 - (1 - p_N)^N$", MODEL),
            (r"if responsibility is shared exactly, \ $\beta = 1$, \ each helps much less and the group barely less; "
             r"\ only a steeper fall makes crowds worse than one person", PERSON),
            (r"so the laboratory question, \ what each person does, \ and the victim's question, \ whether anyone "
             r"helps, \ can have different answers", YOU),
        ], 5.6, 19, 0.32).move_to([3.6, -0.3, 0])
        tag = psyche_tag(r"\texttt{social.bystanders}")
        with self.voiceover(
            "But there's a catch in that logic, and a little algebra shows it. <bookmark mark='a'/> Suppose one "
            "person alone helps with a chance of point eight five, and each of N bystanders with that chance shrunk "
            "by a power of N. <bookmark mark='b'/> The chance that anyone helps is one minus the chance that nobody "
            "does. <bookmark mark='c'/> If responsibility is shared exactly, so each person's chance falls as one "
            "over N, each helps much less, but the group as a whole barely less. Only a steeper fall makes a crowd "
            "worse than one person. <bookmark mark='d'/> So the laboratory's question, what each person does, and "
            "the victim's question, whether anyone helps, can have different answers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(cs[1]))
            vo.wait_until("c")
            self.play(Create(cs[0]), Create(cs[2]), FadeIn(key), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def street(self):
        head = heading(r"What cameras show")
        big = VGroup(label(r"9 in 10", font_size=72, color=GOOD),
                     label(r"of 219 filmed public conflicts: \ at least one bystander stepped in", font_size=20,
                           color=GREY_A))
        big.arrange(DOWN, buff=0.2).move_to([-3.4, 0.6, 0])
        flags = label(r"the Netherlands, \ the UK, \ South Africa", font_size=18, color=CROWD).next_to(big, DOWN,
                                                                                                    buff=0.4)
        rows = rows_of([
            (r"Fischer and colleagues, \ 2011: \ 105 effects, \ more than 7{,}700 people: \ the bystander effect is "
             r"real, \ $g = -0.35$, \ and weaker when the emergency is dangerous", WHITE),
            (r"Philpot, \ Liebst, \ Levine, \ Bernasco and Lindegaard, \ 2020: \ city-centre camera footage of "
             r"real disputes in the Netherlands, \ the UK and South Africa", CROWD),
            (r"in about nine in ten, \ someone intervened, \ usually several people; \ the more bystanders, \ the "
             r"more likely help was", GOOD),
            (r"each bystander may feel less responsible; \ but a crowd still means more people who might act", YOU),
        ], 6.2, 20, 0.34).move_to([3.2, -0.3, 0])
        tag = published_tag(r"Fischer et al.\ (2011); \ Philpot et al.\ (2020)")
        with self.voiceover(
            "What does the wider record show? <bookmark mark='a'/> In 2011 Fischer and colleagues pooled a "
            "hundred and five effects from more than seven thousand seven hundred people. The bystander effect is "
            "real, of moderate size, and weaker when the emergency is dangerous. <bookmark mark='b'/> Then in 2020 "
            "Philpot and colleagues looked at what actually "
            "happens, in city-centre camera footage of two hundred and nineteen real disputes in the Netherlands, "
            "the United Kingdom and South Africa. <bookmark mark='c'/> In about nine in ten, someone intervened, usually several "
            "people, and the more bystanders there were, the more likely help was. <bookmark mark='d'/> Each "
            "bystander may feel less responsible. But a crowd still means more people who might act, just as the "
            "algebra said."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(flags))
            vo.wait_until("c")
            self.play(FadeIn(big, shift=UP * 0.2), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
