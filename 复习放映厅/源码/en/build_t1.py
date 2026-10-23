# -*- coding: utf-8 -*-
"""T1 Overview & Foundations, official-slides walkthrough. English edition.
Faithful translation of ../build_t1.py -- same scenes, same structure, same
pedagogy; only the language changes. Outputs t1-ppt.html."""
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
var CFG={title:"ARTI2001 · T1 Overview & Foundations (slide-by-slide)",
  subtitle:"AI vs ML · three paradigms · the maths you need · the ML pipeline and leakage · SPACE to advance",video:""};
KP("Opening",function(){
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);
    setTitle("M1 T1 · Overview & Foundations","Slide-by-slide walkthrough",
      "Skipping the admin slides · four examinable blocks");},
    "This film covers only the parts of M1T1 that are <b>actually examinable</b>. The first half of the deck is course admin -- enrolment, marking, the roadmap -- so we skip it. The substance is four blocks: <b>the difference between AI and machine learning</b>, <b>the three learning paradigms</b>, <b>the mathematics this semester relies on</b>, and most importantly <b>the end-to-end ML pipeline and the discipline of not leaking data</b>. That last block is the heart of the T1 long-answer question. Every concept ends with a summary card and a check question adapted from the slides' own Study check.");
});''')

def KP(name, shots, summ, quiz):
    b = ['KP(%s,function(){' % js(name)]
    for scene, narr in shots:
        b.append('  S(0,function(){%s},%s);' % (scene, js(narr)))
    fields = ",".join('%s:%s' % (k, js(v)) for k, v in summ.items() if v and k != 'kp')
    b.append('  SUM(0,%d,{%s});' % (summ['kp'], fields))
    opts = ",".join(js(o) for o in quiz['o'])
    b.append('  QUIZ(0,%d,{t:%s,o:[%s],a:%d,w:%s});' % (quiz['kp'], js(quiz['t']), opts, quiz['a'], js(quiz['w'])))
    b.append('});'); C.append("\n".join(b))

# ── KP1 · S19 AI vs ML ──────────────────────────────────────────────
KP("1 · AI vs machine learning (S19)",
 [('clearScene();setEq(null);setBig(null);'
   'boxNode(300,108,680,74,"Artificial Intelligence (the big umbrella)","v");'
   'boxNode(430,206,420,66,"Machine Learning","b");'
   'boxNode(500,296,280,58,"Deep Learning","g");'
   'link(640,182,640,206);link(640,272,640,296);'
   'note("AI also covers: rule-based systems, search, logical reasoning",640,384,"");'
   'setCap("<b>AI is the broad field; machine learning is the branch that learns from data.</b>");',
   "The first examinable point is <b>telling AI and machine learning apart</b>. <b>Intelligence</b> is the capacity of an agent to learn, reason, adapt and use knowledge to reach a goal. <b>AI</b> is the <em>broad field</em> of making machines display that -- and it <i>includes</i> rule-based expert systems, search, logical reasoning and more. <b>Machine learning</b> is one <b>branch</b> of it, distinguished by one thing: <em>it induces the rules from data instead of a human writing them down explicitly</em>. Deep learning is in turn the branch of ML that uses neural networks. So this is a <b>containment relationship</b>: AI &sup2; ML &sup2; deep learning."),
  ('clearScene();setBig("Learned, not hard-coded","this is the dividing line between ML and classical AI");',
   "Exams like to ask \"what is the difference between AI and ML\". The standard answer: <b>AI is the larger category</b>, covering every method that makes a machine appear intelligent, <i>including systems that never learn</i>; <b>ML is the branch that induces patterns from data rather than encoding rules explicitly</b>. An example makes it concrete: hand-writing an if-else rule for \"is this a leap year\" is ordinary programming or a rule system -- <b>not</b> ML, because it never gets better from seeing more data. Training on ten thousand labelled photographs to recognise a cat <em>is</em> ML. <s>Not every piece of automation or AI is machine learning</s> -- the test is always \"does it learn from data?\"")],
 {'kp':1,'h':"AI vs machine learning: a containment relationship (S19)",
  'k':"<b>AI &sup2; ML &sup2; deep learning.</b> AI is the broad field of making machines appear intelligent (rule systems, search, reasoning included); <b>ML is the branch that induces patterns from data rather than encoding rules</b>; deep learning is the neural-network branch of ML.",
  'm':"The dividing line for ML is <em>induction from data vs rules written by a human</em>. Classical AI can be entirely rule-based and never learn; ML depends on data and improves as it sees more.",
  'w':"<s>Not all AI or automation is ML.</s> A hand-written if-else rule (leap years, say) is programming, not machine learning -- it does not improve with more data.",
  'e':"T1 regularly asks for the AI-vs-ML distinction: AI is larger and includes rule systems; ML is the learn-from-data branch. The test is always whether the method learns from data."},
 {'kp':1,'t':"Which statement describes the relationship between AI and machine learning most accurately?",
  'o':["AI and ML are synonyms",
       "<b>AI is the broad field (including rule systems); ML is the branch that induces patterns from data rather than hard-coding rules</b>",
       "ML is broader than AI","AI is one algorithm within ML"],'a':1,
  'w':"<b>AI &sup2; ML.</b> AI is the <em>whole field</em> of making machines appear intelligent, and it includes rule-based expert systems, search and logical reasoning -- none of which need to learn. <b>Machine learning is specifically the branch that induces patterns from data.</b> Deep learning is in turn a subset of ML. To decide whether something is ML, ask <s>does it learn from data</s>, not whether it seems intelligent."})

# ── KP2 · S20 three paradigms ───────────────────────────────────────
KP("2 · ★ The three learning paradigms (S20)",
 [('clearScene();setEq(null);setBig(null);'
   'boxNode(120,180,320,100,"Supervised","b");'
   'boxNode(490,180,300,100,"Unsupervised","g");'
   'boxNode(840,180,320,100,"Reinforcement","y");'
   'note("every example carries its answer (a label)",280,330,"b");'
   'note("data only, no answers",640,330,"g");'
   'note("only a good/bad signal (reward)",1000,330,"y");'
   'setCap("<b>The test: what form of feedback can you get?</b>");',
   "The second examinable point is the <b>three learning paradigms</b>, and there is only one test that separates them: <b>what form of feedback is available to you</b>. <b>Supervised learning</b> -- every example <em>carries the correct answer (a label)</em>, and you learn the mapping from input to output; classification predicts a category, regression predicts a continuous value. <b>Unsupervised learning</b> -- <em>data only, no labels</em>; the algorithm has to find structure by itself (clustering, dimensionality reduction). <b>Reinforcement learning</b> -- <em>no correct answers, only an evaluation of good or bad (a reward)</em>, and a policy is learned by trial and error. The first two modules of this course map straight onto the first two: <b>M1 supervised</b>, <b>M2 unsupervised</b>. M3's neural networks are a <i>model</i>, not a fourth kind of problem."),
  ('clearScene();setBig("Labels, or their absence","supervised = labelled · unsupervised = unlabelled · reinforcement = reward only");',
   "Fix the boundaries firmly. <b>The only test separating supervised from unsupervised is whether the training data carries labels</b> -- the same pile of data is a supervised problem if you were given the answers and an unsupervised one if you were not. <s>Two easy mistakes</s>: (1) do not treat \"neural network\" as a fourth category alongside supervised -- it is a <b>model</b>, and it can be trained either way; when asked which <em>kind of learning problem</em> something is, answer supervised / unsupervised / reinforcement, not a model name. (2) Within supervised learning, regression and classification are separated by whether the target is <b>continuous or discrete</b> -- that is a <i>second-level</i> split, a different level of the hierarchy, so do not mix it with the three-way one. Reinforcement learning is not in your three modules, but the three-way split itself is examinable.")],
 {'kp':2,'h':"★ The three learning paradigms (S20)",
  'k':"The test is <b>the form of the feedback</b>: <b>supervised</b> (every example labelled, learn input&rarr;output), <b>unsupervised</b> (no labels, find structure), <b>reinforcement</b> (reward only, learn a policy by trial and error). M1 is supervised, M2 unsupervised.",
  'm':"Supervised vs unsupervised turns on <em>one</em> thing: does the training data carry labels. Within supervised, regression vs classification is a second-level split on whether the target is continuous or discrete. A neural network is a model, not a fourth kind of problem.",
  'w':"<s>A neural network is not a category of learning problem.</s> It is a model, trainable either way. Asked \"which kind of learning\", answer supervised / unsupervised / reinforcement -- never a model name.",
  'e':"Reliably examined. The test is the feedback available: a full answer / nothing / only a good-bad signal. Regression vs classification sits one level below -- keep the levels apart."},
 {'kp':2,'t':"What most fundamentally distinguishes supervised, unsupervised and reinforcement learning?",
  'o':["They use different algorithms","The amount of data available",
       "<b>The form of feedback available: a full correct answer / nothing at all / only an evaluation of good or bad</b>",
       "Whether the output is continuous or discrete"],'a':2,
  'w':"The three-way split rests on <b>the form of the supervisory signal</b>: supervised learning has a <em>full correct answer</em> per example; unsupervised has <s>no answers at all</s> and only mines structure; reinforcement has only a <b>reward</b>, which is often delayed. Option D -- continuous vs discrete output -- is the test that separates regression from classification <em>inside</em> supervised learning. Different level of the hierarchy; keep them apart."})

# ── KP3 · S23-24 the maths ──────────────────────────────────────────
KP("3 · The maths you need: linear algebra and calculus (S23-24)",
 [('clearScene();setEq(null);setBig(null);'
   'setEq("$$x^{\\\\top}y=\\\\sum_i x_iy_i,\\\\quad (AB)_{ij}=\\\\sum_k A_{ik}B_{kj},\\\\quad \\\\lVert x\\\\rVert=\\\\sqrt{x^{\\\\top}x}$$","top");'
   'setCap("<b>Linear algebra: inner product, matrix product, transpose, norm -- used all semester.</b>");',
   "The deck recaps the mathematics this semester leans on. From <b>linear algebra</b>, the pieces that recur: the <b>inner (dot) product</b> x&#7488;y = &Sigma;x&#7522;y&#7522; -- a linear score w&#7488;x <em>is</em> this; the <b>matrix product</b> (AB)&#7522;&#11388; = &Sigma;&#8342;A&#7522;&#8342;B&#8342;&#11388; -- <i>always check the dimensions first: columns of A must match rows of B</i>; the <b>transpose</b>, which swaps rows and columns; and the <b>norm</b> &Vert;x&Vert; = &radic;(x&#7488;x) -- the SVM margin 1/&Vert;w&Vert; is built from it. Also <b>invertibility, rank and eigenvalues</b> -- the normal equation (X&#7488;X)&#8315;&#185; needs full column rank so that X&#7488;X is invertible. None of this is examined on its own, but every calculation in T2 and T4 stands on it."),
  ('clearScene();setEq("$$\\\\frac{d(x^n)}{dx}=nx^{n-1},\\\\quad [f(g(x))]\'=f\'(g(x))g\'(x),\\\\quad \\\\nabla J=\\\\Big[\\\\tfrac{\\\\partial J}{\\\\partial\\\\theta_1},\\\\dots\\\\Big]$$","top");'
   'setCap("<b>Calculus: the power rule, the chain rule, and the gradient as a vector of partials.</b>");',
   "From <b>calculus</b>: the <b>power rule</b> d(x&#8319;)/dx = nx&#8319;&#8315;&#185;; the <b>chain rule</b> [f(g(x))]&prime; = f&prime;(g(x))&middot;g&prime;(x) -- deriving the logistic-regression gradient and back-propagation both rest entirely on it; the <b>exponential and log</b> derivatives d(e&#739;) = e&#739; and d(ln x) = 1/x; and the <b>gradient</b> &nabla;J, which is \"the partial derivatives of J with respect to each parameter, <em>collected into a vector</em>\", pointing in the direction of steepest increase. <b>T1's tutorial questions Q1 and Q2 are differentiation drills on exactly these rules</b> -- differentiating a squared loss, differentiating a sigmoid. Get the power rule and the chain rule fluent and the hand-computed gradients in T2 and T3 become substitution exercises.")],
 {'kp':3,'h':"Mathematical foundations: linear algebra + calculus recap (S23-24)",
  'k':"<b>Linear algebra</b>: inner product x&#7488;y = &Sigma;x&#7522;y&#7522; (a linear score is one), matrix product (check dimensions first), transpose, norm &Vert;x&Vert; = &radic;(x&#7488;x), invertibility and rank (the normal equation needs full column rank). <b>Calculus</b>: power rule, chain rule, gradient as a vector of partials.",
  'm':"These are the tools behind every calculation in T2, T3 and T4: w&#7488;x is an inner product, 1/&Vert;w&Vert; is a norm, (X&#7488;X)&#8315;&#185; needs invertibility, and hand-computed gradients come from the power and chain rules.",
  'w':"<s>Check dimensions before multiplying matrices</s> (columns of A = rows of B) or the product does not exist. The gradient is a <em>vector</em> -- one partial derivative per parameter -- not a single number.",
  'e':"T1's tutorial Q1-Q2 are differentiation drills on the power and chain rules. This material is not examined deeply on its own, but it underpins the normal equation in T2, the gradients in T3 and the margin in T4, so it has to be fluent."},
 {'kp':3,'t':"Differentiating L = (&sigma;(z) &minus; y)&sup2; with respect to z by the chain rule, what happens first?",
  'o':["The result is 0",
       "<b>Differentiate the square first, giving 2(&sigma;(z) &minus; y), then multiply by the inner derivative &sigma;&prime;(z) -- peel from the outside in</b>",
       "Differentiate with respect to y first","The power rule does not apply"],'a':1,
  'w':"The chain rule <b>peels from the outside inwards</b>: the outermost operation is the square, so differentiate that first while holding the inside fixed, giving 2(&sigma;(z) &minus; y); then multiply by the derivative of the inside, &sigma;&prime;(z) = &sigma;(z)(1 &minus; &sigma;(z)). <s>No layer may be skipped.</s> This power-rule-plus-chain-rule routine is exactly how T2 derives the least-squares gradient and T3 derives the logistic-regression gradient (p &minus; y)x -- and it is what T1's tutorial is drilling."})

# ── KP4 · S26 optimisation ──────────────────────────────────────────
KP("4 · Optimisation: loss, convexity, gradient descent (S26)",
 [('clearScene();setEq(null);setBig(null);'
   'matrix({rows:4,cols:2,cw:340,ch:54,y:190,'
   'cell:function(i,j){var t=[["Concept","The point"],'
   '["Loss / objective","measures how wrong the prediction is; smaller is better"],'
   '["Convexity","bowl-shaped -> a local optimum is the global one"],'
   '["Gradient descent","theta <- theta - alpha * grad L, repeated"]];return t[i][j];},'
   'dim:function(i,j){return i===0;},hl:function(i,j){return false;}});'
   'setEq("$$\\\\theta\\\\leftarrow\\\\theta-\\\\alpha\\\\nabla L(\\\\theta)$$","top");',
   "Training a machine learning model is fundamentally <b>optimisation</b>: define a <b>loss (objective) function</b> that measures how wrong the predictions are, then <b>minimise</b> it. The key ideas: <b>convexity</b> -- is the loss surface bowl-shaped? For a convex function <em>a local optimum is the global optimum</em> (linear regression and logistic regression are convex; neural networks are not). <b>Gradient descent</b>, &theta; &larr; &theta; &minus; &alpha;&nabla;L, is the general-purpose minimiser, with &alpha; the learning rate. <b>Convergence</b> -- stop when J flattens out. The deck also names the two concrete losses you will meet: <b>MSE</b> = (1/n)&Sigma;(y &minus; &#375;)&sup2; for regression and <b>binary cross-entropy</b> L = &minus;[y&middot;log p + (1&minus;y)&middot;log(1&minus;p)] for classification -- which are precisely the losses of T2 and T3."),
  ('clearScene();setBig("Learning = minimising a loss","define the loss -> take the gradient -> descend -> converge");',
   "Hold on to the single skeleton that runs through all of Module 1: <b>learning is defining a loss and minimising it</b>. Different models only swap the loss and the assumptions: <i>regression uses MSE, classification uses cross-entropy, the SVM uses hinge loss</i>; and the minimisation is done either by <b>gradient descent</b> (general) or by a <b>closed-form solution</b> (available only for a few models such as linear regression). <b>Local versus global optimum</b> is the distinction that matters: convex problems -- the regression, logistic regression and SVM of M1 -- have no bad local optima, so any starting point reaches the same bottom; non-convex ones (neural networks) can get stuck, and the starting point and random seed affect the result. Once this skeleton is clear, T2, T3 and T4 are the same derivation with different pieces substituted in.")],
 {'kp':4,'h':"Optimisation: loss, convexity, gradient descent (S26)",
  'k':"Training = <b>minimising a loss</b>. Key ideas: <b>convexity</b> (bowl-shaped &rarr; local = global optimum), <b>gradient descent</b> &theta; &larr; &theta; &minus; &alpha;&nabla;L, convergence. Two concrete losses: MSE (regression), binary cross-entropy (classification).",
  'm':"One skeleton: define a loss &rarr; take its gradient &rarr; descend (or solve in closed form) &rarr; converge. Models only swap the loss (MSE / cross-entropy / hinge). Convex problems have no bad local optima; non-convex ones can get stuck.",
  'w':"<s>Convex and non-convex behave very differently.</s> M1's regression, logistic regression and SVM are convex, with a unique optimum; neural networks are not, so the starting point matters. Closed forms exist for few models -- gradient descent is general.",
  'e':"The through-line of M1. Be able to write the update, distinguish convex from non-convex, and recognise MSE and BCE. T2 and T3 are the same optimisation with a different loss."},
 {'kp':4,'t':"Why does convexity matter?",
  'o':["It makes training faster",
       "<b>For a convex function a local optimum is the global optimum -- gradient descent reaches it from any starting point and cannot get stuck in a bad local minimum</b>",
       "It removes the need for a learning rate","It guarantees no overfitting"],'a':1,
  'w':"<b>A convex (bowl-shaped) function has a single lowest point</b>, so as long as &alpha; is sensible, gradient descent rolls to the same global optimum from <em>any</em> starting point and <s>there are no bad local minima to be trapped in</s>. The objectives of linear regression, logistic regression and the SVM are all convex. A neural network is <b>non-convex</b> -- its loss surface is full of dips, so the starting point and the random seed affect the final result, which is one of the reasons deep learning is hard to tune."})

# ── KP5 · S29 the pipeline ──────────────────────────────────────────
KP("5 · ★ The end-to-end ML pipeline (S29)",
 [('clearScene();setEq(null);setBig(null);'
   'boxNode(80,104,300,58,"1. Data and preparation","b");'
   'boxNode(80,178,300,58,"2. Train / select a model","");'
   'boxNode(80,252,300,58,"3. Evaluate","y");'
   'boxNode(80,326,300,58,"4. Deploy and monitor","g");'
   'note("collect representative data, clean it, explore it",430,138,"","start");'
   'note("fit the parameters, choose the hyper-parameters",430,212,"","start");'
   'note("quantify on held-out data, compare to a baseline",430,286,"","start");'
   'note("watch the input distribution; retrain when it moves",430,360,"","start");'
   'link(230,162,230,178);link(230,236,230,252);link(230,310,230,326);',
   "The third block is the <b>end-to-end ML pipeline</b>: (1) <b>data and preparation</b> -- collect representative data, clean it, explore it; (2) <b>training</b> -- fit the parameters, choose the model and hyper-parameters; (3) <b>evaluation</b> -- quantify performance on <em>held-out</em> data and compare against a baseline; (4) <b>deployment and monitoring</b> -- once live, watch the input distribution and retrain when it moves. The deck stresses that this pipeline <b>doubles as a diagnostic tool</b>: good on train but poor on test &rarr; overfitting; poor on both &rarr; underfitting; accuracy falls after deployment &rarr; data shift. <s>Every step can go wrong</s>, and the T1 long-answer question is precisely \"identify what has gone wrong in this pipeline and say what to do about it\"."),
  ('clearScene();setBig("The pipeline diagnoses too","good train + poor test = overfitting · both poor = underfitting · falls in production = data shift");',
   "Knowing \"the pipeline is also a diagnostic\" is the skeleton of the T1 long-answer question. <b>Low training error, high test error</b> &rarr; <em>overfitting (high variance)</em>: simplify the model, add regularisation, get more data. <b>Both errors high</b> &rarr; <em>underfitting (high bias)</em>: add features, increase capacity. <b>Accuracy drops after deployment</b> with no code change &rarr; <em>data shift</em>: investigate what changed in the inputs, gather representative recent data, retrain and re-evaluate if needed. <s>Two answers that lose marks</s>: using the model's own predictions as labels and continuing to train (this bakes in and amplifies its errors), and re-evaluating on the original training set (which cannot reveal a problem that lives in the new data).")],
 {'kp':5,'h':"★ The ML pipeline is also a diagnostic table (S29)",
  'k':"The pipeline: <b>(1) data preparation &rarr; (2) train / select &rarr; (3) evaluate on held-out data against a baseline &rarr; (4) deploy and monitor</b>. It <em>doubles as a diagnostic</em>: good train + poor test = overfitting; both poor = underfitting; drops in production = data shift.",
  'm':"Each step can fail. Overfitting &rarr; simplify, regularise, add data. Underfitting &rarr; add features, increase capacity. Data shift &rarr; investigate what changed in the inputs, collect fresh representative data, retrain and re-evaluate.",
  'w':"<s>Never use the model's own predictions as labels and keep training</s> (it bakes in the errors). <s>Never re-evaluate only on the original training set</s> -- it cannot reveal a problem in the new data.",
  'e':"Answer the T1 long-answer question from this diagnostic table: name the failure (overfitting / underfitting / data shift), then give two targeted remedies."},
 {'kp':5,'t':"A model trained on 2020-2023 data, with no code changes, is noticeably less accurate in 2026. What is the most appropriate first step?",
  'o':["Keep using it -- its training accuracy was high",
       "Re-evaluate on the original training set to confirm it still works",
       "<b>Investigate what has changed in the input data, collect representative recent samples, and retrain and re-evaluate if needed</b>",
       "Label the new data with the model's own predictions and continue training"],'a':2,
  'w':"This is textbook <b>data shift</b>: the deployment environment no longer matches the training data. The right first step is to <em>investigate what changed in the inputs</em>, collect recent representative data, and retrain and re-evaluate if necessary. <s>Option B reveals nothing</s> -- the problem lives in the new data, not the old. <s>Option D bakes the model's own errors in and amplifies them.</s> This question is the prototype for T1's example multiple-choice items."})

# ── KP6 · S30 no leakage ────────────────────────────────────────────
KP("6 · ★★ Preparing data without leaking it (S30)",
 [('clearScene();setEq(null);setBig(null);'
   'boxNode(280,104,720,58,"1. Split into train / validation / test FIRST","g");'
   'boxNode(280,178,720,58,"2. Fit preprocessing on the training set only (put it in a Pipeline)","g");'
   'boxNode(280,252,720,58,"3. Fit on train, choose hyper-parameters on validation","");'
   'boxNode(280,326,720,58,"4. Touch the test set once, then report","r");'
   '[162,236,310].forEach(function(y){link(640,y,640,y+16);});'
   'setCap("<b>The order is not negotiable: splitting must come before any preprocessing.</b>");',
   "This is <b>the core examinable point of T1</b>: <b>do not leak the answers into the data while preparing it</b>. The rule in one line -- <b>split first, preprocess second</b>. The reason is that <s>preprocessing is part of training, not a neutral operation</s>: an imputer that fills missing values, an encoder, a scaler that standardises, a feature-selection rule -- every one of them <em>learns something from the data</em>. Those objects <b>must be fitted on the training set only</b>, then applied unchanged to validation, test and future data -- which in practice means <b>putting them inside a Pipeline</b>. If you fit a scaler on <i>all</i> the data before splitting, the test set's statistics have leaked into the model and your evaluation comes out <b>optimistically biased</b>. That is <em>preprocessing leakage</em>."),
  ('clearScene();setBig("Two kinds of leakage","preprocessing leakage (fitting before the split) · selection leakage (choosing hyper-parameters on the test set)");',
   "You need to be able to recognise both kinds; they are a standing source of lost marks in the T1 long-answer question. <b>Preprocessing leakage</b>: fitting a scaler or imputer on the whole dataset before splitting -- the fix is to <i>split first and put preprocessing inside a Pipeline so it is fitted only on the training fold</i>. <b>Selection leakage</b>: comparing several hyper-parameter settings on the <em>test set</em> and keeping the best -- once the test set has taken part in the choice, it has <b>become a second validation set</b> and the score is no longer clean; worse, \"the maximum over N attempts\" is systematically optimistic. The fix is to <i>choose hyper-parameters on a validation set and touch the test set once</i>. <s>The sentence to memorise</s>: repeatedly inspecting the test result and adjusting on the basis of it turns the test set into another validation set and produces an over-optimistic estimate. This comes up almost every year.")],
 {'kp':6,'h':"★★ Preparing data without leakage (S30)",
  'k':"<b>Split first, preprocess second.</b> Preprocessing (imputer / scaler / encoder / selection) learns from the data, so it <em>must be fitted on the training set only, inside a Pipeline</em>, then applied unchanged. Fitting before the split is preprocessing leakage &rarr; a biased evaluation.",
  'm':"Two kinds: <b>preprocessing leakage</b> (fitting before the split) and <b>selection leakage</b> (tuning on the test set turns it into a second validation set; the max over N attempts is systematically optimistic). Fix: choose on validation, touch test once.",
  'w':"<s>Preprocessing is not neutral</s> -- it is part of training. <s>The test set is contaminated the moment you use it twice</s>: inspecting the score and adjusting makes it a validation set.",
  'e':"<b>The core T1 long-answer topic.</b> Memorise: repeatedly inspecting the test result and adjusting turns the test set into a second validation set and gives an over-optimistic estimate. Answer structure: split first &rarr; Pipeline &rarr; choose on validation &rarr; test once."},
 {'kp':6,'t':"A pipeline: (1) fit StandardScaler on all the data, (2) split into train/test, (3) compare 8 hyper-parameter settings on the test set and keep the best, (4) report that test accuracy. How many serious errors are there?",
  'o':["None","One: the hyper-parameter search is not fine enough",
       "<b>At least two: preprocessing leakage (scaler fitted before the split) and selection leakage (hyper-parameters chosen on the test set)</b>",
       "One: the test set is too small"],'a':2,
  'w':"Two independent leaks occur at once. (1) <b>Preprocessing leakage</b> -- the scaler is fitted on everything before the split, so the test set's statistics enter the model; the fix is to <em>split first</em> and place the scaler in a Pipeline so it is fitted on the training fold only. (2) <b>Selection leakage</b> -- comparing 8 settings on the test set and keeping the best makes it a second validation set, and the maximum of 8 attempts is systematically optimistic. The correction: split into train/validation/test, choose on validation, and touch the test set <b>once</b>. This is the prototype of the T1 long-answer question."})

# ── closing ─────────────────────────────────────────────────────────
C.append(r'''KP("End · revision checklist",function(){
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("M1 T1 · Overview & Foundations","Walkthrough complete",
      "AI ⊃ ML · three paradigms · mathematical tools · the pipeline and leakage");},
    "That is the examinable content of T1. Four sentences to take away: <b>(1) AI is the broad field and ML is the branch that learns patterns from data; (2) the three paradigms are separated by the feedback available -- supervised (labelled) / unsupervised (unlabelled) / reinforcement (reward only), with M1 supervised and M2 unsupervised; (3) the mathematical tools are the inner product, norm and matrix invertibility from linear algebra, the power rule, chain rule and gradient from calculus, and loss, convexity and gradient descent from optimisation; (4) the ML pipeline is both a sequence of steps and a diagnostic table, and its most important rule is split first, preprocess second, touch the test set once -- which is what prevents the two kinds of leakage.</b> The T1 long-answer question almost always lands on the pipeline and leakage, so make the memorised sentence from concept 6 secure. Good luck in the exam.");
});
window.__startProjector(CFG);
})();''')

body = "\n".join(C)
full = head + "<script>\n" + body + "\n</script>\n"
full = full.replace("<title>Projector</title>", "<title>T1 Overview &amp; Foundations</title>")
io.open("t1-ppt.html", "w", encoding="utf-8").write(full)
print("t1-ppt.html written:", len(full), "chars;", body.count("KP("), "KP;",
      body.count("SUM("), "SUM;", body.count("QUIZ("), "QUIZ;", body.count("S(0,function"), "shots")
