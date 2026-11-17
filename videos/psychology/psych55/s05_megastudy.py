from __future__ import annotations

from videos.psychology.psych55.common import *  # noqa: F403


class Megastudy(VoiceoverScene):
    def construct(self):
        card_section(self, 4, r"The megastudy", r"What if you test fifty nudges at once?", marr=("how",))
        self.design()
        self.curse()
        self.shrink()

    def design(self):
        rows_section(self, r"Fifty-three ways to the gym", [
            (r"Milkman and colleagues, \ 2021: \ about 61,000 members of a gym chain, \ randomized to 53 four-week "
             r"interventions or a control", WHITE),
            (r"reminders, \ rewards, \ planning, \ norms, \ commitments: \ every arm measured on the same outcome, \ "
             r"weekly visits", MODEL),
            (r"many arms helped a little; \ the best-performing one paid small bonus points for returning after a "
             r"missed workout", GOOD),
            (r"neither behavioural scientists nor laypeople forecast well which arms would work", AUTH),
            (r"and the winner's estimate is biased upwards, \ simply because it won", PERSON),
        ], "What if you test fifty nudges at once? <bookmark mark='a'/> In 2021 Katherine Milkman and colleagues "
           "randomized about sixty-one thousand members of a gym chain to fifty-three four-week interventions, or a "
           "control. <bookmark mark='b'/> Reminders, rewards, planning, norms and commitments, every arm measured on "
           "the same outcome: weekly visits. <bookmark mark='c'/> Many arms helped a little. The best-performing one "
           "paid small bonus points for returning after a missed workout. <bookmark mark='d'/> Neither behavioural "
           "scientists nor laypeople forecast well which arms would work. <bookmark mark='e'/> And the winner's "
           "estimate is biased upwards, simply because it won.", tag=published_tag(r"Milkman et al.\ (2021)"))

    def curse(self):
        d = load("mega")
        head = heading(r"The winner's curse")
        est, tru, shr = np.asarray(d["est"]), np.asarray(d["true"]), np.asarray(d["shrunk"])
        A = axes([-0.05, 0.08], [-0.05, 0.08], x_length=4.2, y_length=4.0, xticks=[-0.04, 0, 0.04, 0.08],
                 yticks=[-0.04, 0, 0.04, 0.08], xfmt=lambda v: f"{100 * v:+.0f}", yfmt=lambda v: f"{100 * v:+.0f}",
                 xlabel=r"true effect (points)", ylabel=r"estimate", center=[-3.9, 0.0, 0], font_size=12)
        diag = DashedLine(A.ax.c2p(-0.05, -0.05), A.ax.c2p(0.08, 0.08), color=GREY_B)
        pts = scatter(A.ax, tru, est, CROWD, radius=0.06)
        k = int(d["winner"])
        win = Dot(A.ax.c2p(float(tru[k]), float(est[k])), radius=0.11, color=AUTH)
        rows = rows_of([
            (r"Psyche's megastudy: \ 53 arms, \ true effects of about one point on average (spread 1.2), \ 1,200 "
             r"people an arm", WHITE),
            (r"each estimate is truth plus noise; \ the arm that looks best is usually one whose noise happened to "
             r"be high", MODEL),
            (rf"the winner: \ estimated {100 * d['winner_est']:+.1f} points, \ truly {100 * d['winner_true']:+.1f}", AUTH),
            (r"selecting the maximum selects the luckiest: \ Part 50's filter, \ inside a single study", YOU),
        ], 7.0, 19, 0.36).move_to([2.9, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.megastudy}, \ 53 simulated arms")
        with self.voiceover(
            "Here's the winner's curse. <bookmark mark='a'/> Psyche's megastudy has fifty-three arms, with true "
            "effects of about one point on average, and twelve hundred people in each arm. <bookmark mark='b'/> Each "
            "estimate is the truth plus noise, and the arm that looks best is usually one whose noise happened to be "
            "high. <bookmark mark='c'/> Here the winner is estimated at seven points, and truly about one and a half. "
            "<bookmark mark='d'/> Selecting the maximum selects the luckiest. It's Part 50's filter, inside a single "
            "study."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(diag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(pts))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(win, scale=1.5))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def shrink(self):
        d, c = load("mega"), load("curse")
        rows_section(self, r"Shrinkage", [
            (r"empirical Bayes (\emph{Statistics, Built} Part 25): \ pull each estimate toward the average of all "
             r"arms, \ by how noisy it is relative to the real spread", WHITE),
            (rf"here the weight on each arm's own estimate is {d['weight']:.2f}: \ the winner's {100 * d['winner_est']:+.1f} "
             rf"becomes {100 * d['winner_shrunk']:+.1f}", MODEL),
            (rf"over 400 simulated megastudies: \ the winner averages {100 * c['est']:+.1f} points estimated, \ "
             rf"{100 * c['true']:+.1f} true, \ {100 * c['shrunk']:+.1f} shrunk", GOOD),
            (rf"shrinkage cuts the winner's squared error by a factor of about {c['mse_raw'] / c['mse_shrunk']:.0f}; \ "
             rf"Milkman and colleagues reported shrunk estimates for this reason", PERSON),
        ], "The fix is shrinkage. <bookmark mark='a'/> Empirical Bayes, from Statistics, Built's Part 25, pulls each "
           "estimate toward the average of all arms, by how noisy it is relative to the real spread. "
           "<bookmark mark='b'/> Here the weight on each arm's own estimate is under a half, and the winner's seven "
           "points become about four. <bookmark mark='c'/> Over four hundred simulated megastudies, the winner "
           "averages about five points estimated, about three true, and a little over two once shrunk. "
           "<bookmark mark='d'/> Shrinkage cuts the winner's squared error by a factor of about four. That's why "
           "megastudies report shrunk estimates.", tag=psyche_tag(r"\texttt{work.megastudy}, \ 400 replications"))
