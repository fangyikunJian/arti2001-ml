# -*- coding: utf-8 -*-
"""CME295 L7 模块 o —— 字幕第 881–950 句（94:52–101:14）：⭐ ReAct 循环逐步走查
（泰迪熊觉得冷），以及多 agent 与 A2A 协议。
"""


def loop(cur):
    """observe / plan / act 三格，cur 高亮其中一个。"""
    labs = ("observe 观察", "plan 计划", "act 行动")
    out = ""
    for i, lab in enumerate(labs):
        cls = '"y"' if (i + 1) == cur else '"d"'
        out += '  boxNode(%d,254,300,48,"%s",%s);\n' % (160 + i * 340, lab, cls)
        if i:
            out += '  link(%d,278,%d,278);\n' % (160 + i * 340 - 40, 160 + i * 340)
    out += '  note("⟵  还没达成目标就绕回来",640,318,"g");\n'
    return out


def add(KP):

    KP("⭐ ReAct 循环走查，与多 agent",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("94:52","you might see the language changing a bit from paper to paper",166);
  note("⭐ 三个阶段，以及一个很接地气的例子",640,222,"y");
''' + loop(0) + r'''  boxNode(300,348,680,42,"输入：我的泰迪熊冷了，请做点什么","b");''',
         "<b>他先把三个阶段摆出来，然后用一个很接地气的例子走一遍。</b><br>⭐ 三阶段是 <b>observe（观察）→ plan（计划）→ act（行动）</b>,但讲者加了一个很诚实的提醒：「<b>它不一定非得叫这个名字、也不一定非得是这个顺序 —— 比如 ReAct 原论文引入的我想是 think、observe、act；你会看到说法从一篇论文到另一篇在变，但高层直觉不变</b>」。<br>⚠ 例子是：<b>天气转凉，「我的泰迪熊冷了，请做点什么」</b>。<br>⇒ 请带着一个问题看接下来五镜：<b>这句话里既没有「温度」也没有任何数字，而系统最后真的把空调调高了 5 度 —— 中间每一步是怎么接上的</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("95:28","first, you have this observe stage, which translates the user query into an actionable formulation",166);
  note("⭐ 第一步 observe：把一句话翻译成「可以动手的说法」",640,222,"y");
''' + loop(1) + r'''  boxNode(120,348,1040,42,"用户的熊冷了，这可能和房间当前温度有关，而那个温度现在未知","y");''',
         "<b>第一步 observe 做的事，用一句话说就是「翻译」。</b><br>⭐ 「<b>你有这个 observe 阶段，它把用户的查询翻译成一个可以动手的表述</b>」—— 具体到这里：<b>「用户的泰迪熊冷了，这可能是因为房间当前的温度，而那个温度目前是未知的」</b>。<br>⚠ 请注意这一步<b>凭空多出了两样东西</b>：<b>① 它把「冷」接到了「温度」这个概念上（而用户没说温度）;② 它标出了「那个温度现在未知」—— 也就是识别出了一个缺口</b>。<br>⇒ 「<b>所以一下子你就知道，你得对温度做点什么</b>」。<b>observe 的产出不是答案，是「下一步该查什么」</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("95:52","which may be due to the current temperature of the room, which is currently unknown",166);
  says("96:15","you want to determine the temperature of the room",192);
  note("⭐ 第二步 plan：把那个缺口写成一件明确要做的事",640,222,"y");
''' + loop(2) + r'''  boxNode(80,348,520,42,"plan：确定房间的温度","v");
  boxNode(660,348,520,42,"act：调用 get_current_room_temperature","g");''',
         "<b>第二步 plan，第三步 act —— 而它们的分工很干净。</b><br>⭐ <b>plan 把那个「未知」变成一件明确要做的事：「你想确定房间的温度」;而「幸运的是，在你的工具里你可能正好有做这类事的东西 —— 这就是你用上它的地方」⇒ act 阶段就是「用上这些可能在上下文里的 API」,比如 get_current_room_temperature</b>。<br>⚠ 请看清三者的分工：<b>observe 说「现在是什么情况」,plan 说「那该做什么」,act 说「用哪个工具做」—— 而上一块讲的 tool calling，正好整个嵌在 act 这一格里</b>。<br>⇒ <b>agent 不是取代工具，它是在工具外面套了一个循环</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("96:56","this is why you go back to the observed stage",166);
  note("⭐ 工具返回之后，为什么要绕回 observe",640,222,"y");
''' + loop(1) + r'''  boxNode(80,348,520,42,"工具返回：65 华氏度","b");
  boxNode(660,348,520,42,"observe：比预期冷","y");''',
         "<b>工具返回了一个数，而光有数还不够 —— 所以绕回 observe。</b><br>⭐ 「<b>这些工具对 LLM 有用，是因为你把信息以它能解读的形式输出回去 ⇒ 这个工具返回了温度，而你现在需要解读这个温度意味着什么 —— 这就是为什么你回到 observe 阶段：你描述世界现在是什么样子、以及你该对它做什么</b>」。<br>⚠ 这一步是<b>整个循环的关键</b>：<b>65 华氏度本身不是结论，「65 度比预期冷」才是 ⇒ observe 负责把「事实」变成「判断」</b>。<br>⇒ 而「<b>比预期冷</b>」这个判断，正是下一轮 plan 的输入。<b>循环就是这样一圈圈接上的</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("97:06","the temperature of the room is cold",166);
  says("97:27","I need to increase the temperature",192);
  note("⭐ 第二圈：plan ⟶ act ⟶ observe ⟶ 退出",640,222,"y");
  seq(60,254,["plan：要升温","act：调升温函数","observe：温度对了","退出循环"],"g",270,48);
  note("「一旦完成，observe 阶段断定温度已经设到正确的温度」",640,330,"y");
  note("⚠ 而退出的依据不是「做完了几步」,是「目标达成了没有」",640,374,"r");''',
         "<b>第二圈走得很快，而循环就在这里收口。</b><br>⭐ <b>plan：「这比预期冷，所以我需要把温度升上去」⇒ act：「幸运的是它有一个函数能接收升温的参数，于是你可以调整温度」⇒ observe：「一旦完成，observe 阶段断定温度现在已经设到了正确的温度」⇒ 「这就是你可以退出循环、把回应返回给用户的时候」</b>。<br>⚠ 请注意<b>退出的依据</b>:<b>不是「走满了几步」,而是「目标达成了没有」—— 而那个判断是 observe 阶段做的 ⇒ 所以 observe 既是入口也是出口，它在每一圈都要回答「到了吗」</b>。<br>⇒ 最后输出给用户的是人话：「<b>我们把温度调高了 5 度</b>」。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("97:58","this is the time where you can exit the loop and return the response to the user",166);
  says("98:32","at each stage, the LLM tries to see if it has reached the goal yet",192);
  note("⭐ 到底什么让一个工作流成为「agentic」的",640,222,"y");
  boxNode(60,254,250,46,"一个初始查询","b");
  boxNode(330,254,250,46,"一些能做的动作","g");
  boxNode(600,254,310,46,"每一步问「到了吗」","y");
  boxNode(930,254,250,46,"到了才输出","v");
  note("「否则它可能还有更多推理循环，在那里做更多工作」",640,330,"g");
  note("⚠ 一句话：agent = 工具 + 循环 + 一个「达成没有」的判断",640,374,"r");''',
         "<b>讲者在这里把定义收了一次，而这是整块最该记的一句。</b><br>⭐ 「<b>我刚才描述的那个循环里的东西，就是让一个工作流成为 agentic 的那件事：你有某个初始查询、有一些你能执行的动作，然后在每一个阶段，LLM 试着看它有没有达成目标 —— 如果达成了，它就去输出阶段；否则它可能还有更多推理循环，在那里做更多工作</b>」。<br>⚠ 所以一句话版本是：<b>agent = 工具 + 循环 + 一个「达成没有」的判断</b>。<br>⇒ 而这也立刻暴露了它的风险：<b>如果那个判断出错，它要么提前收工、要么永远转下去 —— 讲者最后那一段讲的正是这件事</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("99:07","you could have an agent for setting the thermostat",166);
  says("99:50","this is what prompted Google to release the Agent2Agent protocol earlier this year",192);
  note("⭐ 再上一层：不止一个 agent",640,222,"y");
  boxNode(60,254,250,46,"调温度的 agent","g");
  boxNode(330,254,250,46,"管能耗的 agent","b");
  boxNode(600,254,250,46,"管空气质量的 agent","v");
  boxNode(890,254,290,46,"用户只对其中一个说话","y");
  note("「而可能让它们全都互相通信」—— 于是又需要一套标准",640,330,"g");
  note("⚠ 和工具那边一模一样的故事：MCP 管「模型↔工具」,A2A 管「agent↔agent」",640,374,"r");''',
         "<b>再往上推一层：家里不止一个 agent。</b><br>⭐ 「<b>你可以有一个调恒温器的 agent；但也许在你家里，你还想管能源怎么分配、或者空气质量 ⇒ 所以你可以有不同的 agent。而一个有意思的用例是：让用户对其中一个 agent 说话，然后可能让它们全都互相通信</b>」。<br>⚠ 于是同一个故事又演了一遍：「<b>这就引出了对 agent 之间通信也要标准化的潜在需求，类似于我们在 LLM host 和工具之间看到的那样 ⇒ 这正是促使 Google 在今年早些时候发布 Agent2Agent 协议的原因</b>」。<br>⇒ <b>MCP 管「模型 ↔ 工具」,A2A 管「agent ↔ agent」—— 两层，两套协议</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("100:12","it typically exposes a set of skills",166);
  says("100:29","define how the agent executes a given request",192);
  note("⭐ A2A 要你定义的两样东西",640,222,"y");
  boxNode(80,254,500,50,"① 这个 agent 会做什么","g");
  boxNode(700,254,500,50,"② 它怎么执行一个请求","y");
  note("一组 skills，还要给例子让别的 agent 知道",330,328,"g");
  note("执行时发什么状态 · 被叫停时怎么取消",950,328,"y");
  note("⚠ 而每个 agent「独立运作、有自己的推理循环」—— 彼此只看得到输入输出",640,374,"r");''',
         "<b>A2A 具体要你填什么，讲者给了两样。</b><br>⭐ <b>① 能力：「它典型地暴露一组 skills —— 它能做些什么，而且它给出例子，好让别的 agent 知道」;② 执行：「另一个关键的事情是定义这个 agent 怎么执行一个给定的请求 —— 比如执行一个查询时，你向别的 agent 发出什么状态？还有一个 cancel 方法，假如某个 agent 说『停下你在做的事』,取消一个动作的流程是什么？」</b><br>⚠ 而一个学生问「每个 agent 是不是一个带上下文做某些任务的 LLM」,答案是<b>可以这么理解</b>：「<b>这些 agent 独立运作 —— 它们有自己的推理循环，而别的 agent 看到的只有输入和输出</b>」。另一个学生提醒<b>token 预算可能失控</b>,讲者承认「这确实是个顾虑」。", 0)],
       {"h": "⭐ ReAct 循环与多 agent",
        "k": "三阶段：<b>「我们把这些步骤分成 observe、plan、act —— 但它不一定非得叫这个名字或是这个顺序；比如 ReAct 原论文引入的我想是 think、observe、act ⇒ 你会看到说法从一篇论文到另一篇在变，但高层直觉不变」</b>；例子是「<b>我的泰迪熊冷了，请做点什么</b>」。<br>走查：<b>① observe「把用户的查询翻译成一个可以动手的表述」——「用户的泰迪熊冷了，这可能是因为房间当前的温度，而那个温度目前是未知的」; ② plan ——「你想确定房间的温度」,而「幸运的是在你的工具里你可能正好有做这类事的东西」; ③ act —— 调 get_current_room_temperature；④ 回到 observe ——「这些工具对 LLM 有用，是因为你把信息以它能解读的形式输出回去⋯⋯你现在需要解读这个温度意味着什么」,结论是「65 华氏度，比预期冷」; ⑤ plan「我需要把温度升上去」⇒ act 调升温函数 ⇒ observe「断定温度现在已经设到了正确的温度」⇒ 「这就是你可以退出循环、把回应返回给用户的时候」</b>。<br>收口：<b>「我刚才描述的那个循环里的东西，就是让一个工作流成为 agentic 的那件事：你有某个初始查询、有一些你能执行的动作，然后在每一个阶段 LLM 试着看它有没有达成目标 —— 达成了就去输出阶段，否则它可能还有更多推理循环」</b>。<br>多 agent 与 A2A：<b>「你可以有一个调恒温器的 agent⋯⋯还想管能源分配、或者空气质量」⇒ 「让用户对其中一个说话，然后让它们全都互相通信」⇒ 「这正是促使 Google 在今年早些时候发布 Agent2Agent 协议的原因」; 它要你定义「一组 skills（它能做什么，并给出例子）」和「这个 agent 怎么执行一个给定的请求（发什么状态、怎么 cancel）」; 而「这些 agent 独立运作，它们有自己的推理循环」</b>。",
        "m": "⭐ 三格的分工很干净：<b>observe 说「现在是什么情况」,plan 说「那该做什么」,act 说「用哪个工具做」—— 而上一块讲的整套 tool calling，正好嵌在 act 这一格里 ⇒ agent 不是取代工具，它是在工具外面套了一个循环</b>。<br>⭐ 而<b>第二次 observe 是整个循环的关键</b>:<b>65 华氏度本身不是结论，「65 度比预期冷」才是 ⇒ observe 负责把「事实」变成「判断」,而那个判断正是下一轮 plan 的输入</b>。<br>⭐ 退出的依据<b>不是「走满几步」,是「目标达成了没有」</b>:<b>而那个判断由 observe 做 ⇒ observe 既是入口也是出口，它每一圈都要回答「到了吗」</b> ⇒ 一句话：<b>agent = 工具 + 循环 + 一个「达成没有」的判断</b>。",
        "w": " 第一步 observe 凭空多出了两样东西，<b>值得单独体会</b>:<b>① 它把「冷」接到了「温度」这个概念上（用户没说温度）;② 它标出了「那个温度现在未知」—— 也就是识别出了一个缺口 ⇒ observe 的产出不是答案，是「下一步该查什么」</b>。<br>⚠ 而 ReAct 的三个阶段名字<b>不要死记</b>:原论文用的是 think / observe / act。<br>⚠ 「达成没有」那个判断一旦出错，<b>agent 要么提前收工、要么永远转下去 —— 讲者最后那一段讲的正是这件事</b>。",
        "r": "⇒ 两层两套协议请一起记：<b>MCP 管「模型 ↔ 工具」,A2A 管「agent ↔ agent」—— 而两者出现的逻辑一模一样：有了多个实现，就需要一个标准</b>。<br>⇒ 而 A2A 里 <b>cancel 这一项值得留意</b>:<b>它说明多 agent 系统里「停下来」本身就是一个需要被设计的动作</b>。<br>⇒ 一个学生提的 <b>token 预算</b> 问题讲者承认是真顾虑：<b>「每个 agent 不会吃掉彼此的预算，但它可能吃掉你的钱」</b>。<br>⇒ 更多（ReAct 原论文、A2A 规范、多 agent 的编排模式）见<b>深度笔记</b>。",
        },
       {"t": "ReAct 循环里，工具返回数据之后为什么要绕回 observe？而循环凭什么退出？",
        "o": ["为了记日志；走满固定步数就退出",
              "因为工具返回的是「事实」（65 华氏度），而 observe 负责把事实变成「判断」（比预期冷）——那个判断才是下一轮 plan 的输入；而退出的依据不是走了几步，是 observe 每一圈都回答的那个「目标达成了没有」",
              "为了省 token；由用户手动退出",
              "为了重新检索；达到上下文上限就退出"],
        "a": 1,
        "w": "⇒ 所以 observe 既是入口也是出口。而一句话版本是：agent = 工具 + 循环 + 一个「达成没有」的判断 —— 这个判断一旦出错，它要么提前收工、要么永远转下去。"})
