# AI, Built — Part 4: Change

Part 4 of a twenty-part series on the mathematics of modern AI models (see [the series plan](../README.md)). Every
training step needs the derivative of the loss with respect to every number in the model: 124,439,808 for GPT-2,
4.02 billion for Qwen3-4B. This part builds the machine that computes them, the chain rule run backwards, as the
series' own small library (`explainer/ai/autodiff.py`), checks it, and trains with it. A hook and eight chapters:

* **The derivative.** Part 1's surprise curve under a magnifying lens, straightening as the zoom grows; secants
  closing on the tangent, f(x + h) ≈ f(x) + f′(x)h; eˣ, ln x, and the chain rule as stretch factors that multiply
  along three number lines.
* **The gradient.** Partial derivatives as slices of a surface (3D); the gradient, uphill; gradient descent as a
  ball rolling down; contour lines, and the slope along any direction as ∇f · u (Part 3's dot product), swept.
* **The Jacobian.** A map that bends the plane; zoomed in, its grid straightens onto the Jacobian's straight grid;
  the determinant as local area; the chain rule as a product of Jacobians.
* **Forwards or backwards.** The gradient of a chain of maps as a product of Jacobians, with their shapes; forward
  accumulation carries a column per parameter, reverse a single row; Linnainmaa (1970), Rumelhart, Hinton and
  Williams (1986).
* **Backpropagation by hand.** One input, weight and bias, a sigmoid and a squared error: values forwards
  (loss 0.854), gradients backwards (∂L/∂w = −0.259), local derivatives at each step; gradients add where a value
  is used twice.
* **The library.** Its multiplication and its `backward`, on screen as written; on a 256-number network, the gradients
  agree with finite differences to 2 × 10⁻¹⁰ and with PyTorch to 3 × 10⁻¹⁷.
* **Training.** Part 1's letter pairs as 729 scores trained by gradient descent with the library (Adam, 1,500 steps):
  from log₂ 27 = 4.75 bits to 3.33, the counting answer, the scores becoming the log of the counts (correlation 0.995).
* **Curvature.** The Hessian, its eigenvectors and eigenvalues; a bowl reshaping into a saddle (3D); a narrow valley
  (curvatures 1 and 25): gradient descent's zigzag (26 steps to within 1%), momentum, and Newton's one step.
* **Recap**, where it comes back, Part 5's teaser, references.

Run from the repo root:

```
python -m videos.ai.ai4.compute          # needs Part 1's books (.cache/ai1) and GPT-2 / Qwen3-4B's weight headers
python tools/build.py ai4                # English
python tools/build.py ai4 --lang zh      # Chinese
```

References: I. Goodfellow, Y. Bengio & A. Courville, *Deep Learning* (2016); A. Griewank & A. Walther, *Evaluating
Derivatives* (2008); J. Nocedal & S. J. Wright, *Numerical Optimization* (2006); Linnainmaa (1970); Rumelhart,
Hinton & Williams (1986); Baydin et al. (2018); Dauphin et al. (2014); Paszke et al. (2019); Karpathy, micrograd (2020).
