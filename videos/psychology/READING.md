# Psychology, Built: textbooks, theories and classic studies

The series' reading, kept in one place, and the check that it covers what a psychology degree teaches. Part 1
lists the textbooks the series follows, with the parts that cover each. Part 2 walks the chapters every
introductory textbook shares, topic by topic, and says where in the films each is taught. Part 3 is the index of
the field's major theories, with what the record now shows about each. Part 4 is the index of the classic studies
that the textbooks retell. Part 5 says where each part's paper list lives, and Part 6 says, honestly, what the
series does not cover in depth. The spine in Part 1 is grouped by the upper-level courses of a major and a
graduate programme, so it doubles as the map of those courses.

Every "where" below is a part and a chapter (`28 · ch. 5` is Part 28, chapter 5; `hook` is the part's opening),
located in the scenes themselves: `tests/test_psychology_reading.py` checks that each part and chapter exists and
that the theory's or study's author is named in the scenes of the parts given, so this map cannot drift from the
films. Verdicts in Part 3 are short summaries; the Replication Ledger (`explainer/psychology/ledger.py`) holds the
sourced record of every finding the films present.

## 1. The textbook spine

| Textbook | Parts |
|---|---|
| **Introductory** | |
| Myers & DeWall, *Psychology* | 1–4, 5–10, 11–17, 19–29, 30–42, 51–57 (Part 2 below follows its chapter order) |
| Gleitman, Gross & Reisberg, *Psychology* | 1–42 |
| Schacter, Gilbert, Nock & Wegner, *Psychology* | 1–42 |
| Gray & Bjorklund, *Psychology* | 1–42 |
| James, *The Principles of Psychology* (1890) | 1, 18, 20, 27, 29 |
| **Biological** | |
| Kandel et al., *Principles of Neural Science* | 5, 6, 7, 10, 13, 15, 17, 20 |
| Bear, Connors & Paradiso, *Neuroscience: Exploring the Brain* | 5–10, 13, 15 |
| Gazzaniga, Ivry & Mangun, *Cognitive Neuroscience* | 7, 8, 18, 20, 23, 27, 49 |
| Plomin et al., *Behavioral Genetics* | 9, 31, 32, 33 |
| **Sensation and perception** | |
| Wolfe et al., *Sensation & Perception*; Goldstein & Cacciamani, *Sensation and Perception* | 11–15 |
| Green & Swets, *Signal Detection Theory and Psychophysics*; Macmillan & Creelman, *Detection Theory* | 12, 56 |
| Kingdom & Prins, *Psychophysics* | 11 |
| **Learning** | |
| Bouton, *Learning and Behavior* | 16, 17, 40 |
| Sutton & Barto, *Reinforcement Learning* | 17, 48, 59 |
| **Cognition** | |
| Anderson, *Cognitive Psychology and Its Implications*; Eysenck & Keane, *Cognitive Psychology* | 18–27 |
| Baddeley, Eysenck & Anderson, *Memory* | 19–21 |
| Kahana, *Foundations of Human Memory* | 20, 21 |
| Kahneman, *Thinking, Fast and Slow*; Hastie & Dawes, *Rational Choice in an Uncertain World* | 26, 55 |
| Luce, *Response Times* | 1, 25 |
| **Development** | |
| Siegler et al., *How Children Develop*; Berk, *Development Through the Lifespan* | 30, 31 |
| **Social and personality** | |
| Aronson, Wilson & Sommers, *Social Psychology*; Gilovich, Keltner, Chen & Nisbett, *Social Psychology* | 34–38 |
| Funder, *The Personality Puzzle* | 33 |
| Deary, *Intelligence: A Very Short Introduction*; Mackintosh, *IQ and Human Intelligence* | 32 |
| Heine, *Cultural Psychology* | 38 |
| **Clinical** | |
| Barlow, Durand & Hofmann, *Psychopathology* | 39–42 |
| American Psychiatric Association, *DSM-5-TR*; WHO, *ICD-11* (described, not reproduced) | 39 |
| Lambert (ed.), *Bergin and Garfield's Handbook of Psychotherapy and Behavior Change*; Wampold & Imel, *The Great Psychotherapy Debate* | 42 |
| **Methods and the graduate toolkit** | |
| Shadish, Cook & Campbell, *Experimental and Quasi-Experimental Designs* | 2, 31, 43 |
| Lord & Novick, *Statistical Theories of Mental Test Scores* | 3, 45 |
| Bollen, *Structural Equations with Latent Variables*; Kline, *Principles and Practice of SEM* | 44 |
| Embretson & Reise, *Item Response Theory for Psychologists* | 45 |
| Train, *Discrete Choice Methods with Simulation* | 46 |
| Hoffman, *Longitudinal Analysis*; Snijders & Bosker, *Multilevel Analysis* | 47 |
| Farrell & Lewandowsky, *Computational Modeling of Cognition and Behavior*; Lee & Wagenmakers, *Bayesian Cognitive Modeling*; Busemeyer & Diederich, *Cognitive Modeling* | 25, 48 |
| Griffiths, Chater & Tenenbaum, *Bayesian Models of Cognition* | 14, 22, 48, 58 |
| Dayan & Abbott, *Theoretical Neuroscience* | 5, 6, 13, 17, 58 |
| Poldrack, Mumford & Nichols, *Handbook of Functional MRI Data Analysis*; Luck, *An Introduction to the Event-Related Potential Technique* | 8, 49 |
| Borenstein et al., *Introduction to Meta-Analysis* | 42, 50 |
| **Practice** | |
| Wickens et al., *Engineering Psychology and Human Performance*; Reason, *Human Error* | 51 |
| Card, Moran & Newell, *The Psychology of Human-Computer Interaction*; Norman, *The Design of Everyday Things* | 52 |
| Schmitt (ed.), *The Oxford Handbook of Personnel Assessment and Selection* | 53 |
| Dunlosky et al. (2013); Sweller, Ayres & Kalyuga, *Cognitive Load Theory* | 54 |
| Thaler & Sunstein, *Nudge* | 55 |
| Wells and Wixted's reviews; Kassin's reviews of confessions | 56 |
| Taylor, *Health Psychology* | 57 |
| **The frontier** | |
| Clark, *Surfing Uncertainty*; Parr, Pezzulo & Friston, *Active Inference* | 58 |
| Huys, Maia & Frank, "Computational psychiatry as a bridge from neuroscience to clinical applications" (2016) | 59 |
| Mitchell, *Artificial Intelligence: A Guide for Thinking Humans*; Frank, "Baby steps in evaluating the capacities of large language models" (2023) | 60 |
| **History and metascience** | |
| Boring, *A History of Experimental Psychology*; Hunt, *The Story of Psychology*; Danziger, *Constructing the Subject* | 1, 2, 3 |
| Chambers, *The Seven Deadly Sins of Psychology*; Ritchie, *Science Fictions*; Meehl's papers | 4, 43, 50, 61, 62 |

## 2. The introductory course, topic by topic

The chapters below are those every introductory textbook shares, in Myers and DeWall's order. Each row names the
classic sources and where the films teach it; most topics then climb, in the same chapter, to the model and the
record (see the part's README).

### The story of psychology

| Topic | Classic sources | Where (part · chapter) |
|---|---|---|
| Kant's objections, Fechner's reply | Kant 1786; Fechner 1860 | 1 · ch. 5 |
| Wundt's laboratory and structuralism | Wundt 1879; Titchener | 1 · ch. 6 |
| Functionalism and James's Principles | James 1890 | 1 · ch. 8 |
| The schools: Gestalt, psychoanalysis, behaviourism, humanistic, cognitive | 1900s–1960s | 1 · ch. 8 |
| Behaviourism bans the mind | Watson 1913; Skinner | 1 · ch. 7 |
| The cognitive revolution | Miller, Chomsky, Newell & Simon 1956 | 1 · ch. 8 |
| Marr's three levels | Marr 1982 | 1 · ch. 9 |

### Thinking critically with psychological science

| Topic | Classic sources | Where (part · chapter) |
|---|---|---|
| Clever Hans and expectancy effects | Pfungst 1907; Rosenthal | 2 · ch. 1 |
| Random assignment and the experiment | Peirce & Jastrow 1884 | 2 · ch. 5 |
| Correlation, confounds and causation |  | 2 · ch. 4 |
| Placebo, blinding and demand | Orne 1962 | 2 · ch. 7 |
| Research ethics | Belmont 1979 | 2 · ch. 10; 62 · ch. 3 |
| Measurement: scales, reliability, validity | Stevens 1946; Cronbach & Meehl 1955 | 3 · ch. 7 |
| The Barnum effect | Forer 1949 | 3 · ch. 3 |
| Effect sizes, p-values and power | Cohen 1962 | 4 · ch. 3 |
| The replication crisis | Bem 2011; Open Science Collaboration 2015 | 4 · ch. 9 |
| Why most published findings are false | Ioannidis 2005 | 4 · ch. 3 |
| Statistical reasoning in everyday life |  | 42 · ch. 2 |

### The biology of mind

| Topic | Classic sources | Where (part · chapter) |
|---|---|---|
| The neuron and the action potential | Hodgkin & Huxley 1952 | 5 · ch. 4 |
| Synapses and neurotransmitters | Loewi 1921 | 6 · ch. 1 |
| Drugs at the synapse |  | 6 · ch. 2 |
| Hebbian learning and LTP | Hebb 1949; Bliss & Lømo 1973 | 6 · ch. 4 |
| Habituation and sensitization in Aplysia | Kandel 1970s | 6 · ch. 5 |
| Localization: Gall to Lashley | Gall; Flourens; Lashley 1929 | 7 · ch. 2 |
| Broca's and Wernicke's areas | Broca 1861; Wernicke 1874 | 7 · ch. 3; 23 · ch. 10 |
| Phineas Gage | Harlow 1848 | 7 · hook |
| H.M. and memory | Scoville & Milner 1957 | 7 · ch. 7; 20 · ch. 10 |
| The split brain | Sperry; Gazzaniga | 7 · ch. 8 |
| Plasticity |  | 7 · ch. 10 |
| The cortex's maps and the homunculus | Penfield & Boldrey 1937 | 7 · ch. 5 |
| EEG, ERPs, MRI and fMRI | Berger 1929; Ogawa 1990 | 8 · ch. 2; 49 · ch. 9 |
| Behaviour genetics: twins and adoption | Falconer; Bouchard 1990 | 9 · ch. 3 |
| Heritability, and what it is not |  | 9 · ch. 6 |
| Genome-wide association and polygenic scores |  | 9 · ch. 10 |
| Evolutionary psychology |  | 9 · ch. 11 |
| The endocrine system and stress | the HPA axis and its feedback loop | 10 · ch. 8 |

### Consciousness and the two-track mind

| Topic | Classic sources | Where (part · chapter) |
|---|---|---|
| Circadian rhythms and sleep stages | Kleitman; Aserinsky 1953 | 10 · ch. 3 |
| Why we sleep; sleep deprivation | Borbély 1982 | 10 · ch. 4 |
| Dreams |  | 10 · ch. 7 |
| Psychoactive drugs, tolerance and withdrawal | Solomon & Corbit 1974 | 10 · ch. 11 |
| Hypnosis |  | 42 · ch. 9 |
| Blindsight, neglect and implicit processing | Weiskrantz 1974 | 27 · ch. 3 |
| Theories of consciousness | Baars; Tononi; Dehaene | 27 · ch. 6 |
| Free will and Libet's clock | Libet 1983 | 27 · ch. 10 |

### Nature, nurture and human diversity

| Topic | Classic sources | Where (part · chapter) |
|---|---|---|
| Gene–environment interplay |  | 9 · ch. 8 |
| Temperament | Thomas & Chess; Kagan | 33 · ch. 8; 30 · ch. 11 |
| Parents and peers | Harris 1995 | 31 · ch. 7 |
| Culture and the self | Markus & Kitayama 1991 | 38 · ch. 3 |
| Gender differences and similarities | Hyde 2005 | 33 · ch. 11 |

### Developing through the lifespan

| Topic | Classic sources | Where (part · chapter) |
|---|---|---|
| Habituation and looking time | Fantz; Spelke | 30 · ch. 2 |
| Piaget's stages | Piaget | 30 · ch. 1 |
| Vygotsky and the zone of proximal development | Vygotsky 1978 | 30 · ch. 11 |
| Object permanence and core knowledge | Baillargeon; Spelke | 30 · ch. 5 |
| Theory of mind and false belief | Wimmer & Perner 1983 | 30 · ch. 9 |
| Attachment: Harlow, Bowlby, Ainsworth | Harlow 1958; Ainsworth 1978 | 30 · ch. 10 |
| Parenting styles | Baumrind 1966; Maccoby & Martin 1983 | 31 · ch. 7 |
| Ecological systems | Bronfenbrenner 1979 | 31 · ch. 7 |
| Sensitive periods and early adversity | Nelson et al., Bucharest | 31 · ch. 5 |
| Adolescence |  | 31 · ch. 6 |
| Moral development | Kohlberg; Gilligan | 31 · ch. 9; 38 · ch. 7 |
| Erikson's stages and identity | Erikson 1950 | 31 · ch. 9 |
| Cognitive ageing and dementia | Salthouse; Stern | 31 · ch. 11 |

### Sensation and perception

| Topic | Classic sources | Where (part · chapter) |
|---|---|---|
| Thresholds and Weber's law | Weber 1834; Fechner 1860 | 11 · ch. 1 |
| Signal detection theory | Green & Swets 1966 | 12 · ch. 2 |
| The eye, receptive fields and edges | Kuffler 1953; Hubel & Wiesel 1959 | 13 · ch. 5 |
| Trichromacy and opponent processes | Young–Helmholtz; Hering | 13 · ch. 10 |
| Gestalt grouping | Wertheimer 1923 | 14 · ch. 2 |
| Depth perception | Julesz 1971 | 14 · ch. 3 |
| Perceptual constancy and illusions |  | 14 · ch. 4; 13 · ch. 11 |
| Perception as inference | Helmholtz 1867 | 14 · ch. 5 |
| Face perception | Kanwisher 1997 | 14 · ch. 10 |
| Hearing: place and timing theories of pitch | Helmholtz; Licklider | 15 · ch. 4 |
| Sound localization | Jeffress 1948 | 15 · ch. 5 |
| Pain and gate control | Melzack & Wall 1965 | 15 · ch. 10 |
| Smell, taste, touch, balance |  | 15 · ch. 11 |
| Sensory interaction: McGurk | McGurk & MacDonald 1976 | 15 · ch. 7 |

### Learning

| Topic | Classic sources | Where (part · chapter) |
|---|---|---|
| Classical conditioning | Pavlov 1927 | 16 · ch. 1 |
| Operant conditioning and the law of effect | Thorndike 1898; Skinner 1938 | 16 · ch. 2 |
| Schedules of reinforcement | Ferster & Skinner 1957 | 16 · ch. 3 |
| Contingency and blocking | Rescorla 1968; Kamin 1969 | 16 · ch. 5 |
| The Rescorla–Wagner model | Rescorla & Wagner 1972 | 16 · ch. 6 |
| Biological constraints: taste aversion | Garcia & Koelling 1966 | 16 · ch. 12 |
| Observational learning | Bandura, Ross & Ross 1961 | 16 · ch. 12 |
| Latent learning and cognitive maps | Tolman 1948 | 17 · ch. 7 |
| Dopamine and reward prediction error | Schultz, Dayan & Montague 1997 | 17 · ch. 3 |

### Memory

| Topic | Classic sources | Where (part · chapter) |
|---|---|---|
| Ebbinghaus's forgetting curve | Ebbinghaus 1885 | 20 · ch. 1; 21 · ch. 1 |
| The modal model | Atkinson & Shiffrin 1968 | 19 · ch. 4; 20 · ch. 6 |
| Sensory memory | Sperling 1960 | 19 · ch. 2 |
| Short-term memory and chunking | Miller 1956; Cowan 2001 | 19 · ch. 1 |
| Working memory | Baddeley & Hitch 1974 | 19 · ch. 4 |
| Serial position | Murdock 1962 | 20 · ch. 2 |
| Levels of processing | Craik & Lockhart 1972 | 20 · ch. 4 |
| Encoding specificity and context | Tulving; Godden & Baddeley 1975 | 20 · ch. 5 |
| Episodic and semantic memory | Tulving 1972 | 20 · ch. 10 |
| Interference and retrieval-induced forgetting | Anderson et al. 1994 | 21 · ch. 2 |
| Consolidation and reconsolidation | Müller & Pilzecker 1900; Nader 2000 | 21 · ch. 3 |
| Spacing and testing effects | Cepeda 2006; Roediger & Karpicke 2006 | 21 · ch. 6; 54 · ch. 2 |
| Schemas and reconstruction | Bartlett 1932 | 21 · ch. 7 |
| False memories: DRM | Roediger & McDermott 1995 | 21 · ch. 8 |
| Misinformation | Loftus & Palmer 1974 | 21 · ch. 9 |
| Flashbulb memories | Talarico & Rubin 2003 | 21 · ch. 10 |

### Thinking and language

| Topic | Classic sources | Where (part · chapter) |
|---|---|---|
| Concepts and prototypes | Rosch 1975 | 22 · ch. 3 |
| Problem solving as search | Newell & Simon 1972 | 24 · ch. 4 |
| Insight and fixation | Köhler 1925; Duncker 1945 | 24 · ch. 6 |
| Heuristics and biases | Tversky & Kahneman 1974 | 26 · ch. 6 |
| Framing and prospect theory | Kahneman & Tversky 1979 | 26 · ch. 3 |
| Overconfidence | Lichtenstein, Fischhoff & Phillips 1982 | 26 · ch. 7 |
| Language: structure and acquisition | Chomsky 1959 | 23 · ch. 7 |
| Statistical learning of words | Saffran, Aslin & Newport 1996 | 23 · ch. 6 |
| Critical periods for language | Johnson & Newport 1989 | 23 · ch. 9 |
| Language and thought | Whorf 1956 | 23 · ch. 11 |
| Mental imagery and rotation | Shepard & Metzler 1971 | 24 · ch. 9 |

### Intelligence

| Topic | Classic sources | Where (part · chapter) |
|---|---|---|
| Binet and the first tests | Binet & Simon 1905 | 32 · ch. 6 |
| Spearman's g and factor analysis | Spearman 1904 | 32 · ch. 2 |
| Multiple intelligences and their critics | Gardner 1983; Sternberg | 32 · ch. 12 |
| The Flynn effect | Flynn 1987 | 32 · ch. 9 |
| Heritability of IQ |  | 32 · ch. 9 |
| Group differences and measurement invariance |  | 32 · ch. 10 |
| Eugenics and the misuse of tests |  | 32 · ch. 11 |

### What drives us

| Topic | Classic sources | Where (part · chapter) |
|---|---|---|
| Drives and homeostasis | Cannon 1932; Hull 1943 | 28 · ch. 1 |
| Hunger |  | 28 · ch. 2 |
| Arousal and Yerkes–Dodson | Yerkes & Dodson 1908 | 28 · ch. 3 |
| Maslow's hierarchy of needs | Maslow 1943 | 28 · ch. 5 |
| Intrinsic motivation and self-determination | Deci 1971; Ryan & Deci 2000 | 28 · ch. 5 |
| Achievement and goals | Atkinson 1957; Locke & Latham 2002 | 28 · ch. 6; 53 · ch. 10 |
| Self-control and delay of gratification | Mischel; Baumeister 1998 | 28 · ch. 10 |
| Affiliation and belonging |  | 37 · ch. 11 |

### Emotions, stress and health

| Topic | Classic sources | Where (part · chapter) |
|---|---|---|
| James–Lange and Cannon–Bard | James 1884; Cannon 1927 | 29 · ch. 1 |
| Schachter–Singer's two factors | Schachter & Singer 1962 | 29 · ch. 2 |
| Basic emotions and facial expressions | Ekman 1971 | 29 · ch. 3 |
| Constructed emotion | Barrett 2017 | 29 · ch. 5 |
| Appraisal | Lazarus 1991 | 29 · ch. 7 |
| Facial feedback | Strack et al. 1988 | 29 · ch. 6 |
| Stress and illness | Selye 1956; Cohen et al. 1991 | 29 · ch. 9 |
| Affective forecasting | Gilbert & Wilson | 29 · ch. 10 |
| Happiness, income and the Easterlin paradox | Easterlin 1974 | 29 · ch. 11 |
| Placebo and nocebo |  | 57 · ch. 3 |
| Stress, appraisal and coping | Lazarus & Folkman 1984 | 29 · ch. 9 |
| Health-behaviour models | Rosenstock 1966; Prochaska & DiClemente 1983 | 57 · ch. 6 |

### Social psychology

| Topic | Classic sources | Where (part · chapter) |
|---|---|---|
| Conformity | Asch 1951 | 34 · ch. 1 |
| Obedience | Milgram 1963 | 34 · ch. 3 |
| The Stanford prison study, and its record | Zimbardo 1971 | 34 · ch. 4 |
| Bystanders | Darley & Latané 1968 | 34 · ch. 5 |
| Social facilitation and loafing | Triplett 1898; Zajonc 1965 | 34 · ch. 6 |
| Persuasion and compliance | Petty & Cacioppo; Cialdini | 34 · ch. 8 |
| Attribution and its biases | Heider; Kelley; Ross 1977 | 35 · ch. 2 |
| Cognitive dissonance | Festinger & Carlsmith 1959 | 35 · ch. 3 |
| Attitudes and behaviour | LaPiere 1934; Ajzen 1991 | 35 · ch. 4 |
| Priming and its collapse | Bargh et al. 1996; Doyen 2012 | 35 · ch. 7 |
| Social identity and minimal groups | Tajfel 1971 | 36 · ch. 2 |
| Realistic conflict | Sherif 1954 | 36 · ch. 2 |
| Stereotypes, prejudice, implicit measures | Greenwald 1998 | 36 · ch. 5 |
| Contact | Allport 1954 | 36 · ch. 8 |
| Cooperation and games | Axelrod 1984; Fehr & Gächter 2002 | 37 · ch. 3 |
| Kin selection and reciprocity | Hamilton 1964; Trivers 1971 | 37 · ch. 3 |
| Attraction and relationships |  | 37 · ch. 7 |
| Culture and morality | Haidt 2001; Henrich 2010 | 38 · ch. 7 |

### Personality

| Topic | Classic sources | Where (part · chapter) |
|---|---|---|
| Freud and the psychodynamic tradition | Freud | 33 · ch. 10 |
| Humanistic theories | Rogers; Maslow | 42 · ch. 4 |
| The lexical hypothesis and the Big Five | Allport & Odbert 1936; Goldberg | 33 · ch. 1 |
| The person–situation debate | Mischel 1968 | 33 · ch. 5 |
| Stability and change | Roberts et al. 2006 | 33 · ch. 7 |
| Self-esteem and self-serving bias |  | 35 · ch. 2 |

### Psychological disorders

| Topic | Classic sources | Where (part · chapter) |
|---|---|---|
| Defining disorder; harmful dysfunction | Wakefield 1992 | 39 · ch. 3 |
| Rosenhan and diagnostic reliability | Rosenhan 1973; Spitzer | 39 · hook |
| The biopsychosocial and diathesis–stress models | Engel 1977; Zubin & Spring 1977 | 39 · ch. 3 |
| Classification: DSM and ICD |  | 39 · ch. 2 |
| Anxiety disorders and conditioned fear | Watson & Rayner 1920; Mowrer | 40 · ch. 4 |
| OCD and PTSD |  | 40 · ch. 4 |
| Depression: learned helplessness and Beck's model | Seligman 1967; Beck 1967 | 40 · ch. 6 |
| Bipolar disorder and suicide |  | 40 · ch. 12 |
| Schizophrenia and dopamine | Kraepelin; Bleuler; Carlsson | 41 · ch. 6 |
| Addiction |  | 41 · ch. 9 |
| Autism and ADHD |  | 41 · ch. 10 |
| Eating and personality disorders |  | 39 · ch. 9 |

### Therapy

| Topic | Classic sources | Where (part · chapter) |
|---|---|---|
| Does therapy work? Eysenck's challenge | Eysenck 1952 | 42 · ch. 7 |
| Meta-analysis and the dodo bird | Smith & Glass 1977 | 42 · ch. 4 |
| Client-centred therapy and the alliance | Rogers 1957; Horvath et al. 2011 | 42 · ch. 4 |
| Cognitive and behavioural therapies | Beck; Wolpe | 42 · ch. 4; 40 · ch. 3 |
| Medication and its trials | Kirsch 2008; Cipriani 2018 | 40 · ch. 10 |
| Treatments that harm | Lilienfeld 2007 | 42 · ch. 9 |
| ECT, lobotomy and the body treatments |  | 42 · ch. 7 |

### Psychology at work (the appendices)

| Topic | Classic sources | Where (part · chapter) |
|---|---|---|
| Human factors | Fitts & Jones 1947 | 51 · ch. 2; 52 · ch. 4 |
| Selection and validity | Schmidt & Hunter 1998 | 53 · ch. 8 |
| Work motivation: Herzberg and Vroom | Herzberg 1959; Vroom 1964 | 53 · ch. 10 |
| Leadership | Lewin, Lippitt & White 1939; Bass 1985 | 53 · ch. 12 |
| Learning in school | Dunlosky et al. 2013 | 54 · ch. 5 |
| Nudges | Thaler & Sunstein 2008 | 55 · ch. 5 |
| Eyewitnesses and the law | Wells; Wixted | 56 · ch. 3 |
| Health psychology |  | 57 · ch. 6 |

## 3. Theories, and what the record shows

The theories a textbook names, where the films build or test them, and a one-line verdict. Where a theory is
drawn as a theory card in the films, the verdict there is the same.

| Theory | Who | Where (part · chapter) | What the record shows |
|---|---|---|---|
| Fechner's law: sensation grows as the log of intensity | Fechner 1860 | 11 · ch. 2 | holds where Weber's law holds; Stevens's power law fits magnitude estimates better |
| Signal detection theory | Tanner & Swets 1954; Green & Swets 1966 | 12 · ch. 1 | the standard model of detection; the equal-variance version often fails, the unequal-variance one fits |
| Trichromatic and opponent-process theories of colour | Young, Helmholtz; Hering | 13 · ch. 10 | both right, at different stages |
| Perception as unconscious inference | Helmholtz 1867 | 14 · ch. 5 | the Bayesian observer predicts cue combination well; where priors come from is open |
| Gate control of pain | Melzack & Wall 1965 | 15 · ch. 10 | the idea of spinal gating survives; the original circuit does not |
| Hebb's rule | Hebb 1949 | 6 · ch. 4 | found in LTP and spike timing; plain Hebbian learning is unstable without a normalizer |
| Rescorla–Wagner | Rescorla & Wagner 1972 | 16 · ch. 6 | predicts blocking and overexpectation; fails on latent inhibition and spontaneous recovery |
| Reward prediction error | Schultz, Dayan & Montague 1997 | 17 · ch. 3 | one of the best-supported links between a model and neurons; dopamine does more than signal error |
| Cognitive maps | Tolman 1948 | 17 · ch. 7 | place and grid cells; model-based control |
| Social learning theory | Bandura 1977 | 16 · ch. 12 | imitation is robust; the step from the Bobo doll to media violence is contested |
| Filter and attenuation theories of attention | Broadbent 1958; Treisman 1960 | 18 · ch. 1 | replaced by load and normalization accounts |
| Feature integration theory | Treisman & Gelade 1980 | 18 · ch. 2 | the serial/parallel split did not survive; guided search did |
| The magical number seven | Miller 1956 | 19 · ch. 1 | nearer four chunks (Cowan 2001); slots against resources still argued |
| The multicomponent model of working memory | Baddeley & Hitch 1974 | 19 · ch. 4 | a durable framework; the episodic buffer is loosely specified |
| Levels of processing | Craik & Lockhart 1972 | 20 · ch. 4 | deep processing helps, but 'depth' was never measured independently |
| The temporal context model | Howard & Kahana 2002 | 20 · ch. 8 | fits recency and contiguity in recall |
| Consolidation and two stores | McClelland, McNaughton & O'Reilly 1995 | 21 · ch. 4 | complementary learning systems widely used; the standard model is contested by multiple-trace theory |
| Prototype and exemplar theories | Rosch 1975; Nosofsky 1986 | 22 · ch. 3 | exemplar models fit the classic structures better |
| Shepard's universal law of generalization | Shepard 1987 | 22 · ch. 6 | replicated across species and stimuli |
| Universal grammar against statistical learning | Chomsky 1965; Saffran et al. 1996 | 23 · ch. 7 | open; infants and language models both learn more from statistics than once thought |
| Linguistic relativity | Sapir; Whorf 1956 | 23 · ch. 11 | the strong form failed; weak effects on colour and space are replicated |
| Mental models | Johnson-Laird 1983 | 24 · ch. 2 | explains many errors of deduction; rivals remain |
| Problem solving as search | Newell & Simon 1972 | 24 · ch. 4 | the foundation of cognitive architectures and AI planning |
| The drift-diffusion model | Ratcliff 1978 | 25 · ch. 7 | fits choices and full response-time distributions |
| Expected utility | von Neumann & Morgenstern 1944 | 26 · ch. 2 | violated by Allais and Ellsberg |
| Prospect theory | Kahneman & Tversky 1979 | 26 · ch. 3 | the best simple descriptive model of risky choice; loss aversion is smaller than first reported |
| Heuristics and biases against fast and frugal heuristics | Tversky & Kahneman 1974; Gigerenzer | 26 · ch. 7 | both programmes have well-replicated findings; framing and natural frequencies |
| Dual-process theories (System 1 and 2) | Evans; Kahneman 2011 | 26 · ch. 11 | a useful description; criticized as untestable as a theory |
| Global workspace theory | Baars 1988; Dehaene | 27 · ch. 6 | ignition is found; the 2023 adversarial collaboration challenged some predictions |
| Integrated information theory | Tononi 2004 | 27 · ch. 7 | contested; called pseudoscience by some, defended by others |
| Drive-reduction theory | Hull 1943 | 28 · ch. 1 | cannot explain curiosity or self-stimulation |
| Hierarchy of needs | Maslow 1943 | 28 · ch. 5 | universal needs, yes; a fixed order, no |
| Self-determination theory | Deci & Ryan 1985 | 28 · ch. 5 | broad correlational support; the undermining effect is real, its scope argued |
| Ego depletion | Baumeister et al. 1998 | 28 · ch. 8 | failed in multi-lab replications |
| James–Lange, Cannon–Bard and two-factor theories | James 1884; Cannon 1927; Schachter & Singer 1962 | 29 · ch. 2 | the misattribution study has not replicated cleanly; bodily feedback matters but does not specify the emotion |
| Basic emotions against constructed emotion | Ekman 1972; Barrett 2017 | 29 · ch. 5 | open; recognition across cultures is above chance but far from universal |
| Piaget's stages | Piaget 1952 | 30 · ch. 1 | the sequence holds roughly; infants know more, earlier, than the stages allow |
| Attachment theory | Bowlby 1969; Ainsworth 1978 | 30 · ch. 10 | secure attachment predicts later outcomes modestly |
| Psychosocial stages | Erikson 1950 | 31 · ch. 9 | a framework, little tested directly |
| Moral stages | Kohlberg 1958 | 31 · ch. 9 | the sequence replicates; reasoning predicts behaviour weakly; intuitionist rivals |
| g and the positive manifold | Spearman 1904 | 32 · ch. 2 | the manifold is among psychology's most replicated facts; what produces it is argued (g, mutualism, sampling) |
| The Big Five | Goldberg 1990; McCrae & Costa | 33 · ch. 1 | replicated across languages, with a sixth factor in HEXACO |
| Psychoanalysis | Freud | 33 · ch. 10 | most specific claims untested or unsupported; the unconscious, in a different sense, is central |
| Cognitive dissonance | Festinger 1957 | 35 · ch. 3 | the induced-compliance effect replicates, smaller in multi-lab tests |
| Self-perception theory | Bem 1972 | 35 · ch. 3; 28 · ch. 5 | explains overjustification; coexists with dissonance |
| Social identity theory | Tajfel & Turner 1979 | 36 · ch. 2 | minimal-group favouritism replicates |
| The contact hypothesis | Allport 1954 | 36 · ch. 8 | contact reduces prejudice, with smaller effects in randomized studies |
| Kin selection and reciprocal altruism | Hamilton 1964; Trivers 1971 | 37 · ch. 3 | the foundations of evolutionary accounts of cooperation |
| Moral foundations theory | Haidt & Graham 2007 | 38 · ch. 7 | the measures replicate partly; the five-factor structure is contested |
| The transtheoretical model (stages of change) | Prochaska & DiClemente 1983 | 57 · ch. 6 | stage-matched interventions do no better than others |
| Transformational leadership | Burns 1978; Bass 1985; critique: van Knippenberg & Sitkin 2013 | 53 · ch. 12 | correlates with outcomes, but the questionnaires mix leadership with its effects |
| The biopsychosocial model | Engel 1977 | 39 · ch. 3 | a framework rather than a testable theory |
| Symptom networks | Borsboom 2008 | 39 · ch. 8 | a productive alternative to latent disorders; network estimates replicate unevenly |
| Learned helplessness | Seligman & Maier 1967 | 40 · ch. 7 | revised by its authors in 2016: passivity is the default, control is learned |
| Beck's cognitive model of depression | Beck 1967 | 40 · ch. 6 | the basis of CBT; negative thinking is as much a symptom as a cause |
| The monoamine hypothesis | Schildkraut 1965 | 40 · ch. 9 | the simple serotonin-deficit story is not supported |
| The dopamine hypothesis of schizophrenia | Carlsson; Howes & Kapur 2009 | 41 · ch. 3 | presynaptic dopamine excess is supported; aberrant salience links it to symptoms |
| Predictive coding and the free-energy principle | Rao & Ballard 1999; Friston 2010 | 58 · ch. 8 | predictive coding is testable and partly supported; the free-energy principle is a framework |
| Efficient coding | Barlow 1961 | 58 · ch. 2 | sparse coding reproduces V1 receptive fields |

## 4. The classic studies

The experiments the textbooks retell, and where the films show them; most have a Ledger row with what happened when
they were run again.

| Study | Who | Where (part · chapter) |
|---|---|---|
| Clever Hans | Pfungst 1907 | 2 · ch. 1 |
| Ebbinghaus's savings | Ebbinghaus 1885 | 20 · ch. 1 |
| Little Albert | Watson & Rayner 1920 | 16 · ch. 2 |
| Bartlett's War of the Ghosts | Bartlett 1932 | 21 · ch. 7 |
| Stroop interference | Stroop 1935 | 18 · ch. 8 |
| Tolman's rats | Tolman & Honzik 1930 | 17 · ch. 7 |
| Asch's lines | Asch 1951 | 34 · ch. 1 |
| Robbers Cave | Sherif et al. 1954/1961 | 36 · ch. 2 |
| Olds and Milner's self-stimulating rat | Olds & Milner 1954 | 28 · ch. 4 |
| Miller's magical number | Miller 1956 | 19 · ch. 1 |
| Harlow's monkeys | Harlow 1958 | 30 · ch. 10 |
| Festinger and Carlsmith's one dollar | Festinger & Carlsmith 1959 | 35 · ch. 3 |
| Sperling's partial report | Sperling 1960 | 19 · ch. 2 |
| Bandura's Bobo doll | Bandura, Ross & Ross 1961 | 16 · ch. 12 |
| Milgram's obedience | Milgram 1963 | 34 · ch. 3 |
| Garcia's taste aversion | Garcia & Koelling 1966 | 16 · ch. 12 |
| Sternberg's memory scanning | Sternberg 1966 | 19 · ch. 5 |
| Seligman's dogs | Seligman & Maier 1967 | 40 · ch. 7 |
| Darley and Latané's bystanders | Darley & Latané 1968 | 34 · ch. 5 |
| The marshmallow test | Mischel et al. 1972 | 28 · ch. 10 |
| Shepard and Metzler's rotations | Shepard & Metzler 1971 | 24 · ch. 9 |
| Tajfel's minimal groups | Tajfel 1971 | 36 · ch. 2 |
| The Stanford prison study | Haney, Banks & Zimbardo 1973 | 34 · ch. 4 |
| Rosenhan's pseudopatients | Rosenhan 1973 | 39 · hook |
| Loftus and Palmer's car crash | Loftus & Palmer 1974 | 21 · hook |
| Wason's selection task | Wason 1966 | 24 · hook |
| The Asian disease problem | Tversky & Kahneman 1981 | 26 · ch. 3 |
| Libet's clock | Libet et al. 1983 | 27 · ch. 10 |
| Strack's pens | Strack, Martin & Stepper 1988 | 29 · ch. 6 |
| The DRM lists | Roediger & McDermott 1995 | 21 · ch. 8 |
| Schultz's dopamine neurons | Schultz, Dayan & Montague 1997 | 17 · ch. 3 |
| The invisible gorilla | Simons & Chabris 1999 | 18 · ch. 6 |
| Ego depletion's 23 laboratories | Hagger et al. 2016 | 28 · ch. 9 |
| Feeling the future | Bem 2011 | 4 · ch. 1 |
| The dead salmon | Bennett et al. 2009/2010 | 8 · ch. 7 |
| One hundred replications | Open Science Collaboration 2015 | 4 · ch. 9 |
| The Bucharest Early Intervention Project | Nelson et al. 2007 | 31 · ch. 5 |
| Many Analysts | Silberzahn et al. 2018 | 50 · ch. 10 |

## 5. Papers, part by part

Each part's README ends with its own reading: a **Sources** section listing every book, paper and dataset the
part draws on, with full references, and a **Ledger** table of the findings it enters, each with its original study
and the replications that followed (the full record, with sources and the date checked, is in
`explainer/psychology/ledger.py`). The parts' READMEs are `videos/psychology/psychN/README.md`, N = 1 … 62.

## 6. What the series does not cover in depth

A degree is also defined by what it leaves out. These topics appear in introductory or upper-level textbooks and
are touched only in passing here, if at all:

| Topic | Where it is touched | Why it is not a chapter |
|---|---|---|
| Sexuality and sexual development | 33 (gender differences), 37 (attraction, mate preferences) | the series has no part on sexual behaviour; its science is mostly survey-based and outside the series' model-and-data spine |
| Dissociative, somatic and sexual disorders | 39 (the map of the manual) | named on the map of the manual; the series treats in depth the disorders it can model (fear, mood, psychosis, addiction) |
| Eating and personality disorders | 39 (the map of the manual), 42 (DBT) | described with their record, not modelled |
| Positive psychology (PERMA, flow, strengths) | 29 (happiness), 47 (experience sampling) | its strongest results are the well-being findings of Part 29 |
| Psychology of religion, environmental, community, sport and forensic psychology beyond the courtroom | 38, 55, 56 | applied fields outside the series' acts |
| Psychology's careers and professions | 62 (the roles) | told as the roles a graduate can take, not as a careers guide |
| Parapsychology | 4 (Bem's *Feeling the Future*) | the series uses it as the case that started the replication crisis |
