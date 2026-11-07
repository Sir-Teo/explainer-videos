from __future__ import annotations

import numpy as np

from explainer.stats.world import World
from videos.stats.stats18.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.digest()
        self.result()
        self.island()
        self.recreate()
        self.question()
        self.objectives()

    def digest(self):
        tl = timeline(lit=(1936,)).to_edge(UP, buff=0.35)
        hc = history_card(1936, r"the \emph{Literary Digest}, \ New York",
                          r"10 million ballots mailed to telephone subscribers, \ car owners and its own readers; \ about "
                          r"2.4 million returned: \ Landon 57\%, \ Roosevelt 43\%", color=RED, width=10.4, font_size=24
                          ).move_to([0, 1.1, 0])
        rows = fit_rows(VGroup(
            label(r"the largest poll ever taken", font_size=24),
            label(r"it had called every election since 1916", font_size=24, color=GREY_A),
        ), 12.4, 0.3, [0, -1.5, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In the autumn of 1936 the Literary Digest, an American weekly magazine, ran the "
            "largest opinion poll ever taken. It mailed ten million mock ballots to people on lists of telephone "
            "subscribers and car owners, and to its own readers, and about two point four million came back. They "
            "favoured the Republican challenger, Alf Landon, over President Franklin Roosevelt, by fifty-seven "
            "percent to forty-three. <bookmark mark='b'/> Under a simple-random-sampling formula, two point four "
            "million responses would imply a tiny margin of error. <bookmark mark='c'/> And the Digest had correctly "
            "called every presidential election since 1916."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def result(self):
        bars = VGroup(
            share_bar(0.57, width=8.0, center=[0.6, 1.4, 0]),
            share_bar(36.54 / (36.54 + 60.80), width=8.0, center=[0.6, 0.0, 0]),
            share_bar(0.44, width=8.0, center=[0.6, -1.4, 0]),
        )
        names = VGroup(label(r"\emph{Literary Digest}", font_size=24).next_to(bars[0], LEFT, buff=0.3),
                       label(r"the election", font_size=24).next_to(bars[1], LEFT, buff=0.3),
                       label(r"Gallup", font_size=24).next_to(bars[2], LEFT, buff=0.3))
        vals = VGroup(label(r"Landon 57\%", font_size=22).move_to(bars[0][0]), label(r"Landon 37.5\%", font_size=22).move_to(bars[1][0]),
                      label(r"Landon 44\%", font_size=22).move_to(bars[2][0]))
        foot = fit_rows(VGroup(
            label(r"Roosevelt: \ 61\% of all votes, \ 46 states; bars normalize the two candidates", font_size=24, color=RED),
            label(r"George Gallup, \ with about 50,000 chosen by quota, \ called the winner", font_size=22, color=GREY_A),
        ), 12.4, 0.25, [0, -2.8, 0])
        tag = historical_tag(r"Squire (1988); \ official returns", corner=UR)
        with self.voiceover(
            "<bookmark mark='a'/> Here is the Digest's forecast, with Landon, the challenger, in blue. <bookmark "
            "mark='b'/> And here's the election. Roosevelt won about sixty-one percent of the vote, and forty-six of "
            "the forty-eight states: one of the largest landslides in American history. The Digest was wrong by about"
            " twenty points. <bookmark mark='c'/> A young pollster called George Gallup, with a sample of about fifty"
            " thousand chosen by quotas to mirror the electorate, predicted Roosevelt's victory, and even predicted, "
            "in advance, the Digest's mistake. Within two years the Digest was gone."
        ) as vo:
            self.add(tag)
            vo.wait_until("a")
            self.play(FadeIn(names[0]), FadeIn(bars[0]), FadeIn(vals[0]))
            vo.wait_until("b")
            self.play(FadeIn(names[1]), FadeIn(bars[1]), FadeIn(vals[1]), FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(names[2]), FadeIn(bars[2]), FadeIn(vals[2]), FadeIn(foot[1]))
        self.clear_scene()

    def island(self):
        Wd = World()
        mp = IslandMap(Wd.towns, center=[-2.2, 0.0, 0], scale=0.78)
        rows = fit_rows(VGroup(
            label(r"the World: \ 741,311 adults in 200 towns", font_size=24),
            label(r"an election: \ Blue, \ the challenger, \ against Red", font_size=24),
            label(r"we know every vote: \ Blue 38.2\%", font_size=24, color=BLUE),
            label(r"the World's polling firm can run any survey", font_size=22, color=GREY_A),
        ), 4.6, 0.4, [4.6, 0.2, 0])
        tag = simulated_tag(r"the World's survey block", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> We can rerun 1936 on the World. Its seven hundred and forty-one thousand adults "
            "live in two hundred towns on an island, here sized by population and coloured by region. <bookmark "
            "mark='b'/> They're voting in an election between a challenger, Blue, and the incumbent, Red. <bookmark "
            "mark='c'/> Because the World is ours, we know every vote: Blue has thirty-eight point two percent. "
            "<bookmark mark='d'/> And the World now has a polling firm that can run any survey we design, honest or "
            "not."
        ) as vo:
            self.add(tag)
            vo.wait_until("a")
            self.play(Create(mp.coast), LaggedStart(*[GrowFromCenter(d_) for d_ in mp.dots], lag_ratio=0.005), FadeIn(rows[0]),
                      run_time=2.5)
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def recreate(self):
        d = load("digest")
        steps = VGroup(
            VGroup(label(r"all adults", font_size=22), MathTex(f"{d['N']:,}", font_size=28)),
            VGroup(label(r"on the registers", font_size=22, color=FRAME), MathTex(f"{d['n_listed']:,}", font_size=28, color=FRAME)),
            VGroup(label(r"returned a ballot", font_size=22, color=RESP), MathTex(f"{d['n_returns']:,}", font_size=28, color=RESP)),
        )
        for k, s_ in enumerate(steps):
            s_.arrange(DOWN, buff=0.15).move_to([-4.6 + 4.6 * k, 2.2, 0])
        arrows = VGroup(*[Arrow(steps[k].get_right(), steps[k + 1].get_left(), buff=0.2, color=GREY_B) for k in range(2)])
        bars = VGroup(*[share_bar(s, width=3.6, height=0.4, center=[-4.6 + 4.6 * k, 0.9, 0])
                        for k, s in enumerate((d["truth"], d["blue_listed"], d["blue_returns"]))])
        pct = VGroup(*[MathTex(rf"\text{{Blue}}\ {100 * s:.1f}\%", font_size=26, color=BLUE).next_to(bars[k], DOWN, buff=0.15)
                       for k, s in enumerate((d["truth"], d["blue_listed"], d["blue_returns"]))])
        srs = fit_rows(VGroup(
            label(r"a simple random sample of 1,000:", font_size=24),
            MathTex(rf"\text{{Blue}}\ {100 * d['srs_est']:.1f}\%,\ \ 95\%\ \text{{CI}}\ [{100 * d['srs_ci'][0]:.1f},\ {100 * d['srs_ci'][1]:.1f}]",
                    font_size=28, color=HIT),
        ), 12.4, 0.2, [0, -1.6, 0])
        tag = simulated_tag(r"the World's Digest", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> The World's Digest works the same way. Start from all the adults. <bookmark "
            "mark='b'/> Mail a ballot to everyone on the island's telephone and car registers: two hundred and eight "
            "thousand people, the better-off ones. <bookmark mark='c'/> About one in six sends it back: thirty-four "
            "and a half thousand ballots. <bookmark mark='d'/> Among all adults, Blue has thirty-eight percent. Among"
            " the listed, forty-seven. Among those who returned a ballot, fifty-eight: a confident Blue victory, and "
            "wrong by twenty points. <bookmark mark='e'/> Meanwhile a simple random sample of just a thousand adults "
            "says thirty-eight percent, with an interval of thirty-five to forty-one, which contains the truth."
        ) as vo:
            self.add(tag)
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), FadeIn(bars[0]), FadeIn(pct[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[0]), FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[1]), FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(bars[1]), FadeIn(pct[1]))
            self.play(FadeIn(bars[2]), FadeIn(pct[2]))
            vo.wait_until("e")
            self.play(FadeIn(srs))
        self.clear_scene()

    def question(self):
        rows = fit_rows(VGroup(
            label(r"34,588 ballots, \ wrong by 20 points", font_size=28, color=RES),
            label(r"1,000 random people, \ right to within 3", font_size=28, color=HIT),
            label(r"how can a small sample speak for a nation?", font_size=26),
            label(r"and why can't a huge one?", font_size=26, color=OBS),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Thirty-four thousand ballots, wrong by twenty points. <bookmark mark='b'/> A "
            "thousand random people, right to within three. <bookmark mark='c'/> How can so few speak for so many, "
            "<bookmark mark='d'/> and why can't the many speak for themselves? The answers are about how the sample "
            "was chosen, not how big it is."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 18", font_size=34, color=GREY_B), label(r"Who Did You Ask?", font_size=60)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"frame and nonresponse bias; \ Meng's identity: \ why size can't buy back bias",
            r"design-based inference: \ the randomness is in the selection",
            r"simple random sampling, \ stratification, \ clusters and stages",
            r"unequal probabilities: \ Hansen--Hurwitz, \ Horvitz--Thompson, \ Basu's elephants",
            r"ratio and regression estimators; \ weighting and raking; \ polls from 1948 to 2020",
        ], color=BLUE, font_size=26)
        prereq = note(r"prerequisites: \ Parts 8 and 11").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.survey}; \ the World's polling firm; \ the island map").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part eighteen: who did you ask? <bookmark mark='b'/> We'll separate the Digest's "
            "two mistakes and measure them with Xiao-Li Meng's identity; see why a probability sample needs no model "
            "of the population; build simple random, stratified and cluster samples; meet unequal-probability "
            "estimators and Basu's elephants; use auxiliary information, weighting and raking; and look at what went "
            "wrong with the polls of 1948, 2016 and 2020."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
