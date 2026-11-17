from __future__ import annotations

from videos.psychology.psych61.common import *  # noqa: F403


class Integrative(VoiceoverScene):
    def construct(self):
        card_section(self, 6, r"Integrative experiment design", r"What if an experiment were a space, \ not a point?",
                     marr=("how",))
        self.idea()
        self.surrogate()

    def idea(self):
        rows_section(self, r"Beyond twenty questions", [
            (r"Almaatouq and colleagues, \ 2024: \ Newell's complaint (Part 58), \ answered with design", WHITE),
            (r"list the dimensions on which experiments on a question differ; \ that defines a space", MODEL),
            (r"sample many points of the space, \ often online and in parallel", PERSON),
            (r"fit a surrogate model of the effect across the space; \ theories compete to predict cells nobody has "
             r"run", GOOD),
            (r"the result is a map of where an effect holds, \ instead of a debate between two cells", YOU),
        ], "What if an experiment were a space, not a point? <bookmark mark='a'/> In 2024 Abdullah Almaatouq and "
           "colleagues answered Newell's complaint from Part 58 with design. <bookmark mark='b'/> List the dimensions "
           "on which experiments on a question differ. That defines a space. <bookmark mark='c'/> Sample many points "
           "of the space, often online and in parallel. <bookmark mark='d'/> Fit a surrogate model of the effect "
           "across the space, and let theories compete to predict cells nobody has run. <bookmark mark='e'/> The "
           "result is a map of where an effect holds, instead of a debate between two cells.",
           tag=published_tag(r"Almaatouq et al.\ (2024)"))

    def surrogate(self):
        d = load("space")
        head = heading(r"120 cells run, \ 904 predicted")
        eff = np.asarray(d["effects"])
        pred = np.asarray(d["pred"])
        run = np.asarray(d["run"])
        rest = np.setdiff1d(np.arange(len(eff)), run)
        A = axes([-1.2, 1.6], [-1.2, 1.6], x_length=4.2, y_length=4.0, xticks=[-1, 0, 1], yticks=[-1, 0, 1],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"true effect", ylabel=r"surrogate's prediction",
                 center=[-3.8, 0.0, 0], font_size=12)
        diag = DashedLine(A.ax.c2p(-1.2, -1.2), A.ax.c2p(1.6, 1.6), color=GREY_B, stroke_width=1.5)
        pts = scatter(A.ax, eff[rest], pred[rest], MODEL, radius=0.025)
        rows = rows_of([
            (r"the reminder experiment's 1,024 cells; \ 120 run at random, \ each with noise", WHITE),
            (r"a surrogate: \ the ten main effects and their 45 pairwise interactions, \ fitted with a ridge "
             r"penalty", MODEL),
            (rf"for the 904 cells never run, \ predictions correlate {d['held_out_r']:.2f} with the truth", GOOD),
            (r"a single study would have reported one of these points; \ the space shows which choices matter, \ "
             r"and where the effect reverses", YOU),
        ], 6.4, 19, 0.36).move_to([3.0, -0.1, 0])
        tag = psyche_tag(r"\texttt{community.integrative}")
        with self.voiceover(
            "Here it is with the reminder experiment. <bookmark mark='a'/> Its thousand and twenty-four cells, of "
            "which a hundred and twenty are run at random, each with noise. <bookmark mark='b'/> The surrogate is a "
            "model with the ten main effects and their forty-five pairwise interactions, fitted with a ridge penalty. "
            "<bookmark mark='c'/> For the nine hundred and four cells nobody ran, its predictions correlate zero "
            "point nine nine with the truth. <bookmark mark='d'/> A single study would have reported one of these "
            "points. The space shows which choices matter, and where the effect reverses. In Psyche the effect "
            "really is this simple; real spaces may need more runs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(diag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(pts))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
