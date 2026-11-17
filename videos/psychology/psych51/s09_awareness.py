from __future__ import annotations

from videos.psychology.psych51.common import *  # noqa: F403


class Awareness(VoiceoverScene):
    def construct(self):
        card_section(self, 8, r"Situation awareness", r"What does an operator need to know, \ right now?")
        self.levels()
        self.errors()
        self.measure()

    def levels(self):
        chips_section(self, r"Three levels", [
            (r"1. \ perceive", r"notice the elements: \ the airspeed, \ the other aircraft, \ the warning light", PERSON),
            (r"2. \ comprehend", r"put them together: \ what does this pattern mean for my goals?", MODEL),
            (r"3. \ project", r"say what happens next: \ where will that aircraft be in two minutes?", GOOD),
        ], "What does an operator need to know, right now? Mica Endsley's answer in 1995 has three levels. "
           "<bookmark mark='a'/> Level one: perceive the elements, like the airspeed, the other aircraft, the warning "
           "light. <bookmark mark='b'/> Level two: comprehend them together. What does this pattern mean for my "
           "goals? <bookmark mark='c'/> And level three: project. Where will that aircraft be in two minutes? An "
           "expert's advantage lives mostly at levels two and three, in Part 24's chunks and schemas.",
           foot=r"Parts 18, \ 19 and 24 in one sentence: \ what is attended, \ held, \ and understood",
           tag=published_tag(r"Endsley (1995)"))

    def errors(self):
        head = heading(r"Where awareness fails")
        A = axes([0.3, 3.7], [0, 0.9], x_length=5.4, y_length=3.0, xticks=None, yticks=[0, 0.4, 0.8],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"share of errors", center=[-3.3, 0.3, 0], font_size=12)
        share = [0.763, 0.203, 0.034]
        cols = [PERSON, MODEL, GOOD]
        b = bars(A.ax, [1, 2, 3], share, cols, width=0.6)
        names = VGroup(*[label(s, font_size=14, color=c).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.12)
                         for i, (s, c) in enumerate(zip([r"perceive", r"comprehend", r"project"], cols))])
        rows = rows_of([
            (r"Debra Jones and Mica Endsley coded the awareness errors in aviation incident reports", WHITE),
            (r"about three quarters were at level one: \ the information was not perceived, \ often because it was "
             r"not displayed, \ hard to see, \ or never looked at", PERSON),
            (r"most of the rest were at level two: \ the information seen, \ its meaning missed", MODEL),
            (r"a design target: \ put the elements where the eyes already are, \ and show what they mean", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Jones \& Endsley (1996)")
        with self.voiceover(
            "Where does awareness fail? <bookmark mark='a'/> Debra Jones and Mica Endsley coded the awareness errors in "
            "aviation incident reports. <bookmark mark='b'/> About three quarters were at level one. The information "
            "wasn't perceived, often because it wasn't displayed, was hard to see, or was never looked at. "
            "<bookmark mark='c'/> Most of the rest were at level two: the information was seen, but its meaning was "
            "missed. <bookmark mark='d'/> That's a design target. Put the elements where the eyes already are, and "
            "show what they mean."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[1]), FadeIn(b[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def measure(self):
        chips_section(self, r"Measuring awareness", [
            (r"SAGAT", r"freeze the simulator, \ blank the displays, \ ask questions at all three levels, \ and score "
                       r"the answers against the simulator's truth", MODEL),
            (r"SPAM", r"ask while the task runs, \ displays visible: \ the time to answer measures how ready the "
                      r"knowledge was", PERSON),
            (r"SART", r"self-ratings after the run: \ they track confidence, \ which Part 25 showed is a different "
                      r"thing", AUTH),
            (r"the critique", r"``lost awareness'' can become a label for blame after the fact (Dekker); \ the "
                              r"measure is useful only if it was taken before anyone knew the outcome", YOU),
        ], "How is awareness measured? <bookmark mark='a'/> The freeze probe, SAGAT: stop the simulator, blank the "
           "displays, ask questions at all three levels, and score the answers against the simulator's truth. "
           "<bookmark mark='b'/> Online probes, SPAM: ask while the task runs, with the displays visible, and use the "
           "time to answer as a measure of how ready the knowledge was. <bookmark mark='c'/> Self-ratings, SART, after "
           "the run. They track confidence, and Part 25 showed that confidence is a different thing. "
           "<bookmark mark='d'/> And a critique. Lost awareness can become a label for blame after the fact, as Sidney "
           "Dekker warns. The measure is useful only when it was taken before anyone knew the outcome.",
           chip_w=2.8, text_w=9.2)
