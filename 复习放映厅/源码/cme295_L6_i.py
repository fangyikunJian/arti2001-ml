# -*- coding: utf-8 -*-
"""CME295 L6 模块 i —— 字幕第 476–539 句（58:58–66:04）：GRPO 登场、名字拆开、和 PPO
共同的两件事、那个 value function 瓶颈、相对 advantage，以及「为什么这么做」。

⚠ 2026-11-07 第四轮：旁白压到约 280 字、13 镜 → 8 镜、4 KP → 1。
"""


def add(KP):

    KP("⭐ GRPO：它只改了 advantage 那一处",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("58:58","it has been the go to RL algorithm for all these reasoning tasks",166);
  says("59:11","GRPO stands for group relative policy optimization",192);
  note("⭐ 把名字拆开读，算法就说完了一半",640,222,"y");
  boxNode(70,254,340,50,"Group","y");
  boxNode(450,254,340,50,"Relative","v");
  boxNode(830,254,340,50,"Policy Optimization","g");
  note("参照是「同一 prompt 的一组」",240,330,"y");
  note("advantage 是「相对的」",620,330,"v");
  note("和 PPO 一样：优化策略",1000,330,"g");
  note("⚠ 出处是 DeepSeekMath（2024-02）—— R1 不是发明者，是最成功的使用者",640,374,"r");''',
         "<b>这一讲最常被引用的那个缩写终于登场了，而名字本身就是定义。</b><br>⭐ 先把结论给你，接下来几镜会好听很多：<b>GRPO 和 PPO 的目标完全一样、约束也完全一样，它们只在「advantage 怎么算」这一处不同 —— 而那一处的改动省掉了一整个模型</b>。<br>⚠ 再把 advantage 确认一遍（L5 讲过）:<b>advantage =「实际拿到的」−「本来预期的」;为正就把这个行为的概率往上调，为负就往下调</b> ⇒ 而「<b>本来预期的</b>」是什么，<b>就是 PPO 和 GRPO 唯一的分歧点</b>。注意 advantage 关心的从来不是「好不好」,而是「<b>比预期好不好</b>」。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("60:16","there is a key difference",166);
  note("⭐ GRPO 的「继承清单」—— 只有最后一格不一样",640,196,"y");
  boxNode(60,228,270,48,"目标 · advantage","g");
  boxNode(350,228,250,48,"clip","g");
  boxNode(620,228,250,48,"KL penalty","g");
  boxNode(890,228,320,48,"advantage 怎么算","r");
  note("✓ 和 PPO 一样",195,300,"g");
  note("✓ 一样",475,300,"g");
  note("✓ 一样",745,300,"g");
  note("✗ 不一样",1050,300,"r");
  note("⚠ clip 管「速度上限」（对 π_old）· KL 管「位移上限」（对 π_ref）—— 两条并存",640,348,"r");''',
         "<b>他把 L5 那两层「别跑太远」又说了一遍，然后给出这一整块那句关键的话。</b><br>⭐ 这个「<b>只改一处</b>」的结构本身值得学：<b>GRPO 不是一个新框架，它是对一个成熟算法的一处替换 —— 而那一处替换省掉了一整个要训练的模型 ⇒ 改动最小、收益最大、而且你一眼就能看懂改了什么，这是最好的那种论文</b>。<br>⚠ 而那两层约束很容易混：<b>偏离「旧模型」（π_old，上一轮 RL 迭代）由 clip 管；偏离「基础模型」（π_ref，SFT 那个）由 KL 惩罚管 —— 它们并存，不是二选一</b>。从这里开始的几镜是技术核心，请放慢。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("60:50","along with something else that it was training jointly at training time, which was called the value function",166);
  says("61:37","you had to train a value function jointly with your policy",192);
  note("⭐ 先把 PPO 那一套回忆完，不然下一镜的对比没有意义",640,222,"y");
  boxNode(80,254,500,50,"奖励是「completion 级」","y");
  boxNode(700,254,500,50,"更新要「token 级」","v");
  note("整条写完才有一个数",330,328,"y");
  note("每个 token 都要决定上调还是下调",950,328,"v");
  note("⇒ 所以要一个 value function 告诉你「写到这里形势好不好」（功劳分配）",640,372,"g");''',
         "<b>先把 PPO 那一套完整回忆一遍，然后是那个瓶颈。</b><br>⭐ value function 的定义原样记住：<b>输入是一段部分生成（prompt + 写了一半的回答）,输出是「如果按当前策略写完，最终奖励大概是多少」—— 它是一个「预期」的估计器，而 advantage 就是「实际 − 预期」</b>。<br>⚠ 而「<b>联合训练</b>」这四个字是瓶颈的源头，代价算一下：<b>它典型地和策略一样大（比如 7B）,要存参数 + 梯度 + 优化器状态 ⇒ 大致把训练显存翻了一倍；而且它还要调超参、还可能训不稳 —— 它自己就是一个会出问题的模型 ⇒ 去掉它不只是省钱，也去掉了一个误差来源</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("61:59","compare it with the average of rewards of completions for that same prompt",166);
  says("62:35","a relative measure of the reward for that completion and all the other rewards of the other completions",192);
  note("⭐ 整个 GRPO 的核心，就这一句",640,222,"y");
  boxNode(80,254,500,50,"PPO：模型「预测」预期","r");
  boxNode(700,254,500,50,"GRPO：同组样本「当场测」","g");
  note("学出来的估计器",330,328,"r");
  note("蒙特卡洛估计：A_i = r_i − 组内均值",950,328,"g");
  note("⚠ 一组全对或全错 ⇒ advantage 全为 0 ⇒ 这道题不产生梯度（免费的课程学习）",640,374,"r");''',
         "<b>整个 GRPO 的核心就这四句话，而这一招只换了一样东西。</b><br>⭐ 为什么它在 LLM 上特别合适、在传统 RL 上不行：<b>传统 RL 里一个状态只能走一次（你没法把机器人倒回去重走）；LLM 里同一个 prompt 可以采样无数次，每次都是一个完整独立的轨迹 ⇒ 「同一个起点重开 g 次」在 LLM 上免费 —— 这就是为什么 GRPO 必须等到 LLM 时代才被发明</b>。<br>⚠ 「<b>同一个 prompt</b>」是全部的关键：<b>比较只能在同一道题内部进行，跨题比较没有意义（难题的奖励本来就低）</b>；而那个「全对全错不产生梯度」<b>既是免费的 curriculum，也是一个已知缺点 —— 那一组算力白费了，DAPO 专门在修</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("63:02","the big benefit here is that we do not use value functions",166);
  note("⭐ 好处一句话，而那笔交换非常清楚",640,196,"y");
  boxNode(80,228,500,50,"省下：一个要训的大模型","g");
  boxNode(700,228,500,50,"付出：每题生成 g 条","y");
  note("参数 + 梯度 + 优化器状态 + 调参 + 不稳",330,302,"g");
  note("推理算力 × g",950,302,"y");
  note("⭐ 它是「把训练成本换成了推理成本」—— 而这笔交换划算",640,348,"y");
  note("⚠ 生成是推理（不存梯度、可并行）,训 value function 是训练（显存好几倍）",640,386,"r");''',
         "<b>好处用一句话说完，而那个交换不是「净赚」,要算清楚。</b><br>⭐ 为什么划算的理由很具体：<b>生成 completion 是「推理」⇒ 不存梯度、可大批量并行、可用量化和 FlashAttention；训一个 value function 是「训练」⇒ 要存梯度和优化器状态 ⇒ 「多生成几条」比「多训一个模型」便宜得多，工程上也简单得多</b>。<br>⚠ 而「<b>我们做的唯一一件事</b>」值得记住：<b>GRPO 的全部实现差异就是「采 g 条，然后减去均值」—— 没有新网络、没有新损失项、没有新超参（除了 g）⇒ 改动小到几十行代码，这就是它被普及得这么快的原因</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("63:53","they have been developed before all these LLMs became a thing",166);
  says("64:51","use that as some kind of baseline to put this reward into context",192);
  note("⭐ 一个很有启发的角度：方法的假设来自它被发明时的那个问题",640,222,"y");
  boxNode(80,254,500,50,"PPO · 2017","d");
  boxNode(700,254,500,50,"GRPO · 2024","g");
  note("Atari / 机器人：轨迹长、每步有奖励、重开很贵",330,328,"d");
  note("LLM：只有终局奖励、重开几乎免费",950,328,"g");
  note("⚠ 所以那个「必须学一个估计器」的理由在 LLM 上消失了 —— GRPO 只是注意到了",640,374,"r");''',
         "<b>讲者的回答从一个时间差开始，而这个角度很有启发。</b><br>⭐ 请记下这个思维习惯：<b>一个方法的设计假设来自它被发明时的那个问题，而不是你现在的问题 ⇒ 搬用一个方法之前，先问「它当初是为什么样的问题设计的」</b>。<br>⚠ 而「<b>把奖励放进上下文</b>」这个说法非常准：<b>一个奖励数字本身没有意义 ——「这条回答拿了 1 分」什么也不告诉你，除非你知道「同一道题的其它尝试拿了多少分」⇒ 「上下文」= 同组的其它尝试</b>。这在统计上有标准名字（<b>减去基线以降低方差</b>）,<b>GRPO 的贡献不是提出这个想法，而是「找到一个不用训练就能得到的基线」</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("65:21","if you find a good solution, it's a good solution to a hard problem",166);
  note("⭐ 「难题的好解更值钱」—— 而它是自动实现的",640,196,"y");
  boxNode(80,228,500,50,"容易题：组内大多对","d");
  boxNode(700,228,500,50,"难题：组内大多错","y");
  note("组内平均高 ⇒ 你答对了 advantage 很小",330,302,"d");
  note("组内平均低 ⇒ 你答对了 advantage 很大",950,302,"y");
  note("⭐ 不需要任何额外机制 —— 它是「减去组内均值」的直接后果",640,348,"y");
  note("⚠ 而 PPO 也靠基线做这件事，但那个基线是一个模型「猜」的",640,386,"r");''',
         "<b>那个例子说清了「相对」为什么必要，而它自动实现的方式很优雅。</b><br>⭐ 和 PPO 一对照差别就清楚了：<b>PPO 的基线是模型猜的，猜得准不准直接决定这个校正对不对；GRPO 的基线是「当场测的」,所以天然更可靠</b>。<br>⚠ 「<b>烤进（bake into）</b>」这个词用得很好：<b>它指「不是外加一个规则，而是让它成为公式的自然结果」—— 而这正是好设计的标志：你想要的性质是机制的副产品，不是补丁；如果一个性质要靠额外规则来保证，通常说明主机制还没找对</b>。注意最终被改的是<b>每一个 token 的生成概率</b>,advantage 只是那个改动的幅度。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("65:37","GRPO was developed a year ago",166);
  says("66:04","we will have a walkthrough of exactly how it works",192);
  note("⭐ 时间差论证的收尾，以及一个很体贴的预告",640,222,"y");
  boxNode(80,254,500,50,"「改进了 PPO」","d");
  boxNode(700,254,500,50,"「为新问题重新设计」","g");
  note("原方法在同一个问题上做得不够好",330,328,"d");
  note("问题变了，原方法的假设不再适用",950,328,"g");
  note("⚠ 后者贡献往往更大，因为它需要你先看清「问题变了」这件事",640,374,"r");''',
         "<b>时间差论证的收尾，然后他预告：不懂没关系，马上有一次图示走查。</b><br>⭐ 在走查开始前，先自己把 GRPO 说一遍：<b>① 对一道题采 g 条 completion ② 每条算一个奖励 ③ advantage = 自己的奖励 − 这 g 条的平均 ④ 用它更新策略，clip 和 KL 照旧</b> —— 能说出这四步，下面的流程图就只是在给它配图。<br>⚠ 而讲者在这里还是用「<b>我会那样去想它</b>」这种措辞：<b>他在给一个「理解方式」,而不是在陈述论文里写的动机 —— 和他之前标注「我在做假设」是同一种克制</b>。走查里会补上一个细节：<b>advantage 实际上不只减均值，还除了一个标准差，而他会主动说「那可能不是最好的做法」</b>。", 0)],
       {"h": "⭐ GRPO：只改 advantage 那一处",
        "k": "<b>「它一直是所有这些推理任务的首选 RL 算法」; 「GRPO 代表 group relative policy optimization」</b>。<br>共同点与差别：<b>「有一个关键差别」—— 目标（最大化 advantage）、clip、KL penalty 三样都和 PPO 一样，只有「advantage 怎么算」不同</b>。<br>PPO 那一套：<b>「连同它在训练时联合训练的另一个东西，那个东西叫 value function」; 「你必须把一个 value function 和你的策略联合训练」</b>。<br>GRPO 的办法：<b>「把它和『同一个 prompt 的那些 completion 的奖励的平均值』比较」; 「衡量那个 completion 的奖励和所有其它 completion 的奖励之间的一个『相对度量』」⇒ 「这里的大好处是我们不用 value function 了」</b>。<br>为什么：<b>「传统的 RL 算法都是在所有这些 LLM 成为一件事之前被开发出来的」; 「用那个当成某种基线，把这个奖励『放进上下文』里」; 「如果你找到一个好的解，那是『对一个难问题的』好解」; 「GRPO 是一年前被开发出来的」⇒ 「我们会有一次关于它到底怎么工作的走查」</b>。",
        "m": "⭐ 名字拆开就说完了一半：<b>Policy Optimization 和 PPO 一样、Relative 是「相对某个参照」、Group 是「那个参照是同一个 prompt 的一组 completion」</b>；而 advantage =「实际 − 预期」,<b>「预期」是什么就是两者唯一的分歧点</b>。<br>⭐ 这一招的本质：<b>用「蒙特卡洛当场测」替换「学出来的估计器」—— A_i = r_i − 组内均值</b>；而它<b>在 LLM 上特别合适、在传统 RL 上不行</b>：<b>传统 RL 一个状态只能走一次，LLM 同一个 prompt 可以采样无数次 ⇒ 「重开 g 次」在 LLM 上免费，这就是为什么 GRPO 必须等到 LLM 时代</b>。<br>⭐ 而「难题的好解更值钱」是<b>自动实现</b>的：<b>难题组内平均低 ⇒ 同样答对 advantage 就更大 —— 它是「减去组内均值」的直接后果，不需要任何额外机制</b>。",
        "w": " 那笔交换不是「净赚」:<b>省下一个和策略同等大小的 value function（参数 + 梯度 + 优化器状态 + 调参 + 不稳）,付出每题生成 g 条 ⇒ 它把训练成本换成了推理成本 —— 而这划算，因为生成是推理（不存梯度、可并行）,训 value function 是训练（显存好几倍）</b>。<br>⚠ 两层约束别混：<b>clip 对 π_old 管「速度上限」,KL 对 π_ref 管「位移上限」—— 并存，不是二选一</b>。<br>⚠ 「一组全对或全错 ⇒ advantage 全为 0」<b>既是免费的课程学习，也是一个已知缺点</b>（那一组算力白费，DAPO 专门在修）。",
        "r": "⇒ 请记下这个思维习惯：<b>一个方法的设计假设来自它被发明时的那个问题 —— 搬用之前先问「它当初是为什么样的问题设计的」</b>；而「改进」和「<b>为新问题重新设计</b>」要分开：<b>后者贡献往往更大，因为它需要你先看清「问题变了」这件事</b>。<br>⇒ 「<b>烤进（bake into）</b>」是好设计的标志：<b>你想要的性质是机制的副产品，不是补丁</b>。<br>⇒ 更多（GAE 为什么被整个扔掉、功劳分配、GRPO 名字里每个词的来历、作者动机与讲者诠释的区别）见<b>深度笔记</b>。",
        },
       {"t": "GRPO 相对 PPO 只改了哪一处？而「难题的好解更值钱」是怎么实现的？",
        "o": ["改了 clip 的区间；靠给难题手动加权重",
              "只改了「advantage 怎么算」—— 用「同一 prompt 采 g 条的平均奖励」当基线（蒙特卡洛当场测，替换学出来的估计器）；而「难题更值钱」是「减去组内均值」的自动后果，不需要任何额外机制",
              "改了 KL 的参照物；靠一个难度分类器",
              "改了奖励模型；靠 value function 预测难度"],
        "a": 1,
        "w": "⇒ 而这招在 LLM 上才成立：传统 RL 一个状态只能走一次，LLM 同一个 prompt 可以重采无数次 —— 所以 GRPO 必须等到 LLM 时代才被发明。"})
