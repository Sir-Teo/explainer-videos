"""Scene order for the final cut: (module, Scene class, chapter title)."""

TITLE = "The Navier–Stokes Equations, Derived and Visualized"

SCENES = [
    ("s01_hook", "Hook", "Every swirl obeys one equation"),
    ("s02_fields", "VelocityField", "Describing a fluid: fields"),
    ("s03_newton", "NewtonForParcels", "F = ma for a fluid parcel"),
    ("s04_material_derivative", "MaterialDerivative", "Acceleration: the material derivative"),
    ("s05_pressure", "PressureForce", "The pressure force"),
    ("s06_viscosity", "ViscousForce", "The viscous force"),
    ("s07_continuity", "Incompressibility", "Conservation of mass"),
    ("s08_pressure_poisson", "PressureEnforcer", "What decides the pressure?"),
    ("s09_full_equation", "FullEquation", "Putting it together"),
    ("s10_reynolds", "ReynoldsNumber", "The Reynolds number"),
    ("s11_turbulence", "Turbulence", "Instability and turbulence"),
    ("s12_millennium", "MillenniumProblem", "Vortex stretching and the $1M question"),
    ("s13_forced_blowup", "ForcedBlowup", "2026: OpenAI's forced blow-up claim"),
    ("s14_outro", "Outro", "Recap"),
]
