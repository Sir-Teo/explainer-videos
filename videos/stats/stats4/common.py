"""Helpers shared by the scenes of Part 4 of *Statistics, Built* ("Matrices for Statistics")."""

from __future__ import annotations

import numpy as np

from explainer.stats import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 4

DATA = S.DATA  # the data vector y
FIT = S.EST  # the projection Hy (fitted values)
RES = S.RESID  # the residual (I - H)y
SPACE = S.LIK  # the column space
EIG = S.ACCENT  # eigenvectors and eigenvalues
EXACT = S.TRUTH
SIM = S.EST


def money(v: float) -> str:
    return f"{v:,.0f}"


def mat_tex(M, fmt="{:.2f}") -> str:
    rows = [" & ".join(fmt.format(v) for v in r) for r in np.atleast_2d(M)]
    return r"\begin{pmatrix}" + r" \\ ".join(rows) + r"\end{pmatrix}"


class ProjectionLab:
    """The part's build: a subspace of R^3 (a plane spanned by two columns, or a line), a data vector y, its
    projection Hy and the residual (I - H)y, drawn in an ``NSpace`` that can turn.  ``lab.objects`` are redrawn every
    frame; reveal them with ``NSpace.reveal``."""

    def __init__(self, A, y, scale=0.62, center=(-3.2, -1.2, 0), angle=-0.6, tilt=0.38, axis_len=5.6):
        A = np.atleast_2d(np.asarray(A, float))
        if A.shape[0] != 3:
            A = A.T
        if A.shape[0] != 3 or A.shape[1] not in (1, 2) or np.linalg.matrix_rank(A) != A.shape[1]:
            raise ValueError("ProjectionLab needs one or two independent columns in R^3")
        self.A, self.y = A, np.asarray(y, float)
        q, _ = np.linalg.qr(A, mode="reduced")
        self.P = q @ q.T
        self.Py = self.P @ self.y
        self.r = self.y - self.Py
        self.ns = NSpace(scale=scale, center=center, angle=angle, tilt=tilt, axis_len=axis_len)
        ns = self.ns
        if A.shape[1] == 2:
            self.space = ns.plane(q[:, 0], q[:, 1], extent=3.4, color=SPACE, opacity=0.16)
        else:
            self.space = ns.line(A[:, 0], extent=1.3 * float(np.linalg.norm(self.y)), color=SPACE)
        self.vy = ns.vector(self.y, color=DATA)
        self.vfit = ns.vector(self.Py, color=FIT, stroke_width=6)
        self.vres = ns.vector(self.r, color=RES, origin=self.Py)
        self.angle_mark = ns.right_angle(self.Py, -self.Py, self.r, size=0.45)
        self.objects = [self.space, self.vy, self.vfit, self.vres, self.angle_mark]

    def stop(self):
        for m in self.objects:
            m.clear_updaters()
