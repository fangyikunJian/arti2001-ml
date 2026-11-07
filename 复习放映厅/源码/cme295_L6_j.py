# -*- coding: utf-8 -*-
"""CME295 L6 模块 j —— 字幕第 540–610 句（66:49–73:16）：GRPO 与 PPO 的两张流程图、
哪些模型要训哪些冻结，以及两个损失函数的两个相同点、第一个不同点。

⚠ 2026-11-07 第四轮：旁白压到约 280 字、14 镜 → 9 镜、4 KP → 1。
"""


def add(KP):

    KP("⭐ 两张流程图，与两个损失函数的异同",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("66:49","you pass them through the reward model that gives you g rewards",166);
  says("67:09","it's reward minus the average over the standard deviation of those rewards is how they defined it",192);
  note("⭐ 流程图四步走完，而 advantage 比「减均值」多了一步",640,222,"y");
  seq(90,254,["query","策略 ⇒ g 条","g 个奖励","(r − 均值) / 标准差"],"g",250,48);
  note("⭐ 和 PPO 的差别只在第三步：1 条 vs g 条 —— 而它让 value function 可以不要了",640,330,"y");
  note("⚠ 而「除以标准差」讲者立刻打了问号：「顺带说一句」—— 这是一张欠条",640,370,"r");''',
         "<b>一张流程图四步就走完了，而实际公式比「减均值」多了一步。</b><br>⭐ 「<b>g</b>」就是名字里的 Group：<b>它是 GRPO 唯一新增的超参数，典型 8 到 64 —— 太小则均值估不准、advantage 噪声大；太大则每步要生成的 token 数线性增长</b>。<br>⚠ 而「除以标准差」的问题很具体：<b>一组里只有一条对 ⇒ 标准差很小 ⇒ 除完 advantage 巨大；对错各半 ⇒ 标准差最大 ⇒ 除完反而被压小 ⇒ 「几乎答不出的题」被放大，「刚好在能力边界上的题」被压制 —— 恰好和你想要的相反</b>。<b>后来 Dr. GRPO 正是把它去掉了 —— 一个被全行业抄了一年的公式，其中一项其实是可疑的</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("67:30","we, of course, don't want to deviate too much",166);
  note("⭐ GRPO 五步，请背下来",640,196,"y");
  seq(70,226,["采 g 条","算 g 个奖励","减均值 / 标准差","调策略（clip）","KL 拉住"],"g",225,48);
  note("⭐ 而真正的重点是这里「没有」的东西",640,302,"y");
  note("没有 value function · 没有 GAE · 没有「每 token 的价值估计」",640,342,"g");
  note("⚠ 少掉这三样，就是 GRPO 的全部卖点",640,382,"r");''',
         "<b>最后两步，GRPO 就讲完了 —— 一共五步。</b><br>⭐ 注意 <b>KL 那一项在 GRPO 里的位置和 PPO 不一样</b>（后面专门讲）:<b>GRPO 把 KL 写成「目标函数里显式的一项」,PPO 典型地「把它塞进 advantage 的奖励里」</b> —— 讲者说这「更像是一个技术细节」,<b>但它在读代码时会直接影响你找哪一行</b>。<br>⚠ 接下来几镜是 PPO 的同一张图，<b>而它会明显更复杂 —— 那个复杂度差距本身就是 GRPO 流行的原因</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("68:00","you only have one completion",166);
  says("68:51","only the last token has the reward of the whole completion",192);
  note("⭐ PPO 只采一条 —— 于是它「没有可比对象」",640,222,"y");
  seq(70,254,["−βKL","−βKL","−βKL","…","−βKL","r −βKL"],"d",185,46);
  note("一条 completion 有 T 个 token ⇒ 奖励是一个长度 T 的向量",640,330,"y");
  note("⚠ 前 T−1 格只有 KL 惩罚，只有最后一格带上任务奖励 r —— 任务奖励是稀疏的",640,372,"r");''',
         "<b>PPO 的前三步，差别只在「一条」还是「g 条」—— 而这一步信息量很大。</b><br>⭐ <b>「只采一条」和「必须训一个 value function」是因果关系，不是两个独立的设计选择</b>：<b>没有可比对象 ⇒ 必须从别处得到「预期值」⇒ 那就是 value function 存在的全部理由</b> ⇒ 反过来就是理解 GRPO 的最短路径：<b>采 g 条 ⇒ 有了可比对象 ⇒ 不再需要那个模型 —— GRPO 是「用采样换掉了一个模型」</b>。<br>⚠ 而把 KL 写成「每 token」是一个<b>「不用改算法，只改输入」的实现技巧</b>：<b>它解释了 L5 那个困惑 —— 公式里 KL 写在目标函数里，代码里它在奖励里，两者数学上等价</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("69:01","it's just good to know that people implement it that way",166);
  says("69:45","you can think of it as some complicated formula",192);
  note("⭐ PPO 手上有两个「每 token」的向量，而 GAE 把它们揉成一个",640,222,"y");
  boxNode(60,254,250,46,"奖励向量","y");
  boxNode(60,310,250,46,"价值向量","v");
  link(310,300,420,300);
  boxNode(420,278,280,50,"GAE","d");
  link(700,303,810,303);
  boxNode(810,278,330,50,"advantage 向量","g");
  note("⚠ GRPO 干脆不做 token 级的功劳分配 —— 整条共享同一个 advantage",640,382,"r");''',
         "<b>value function 也是「每 token」的，而 GAE 的工作就是把两个向量揉成一个。</b><br>⭐ 于是 <b>PPO 的复杂度来源清楚了</b>：<b>它要在「token 级」上做功劳分配 ⇒ 需要一个「每一步都能给出预测」的模型 ⇒ 而那个模型必须和策略同等规模（它也要读懂整个上下文）</b>。<br>⚠ GAE 一句话讲完：<b>它估「从第 t 步起比预期好多少」—— 只看下一步偏差小、看到结尾方差大，而 GAE 把各步长按 λ 的幂加权平均，一个偏差 / 方差的旋钮</b>。<b>而 GRPO 的 advantage 是「序列级」的 —— 这是一个真实的精度损失，但实践证明在 LLM 上不要紧，省下的成本很大</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("70:06","you use advantages that are a result of this group computation",166);
  note("⭐ 一个学生问了一个极好的问题：这些框里，哪些要训？",640,196,"y");
  boxNode(80,228,500,50,"PPO 的框","r");
  boxNode(700,228,500,50,"GRPO 的框","g");
  note("策略 · 参考 · 奖励 · 价值",330,302,"r");
  note("策略 · 参考 · 奖励",950,302,"g");
  note("⭐ 但框不等于模型 —— 有的要训，有的冻住，有的根本不是模型",640,348,"y");
  note("⚠ 而「要训几个」才是决定成本的那个数 —— 下面两镜把这笔账算精确",640,386,"r");''',
         "<b>把两者的 advantage 来源并排说一次，然后一个学生问了一个极好的问题。</b><br>⭐ 这个问题问的正是最实际的那一点：<b>流程图上画了好几个框，但框不等于模型 —— 而「要训几个模型」才是决定成本的那个数</b>。<br>⚠ 在看答案之前你可以先自己数一遍。<b>这一问会把 L5 那个「四个模型」的粗略说法精确化：「养」里面，「要训」和「只要前向」的成本差好几倍</b>。另外讲者又强调了一次 <b>PPO 的 advantage 是 token 级的</b> —— 这是两者精度上的差别。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("70:52","in the reasoning case, we are actually not training a reward model",166);
  note("⭐ 先说「冻住」的那些 —— 而推理场景里少掉了一整个",640,196,"y");
  boxNode(80,228,500,50,"冻结：只做前向","d");
  boxNode(700,228,500,50,"要训：还要梯度 + 优化器","r");
  note("只占参数的显存",330,302,"d");
  note("显存大约是前者的 4 倍",950,302,"r");
  note("⭐ 而推理场景里根本没有奖励模型 —— 那一格是一段代码，不占显存",640,348,"y");
  note("⚠ L5：策略+价值（训）+ 参考+奖励（冻）= 4 个网络 ｜ L6：2 个网络 + 1 段代码",640,386,"r");''',
         "<b>先说「冻住的」那些，而推理场景里少掉了一整个。</b><br>⭐ 「<b>冻结</b>」的实际含义：<b>只做前向、不算梯度、不更新参数 ⇒ 只占参数的显存，不占梯度和优化器状态；而梯度 + Adam 状态大致是参数的 3 倍 —— 所以「冻结」和「要训」在成本上差 4 倍</b>。<br>⚠ 而那一格在推理里<b>根本不是一个网络</b>：<b>一般 RLHF 里奖励模型是一个和策略同等规模、训好后冻住的网络；推理场景里它是一段 Python 代码（跑单元测试、比字符串）⇒ 不占显存、不占 GPU、也不会给错答案</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("71:21","in the GRPO case, we only train the policy model",166);
  note("⭐ 讲者第二次说「关键差别」—— 而这次说的是成本",640,196,"y");
  boxNode(80,228,500,50,"PPO 要训 2 个","r");
  boxNode(700,228,500,50,"GRPO 要训 1 个","g");
  note("策略 + value function，同等规模",330,302,"r");
  note("只有策略",950,302,"g");
  note("⭐ 「要训」是最贵的那一类 ⇒ 这大致把训练显存需求砍掉一半",640,348,"y");
  note("⚠ 两次「关键差别」是同一件事：换 advantage 的算法 = 省掉那个模型",640,386,"r");''',
         "<b>关键差别，讲者亲口定性 —— 而这次是从成本的角度说的。</b><br>⭐ 两次「关键差别」说的内容不同但指的是同一件事：<b>第一次是方法上的（「差别在于它怎么计算 advantage」）,这一次是成本上的（「差别在于我们训练哪些模型」）</b>。<br>⚠ 顺便把它放进这门课的大图景：<b>L4 讲怎么让一次训练 / 推理更省（量化、FlashAttention、MoE）；L5 讲怎么对齐，而代价是四个模型；L6 在可验证任务上把那四个砍到两个 + 一段代码 ⇒ 这门课从头到尾都在算同一笔账：怎么用更少的资源拿到同样的能力</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("71:57","they look scary",166);
  says("72:11","both of them, they operate on the ratio of the probability of the current policy and the probability of the old policy",192);
  note("⭐ 从图切到数学 —— 而两个公式各有同样的三块",640,222,"y");
  boxNode(80,254,340,48,"ratio × advantage","g");
  boxNode(470,254,340,48,"clip","y");
  boxNode(860,254,340,48,"KL","v");
  note("动力：往哪推、推多少",250,330,"g");
  note("速度限制：一步最多多远",640,330,"y");
  note("位移限制：总共最多离家多远",1030,330,"v");
  note("⚠ 陷阱：r_θ 不是奖励，是概率比；而「old」是上一轮 RL 迭代，不是 SFT 模型",640,374,"r");''',
         "<b>从图切到数学，而讲者的处理方式很聪明：他不逐符号解释，他找相同点和不同点。</b><br>⭐ 这是读任何「X 的改进版」论文的正确姿势：<b>只读 diff —— 你只需要记住差异，共同部分 L5 已经讲过了</b>。<br>⚠ 那个比值在做什么一句话说清：<b>&gt; 1 ⇒ 新策略更倾向于这条输出，&lt; 1 ⇒ 更不倾向；乘上 advantage 就是「往好的方向推，推多少由 advantage 定」</b>；而 clip <b>把这个比值截断在 [1−ε, 1+ε]（典型 ε = 0.2）⇒ 一次更新最多把概率改变 20%，防止一步推到坏区域而 RL 很难回来</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("72:58","this clipping function just allows you to not make updates that are too big",166);
  note("⭐ clip 的两张图，以及第一个不同点",640,194,"y");
  axes({x0:260,x1:1020,y0:330,y1:214});
  curve([[260,320],[560,240],[1020,240]],"g");
  curve([[260,240],[760,240],[1020,320]],"r");
  note("advantage 为正：超过 1+ε 就削平",400,224,"g");
  note("为负：低于 1−ε 也削平",900,224,"r");
  note("比值 r_θ  ⟶",1020,352,"d","end");
  note("⚠ 第一个不同点：同一个 KL，GRPO 写在目标函数里，PPO 塞在奖励里",640,382,"r");''',
         "<b>讲者直接把你送回 L5 那两张图，然后给出第一个不同点。</b><br>⭐ 两张图的结论：<b>clip 是「单边封顶」—— 往对的方向走可以，但一步走太远就没有收益了</b>；为什么不直接加惩罚项：<b>惩罚项会把梯度一直拉回来，哪怕那一步本来是对的；clip 在允许范围内完全不干扰，超出后梯度直接变零 —— 「不罚你，只是不再奖励你」</b>。<br>⚠ 而 KL 位置这个「技术细节」有一个实际后果：<b>PPO 的 KL 要经过 GAE 加权 ⇒ 实际强度被 λ 和 γ 影响；GRPO 的 KL 直接以 β 出现 ⇒ 可控、可读 ⇒ 读代码时：PPO 去看奖励向量怎么拼的，GRPO 去看损失的最后一项</b>。", 0)],
       {"h": "⭐ 两张流程图与损失的异同",
        "k": "GRPO 五步：<b>「你把它们过一遍那个给你 g 个奖励的奖励模型」; 「他们定义的方式是：奖励减去平均值，再除以那些奖励的标准差」; 「我们当然不想偏离太多」</b>。<br>PPO 同一张图：<b>「你只有一条 completion」; 「只有最后一个 token 带着整条 completion 的奖励」; 「人们是那样实现的，知道一下就好」; 「你可以把它想成某个复杂的公式」（GAE）; 「你用的是这个组计算得出的那些 advantage」</b>。<br>哪些要训：<b>「在推理这个情形里，我们其实并没有在训练一个奖励模型」; 「在 GRPO 的情形里，我们只训练策略模型」</b>。<br>两个损失：<b>「它们看起来很可怕」; 「两者都作用在当前策略的概率和旧策略的概率之比上」; 「这个裁剪函数只是让你不做太大的更新」; 「那个 KL 散度其实是目标函数里显式的一部分」</b>。",
        "m": "⭐ 两张图的差别只在第三步（<b>1 条 vs g 条</b>）,而<b>「只采一条」和「必须训一个 value function」是因果关系</b>：<b>没有可比对象 ⇒ 必须从别处得到「预期值」⇒ 那就是 value function 存在的全部理由 ⇒ 反过来，采 g 条就不再需要它 —— GRPO 是「用采样换掉了一个模型」</b>。<br>⭐ 而「<b>框不等于模型</b>」:<b>冻结 = 只做前向，只占参数显存；要训还要梯度 + 优化器状态（大致是参数的 3 倍）⇒ 两者成本差 4 倍</b> ⇒ 账算出来是：<b>L5 的 RLHF + PPO = 4 个网络（2 个要训）;L6 的推理 + GRPO = 2 个网络 + 1 段代码（1 个要训）—— 最贵的那一项减半</b>。<br>⭐ 两次「关键差别」是同一件事：<b>换 advantage 的算法 = 省掉那个模型</b>。",
        "w": " 「<b>除以标准差</b>」是一张欠条：<b>一组里只有一条对 ⇒ 标准差小 ⇒ advantage 被放大；对错各半 ⇒ 标准差大 ⇒ 反而被压小 ⇒ 恰好和你想要的相反，而后来 Dr. GRPO 把它去掉了</b>。<br>⚠ 两个符号陷阱在这里最容易中招：<b>r_θ 不是奖励，是「新策略 ÷ 旧策略」的概率比；而「old」是上一轮 RL 迭代的策略，SFT 模型叫 π_ref（它在 KL 那一项里）</b>。<br>⚠ 而 <b>GRPO 的 advantage 是「序列级」的</b>（整条共享一个值）,PPO 是 token 级的 —— <b>这是一个真实的精度损失，但实践证明在 LLM 上不要紧</b>。",
        "r": "⇒ KL 位置这个「技术细节」有实际后果：<b>PPO 的 KL 经过 GAE 加权 ⇒ 强度被 λ、γ 影响；GRPO 的 KL 直接以 β 出现 ⇒ 可控可读 ⇒ 读代码时 PPO 去看奖励向量怎么拼的，GRPO 去看损失的最后一项</b>。<br>⇒ clip 是「<b>单边封顶</b>」:<b>不罚你，只是不再奖励你 —— 比惩罚项温和</b>；而它和 KL 管两件事：<b>clip 对 π_old 管速度，KL 对 π_ref 管位移</b>。<br>⇒ 更多（GAE 的 λ 旋钮、per-token 奖励向量的实现、这门课从 L4 到 L6 的同一笔账）见<b>深度笔记</b>。",
        },
       {"t": "为什么 PPO 必须训一个 value function，而 GRPO 不用？这笔账差多少？",
        "o": ["因为 PPO 的损失更复杂；差一点点显存",
              "因为 PPO 只采一条 completion ⇒ 没有可比对象 ⇒ 必须从别处得到「预期值」；而 GRPO 采 g 条就有了可比对象。账是：L5 的 RLHF 4 个网络（2 个要训），L6 是 2 个网络 + 1 段代码（1 个要训）—— 最贵的那一项减半",
              "因为 PPO 的奖励是 token 级的；差四倍算力",
              "因为 GRPO 不需要 KL；差一个优化器"],
        "a": 1,
        "w": "⇒ 所以 GRPO 不是「发明了一个新的 advantage」，它是「用采样换掉了一个模型」。而「冻结」和「要训」在成本上差 4 倍（梯度 + Adam 状态大致是参数的 3 倍）。"})
