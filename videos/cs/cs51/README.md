# Computer Science, Built — Part 51: Light and Pixels

Part 51 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first part of Act X, *Horizons and Trust*. A picture is millions of samples of
light. Projecting triangles onto a screen is linear algebra plus one division, getting the samples right is Nyquist
again, and the physics of light comes down to one integral equation, which Monte Carlo solves one bounced path at a
time. We build both ways of making a picture, a rasterizer and a ray tracer, and end with a path tracer that renders
the series' own box, its noise falling as 1/√N.

The instruments are in `explainer/cs/graphics/` (tested in `tests/test_cs51_raster.py` and
`tests/test_cs51_light.py`):
* `transform.py`: 4 × 4 homogeneous matrices (translation, scaling, rotations, composition applied right to left) and
  the rotate-then-translate demo; OpenGL's perspective matrix (`gluPerspective`'s) and the frustum folded into the NDC
  cube; window depth, the smallest depth gap a b-bit buffer resolves (by bisection, checked against the closed form)
  and z-fighting between two close planes; Euler angles (yaw, pitch, roll about Z, Y, X) and the singular values of
  the map from angle rates to spin; quaternions with the Hamilton product, and Shoemake's slerp against linear Euler
  interpolation.
* `raster.py`: edge functions (Part 22's orientation test) on vertices snapped to 1/256 pixel, the top-left fill rule,
  barycentrics, Sutherland–Hodgman clipping against the near plane in homogeneous space, perspective-correct
  interpolation of a/w and 1/w, a z-buffer (cleared to 1, test GL_LESS) and fragment counters; the demos built on it:
  a triangle coloured by its barycentrics, a checkered floor three ways (affine, with 1/w, ray cast), Lambert, Phong
  and Blinn–Phong on a sphere of 360 triangles with Gouraud against Phong shading and the exact sphere, a mip pyramid
  with nearest, bilinear and trilinear sampling (λ = log₂ ρ) against 16× supersampling and a 256-sample reference, and
  the z-buffer against the painter's algorithm.
* `ray.py`: ray–sphere (the quadratic, solved without cancellation) and Möller–Trumbore intersection; random terrain
  meshes; BVHs built by median split and by binned SAH, traversed nearest child first, against brute force; a Whitted
  ray tracer (a checkerboard floor, mirror, glass and diffuse spheres, one point light with hard shadows) with Snell
  refraction, Fresnel–Schlick weights and total internal reflection, traced breadth first with ray counts by kind.
* `brdf.py`: Lambert, normalized Phong ((n + 2)/2π) and Blinn–Phong ((n + 8)/8π, an approximation), Cook–Torrance
  with the GGX distribution, Smith masking and Fresnel–Schlick; samplers and their pdfs (uniform and cosine
  hemisphere, GGX half vectors, a Phong lobe, a cone); white-furnace albedos by quadrature and by Monte Carlo;
  reciprocity on 10,000 random pairs of directions; light, BRDF and multiple importance sampling (balance and power
  heuristics) for one glossy point under a spherical light.
* `path.py`: the series' scene, a Cornell-like box open at the front (white walls of albedo 0.73, a red and a green
  wall, a 0.25 × 0.25 light in the ceiling, a mirror ball, a white ball and a small blue ball), and a path tracer
  compiled with numba: cosine or uniform sampling, next-event estimation, Russian roulette from the third bounce, and
  each path's light filed by its number of reflections, so the image splits into the terms of the Neumann series; a
  2048-spp reference, convergence, four sampling strategies, the roulette check, an edge-avoiding à-trous denoiser on
  a g-buffer (normal, albedo and position of the first non-mirror hit), and sRGB output through a Reinhard curve.
* `curves.py`: de Casteljau's construction and the Bernstein form, subdivision of a cubic, B-splines by the Cox–de
  Boor recursion and their continuity at the knots, and Catmull–Clark subdivision of a cube with the limit positions
  of Halstead, Kass and DeRose.

## Chapters

* **Hook. A picture is samples of light.** Our path tracer's 128 × 128 box at 1, 4, 16 and 256 paths per pixel, with
  error on the surfaces 0.283, 0.129, 0.076 and 0.021: it falls like N^−0.46, close to the 1/√N of Part 20's Monte
  Carlo. Two ways to make a picture: a rasterized triangle blending three colours, and a 160 × 120 Whitted ray-traced
  image that took 41,563 rays; Sketchpad (1963) and Whitted (1980); the plan.
* **1. Transforms and rotations.** A matrix moves every point at once (its columns are where the axis arrows land),
  but never the origin; homogeneous coordinates (Möbius 1827) make translation linear, a shear one dimension up, with
  points at w = 1 and directions at w = 0. Order matters: rotating the unit square 90° and then translating it by 2
  puts its corners at (2, 0), (2, 1), (1, 1), (1, 0), the other order at (0, 2), (0, 3), (−1, 3), (−1, 2); a renderer
  chains P V M x. Gimbal lock measured: the singular values of the map from angle rates to spin are 1,
  √(1 + sin p) and √(1 − sin p), so 1.307, 1 and 0.541 at a pitch of 45°, a smallest of 0.012 at 89°, and 0 with rank
  2 at 90°. Quaternions (Hamilton 1843) against Euler angles and matrices; slerp (Shoemake 1985) from (yaw, pitch,
  roll) = (0, 0, 0) to (150, 80, −100) degrees in 40 steps turns a constant 3.48° a step, 139.2° in all, exactly the
  single rotation between the ends, against 237.2°, unevenly, for Euler angles moved in straight lines.
* **2. Perspective projection.** Similar triangles (Alberti 1435): y′ = n y/d, twice as far, half as tall; division
  is not linear, so the matrix copies the distance into w and the hardware divides once per vertex. The third row,
  from near ↦ −1 and far ↦ +1: z_ndc = (f + n)/(f − n) − 2fn/((f − n) d), affine in 1/d. Ours (60°, 4:3, near 1, far
  4) has entries 1.299, 1.732, −1.667, −2.667 and −1; the frustum folds into the cube [−1, 1]³, straight lines stay
  straight, and three equally spaced slices (d = 1.75, 2.5, 3.25) crowd towards the far face at z_ndc = 0.14, 0.60,
  0.85; clipping comes first, while everything is linear. Where depth goes, for near 0.1 and far 1000: half the stored
  range is used by distance 0.20 and 90% by 1.00; a 4-bit buffer whose last step spans the back half, 8 to 16. The
  smallest gap a 24-bit buffer resolves, by bisection and the closed form Δ ≈ d²(f − n)/(f n (2^b − 1)): at distance
  1000 it is 5.9 with the near plane at 0.01, 0.60 at 0.1 and 0.060 at 1. Z-fighting, two planes 0.01 apart at
  distance 50 over 19,200 pixels: 99.4% drawn wrong with near 0.01 and 16 bits, 31.9% with 24 bits, 71.9% with near 1
  and 16 bits, 0.0% with near 1 and 24 bits; reversed floating-point depth.
* **3. Rasterization and the z-buffer.** Edge functions (Part 22's orientation test; Pineda 1988) and the top-left
  rule: at 160 × 120, 9,804 pixels of the triangle's bounding box tested and 4,748 inside. Barycentric coordinates,
  free from the edge functions, painted as red, green and blue. Why interpolate 1/w: equal steps on the screen are
  growing steps on a receding floor, while u/w and 1/w are affine in screen position. A checkered floor of two
  triangles (3,934 pixels): affine interpolation colours 48.5% of them wrongly, interpolation with 1/w none, and its
  texture coordinates agree with a ray cast to 1.8 × 10⁻¹⁴; the original PlayStation's wobbling textures. The z-buffer
  (Catmull 1974) on two triangles that pass through each other: of 1,164 overlap pixels the orange one is in front in
  693 and the blue one in 471; the painter's order gets 472 pixels wrong, the z-buffer 1 (a coverage tie on an outer
  edge), with 5,883 fragments passing the depth test and 693 failing. Our rasterizer end to end: clip coordinates,
  near-plane clipping, the division, the viewport, edge functions, the depth test, the a/w and 1/w blend.
* **4. Shading.** Lambert's cosine law (1760) from irradiance, E = E⊥ (N · L); Phong's highlight about the mirror
  direction (1975), R = 2(N · L)N − L, with power s = 32; Blinn's halfway vector (1977) and why s′ = 4s gives the
  same width, since cos^s α ≈ e^(−sα²/2) and H is α/2 from N; Gouraud (1971) against Phong shading on a sphere of 360
  triangles, where the highlight is a star or a disc: the largest per-pixel difference is 0.34 of full brightness, and
  against the exact, ray-cast sphere the error is 0.040 for Gouraud and 0.0079 for Phong, 5 times smaller. Normals
  move by the inverse transpose, n′ = M^−⊤ n.
* **5. Textures and sampling.** Moiré is aliasing: 9 cycles sampled 10 times read as 1 cycle, |f − k f_s|, and
  Nyquist (Part 36) asks for more than two samples per cycle. One floor, four samplers, against 256 jittered samples
  per pixel over 19,200 pixels: point sampling's error is 0.199, the trilinear mipmap's (8 texel reads) 0.065, 3.1
  times smaller, and 16 samples per pixel reach 0.053. Mipmaps (Williams 1983): levels from 128 × 128 down to 1 × 1,
  grey from level 5, 16,384 texels becoming 21,845 (33.33% more, the geometric series' third). The level λ = log₂ ρ
  from the pixel's footprint, 0 at the bottom of the frame and 7 at the horizon; anisotropic filtering with
  N = ⌈ρmax/ρmin⌉ probes; supersampling against MSAA (16 shaded samples against 4 coverage samples and one shader
  run).
* **6. The GPU pipeline.** Vertex fetch, vertex shader, clip and divide, rasterize, fragment shader, depth and blend,
  the two shaders written by the programmer; a vertex and a fragment shader in the style of GLSL (illustrative). SIMT:
  about 2 million pixels at 60 frames a second, fragments in 2 × 2 quads packed into warps of 32 lanes, a branch that
  splits a warp running both sides. Derivatives by subtraction within a quad: chapter 3's 4,748 pixels touch 1,236
  quads, so 196 helper lanes, 4% extra. Early depth testing on chapter 3's crossing triangles: of 6,576 fragments 693
  fail and are never shaded, and 471 of the 5,883 shaded are painted over, leaving 5,412 visible pixels.
* **7. Ray tracing.** One ray through every pixel (Appel 1968), 19,200 primary rays in our Whitted tracer; ray meets
  sphere as a quadratic whose discriminant decides two hits, a graze or a miss, computed without cancellation (Part
  4); Möller–Trumbore (1997) by Cramer's rule; Whitted's ray tree in a 2D slice (shadow rays, reflection, refraction)
  and our counts: 19,200 primary, 13,650 shadow, 4,397 reflection and 4,316 refraction rays, 41,563 in all, 2.16 per
  pixel. Snell's law in vectors and total internal reflection beyond 41.8°, which a ray inside a ball never reaches
  (0 counted); exact Fresnel against Schlick's fit (1994), R₀ = 0.04 for glass, and the rim of our glass ball as a
  mirror.
* **8. Acceleration structures.** Brute force: 41,563 rays against 100,000 triangles is about 4.2 × 10⁹ tests. A BVH
  over 40 illustrative triangles by median splits (31 nodes, 16 leaves of at most 3, 4 levels below the root); the
  traversal with Kay and Kajiya's slabs, nearer child first: one ray tests 17 boxes (11 entered, 6 skipped) and 8 of
  the 40 triangles, and finds the same hit. The surface area heuristic (MacDonald and Booth 1990): on 12 boxes, 9
  bunched and 3 spread out, the median split costs 8.6, the cheapest plane 6.9, no split 12. Our 3D BVH on terrains of
  100 to 100,000 triangles: 6.8 to 10.3 triangle tests per ray with median splits, 2.1 to 2.9 with the SAH; at 100,000
  triangles, 2.5 tests and 39 boxes per ray against 100,000 tests, each tenfold increase adding 9 to 10 box visits,
  the SAH tree deeper (19 levels against 15) yet cheaper to walk, and the same nearest hit as brute force on 100% of
  the rays checked.
* **9. Radiometry and BRDFs.** Solid angle, Ω = 2π(1 − cos α) for a cap, 2π for the hemisphere; flux, irradiance and
  radiance, which is constant along a ray; the BRDF (Nicodemus et al. 1977) and the reflection equation; Lambert's
  ρ/π, and why π; microfacets, Cook–Torrance (1982) and GGX (Walter et al. 2007). Reciprocity on 10,000 random pairs:
  Lambert, Phong and Blinn–Phong exact, GGX to 6 × 10⁻¹⁵. The white furnace: Lambert returns 1 at every angle,
  normalized Phong at n = 10 returns 1 head-on and 0.23 at 80°, Blinn–Phong at n = 10 returns 1.075 head-on (Monte
  Carlo 1.070 ± 0.003), creating energy, and GGX at α = 1 returns 0.307 head-on, losing 69% (0.988 at α = 0.1).
* **10. The rendering equation.** Light arriving is light leaving somewhere else: Kajiya's equation (1986); the
  operator T and the Neumann series L = L_e + T L_e + T² L_e + ⋯, which converges because each reflection keeps at
  most its albedo (in a closed room of walls of albedo 0.73 the bounces add up to 1/(1 − 0.73) = 3.70 times the light
  emitted); each term is a set of paths (Veach 1997). Our path tracer's bounce images, 0 to 7 and up at 2048 paths per
  pixel, summed on screen: direct light leaves the ceiling black, bounce 2 lights it and brings the colour bleeding.
  The mean radiance of the bounce images, 0.128, 0.067, 0.026, 0.012, …, each term from bounce 1 on 0.38 to 0.53
  times the one before; the eight add up exactly to the reference's mean, 0.2466; 43% of the light reaching the eye
  from surfaces took two or more bounces; radiosity (Goral et al. 1984).
* **11. Path tracing.** The Monte Carlo estimator and the throughput β; one path in a side view of our box (back
  wall, ceiling, the matte ball, the lamp). Cosine-weighted sampling by Malley's method, p = cos θ/π, so that
  f cos θ/p is just the albedo. Russian roulette (Arvo and Kirk 1990): E[X′] = q · X/q = X, at the price
  Var[X′] = Var[X] + (1/q − 1)E[X²]; our tracer plays from the third bounce with q the throughput, capped at 0.95
  (q = 0.73³ = 0.39 for a path among walls of 0.73). Next-event estimation: the light is a sixteenth of the ceiling,
  and none of 9 random bounces from the floor found it in the side view, so a shadow ray aims at a point on it,
  dω = cos θ′ dA/d², and light reached by chance is then ignored except after a mirror. Multiple importance sampling
  (Veach and Guibas 1995), in one dimension: unbiased for any weights that sum to one, and the balance heuristic.
* **12. Our path tracer, and denoising.** The noise up close at 1 to 256 paths per pixel (0.026 s to 6.37 s), the
  variance σ²/N; on log axes the fitted slopes are −0.46 on surfaces and over all pixels, the last point lifted by
  the reference's own noise (about 0.283/√2048 = 0.0063, against 0.0206). Four strategies at 16 spp, efficiency
  1/(error² × time) relative to the first: cosine sampling with NEE 1.00 (error 0.075), uniform with NEE 0.70, cosine
  without NEE 0.11, uniform without NEE 0.070; NEE is worth 9.0 times, the cosine 1.42 times with NEE and 1.59
  without. Roulette tested on 12 renders each way (64 × 64, 16 spp): mean 0.2463 ± 0.0009 against 0.2474 ± 0.0007
  (z = −0.95), a per-pixel RMS z-score of 1.04, and 3.16 rays per path against 6.96, 55% fewer, in 1.06 s against
  1.99 s. MIS measured on one glossy point (normalized Phong with n = 10, 100, 1000: lobe widths 18.1°, 5.7°, 1.8°)
  under a round light of angular radius 1.0°, 5.7° and 19.5°, 32 samples, 4,000 trials a cell: worst relative errors
  0.93 for light sampling, 4.64 for BRDF sampling, 0.095 for the balance heuristic and 0.084 for the power heuristic.
  The edge-avoiding à-trous filter (Dammertz et al. 2010): a B3 kernel, three passes with taps 1, 2 and 4 pixels
  apart, weights by colour, normal, albedo and position, and demodulation by the albedo; at 16 spp the surface error
  falls from 0.077 to 0.019, 4.0 times smaller, all pixels from 0.127 to 0.105, the indirectly lit ceiling turns
  blotchy, and the filter takes 0.34 s against a 0.43 s render.
* **13. Curves, surfaces and fonts.** De Casteljau (Citroën, 1959) and Bézier (Renault): the cubic with control
  points (0, 0), (1, 2), (3, 2.2), (4, 0.2) passes through (2, 1.6) at t = ½, and the construction splits it in two;
  the Bernstein polynomials, the convex hull, and transforms acting on control points alone. A uniform cubic B-spline
  (Cox and de Boor 1972) of seven points and four pieces: across the knots the position jumps by 10⁻¹⁵ to 10⁻¹⁴, the
  slope by 10⁻¹³ to 10⁻¹², the curvature by 10⁻¹¹ to 10⁻¹⁰, while the third derivative jumps by 9.85, 5.66 and 8.94:
  C²; local control; NURBS. Catmull–Clark (1978) on a cube: 6, 24, 96, 384 and 1,536 faces with V − E + F = 2
  throughout, a corner's distance from the centre 1.7321, 0.9623, 0.8821, 0.8687, 0.8665 against the limit 0.8660
  (Halstead et al. 1993); *Geri's Game* (1997). The word "Light" as Manim draws it from TeX's fonts: 110 cubic curves,
  and 536 in the heading above it; PostScript and Type 1 fonts store cubics, TrueType quadratics; letters filled by
  winding number with coverage averaged in each pixel.
* **14. Frontier: real time, and neural rendering.** A few samples, then clean up: our 16-path image (error 0.077)
  denoised to 0.019, below 256 paths' 0.021; ray-tracing hardware since 2018, ReSTIR (Bitterli et al. 2020) and
  learned denoisers and upscalers; neural radiance fields (Mildenhall et al. 2020) and 3D Gaussian splatting (Kerbl et
  al. 2023), this part's rendering run in reverse (*AI, Built* 22), and what is lost. Four open problems (caustics,
  denoisers with guarantees, inverse rendering, perceptual error) and the ★ research problem.
* **Outro.** Recap, payoffs, practice, problems, next part.

## Build

```bash
python -m videos.cs.cs51.compute
python -m unittest tests.test_cs51_raster tests.test_cs51_light
python tools/build.py cs51
```

## Problems, with solutions

1. **Perspective.** Derive the perspective matrix that maps the frustum to the cube [−1, 1]³, and show depth is
   affine in 1/z.

   *Solution.* In eye space the camera is at the origin looking down −z, so a point in front is at distance d = −z.
   By similar triangles a point at height y lands on a screen at distance n at height n y/d. Scale the screen so the
   top of the field of view, y = d tan(fov/2), lands at 1: y_ndc = c y/d with c = cot(fov/2), and likewise
   x_ndc = (c/a) x/d for aspect ratio a. Both are linear in the point divided by d = −z, so the fourth row is
   (0, 0, −1, 0), which puts w = d, and the first two rows are (c/a, 0, 0, 0) and (0, c, 0, 0). Depth may not depend
   on x or y, so the third row is (0, 0, A, B), and after the division z_ndc = (A z + B)/(−z) = −A + B/d. Asking for
   d = n ↦ −1 and d = f ↦ +1 gives −A + B/n = −1 and −A + B/f = 1; subtracting, B(1/n − 1/f) = −2, so
   B = 2fn/(n − f), and then A = 1 + B/n = (f + n)/(n − f). Hence
   z_ndc = (f + n)/(f − n) − (2fn/(f − n)) · (1/d): affine in 1/d = −1/z, not in z. The side faces x = ±a d tan(fov/2)
   and y = ±d tan(fov/2) go to ±1, so the frustum becomes the cube. For ours (60°, 4:3, n = 1, f = 4): c = √3 = 1.732,
   c/a = 1.299, A = −5/3, B = −8/3, and d = 1, 1.75, 2.5, 3.25, 4 land at z_ndc = −1, 0.14, 0.60, 0.85, 1. The price:
   dz_ndc/dd = 2fn/((f − n) d²), so one step 1/(2^b − 1) of window depth (z_ndc + 1)/2 spans
   Δ ≈ d²(f − n)/(f n (2^b − 1)): 5.96 at d = 1000 for n = 0.01, f = 1000 and b = 24 (bisection on the exact mapping:
   5.93), and 0.060 for n = 1.

2. **Why 1/w.** Show that interpolating u/w and 1/w linearly in screen space gives perspective-correct u.

   *Solution.* A triangle lies in a plane m · P = k of eye space (k ≠ 0, or the eye is in the plane and the triangle
   is seen edge on). Screen position (x_s, y_s) is an affine function of (x/w, y/w), with w = −z, so every point of
   the plane is P = w r(x_s, y_s), where r = (x/w, y/w, −1) is affine in screen position. Substituting,
   w (m · r) = k, so 1/w = (m · r)/k is affine in (x_s, y_s). An attribute that is affine over the triangle in 3D,
   u = g · P + h, gives u/w = g · r + h · (1/w), again affine in screen position. Linear interpolation with
   screen-space barycentrics λᵢ reproduces affine functions exactly, so u/w = Σ λᵢ uᵢ/wᵢ and 1/w = Σ λᵢ/wᵢ, and
   u = (Σ λᵢ uᵢ/wᵢ)/(Σ λᵢ/wᵢ); equivalently the true barycentrics are bᵢ = (λᵢ/wᵢ)/Σⱼ (λⱼ/wⱼ). Interpolating u directly
   is wrong whenever the wᵢ differ, since u is a ratio of two affine functions, not one. Example: an edge from depth 2
   to depth 12 with u from 0 to 8, like our floor. At the screen midpoint affine interpolation gives u = 4; the
   correct value is (½ · 0/2 + ½ · 8/12)/(½ · 1/2 + ½ · 1/12) = 1.14, at depth 3.43, and the floor's own midpoint
   (depth 7, u = 4) appears 86% of the way across. On our two-triangle floor affine interpolation colours 48.5% of the
   3,934 pixels wrongly, interpolation with 1/w none, matching the ray cast to 1.8 × 10⁻¹⁴.

3. **Möller–Trumbore.** Derive the ray–triangle test with Cramer's rule.

   *Solution.* A point of the triangle is (1 − u − v) v₀ + u v₁ + v v₂ with u, v ≥ 0 and u + v ≤ 1. Setting it equal
   to the ray o + t d and writing e₁ = v₁ − v₀, e₂ = v₂ − v₀, s = o − v₀ gives −t d + u e₁ + v e₂ = s, the linear
   system [−d e₁ e₂](t, u, v)ᵀ = s. With det[a b c] = a · (b × c), the determinant is
   (−d) · (e₁ × e₂) = e₁ · (d × e₂) = e₁ · p, where p = d × e₂; if it is near zero the ray is parallel to the plane.
   Cramer's rule replaces one column by s: u = det[−d s e₂]/det = −d · (s × e₂)/det = s · p/det; with q = s × e₁,
   v = det[−d e₁ s]/det = d · (s × e₁)/det = d · q/det, and t = det[s e₁ e₂]/det = s · (e₁ × e₂)/det = e₂ · q/det.
   It is a hit when u ≥ 0, v ≥ 0, u + v ≤ 1 and t > t_min: two cross products, four dot products and one reciprocal,
   with early exits after u and after v, and u, v left over as interpolation weights. Check: v₀ = (0, 0, 0),
   v₁ = (1, 0, 0), v₂ = (0, 1, 0), o = (0.2, 0.3, 1), d = (0, 0, −1) give p = (1, 0, 0), det = 1, u = 0.2,
   q = (0, 1, −0.3), v = 0.3 and t = 1, as `ray.moller_trumbore` returns.

4. **Russian roulette.** Prove that Russian roulette leaves the path tracer unbiased, and compute its effect on
   variance.

   *Solution.* At a vertex, let X ≥ 0 be the light the rest of the path would contribute, and let the path continue
   with probability q ∈ (0, 1], chosen from the path so far, by a coin independent of everything else; the survivor's
   contribution is divided by q, so X′ = X/q with probability q and 0 otherwise. Given the path so far and X,
   E[X′] = q · X/q + (1 − q) · 0 = X, and by the tower property E[X′] = E[X]. Roulette is applied at every vertex from
   the third bounce on; by induction from the last vertex back, each vertex's estimate keeps its expectation, so every
   term T^k L_e of the series keeps its expected value (both versions are capped at 32 reflections, so they estimate
   the same sum). For the variance, E[X′² | X] = q X²/q² = X²/q, so Var[X′] = E[X²/q] − E[X]² =
   Var[X] + E[(1/q − 1) X²]. For a whole sample F = H + T, with H gathered before the coin and T after, F′ = H + I T/q
   with E[I] = q, and Var[F′] = Var[F] + E[(1 − q) T²/q]: the added variance is largest when q is small and T large,
   which is why q is the throughput β: a survivor's weight β/q returns to 1, and paths are killed mostly where their
   tail is dim. With β = 0.73³, q = 0.389 and 1/q − 1 = 1.57 at that vertex. Capping q at 0.95 means at most
   0.95/0.05 = 19 further bounces are expected even in a white furnace. What matters is efficiency, the inverse of
   variance times time: in our check the means agree (0.2463 ± 0.0009 against 0.2474 ± 0.0007, z = −0.95), the
   per-pixel RMS z-score is 1.04, and roulette cuts the rays per path from 6.96 to 3.16 (55% fewer) and the time from
   1.99 s to 1.06 s.

5. **Build.** Add next-event estimation for a second light to our path tracer, and measure the noise at 16 spp.

   *Solution notes.* In `path.py`, give `cornell_scene` a second emitter rectangle (for instance another
   0.25 × 0.25 square, on the back wall or elsewhere on the ceiling) and replace the scene's single `light` index by a
   list of indices, packed by `_pack` as an integer array with each light's area and power (area times the luminance
   of its radiance). In `_kernel`, at each diffuse vertex choose light j with probability Pⱼ (½ each, or proportional
   to power), sample a point uniformly on it as now, and divide its contribution, f L_e cos θ cos θ′ A/d² V, by Pⱼ;
   or loop over both lights with one shadow ray each and no division. The rule that stops light being counted twice
   must cover every sampled light: `obj != light` becomes a test of an `is_light` flag, still counting emission at
   depth 0 and after a mirror; the one-sided test `cl > 0` uses each light's own axis and `rsign`. Getting either rule
   wrong for one light makes it too bright or drops its direct light, and the tests catch both: the bounce-1 image is
   linear in the emitters, so with both lights it must equal the sum of the bounce-1 images with each light alone to
   within noise (per-pixel z-scores near 1, as in the roulette check); and a two-light version of `furnace_scene` must
   still return L = emit/(1 − ρ) at every bounce. To measure, render a 2048-spp reference of the new scene, then 16-spp
   images with (a) NEE for the old light only, the new one found by chance, (b) a uniform choice of light, (c) a choice
   by power, (d) both lights at every vertex, and compare `rmse` on the surfaces, time and the efficiency
   1/(error² × time) as `sampling_comparison` does. Expect (a) to be far noisier wherever the new light dominates,
   (c) to beat (b) when the lights differ in power, and (d) to have the lowest error per path at the cost of two
   shadow rays.

6. **★ Research.** Caustic paths with provably near-optimal variance.

   *Discussion.* Open. A specular–diffuse–specular path, such as light focused by glass onto a floor and seen in a
   mirror, is hard for every local way of building paths: a light path hits the floor, but its connection to the eye
   must pass through the mirror in exactly the reflected direction; an eye path reaches the floor through the mirror,
   but its connection to the light must pass through the glass in exactly the refracted direction. Neither can be
   sampled by a shadow ray, so unbiased methods find these paths only by chance, and with a point light and a pinhole
   camera, as Veach's thesis observes, some cannot be sampled at all. Our own box shows the easier case: light
   reflected by the mirror ball onto the floor (a caustic) reaches the eye only when a cosine-sampled bounce from the
   floor happens to strike the mirror and then the small light. Existing methods trade one property for another:
   photon mapping and its progressive and vertex-merging forms are consistent but biased; Metropolis light transport
   and manifold exploration are unbiased but come with no useful variance bound; specular manifold sampling has an
   unbiased form whose cost depends on the scene. The problem asks for an estimator together with a theorem: define
   the class of estimators allowed (unbiased, at most a fixed number of ray casts per sample), the best variance any
   of them can reach on a family of scenes, and an algorithm within a constant factor of it. A good partial answer would settle a
   restricted family, such as a single smooth convex refractor over a diffuse plane, seen through one planar mirror,
   with a matching lower bound; or prove that an existing method's variance is bounded relative to the integrand on
   such a family.

## 习题与解答

1. **透视。** 推导把视锥体映到立方体 [−1, 1]³ 的透视矩阵，并证明深度是 1/z 的仿射函数。

   *解答。* 在眼空间中，相机在原点，朝 −z 方向看，所以前方一点的距离是 d = −z。由相似三角形，高度为 y 的点落在距离 n 的屏幕上，
   高度为 n y/d。把屏幕缩放，使视野的上边缘 y = d tan(fov/2) 落在 1：y_ndc = c y/d，其中 c = cot(fov/2)；同理，宽高比为 a 时
   x_ndc = (c/a) x/d。两者都是点的线性函数除以 d = −z，所以第四行取 (0, 0, −1, 0)，使 w = d，前两行取 (c/a, 0, 0, 0) 和
   (0, c, 0, 0)。深度不能依赖 x 和 y，所以第三行是 (0, 0, A, B)，除法之后 z_ndc = (A z + B)/(−z) = −A + B/d。要求 d = n ↦ −1、
   d = f ↦ +1，得 −A + B/n = −1 和 −A + B/f = 1；相减得 B(1/n − 1/f) = −2，所以 B = 2fn/(n − f)，再得
   A = 1 + B/n = (f + n)/(n − f)。于是 z_ndc = (f + n)/(f − n) − (2fn/(f − n)) · (1/d)：是 1/d = −1/z 的仿射函数，而不是 z 的。侧面
   x = ±a d tan(fov/2) 和 y = ±d tan(fov/2) 都映到 ±1，所以视锥体变成立方体。对我们的参数（60°，4:3，n = 1，f = 4）：
   c = √3 = 1.732，c/a = 1.299，A = −5/3，B = −8/3，d = 1、1.75、2.5、3.25、4 分别落在 z_ndc = −1、0.14、0.60、0.85、1。代价是：
   dz_ndc/dd = 2fn/((f − n) d²)，所以窗口深度 (z_ndc + 1)/2 的一个台阶 1/(2^b − 1) 跨越 Δ ≈ d²(f − n)/(f n (2^b − 1))：n = 0.01、
   f = 1000、b = 24 时在 d = 1000 处为 5.96（在精确映射上二分得 5.93），n = 1 时为 0.060。

2. **为什么是 1/w。** 证明在屏幕空间中线性插值 u/w 和 1/w，得到的是透视正确的 u。

   *解答。* 三角形位于眼空间的一个平面 m · P = k 上（k ≠ 0；否则眼睛在平面内，三角形只是一条线）。屏幕位置 (x_s, y_s) 是
   (x/w, y/w) 的仿射函数，其中 w = −z，所以平面上每一点都是 P = w r(x_s, y_s)，r = (x/w, y/w, −1) 是屏幕位置的仿射函数。代入得
   w (m · r) = k，所以 1/w = (m · r)/k 是 (x_s, y_s) 的仿射函数。在三维中沿三角形仿射变化的属性 u = g · P + h，给出
   u/w = g · r + h · (1/w)，同样是屏幕位置的仿射函数。用屏幕空间的重心坐标 λᵢ 做线性插值能精确地重现仿射函数，所以
   u/w = Σ λᵢ uᵢ/wᵢ，1/w = Σ λᵢ/wᵢ，u = (Σ λᵢ uᵢ/wᵢ)/(Σ λᵢ/wᵢ)；等价地，真正的重心坐标是 bᵢ = (λᵢ/wᵢ)/Σⱼ (λⱼ/wⱼ)。只要各 wᵢ
   不相等，直接插值 u 就是错的，因为 u 是两个仿射函数之比，而不是一个仿射函数。例子：一条边从深度 2 到深度 12，u 从 0 到 8，就像
   我们的地板。在屏幕上的中点，仿射插值给出 u = 4；正确的值是 (½ · 0/2 + ½ · 8/12)/(½ · 1/2 + ½ · 1/12) = 1.14，深度为 3.43；而地板
   自己的中点（深度 7，u = 4）出现在屏幕上 86% 的位置。在我们由两个三角形组成的地板上，仿射插值把 3,934 个像素中的 48.5% 涂错，
   用 1/w 插值一个也不错，与光线投射的结果相差 1.8 × 10⁻¹⁴。

3. **Möller–Trumbore。** 用克拉默法则推导光线与三角形的求交测试。

   *解答。* 三角形上的点是 (1 − u − v) v₀ + u v₁ + v v₂，u, v ≥ 0，u + v ≤ 1。令它等于光线 o + t d，记 e₁ = v₁ − v₀、e₂ = v₂ − v₀、
   s = o − v₀，得 −t d + u e₁ + v e₂ = s，即线性方程组 [−d e₁ e₂](t, u, v)ᵀ = s。用 det[a b c] = a · (b × c)，行列式为
   (−d) · (e₁ × e₂) = e₁ · (d × e₂) = e₁ · p，其中 p = d × e₂；它接近零时，光线与平面平行。克拉默法则把一列换成 s：
   u = det[−d s e₂]/det = −d · (s × e₂)/det = s · p/det；记 q = s × e₁，v = det[−d e₁ s]/det = d · (s × e₁)/det = d · q/det，
   t = det[s e₁ e₂]/det = s · (e₁ × e₂)/det = e₂ · q/det。u ≥ 0、v ≥ 0、u + v ≤ 1 且 t > t_min 时相交：两次叉积、四次点积、一次求倒数，
   算出 u 和 v 后都可以提前退出，剩下的 u、v 正好用作插值权重。验算：v₀ = (0, 0, 0)、v₁ = (1, 0, 0)、v₂ = (0, 1, 0)、
   o = (0.2, 0.3, 1)、d = (0, 0, −1)，得 p = (1, 0, 0)，det = 1，u = 0.2，q = (0, 1, −0.3)，v = 0.3，t = 1，与 `ray.moller_trumbore`
   的结果一致。

4. **俄罗斯轮盘赌。** 证明俄罗斯轮盘赌使路径追踪保持无偏，并计算它对方差的影响。

   *解答。* 在某个顶点，设 X ≥ 0 是路径其余部分会贡献的光，路径以概率 q ∈ (0, 1] 继续；q 由到此为止的路径决定，抛的硬币与其他一切
   独立；幸存者的贡献除以 q，所以 X′ 以概率 q 等于 X/q，否则为 0。给定到此为止的路径和 X，E[X′] = q · X/q + (1 − q) · 0 = X，由
   全期望公式得 E[X′] = E[X]。从第三次反弹起每个顶点都做轮盘赌；从最后一个顶点往回归纳，每个顶点的估计都保持期望，所以级数的每一项
   T^k L_e 都保持期望值（两个版本都封顶在 32 次反射，所以估计的是同一个和）。方差：E[X′² | X] = q X²/q² = X²/q，所以
   Var[X′] = E[X²/q] − E[X]² = Var[X] + E[(1/q − 1) X²]。对整个样本 F = H + T，H 是硬币之前收集的光，T 是之后的，F′ = H + I T/q，
   E[I] = q，于是 Var[F′] = Var[F] + E[(1 − q) T²/q]：q 小而 T 大时增加的方差最大，这就是 q 取路径权重（吞吐量）β 的原因：幸存者的
   权重 β/q 回到 1，被终止的路径大多是尾部本来就暗的。β = 0.73³ 时，该顶点 q = 0.389，1/q − 1 = 1.57。把 q 封顶在 0.95，意味着即使
   在白炉里，预期的后续反弹也至多 0.95/0.05 = 19 次。真正要看的是效率，即方差乘时间的倒数：在我们的检验中，均值一致
   （0.2463 ± 0.0009 对 0.2474 ± 0.0007，z = −0.95），逐像素 z 分数的均方根是 1.04，而轮盘赌把每条路径的光线数从 6.96 降到 3.16
   （少 55%），时间从 1.99 秒降到 1.06 秒。

5. **动手。** 给我们的路径追踪器加上对第二个光源的下一事件估计，并在每像素 16 个样本时测量噪声。

   *解答要点。* 在 `path.py` 中，给 `cornell_scene` 加第二个发光矩形（比如另一个 0.25 × 0.25 的正方形，放在后墙上或天花板的别处），
   把场景里唯一的 `light` 下标换成一个下标列表，由 `_pack` 打包成整数数组，并附上每个光源的面积和功率（面积乘以其辐射亮度
   换算成的亮度）。在 `_kernel` 中，在每个漫反射顶点以概率 Pⱼ 选光源 j（各 ½，或按功率成比例），像现在一样在它上面均匀取一点，把贡献
   f L_e cos θ cos θ′ A/d² V 除以 Pⱼ；或者对两个光源各发一条阴影射线，不做除法。防止光被计两次的规则必须覆盖每个被采样的光源：
   `obj != light` 改为检查一个 `is_light` 标志，深度 0 和镜面反射之后仍然计入发光；单面发光的测试 `cl > 0` 要用每个光源自己的轴和
   `rsign`。任何一个光源的这两条规则写错，它就会过亮，或者丢掉直接光，而测试能抓住这两种错误：第一次反弹的图像对发光体是线性的，
   所以两个光源时，它必须在噪声范围内等于各光源单独时第一次反弹图像之和（逐像素 z 分数接近 1，像轮盘赌检验那样）；双光源版本的
   `furnace_scene` 在每次反弹都仍须给出 L = emit/(1 − ρ)。测量时，先为新场景渲染一张 2048 spp 的参考图，再渲染 16 spp 的图像：
   (a) 只对原来的光源做 NEE，新光源靠碰运气找到；(b) 均匀地选光源；(c) 按功率选；(d) 每个顶点两个光源都采样；然后像
   `sampling_comparison` 那样比较表面上的 `rmse`、时间和效率 1/(误差² × 时间)。预计 (a) 在新光源占主导的地方噪声大得多；两个光源
   功率不同时 (c) 胜过 (b)；(d) 每条路径的误差最低，代价是两条阴影射线。

6. **★ 研究。** 方差可证明接近最优的焦散路径估计。

   *讨论。* 尚未解决。镜面–漫反射–镜面路径，例如被玻璃聚焦到地板上、又在镜子里被看到的光，对每一种局部构造路径的方法都很难：从光源
   出发的路径能打到地板，但它与眼睛的连接必须恰好沿反射方向穿过镜子；从眼睛出发的路径能经镜子到达地板，但它与光源的连接必须恰好沿
   折射方向穿过玻璃。两者都不能用一条阴影射线采到，所以无偏方法只能碰运气找到这些路径；Veach 的博士论文指出，点光源加针孔相机时，
   有些这样的路径根本无法被采样。我们自己的盒子里就有较容易的情形：镜面球反射到地板上的光（一种焦散），只有当地板上按余弦采样的一次
   反弹恰好打中镜子、再打中那个小光源时，才能到达眼睛。现有方法各有取舍：光子映射及其渐进式和顶点合并的变体是一致的，但有偏；
   Metropolis 光传输和流形探索是无偏的，但没有有用的方差界；镜面流形采样有一种无偏的形式，代价却依赖于场景。这道题要的是估计器加一个定理：
   规定允许的估计器类（无偏、每个样本至多固定次数的光线投射），任何估计器在一族场景上能达到的最好方差，以及一个在它常数倍之内的算法。
   好的部分答案可以解决一个受限的场景族，比如一个光滑的凸折射体放在漫反射平面上方、透过一面平面镜观看，并给出相匹配的下界；或者在
   这样的场景族上，证明某个现有方法的方差相对于被积函数有界。

## Glossary additions

* **homogeneous coordinates, w, clip coordinates, NDC, viewport** — points with an extra coordinate so that
  translation and perspective are matrices; the space before the division; the cube [−1, 1]³ after it; the map to
  pixels.
* **model, view and projection matrices, frustum, near and far planes, clipping** — object to world, world to eye,
  eye to clip; the truncated pyramid the camera sees; cutting triangles to it before the division.
* **depth buffer (z-buffer), window depth, z-fighting, reversed depth** — a depth per pixel; depth stored in [0, 1];
  two surfaces that round to the same depth; near at 1 and far at 0 in floating point.
* **Euler angles, gimbal lock, quaternion, slerp** — three angles about fixed axes; the lost degree of freedom when
  two axes align; four numbers for a rotation; interpolation along the great circle.
* **rasterization, edge function, top-left rule, fragment** — finding the pixels a triangle covers; the signed area
  test; the tie-break for centres on an edge; a candidate pixel with its interpolated values.
* **barycentric coordinates, perspective-correct interpolation** — a point's weights on a triangle's corners;
  interpolating a/w and 1/w, then dividing.
* **painter's algorithm** — drawing whole triangles from back to front.
* **Lambert's cosine law, Phong and Blinn–Phong models, Gouraud and Phong shading, normal matrix** — diffuse
  brightness; highlights about the mirror and the halfway vector; lighting at vertices or per pixel; the inverse
  transpose for normals.
* **aliasing, moiré, texel, mipmap, level of detail, trilinear and anisotropic filtering** — high frequencies read as
  low ones; a texture's pixel; the prefiltered pyramid; λ = log₂ ρ; blending two levels; several probes along a long
  footprint.
* **supersampling, MSAA** — several shaded samples per pixel; several coverage samples, one shader run.
* **vertex shader, fragment shader, SIMT, warp, quad, helper lane, early depth test** — the programmable stages; one
  instruction stream for many lanes; 32 lanes; a 2 × 2 block for derivatives; a lane run only to be subtracted;
  testing depth before shading.
* **ray casting, Whitted ray tracing, shadow ray, Snell's law, total internal reflection, Fresnel, Schlick's
  approximation** — the nearest hit along a ray; recursive reflection and refraction; a ray towards the light; bending
  at an interface; no refracted ray; the reflected fraction and its fifth-power fit.
* **BVH, slab test, surface area heuristic** — boxes in boxes over the objects; a ray against a box; choosing splits
  by expected cost.
* **solid angle, steradian, flux, irradiance, radiance** — area on the unit sphere; its unit; watts; watts per area;
  watts per area across the beam per steradian.
* **BRDF, albedo, reciprocity, white furnace, microfacet, GGX** — radiance out per irradiance in; the fraction
  reflected; symmetry in the two directions; the test that a surface returns at most what it receives; tiny mirrors;
  their distribution of normals.
* **rendering equation, Neumann series, direct and indirect light, colour bleeding, radiosity** — energy balance at
  every point and direction; the solution as a sum over bounces; one bounce and more; colour carried from surface to
  surface; the matte-only finite-element method.
* **path tracing, throughput, importance sampling, cosine-weighted sampling, Russian roulette** — one sampled
  direction per bounce; a path's running weight; sampling where the integrand is large; Malley's method; ending paths
  at random without bias.
* **next-event estimation, multiple importance sampling, balance and power heuristics** — a shadow ray to a point on
  the light; combining strategies with weights that sum to one; two such weightings.
* **spp, efficiency, denoising, à-trous filter, g-buffer, demodulation** — samples per pixel; 1/(error² × time);
  trading noise for bias; a sparse filter in passes; per-pixel normal, albedo and position; filtering light divided by
  albedo.
* **Bézier curve, de Casteljau's construction, Bernstein polynomials, B-spline, NURBS** — a polynomial curve from
  control points; repeated linear interpolation; its weights; smooth piecewise curves with local control; their
  rational form with uneven knots.
* **Catmull–Clark subdivision, limit surface, winding number** — refining a mesh towards a smooth surface; where
  refinement converges; how many times an outline goes round a point.
* **caustic, specular–diffuse–specular path** — light focused by mirrors or glass; a path no shadow ray can sample.
* **neural radiance field, Gaussian splatting, ReSTIR** — a network giving colour and density along rays; millions of
  rasterized Gaussians; reusing light samples across pixels and frames.

## Sources

* M. Pharr, W. Jakob and G. Humphreys, *Physically Based Rendering: From Theory to Implementation* (4th ed., 2023);
  S. Marschner and P. Shirley, *Fundamentals of Computer Graphics*; T. Akenine-Möller, E. Haines, N. Hoffman, A. Pesce,
  M. Iwanicki and S. Hillaire, *Real-Time Rendering* (4th ed., 2018); J. F. Hughes, A. van Dam, M. McGuire, D. F.
  Sklar, J. D. Foley, S. K. Feiner and K. Akeley, *Computer Graphics: Principles and Practice* (3rd ed., 2013); G.
  Farin, *Curves and Surfaces for CAGD: A Practical Guide* (5th ed., 2002).
* I. E. Sutherland, "Sketchpad: a man-machine graphical communication system", AFIPS Spring Joint Computer
  Conference 1963; A. R. Smith, "A pixel is not a little square", Microsoft Technical Memo 6 (1995).
* K. Shoemake, "Animating rotation with quaternion curves", SIGGRAPH 1985.
* I. E. Sutherland and G. W. Hodgman, "Reentrant polygon clipping", Comm. ACM 1974; E. Catmull, *A Subdivision
  Algorithm for Computer Display of Curved Surfaces*, PhD thesis, University of Utah (1974); J. Pineda, "A parallel
  algorithm for polygon rasterization", SIGGRAPH 1988.
* H. Gouraud, "Continuous shading of curved surfaces", IEEE Trans. Computers 1971; B. T. Phong, "Illumination for
  computer generated pictures", Comm. ACM 1975; J. F. Blinn, "Models of light reflection for computer synthesized
  pictures", SIGGRAPH 1977.
* L. Williams, "Pyramidal parametrics", SIGGRAPH 1983.
* A. Appel, "Some techniques for shading machine renderings of solids", AFIPS Spring Joint Computer Conference 1968;
  T. Whitted, "An improved illumination model for shaded display", Comm. ACM 1980; T. Möller and B. Trumbore, "Fast,
  minimum storage ray-triangle intersection", Journal of Graphics Tools 1997; C. Schlick, "An inexpensive BRDF model
  for physically-based rendering", Computer Graphics Forum (Eurographics) 1994.
* S. M. Rubin and T. Whitted, "A 3-dimensional representation for fast rendering of complex scenes", SIGGRAPH 1980;
  T. L. Kay and J. T. Kajiya, "Ray tracing complex scenes", SIGGRAPH 1986; J. D. MacDonald and K. S. Booth,
  "Heuristics for ray tracing using space subdivision", The Visual Computer 1990.
* F. E. Nicodemus, J. C. Richmond, J. J. Hsia, I. W. Ginsberg and T. Limperis, *Geometrical Considerations and
  Nomenclature for Reflectance*, NBS Monograph 160 (1977); R. L. Cook and K. E. Torrance, "A reflectance model for
  computer graphics", ACM TOG 1982; B. Walter, S. R. Marschner, H. Li and K. E. Torrance, "Microfacet models for
  refraction through rough surfaces", EGSR 2007.
* J. T. Kajiya, "The rendering equation", SIGGRAPH 1986; C. M. Goral, K. E. Torrance, D. P. Greenberg and B.
  Battaile, "Modeling the interaction of light between diffuse surfaces", SIGGRAPH 1984; E. Veach, *Robust Monte Carlo
  Methods for Light Transport Simulation*, PhD thesis, Stanford University (1997); E. Veach and L. J. Guibas,
  "Optimally combining sampling techniques for Monte Carlo rendering", SIGGRAPH 1995; J. Arvo and D. Kirk, "Particle
  transport and image synthesis", SIGGRAPH 1990.
* H. Dammertz, D. Sewtz, J. Hanika and H. P. A. Lensch, "Edge-avoiding À-Trous wavelet transform for fast global
  illumination filtering", High Performance Graphics 2010.
* M. G. Cox, "The numerical evaluation of B-splines", J. Inst. Maths Applics 1972; C. de Boor, "On calculating with
  B-splines", J. Approximation Theory 1972; E. Catmull and J. Clark, "Recursively generated B-spline surfaces on
  arbitrary topological meshes", Computer-Aided Design 1978; M. Halstead, M. Kass and T. DeRose, "Efficient, fair
  interpolation using Catmull–Clark surfaces", SIGGRAPH 1993; T. DeRose, M. Kass and T. Truong, "Subdivision surfaces
  in character animation", SIGGRAPH 1998.
* B. Bitterli, C. Wyman, M. Pharr, P. Shirley, A. Lefohn and W. Jarosz, "Spatiotemporal reservoir resampling for
  real-time ray tracing with dynamic direct lighting", SIGGRAPH 2020; B. Mildenhall, P. P. Srinivasan, M. Tancik,
  J. T. Barron, R. Ramamoorthi and R. Ng, "NeRF: representing scenes as neural radiance fields for view synthesis",
  ECCV 2020; B. Kerbl, G. Kopanas, T. Leimkühler and G. Drettakis, "3D Gaussian splatting for real-time radiance field
  rendering", SIGGRAPH 2023.
* For the research problem: H. W. Jensen, "Global illumination using photon maps", Eurographics Workshop on Rendering
  1996; T. Hachisuka, S. Ogaki and H. W. Jensen, "Progressive photon mapping", SIGGRAPH Asia 2008; I. Georgiev, J.
  Křivánek, T. Davidovič and P. Slusallek, "Light transport simulation with vertex connection and merging", SIGGRAPH
  Asia 2012; E. Veach and L. J. Guibas, "Metropolis light transport", SIGGRAPH 1997; W. Jakob and S. Marschner,
  "Manifold exploration", SIGGRAPH 2012; T. Zeltner, I. Georgiev and W. Jakob, "Specular manifold sampling for
  rendering high-frequency caustics and glints", SIGGRAPH 2020.
