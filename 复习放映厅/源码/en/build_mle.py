# -*- coding: utf-8 -*-
"""Where least squares comes from: maximum likelihood.
Original English film on standard mathematics, built on the projector engine.
Outputs mle-ppt.html.

Layout budget, measured at the tightest realistic window (817x705 pane):
  * caption panel top falls to y = 407  ->  scene content must end by y <= 392
  * a top-anchored equation reaches y = 225  ->  with one on screen, scene
    content must start at y >= 235
  * #big is vertically centred and can span y 251..469, so a note sharing a
    shot with it belongs above, at y ~= 228
  * four summary fields under ~950 characters combined
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
var CFG={title:"Where least squares comes from · maximum likelihood",
  subtitle:"noise model → likelihood → log → the squares fall out · SPACE to advance",video:""};

/* the same four points as the fitting film, now with their least-squares line y = 2.3x */
var PX=[1,2,3,4], PY=[2,6,5,10];
var AX={l:380,r:920,t:196,b:385};
function px(x){return 420+(x-1)*140;}
function py(y){return 385-(y-2)*22;}
function FIT(x){return 2.3*x;}
function plot(){ axes(AX);
  note("x",934,382,"");note("y",368,190,"");
  var p=[];for(var i=0;i<4;i++)p.push([px(PX[i]),py(PY[i])]);
  return p; }
function fitline(){ curve([[px(0.9),py(FIT(0.9))],[px(4.25),py(FIT(4.25))]],"fit"); }
/* a sideways gaussian hugging the vertical line x = x0: the noise around one prediction */
function bell(x0,cls,amp){ var X=px(x0),Y=py(FIT(x0)),b=[];
  for(var t=-64;t<=64;t+=2) b.push([X+(amp||72)*Math.exp(-t*t/1352), Y+t]);
  curve(b,cls||"fit g"); return [X,Y]; }
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
    setTitle("Where least squares comes from","Maximum likelihood",
      "We chose to square the errors. Was that arbitrary?");},
    "In the fitting film we squared the residuals because signs cancel and squares are smooth. Both true, and both a little unsatisfying: <b>they are reasons to prefer squares, not a derivation of them.</b> This film gives the derivation. We make one honest assumption about how the data was generated, ask which parameters make the data we actually saw most probable, and <b>the sum of squared errors falls out on its own</b> -- nobody chooses it. Along the way the assumption becomes visible, which is the real prize: once you can see it, you can see when it fails and what to use instead. Press N to toggle this narration.");
});''')

# ── KP1 · the noise model ───────────────────────────────────────────
KP("1 · An honest model of the noise",
   [('clearScene();setEq(null);setBig(null);'
     'var p=plot();dots(p,"a",5);fitline();'
     'setCap("<b>The points do not sit on the line. So say something about how they miss it.</b>");',
     "Real data never lies on a line, and until now we treated that as an inconvenience to be minimised. <b>Maximum likelihood treats it as information.</b> Instead of asking which line passes closest to the points, we write down a story for how the points were produced: a straight-line relationship, plus a random disturbance for everything the model does not capture -- measurement error, omitted variables, ordinary noise. Once that story is written as a formula we can ask a much sharper question: <em>which line makes the data we actually observed the most probable?</em>"),
    ('clearScene();setEq("$$y^{(i)}=\\\\theta^{\\\\top}x^{(i)}+\\\\varepsilon^{(i)},\\\\qquad \\\\varepsilon^{(i)}\\\\sim\\\\mathcal{N}(0,\\\\sigma^2)$$","top");'
     'var p=plot();dots(p,"a",5);fitline();bell(3,"fit g");'
     'note("the noise around one prediction",790,286,"g","start");',
     "Here is the story in symbols. Each observation is the line's value plus a disturbance drawn from a <b>normal distribution centred on zero</b>. The bell drawn sideways at x = 3 is that distribution: the line gives the mean, and the noise scatters the observation above or below it. Two conditions come attached. <b>Zero mean</b> says the model is not systematically high or low. <b>The same &sigma; for every point, drawn independently</b>, says the noise does not grow with x and that one point's error tells you nothing about the next one's."),
    ('clearScene();setEq(null);setBig("Why a normal distribution?","many small independent effects add up");'
     'note("the central limit theorem makes it the natural default -- not a law of nature",640,392,"y");',
     "Why normal, of all the distributions available? The honest answer is <b>convenience backed by a theorem</b>. The central limit theorem says that a sum of many small independent effects tends towards a normal distribution, and \"everything I left out of the model\" is often exactly such a sum. That makes it a reasonable default. <s>It is not a law of nature</s>, and the assumption is testable: plot the residuals and look. If they fan out as x grows, or a few sit absurdly far out, the story is wrong and the method built on it will mislead you.")],
   {'kp':1,'h':"An honest model of the noise",
    'k':"Write down how the data was <b>generated</b>: y = &theta;&#7488;x + &epsilon; with &epsilon; drawn from <b>N(0, &sigma;&sup2;)</b>, independently and with the same &sigma; for every point.",
    'm':"Zero mean says the model is not systematically high or low; a shared &sigma; says the noise does not grow with x; independence says one point's error predicts nothing about the next. The normal shape is justified by the central limit theorem -- many small independent effects add up.",
    'w':"<s>This is an assumption, not a fact.</s> It is testable: plot the residuals and look for fanning-out or extreme outliers.",
    'e':"Everything that follows is a consequence of this line. Change the noise distribution and you change the loss function."},
   {'kp':1,'t':"What does the assumption &epsilon; ~ N(0, &sigma;&sup2;) with the same &sigma; for all i actually claim?",
    'o':["That the data lies exactly on a straight line",
         "<b>That the noise is centred on zero, equally spread at every x, and independent across observations</b>",
         "That &theta; is a random variable with a normal distribution",
         "That the residuals must sum to exactly zero"],
    'a':1,
    'w':"The three claims are <b>zero mean</b> (no systematic bias), <b>constant variance</b> (spread does not change with x -- called homoscedasticity), and <b>independence</b>. Note what it does <em>not</em> say: &theta; is treated as a fixed unknown constant, not a random variable. Treating &theta; as random is the Bayesian move, and it leads somewhere different -- to MAP estimation and regularisation."})

# ── KP2 · likelihood ────────────────────────────────────────────────
KP("2 · ★ Likelihood: the same formula read backwards",
   [('clearScene();setEq(null);setBig(null);'
     'boxNode(105,150,470,104,"probability","b");'
     'boxNode(700,150,470,104,"likelihood","y");'
     'link(575,202,700,202);'
     'note("θ fixed, data varies",340,290,"b");'
     'note("data fixed, θ varies",935,290,"y");'
     'note("one formula, two readings -- and only one of them is a probability",640,352,"");',
     "Now the move that gives the method its name, and the one place people reliably get lost. <b>We have a single formula, and we read it two different ways.</b> Read with &theta; fixed and the data varying, it is a probability: it tells you how likely various datasets are. Read with <b>the data fixed at what we actually observed and &theta; varying</b>, it becomes a function of the parameters -- the likelihood. Same expression, opposite roles. The data has already happened; the parameters are what we are searching over."),
    ('clearScene();setEq("$$L(\\\\theta)=\\\\prod_{i=1}^{m}\\\\frac{1}{\\\\sqrt{2\\\\pi}\\\\,\\\\sigma}\\\\exp\\\\!\\\\left(-\\\\frac{(y^{(i)}-\\\\theta^{\\\\top}x^{(i)})^2}{2\\\\sigma^2}\\\\right)$$","top");'
     'setCap("<b>Independence is what lets us multiply. Every point contributes a factor.</b>");'
     'note("a parameter that explains every point well makes this product large",640,340,"g");',
     "Because the points are assumed independent, the probability of seeing all of them together is the <b>product</b> of the individual probabilities -- that is exactly what independence buys us. Look at what each factor rewards: the exponent contains the squared residual with a minus sign, so <em>a point the line explains well contributes a factor close to its maximum, and a badly explained point contributes a tiny one</em>. Maximising this product means finding the &theta; under which the observed data is least surprising."),
    ('clearScene();setEq(null);setBig("L(θ) is not a probability","the data has happened; θ is not random here");'
     'note("it does not integrate to one over θ, and asking P(θ | data) needs a prior",640,392,"r");',
     "One correction worth making early, because it stays with you. <b>L(&theta;) is not a probability distribution over &theta;.</b> It does not integrate to one over the parameters, and a value of 0.03 does not mean \"a 3% chance this &theta; is right\". It is a <em>score</em>: how well each candidate &theta; accounts for the data we hold. The question \"what is the probability of &theta; given the data?\" is a perfectly good question, but answering it requires a prior over &theta; and Bayes' rule -- a different framework, which we will meet at the end of this film.")],
   {'kp':2,'h':"★ Likelihood: one formula, read backwards",
    'k':"The same expression is a <b>probability</b> when &theta; is fixed and the data varies, and a <b>likelihood</b> when the data is fixed and &theta; varies. Independence lets us multiply one factor per observation.",
    'm':"Each factor holds exp(&minus;residual&sup2;/2&sigma;&sup2;), so a well-explained point contributes a large factor and a badly explained one contributes almost nothing. Maximising the product finds the &theta; that makes the observed data least surprising.",
    'w':"<s>L(&theta;) is not a probability over &theta;.</s> It does not integrate to one, and P(&theta; | data) is a different object that needs a prior.",
    'e':"\"Likelihood\" always means: data fixed, parameters varying. Say it that way and the rest of the derivation stays clear."},
   {'kp':2,'t':"Which statement about the likelihood L(&theta;) is correct?",
    'o':["It is the probability that &theta; is the true parameter",
         "<b>It is the probability of the observed data, viewed as a function of &theta;</b>",
         "It is always between 0 and 1 and integrates to 1 over &theta;",
         "It can only be computed once &theta; is known"],
    'a':1,
    'w':"L(&theta;) evaluates the probability of the data we <em>already have</em>, for each candidate &theta;. <b>It says nothing directly about the probability of &theta; itself</b> -- that would be P(&theta; | data), which requires a prior and Bayes' rule. And it need not lie in [0,1]: with continuous data these are probability <em>densities</em>, which can exceed 1."})

# ── KP3 · the log ───────────────────────────────────────────────────
KP("3 · Why we take the logarithm",
   [('clearScene();setEq(null);setBig(null);'
     'boxNode(130,148,440,92,"product of m factors","r");'
     'boxNode(710,148,440,92,"sum of m terms","g");'
     'link(570,194,710,194,"g");note("log",640,180,"g");'
     'note("multiply 1000 numbers near 0.01 and a 64-bit float returns exactly 0",640,300,"r");'
     'note("sums are also far easier to differentiate",640,352,"");',
     "Products are awkward for two separate reasons, and the logarithm fixes both. <b>Numerically</b>, multiplying a thousand small densities underflows to exactly zero in floating point, and a gradient of zero tells you nothing. <b>Analytically</b>, the derivative of a product of m factors is a mess, while the derivative of a sum is the sum of derivatives. Taking the log turns the product into a sum and both problems disappear. This is not a trick special to this derivation -- <em>working with log-probabilities is standard practice everywhere in machine learning</em>."),
    ('clearScene();setEq(null);setBig("log is strictly increasing","so the maximiser does not move");'
     'note("if a > b then log a > log b -- the ranking of every θ is preserved exactly",640,392,"g");',
     "But is it legitimate? Yes, and the reason is worth stating precisely. <b>The logarithm is strictly increasing</b>, so if one parameter gives a higher likelihood than another, it also gives a higher log-likelihood. The <em>ranking of every candidate &theta; is preserved exactly</em>, and therefore so is the winner. Note carefully what is and is not preserved: <s>the value changes</s> -- the maximum of log L is not the maximum of L -- but the <b>location</b> of the maximum, which is the only thing we want, does not move."),
    ('clearScene();setEq("$$\\\\ell(\\\\theta)=m\\\\log\\\\frac{1}{\\\\sqrt{2\\\\pi}\\\\sigma}-\\\\frac{1}{2\\\\sigma^{2}}\\\\sum_{i=1}^{m}\\\\big(y^{(i)}-\\\\theta^{\\\\top}x^{(i)}\\\\big)^{2}$$","top");'
     'setCap("<b>Two pieces: a constant, and something we have already met.</b>");'
     'note("the first term has no θ in it at all",640,320,"");'
     'note("look hard at the second one",640,372,"y");',
     "Taking the log of the product gives this. It has exactly two pieces, and the first one <b>contains no &theta;</b> -- it depends only on m and &sigma;, so as far as our search is concerned it is a constant, and adding a constant never moves a maximum. That leaves the second piece to do all the work. Look at what is inside the sum: <em>the squared difference between each observation and the line's prediction</em>. We did not put that there. It arrived from the exponent of the normal density.")],
   {'kp':3,'h':"Why the logarithm is safe and useful",
    'k':"The log turns the <b>product</b> into a <b>sum</b>: it prevents floating-point underflow, and it makes differentiation tractable.",
    'm':"It is legitimate because <b>log is strictly increasing</b>, so the ranking of every candidate &theta; -- and therefore the location of the maximum -- is preserved exactly. Working in log-probabilities is standard practice throughout the subject.",
    'w':"<s>The value of the maximum does change.</s> Only its <b>location</b> is preserved, and location is all we are after.",
    'e':"After the log, the expression splits into a &theta;-free constant plus a term containing the sum of squared residuals."},
   {'kp':3,'t':"Why is maximising log L(&theta;) equivalent to maximising L(&theta;)?",
    'o':["Because log L and L have the same value at the maximum",
         "<b>Because log is strictly increasing, so it preserves the ranking of every &theta;</b>",
         "Because the logarithm removes the &sigma; term",
         "It is not equivalent; it is an approximation that works well in practice"],
    'a':1,
    'w':"A strictly increasing transformation cannot change which input is largest, so <b>the argmax is identical</b> -- this is exact, not an approximation. The <em>values</em> differ, of course: log of the maximum is not the maximum. Removing constants is a separate, also-exact simplification: adding or dropping a term with no &theta; in it cannot move the maximiser either."})

# ── KP4 · the punchline ─────────────────────────────────────────────
KP("4 · ★★ The squares fall out",
   [('clearScene();setEq(null);setBig(null);'
     'boxNode(88,150,430,96,"maximise  ℓ(θ)","g");'
     'boxNode(600,150,150,96,"⇔","");'
     'boxNode(830,150,362,96,"minimise  J(θ)","y");'
     'note("drop the constant, flip the minus sign, and the σ² only rescales",640,304,"");'
     'note("a positive rescaling cannot move a minimiser",640,356,"g");',
     "Now put the pieces together. The first term of the log-likelihood has no &theta;, so drop it. The second carries a minus sign, so <b>maximising the log-likelihood is minimising what follows it</b>. And what follows it is the sum of squared residuals divided by 2&sigma;&sup2; -- but &sigma;&sup2; is a fixed positive number, and dividing an objective by a positive constant <em>rescales its height without moving its minimiser</em>. Strip all of that away and what remains is precisely the cost function we invented earlier."),
    ('clearScene();setEq("$$\\\\arg\\\\max_{\\\\theta}\\\\ \\\\ell(\\\\theta)\\\\;=\\\\;\\\\arg\\\\min_{\\\\theta}\\\\ \\\\tfrac{1}{2}\\\\sum_{i=1}^{m}\\\\big(y^{(i)}-\\\\theta^{\\\\top}x^{(i)}\\\\big)^{2}$$","top");'
     'setCap("<b>Least squares is maximum likelihood under Gaussian noise. Not a coincidence.</b>");'
     'note("the same θ solves both -- and it is the normal-equations solution",640,340,"g");',
     "There it is. <b>Least squares is not an arbitrary choice; it is the maximum-likelihood estimator for a linear model with Gaussian noise.</b> Squaring the residuals was never really a decision about arithmetic convenience -- it was, implicitly, a decision about the noise. And notice that &sigma; has vanished entirely from the right-hand side: <em>the fitted line does not depend on how noisy you think the data is</em>. That is a genuinely useful fact. You do not need to know &sigma; to fit the line, though you do need it to say how uncertain the fit is."),
    ('clearScene();setEq(null);setBig("Squaring is a noise model","made before you knew you were making it");'
     'note("choose a different noise distribution and a different loss function appears",640,392,"y");',
     "This is the idea worth carrying out of the film. <b>Every loss function is a noise assumption in disguise.</b> When you reached for squared error you were assuming Gaussian noise, whether or not you knew it. That reframing is what makes the next step obvious rather than mysterious: if the noise is <em>not</em> Gaussian, running the same derivation with the correct density produces a different loss -- and using squared error anyway is not merely suboptimal, it is answering a question about a different dataset than the one you have.")],
   {'kp':4,'h':"★★ Least squares = maximum likelihood",
    'k':"Drop the &theta;-free constant, flip the sign, and note that 1/2&sigma;&sup2; is a positive rescaling: <b>maximising the Gaussian log-likelihood is exactly minimising the sum of squared residuals</b>.",
    'm':"&sigma; disappears from the argmax entirely, so <b>the fitted line does not depend on how noisy you believe the data to be</b> -- though &sigma; is still needed to quantify uncertainty in the fit.",
    'w':"<s>Squaring the errors was never a neutral choice.</s> It is a Gaussian noise assumption, made implicitly the moment you write down squared error.",
    'e':"Say it in one line: least squares is the MLE for a linear model with independent Gaussian noise of constant variance."},
   {'kp':4,'t':"In the step from log-likelihood to least squares, why can the factor 1/2&sigma;&sup2; be dropped?",
    'o':["Because &sigma; is assumed to equal 1",
         "<b>It is a fixed positive constant, and rescaling an objective does not move its minimiser</b>",
         "Because the logarithm has already removed it",
         "It cannot be dropped; least squares is only an approximation to the MLE"],
    'a':1,
    'w':"Multiplying an objective by any positive constant <b>changes its height but not the location of its optimum</b> -- the same reasoning that justified the &frac12; in the original cost function. So &sigma; drops out of the fitting problem entirely and the equivalence is <em>exact</em>. &sigma; still matters, but for confidence intervals, not for the fitted line."})

# ── KP5 · change the noise, change the loss ─────────────────────────
KP("5 · ★ Change the noise, change the loss",
   [('clearScene();setEq(null);setBig(null);'
     'matrix({rows:3,cols:3,cw:352,ch:60,x:88,y:150,'
     'cell:function(i,j){var t=[["assumed noise","resulting loss","behaviour"],'
     '["Gaussian","squared error","outliers dominate"],'
     '["Laplace (heavy tails)","absolute error","outliers tolerated"]];return t[i][j];},'
     'hl:function(i,j){return i===0?"hl":"";},dim:function(i,j){return i===0;}});'
     'note("the loss is a consequence of the noise model, never an independent choice",640,368,"y");',
     "Run the derivation again with a different density and watch the loss change. If the noise follows a <b>Laplace distribution</b> -- same bell-like shape but with heavier tails, so extreme values are far less surprising -- its density carries the absolute residual in the exponent rather than the squared one. The very same three steps then produce <b>minimise the sum of absolute errors</b>. Not because someone decided robustness would be nice, but because that is what the assumption implies."),
    ('clearScene();setEq(null);setBig("Robustness, defined","how surprised the model is by a far-off point");'
     'note("under a Gaussian, a 10σ point is astronomically unlikely -- so it drags the fit",640,392,"r");',
     "This gives \"robust\" a definition sharper than the everyday one. <b>A Gaussian assigns vanishingly small probability to a point ten standard deviations out</b>, so the estimator will bend the line a long way rather than accept such an observation -- one bad reading can pull the whole fit. Under heavier tails the same point is merely unusual, and the fit barely moves. <em>Sensitivity to outliers is not a flaw in least squares; it is the correct behaviour under an assumption that says outliers essentially do not happen.</em>"),
    ('clearScene();setEq(null);setBig(null);'
     'boxNode(120,148,450,96,"residual plot fans out","r");'
     'boxNode(710,148,450,96,"σ is not constant","y");'
     'link(570,196,710,196);'
     'note("the fix is weighted least squares, or a transform of y -- not a bigger model",640,300,"");'
     'note("plotting residuals against x is the cheapest diagnostic in the subject",640,352,"g");',
     "The practical payoff is a diagnostic that costs nothing. <b>Plot the residuals against x and look at the shape.</b> A shapeless horizontal band is what the assumption predicts. If the spread widens as x grows, the constant-&sigma; assumption is violated, and the answer is <em>weighted least squares</em> -- giving noisier observations less influence -- or a transformation such as modelling log y. If the residuals show a curve, the linear part of the model is wrong. <s>Adding more features is the wrong reflex</s> when the residual plot is telling you the noise model, not the mean model, is at fault.")],
   {'kp':5,'h':"★ Every loss is a noise assumption",
    'k':"Re-run the derivation with a different density and a different loss appears: <b>Gaussian &rarr; squared error</b>, <b>Laplace &rarr; absolute error</b>. The loss is a consequence, never an independent choice.",
    'm':"A Gaussian treats a far-off point as almost impossible, so the fit bends to accommodate it -- outlier sensitivity is <em>correct behaviour</em> under that assumption. Heavier tails find the same point merely unusual and the fit barely moves.",
    'w':"<s>A fanning residual plot is not a sign of missing features.</s> Non-constant &sigma; calls for weighted least squares or a transform of y, not a bigger model.",
    'e':"Plot residuals against x: a flat band supports the assumptions, a widening band breaks constant variance, a curve breaks linearity."},
   {'kp':5,'t':"Residuals form a clear widening funnel as x increases. What is the right reading?",
    'o':["The model needs more features",
         "<b>The constant-variance assumption is violated -- consider weighted least squares or a transform of y</b>",
         "The learning rate is too large",
         "The data contains outliers that should simply be deleted"],
    'a':1,
    'w':"A funnel is the signature of <b>heteroscedasticity</b>: the noise grows with x, which the model assumed it would not. The fix targets the <em>noise</em> model -- weight each observation by its precision, or model log y instead. A <b>curved</b> residual pattern would be the one indicating a wrong mean model, and that is when more or better features help."})

# ── KP6 · MAP and regularisation ────────────────────────────────────
KP("6 · ★★ Adding a prior: from MLE to ridge",
   [('clearScene();setEq("$$p(\\\\theta\\\\mid \\\\text{data})\\\\;\\\\propto\\\\;p(\\\\text{data}\\\\mid\\\\theta)\\\\;p(\\\\theta)$$","top");'
     'setCap("<b>Treat &theta; as uncertain too, and Bayes\' rule gives you one extra factor.</b>");'
     'note("MLE keeps only the first factor on the right",640,320,"");'
     'note("the prior says what we believed about θ before seeing any data",640,372,"v");',
     "Return to the objection raised in concept 2: likelihood scores parameters but says nothing about the probability <em>of</em> a parameter. <b>Bayes' rule closes that gap, at the cost of one extra ingredient -- a prior.</b> Maximum likelihood keeps only the first factor on the right and ignores the second, which amounts to treating every value of &theta; as equally plausible beforehand. Choosing the &theta; that maximises the whole right-hand side instead is called <b>MAP</b> estimation: maximum a posteriori."),
    ('clearScene();setEq("$$\\\\min_{\\\\theta}\\\\ \\\\tfrac{1}{2}\\\\sum_i\\\\big(y^{(i)}-\\\\theta^{\\\\top}x^{(i)}\\\\big)^{2}+\\\\lambda\\\\lVert\\\\theta\\\\rVert^{2}$$","top");'
     'setCap("<b>A Gaussian prior on &theta; turns MAP into ridge regression.</b>");'
     'note("λ = σ²/τ²  ·  noisy data or a tight prior both pull θ towards zero",640,344,"g");',
     "Put a normal prior centred at zero on &theta; itself, take logs of both factors, and the result is remarkable in its ordinariness: <b>the familiar least-squares term plus a penalty on the size of &theta;</b>. That is ridge regression, also known as L2 regularisation, and it was not designed -- it fell out. The penalty weight is &lambda; = &sigma;&sup2;/&tau;&sup2;, the ratio of noise variance to prior variance, which reads exactly as it should: <em>noisy data, or a confident prior that &theta; is small, both pull the estimate towards zero</em>."),
    ('clearScene();setEq(null);setBig("A penalty is a prior","just as a loss function is a noise model in disguise");'
     'note("L2 penalty ⇔ normal prior.   L1 penalty ⇔ Laplace prior, which produces zeros.",640,392,"v");',
     "The film closes where it opened, one level up. <b>A loss function encodes an assumption about the noise; a regularisation term encodes an assumption about the parameters.</b> Swapping the normal prior for a Laplace prior turns the L2 penalty into an L1 penalty and yields the lasso, whose defining behaviour -- <em>driving coefficients exactly to zero</em> -- traces directly back to the sharp peak of the Laplace density at the origin. None of these pieces are arbitrary. Each one is a modelling belief written in a compact notation, and knowing which belief you have written down is what lets you tell when it is wrong.")],
   {'kp':6,'h':"★★ From MLE to MAP: where regularisation comes from",
    'k':"Bayes' rule multiplies the likelihood by a <b>prior</b> on &theta;. Maximising that product is <b>MAP</b> estimation; MLE is the special case that ignores the prior.",
    'm':"A zero-centred Gaussian prior on &theta; adds &lambda;&Vert;&theta;&Vert;&sup2; to the least-squares objective -- <b>ridge regression falls out</b>, with &lambda; = &sigma;&sup2;/&tau;&sup2;. Noisy data or a tight prior both shrink &theta; towards zero.",
    'w':"<s>Regularisation is not an ad-hoc trick to stop overfitting.</s> It is a prior belief about the parameters, written in the objective.",
    'e':"L2 penalty &harr; normal prior; L1 penalty &harr; Laplace prior, whose sharp peak at zero is why the lasso produces exact zeros."},
   {'kp':6,'t':"Adding &lambda;&Vert;&theta;&Vert;&sup2; to a least-squares objective corresponds to what, in the probabilistic reading?",
    'o':["Assuming the noise is Laplace rather than Gaussian",
         "<b>Placing a zero-centred Gaussian prior on &theta; and doing MAP instead of MLE</b>",
         "Increasing the assumed noise variance &sigma;&sup2;",
         "Nothing probabilistic; it is a purely numerical device"],
    'a':1,
    'w':"The L2 penalty is the log of a <b>zero-centred normal prior on the parameters</b>, so ridge is MAP estimation under that prior. A Laplace <em>noise</em> model would change the loss term to absolute error, not add a penalty; a Laplace <em>prior</em> would give the L1 penalty and the lasso. Larger &sigma;&sup2; does increase &lambda; = &sigma;&sup2;/&tau;&sup2;, but the penalty's origin is the prior."})

C.append(r'''KP("End · the chain",function(){
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("Maximum likelihood · complete","One assumption, three steps, a familiar answer",
      "noise model → likelihood → log → least squares → and back out again");},
    "The chain, end to end. <b>(1)</b> Assume a generating story: y = &theta;&#7488;x + &epsilon; with independent Gaussian noise of constant variance. <b>(2)</b> Read that story with the data fixed and the parameters varying -- the <b>likelihood</b>, a product of one factor per observation, and <em>not</em> a probability over &theta;. <b>(3)</b> Take the logarithm, which is safe because it is strictly increasing and useful because it turns the product into a sum. <b>(4)</b> Drop the &theta;-free constant and the positive scaling, and what is left is exactly the least-squares cost -- so <b>least squares is the MLE under Gaussian noise</b>, and &sigma; never enters the fitted line. <b>(5)</b> Change the noise and the loss changes with it: Laplace gives absolute error, and outlier sensitivity turns out to be correct behaviour under a Gaussian rather than a defect. <b>(6)</b> Multiply in a prior over &theta; and MAP replaces MLE: a normal prior yields ridge, a Laplace prior yields the lasso. Every loss is a noise model, and every penalty is a prior.");
});
window.__startProjector(CFG);
})();''')

body = "\n".join(C)
full = head + "<script>\n" + body + "\n</script>\n"
full = full.replace("<title>Projector</title>", "<title>Maximum Likelihood</title>")
io.open("mle-ppt.html", "w", encoding="utf-8").write(full)
print("mle-ppt.html written:", len(full), "chars;", body.count("KP("), "KP;",
      body.count("SUM("), "SUM;", body.count("QUIZ("), "QUIZ;", body.count("S(0,function"), "shots")
