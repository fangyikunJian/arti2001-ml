# -*- coding: utf-8 -*-
"""CME295 L7 模块 a —— 字幕第 1–47 句（00:05–06:20）：开场、L6 回顾（推理模型 / GRPO /
长度偏置与两个修法），以及今天要修的那两条弱点。

⚠ 新标准：旁白约 280 字、每镜扛 7–8 句字幕。
"""


def add(KP):

    KP("⭐ 开场，与 L6 的回顾",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("00:19","to let our LLM interact with the outside world with other systems",166);
  note("⭐ 到现在为止，我们的 LLM「纯粹是靠它自己」",640,196,"y");
  boxNode(80,228,500,50,"L1–L6 做的事","d");
  boxNode(700,228,500,50,"今天要做的事","g");
  note("把这个模型本身造好、训好、让它会推理",330,302,"d");
  note("把它接到别的系统上去",950,302,"g");
  note("今天三个关键词：RAG · tool calling · agent",640,348,"y");
  note("⚠ 它修的正是 L6 开头那张弱点清单上的第 ② 和第 ③ 条",640,386,"r");''',
         "<b>第七讲，而它要做的事一句话说得清：把 LLM 从「自己一个人」接到外面去。</b><br>⭐ 请注意讲者的措辞：「<b>到现在为止，我们的 LLM 纯粹是靠它自己</b>」—— <b>前六讲全在「把这个模型本身造好」（架构、训练、对齐、推理）,而今天第一次讨论「它和外部系统怎么打交道」</b>。<br>⚠ 这一讲的难度和 L6 完全不同：<b>数学很少，但新概念和新缩写密度极高（RAG、BM25、HyDE、NDCG、MCP、ReAct、A2A…）⇒ 难的不是推导，是「哪个词指哪件事」</b>。所以这部片子会把术语对照做得很密，<b>你要做的是把每个词挂到它解决的那个具体问题上</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("01:07","we saw the differences between reasoning model and what we call the vanilla LLM",166);
  note("⭐ 先回顾 L6：推理模型改的只是「输出的形状」",640,196,"y");
  boxNode(80,226,220,46,"vanilla：prompt","d");
  link(300,249,370,249);
  boxNode(370,226,200,46,"回应","d");
  boxNode(80,282,220,46,"推理模型：prompt","y");
  link(300,305,370,305);
  boxNode(370,282,280,46,"推理链（通常藏起来）","v");
  link(650,305,720,305);
  boxNode(720,282,200,46,"回应","g");
  note("⚠ 而「通常对用户隐藏」那一句，正是 L6 讲的「思考摘要不是原始链」",640,352,"r");''',
         "<b>照例先回顾上一讲，而他用一张对照图把 L6 的核心结论摆出来。</b><br>⭐ 「<b>如果我们让 LLM 在输出回应之前先推理，在数学和代码这类推理任务上就能拿到性能</b>」—— 这就是 L6 的全部：<b>模型没变、架构没变，变的是输出从「答案」变成「推理链 + 答案」</b>。<br>⚠ 而「推理链<b>通常对用户是隐藏的</b>」这半句别跳过：<b>L6 花了整整一个知识点讲它 —— 界面上那几行是另一个模型做的摘要，不是原始链；而最硬的理由是商业的：原始链是最值钱的那份训练数据</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("02:09","a core RL algorithm called GRPO, which stands for Group Relative Policy Optimization",166);
  says("03:12","rewarding the model for outputting a reasoning chain",192);
  note("⭐ GRPO 一句话：用同组的均值当基线，于是不用 value function",640,222,"y");
  seq(90,254,["query","策略 ⇒ g 条","g 个奖励","减组内均值 = advantage"],"g",250,48);
  note("两个奖励：① 有没有写推理链 ② 回应好不好 —— 都是程序能判的",640,330,"g");
  note("⚠ 「它不训练一个 value function」—— 这是 GRPO 和 PPO 唯一的实质差别",640,374,"r");''',
         "<b>回顾 GRPO，而他挑出来强调的正是那一处实质差别。</b><br>⭐ 「<b>一个值得注意的方面是它不训练一个 value function</b>」—— 请把 L6 那句最小集再过一遍：<b>PPO 靠一个学出来的 value function 当基线，GRPO 靠同一个 prompt 采 g 条回答的平均奖励当基线 ⇒ 那一处替换省掉了一整个要训练的模型</b>。<br>⚠ 而两个奖励也请一起记住，因为它们是整件事能成立的前提：<b>「有没有推理链」用一个正则就能查，「回应对不对」跑测试或比答案就行 ⇒ 不需要奖励模型 ⇒ 不用标注、不会被 hack、信号可以无限生成</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("03:29","as the RL training progresses, we have an improvement of the model on these reasoning tasks",166);
  note("⭐ 两张图：左边表现在涨，右边长度也在涨",640,194,"y");
  axes({x0:240,x1:1040,y0:348,y1:246});
  curve(fn(function(x){return 348-92*(1-Math.exp(-(x-240)/170));},240,1040,60),"g");
  curve([[240,344],[640,286],[1040,254]],"r");
  note("表现：涨到这里就平了",540,232,"g");
  note("长度：一路涨",910,264,"r");
  note("RL 步数  ⟶",1040,370,"d","end");''',
         "<b>那条曲线，以及它旁边那条一直没停的线。</b><br>⭐ 前半段的因果是<b>正向</b>的：<b>RL 奖励「答对」⇒ 模型发现多想几步更容易答对 ⇒ 写得更长 ⇒ 真的答对更多</b>。讲者用的数据集是 <b>AIME</b>（美国奥赛资格考），L6 讲过它「难而且极好判」。<br>⚠ 但第二张图上那条线<b>没有跟着平下来</b>：<b>「即使在图的后段表现已经趋于平稳，输出长度仍然在增加」⇒ 分岔点之后，你的推理成本还在线性增长，而什么也没换到 —— 纯亏</b>。这就是下一镜那个诊断的起点。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("04:19","the output length was still increasing",166);
  says("04:49","this is a phenomenon called length bias",192);
  note("⭐ 回到损失里找原因 —— 而根因在一个归一化因子上",640,222,"y");
  boxNode(80,254,760,46,"一条 5000 token 的回答  ⟶  整条打折 1/5000","d");
  boxNode(80,310,340,46,"100 token  ⟶  打折 1/100","y");
  note("⇒ 同样答错，写短的被罚得更重 ⇒ 模型学会「要错就错得长一点」",640,374,"r");''',
         "<b>他们回到 GRPO 的损失里找原因，而找到的东西叫「长度偏置」。</b><br>⭐ 讲者的原话是：「<b>损失里有一项，会让一个 token 的贡献因为它在短回答里还是长回答里而不同</b>」—— 这就是 L6 花了一整块讲的那个 <b>1/|o_i|</b>:<b>它只取决于「这一整条有多长」,对整条统一打折 ⇒ 一个 token 好不好，不该取决于它所在那条回答恰好有多长</b>。<br>⚠ 而它只在<b>答错那一半</b>作祟：答对时它把模型推向「短而对」（是好事）;答错时「写短罚得更重」⇒ <b>训练后期剩下的大多是答错的 ⇒ 表现不涨，长度一直涨</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("05:37","enumerate the strengths and the weaknesses of vanilla LLMs",166);
  says("06:01","see how we can connect our LLM to the ever evolving knowledge base",192);
  note("⭐ 两个修法，然后回到那张弱点清单",640,222,"y");
  boxNode(80,254,500,46,"DAPO：归一化因子不再依赖位置","g");
  boxNode(700,254,500,46,"GRPO Done Right：整个删掉","y");
  boxNode(80,312,500,46,"今天 ① 接到不断更新的知识库","b");
  boxNode(700,312,500,46,"今天 ② 让它替我们「做事」","v");
  note("⚠ 一个解「知识停在 cutoff」,一个解「全是说，没有做」—— 正是弱点 ② 和 ③",640,376,"r");''',
         "<b>两个修法一句话带过，然后他把话头接回那张弱点清单。</b><br>⭐ 两个修法 L6 讲透过：<b>DAPO 把分母换成整组总长度（还归一化，只是统一了）,Dr. GRPO 把它整个删掉（连归一化都不做）—— 两者都消除了「长度依赖」</b>。<br>⚠ 而这一讲的定位现在很清楚：<b>L6 修的是弱点 ①（推理能力有限）,今天一次修两条 —— ② 知识停在 cutoff date ⇒ RAG；③ 全是说、没有做 ⇒ tool calling 与 agent</b>。<b>两个半场，中间 Afshine 交棒给 Shervine</b>；而剩下的弱点 ④（难评估）留给 L8。", 0)],
       {"h": "⭐ 开场与 L6 的回顾",
        "k": "<b>「今天我们要聚焦在一些实用技术上，让我们的 LLM 和外部世界、和别的系统交互 —— 因为到现在为止，我们的 LLM 纯粹是靠它自己」; 「今天这节课会聚焦在 RAG、tool calling 和 agents」</b>。<br>L6 回顾：<b>「我们看了推理模型和我们所说的 vanilla LLM 之间的差别」—— 推理模型「拿一个 prompt 作为输入，输出的是一条推理链（通常对用户是隐藏的）加上一个回应」; 「我们看了一个核心的 RL 算法叫 GRPO，它代表 Group Relative Policy Optimization」,而「一个值得注意的方面是它不训练一个 value function」; 两个精心挑选的奖励是「奖励模型输出一条推理链」和「奖励模型产生一个好的回应」⇒ 「随着 RL 训练推进，模型在这些推理任务上有提升」</b>。<br>那个 bug：<b>「即使在上面那张图的后段表现已经趋于平稳，我们看到输出长度仍然在增加」⇒ 回到损失里发现「有一项会让一个 token 的贡献不同，取决于它是在一个短回应里还是长回应里」⇒ 「这个现象叫 length bias」;两个缓解办法是 DAPO（归一化因子不依赖 token 在哪一句里）和「GRPO Done Right」（直接把归一化项去掉）</b>。<br>今天：<b>「第一件是看我们怎么把 LLM 连到不断演进的知识库上，特别是怎么拿到最新的信息；第二件是我们的 LLM 怎么帮我们执行动作 —— 这部分会和 Shervine 一起看 tool calling 和 agentic workflows」</b>。",
        "m": "⭐ 这一讲的定位要钉死：<b>L6 修弱点 ①（推理能力有限）,L7 一次修两条 —— ② 知识停在 cutoff date ⇒ RAG；③ 全是说没有做 ⇒ tool calling 与 agent；而 ④（难评估）留给 L8</b>。<br>⭐ GRPO 的一句话最小集请再过一遍：<b>PPO 靠一个学出来的 value function 当基线，GRPO 靠同一个 prompt 采 g 条的平均奖励当基线 ⇒ 省掉一整个要训练的模型</b>；而两个奖励都是<b>程序能判的</b>,所以不需要奖励模型。<br>⭐ 长度偏置的机制：<b>1/|o_i| 对整条统一打折 ⇒ 同样答错，写短的每个 token 被罚得更重 ⇒ 模型学会「要错就错得长一点」⇒ 训练后期剩下的大多是答错的，于是表现不涨而长度一直涨</b>。",
        "w": " 这一讲的难度和 L6 完全不同：<b>数学很少，但新概念和缩写密度极高（RAG、BM25、HyDE、NDCG、MCP、ReAct、A2A…）⇒ 难的不是推导，是「哪个词指哪件事」</b> ⇒ <b>听的时候把每个词挂到它解决的那个具体问题上，比记定义有用</b>。<br>⚠ 而「推理链<b>通常对用户是隐藏的</b>」这半句别跳过：<b>界面上那几行是另一个模型做的摘要，不是原始链 —— 而最硬的理由是商业的：原始链是最值钱的那份训练数据</b>。",
        "r": "⇒ 那张曲线的前半段是<b>正向</b>的：<b>RL 奖励「答对」⇒ 模型发现多想几步更容易答对 ⇒ 写得更长 ⇒ 真的答对更多 ⇒ 长度增长本来是「能力增长的副产品」</b>；问题只出在分岔点之后。<br>⇒ 而那个 bug <b>难发现正是因为它不在奖励里，它在损失的分母里</b> —— L6 把这件事总结成一句方法论：<b>每一个归一化、每一个对称假设，都是一个隐含的偏好声明</b>。<br>⇒ 这一讲两个半场：<b>上半场 Afshine 讲 RAG，下半场 Shervine 讲工具与 agent</b>。",
        },
       {"t": "这一讲修的是 L6 那张弱点清单上的哪两条？分别用什么修？",
        "o": ["弱点 ① 和 ④；分别用 GRPO 和新的 benchmark",
              "弱点 ②（知识停在 cutoff date）用 RAG，弱点 ③（全是说、没有做）用 tool calling 与 agent —— 而 ④（难评估）留给 L8",
              "弱点 ① 和 ②；都用 RAG",
              "弱点 ③ 和 ④；都用 agent"],
        "a": 1,
        "w": "⇒ 两条解法的性质不同：RAG 补「读到的」，工具补「做得到的」—— 而讲者后面会点明两者「在某种意义上都在做同一件事」。"})
