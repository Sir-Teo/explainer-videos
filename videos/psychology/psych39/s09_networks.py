from __future__ import annotations

from videos.psychology.psych39.common import *  # noqa: F403

NODES = [r"sleep", r"fatigue", r"concentration", r"mood", r"interest", r"guilt", r"appetite", r"worry",
         r"agitation"]


def symptom_web(active=0, strong=True, radius=1.7) -> VGroup:
    """Nine symptom nodes on a circle with edges between all pairs (thick for strong connections)."""
    pts = [np.array([radius * np.cos(TAU * k / 9 + PI / 2), radius * np.sin(TAU * k / 9 + PI / 2), 0])
           for k in range(9)]
    edges = VGroup()
    for i in range(9):
        for j in range(i + 1, 9):
            edges.add(Line(pts[i], pts[j], color=GREY_D, stroke_width=2.2 if strong else 0.8,
                           stroke_opacity=0.8 if strong else 0.4))
    nodes = VGroup()
    for k, (p, n) in enumerate(zip(pts, NODES)):
        on = k < active
        c = Circle(radius=0.2, color=AUTH if on else SYMP, fill_opacity=0.9 if on else 0.15, stroke_width=2)
        nodes.add(VGroup(c.move_to(p), label(n, font_size=13, color=GREY_A).move_to(p * 1.32)))
    return VGroup(edges, nodes)


class Networks(VoiceoverScene):
    def construct(self):
        self.card()
        self.web()
        self.hysteresis()
        self.episode()

    def card(self):
        card = chapter_card(8, r"Symptoms that cause each other", r"Is a disorder a cause, \ or a system?",
                            lit={2016: r"Cramer et al.", 2017: r"Borsboom"}, part=PART, scale=("person",),
                            marr=("how",))
        with self.voiceover("Chapter eight. Symptoms that cause each other."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def web(self):
        head = heading(r"No hidden cause")
        web = symptom_web(active=0).move_to([-3.4, -0.3, 0])
        chain = [0, 1, 2, 3]
        rows = rows_of([
            (r"the usual picture: \ a hidden disorder causes the symptoms, \ as a virus causes a fever", WHITE),
            (r"the network picture: \ the symptoms cause each other; \ poor sleep brings fatigue, \ fatigue "
             r"hurts concentration, \ failure lowers mood, \ and low mood disturbs sleep", SYMP),
            (r"the disorder is the state the whole network settles in, \ not a thing behind it", MODEL),
            (r"Borsboom, \ 2017: \ a network theory of mental disorders; \ Cramer and colleagues, \ 2016: \ "
             r"depression as a dynamical system", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Cramer et al.\ (2016); \ Borsboom (2017)")
        with self.voiceover(
            "The deepest alternative to categories rethinks what a disorder is. <bookmark mark='a'/> The usual "
            "picture is a hidden disorder that causes the symptoms, the way a virus causes a fever. "
            "<bookmark mark='b'/> The network picture says the symptoms cause each other. Poor sleep brings fatigue. "
            "Fatigue hurts concentration. Failing at things lowers mood. And low mood disturbs sleep. "
            "<bookmark mark='c'/> The disorder is the state the whole network settles into, not a thing behind it. "
            "<bookmark mark='d'/> Denny Borsboom set out the theory, and Angélique Cramer and colleagues modelled "
            "depression this way, as a dynamical system."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(web))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            for k in chain:
                self.play(web[1][k][0].animate.set_fill(AUTH, opacity=0.9).set_stroke(AUTH), run_time=0.5)
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def hysteresis(self):
        d = load("sweep")
        head = heading(r"Stress up, \ stress down")
        lev = np.asarray(d["levels"], float)
        A = axes([-2, 6], [0, 9], x_length=4.6, y_length=2.6, xticks=[-2, 0, 2, 4, 6], yticks=[0, 3, 6, 9],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"stress", ylabel=r"active symptoms",
                 center=[-3.6, 1.0, 0], font_size=13)
        B = axes([-2, 6], [0, 9], x_length=4.6, y_length=2.0, xticks=[-2, 0, 2, 4, 6], yticks=[0, 9],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"stress", ylabel=r"active",
                 center=[-3.6, -2.2, 0], font_size=13)
        su = curve(A.ax, lev, d["strong_up"], AUTH, stroke_width=4)
        sd = curve(A.ax, lev, d["strong_down"], SYMP, stroke_width=4)
        wu = curve(B.ax, lev, d["weak_up"], AUTH, stroke_width=3)
        wd = curve(B.ax, lev, d["weak_down"], SYMP, stroke_width=3)
        la = label(r"strongly connected", font_size=14, color=GREY_A).next_to(A, UP, buff=0.05)
        lb = label(r"weakly connected", font_size=14, color=GREY_A).next_to(B, UP, buff=0.05)
        key = legend([(AUTH, r"stress rising"), (SYMP, r"stress falling")], font_size=13).move_to(A.ax.c2p(0.2, 7))
        rows = rows_of([
            (r"Psyche: \ nine symptoms, \ each switching on with a chance that rises with stress and with how many "
             r"of its neighbours are on", WHITE),
            (r"strongly connected: \ as stress rises the symptoms switch on together, \ suddenly; \ as stress falls "
             r"they stay on, \ and switch off only at a much lower level", AUTH),
            (r"this is hysteresis: \ at the same stress, \ the network can be well or ill, \ depending on where it "
             r"came from", MODEL),
            (r"weakly connected: \ symptoms rise and fall smoothly with stress; \ in the model, \ vulnerability is "
             r"the strength of the connections", GOOD),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{clinic.sweep}; \ after Cramer et al.\ (2016)")
        with self.voiceover(
            "Psyche builds such a network. <bookmark mark='a'/> Nine symptoms, each switching on with a chance that "
            "rises with stress, and with how many of its neighbours are on. Then stress is raised, and lowered "
            "again. <bookmark mark='b'/> When the connections are strong, the symptoms switch on together, suddenly, "
            "as stress rises. As stress falls they stay on, and switch off only at a much lower level. "
            "<bookmark mark='c'/> That's hysteresis. At the same level of stress, the network can be well or ill, "
            "depending on where it came from. <bookmark mark='d'/> When the connections are weak, symptoms rise and "
            "fall smoothly with stress. In this model, vulnerability is the strength of the connections."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(la))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(su), run_time=1.5)
            self.play(Create(sd), FadeIn(key), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(B), FadeIn(lb), Create(wu), Create(wd))
        self.clear_scene()

    def episode(self):
        d = load("episode")
        head = heading(r"An episode")
        t = np.arange(len(d["strong_path"]))
        A = axes([0, 300], [0, 9], x_length=6.0, y_length=2.4, xticks=[0, 100, 200, 300], yticks=[0, 9],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"time", ylabel=r"active symptoms",
                 center=[-2.9, 0.6, 0], font_size=13)
        span = Rectangle(width=abs(A.ax.c2p(120, 0)[0] - A.ax.c2p(60, 0)[0]), height=2.4,
                         stroke_width=0, fill_color=AUTH, fill_opacity=0.12)
        span.move_to([(A.ax.c2p(60, 0)[0] + A.ax.c2p(120, 0)[0]) / 2, A.ax.c2p(0, 4.5)[1], 0])
        ls = label(r"a stressful spell", font_size=13, color=AUTH).next_to(span, UP, buff=0.05)
        strong = curve(A.ax, t, d["strong_path"], AUTH, stroke_width=3)
        weak = curve(A.ax, t, d["weak_path"], GOOD, stroke_width=2)
        key = legend([(AUTH, r"strongly connected"), (GOOD, r"weakly connected")], font_size=13).move_to(
            A.ax.c2p(240, 7.5))
        rows = rows_of([
            (r"everyday stress, \ then a stressful spell, \ then everyday stress again", WHITE),
            (rf"the strongly connected network tips into an episode fast, \ and after the stress ends it takes "
             rf"{d['strong_recover']} steps to recover; \ the weakly connected one, \ {d['weak_recover']}", AUTH),
            (r"a model of why episodes can start suddenly and end slowly, \ and why the same stress can leave one "
             r"person ill and another well", MODEL),
            (r"a model, \ not a finding: \ the network idea is tested against data in Parts 40 and 47", YOU),
        ], 12.0, 19, 0.3).move_to([0, -2.3, 0])
        tag = psyche_tag(r"\texttt{clinic.episode}, \ median of 21 runs")
        with self.voiceover(
            "Here's an episode in time. <bookmark mark='a'/> Everyday stress, then a stressful spell, then everyday "
            "stress again. <bookmark mark='b'/> The strongly connected network tips into an episode fast, and after "
            f"the stress ends it takes {d['strong_recover']} steps to recover. The weakly connected one takes "
            f"{d['weak_recover']}. <bookmark mark='c'/> It's a model of why episodes can start suddenly and end "
            "slowly, and why the same stress can leave one person ill and another well. "
            "<bookmark mark='d'/> It's a model, not a finding. The network idea is tested against data in Parts 40 "
            "and 47."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(span), FadeIn(ls))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(strong), Create(weak), FadeIn(key), run_time=2.5)
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
