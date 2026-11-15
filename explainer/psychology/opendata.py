"""Open trial-level datasets of *Psychology, Built*: fetched from their public home once, cached, checksummed.

Most of the Archive (:mod:`explainer.psychology.archive`) holds published summary numbers.  A few parts fit models
to raw trial-level data that its authors have shared; that data is not copied into the repository.  It is
downloaded on first use into ``.cache/psychology_data/`` (git-ignored) and checked against the SHA-256 recorded
here, so a changed file is noticed rather than silently fitted.  Each dataset also has a row in the Archive's
``SOURCES.md`` saying where it comes from and what was checked.

* :func:`bays_2009`: continuous report of colour, set sizes 1, 2, 4 and 6, sample durations 100, 500 and 2,000 ms,
  12 observers, 7,271 trials (Bays, Catalao and Husain, *Journal of Vision* 9(10):7, 2009); shared by Paul Bays on
  the Open Science Framework (osf.io/c2yx5).  Part 19.
* :func:`peers_free_recall`: immediate free recall of 16-word lists, 126 people and 3,528 lists, from the Penn
  Electrophysiology of Encoding and Retrieval Study (Kahana lab), in the subset packaged with the psifr analysis
  package (a CSV inside its wheel on PyPI; both the wheel and the CSV are checked).  Part 20.
* :func:`murre_2021`: Murre's direct replication of Godden and Baddeley's divers, sixteen divers' words recalled in
  four conditions, from the workbook he shared on the Open Science Framework (osf.io/q2vjk).  Part 20.

* :func:`choices13k`: 13,006 risky choice problems, each answered by about 16 people (Peterson et al., *Science*
  372, 2021), from github.com/jcpeterson/choices13k at a fixed commit.  Part 26.

* :func:`ego_depletion_rrr`: the ego-depletion Registered Replication Report's table of 23 laboratories and
  the original study (Hagger et al. 2016), from osf.io/jymhe.  Part 28.

* :func:`faces_1962` and :func:`coles_2019`: Abelson and Sermat's facial expressions with Engen's scales, and
  the facial-feedback meta-analysis table (Coles, Larsen and Lench 2019).  Part 29.

Nothing here imports manim.
"""

from __future__ import annotations

import hashlib
import time
import urllib.request
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / ".cache" / "psychology_data"
UA = {"User-Agent": "explainer-videos/psychology (education)"}

SOURCES = {
    "bays_2009": {
        "url": "https://osf.io/download/dfhys/",
        "page": "https://osf.io/c2yx5/",
        "file": "bays_2009_Exp_data.mat",
        "sha256": "467d479936f8a06f6fe2a5ca54d51a1907df00fc66169b8e4a21121d91e6dd9e",
    },
    "peers_free_recall": {
        # psifr 0.10.1 on PyPI (GPL-3.0-or-later) ships a subset of PEERS immediate free recall as a CSV
        "url": "https://files.pythonhosted.org/packages/d1/d2/f40f44465ef714a70715895cb1ae5ca5c6826133d5cbe091c1bb1ec49a45/"
               "psifr-0.10.1-py3-none-any.whl",
        "page": "https://pypi.org/project/psifr/0.10.1/",
        "file": "psifr-0.10.1-py3-none-any.whl",
        "sha256": "cd22befa61d5d6cbcb3fef970d5c1f7eda5b9acd94618cac08095dc9a271f562",
        "member": "psifr/data/peers_notask.csv",
        "member_sha256": "592f67aae9f8f9bd45a019727c7a498579017d0b7ebdf45666a647a432ce1684",
    },
    "murre_2021": {
        # J. M. J. Murre, Royal Society Open Science 8 (2021) 200724; the workbook at osf.io/q2vjk (component 5xas9)
        "url": "https://osf.io/download/j37sh/",
        "page": "https://osf.io/q2vjk/",
        "file": "murre_2021.xlsx",
        "sha256": "a15c0aaab08d89ad706d692c3201d95c3e24ec6f5afa156b0097c08db5515ce5",
    },
    "overshadowing_rrr1": {
        # V. K. Alogna et al., Perspectives on Psychological Science 9 (2014) 556-578; osf.io/ybeur (component xui4e)
        "url": "https://osf.io/download/dv5ei/",
        "page": "https://osf.io/ybeur/",
        "file": "overshadowing_rrr1.xlsx",
        "sha256": "562b471251e65102694b0449adf71bb8c588deeeb5f09664fb824894c71295db",
    },
    "overshadowing_rrr2": {
        "url": "https://osf.io/download/dy6at/",
        "page": "https://osf.io/ybeur/",
        "file": "overshadowing_rrr2.xlsx",
        "sha256": "81be7ccd1ae7973fb223c745050fc3fc3c551705366d158542067bffde44b775",
    },
    # Part 24: Ganis and Kievit's mental rotation validation data (figshare 1045385, CC BY 4.0), and Ragni's 2016
    # syllogism data as packaged in the CCOBRA benchmark (MIT licence) at a fixed commit
    "ganis_kievit_2015": {
        "url": "https://ndownloader.figshare.com/files/3702010",
        "page": "https://doi.org/10.6084/m9.figshare.1045385",
        "file": "ganis_kievit_2015_behavioural_data.zip",
        "sha256": "3b56dde3defc36d54c85b671f83ade2f7ded685b326be973583ad115bb994e03",
        "licence": "CC BY 4.0",
    },
    "ragni_2016": {
        "url": "https://raw.githubusercontent.com/CognitiveComputationLab/ccobra/fa6e8aa8d0b8cde486b0c6f108d87d7c3e64a40b/benchmarks/syllogistic/data/Ragni2016.csv",
        "page": "https://github.com/CognitiveComputationLab/ccobra",
        "file": "ccobra_ragni2016.csv",
        "sha256": "9cb59c33816727a173d3eed202e3f663ddc3e6ae294bc4da705ada04113efd18",
        "licence": "MIT",
    },
    # Part 25: Wagenmakers et al.'s (2008) speed-accuracy lexical decisions and Ratcliff and Rouder's (1998)
    # brightness discrimination, as packaged in the R package rtdists
    'speed_acc_2008': {'url': 'https://cran.r-project.org/src/contrib/rtdists_0.12-0.tar.gz', 'urls': ['https://cran.r-project.org/src/contrib/rtdists_0.12-0.tar.gz', 'https://cran.r-project.org/src/contrib/Archive/rtdists/rtdists_0.12-0.tar.gz'], 'page': 'https://cran.r-project.org/package=rtdists', 'file': 'rtdists_0.12-0.tar.gz', 'sha256': 'cf9ff4638cee0e8f412c02b950616eb9b6544a58654e1ae1d0dd264f1c76d3a1', 'licence': 'GPL (>= 3)', 'member': 'rtdists/data/speed_acc.RData', 'member_sha256': '991429ecb0a6711dd32422ee4cff9eb7d3010c9de9434387aa36b8788e573f62'},
    'rr98': {'url': 'https://cran.r-project.org/src/contrib/rtdists_0.12-0.tar.gz', 'urls': ['https://cran.r-project.org/src/contrib/rtdists_0.12-0.tar.gz', 'https://cran.r-project.org/src/contrib/Archive/rtdists/rtdists_0.12-0.tar.gz'], 'page': 'https://cran.r-project.org/package=rtdists', 'file': 'rtdists_0.12-0.tar.gz', 'sha256': 'cf9ff4638cee0e8f412c02b950616eb9b6544a58654e1ae1d0dd264f1c76d3a1', 'licence': 'GPL (>= 3)', 'member': 'rtdists/data/rr98.rda', 'member_sha256': '91ff255d3cb557fc98692517163eb5b9615d4e6e05e98992b3a0d164945724d8'},
    # Part 23: the Natural Stories corpus (Futrell et al., Language Resources and Evaluation 55 (2021) 63-77),
    # github.com/languageMIT/naturalstories at a fixed commit; no licence is stated, so it is fetched, never
    # redistributed
    "naturalstories_words": {
        "url": "https://raw.githubusercontent.com/languageMIT/naturalstories/4700daad696e942f5aba23c957a7423d0de66612/naturalstories_RTS/processed_wordinfo.tsv",
        "page": "https://github.com/languageMIT/naturalstories",
        "file": "naturalstories_processed_wordinfo.tsv",
        "sha256": "047d2a0b84eff99d90535d1517f7fa7d466b81fbd60e990f2f08caac04d8aa56",
    },
    # Part 26: choices13k (Peterson, Bourgin, Agrawal, Reichman and Griffiths, Science 372 (2021) 1209-1214),
    # github.com/jcpeterson/choices13k at a fixed commit; no licence is stated, so it is fetched, never redistributed
    "choices13k_selections": {
        "url": "https://raw.githubusercontent.com/jcpeterson/choices13k/821ae7e88386b508ebb46fae76fac63cb62ec876/c13k_selections.csv",
        "page": "https://github.com/jcpeterson/choices13k",
        "file": "choices13k_selections.csv",
        "sha256": "e21941718b83fd97a5997545489a66ce27bec3b3f62700a0774fb5f997fea5c7",
    },
    "choices13k_problems": {
        "url": "https://raw.githubusercontent.com/jcpeterson/choices13k/821ae7e88386b508ebb46fae76fac63cb62ec876/c13k_problems.json",
        "page": "https://github.com/jcpeterson/choices13k",
        "file": "choices13k_problems.json",
        "sha256": "c6bdb0ae7e0d0ca127b649b4996a7a49b3d0c4c43e5f9a851677fe4527276632",
    },
    # Part 28: the ego-depletion Registered Replication Report (Hagger et al., Perspectives on Psychological Science
    # 11 (2016) 546-573), its per-laboratory table of reaction-time variability at osf.io/jymhe (component kh85v); no
    # licence is stated, so it is fetched, never redistributed
    "ego_depletion_rrr": {
        "url": "https://osf.io/download/v3rdw/",
        "page": "https://osf.io/jymhe/",
        "file": "ego_depletion_rrr_RTV.csv",
        "sha256": "fcdb1a36e15e8e52956fb4997ca10ac7c0e9ae6053e1b32d8b5c7291fdae47b1",
    },
    # Part 30: ManyBabies 1's lab-by-age effect sizes for the infant-directed speech preference (psymetadata)
    'manybabies2020': {'url': 'https://cran.r-project.org/src/contrib/psymetadata_1.0.1.tar.gz', 'urls': ['https://cran.r-project.org/src/contrib/psymetadata_1.0.1.tar.gz', 'https://cran.r-project.org/src/contrib/Archive/psymetadata/psymetadata_1.0.1.tar.gz'], 'page': 'https://cran.r-project.org/package=psymetadata', 'file': 'psymetadata_1.0.1.tar.gz', 'sha256': '9b5f0cb8ab98e64fb7807483bb74fdaf16c18b010c081f0f93308c1da10b2bd4', 'licence': 'GPL (>= 2)', 'member': 'psymetadata/data/manybabies2020.rda', 'member_sha256': '1db921862cbc8e1701fb314d8e8262dbb84b7920b60172358b8221c53048dd22'},
    # Part 29: Abelson and Sermat's facial expressions (smacof), and Coles, Larsen and Lench's facial-feedback
    # meta-analysis table (psymetadata)
    'faceexp': {'url': 'https://cran.r-project.org/src/contrib/smacof_2.1-7.tar.gz', 'urls': ['https://cran.r-project.org/src/contrib/smacof_2.1-7.tar.gz', 'https://cran.r-project.org/src/contrib/Archive/smacof/smacof_2.1-7.tar.gz'], 'page': 'https://cran.r-project.org/package=smacof', 'file': 'smacof_2.1-7.tar.gz', 'sha256': '7a965a4e06a2ef1e01e37ae7ce6a55f2e745d4aaf99eb1c592b3d835bac9493a', 'licence': 'GPL-3', 'member': 'smacof/data/FaceExp.rda', 'member_sha256': 'b104ed979ec2e0910ba1a562f784e0054aaa35ac99cc816694c5adef0b488372'},
    'facescale': {'url': 'https://cran.r-project.org/src/contrib/smacof_2.1-7.tar.gz', 'urls': ['https://cran.r-project.org/src/contrib/smacof_2.1-7.tar.gz', 'https://cran.r-project.org/src/contrib/Archive/smacof/smacof_2.1-7.tar.gz'], 'page': 'https://cran.r-project.org/package=smacof', 'file': 'smacof_2.1-7.tar.gz', 'sha256': '7a965a4e06a2ef1e01e37ae7ce6a55f2e745d4aaf99eb1c592b3d835bac9493a', 'licence': 'GPL-3', 'member': 'smacof/data/FaceScale.rda', 'member_sha256': '088989fe9b5445fc576bb27755456024ca19078342df9b86cc868ecd8e529653'},
    'coles2019': {'url': 'https://cran.r-project.org/src/contrib/psymetadata_1.0.1.tar.gz', 'urls': ['https://cran.r-project.org/src/contrib/psymetadata_1.0.1.tar.gz', 'https://cran.r-project.org/src/contrib/Archive/psymetadata/psymetadata_1.0.1.tar.gz'], 'page': 'https://cran.r-project.org/package=psymetadata', 'file': 'psymetadata_1.0.1.tar.gz', 'sha256': '9b5f0cb8ab98e64fb7807483bb74fdaf16c18b010c081f0f93308c1da10b2bd4', 'licence': 'GPL (>= 2)', 'member': 'psymetadata/data/coles2019.rda', 'member_sha256': '93de0be5403efd82d2ad0eb77e2cb30d8c125fba953e2fb347b44c2a1b281b2c'},
    # Part 22: data inside CRAN source packages (catlearn, smacof, janeaustenr), read as data by rdata.py
    'nosof94': {'url': 'https://cran.r-project.org/src/contrib/catlearn_1.1.tar.gz', 'urls': ['https://cran.r-project.org/src/contrib/catlearn_1.1.tar.gz', 'https://cran.r-project.org/src/contrib/Archive/catlearn/catlearn_1.1.tar.gz'], 'page': 'https://cran.r-project.org/package=catlearn', 'file': 'catlearn_1.1.tar.gz', 'sha256': '6ba6593d615586d3341088f1482d1d0fc3f1eb5f24ebcdb5885cb3f755efdcb6', 'licence': 'GPL (>= 2)', 'member': 'catlearn/data/nosof94.RData', 'member_sha256': '4c9959b80d0311b5db13942665948a34ce5eee6559eb4ca8e5b66c10462670a0'},
    'homa76': {'url': 'https://cran.r-project.org/src/contrib/catlearn_1.1.tar.gz', 'urls': ['https://cran.r-project.org/src/contrib/catlearn_1.1.tar.gz', 'https://cran.r-project.org/src/contrib/Archive/catlearn/catlearn_1.1.tar.gz'], 'page': 'https://cran.r-project.org/package=catlearn', 'file': 'catlearn_1.1.tar.gz', 'sha256': '6ba6593d615586d3341088f1482d1d0fc3f1eb5f24ebcdb5885cb3f755efdcb6', 'licence': 'GPL (>= 2)', 'member': 'catlearn/data/homa76.RData', 'member_sha256': '99f1af2ea059d7e97c93bc2f1b821d38be2a4d51a7628b7be7d1456ea39d4e24'},
    'ekman_1954': {'url': 'https://cran.r-project.org/src/contrib/smacof_2.1-7.tar.gz', 'urls': ['https://cran.r-project.org/src/contrib/smacof_2.1-7.tar.gz', 'https://cran.r-project.org/src/contrib/Archive/smacof/smacof_2.1-7.tar.gz'], 'page': 'https://cran.r-project.org/package=smacof', 'file': 'smacof_2.1-7.tar.gz', 'sha256': '7a965a4e06a2ef1e01e37ae7ce6a55f2e745d4aaf99eb1c592b3d835bac9493a', 'licence': 'GPL-3', 'member': 'smacof/data/ekman.rda', 'member_sha256': '0d03901d8212bd1e6907a35c21ccc78e1701e23162025fd53fe3b04896ef418a'},
    'rothkopf_1957': {'url': 'https://cran.r-project.org/src/contrib/smacof_2.1-7.tar.gz', 'urls': ['https://cran.r-project.org/src/contrib/smacof_2.1-7.tar.gz', 'https://cran.r-project.org/src/contrib/Archive/smacof/smacof_2.1-7.tar.gz'], 'page': 'https://cran.r-project.org/package=smacof', 'file': 'smacof_2.1-7.tar.gz', 'sha256': '7a965a4e06a2ef1e01e37ae7ce6a55f2e745d4aaf99eb1c592b3d835bac9493a', 'licence': 'GPL-3', 'member': 'smacof/data/morse2.rda', 'member_sha256': '4c19c884caac229dae621d0a345e15750b1ad1aa7e2ee8337f77285e315ee06b'},
    'austen_emma': {'url': 'https://cran.r-project.org/src/contrib/janeaustenr_1.0.0.tar.gz', 'urls': ['https://cran.r-project.org/src/contrib/janeaustenr_1.0.0.tar.gz', 'https://cran.r-project.org/src/contrib/Archive/janeaustenr/janeaustenr_1.0.0.tar.gz'], 'page': 'https://cran.r-project.org/package=janeaustenr', 'file': 'janeaustenr_1.0.0.tar.gz', 'sha256': 'b4c32ee1395ee4a8efe714c535c0fe578b0dbf5f3bb85b41fa5cc87569b8e8aa', 'licence': 'MIT', 'member': 'janeaustenr/data/emma.rda', 'member_sha256': '65594dab7e37779e5b36c8551886d35cef2149fb442793e49b9879a4287f33f2'},
    'austen_mansfieldpark': {'url': 'https://cran.r-project.org/src/contrib/janeaustenr_1.0.0.tar.gz', 'urls': ['https://cran.r-project.org/src/contrib/janeaustenr_1.0.0.tar.gz', 'https://cran.r-project.org/src/contrib/Archive/janeaustenr/janeaustenr_1.0.0.tar.gz'], 'page': 'https://cran.r-project.org/package=janeaustenr', 'file': 'janeaustenr_1.0.0.tar.gz', 'sha256': 'b4c32ee1395ee4a8efe714c535c0fe578b0dbf5f3bb85b41fa5cc87569b8e8aa', 'licence': 'MIT', 'member': 'janeaustenr/data/mansfieldpark.rda', 'member_sha256': 'c5903def1e79b8494097f9bc5c52d0fb173084450432c10dfd9647c0d3bd3e2d'},
    'austen_northangerabbey': {'url': 'https://cran.r-project.org/src/contrib/janeaustenr_1.0.0.tar.gz', 'urls': ['https://cran.r-project.org/src/contrib/janeaustenr_1.0.0.tar.gz', 'https://cran.r-project.org/src/contrib/Archive/janeaustenr/janeaustenr_1.0.0.tar.gz'], 'page': 'https://cran.r-project.org/package=janeaustenr', 'file': 'janeaustenr_1.0.0.tar.gz', 'sha256': 'b4c32ee1395ee4a8efe714c535c0fe578b0dbf5f3bb85b41fa5cc87569b8e8aa', 'licence': 'MIT', 'member': 'janeaustenr/data/northangerabbey.rda', 'member_sha256': 'd4b8163fba67575e3125f532752baf7d86bf25dbf975aa596b92d3868cab9519'},
    'austen_persuasion': {'url': 'https://cran.r-project.org/src/contrib/janeaustenr_1.0.0.tar.gz', 'urls': ['https://cran.r-project.org/src/contrib/janeaustenr_1.0.0.tar.gz', 'https://cran.r-project.org/src/contrib/Archive/janeaustenr/janeaustenr_1.0.0.tar.gz'], 'page': 'https://cran.r-project.org/package=janeaustenr', 'file': 'janeaustenr_1.0.0.tar.gz', 'sha256': 'b4c32ee1395ee4a8efe714c535c0fe578b0dbf5f3bb85b41fa5cc87569b8e8aa', 'licence': 'MIT', 'member': 'janeaustenr/data/persuasion.rda', 'member_sha256': '758a227662b5f94785199b5c80a3d23533b397d476ddc43289181fb556d945a0'},
    'austen_prideprejudice': {'url': 'https://cran.r-project.org/src/contrib/janeaustenr_1.0.0.tar.gz', 'urls': ['https://cran.r-project.org/src/contrib/janeaustenr_1.0.0.tar.gz', 'https://cran.r-project.org/src/contrib/Archive/janeaustenr/janeaustenr_1.0.0.tar.gz'], 'page': 'https://cran.r-project.org/package=janeaustenr', 'file': 'janeaustenr_1.0.0.tar.gz', 'sha256': 'b4c32ee1395ee4a8efe714c535c0fe578b0dbf5f3bb85b41fa5cc87569b8e8aa', 'licence': 'MIT', 'member': 'janeaustenr/data/prideprejudice.rda', 'member_sha256': '9704d3d55b0e59f3e9f6d6032d192200f925ec7b2ba4f1dba402f179578ae3c9'},
    'austen_sensesensibility': {'url': 'https://cran.r-project.org/src/contrib/janeaustenr_1.0.0.tar.gz', 'urls': ['https://cran.r-project.org/src/contrib/janeaustenr_1.0.0.tar.gz', 'https://cran.r-project.org/src/contrib/Archive/janeaustenr/janeaustenr_1.0.0.tar.gz'], 'page': 'https://cran.r-project.org/package=janeaustenr', 'file': 'janeaustenr_1.0.0.tar.gz', 'sha256': 'b4c32ee1395ee4a8efe714c535c0fe578b0dbf5f3bb85b41fa5cc87569b8e8aa', 'licence': 'MIT', 'member': 'janeaustenr/data/sensesensibility.rda', 'member_sha256': '0fef9c0d7598e30a0c09e866e3db4117b4a47d31cbc28cc8783eb4abdad03593'},
}


def _get(url: str, retries: int = 4, timeout: int = 90) -> bytes:
    err = None
    for k in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                return r.read()
        except Exception as e:  # network errors and rate limits: back off and retry
            err = e
            time.sleep(min(2 ** k, 20))
    raise RuntimeError(f"failed to fetch {url}: {err}")


def path(key: str) -> Path:
    """The local copy of dataset ``key``, downloaded and checked on first use."""
    src = SOURCES[key]
    p = CACHE / src["file"]
    if not p.exists():
        raw, err = None, None
        for url in src.get("urls", [src["url"]]):
            try:
                raw = _get(url)
                break
            except Exception as e:  # the next mirror
                err = e
        if raw is None:
            raise RuntimeError(f"{key}: no source answered: {err}")
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_name(p.name + ".tmp")
        tmp.write_bytes(raw)
        tmp.replace(p)
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    if h != src["sha256"]:
        raise RuntimeError(f"{key}: the downloaded file's SHA-256 {h[:12]} is not the recorded "
                           f"{src['sha256'][:12]}; the source changed, so check it at {src['page']}")
    return p


def available(key: str) -> bool:
    """Whether dataset ``key`` is cached or can be fetched now."""
    try:
        path(key)
        return True
    except Exception:
        return False


def bays_2009() -> dict:
    """Bays, Catalao and Husain (2009), one entry per trial.

    ``subject`` (1-12), ``set_size`` (1, 2, 4, 6), ``duration`` (sample display, ms: 100, 500, 2000), ``target`` and
    ``response`` (colour angles, radians), ``error`` (response minus target, wrapped to [-pi, pi)), ``nontarget``
    (trials x 5, the other items' colours, NaN where the display had fewer) and ``nontarget_error`` (response minus
    each non-target, wrapped)."""
    from scipy.io import loadmat

    m = loadmat(path("bays_2009"))
    nt = np.asarray(m["nontarget"], float)
    resp = m["response"].ravel().astype(float)
    return {
        "subject": m["subject"].ravel().astype(int),
        "set_size": m["n_items"].ravel().astype(int),
        "duration": m["delay"].ravel().astype(int),
        "target": m["target"].ravel().astype(float),
        "response": resp,
        "error": m["error"].ravel().astype(float),
        "nontarget": nt,
        "nontarget_error": (resp[:, None] - nt + np.pi) % (2 * np.pi) - np.pi,
    }


def member_path(key: str):
    """The local copy of a file inside an archive source, extracted and checked on first use."""
    import zipfile

    src = SOURCES[key]
    out = CACHE / (key + "_" + Path(src["member"]).name)
    if not out.exists():
        archive_path = path(key)
        if str(archive_path).endswith((".tar.gz", ".tgz")):
            import tarfile

            with tarfile.open(archive_path, "r:gz") as t:  # one member read as bytes; nothing is extracted to disk
                raw = t.extractfile(src["member"]).read()
        else:
            with zipfile.ZipFile(archive_path) as z:
                raw = z.read(src["member"])
        tmp = out.with_name(out.name + ".tmp")
        tmp.write_bytes(raw)
        tmp.replace(out)
    h = hashlib.sha256(out.read_bytes()).hexdigest()
    if h != src["member_sha256"]:
        raise RuntimeError(f"{key}: {src['member']} has SHA-256 {h[:12]}, not the recorded {src['member_sha256'][:12]}")
    return out


def peers_free_recall() -> dict:
    """Immediate free recall of 16-word lists from the Penn Electrophysiology of Encoding and Retrieval Study
    (PEERS, Kahana lab), as packaged with psifr: 126 subjects, 3,528 lists.

    ``subject`` and ``session`` per list; ``words`` (lists x 16) in study order; ``recalls`` (lists x 24) of serial
    positions 1..16 in output order, 0 for an intrusion and for padding; ``intrusions`` per list."""
    import csv

    rows = list(csv.DictReader(open(member_path("peers_free_recall"), newline="")))
    study, rec = {}, {}
    for r in rows:
        k = (int(r["subject"]), int(r["session"]), int(r["list"]))
        if r["trial_type"] == "study":
            study.setdefault(k, {})[r["item"]] = int(r["position"])
        else:
            rec.setdefault(k, []).append(r["item"])
    keys = sorted(study)
    n = 16
    words = np.empty((len(keys), n), dtype=object)
    recalls = np.zeros((len(keys), 24), int)
    intr = np.zeros(len(keys), int)
    for i, k in enumerate(keys):
        for w, p in study[k].items():
            words[i, p - 1] = w
        seq = [study[k].get(w, 0) for w in rec.get(k, [])][:24]
        recalls[i, :len(seq)] = seq
        intr[i] = sum(1 for p in seq if p == 0)
    return {"subject": np.array([k[0] for k in keys]), "session": np.array([k[1] for k in keys]), "words": words,
            "recalls": recalls, "intrusions": intr, "list_length": n}


def _xlsx_cells(file, sheet: int = 1) -> dict:
    """The values of one worksheet of an .xlsx file, by cell reference ("B18" -> "10"), read with the standard
    library (an .xlsx file is a zip of XML; nothing in it is executed)."""
    import xml.etree.ElementTree as ET
    import zipfile

    m = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    with zipfile.ZipFile(file) as z:
        shared = [''.join(t.text or "" for t in si.iter(m + "t"))
                  for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(m + "si")]
        root = ET.fromstring(z.read(f"xl/worksheets/sheet{sheet}.xml"))
    out = {}
    for c in root.iter(m + "c"):
        v = c.find(m + "v")
        if v is not None:
            out[c.get("r")] = shared[int(v.text)] if c.get("t") == "s" else v.text
    return out


def murre_2021() -> dict:
    """Murre's replication of Godden and Baddeley: sixteen divers, each learning a list of 36 words on land or
    underwater and recalling it four minutes later on land or underwater (all four combinations, in a Graeco-Latin
    square).  ``scores`` is (16, 4): words recalled in the order DD, DW, WD, WW (learning place first; D = dry,
    W = wet), one row per diver, taken from the 'Analysis' sheet of the published workbook."""
    cells = _xlsx_cells(path("murre_2021"), 1)
    col = lambda c, r0: [float(cells[f"{c}{r}"]) for r in range(r0, r0 + 16)]  # noqa: E731
    dd, wd = col("B", 18), col("C", 18)  # recall on land: learned on land, learned underwater
    dw, ww = col("B", 34), col("C", 34)  # recall underwater
    return {"scores": np.array([dd, dw, wd, ww]).T, "conditions": ("DD", "DW", "WD", "WW"), "words": 36}


def overshadowing_rrr(study: int) -> dict:
    """The verbal-overshadowing Registered Replication Report (Alogna et al. 2014), per lab.  Study 1 had the
    description straight after the film; study 2 had it after a 20-minute filler task, as in the original Study 1.
    ``verbal`` and ``control`` are (labs, 2) arrays of (correct identifications, people included); ``original`` and
    ``online`` are the same pairs for the original study and the online (MTurk) sample, which the report kept out of
    its meta-analysis.  ``labs`` names the first author of each lab."""
    cells = _xlsx_cells(path(f"overshadowing_rrr{study}"), 1)
    rows = sorted({int("".join(ch for ch in ref if ch.isdigit())) for ref in cells})
    out = {"verbal": [], "control": [], "labs": []}
    for r in rows:
        if not str(cells.get(f"H{r}", "")).isdigit():
            continue
        v = (int(cells[f"I{r}"]), int(cells[f"H{r}"]))
        c = (int(cells[f"Q{r}"]), int(cells[f"P{r}"]))
        who = cells[f"A{r}"]
        if who.startswith("ORIGINAL"):
            out["original"] = np.array([v, c])
        elif who.startswith("ONLINE"):
            out["online"] = np.array([v, c])
        else:
            out["verbal"].append(v)
            out["control"].append(c)
            out["labs"].append(who.split(",")[0].strip())
    out["verbal"], out["control"] = np.array(out["verbal"]), np.array(out["control"])
    return out


def _rframe(key) -> dict:
    """A data frame saved in an R data file, as {column: numpy array}; factors become their labels."""
    from explainer.psychology import rdata

    obj = rdata.load(member_path(key))[0][1]
    out = {}
    for name, col in zip(obj["attrs"]["names"]["value"], obj["value"]):
        v = col["value"]
        lev = col["attrs"].get("levels", {}).get("value") if col["attrs"] else None
        out[name] = np.array([lev[i - 1] if (lev and i is not None) else i for i in v], dtype=object if lev else float)
    return out


def nosof94() -> dict:
    """Nosofsky, Gluck, Palmeri, McKinley and Glauthier (1994): the mean probability of error in each of the first 16
    blocks of 16 trials for the six problems of Shepard, Hovland and Jenkins (1961), 40 learners per problem, as
    packaged in the R package catlearn.  ``error`` is (6 types, 16 blocks)."""
    d = _rframe("nosof94")
    err = np.zeros((6, 16))
    for t, b, e in zip(d["type"], d["block"], d["error"]):
        err[int(t) - 1, int(b) - 1] = e
    return {"error": err}


def homa76() -> dict:
    """Homa and Vosburgh (1976), the immediate test: probability correct by stimulus type (prototype, low, medium
    and high distortions, old items, random patterns), training condition and category size, from catlearn."""
    d = _rframe("homa76")
    keep = d["phase"] == "imm"
    return {k: v[keep] for k, v in d.items()}


def ekman_1954() -> dict:
    """Ekman (1954): similarity (0 to 1) of 14 colours from 434 to 674 nm, rated by 31 people, from smacof."""
    from explainer.psychology import rdata

    obj = rdata.load(member_path("ekman_1954"))[0][1]
    n = obj["attrs"]["Size"]["value"][0]
    v = obj["value"]
    S = np.ones((n, n))
    k = 0
    for j in range(n):  # an R dist object stores its lower triangle column by column
        for i in range(j + 1, n):
            S[i, j] = S[j, i] = v[k]
            k += 1
    return {"similarity": S, "nm": np.array(obj["attrs"]["Labels"]["value"], float)}


def rothkopf_1957() -> dict:
    """Rothkopf (1957): 598 people heard two Morse signals one after the other and said whether they were the same.
    ``same`` (36 x 36) is the proportion of 'same' for row signal i and column signal j, from smacof's asymmetric
    matrix (stored as 1 minus that proportion).  The row is the signal heard first: with that reading the matrix
    reproduces Tversky's (1977) count from Rothkopf's table (the shorter signal first is called 'same' more often in
    336 of 555 pairs of unequal length; ``concepts.prominence_asymmetry``).  ``signals`` are the codes and
    ``symbols`` the letters and digits (A to Z, then 1 to 9 and 0, as the codes show)."""
    from explainer.psychology import rdata

    obj = rdata.load(member_path("rothkopf_1957"))[0][1]
    codes = obj["attrs"]["dimnames"]["value"][0]["value"]
    D = np.array(obj["value"], float).reshape(36, 36, order="F")
    symbols = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + list("1234567890")
    return {"same": 1.0 - D, "signals": codes, "symbols": symbols}


def austen() -> list:
    """Jane Austen's six novels as lower-case word tokens (729,322 of them), from the R package janeaustenr."""
    import re

    from explainer.psychology import rdata

    tokens = []
    for book in ("prideprejudice", "persuasion", "northangerabbey", "sensesensibility", "mansfieldpark", "emma"):
        lines = rdata.load(member_path("austen_" + book))[0][1]["value"]
        tokens += re.findall(r"[a-z]+", " ".join(x for x in lines if x).lower())
    return tokens


def natural_stories() -> dict:
    """The Natural Stories corpus's self-paced reading times, one entry per word of its ten stories in reading
    order: ``word`` (as shown, with punctuation), ``story`` (1-10), ``zone`` (position in the story), ``n`` (readers
    after exclusions) and ``rt`` (their mean reading time, ms), from ``processed_wordinfo.tsv`` (realigned in
    2025)."""
    import csv

    with open(path("naturalstories_words"), newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    rows.sort(key=lambda r: (int(r["item"]), int(r["zone"])))
    return {"word": np.array([r["word"] for r in rows]), "story": np.array([int(r["item"]) for r in rows]),
            "zone": np.array([int(r["zone"]) for r in rows]), "n": np.array([int(r["nItem"]) for r in rows]),
            "rt": np.array([float(r["meanItemRT"]) for r in rows])}


def mental_rotation() -> dict:
    """Ganis and Kievit's (2015) mental rotation validation study: 54 people, 96 trials each, judging whether two
    Shepard-Metzler objects at 0, 50, 100 or 150 degrees apart are the same object or mirror images.  Per trial:
    ``subject``, ``trial``, ``rt`` (ms; NaN when no response came in time), ``same`` (the right answer was
    'same'), ``angle`` (degrees) and ``correct`` (a time-out counts as an error), read from each person's
    workbook in the published zip."""
    import io
    import re
    import zipfile

    cols = {k: [] for k in ("subject", "trial", "rt", "same", "angle", "correct")}
    with zipfile.ZipFile(path("ganis_kievit_2015")) as z:
        names = sorted((n for n in z.namelist() if re.fullmatch(r"Behavioural_data/sub\d+\.xlsx", n)),
                       key=lambda n: int(re.search(r"sub(\d+)", n).group(1)))
        for name in names:
            sid = int(re.search(r"sub(\d+)", name).group(1))
            cells = _xlsx_cells(io.BytesIO(z.read(name)), 1)
            r = 5
            while f"A{r}" in cells and cells.get(f"B{r}"):
                rt = cells.get(f"C{r}")
                cols["subject"].append(sid)
                cols["trial"].append(int(float(cells[f"A{r}"])))
                cols["rt"].append(float(rt) if rt not in (None, "", "N/A") else np.nan)
                cols["same"].append(cells.get(f"D{r}") == "[b]")
                cols["angle"].append(float(cells[f"F{r}"]))
                cols["correct"].append(cells.get(f"G{r}") in ("1", "1.0"))
                r += 1
    out = {k: np.array(v) for k, v in cols.items()}
    out["correct"] &= np.isfinite(out["rt"])
    return out


def syllogisms_ragni2016() -> dict:
    """Ragni's 2016 syllogism data from the CCOBRA benchmark: 139 people, each answering all 64 syllogisms with one
    of nine responses.  Per answer: ``id`` (person), ``sequence`` (position), ``task`` (premises, e.g.
    'Some;models;managers/All;models;clerks'), ``response`` ('Some;managers;clerks' or 'NVC'), ``age``, ``gender``."""
    import csv

    with open(path("ragni_2016"), newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return {"id": np.array([int(r["id"]) for r in rows]), "sequence": np.array([int(r["sequence"]) for r in rows]),
            "task": np.array([r["task"] for r in rows]), "response": np.array([r["response"] for r in rows]),
            "age": np.array([int(r["age"]) if r["age"].isdigit() else -1 for r in rows]),
            "gender": np.array([r["gender"] for r in rows])}


def speed_acc() -> dict:
    """Wagenmakers, Ratcliff, Gomez and McKoon (2008), Experiment 1, with the two extra participants of Heathcote and
    Love (2012): 17 people deciding whether a letter string is a word, in blocks that stressed speed or accuracy.
    Trials the papers excluded (``censor``) are dropped.  Per trial: ``id`` (str), ``speed`` (True in speed
    blocks), ``word`` (the string was a word), ``frequency`` (high, low, very_low; nw_* for non-words), ``said_word``
    and ``correct`` (bool), and ``rt`` in seconds."""
    d = _rframe("speed_acc_2008")
    keep = d["censor"].astype(float) == 0
    resp = d["response"][keep]
    word = d["stim_cat"][keep] == "word"
    return {"id": d["id"][keep].astype(str), "speed": d["condition"][keep] == "speed", "word": word.astype(bool),
            "frequency": d["frequency"][keep].astype(str), "said_word": (resp == "word").astype(bool),
            "correct": (d["stim_cat"][keep] == resp).astype(bool), "rt": d["rt"][keep].astype(float)}


def rr98() -> dict:
    """Ratcliff and Rouder (1998), Experiment 1: three people (jf, kr, nh) judging whether a patch of pixels was
    drawn from a light or a dark distribution, at 33 levels of brightness (``strength`` 0, darkest, to 32), in
    blocks that stressed speed or accuracy.  Trials flagged as outliers are dropped.  Per trial: ``id``, ``speed``,
    ``strength`` (int), ``light`` (the source was light), ``said_light``, ``correct`` and ``rt`` (seconds)."""
    d = _rframe("rr98")
    keep = d["outlier"].astype(float) == 0
    return {"id": d["id"][keep].astype(str), "speed": d["instruction"][keep] == "speed",
            "strength": d["strength"][keep].astype(int), "light": d["source"][keep] == "light",
            "said_light": d["response"][keep] == "light", "correct": d["correct"][keep].astype(float) == 1,
            "rt": d["rt"][keep].astype(float)}


def choices13k() -> dict:
    """choices13k (Peterson et al. 2021): 13,006 choices between two gambles, each problem answered by about 16
    people on Amazon Mechanical Turk, five trials each.  One entry per row of the published table (a problem in one
    block): ``problem``, ``feedback`` (whether outcomes were shown after each choice), ``n`` (people), ``block``,
    ``amb`` (gamble B's probabilities hidden), ``corr``, ``b_rate`` (the mean proportion choosing B) and ``A``,
    ``B``: the gambles, each a list of (probability, payoff) arrays.  Read as CSV and JSON; nothing is evaluated."""
    import csv
    import json

    with open(path("choices13k_selections"), newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with open(path("choices13k_problems"), encoding="utf-8") as f:
        probs = json.load(f)
    if len(probs) != len(rows):
        raise RuntimeError("choices13k: the problems and selections tables differ in length")
    tf = {"True": True, "False": False}
    return {"problem": np.array([int(r["Problem"]) for r in rows]),
            "feedback": np.array([tf[r["Feedback"]] for r in rows]),
            "n": np.array([int(r["n"]) for r in rows]), "block": np.array([int(r["Block"]) for r in rows]),
            "amb": np.array([tf[r["Amb"]] for r in rows]), "corr": np.array([int(r["Corr"]) for r in rows]),
            "b_rate": np.array([float(r["bRate"]) for r in rows]),
            "A": [np.array(probs[str(i)]["A"], dtype=float) for i in range(len(rows))],
            "B": [np.array(probs[str(i)]["B"], dtype=float) for i in range(len(rows))]}


def ego_depletion_rrr() -> dict:
    """The ego-depletion Registered Replication Report (Hagger et al. 2016): one row per laboratory, the primary
    outcome (reaction-time variability on the multi-source interference task) after the depleting or the control
    version of the letter-crossing task.  Columns: ``lab``, ``language`` ('English' or 'Non-English'), ``m_dep``,
    ``sd_dep``, ``n_dep``, ``m_ctl``, ``sd_ctl``, ``n_ctl``.  The first row is the study the protocol was based on
    (Sripada et al.), not a replication; ``original`` marks it.  Read as CSV (Latin-1, as published)."""
    import csv

    with open(path("ego_depletion_rrr"), newline="", encoding="latin-1") as f:
        rows = list(csv.reader(f))
    head, body = rows[0], [r for r in rows[1:] if len(r) > 8 and r[3].strip()]
    out = {k: [] for k in ("lab", "language", "m_dep", "sd_dep", "n_dep", "m_ctl", "sd_ctl", "n_ctl", "original")}
    for r in body:
        out["lab"].append(r[1].strip())
        out["language"].append(r[2].strip())
        for k, i in (("m_dep", 3), ("sd_dep", 4), ("n_dep", 5), ("m_ctl", 6), ("sd_ctl", 7), ("n_ctl", 8)):
            out[k].append(float(r[i]))
        out["original"].append(r[0].strip() == "0")
    return {k: np.array(v) for k, v in out.items()}


def faces_1962() -> dict:
    """Abelson and Sermat (1962): dissimilarities of 13 posed facial expressions (Engen, Levy and Schlosberg's
    Lightfoot series), with each face's mean rating on Engen et al.'s (1958) three scales: pleasant-unpleasant
    (``PU``), attention-rejection (``AR``) and tension-sleep (``TS``).  From smacof's ``FaceExp`` and
    ``FaceScale``."""
    from explainer.psychology import rdata

    obj = rdata.load(member_path("faceexp"))[0][1]
    n = obj["attrs"]["Size"]["value"][0]
    v = obj["value"]
    D = np.zeros((n, n))
    k = 0
    for j in range(n):  # an R dist object stores its lower triangle column by column
        for i in range(j + 1, n):
            D[i, j] = D[j, i] = v[k]
            k += 1
    sc = rdata.load(member_path("facescale"))[0][1]
    names = sc["attrs"]["names"]["value"]
    scales = {nm: np.array(col["value"], float) for nm, col in zip(names, sc["value"])}
    labels = sc["attrs"]["row.names"]["value"]
    return {"D": D, "labels": list(labels), **scales}


def manybabies_2020() -> dict:
    """ManyBabies 1 (ManyBabies Consortium 2020): one row per laboratory and age group, with Cohen's d for the
    preference for infant-directed over adult-directed speech (``yi``), its variance ``vi``, the number of infants
    ``ni``, the ``lab``, the ``method`` (central fixation, eye tracking, head-turn preference), whether the stimuli
    were in the infants' native North American English ``nae``, and mean age in months ``age_mo``.  From
    psymetadata's ``manybabies2020``."""
    from explainer.psychology import rdata

    obj = rdata.load(member_path("manybabies2020"))[0][1]
    cols = {nm: col for nm, col in zip(obj["attrs"]["names"]["value"], obj["value"])}
    out = {}
    for k, col in cols.items():
        v = col["value"]
        levels = (col.get("attrs") or {}).get("levels")
        if levels:
            names = levels["value"]
            out[k] = [None if x is None else names[x - 1] for x in v]
        elif k in ("yi", "vi", "age_mo", "age_mo_centered"):
            out[k] = np.array([np.nan if x is None else x for x in v], float)
        elif k in ("es_id", "ni", "nae"):
            out[k] = np.array([-1 if x is None else x for x in v], int)
        else:
            out[k] = list(v)
    return out


def coles_2019() -> dict:
    """Coles, Larsen and Lench's (2019) facial-feedback meta-analysis: one row per effect size (Cohen's d ``yi``
    and its variance ``vi``), with ``study_id``, ``year``, publication status ``file_drawer``, the manipulation
    ``proc``, the stimuli ``stim`` and ``proc_aware``.  From psymetadata's ``coles2019``."""
    from explainer.psychology import rdata

    obj = rdata.load(member_path("coles2019"))[0][1]
    cols = {nm: col["value"] for nm, col in zip(obj["attrs"]["names"]["value"], obj["value"])}
    out = {}
    for k, v in cols.items():
        if k in ("yi", "vi", "prop_women"):
            out[k] = np.array([np.nan if x is None else x for x in v], float)
        elif k in ("study_id", "es_id", "year"):
            out[k] = np.array([-1 if x is None else x for x in v], int)  # -1: not recorded
        else:
            out[k] = list(v)
    return out
