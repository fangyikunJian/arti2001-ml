# -*- coding: utf-8 -*-
"""Fitting a line: from residuals to the normal equations.
Original English film on standard first/second-year mathematics, built on the
projector engine. Outputs fitline-ppt.html.

Layout budget (English edition):
  * caption panel top sits at y = 406, so scene elements must end by y <= 395
  * a summary card has ~336 units for body text = 11 lines; keep the four
    fields under ~950 characters combined, each ideally under 250.
"""
import io
head = io.open("eng.txt", encoding="utf-8").read()
def js(t): return '"' + t.replace('\\', '\\\\').replace('"', '\\"') + '"'
C = []

C.append(r'''(function(){
var E=window.__engine;
var S=E.S,KP=E.KP,SUM=E.SUM,QUIZ=E.QUIZ,W=E.W,H=E.H,rng=E.rng;
var clearScene=E.clearScene,setTitle=E.setTitle,setBig=E.setBig,setCap=E.setCap,
    setEq=E.setEq,flip=E.flip,T=E.T,note=E.note,dots=E.dots,curve=E.curve,fn=E.fn,
    boxNode=E.boxNode,link=E.link,matrix=E.matrix,axes=E.axes,noTitle=E.noTitle;
var CFG={title:"Fitting a line · from residuals to the normal equations",
  subtitle:"residuals → cost → convexity → gradient descent → learning rate → closed form · SPACE to advance",video:""};

/* the worked dataset used throughout: x = 1,2,3,4 and y = 2,6,5,10.
   the candidate line f(x) = 1.8x + 1.2 gives residuals -1.0, +1.2, -1.6, +1.6
   (the least-squares answer for this data is y = 2.3x, so the candidate is close
   but deliberately not optimal -- and the residuals are large enough to draw).
   the plot band is 196..385: clear of a one-line equation at the top, and clear
   of the caption panel, whose top can fall to y = 407 in a small window. */
var PX=[1,2,3,4], PY=[2,6,5,10];
var AX={l:380,r:920,t:196,b:385};
function px(x){return 420+(x-1)*140;}
function py(y){return 385-(y-2)*22;}
function LINE(x){return 1.8*x+1.2;}
function plot(){ axes(AX);
  note("x",934,382,"");note("y",368,190,"");
  var p=[];for(var i=0;i<4;i++)p.push([px(PX[i]),py(PY[i])]);
  return p; }
/* blue = the data, yellow = the candidate under examination, coral = the error */
function candidate(){ curve([[px(0.85),py(LINE(0.85))],[px(4.25),py(LINE(4.25))]],"fit y"); }
''')


def KP(name, shots, summ, quiz):
    b = ['KP(%s,function(){' % js(name)]
    for scene, narr in shots:
        b.append('  S(0,function(){%s},%s);' % (scene, js(narr)))
    fields = ",".join('%s:%s' % (k, js(v)) for k, v in summ.items() if v and k != 'kp')
    b.append('  SUM(0,%d,{%s});' % (summ['kp'], fields))
    opts = ",".join(js(o) for o in quiz['o'])
    b.append('  QUIZ(0,%d,{t:%s,o:[%s],a:%d,w:%s});' % (quiz['kp'], js(quiz['t']), opts, quiz['a'], js(quiz['w'])))
    b.append('});'); C.append("\n".join(b))


C.append(r'''KP("Opening",function(){
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);
    setTitle("Fitting a line","From residuals to the normal equations",
      "One question, six steps: what does the best line even mean?");},
    "Every idea in this film comes from one ordinary question: <b>given a cloud of points, which straight line is the best one?</b> The interesting part is that the question is not well posed until we <em>define</em> what \"best\" means, and once we do, the rest is calculus and linear algebra you already have. Six steps: <b>measure the error on one point (residual) &rarr; compress the whole line into one number (cost) &rarr; look at the shape of that number (convexity) &rarr; walk downhill on it (gradient descent) &rarr; choose the step size (learning rate) &rarr; and finally solve it in one shot (normal equations)</b>. Press N at any time to toggle this narration.");
});''')

# ── KP1 · residuals ─────────────────────────────────────────────────
KP("1 · The residual: error at a single point",
   [('clearScene();setEq(null);setBig(null);'
     'var p=plot();dots(p,"a",5);candidate();'
     'note("a candidate line",600,246,"y");'
     'setCap("<b>Four data points and one candidate line. How wrong is it?</b>");',
     "Here are four measurements and one candidate straight line. Before we can ask which line is <em>best</em>, we need to say how wrong a given line is -- and the honest place to start is a single point. <b>The residual of point i is the vertical gap between the value we observed and the value the line predicts</b>: e&#7522; = y&#7522; &minus; f(x&#7522;). Notice the word <b>vertical</b>. We are not measuring the shortest distance from the point to the line; we are measuring the error <em>in the thing we are trying to predict</em>, which is y."),
    ('clearScene();setEq("$$e_i = y_i - f(x_i)$$","top");'
     'var p=plot();dots(p,"a",5);candidate();'
     'for(var i=0;i<4;i++){var q=p[i];link(q[0],py(LINE(PX[i])),q[0],q[1],"r");}'
     'note("residual",716,306,"r","start");',
     "Drawn in, the residuals are the little vertical bars. <b>The sign carries information</b>: a positive residual means the observation sits <em>above</em> the line, so the model <b>under-predicted</b>; a negative residual means the model <b>over-predicted</b>. With f(x) = 1.8x + 1.2 on this data the four residuals are &minus;1.0, +1.2, &minus;1.6 and +1.6. <s>A common slip is to read the sign backwards</s> -- it is observed minus predicted, so negative means the prediction was too high."),
    ('clearScene();setEq(null);setBig("Vertical, not perpendicular","because the quantity we predict is y");'
     'note("perpendicular distance would charge us for error in x as well -- but x is given",640,392,"y");',
     "Why the vertical gap rather than the perpendicular distance to the line? Because of what the model is <em>for</em>. We are handed x and asked to produce y; the x value is not in question. <b>Perpendicular distance would charge the model for error in x too</b>, which is not the task. (There is a genuine technique that does exactly that -- total least squares -- and it is the right tool when both variables are measured with noise. It is a different problem from ordinary regression.)")],
   {'kp':1,'h':"The residual: how wrong one point is",
    'k':"The residual is the <b>vertical</b> gap between observation and prediction: <b>e&#7522; = y&#7522; &minus; f(x&#7522;)</b>. Positive means the model under-predicted; negative means it over-predicted.",
    'm':"Vertical rather than perpendicular because the model's job is to produce y from a given x. Perpendicular distance would also charge for error in x, which is a different problem (total least squares).",
    'w':"<s>Do not read the sign backwards.</s> It is observed minus predicted, so a negative residual means the prediction was too <em>high</em>.",
    'e':"Everything downstream is built on this one quantity: the cost function squares it, the gradient is proportional to it, and the normal equations set its weighted sum to zero."},
   {'kp':1,'t':"An observation has y = 145 while the line predicts 150. What is the residual, and what does it say?",
    'o':["+5, the model under-predicted",
         "<b>&minus;5, the model over-predicted</b>",
         "5, with no direction","0, because the two are close"],
    'a':1,
    'w':"The residual is observed minus predicted: 145 &minus; 150 = <b>&minus;5</b>. <b>The negative sign says the prediction was too high</b> -- the line sits above this point. A positive residual would mean the point sits above the line and the model under-predicted. Reading this sign correctly matters, because the gradient inherits it."})

# ── KP2 · cost function ─────────────────────────────────────────────
KP("2 · ★ From many residuals to one number",
   [('clearScene();setEq(null);setBig(null);'
     'boxNode(140,150,460,80,"residuals: +3 and −3","b");'
     'boxNode(700,150,440,80,"their sum: 0","r");'
     'link(600,190,700,190);'
     'note("a badly wrong line can score a perfect zero",640,290,"r");'
     'note("so we cannot simply add the residuals up",640,344,"y");',
     "To compare whole lines we need <em>one</em> number per line, not a list of residuals. The obvious move -- add them up -- fails immediately. <b>Residuals carry signs, so they cancel.</b> A line that misses one point by +3 and another by &minus;3 scores a sum of exactly zero, tying with a line that passes through both perfectly. Any honest measure of total error has to remove the signs first."),
    ('clearScene();setEq("$$J(w,b)=\\\\frac{1}{2m}\\\\sum_{i=1}^{m}\\\\big(f(x_i)-y_i\\\\big)^2$$","top");'
     'setCap("<b>Square each residual, then average. Smaller is better.</b>");'
     'note("squaring kills the sign AND punishes big misses harder",640,300,"g");'
     'note("miss by 10 → charged 100.   miss by 2 → charged 4.",640,350,"");',
     "Squaring fixes it, and does something extra worth noticing. <b>It removes the sign, and it punishes large errors disproportionately</b>: a miss of 10 is charged 100 while a miss of 2 is charged only 4. That is a real modelling choice, not a neutral one -- it is why least squares is <em>sensitive to outliers</em>. If a single wild point should not dominate the fit, absolute error or a robust loss is the better tool. We average over the m points so the number does not grow simply because the dataset is larger."),
    ('clearScene();setEq("$$\\\\tfrac{d}{du}\\\\Big[\\\\tfrac{1}{2}u^2\\\\Big]=u$$","top");'
     'setBig(null);setCap("<b>The one-half is bookkeeping: it cancels the 2 that differentiation produces.</b>");'
     'note("it changes the height of J, never the location of its minimum",640,330,"y");',
     "The factor of one-half in front looks arbitrary and is purely cosmetic. <b>Differentiating a square produces a factor of 2, and the one-half absorbs it</b>, leaving clean gradients later. Multiplying an objective by any positive constant <em>changes its height but never the location of its minimum</em>, so the fitted line is identical with or without it. Different textbooks make different choices here; only the constant in front of the gradient changes.")],
   {'kp':2,'h':"★ The cost function: one number per line",
    'k':"Residuals cancel if you add them, so we <b>square and average</b>: J(w,b) = (1/2m)&Sigma;(f(x&#7522;) &minus; y&#7522;)&sup2;. Smaller is better, and learning becomes <b>minimise J</b>.",
    'm':"Squaring removes the sign <em>and</em> charges large misses disproportionately (10 costs 100, 2 costs 4) -- which is exactly why least squares is sensitive to outliers. The &frac12; is bookkeeping: it cancels the 2 that differentiation produces.",
    'w':"<s>The &frac12; is not a modelling decision.</s> Scaling an objective by a positive constant moves its height, never its minimiser -- the fitted line is unchanged.",
    'e':"This is the template for the whole subject: define a loss, then minimise it. Only the loss changes from model to model."},
   {'kp':2,'t':"Why square the residuals instead of just adding them?",
    'o':["Squaring makes the arithmetic easier",
         "<b>Because residuals have signs and would cancel -- a line missing by +3 and &minus;3 would score zero</b>",
         "To make J differentiable, which addition is not",
         "Because it guarantees the fit is unique"],
    'a':1,
    'w':"The decisive reason is <b>cancellation</b>: a plain sum lets a badly wrong line score zero, so it cannot rank lines at all. Squaring removes the sign and, as a side effect, <em>weights large errors more heavily</em>. Taking absolute values would also fix the cancellation, and is used when outliers should not dominate -- squares are preferred here largely because they are smooth and easy to differentiate."})

# ── KP3 · convexity ─────────────────────────────────────────────────
KP("3 · ★ The shape of J: a bowl",
   [('clearScene();setEq(null);setBig(null);'
     'var P={l:340,r:960,t:120,b:340};axes(P);'
     'note("parameter w",950,364,"");note("J(w)",332,132,"");'
     'var pts=[];for(var k=0;k<=60;k++){var x=340+620*k/60,t=(k-32)/30;pts.push([x,150+t*t*180]);}'
     'curve(pts,"fit b");dots([[671,150]],"g",9);'
     'note("the minimum: the best parameter",671,132,"g");',
     "Now change what the axes mean. <b>The horizontal axis is no longer data -- it is a parameter</b>, and the vertical axis is J, the cost that parameter produces. This is a map of parameter space, not of the data. <b>A whole line in the data picture is a single point on this curve.</b> Getting this straight is the single most useful mental move in the topic: fitting is <em>navigating this surface</em>, and every candidate line is one location on it."),
    ('clearScene();setEq(null);setBig("Convex: exactly one minimum","a local minimum is therefore the global one");'
     'note("from any starting point, walking downhill arrives at the same place",640,392,"g");',
     "For squared error with a linear model this bowl is <b>convex</b> -- it curves upward everywhere and has a single lowest point. That is a strong guarantee: <b>any local minimum is automatically the global minimum</b>, so a downhill walk from <em>any</em> starting point ends at the same answer. The initial guess and the random seed cannot change the result. This is emphatically not true in general; a neural network's cost surface is riddled with dips, which is one reason those models are harder to train reliably."),
    ('clearScene();setEq(null);setBig(null);'
     'var P={l:360,r:940,t:110,b:350};axes(P);'
     'note("w",930,374,"");note("b",352,122,"");'
     'var cx=650,cy=228;for(var r=34;r<=140;r+=34){var e=[];'
     'for(var a=0;a<=48;a++){var t=a/48*6.283;e.push([cx+r*1.92*Math.cos(t),cy+r*0.40*Math.sin(t)]);}'
     'curve(e,"fit");}dots([[cx,cy]],"g",9);'
     'note("long thin contours → downhill zig-zags → slow going",640,392,"y");',
     "With two parameters the bowl lives in three dimensions, and we usually draw it flattened, as <b>contours</b> -- each ring is a set of parameters giving the same cost. When the rings come out as long thin ellipses rather than circles, it tells you the parameters are strongly coupled, often because the <em>features live on very different scales</em>. The practical consequence appears in the next step: <b>a downhill walk across a narrow valley zig-zags across it instead of running along it</b>, and convergence crawls. Rescaling the features rounds the contours out and fixes this.")],
   {'kp':3,'h':"★ Convexity: the cost surface is a bowl",
    'k':"Plot J against the <b>parameters</b> and you get a bowl. The axes are parameter space, not data space: <b>an entire line in the data picture is one point here</b>.",
    'm':"Squared error with a linear model is <b>convex</b>, so there is exactly one minimum and any local minimum is the global one -- a downhill walk from any starting point lands on the same answer. Non-convex surfaces (neural networks) give no such guarantee.",
    'w':"<s>Do not read this as a plot of the data.</s> Mixing up data space and parameter space makes every later picture confusing.",
    'e':"Convexity is why the closed-form solution and the iterative one agree, and why long thin contours predict slow convergence."},
   {'kp':3,'t':"What does convexity of the cost surface actually guarantee?",
    'o':["That training will be fast",
         "<b>That there is a single minimum, so a downhill walk from any starting point reaches the same optimum</b>",
         "That the model will not overfit",
         "That no learning rate is needed"],
    'a':1,
    'w':"Convexity is a statement about <b>shape</b>, not speed. One lowest point means <em>no bad local minima to be trapped in</em>, so the starting point cannot change the answer. Speed is governed by the learning rate and the shape of the contours; overfitting is about model capacity versus data, an entirely separate question."})

# ── KP4 · the gradient ──────────────────────────────────────────────
KP("4 · ★★ The gradient, and why we subtract it",
   [('clearScene();setEq("$$\\\\nabla J=\\\\Big[\\\\frac{\\\\partial J}{\\\\partial w},\\\\ \\\\frac{\\\\partial J}{\\\\partial b}\\\\Big]$$","top");'
     'setCap("<b>One partial derivative per parameter, collected into a vector.</b>");'
     'note("each partial answers: if I nudge THIS parameter and hold the rest still, how fast does J change?",640,300,"");'
     'note("the vector points in the direction of steepest INCREASE",640,352,"y");',
     "A partial derivative answers a narrow question: <b>if I nudge this one parameter and hold the others fixed, how fast does J change?</b> Collect one per parameter into a vector and you have the <b>gradient</b>. Its direction is the key fact: <b>the gradient points in the direction of steepest <em>increase</em></b>. Its length says how steep the slope is there. On a flat plateau it is near zero; on a cliff it is long."),
    ('clearScene();setEq("$$w := w-\\\\alpha\\\\frac{\\\\partial J}{\\\\partial w}, \\\\qquad b := b-\\\\alpha\\\\frac{\\\\partial J}{\\\\partial b}$$","top");'
     'setBig(null);setCap("<b>We want to go down, so we step against the gradient. That is the whole of the minus sign.</b>");'
     'note("α sets how far to step; := means compute, then overwrite",640,320,"");',
     "We want J smaller, and the gradient points the way it gets <em>bigger</em> -- so we step in the opposite direction. <b>That is the entire meaning of the minus sign</b>, and it is worth being able to say out loud in one breath. The step size &alpha; is ours to choose. One quiet virtue of the rule: because the gradient shortens as the surface flattens, <b>the steps shrink automatically near the bottom</b> without anyone arranging it."),
    ('clearScene();setEq(null);setBig("Update both at once","compute every partial from the OLD values, then overwrite");'
     'note("updating w first and then using the new w to compute ∂J/∂b is a different algorithm",640,392,"r");',
     "One detail that is easy to get wrong in code. <b>Evaluate every partial derivative using the current parameters, store the results, and only then write them all back.</b> If you update w and immediately use that new w while computing the partial for b, you are no longer stepping along the gradient of J at the point you started from. It often still converges, which is exactly what makes the bug hard to notice."),
    ('clearScene();setEq("$$\\\\frac{\\\\partial J}{\\\\partial w}=\\\\frac{1}{m}\\\\sum_{i=1}^{m}\\\\big(f(x_i)-y_i\\\\big)\\\\,x_i$$","top");'
     'setCap("<b>Work it through and the gradient reads: error × feature, averaged.</b>");'
     'note("large error on a large feature value moves that weight most",640,306,"g");'
     'note("the same shape reappears in logistic regression and the perceptron",640,358,"v");',
     "Differentiating the cost with the chain rule gives something pleasingly interpretable: <b>the gradient is the average of (error &times; feature)</b>. A point the model gets badly wrong contributes a lot; a point it already fits contributes nothing. And the contribution is weighted by the feature value, so <em>a large error on a large input moves that weight the most</em>. This shape -- error times input -- is not an accident of squared loss. The same form appears in logistic regression and the perceptron, because all three sit inside the same family of models.")],
   {'kp':4,'h':"★★ The gradient and the minus sign",
    'k':"The gradient collects one partial derivative per parameter and <b>points in the direction of steepest increase</b>. We want a decrease, so we step against it: <b>w := w &minus; &alpha;&part;J/&part;w</b>.",
    'm':"For squared error the gradient works out to <b>the average of (error &times; feature)</b>: badly-fitted points contribute most, well-fitted points contribute nothing. Steps shrink automatically near the minimum because the gradient shortens there.",
    'w':"<s>Update the parameters simultaneously.</s> Computing one partial, writing it back, then using the new value for the next partial is a different algorithm -- and it often still converges, which hides the bug.",
    'e':"The error-times-feature form recurs across the linear family, so recognising it here pays off later."},
   {'kp':4,'t':"Why does the update rule subtract the gradient rather than add it?",
    'o':["To keep the parameters small",
         "<b>The gradient points towards steepest increase, so the opposite direction is steepest decrease</b>",
         "To make the algorithm converge faster",
         "Either sign works; the convention is arbitrary"],
    'a':1,
    'w':"The gradient is the direction of steepest <em>ascent</em>. Minimising means going the other way, so the update steps against it. <b>Adding the gradient would climb the bowl</b> and drive the cost up -- which is precisely what gradient <em>ascent</em> does when the goal is to maximise something instead."})

# ── KP5 · learning rate ─────────────────────────────────────────────
KP("5 · ★ Choosing the step size",
   [('clearScene();setEq(null);setBig(null);'
     'boxNode(90,140,320,96,"α too small","b");'
     'boxNode(480,140,300,96,"α about right","g");'
     'boxNode(850,140,320,96,"α too large","r");'
     'note("converges, but wastes enormous effort",250,272,"b");'
     'note("fast and stable",630,272,"g");'
     'note("overshoots, oscillates, may diverge",1010,272,"r");'
     'note("α is chosen by you -- it is not learned from the data",640,352,"y");',
     "The step size &alpha; is a <b>hyper-parameter</b>: you pick it, the data does not. Too small and the method still converges, but takes far more iterations than it needs. Too large and each step <em>jumps past</em> the minimum and lands higher on the far wall, so the cost oscillates and can grow without bound. There is no universal value; sensible practice is to try a few orders of magnitude -- 0.001, 0.01, 0.1 -- and watch what happens."),
    ('clearScene();setEq(null);setBig(null);'
     'var P={l:300,r:980,t:110,b:330};axes(P);'
     'note("iteration",968,354,"");note("J",292,122,"");'
     'var a=[];for(var k=0;k<=60;k++)a.push([300+680*k/60,120+200*Math.exp(-k/9)]);curve(a,"fit g");'
     'var b=[];for(var k=0;k<=60;k++)b.push([300+680*k/60,120+200*Math.exp(-k/70)]);curve(b,"fit");'
     'note("healthy: drops fast, then flattens",640,372,"g");'
     'note("barely moving: α too small",640,392,"b");',
     "The practical diagnostic is to <b>plot J against the iteration count</b> and read the shape. A healthy run falls steeply and then flattens. A curve that descends almost imperceptibly says &alpha; is too small. A curve that jumps around or trends upward says &alpha; is too large -- and that one is unambiguous, because with a correct implementation and a sensible step size <b>the cost should never increase</b>."),
    ('clearScene();setEq(null);setBig("Flat but high is not α","the walk has converged; the model is the limitation");'
     'note("a line simply cannot fit a curve, however long you train it",640,392,"y");',
     "One trap worth naming. If the cost falls, flattens, and settles at a value that still seems large, it is tempting to blame &alpha;. <b>Flattening means the optimiser has arrived</b> -- it has found the bottom of the bowl it was given. A high floor says the bowl itself is high: the model is too simple for the data, or the features do not carry the information. <em>A straight line cannot fit a curve no matter how patiently you descend.</em> That is a modelling problem, not an optimisation one.")],
   {'kp':5,'h':"★ The learning rate",
    'k':"&alpha; is a <b>hyper-parameter you choose</b>. Too small converges but wastes iterations; too large overshoots the minimum, oscillates and can diverge. Try a few orders of magnitude and compare.",
    'm':"Diagnose by <b>plotting J against iteration</b>: a steep fall then a flattening is healthy; a barely-moving curve means &alpha; is too small; a rising or jumping curve means it is too large. With a correct implementation the cost should never rise.",
    'w':"<s>Flat but high is not a learning-rate fault.</s> Flattening means the optimiser converged; a high floor points at the model or the features.",
    'e':"Long thin contours from the previous concept are the other cause of slow progress -- and the fix there is rescaling the features, not changing &alpha;."},
   {'kp':5,'t':"Training cost falls quickly, flattens, and stays at a value you consider too high. What does this most likely indicate?",
    'o':["The learning rate is too small",
         "The learning rate is too large",
         "<b>The optimiser has converged; the model or the features are the limitation</b>",
         "The gradient was computed with the wrong sign"],
    'a':2,
    'w':"<b>Flattening is the signature of convergence</b> -- the walk has reached the bottom of its bowl. If that bottom is high, the bowl is high: the model is too simple to represent the pattern, or the inputs do not carry the necessary information. Too small an &alpha; produces a curve that is <em>still descending</em>, and too large produces one that jumps or rises."})

# ── KP6 · normal equations ──────────────────────────────────────────
KP("6 · ★★ Solving it in one step",
   [('clearScene();setEq("$$\\\\nabla J(\\\\theta)=0$$","top");'
     'setBig(null);setCap("<b>The bowl has one bottom, and at the bottom the slope is zero.</b>");'
     'note("so instead of walking downhill, solve for the flat point directly",640,300,"g");'
     'note("this works because the cost is quadratic in the parameters",640,352,"y");',
     "Descending step by step is not the only option. The surface is a bowl with exactly one lowest point, and <b>at that point the slope in every direction is zero</b>. So rather than walking, we can set the gradient to zero and <em>solve</em> for the parameters. This shortcut exists because the cost is <b>quadratic</b> in the parameters, which makes setting the gradient to zero a system of <em>linear</em> equations -- and linear systems we know how to solve exactly."),
    ('clearScene();setEq("$$X^{\\\\top}X\\\\,\\\\theta = X^{\\\\top}y \\\\;\\\\Longrightarrow\\\\; \\\\theta=(X^{\\\\top}X)^{-1}X^{\\\\top}y$$","top");'
     'setCap("<b>The normal equations: one matrix expression, no iteration, no step size.</b>");'
     'note("X stacks the inputs one row per observation, with a column of ones for the intercept",640,300,"");'
     'note("needs X to have full column rank, so that X^T X can be inverted",640,352,"r");',
     "Writing the data as a matrix X -- one row per observation, plus a column of ones so the intercept comes along for the ride -- the stationarity condition becomes <b>X<sup>T</sup>X&theta; = X<sup>T</sup>y</b>, and hence &theta; = (X<sup>T</sup>X)<sup>&minus;1</sup>X<sup>T</sup>y. <b>No iterations, no learning rate, no convergence to monitor.</b> There is a condition: X<sup>T</sup>X must be invertible, which requires the columns of X to be <b>linearly independent</b>. Duplicate a feature, or include one that is an exact combination of others, and the inverse does not exist -- the geometric reading being that the data cannot distinguish those parameters."),
    ('clearScene();setEq(null);setBig(null);'
     'matrix({rows:4,cols:3,cw:330,ch:58,x:105,y:120,'
     'cell:function(i,j){var t=[["","Closed form","Gradient descent"],'
     '["Cost","one matrix inverse","many cheap iterations"],'
     '["Scales to many features","poorly","well"],'
     '["Needs a step size","no","yes"]];return t[i][j];},'
     'hl:function(i,j){return i===0?"hl":"";},dim:function(i,j){return i===0||j===0;}});'
     'note("few features → solve it. many features, or no closed form → descend.",640,368,"y");',
     "So which one should you use? <b>With a modest number of features, solve it directly</b> -- it is exact and there is nothing to tune. Inverting X<sup>T</sup>X costs roughly the cube of the number of features, so as that number grows into the thousands the direct route becomes unattractive and <b>iteration wins</b>. And the deeper reason gradient descent is the method worth learning: <em>most models have no closed form at all</em>. Logistic regression does not. Neural networks do not. Linear regression is the unusually generous case where both roads lead to the same place.")],
   {'kp':6,'h':"★★ The normal equations",
    'k':"At the bottom of the bowl the gradient vanishes. Setting <b>&nabla;J = 0</b> gives a linear system, <b>X<sup>T</sup>X&theta; = X<sup>T</sup>y</b>, so &theta; = (X<sup>T</sup>X)<sup>&minus;1</sup>X<sup>T</sup>y -- exact, with no iteration and no step size.",
    'm':"This works only because the cost is <b>quadratic</b> in the parameters. It needs X<sup>T</sup>X invertible, i.e. the columns of X <b>linearly independent</b>: a duplicated or perfectly collinear feature destroys the inverse, because the data cannot separate those parameters.",
    'w':"<s>The closed form is not simply the better method.</s> Inversion costs about the cube of the feature count, and <b>most models have no closed form at all</b> -- logistic regression and neural networks among them.",
    'e':"Few features: solve directly. Many features, or a model without a closed form: descend. Both give the same answer here because the surface is convex."},
   {'kp':6,'t':"Two of the columns of X are identical. What goes wrong with &theta; = (X<sup>T</sup>X)<sup>&minus;1</sup>X<sup>T</sup>y?",
    'o':["Nothing; duplicated columns are harmless",
         "<b>X<sup>T</sup>X is singular and cannot be inverted -- the data cannot distinguish the two parameters</b>",
         "The answer is correct but takes longer to compute",
         "The cost function stops being convex"],
    'a':1,
    'w':"Identical columns are <b>linearly dependent</b>, so X<sup>T</sup>X is singular and has no inverse. The reading behind the algebra: if two inputs are indistinguishable, then shifting weight from one to the other changes nothing, so <em>infinitely many parameter vectors achieve the same minimum cost</em> and no unique solution exists. The surface stays convex -- it simply has a flat valley floor rather than a single lowest point. Gradient descent will still return one of the equally-good answers."})

C.append(r'''KP("End · the six steps",function(){
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("Fitting a line · complete","One question answered six ways",
      "residual → cost → bowl → gradient → step size → closed form");},
    "Six steps, and every one of them recurs far beyond straight lines. <b>(1)</b> The <b>residual</b> y &minus; f(x) measures one point, vertically, because y is what we predict. <b>(2)</b> Squaring and averaging turns a list of residuals into a single <b>cost</b>, at the price of sensitivity to outliers; the &frac12; is bookkeeping. <b>(3)</b> Seen as a function of the parameters that cost is a <b>convex bowl</b>, so a local minimum is the global one -- and long thin contours warn of slow progress. <b>(4)</b> The <b>gradient</b> points uphill, so we step against it, updating all parameters together; for squared error it reduces to <em>error times feature</em>. <b>(5)</b> The <b>learning rate</b> is yours to choose -- diagnose it from the cost-versus-iteration curve, and remember that flat-but-high indicts the model, not the step size. <b>(6)</b> Because the cost is quadratic we can set the gradient to zero and solve the <b>normal equations</b> outright, provided the columns of X are independent. Linear regression is the rare model where walking and solving both arrive at the same point.");
});
window.__startProjector(CFG);
})();''')

body = "\n".join(C)
full = head + "<script>\n" + body + "\n</script>\n"
full = full.replace("<title>Projector</title>", "<title>Fitting a Line</title>")
io.open("fitline-ppt.html", "w", encoding="utf-8").write(full)
print("fitline-ppt.html written:", len(full), "chars;", body.count("KP("), "KP;",
      body.count("SUM("), "SUM;", body.count("QUIZ("), "QUIZ;", body.count("S(0,function"), "shots")
