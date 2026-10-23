# Machine Learning Revision Projector — English Edition

Open `index.html`. Four self-contained films, one HTML file each.

| file | film | concepts | shots |
|---|---|---|---|
| `T1-Overview-and-Foundations.html` | Overview and Foundations | 6 | 26 |
| `F1-Fitting-a-Line.html` | Fitting a Line | 6 | 33 |
| `F2-Maximum-Likelihood.html` | Where Least Squares Comes From | 6 | 32 |
| `F3-Margin-and-Dual.html` | The Margin and the Dual | 7 | 39 |

Controls: `SPACE` advance · `←` back · `N` narration on/off · `1`–`9` jump to a
concept · `Home` restart. A quiz shot will not advance until you answer it.

Structure of every concept: narration shots → a four-part summary card
(**The result / Why it works / Common misreading / In your exam**) → one
mandatory question with an explanation of the answer.

## Where the mathematics comes from

Films 02–04 are original explanations of standard first-course material, written
for this edition rather than translated from any courseware. They share a running
example — the four points (1,2), (2,6), (3,5), (4,10), whose least-squares line is
y = 2.3x — so the same picture recurs across films.

- **F1** residuals → squared-error cost → convexity → the gradient and the minus
  sign → the learning rate → the normal equations.
- **F2** the Gaussian noise model → likelihood → the log → *least squares is the
  MLE* → other noise models give other losses → MAP gives ridge and lasso.
- **F3** the margin as tie-breaker → functional vs geometric margin → the primal
  quadratic programme → the Lagrangian and strong duality → complementary
  slackness and support vectors → the dual's inner products and kernels → the
  soft margin and C.

## Build

Sources are in `../源码/en/`. Each `build_*.py` reads the shared engine `eng.txt`
and writes one HTML file; run it from that directory:

```
python build_t1.py       # -> t1-ppt.html
python build_fitline.py  # -> fitline-ppt.html
python build_mle.py      # -> mle-ppt.html
python build_svm.py      # -> svm-ppt.html
```

Then copy the outputs here under their delivery names (see the table above).

## Layout budget

English runs longer than Chinese, so the frame is tighter. All numbers are in the
1280×720 frame's own units, and were measured in the smallest realistic window
(an 817×705 pane), which is the worst case — the caption panel is bottom-anchored
with a fixed 44 CSS-px margin, and in a small frame those 44px are ~69 frame units.

- the caption panel's top can fall to **y = 407** → every drawn scene element must
  end by **y ≤ 392**
- a top-anchored equation reaches **y = 230** → with one on screen, scene content
  must start at **y ≥ 240**
- `#big` is lifted 9% out of the caption band and spans roughly **y 224…365**, so a
  note sharing a shot with it goes at **y = 392**, never in between
- a `setBig` headline must fit on one line: keep it **under ~28 characters**
- a centred `note()` is 14px monospace ≈ 8.4px per character; keep it under ~88
  characters so it stays inside the frame
- a summary card holds about 11 lines: keep the four fields **under ~950
  characters combined**

## Verifying a change

Open a film and step every shot, measuring against the *actual* panel positions
rather than assumed ones. The checks that matter: scene bbox bottom vs the caption
panel top; scene bbox top vs the equation panel bottom; scene bbox vs the `#big`
panel; `#big` bottom vs the caption top; `scrollHeight > clientHeight` on the
summary and quiz panels; bbox outside x ∈ [0, 1280]; and shots that draw nothing.

Two traps when scripting this:

- `vh` is the **viewport** height, not the frame height. Frame-relative `%` is what
  you want. Both English layout regressions traced back to this.
- d3 transitions are driven by `requestAnimationFrame`, which does not run while a
  pane is not painting, so measurements can catch elements frozen at their start
  state. Force the final state first:
  `d3.selectAll('#scene *').interrupt().attr('opacity',1)`, and set `r` on circles
  and clear `stroke-dasharray`/`stroke-dashoffset` on paths before a screenshot.
