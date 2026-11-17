from __future__ import annotations

from videos.psychology.psych17.common import *  # noqa: F403


def node(text, color, w=2.6, h=0.9, font_size=24):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_color=color, stroke_width=3,
                         fill_color="#05070B", fill_opacity=1)
    return VGroup(r, wrapped_label(text, w - 0.2, font_size, color).move_to(r))


class Action(VoiceoverScene):
    def construct(self):
        self.card()
        self.actor_critic()
        self.qlearning()
        self.gonogo()

    def card(self):
        card = chapter_card(4, r"From prediction to action", r"How does an error signal teach what to do?",
                            lit={1983: r"Barto, \ Sutton \& Anderson", 2004: r"Frank et al."}, part=PART,
                            scale=("circuit", "mind", "person"), marr=("what", "how", "tissue"))
        with self.voiceover("Chapter four. From prediction to action."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def actor_critic(self):
        head = heading(r"An actor and a critic")
        world = node(r"the world", WHITE).move_to([0, 2.0, 0])
        actor = node(r"the actor: \ which action, \ here?", MB, 3.0).move_to([-3.4, -0.2, 0])
        critic = node(r"the critic: \ how good is this state?", VALUE, 3.0).move_to([3.4, -0.2, 0])
        da = node(r"$\delta$: \ better or worse than expected", DELTA, 3.6).move_to([0, -1.9, 0])
        arrows = VGroup(
            Arrow(actor.get_top(), world.get_left(), color=MB, buff=0.1),
            Arrow(world.get_right(), critic.get_top(), color=GREY_B, buff=0.1),
            Arrow(critic.get_bottom(), da.get_right(), color=VALUE, buff=0.1),
            Arrow(da.get_left(), actor.get_bottom(), color=DELTA, buff=0.1),
        )
        rows = rows_of([
            (r"one error teaches both: \ the critic its values, \ the actor its habits", DELTA),
            (r"a mapping onto the brain: \ critic in the ventral striatum, \ actor in the dorsal striatum, \ "
             r"$\delta$ from dopamine", GREY_A),
        ], 12.6, 25, 0.25).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "Predicting reward is half the job. The other half is choosing what to do. <bookmark mark='a'/> In an "
            "actor-critic system, an actor chooses actions in each state, and the world responds. "
            "<bookmark mark='b'/> A critic learns how good each state is, its value, by temporal-difference "
            "learning. <bookmark mark='c'/> The critic's error, delta, says whether things just went better or worse "
            "than expected. <bookmark mark='d'/> And the same error teaches the actor: if delta is positive after an "
            "action, make that action more likely in that state; if negative, less. It's Thorndike's law of effect, "
            "with the critic deciding what counts as satisfying. <bookmark mark='e'/> A popular mapping puts the "
            "critic in the ventral striatum, the actor in the dorsal striatum, and the error in dopamine, which "
            "reaches both."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(actor), FadeIn(world), GrowArrow(arrows[0]))
            vo.wait_until("b")
            self.play(FadeIn(critic), GrowArrow(arrows[1]))
            vo.wait_until("c")
            self.play(FadeIn(da), GrowArrow(arrows[2]))
            vo.wait_until("d")
            self.play(GrowArrow(arrows[3]), FadeIn(rows[0]))
            vo.wait_until("e")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def qlearning(self):
        head = heading(r"Q-learning: \ values for actions")
        eq = MathTex(r"Q(s, a) \leftarrow Q(s, a) + \alpha\,\big[\,r + \gamma \max_{a'} Q(s', a') - Q(s, a)\,\big]",
                     font_size=46).move_to([0, 1.6, 0])
        pol = MathTex(r"P(a \mid s) = \frac{e^{\beta Q(s, a)}}{\sum_b e^{\beta Q(s, b)}}", font_size=44).move_to(
            [0, 0.0, 0])
        rows = rows_of([
            (r"learn the value of each action in each state, \ by the same TD error", DELTA),
            (r"choose by a softmax: \ $\beta$ sets how strongly the best-valued action is preferred", MB),
            (r"Chris Watkins, \ 1989; \ the core of the program that learned Atari games from pixels in 2015", GREY_A),
        ], 12.4, 27, 0.32).to_edge(DOWN, buff=0.75)
        with self.voiceover(
            "A simpler design drops the separate actor. <bookmark mark='a'/> Learn a value for every action in every "
            "state, Q of s and a: the reward still to come if you take that action and behave well afterwards. The "
            "update is the same temporal-difference error, using the best action available next. "
            "<bookmark mark='b'/> Then choose by a softmax: actions with higher values are chosen more often, and a "
            "second parameter, beta, sets how strongly. A large beta always takes the best-looking action; a small "
            "one spreads its bets. <bookmark mark='c'/> Chris Watkins introduced Q-learning in 1989, and in 2015 a "
            "version of it, with a deep network for Q, learned dozens of Atari games from the pixels on the screen."
        ) as vo:
            self.play(FadeIn(head), Write(eq))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(pol), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def gonogo(self):
        d = load("frank")
        head = heading(r"Go and NoGo in the basal ganglia")
        go = node(r"direct pathway: \ ``Go'', \ D1 receptors", DELTA, 3.0, 0.8, 21).move_to([-4.7, 2.3, 0])
        nogo = node(r"indirect pathway: \ ``NoGo'', \ D2 receptors", INHIB, 3.0, 0.8, 21).move_to([-1.4, 2.3, 0])
        rows = rows_of([
            (r"a dopamine burst strengthens Go for the action just taken; \ a dip strengthens NoGo", WHITE),
            (r"prediction: \ too little dopamine, \ better at learning from punishment; \ more, \ from reward", YOU),
            (r"2004: \ Frank, \ Seeberger and O'Reilly test people with Parkinson's disease, \ on and off medication",
             GREY_A),
            (r"off medication: \ better at avoiding what lost; \ on it: \ better at choosing what won", DELTA),
            (r"the pattern has been found again, \ though not every study separates reward from feedback cleanly",
             GREY_A),
            (r"Psyche's Go/NoGo learner: \ the avoiding side moves; \ choosing A barely does", MODEL),
        ], 6.6, 22, 0.3).to_edge(LEFT, buff=0.55).shift(DOWN * 0.55)
        A = axes([0, 3], [0.5, 0.9], x_length=4.8, y_length=3.0, yticks=[0.5, 0.7, 0.9],
                 ylabel=r"share right at test; \ chance is 0.5", center=[3.75, 0.45, 0], font_size=18)
        ax = A.ax
        bars, labs = VGroup(), VGroup()
        for k, lev in enumerate([r"off \ medication", r"healthy", r"on \ medication"]):
            for j, (key, col) in enumerate([("choose_a", DELTA), ("avoid_b", INHIB)]):
                v = d[key][k]
                x = k + 0.5 + (j - 0.5) * 0.36
                lo, hi = ax.c2p(x, 0.5), ax.c2p(x, v)
                b = Rectangle(width=0.32, height=hi[1] - lo[1], stroke_width=0, fill_color=col, fill_opacity=0.85)
                bars.add(b.move_to([lo[0], (lo[1] + hi[1]) / 2, 0]))
            labs.add(label(lev, font_size=18, color=GREY_A).next_to(ax.c2p(k + 0.5, 0.5), DOWN, buff=0.15))
        key = legend([(DELTA, r"choose A, \ the 80\% winner"), (INHIB, r"avoid B, \ the 20\% loser")], font_size=18)
        key.arrange(RIGHT, buff=0.5).next_to(labs, DOWN, buff=0.25)
        ptag = psyche_tag(r"Psyche: \ a Go/NoGo learner, \ 300 simulated people a level")
        tag = published_tag(archive.FRANK_2004.cite)
        with self.voiceover(
            "The basal ganglia offer a two-sided version. <bookmark mark='a'/> In the striatum, one pathway, the "
            "direct, promotes an action: Go. Another, the indirect, suppresses it: NoGo. They carry different "
            "dopamine receptors. A dopamine burst strengthens Go for whatever was just done; a dip strengthens NoGo. "
            "<bookmark mark='b'/> That makes a prediction. A brain short of dopamine should learn better from "
            "punishments than from rewards, and one with extra dopamine the reverse. <bookmark mark='c'/> In 2004 "
            "Michael Frank, Lauren Seeberger and Randall O'Reilly tested it in people with Parkinson's disease, who "
            "lose dopamine neurons, on and off their medication. <bookmark mark='d'/> Off medication, patients "
            "were better at learning to avoid symbols that had lost; on it, better at choosing symbols that had won. "
            "<bookmark mark='e'/> The asymmetry has been reported again since, though some later studies argue the "
            "task mixes reward with plain feedback about being right. <bookmark mark='f'/> Psyche runs the same task "
            "on a Go and NoGo learner, with dopamine setting the balance between the two. Avoiding the loser rises "
            "as dopamine falls; choosing the winner barely moves. The model gets the direction of the effect, not "
            "all of it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(go), FadeIn(nogo), FadeIn(A), FadeIn(labs), FadeIn(key))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("f")
            self.play(FadeIn(rows[5], shift=RIGHT * 0.15), FadeIn(ptag), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                                                                             lag_ratio=0.15), run_time=2.5)
        self.clear_scene()
