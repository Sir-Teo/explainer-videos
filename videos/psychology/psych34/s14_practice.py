from __future__ import annotations

from videos.psychology.psych34.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.rooms()
        self.ratings()
        self.spreading()

    def card(self):
        card = chapter_card(13, r"In practice: \ rooms, \ ratings and reach", r"How do you design for influence?",
                            lit={2012: r"Bond et al.", 2013: r"Muchnik et al."}, part=PART, scale=("group", "society"),
                            marr=("what",))
        with self.voiceover("Chapter thirteen. In practice: rooms, ratings and reach."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def rooms(self):
        head = heading(r"Designing the room")
        items = [
            (r"committees, \ juries, \ forecasting panels", r"collect independent judgements before discussion: \ the "
             r"diversity identity of chapter eleven, \ and the hidden profile of chapter seven", GOOD),
            (r"speaking up about safety", r"one dissenter breaks a unanimous majority \ (chapter one), \ and peers "
             r"who refuse are the strongest brake on obedience \ (chapter three): \ make dissent someone's job", CROWD),
            (r"incident reviews and audits", r"ask what the situation made easy, \ not only who obeyed: \ the "
             r"dose-response curve of chapter three", AUTH),
            (r"who is heard", r"centralized groups amplify one voice, \ right or wrong \ (chapter ten); \ rotate who "
             r"speaks first", MODEL),
        ]
        rows = VGroup()
        for what, how, c in items:
            rows.add(VGroup(word_chip(what, color=c, font_size=19, width=4.4), wrapped_label(how, 7.6, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to([0, -0.2, 0])
        with self.voiceover(
            "Influence can be designed for. Start with the room. <bookmark mark='a'/> Committees, juries and "
            "forecasting panels should collect independent judgements before anyone talks. That keeps the diversity "
            "that makes a crowd wise, and gets unshared facts onto the table. <bookmark mark='b'/> For speaking up "
            "about safety: one dissenter breaks a unanimous majority, and peers who refuse were the strongest brake "
            "on obedience Milgram found. So make dissent someone's job. <bookmark mark='c'/> In incident reviews "
            "and audits, ask what the situation made easy, not only who went along. <bookmark mark='d'/> And watch "
            "who is heard. A group that listens to one central voice amplifies it, right or wrong, so rotate who "
            "speaks first."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def ratings(self):
        head = heading(r"Ratings that herd")
        A = axes([-0.6, 2.6], [0, 1.4], x_length=5.2, y_length=3.4, xticks=None, yticks=None,
                 center=[-3.4, -0.3, 0], font_size=14)
        b = bars(A.ax, [0, 1, 2], [1.0, 1.25, 1.0], [GREY_B, GOOD, AUTH], width=0.6)
        names = VGroup(*[label(t, font_size=15, color=c).next_to(A.ax.c2p(k, 0), DOWN, buff=0.15) for k, (t, c) in
                         enumerate(((r"untouched", GREY_B), (r"one fake up-vote", GOOD),
                                    (r"one fake down-vote", AUTH)))])
        tops = VGroup(label(r"+25\%", font_size=20, color=GOOD).next_to(A.ax.c2p(1, 1.25), UP, buff=0.1),
                      label(r"corrected", font_size=16, color=AUTH).next_to(A.ax.c2p(2, 1.0), UP, buff=0.1))
        cap = label(r"final rating, \ relative to untouched comments", font_size=16, color=GREY_A).next_to(A, UP,
                                                                                                         buff=0.15)
        rows = rows_of([
            (r"Muchnik, \ Aral and Taylor, \ 2013, \ \emph{Science}: \ on a news site, \ new comments were randomly "
             r"given one up-vote, \ one down-vote, \ or nothing", WHITE),
            (r"one up-vote raised the chance of the next positive rating by 32\%, \ and final ratings by about 25\% "
             r"on average", GOOD),
            (r"a down-vote was corrected by later readers: \ herding ran one way", AUTH),
            (r"so a star rating partly measures how it started: \ hide early scores, \ or show them only after "
             r"people rate", YOU),
        ], 6.2, 20, 0.36).move_to([3.2, -0.3, 0])
        tag = published_tag(r"Muchnik, \ Aral \& Taylor (2013)")
        with self.voiceover(
            "Next, ratings and reviews. <bookmark mark='a'/> In 2013 Muchnik, Aral and Taylor ran an "
            "experiment on a social news site. New comments were randomly given one up-vote, one down-vote, or "
            "nothing. <bookmark mark='b'/> A single up-vote raised the chance of the next positive rating by "
            "thirty-two percent, and final ratings by about a quarter on average. <bookmark mark='c'/> A down-vote "
            "was corrected by later readers. The herding ran one way. <bookmark mark='d'/> So a star rating partly "
            "measures how it started. One remedy is to hide early scores, or show them only after people have "
            "rated, which is the independent-judgement rule again."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(cap), GrowFromEdge(b[0], DOWN))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(b[1], DOWN), FadeIn(tops[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(b[2], DOWN), FadeIn(tops[1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def spreading(self):
        head = heading(r"Spreading a behaviour")
        rows = rows_of([
            (r"Bond and colleagues, \ 2012, \ \emph{Nature}: \ on the day of the 2010 US congressional elections, \ "
             r"61 million Facebook users were randomly shown voting messages", WHITE),
            (r"those shown which of their friends had voted were 0.39\% more likely to vote: \ small per person, \ "
             r"about a third of a million votes in all", GOOD),
            (r"close friends carried most of the effect, \ about four times the message's own", CROWD),
            (r"for anything costly, \ seed clusters, \ not scattered celebrities: \ complex contagion needs "
             r"reinforcement \ (chapter ten)", MODEL),
            (r"and experiments like these on millions of people raise their own question: \ who agreed to take "
             r"part?", AUTH),
        ], 12.4, 22, 0.34).move_to([0, -0.3, 0])
        tag = published_tag(r"Bond et al.\ (2012)")
        with self.voiceover(
            "Last, spreading a behaviour. <bookmark mark='a'/> On the day of the 2010 United States congressional "
            "elections, Bond and colleagues randomly showed sixty-one million Facebook users messages about "
            "voting. <bookmark mark='b'/> Those shown which of their friends had voted were "
            "about 0.4 percent more likely to vote. That's small for each person, and about a third of a million "
            "votes in all. <bookmark mark='c'/> Close friends carried most of the effect, about four times as much "
            "as the message itself. <bookmark mark='d'/> For anything costly, seed clusters of friends rather than "
            "scattered celebrities: complex contagion needs reinforcement. <bookmark mark='e'/> And experiments like "
            "this, on millions of people, raise their own question: who agreed to take part?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
