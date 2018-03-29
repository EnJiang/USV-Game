# USV-Game
一个简单的无人艇包围游戏

## 依赖
1. Python3.
2. pygame. 作为游戏引擎

## 对接说明
我们参考仿照maddpg来实现，但是不直接用它们的代码，因为他们的代码太不flexible了，不如重写。
### 首先说明几组类名词概念：
1. Environment <br>
Opengym AI中的概念，定义了一组agent活动的环境。这个类主要是为了向上兼容gym，它内部的功能基本上都是由再套接一个World类实现的。主要函数和成员有：
+ env = Env(self, world)：初始化一个环境
+ obs_n, reward_n, done_n, info_n = env.step(action_n)：接受n个agent的action，返回每一个agent的observation(就是接下来的可行动作空间)、reward、是否结束以及其他信息
+ action_n = env.decide()： 返回当前n个agent的action
+ obs_n = env.observe()：返回当前n个agent的observation
+  env.reset()：重置整个世界 <br>
+ env.memory：记录了整个游戏的奖励等
这一部分由算法组完成。

2.Policy <br>
**agent个体**而不是**群体**的执行决策的类，应该是个神经网络，主要方法有
+ p = Policy(world)
+ action = p.action(obs)：接收一个可行的动作空间observation，返回一个合法的action
+ p.learn(memory)：通过一局记忆去学习
+ p.save(filename|file obj)：保存策略 <br>
这一部分由算法组完成 <br>

3. World <br>
对整个无人艇世界的包装，可以包装一个已经实现的无人艇游戏来实现。实际上这个东西就是一个Environment，这个类是模拟组和算法组的接口。另外，这个类其实是整合了maddpg中的Scenario和World对象，因为我觉得它设计两个类是多余的。注意，这里写的是基类，会有派生，比如说一次走一步的就可以有个OneStepWorld，离散的可以有PlaneWorld等等……主要函数和成员对象有：
+ w = World(Policy)：接受一定参数，新建一个世界。这里要注意保持接口弹性，后期可能指定agent的个数、类型，障碍物的类型、个数，目标点，等等等等……
+ w.policy_agents：一个list，里面装了所有agent
+ w.policy：一个policy对象
+ obs_n, reward_n, done_n, info_n = w.step(action_n)：接受n个agent的action，返回每一个agent的observation(就是接下来的可行动作空间)、reward、是否结束以及其他信息
+ action_n = w.decide()： 返回当前n个agent的action
+ obs_n = w.observe()：返回当前n个agent的observation
+  w.reset()：重置整个世界 <br>

### 系统构架
从系统功能上来说，首先新建一个策略对象和一个世界对象，假设是单步的：w = OneStepWorld(Policy), 这时构造函数利用传进来的Policy类（注意传进来的不是一个Policy对象的实例）生成一个policy对象，基本上就是self.policy = Policy(self) <br>
这时候world里面已经有了一个policy对象和一个agent的list **当前的版本中，这个list的长度总为1（只有一个agent）** <br>
新建一个世界env = Env(w) <br>
开始主循环： <br>
1. obs_n = env.observe() <br>
1.1 内部发生了return w.observe()
2. action_n = env.decide() <br>
2.2 内部发生了 w.decide() <br>
2.3 在w.decide()中，反复调用action = p.action(obs_n[i], f[i])来生成动作, 这里，f[i]是为了指明以后我们可能会使用多agent，那么policy对象需要知道是在为哪个对象做决定，暂时可以是None <br>
2.4 return w.decide()
3. obs_n, reward_n, done_n, info_n = env.step(action_n) <br>
3.1 内部发生了return w.step(action_n)
4. 如果sum(done_n) == 0(agent全为结束状态), 去6
5. 否则，回到2
6. 这时候游戏已经结束，env的memory中记忆了一系列的obs和reward, 调用w.p.learn(memory)来学习
7. 如果优化达到最优，整个训练结束，w.p.save()
8. 否则，env.reset(),回到1<br>
<br>

从代码实现上来说，Policy和Environment为算法，在上层，再往上的实现和模拟组无关；World为模拟，在下层，再下层的实现和算法组无关

### TODO List
- [ ] Environment的实现
- [ ] Policy的实现
- [ ] OneStepWorld的实现
- [ ] 第一次整系统对接
-----------------------------------
- [ ] PlaneWorld的实现
- [ ] 第二次整系统对接
-----------------------------------
- [ ] 让障碍物动起来
- [ ] 第三次整系统对接
- [ ] 第一篇论文的实验整理和论文书写
-----------------------------------
- [ ] **讨论改成多agent**
