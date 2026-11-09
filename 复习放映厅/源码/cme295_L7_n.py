# -*- coding: utf-8 -*-
"""CME295 L7 模块 n —— 字幕第 811–880 句（87:48–94:21）：tool selection（两阶段结构
第二次出现）、MCP，以及 agent 的定义。
"""


def add(KP):

    KP("⭐ tool selection、MCP，与 agent 的定义",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("87:31","the goal here is to restrict the number of tools to only those that might be useful",166);
  note("⭐ tool selector 两步 —— 而这个形状你见过",640,196,"y");
  boxNode(50,228,300,50,"查询 + 工具清单","b");
  link(350,253,410,253);
  boxNode(410,228,360,50,"LLM 挑出可能相关的","y");
  link(770,253,830,253);
  boxNode(830,228,350,50,"只把这几个放进上下文","g");
  note("清单里每个工具只有「API 名字 + 一两个词的描述」—— 所以这一级很便宜",640,304,"y");
  note("⚠ 它也叫 router（路由）—— 「tool selection 和 routing 是相近的概念」",640,348,"r");''',
         "<b>那张欠条还了，而解法的形状和上半场一模一样。</b><br>⭐ 讲者引的是 <b>Google DeepMind 的一篇技术论文</b>:<b>第一步，「你有你的查询，和一份想多大就多大的工具清单 —— 而这份清单只含 API 名字、也许还有一两个词说它是干什么的」,让 LLM 挑出可能相关的；第二步，「你把选中的工具 API 连同查询一起，只把这些喂进上下文」</b>。<br>⚠ 请把它和上半场逐项对上：<b>「只有名字和一句话」＝ 便宜判据；「挑出可能相关的」＝ 最大化 recall；「只把这几个的完整定义放进去」＝ 候选少了才负担得起昂贵判据</b> ⇒ <b>这就是那条线的第二次出现</b>。它还有一个名字叫 <b>router</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("88:19","you could do it with RAG",166);
  says("88:52","we are going to go very quickly on the standardization issue",192);
  note("⭐ 一个很敏锐的提问：这不就是 RAG 吗？",640,222,"y");
  boxNode(80,254,500,50,"学生：那基本上就是 RAG？","b");
  boxNode(700,254,500,50,"讲者：你可以用 RAG 做，但不是非得","y");
  note("「这是个很好的点」",330,328,"b");
  note("「你也可以让一个 LLM 来干这活，就是挑对工具」",950,328,"y");
  note("⚠ 它们确实同形：都是「从一大堆候选里挑相关的」—— 只是候选从文档换成了工具",640,374,"r");''',
         "<b>马上有学生看穿了：这不就是 RAG 吗？而这个提问非常敏锐。</b><br>⭐ 讲者的回答是「<b>你可以用 RAG 来做，这是个很好的点 —— 但它不一定非得是。你也可以让一个 LLM 来干这活，就是挑对工具，你给 LLM 一些指令让它输出正确答案</b>」。<br>⚠ 这位学生看到的正是<b>这一讲最该带走的那个结构</b>:<b>「从一大堆候选里挑出相关的少数」—— 候选是文档就叫 RAG，候选是工具就叫 tool selection，而解法可以完全一样</b>。<br>⇒ <b>认出这种同构，比记住两套名词有用得多</b>。接下来是第四个缺点：标准化。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("89:17","there is a standard called MCP",166);
  says("89:35","it is called a model context protocol",192);
  note("⭐ 第四个缺点的解法：MCP",640,222,"y");
  boxNode(80,254,500,50,"问题","r");
  boxNode(700,254,500,50,"MCP","g");
  note("每家 LLM 一套写法 ⇒ 同一个工具要实现很多遍",330,328,"r");
  note("一套标准的「怎么把工具暴露给模型」",950,328,"g");
  note("⚠ 「重复不是你想要的」—— 这就是所有协议存在的理由",640,374,"r");''',
         "<b>第四个缺点（没有标准）的解法：MCP。</b><br>⭐ 问题讲者说得很直白：「<b>指定一个工具实现的方式，可能是为某个 LLM 量身定做的 —— 而你不会想要那样，因为对每个 LLM 你可能都得把这些工具一遍遍重新实现；而重复不是你想要的</b>」。<br>⭐ 于是：「<b>这就是为什么有一个叫 MCP 的标准 —— 它来自 Anthropic 团队，把工具暴露给模型的方式标准化了；它是一个协议，叫 model context protocol，它定义了一种呈现这些工具的标准方式</b>」。<br>⚠ 「<b>重复不是你想要的</b>」这句话其实说清了<b>所有协议的存在理由</b>:<b>协议不增加任何能力，它只是把 N×M 的适配工作变成 N+M</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("90:07","prompts are templates that could show the user how to use these tools",166);
  note("⭐ MCP 的四个词 + 一条连接",640,196,"y");
  boxNode(60,226,250,46,"MCP server","v");
  boxNode(330,226,250,46,"tools","g");
  boxNode(600,226,250,46,"prompts","y");
  boxNode(870,226,250,46,"resources","b");
  note("提供工具的那个实例  ｜  函数的实现  ｜  用法模板  ｜  可用的外部数据库",640,296,"d");
  boxNode(340,322,600,44,"MCP server ⟷ MCP client（在你的 LLM host 里，一对一）","v");
  note("⚠ 这些是基础设施细节，记住四个名词和它们各自指什么就够",640,382,"r");''',
         "<b>MCP 的词汇表，四个名词加一条连接。</b><br>⭐ <b>MCP server 是「提供工具的那个实例」;tools 是「你想让别人用的那些函数的实现」;prompts 是「能向用户展示怎么用这些工具的模板」;resources 是「你可以用来完成任务的外部数据库」</b>;而「<b>一个 MCP server 被使用时，和你的 LLM host 里一个叫 MCP client 的基础设施部件有一对一的连接</b>」。<br>⚠ 讲者自己说「<b>这些也许是基础设施细节</b>」—— <b>所以不用深记机制，记住四个名词各指什么就够；考试或面试里被问到 MCP，答「它是一个把工具暴露给模型的标准协议，核心概念是 server / tools / prompts / resources」就够了</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("90:43","we know our teddy bear loves to read poetry",166);
  says("91:15","they are the most experts as at serving such content",192);
  note("⭐ 用一个具体例子把四个名词坐实",640,222,"y");
  boxNode(60,254,250,46,"LLM host","v");
  boxNode(330,254,280,46,"MCP server","g");
  boxNode(630,254,250,46,"tools","y");
  boxNode(900,254,290,46,"resources","b");
  note("比如 Claude  ｜  由书商实现  ｜  找书 / 推荐书  ｜  熊的私人藏书、畅销榜",640,324,"d");
  note("⚠ 为什么由书商来实现：「他们典型地是提供这类内容最在行的」",640,374,"r");''',
         "<b>他用「给泰迪熊推荐一本诗集」把这四个词坐实了。</b><br>⭐ <b>LLM host 是 Claude（因为 MCP 出自 Anthropic）;MCP server「大概由你的图书供应商来实现」;tools 是「找书、推荐书」这类；prompts 是「怎么找一个给定书名、或者按某种口味推荐」的模板；resources 的例子是「泰迪熊的私人藏书」或者「大家买得最多的书」</b>。<br>⚠ 请注意「<b>为什么由书商实现</b>」那个理由：「<b>因为他们典型地是提供这类内容最在行的</b>」—— <b>这正是 MCP 这类协议的意义：让最懂数据的那一方去实现接口，而不是让每个模型厂商各自去猜</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("92:16","I am going to give first a definition",166);
  says("92:25","it is a system that autonomously pursues goal and completes tasks on a user's behalf",192);
  note("⭐ 到 agent 了 —— 讲者说这是「今天最令人兴奋的部分」",640,222,"y");
  setBig("agent 的定义","一个自主地追求目标、代表用户完成任务的系统");
  note("「agent 可以看成在工具之上再加一层」",640,342,"y");
  note("⚠ 而加的那一层是什么，下一镜说 —— 它只有两个字",640,382,"r");''',
         "<b>到 agent 了，而讲者说这是「今天这一讲里可能最令人兴奋的部分」。</b><br>⭐ 他照例<b>先给定义，好让大家对同一件事说话</b>：「<b>它是一个自主地追求目标、并代表用户完成任务的系统</b>」。<br>⭐ 而他给的定位是：「<b>我们看到了 LLM 有了工具会强大多少 —— 而 agent 可以被看作是在它之上再加一层</b>」。<br>⚠ 请注意他在这一讲里<b>第二次</b>用了同一个做法：<b>讲 tool calling 时他去找了 IBM 的定义，讲 agent 时他先立一个定义 —— 「先说清这个词在这里指什么，再往下讲」,对这种人人都在用的热词，这是必要的</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("92:55","it has that recurrence or higher level of reasoning baked into it",166);
  note("⭐ agent 和工具的差别，只有两个字：循环",640,196,"y");
  boxNode(80,228,500,50,"工具","d");
  boxNode(700,228,500,50,"agent","g");
  note("你能执行任务",330,302,"d");
  note("执行任务 ＋ 里面还有推理",950,302,"g");
  note("⭐ 「你可以有多轮迭代」—— 这就是把两者分开的那件事",640,348,"y");
  note("⚠ 而它和前面讲的东西「不一定是不相交的」—— 里面照样可以有推理链",640,386,"r");''',
         "<b>agent 和工具到底差在哪？讲者用大白话说了：差在循环。</b><br>⭐ 「<b>和工具相比，你不只是能执行任务，里面还牵涉到一些推理 ⇒ 你可以有多轮的迭代。而用大白话说，这就是把一个 agent 和一个工具区分开的东西 —— 人们谈 agent 时，它里面都烘焙着那种「递归」或者更高层的推理</b>」。<br>⚠ 而他特意说这个新框架「<b>不一定和我们之前讲的那些不相交 —— 你完全可以在里面有推理链，所以它是可能重叠的；但那个结构由工具调用和迭代组成</b>」。<br>⇒ <b>所以一句话记住：agent = 工具 + 循环 + 一个「还没达成目标就继续」的判断</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("93:43","a hallmark paper called ReAct, to reason plus acts",166);
  says("94:21","it is about decomposing complex tasks into loops of things that can be done atomically",192);
  note("⭐ 那篇标志性论文：ReAct = reason + act",640,222,"y");
  boxNode(80,254,500,50,"为什么需要它","y");
  boxNode(700,254,500,50,"它做的事","g");
  note("复杂目标往往一步做不完",330,328,"y");
  note("拆成一个个能原子地完成的小步，循环地做",950,328,"g");
  note("⚠ 三个阶段叫 observe / plan / act —— 但「名字和顺序不一定非得那样」",640,374,"r");''',
         "<b>最后是那篇标志性论文：ReAct。</b><br>⭐ 名字就是定义：<b>reason + act</b>。而需要它的理由很朴素：「<b>很多时候你有一个查询、想达成一个目标，你没法一步做到 —— 你得把目标分解成可执行的子步骤，逐个执行，然后得出答案；而这正是 ReAct 的全部：把复杂任务分解成一个个能原子完成的事情的循环</b>」。<br>⚠ 讲者在这里加了一个很重要的提醒：「<b>我们把这些步骤分成 observe、plan、act —— 但它不一定非得叫这个名字、也不一定非得是这个顺序；比如 ReAct 原论文引入的我想是 think、observe、act ⇒ 你会看到说法从一篇论文到另一篇在变，但高层直觉不变</b>」。", 0)],
       {"h": "⭐ tool selection · MCP · agent",
        "k": "tool selection（引 Google DeepMind 的一篇技术论文）:<b>「首先你有你的查询，和一份想多大就多大的工具清单 —— 而清单只含 API 名字、也许一两个词说它是干什么的 ⇒ 我们让 LLM 挑出可能相关的那些」; 「第二阶段，你把选中的工具 API 连同查询一起，只把这些喂进上下文」; 「目标是把工具数量限制到只剩那些可能有用的」,而「tool selection 和 routing 是相近的概念」</b>；一个提问：<b>「那基本上就是 RAG？」——「你可以用 RAG 做，这是个很好的点，但它不一定非得是；你也可以让一个 LLM 来干这活」</b>。<br>MCP：<b>「指定一个工具实现的方式可能是为某个 LLM 量身定做的⋯⋯而重复不是你想要的 ⇒ 这就是为什么有一个叫 MCP 的标准，它来自 Anthropic 团队，把工具暴露给模型的方式标准化了」; 词汇是 MCP server（「提供工具的那个实例」）· tools（「函数的实现」）· prompts（「能向用户展示怎么用这些工具的模板」）· resources（「你可以用来完成任务的外部数据库」）,而 server 和 LLM host 里的 MCP client 有一对一连接；例子是给爱读诗的泰迪熊推荐书，MCP server「大概由你的图书供应商实现，因为他们典型地是提供这类内容最在行的」</b>。<br>agent：<b>「它是一个自主地追求目标、并代表用户完成任务的系统」; 「和工具相比，你不只是能执行任务，里面还牵涉到一些推理 ⇒ 你可以有多轮的迭代 —— 这就是把 agent 和工具区分开的东西」; 而 ReAct「reason 加 act」「是把复杂任务分解成一个个能原子完成的事情的循环」,三阶段「observe、plan、act，但不一定非得叫这个名字或是这个顺序」</b>。",
        "m": "⭐ <b>tool selection 就是那条线的第二次出现</b>,逐项对得上：<b>「只有名字和一句话」＝ 便宜判据；「挑出可能相关的」＝ 最大化 recall；「只把这几个的完整定义放进去」＝ 候选少了才负担得起昂贵判据</b> ⇒ 而那位学生问「这不就是 RAG 吗」,<b>看到的正是这个同构：从一大堆候选里挑相关的少数 —— 候选是文档就叫 RAG，是工具就叫 tool selection</b>。<br>⭐ 「<b>重复不是你想要的</b>」说清了所有协议的存在理由：<b>协议不增加任何能力，它只是把 N×M 的适配工作变成 N+M</b>。<br>⭐ 而 <b>agent = 工具 + 循环</b>:<b>多出来的是「还没达成目标就继续」的那个判断 —— 而它和前面讲的东西「不一定不相交」,里面照样可以有推理链</b>。",
        "w": " MCP 那四个名词<b>不用深记机制</b>:<b>讲者自己说「这些也许是基础设施细节」—— 被问到时答「它是一个把工具暴露给模型的标准协议，核心概念是 server / tools / prompts / resources」就够</b>。<br>⚠ 而 ReAct 的三阶段名字<b>不要死记</b>:<b>「observe / plan / act」只是这一讲的叫法，原论文是「think / observe / act」—— 说法会变，高层直觉不变</b>。<br>⚠ 「为什么 MCP server 由书商实现」那个理由值得记：<b>让最懂数据的那一方去实现接口，而不是让每个模型厂商各自去猜</b>。",
        "r": "⇒ 讲者<b>第二次</b>用「先立一个定义再往下讲」这个做法（第一次是 tool calling 引 IBM）⇒ <b>对人人都在用、定义模糊的热词，这是必要的</b>。<br>⇒ 而「<b>可扩展</b>」这条线请收一次：<b>工具太多的三个性能问题由 tool selection 解决，第四个（没有标准）由 MCP 解决 —— 四个缺点到这里全部有了着落</b>。<br>⇒ 更多（DeepMind 那篇 tool selector、MCP 的完整规范、ReAct 原论文）见<b>深度笔记</b>。",
        },
       {"t": "tool selection 和上半场的 RAG 检索是什么关系？而 agent 和工具差在哪？",
        "o": ["毫无关系；agent 就是更大的工具",
              "是同一个结构的第二次出现：先用便宜判据（只看名字和一句话描述）挑出可能相关的少数，再把这几个的完整定义放进上下文 —— 所以学生问「这不就是 RAG 吗」是对的；而 agent 比工具多的是「循环」：多轮迭代加上「还没达成目标就继续」的判断",
              "tool selection 必须用 RAG 实现；agent 差在用了 MCP",
              "两者都靠 SFT；agent 差在模型更大"],
        "a": 1,
        "w": "⇒ 而工具太多的四个缺点到这里全部有了着落：三个性能问题由 tool selection 解决，第四个（没有标准）由 MCP 解决。"})
