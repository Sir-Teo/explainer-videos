from __future__ import annotations

from videos.psychology.psych29.common import *  # noqa: F403


class Fear(VoiceoverScene):
    def construct(self):
        self.card()
        self.roads()
        self.model()
        self.sm()
        self.circuit()

    def card(self):
        card = chapter_card(8, r"Fear in the brain", r"Is the amygdala the seat of fear?",
                            lit={1996: r"LeDoux", 2011: r"Feinstein et al.", 2013: r"Feinstein et al.",
                                 2015: r"LeDoux"},
                            part=PART, scale=("circuit", "brain"), marr=("how", "tissue"))
        with self.voiceover("Chapter eight. Fear in the brain."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def roads(self):
        head = heading(r"LeDoux's two roads")
        eye = word_chip(r"the ear", color=WHITE, font_size=22).move_to([-5.4, 0.4, 0])
        thal = word_chip(r"thalamus", color=COG, font_size=22).move_to([-2.8, 0.4, 0])
        ctx = word_chip(r"auditory cortex", color=BODY, font_size=22).move_to([-0.4, 1.9, 0])
        amy = word_chip(r"amygdala", color=FEAR, font_size=24).move_to([-0.4, -1.1, 0])
        out = word_chip(r"freeze, \ startle, \ racing heart", color=FEAR, font_size=20).move_to([-0.4, -2.6, 0])
        low = Arrow(thal.get_bottom(), amy.get_left(), buff=0.1, color=FEAR, stroke_width=5)
        high1 = Arrow(thal.get_top(), ctx.get_left(), buff=0.1, color=BODY, stroke_width=3)
        high2 = Arrow(ctx.get_bottom(), amy.get_top(), buff=0.1, color=BODY, stroke_width=3)
        a0 = Arrow(eye.get_right(), thal.get_left(), buff=0.1, color=GREY_B)
        a1 = Arrow(amy.get_bottom(), out.get_top(), buff=0.1, color=FEAR)
        ll = label(r"low road: \ fast, \ coarse", font_size=17, color=FEAR).next_to(low, LEFT, buff=0.05)
        hl = label(r"high road: \ slower, \ detailed", font_size=17, color=BODY).next_to(ctx, RIGHT, buff=0.2)
        rows = rows_of([
            (r"Joseph LeDoux, \ studying fear conditioning in rats \ (Part 16): \ a tone paired with a shock comes "
             r"to make the rat freeze", WHITE),
            (r"the tone reaches the amygdala two ways: \ directly from the thalamus, \ and through the cortex", COG),
            (r"cut the auditory cortex, \ and a rat still learns to fear a simple tone: \ the low road suffices", FEAR),
            (r"better safe than sorry: \ start the response on a rough guess, \ then let the cortex confirm or "
             r"cancel it", BODY),
        ], 5.2, 21, 0.32).move_to([4.0, -0.1, 0])
        tag = published_tag(r"LeDoux (1996)")
        with self.voiceover(
            "Fear is the emotion whose circuits are best known, mostly from rats. <bookmark mark='a'/> Joseph "
            "LeDoux studied the fear conditioning of Part 16: a tone paired with a shock comes to make a rat freeze. "
            "<bookmark mark='b'/> He traced how the tone reaches the amygdala, a small structure deep in the "
            "temporal lobe. It arrives two ways: directly from the thalamus, a low road, and through the cortex, a "
            "high road. <bookmark mark='c'/> Remove the auditory cortex, and a rat still learns to fear a simple "
            "tone: the low road is enough. <bookmark mark='d'/> LeDoux's interpretation: better safe than sorry. "
            "Start the defensive response on a rough guess, and let the slower cortex confirm or cancel it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(eye), FadeIn(thal), GrowArrow(a0))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(amy), GrowArrow(low), FadeIn(ll), FadeIn(ctx), GrowArrow(high1), GrowArrow(high2),
                      FadeIn(hl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(out), GrowArrow(a1))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def model(self):
        d = load("fear")
        head = heading(r"A stick, \ or a snake?")
        A = axes([0, 0.6], [0, 1.6], x_length=6.0, y_length=3.6, xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                 yticks=[0, 0.5, 1.0, 1.5], xfmt=lambda v: f"{1000 * v:.0f}", yfmt=lambda v: f"{v:g}",
                 xlabel=r"milliseconds after it appears", ylabel=r"amygdala activity", center=[-3.2, -0.3, 0],
                 font_size=16)
        cs = curve(A.ax, d["t"], d["snake"], FEAR, 4)
        ck = curve(A.ax, d["t"], d["stick"], COG, 4)
        cl = curve(A.ax, d["t"], d["lesion"], GREY_B, 3)
        key = legend([(FEAR, r"snake"), (COG, r"stick"), (GREY_B, r"snake, \ no amygdala")], font_size=17)
        key.move_to(A.ax.c2p(0.45, 0.6))
        rows = rows_of([
            (r"Psyche: \ the thalamic route drives the amygdala on coarse shape after 15 ms; \ the cortical route "
             r"identifies the object after 60 ms \ (illustrative timings)", MODEL),
            (rf"stick and snake start the same response: \ up to {d['early']:.2f} before the cortex reports", COG),
            (r"for the snake the cortex adds drive; \ for the stick it inhibits, \ and the response dies away", FEAR),
            (r"no amygdala, \ no response at all, \ whatever the cortex knows", GREY_B),
        ], 5.6, 21, 0.3).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{emotion.two\_roads}")
        with self.voiceover(
            "Psyche's version of the two roads. <bookmark mark='a'/> A long, curved object appears on the path. The "
            "thalamic route drives the amygdala on coarse shape, quickly; the cortical route identifies the object "
            "later. The timings here are illustrative. <bookmark mark='b'/> A stick and a snake start exactly the "
            "same response, before the cortex has said which it is. <bookmark mark='c'/> For the snake, the cortex "
            "adds drive and the response grows. For the stick, it inhibits, and the response dies away: the jump, "
            "and then the relief. <bookmark mark='d'/> And with no amygdala, there is no response at all, whatever "
            "the cortex knows."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ck), Create(cs), FadeIn(key[:2]), FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(cl), FadeIn(key[2]), FadeIn(rows[3]))
        self.clear_scene()

    def sm(self):
        head = heading(r"S.\,M.")
        rows = rows_of([
            (r"S.\,M.: \ a woman with damage to both amygdalae from a rare genetic disease, \ Urbach--Wiethe "
             r"disease", WHITE),
            (r"Feinstein, \ Adolphs, \ Damasio and Tranel, \ 2011: \ handling live snakes and spiders, \ walking "
             r"through a haunted house, \ watching horror films, \ she reported no fear", FEAR),
            (r"in daily life she had walked into dangerous situations, \ including being held at knifepoint, \ "
             r"without feeling afraid", UNPL),
            (r"2013: \ breathing air rich in carbon dioxide, \ which signals suffocation from inside the body, \ "
             r"she felt panic", BODY),
            (r"the amygdala is needed for fear of things outside the body, \ not for every fear", COG),
        ], 12.2, 25, 0.38).move_to([0, -0.2, 0])
        tag = published_tag(r"Feinstein et al.\ (2011); \ Feinstein et al.\ (2013)")
        with self.voiceover(
            "In people, the clearest evidence is one woman. <bookmark mark='a'/> The patient known as S.M. has "
            "damage to both amygdalae, from a rare genetic disease called Urbach-Wiethe disease. "
            "<bookmark mark='b'/> In 2011 Justin Feinstein, Ralph Adolphs, Antonio Damasio and Daniel Tranel had "
            "her handle live snakes and spiders, walk through a haunted house, and watch horror films. She reported "
            "no fear. <bookmark mark='c'/> In daily life she had walked into dangerous situations, including being "
            "held at knifepoint, without feeling afraid. <bookmark mark='d'/> But in 2013 the same group had her "
            "breathe air rich in carbon dioxide, which signals suffocation from inside the body, and she felt "
            "panic. <bookmark mark='e'/> So the amygdala is needed for fear of things outside the body, not for "
            "every fear."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def circuit(self):
        head = heading(r"Defence, \ or fear?")
        rows = rows_of([
            (r"LeDoux, \ 2015: \ the amygdala circuit detects threat and triggers defensive responses; \ the "
             r"conscious feeling of fear is assembled elsewhere, \ by the cortex", COG),
            (r"so a rat freezing is a defensive survival circuit at work; \ whether it feels afraid is a "
             r"separate question \ (the frontier)", FEAR),
            (r"why it matters: \ drugs that calm the freezing rat may not ease human anxiety, \ which is a feeling "
             r"as well as a response \ (Part 40)", BODY),
            (r"the same distinction runs through this part: \ the body's response, \ and the felt experience, \ "
             r"are related but not the same", WHITE),
        ], 12.2, 25, 0.4).move_to([0, -0.2, 0])
        tag = published_tag(r"LeDoux (2015)")
        with self.voiceover(
            "LeDoux himself later drew a sharper line. <bookmark mark='a'/> In 2015 he argued that the amygdala "
            "circuit detects threat and triggers defensive responses, while the conscious feeling of fear is "
            "assembled elsewhere, by the cortex. <bookmark mark='b'/> On that view a freezing rat shows a defensive "
            "survival circuit at work; whether it feels afraid is a separate question, taken up at the frontier. "
            "<bookmark mark='c'/> It matters in practice: drugs that calm a freezing rat may not ease human "
            "anxiety, which is a feeling as well as a response, as Part 40 will discuss. <bookmark mark='d'/> The "
            "same distinction runs through this whole part: the body's response and the felt experience are "
            "related, but they are not the same thing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
