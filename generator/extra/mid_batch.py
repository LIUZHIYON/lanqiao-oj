"""中等编程题一批 15 道（p48 ~ p62），蓝桥杯省赛风格，覆盖核心算法套路。

约定见 _TEMPLATE.py：
  · 参考解在 generator/reference/pNN_xxx.py，读 stdin、print 答案
  · 这里只手写输入数据，expected 全部由 build_problems 跑参考解得到
  · 每题 7~8 个测试点，第 1 条是可见样例，其余隐藏
  · 随机数据一律用固定种子的 random.Random，换机器也能复现同一份题库
"""
import random

SEED_MID = 20261048
ALPHA = "0123456789abcdefghijklmnopqrstuvwxyz"

PROG_META = [
    dict(pid="p48_reduced_fraction_count", title="既约分数计数", difficulty="提高",
         tags=["数论", "欧拉函数", "容斥"], chapter="第 9 章 19 / 第 5 章 14",
         source="蓝桥杯省赛真题（题意整理）",
         reference="code/ch09-number-theory/19_real_reduced_fraction.py",
         input_format="一行一个整数 n（1 ≤ n ≤ 2022）。",
         output_format="一行一个整数，是互质有序对的个数。",
         statement="<p>分子、分母都从 <code>1</code> 到 <code>n</code> 里取，"
                   "一个分子配一个分母算一个<strong>有序对</strong>："
                   "<code>(2,3)</code> 和 <code>(3,2)</code> 是两个不同的对。</p>"
                   "<p>问这些对里有多少个互质，也就是最大公约数等于 1 —— "
                   "这样的分数已经不能再约分，叫既约分数。</p>"
                   "<p>n = 3 时一共 9 个对，只有 <code>(2,2)</code> 和 <code>(3,3)</code> "
                   "不互质，答案是 7。</p>"
                   "<p>填空版真题问的是 <code>n = 2022</code>（答案 2486423），"
                   "这里改成编程题：读入哪个 n 就算哪个 n。</p>"
                   "<p>别指望双重循环逐对求最大公约数：n = 2000 时是四百万次 gcd，"
                   "本机实测两秒多，正好压过超时线；按层数一次数完才是稳的。</p>",
         idea="<p>按 <code>max(a, b) = k</code> 分层：另一个坐标取 1 到 k，"
              "和 k 互质的恰好有 <code>phi(k)</code> 个，而 <code>(k, j)</code> 与 "
              "<code>(j, k)</code> 是两个方向，所以第 k 层贡献 <code>2 * phi(k)</code>；"
              "只有 <code>(1,1)</code> 被数了两遍，最后减 1。</p>"
              "<p>答案 = <code>2 * (phi(1) + ... + phi(n)) - 1</code>，"
              "用欧拉函数筛一次算完，复杂度接近 O(n)。</p>"
              "<p>另一条独立的路是莫比乌斯容斥：互质的对数 = "
              "<code>Σ mu(d) * (n // d) * (n // d)</code>。两个筛法必须给同一个数，"
              "n 不超过 200 时再拿 gcd 双循环验一遍。</p>"),

    dict(pid="p49_snake_fill_value", title="蛇形填数", difficulty="提高",
         tags=["模拟", "找规律", "等差求和"], chapter="第 13 章 03",
         source="蓝桥杯省赛真题（题意整理）",
         reference="code/ch13-real-problems/03_snake_grid.py",
         input_format="一行两个整数 row 和 col，行号列号都从 1 开始（1 ≤ row, col ≤ 10^9）。",
         output_format="一行一个整数，是那一格里填的数。",
         statement="<p>把 <code>1, 2, 3, ...</code> 依次填进一张无限大的方格表："
                   "行号加列号相同的格子属于同一条反对角线，斜线按 "
                   "<code>2, 3, 4, ...</code> 的顺序处理，同一条斜线上从最上面那行开始往下填。</p>"
                   "<p>左上角长这样（第 1 行第 1 列填 1）：</p>"
                   "<pre>行1:   1   2   4   7  11\n"
                   "行2:   3   5   8  12\n"
                   "行3:   6   9  13\n"
                   "行4:  10  14\n"
                   "行5:  15</pre>"
                   "<p>给你行号和列号，输出那一格的数。</p>"
                   "<p>真题只问第 20 行第 20 列，这里把行列放开到 10^9，"
                   "一格一格模拟填数就不够用了，得把公式推出来。</p>",
         idea="<p>设 <code>s = row + col</code>。比 s 小的斜线有 <code>s - 2</code> 条，"
              "第 t 条斜线有 t - 1 个格子，所以前面一共填了 "
              "<code>1 + 2 + ... + (s-2) = (s-2)(s-1)/2</code> 个数；"
              "本条斜线上这一格排在第 <code>row</code> 个，两者相加就是答案。</p>"
              "<p>行列不太大时照着规则真填一遍网格核对，两种办法一致再交。"
              "Python 的整数没有溢出问题，10^9 量级的乘积直接算。</p>"),

    dict(pid="p50_daily_temperatures", title="每日温度", difficulty="提高",
         tags=["单调栈", "线性"], chapter="第 8 章 27",
         source="蓝桥杯风格算法练习",
         reference="code/ch08-sort-binary-greedy/27_daily_temperatures.py",
         input_format="第一行一个整数 n（1 ≤ n ≤ 100000）；第二行 n 个整数是每天的温度，"
                      "空格分隔（-30 到 45 之间）。",
         output_format="一行 n 个整数，空格分隔。第 i 个数是第 i 天要等几天才出现更高的温度，"
                       "往后都没有更高的就写 0。",
         statement="<p>连续 <code>n</code> 天的温度依次给出。对每一天问：往后看，"
                   "最早再过几天会出现一个<strong>严格更高</strong>的温度？</p>"
                   "<p>比如 <code>73 74 75 71</code>：第 1 天等 1 天到 74 度；"
                   "第 2 天等 1 天到 75 度；第 3 天以后没有更高的，写 0；"
                   "第 4 天是最后一天，也写 0，所以输出 <code>1 1 0 0</code>。</p>"
                   "<p>每天往后扫一遍是 O(n^2)，十万天直接跑不完。"
                   "这题的信号是「每个元素要找右边第一个比它大的」——单调栈的招牌用法。</p>",
         idea="<p>栈里存还没算出答案的那几天的<strong>下标</strong>，栈内温度从底到顶单调不升。"
              "新的一天进来时，只要它比栈顶那天高，栈顶就找到了答案："
              "<code>等待天数 = 今天下标 - 栈顶下标</code>，弹栈接着比，"
              "直到栈空或者栈顶不再比它低，然后把今天压栈。</p>"
              "<p>每个下标进出栈各一次，总共 O(n)。相等不算「更高」，"
              "比较要用严格小于。全程降温、全程升温、全部相同这三种数据各跑一遍，"
              "写法有没有错立刻看得出来。</p>"),

    dict(pid="p51_longest_no_repeat", title="最长无重复子串", difficulty="提高",
         tags=["滑动窗口", "字符串", "哈希"], chapter="第 11 章 35 / 第 8 章 24",
         source="蓝桥杯风格算法练习",
         reference="code/ch11-string/35_exam_no_repeat_substring.py",
         input_format="第一行一个整数 n（1 ≤ n ≤ 200000），是串的长度；"
                      "第二行一个长度为 n 的串，只由小写字母和数字组成，中间没有空格。",
         output_format="一行一个整数，是最长无重复字符连续片段的长度。",
         statement="<p>给一个串，找一段<strong>连续</strong>的片段，要求片段里没有任何字符重复出现，"
                   "问这样的片段最长有多长。</p>"
                   "<p>子串要求连续，子序列不要求连续，这两个概念别混。</p>"
                   "<p>比如 <code>abcabcbb</code>，最长的一段是 <code>abc</code>，长度 3；"
                   "<code>bbbbb</code> 每一格都是 b，答案只有 1；"
                   "整串都不重复时答案就是串长。</p>",
         idea="<p>滑动窗口：<code>right</code> 一路往右扩，用字典 <code>last</code> 记住每个字符"
              "最后出现的位置。若 <code>last[ch]</code> 落在当前窗口里，"
              "左边界直接跳到 <code>last[ch] + 1</code>——左边界只往右走，"
              "不需要一格一格退，也不用把窗口里的字符逐个删掉。</p>"
              "<p>每步用 <code>right - left + 1</code> 更新答案，总复杂度 O(n)。"
              "全相同、全不重复、串长 1 这三种边界数据最容易暴露错误。</p>"),

    dict(pid="p52_interval_merge", title="区间合并", difficulty="提高",
         tags=["排序", "贪心", "扫描线"], chapter="第 8 章 17",
         source="蓝桥杯风格算法练习",
         reference="code/ch08-sort-binary-greedy/17_merge_intervals.py",
         input_format="第一行一个整数 n（1 ≤ n ≤ 100000）；接下来 n 行每行两个整数 l 和 r，"
                      "表示闭区间 [l, r]（0 ≤ l ≤ r ≤ 10^9）。",
         output_format="一行两个整数，空格分隔：合并后剩下的区间个数、被覆盖的总长度。",
         statement="<p>数轴上给了 <code>n</code> 段闭区间，重叠或者端点相接的并成一段："
                   "<code>[1,3]</code> 和 <code>[2,6]</code> 并成 <code>[1,6]</code>，"
                   "<code>[1,3]</code> 和 <code>[3,5]</code> 也并成 <code>[1,5]</code>。</p>"
                   "<p>输出两样东西：合并后还剩几段、这些段盖住的总长度。"
                   "每段贡献 <code>r - l</code>，所以 <code>[7,7]</code> 这种单点区间"
                   "算一段、长度为 0。</p>"
                   "<p>比如 <code>[1,3] [2,6] [8,10] [9,11]</code>："
                   "前两段并成 <code>[1,6]</code>，后两段并成 <code>[8,11]</code>，"
                   "输出 <code>2 8</code>。</p>",
         idea="<p>按左端点排序，然后一遍扫：能并进来就把最后一段的右端点更新成 "
              "<code>max(原右端点, r)</code>（后一段可能被前一段整个包住），"
              "并不进来就新开一段。排序 O(n log n)，扫一遍 O(n)。</p>"
              "<p>核对：把每个区间的左右端点看成事件，按坐标排序后统计覆盖深度——"
              "同一坐标上先处理左端点再处理右端点，相接的两段才会被算成连在一起。"
              "两条路的段数和总长度必须一致，单点区间也要能对上。</p>"),

    dict(pid="p53_range_sum_query", title="区间和查询", difficulty="提高",
         tags=["前缀和", "输入输出"], chapter="第 5 章 07、24",
         source="蓝桥杯风格算法练习",
         reference="code/ch05-brute-force/07_prefix_sum_1d.py",
         input_format="第一行两个整数 n 和 q（1 ≤ n ≤ 40000，1 ≤ q ≤ 15000）；"
                      "第二行 n 个整数是数组（每个的绝对值不超过 10^9）；"
                      "接下来 q 行每行两个整数 l 和 r（1 ≤ l ≤ r ≤ n），下标从 1 开始。",
         output_format="输出 q 行，每行一个整数，是区间 [l, r] 的元素和。",
         statement="<p>数组给定后不再修改，但有很多次询问：每次问第 l 个到第 r 个加起来是多少。</p>"
                   "<p>逐次把区间里的数现加是 O(区间长)，q 次最坏 O(n × q)；"
                   "四万个数、一万五千次询问就完全跑不动了。</p>"
                   "<p>「数组不变、只问区间和」是前缀和的标准场景：预处理一次，"
                   "之后每次询问 O(1)。</p>"
                   "<p>数组里可能有负数，和也可以是负数。</p>",
         idea="<p><code>pre[i]</code> = 前 i 个数之和，<code>pre[0] = 0</code>，"
              "答案 = <code>pre[r] - pre[l-1]</code>。多留 <code>pre[0]</code> 这一格，"
              "l = 1 时不用特判。</p>"
              "<p>和能到 10^14 量级，Python 的整数不怕，但别在循环里反复切片段求和。"
              "一次询问的输出攒到最后一起打印，别让 print 调用一万多次。</p>"
              "<p>核对：询问少的时候把那段直接加起来比一遍，确认下标没有整体错开一格。</p>"),

    dict(pid="p54_diff_range_add", title="差分区间加", difficulty="提高",
         tags=["差分", "前缀和"], chapter="第 5 章 10、26",
         source="蓝桥杯风格算法练习",
         reference="code/ch05-brute-force/10_diff_array.py",
         input_format="第一行两个整数 n 和 q（1 ≤ n ≤ 20000，0 ≤ q ≤ 20000）；"
                      "第二行 n 个整数是初始数组（绝对值不超过 10^5）；"
                      "接下来 q 行每行三个整数 l、r、v（1 ≤ l ≤ r ≤ n，"
                      "v 的绝对值不超过 10^5），表示把第 l 到第 r 个都加上 v，下标从 1 开始。",
         output_format="一行 n 个整数，空格分隔，是全部操作做完之后的数组。",
         statement="<p>长度为 <code>n</code> 的数组，做 <code>q</code> 次操作，"
                   "每次把一段连续的格子整体加同一个数。所有操作做完，把整个数组输出。</p>"
                   "<p>一次一次去改每个格子是 O(n × q)，两边都给到两万就是四亿次，"
                   "完全跑不动。看到「只问最后结果、中途不查询」，就要想到差分。</p>"
                   "<p>差分和前缀和是一对互逆的操作：区间加变成两次单点改，"
                   "最后做一次前缀和还原。</p>",
         idea="<p>建差分数组 <code>d</code>：把 <code>[l, r]</code> 加 v 变成 "
              "<code>d[l] += v</code>、<code>d[r+1] -= v</code>，两次单点操作搞定一段。</p>"
              "<p>所有操作做完后从左往右累加 <code>d</code>，走到第 i 个位置累计到的就是"
              "它的总增量，加上原值即答案。数组多开一格放 <code>r+1</code> 的减记，"
              "越界判断就省掉了。</p>"
              "<p>核对：数组小的时候老老实实逐格改，两边结果必须完全一样。"
              "q = 0（一次操作都没有）也要原样输出初始数组。</p>"),

    dict(pid="p55_prefix_sum_2d", title="二维前缀和", difficulty="提高",
         tags=["前缀和", "二维", "容斥"], chapter="第 5 章 08",
         source="蓝桥杯风格算法练习",
         reference="code/ch05-brute-force/08_prefix_sum_2d.py",
         input_format="第一行两个整数 n 和 m（1 ≤ n, m ≤ 300）；接下来 n 行每行 m 个整数"
                      "（0 到 1000）；然后一行一个整数 q（1 ≤ q ≤ 10000）；"
                      "接下来 q 行每行四个整数 r1、c1、r2、c2"
                      "（1 ≤ r1 ≤ r2 ≤ n，1 ≤ c1 ≤ c2 ≤ m），行列都从 1 开始。",
         output_format="输出 q 行，每行一个整数，是子矩阵 [r1, c1] 到 [r2, c2] 的元素和。",
         statement="<p>一张 <code>n</code> 行 <code>m</code> 列的数字表，很多次询问："
                   "左上角在 <code>(r1, c1)</code>、右下角在 <code>(r2, c2)</code> "
                   "的这一小块里，所有数加起来是多少。</p>"
                   "<p>一块一块直接加是 O(块大小)，三万行三万列的数据量根本不够用；"
                   "「表格不变、反复问子矩阵和」就是二维前缀和的场景。</p>",
         idea="<p><code>ps[i][j] = ps[i-1][j] + ps[i][j-1] - ps[i-1][j-1] + a[i][j]</code>："
              "上面那块加左边这条，重叠的左上角被算了两次要减回来。</p>"
              "<p>询问 = <code>ps[r2][c2] - ps[r1-1][c2] - ps[r2][c1-1] + ps[r1-1][c1-1]</code>，"
              "减掉上面那条和左边那条，多减的左上角再加回来。</p>"
              "<p>多开第 0 行第 0 列全填 0，边界就不用写判断。"
              "整张表的和、单行、单列、1 × 1 这四个特例各验一遍，"
              "容斥符号写错立刻能看出来。小数据时再把那块直接加一遍核对。</p>"),

    dict(pid="p56_friend_circles", title="朋友圈", difficulty="提高",
         tags=["并查集", "连通块", "图论"], chapter="第 10 章 05、06",
         source="蓝桥杯风格算法练习",
         reference="code/ch10-graph/06_dsu_provinces.py",
         input_format="第一行两个整数 n 和 m（1 ≤ n ≤ 50000，0 ≤ m ≤ 100000）；"
                      "接下来 m 行每行两个整数 a 和 b（1 ≤ a, b ≤ n），表示 a 和 b 认识。"
                      "同一条关系可能出现多次，也可能 a 等于 b。",
         output_format="一行两个整数，空格分隔：朋友圈的个数、最大朋友圈里的人数。",
         statement="<p>「认识」是相互的，而且能传递：a 认识 b、b 认识 c，"
                   "那么 a、b、c 就在同一个朋友圈里，哪怕 a 和 c 没直接打过招呼。</p>"
                   "<p>把每人和他所有能间接连上的人归成一个朋友圈，这些圈互不相交。"
                   "问一共有几个圈、最大的圈里有几个人。</p>"
                   "<p>谁都不认识任何人时，n 个人就是 n 个圈，最大的圈 1 人。</p>",
         idea="<p>并查集：把每条关系的两端合并，最后数有多少个根、每个根上挂了多少人"
              "（size 只维护在根上，别在中间节点上取）。</p>"
              "<p><code>find</code> 用循环加路径减半，别写成深层递归——几十万人的长链会把"
              "递归深度顶爆；合并时把小的集合挂到大的下面，树才不会退化成链。</p>"
              "<p>重边和 <code>a = b</code> 的自环在合并前先判掉（同一个根就跳过）。"
              "核对：把关系建成邻接表做一遍广度优先数块，两条路必须一致；"
              "大图跑不动 BFS，就只在几千人的时候验。</p>"),

    dict(pid="p57_dijkstra_shortest", title="单源最短路", difficulty="较难",
         tags=["图论", "最短路", "堆"], chapter="第 10 章 09、10",
         source="蓝桥杯风格算法练习",
         reference="code/ch10-graph/10_dijkstra_heap.py",
         input_format="第一行三个整数 n、m、s（1 ≤ n ≤ 20000，1 ≤ m ≤ 45000，1 ≤ s ≤ n）；"
                      "接下来 m 行每行三个整数 u、v、w，表示一条从 u 到 v 的有向边，"
                      "长度 w（0 ≤ w ≤ 10^4）。两个点之间可能有多条边。",
         output_format="输出 n 行：第 i 行是 s 到第 i 个点的最短距离，走不到输出 -1。",
         statement="<p>有 <code>n</code> 个路口、<code>m</code> 条<strong>单向</strong>道路，"
                   "每条路有长度。从起点 <code>s</code> 出发，按编号 1 到 n 依次输出"
                   "到每个路口的最短距离；到不了的路口输出 <code>-1</code>。</p>"
                   "<p>起点到自己的距离是 0。</p>"
                   "<p>边权都是非负数，所以能上 Dijkstra；一旦会出现负权边，"
                   "这套办法就不成立，要换 Bellman-Ford。</p>"
                   "<p>每轮线性扫最小值的朴素写法是 O(n^2)，两万个点就很吃力，"
                   "点边都多的图要用小根堆优化。</p>",
         idea="<p><code>dist</code> 初始化成一个大数（比如 10^30），起点置 0，"
              "堆里放 <code>(距离, 点)</code>。每次弹出最小的那个："
              "若它比 <code>dist[u]</code> 大，说明是早先留下的过期记录，直接跳过；"
              "否则松弛它的所有出边，谁被改小了就把谁再压进堆。</p>"
              "<p>复杂度 O(m log m)。忘了跳过旧记录，堆里会塞满垃圾；"
              "松弛写成「等于也压栈」同样会多跑很多倍。</p>"
              "<p>核对：三百个点以内用每轮线性找最小值的朴素 Dijkstra 比一遍；"
              "再造一个「某个点没有任何入边」的小图，确认它输出 -1 而不是那个大数。</p>"),

    dict(pid="p58_jump_stones", title="跳石头", difficulty="较难",
         tags=["二分答案", "贪心判定"], chapter="第 8 章 12、30",
         source="蓝桥杯风格算法练习（经典二分答案）",
         reference="code/ch08-sort-binary-greedy/12_bisect_answer_stones.py",
         input_format="第一行三个整数 L、n、m（1 ≤ L ≤ 10^9，0 ≤ n ≤ 50000，0 ≤ m ≤ n）；"
                      "第二行 n 个整数是每块岩石到起点的距离，互不相同且都在 0 到 L 之间"
                      "（n = 0 时没有第二行）。",
         output_format="一行一个整数，是搬走不超过 m 块岩石之后，最短跳跃距离最大能到多少。",
         statement="<p>一条河宽 <code>L</code>，起点在 0，终点在对岸。河里有 <code>n</code> 块岩石，"
                   "位置由它们到起点的距离给出。选手从起点起跳，只能踩岩石和终点，"
                   "最后必须落在终点。</p>"
                   "<p>赛前最多可以搬走 <code>m</code> 块岩石，希望让"
                   "「全程最短的那一跳」尽可能长，问这个最短跳跃距离最大是多少。</p>"
                   "<p>比如河宽 25、岩石在 2、11、14、17、21，最多搬 2 块："
                   "搬走 2 和 14，剩下 11、17、21，四段距离是 11、6、4、4，"
                   "最短的一跳是 4，这时已经不能再更好，答案是 4。</p>"
                   "<p>直接枚举搬哪几块是指数级的，做不动。</p>",
         idea="<p>「让最小值尽量大」是二分答案的信号。猜一个最短距离 <code>x</code> 能不能做到："
              "从左往右扫，和上一个落脚点的间距小于 x 就把这块岩石搬掉（搬走的块数累加），"
              "否则把落脚点挪到这块岩石上。搬的块数不超过 m 就说明 x 可行。</p>"
              "<p>x 越大越难满足，可行性随 x 单调，二分即可。模板用 "
              "<code>mid = (lo + hi + 1) // 2</code> 配 <code>lo = mid</code>，"
              "少写那个 +1 就会原地打转。</p>"
              "<p>核对：岩石不超过 12 块时枚举所有搬法（2^n）取最优和二分的结论比一遍。"
              "搬光所有岩石时答案是 L；m = 0 时答案就是原始的最小间距；"
              "没有岩石时答案也是 L。</p>"),

    dict(pid="p59_subset_sum_count", title="凑数方案数", difficulty="提高",
         tags=["动态规划", "背包", "计数"], chapter="第 7 章 27 / 第 6 章 21",
         source="蓝桥杯风格算法练习",
         reference="code/ch07-dp/27_practice_subset_sum.py",
         input_format="第一行两个整数 n 和 s（1 ≤ n ≤ 100，0 ≤ s ≤ 5000）；"
                      "第二行 n 个整数（1 到 5000），每个数最多只能用一次。",
         output_format="一行一个整数，是总和刚好等于 s 的取法种数，答案可能很大。",
         statement="<p>桌上有 <code>n</code> 个数，每个数要么拿走要么留下（最多用一次）。"
                   "问有多少种取法，能让拿走的数加起来正好等于目标值 <code>s</code>。</p>"
                   "<p>取法只看拿了哪几个位置，不看顺序：哪怕两个数长得一样，"
                   "选前面那个和选后面那个也是两种不同的取法。</p>"
                   "<p>一个都不拿也是一种取法，它的和是 0，所以 <code>s = 0</code> 时答案是 1。</p>"
                   "<p>怎么凑都凑不出来时输出 0。</p>",
         idea="<p>背包数方案：<code>dp[j]</code> = 和为 j 的取法数，<code>dp[0] = 1</code>。"
              "枚举每个数时内层的 j 要从大到小走（<code>for j in range(s, a - 1, -1)</code>），"
              "这样这个数只会被用一次；从小到大就走歪成「可以重复取」的完全背包了。</p>"
              "<p>求最大值的 0-1 背包和数方案的 0-1 背包是同一个套路，"
              "只是把 max 换成加法。</p>"
              "<p>核对：中等规模换一种写法——只维护「出现过的和」的字典，两边要一样；"
              "n 不超过 14 时直接枚举全部子集验一遍。方案数会比 64 位整数还大，"
              "Python 直接算就行。</p>"),

    dict(pid="p60_coin_change_min", title="零钱兑换", difficulty="提高",
         tags=["动态规划", "完全背包", "BFS"], chapter="第 7 章 12、26",
         source="蓝桥杯风格算法练习",
         reference="code/ch07-dp/12_coin_change.py",
         input_format="第一行两个整数 k 和 s（1 ≤ k ≤ 50，0 ≤ s ≤ 20000）；"
                      "第二行 k 个整数是硬币面额（1 到 20000，可能有重复，"
                      "同一种面额想用几枚都行）。",
         output_format="一行一个整数，是最少需要的硬币枚数；怎么都凑不出 s 时输出 -1。",
         statement="<p>有 <code>k</code> 种面额的硬币，每种数量无限，要凑出金额 <code>s</code>，"
                   "问最少用几枚。</p>"
                   "<p>金额 0 不需要任何硬币，答案是 0。</p>"
                   "<p>先想清楚能不能贪心（每次拿最大面额）：<code>1 3 4</code> 凑 6，"
                   "贪心拿 4 再拿 1、1，用 3 枚；而 3 + 3 只要 2 枚。"
                   "面额之间没有整除关系时贪心是错的，得上动态规划。</p>"
                   "<p>凑不出来输出 -1，比如只有 2 和 4 却要凑 3。</p>",
         idea="<p><code>dp[j]</code> = 凑出金额 j 的最少枚数，<code>dp[0] = 0</code>，"
              "其余先记成一个比 s 还大的「不可能」值。外层枚举面额，"
              "内层金额从小到大走，这样同一面额能被反复取用（完全背包）。</p>"
              "<p>最后 <code>dp[s]</code> 还超过 s 就说明凑不出，输出 -1。</p>"
              "<p>核对：金额不超过两千时改用广度优先——把 0 看作起点，"
              "每加一枚硬币算走一步，第一次走到 s 的层数就是最少枚数，"
              "两种做法必须给同一个数。</p>"),

    dict(pid="p61_lcs_length", title="最长公共子序列", difficulty="提高",
         tags=["动态规划", "字符串", "二维"], chapter="第 7 章 21、28",
         source="蓝桥杯风格算法练习",
         reference="code/ch07-dp/21_lcs.py",
         input_format="第一行两个整数 n 和 m（1 ≤ n, m ≤ 1200），是两个串的长度；"
                      "第二行串 A（长度 n），第三行串 B（长度 m），都只由小写字母组成。",
         output_format="一行一个整数，是 A 和 B 的公共子序列的最大长度。",
         statement="<p>子序列是把串中若干个字符按原来的先后顺序挑出来得到的串，允许不连续："
                   "<code>ace</code> 是 <code>abcde</code> 的子序列，<code>ca</code> 不是。</p>"
                   "<p>给两个串，问它们公共的子序列最长有多长。</p>"
                   "<p>比如 <code>abcbdab</code> 和 <code>bdcaba</code>，"
                   "公共子序列有 <code>bcba</code>、<code>bdab</code>，最长是 4。</p>"
                   "<p>两个串一个公共字符都没有时答案是 0。</p>",
         idea="<p>二维 DP：<code>dp[i][j]</code> = A 的前 i 个字符与 B 的前 j 个字符的 "
              "LCS 长度。末尾字符相同，它一定能接在两边的 LCS 后面："
              "<code>dp[i][j] = dp[i-1][j-1] + 1</code>；"
              "不同时，丢掉 A 的最后一个或丢掉 B 的最后一个，取较大的："
              "<code>max(dp[i-1][j], dp[i][j-1])</code>。</p>"
              "<p>每行只依赖上一行，滚动两行就够，省内存也更快。"
              "n × m 的一百四十万次循环是这题的耗时大头，别在里面做多余的事。</p>"
              "<p>核对：交换 A、B 结果必须不变；串很短时枚举它的全部子序列，"
              "逐个判断是不是另一个串的子序列，小规模时和 DP 比一遍。</p>"),

    dict(pid="p62_comb_mod_query", title="组合数取模", difficulty="较难",
         tags=["数论", "组合数学", "逆元"], chapter="第 9 章 11 / 第 12 章 01",
         source="蓝桥杯风格算法练习",
         reference="code/ch09-number-theory/11_mod_arithmetic.py",
         input_format="第一行一个整数 T（1 ≤ T ≤ 200），是询问组数；"
                      "接下来 T 行每行两个整数 n 和 k（0 ≤ n ≤ 100000，0 ≤ k ≤ 100000）。",
         output_format="输出 T 行，每行一个整数，是 C(n, k) 除以 1000000007 的余数；"
                       "k 大于 n 时输出 0。",
         statement="<p>从 n 个不同的东西里挑 k 个，方案数记作 <code>C(n, k)</code>。"
                   "n 上万时组合数大得写不下，所以题目约定：输出它对 "
                   "<code>1000000007</code>（一个质数）取余的结果。</p>"
                   "<p>给 T 组 n、k 依次询问，一组输出一行。</p>"
                   "<p><code>k = 0</code> 时答案是 1（什么都不挑算一种），"
                   "<code>k = n</code> 时也是 1，<code>k</code> 比 <code>n</code> 大时"
                   "根本挑不出来，输出 0。</p>",
         idea="<p>预处理阶乘 <code>fact[i] = i! mod p</code> 与阶乘逆元 "
              "<code>invfact[i]</code>：只对最大的那个 <code>fact[maxN]</code> 用一次"
              "费马小定理求幂 <code>pow(fact[maxN], p-2, p)</code>，"
              "再往前用 <code>invfact[i-1] = invfact[i] * i mod p</code> 倒推。"
              "询问就是 <code>fact[n] * invfact[k] * invfact[n-k] % p</code>，O(1)。</p>"
              "<p>取模之后不能真的做除法：「除以一个数」要换成「乘它的逆元」，"
              "这是所有取模计数题的通用规矩。</p>"
              "<p>核对：k 很小时用连乘、每一步带逆元的写法再算一次；"
              "n 不超过一千时直接拿 <code>math.comb</code> 算精确值再取余，"
              "三条路都得给同一个数。</p>"),
]


def prog_cases():
    cs = {}

    # ---------------------------------------------------------- p48 既约分数计数
    r48 = random.Random(SEED_MID + 1)
    cs["p48_reduced_fraction_count"] = [
        ("样例 n=9", "9\n"),
        ("最小 n=1 只剩 (1,1)", "1\n"),
        ("n=2 只有一对可约", "2\n"),
        ("n=3 两对可约", "3\n"),
        ("随机小 n=60 以内", "{}\n".format(r48.randint(40, 90))),
        ("n=1379", "1379\n"),
        ("n=2000 大规模", "2000\n"),
        ("n=2022 填空题那一档", "2022\n"),
    ]

    # ---------------------------------------------------------- p49 蛇形填数
    cs["p49_snake_fill_value"] = [
        ("样例 第 3 行第 2 列", "3 2\n"),
        ("左上角 1 1", "1 1\n"),
        ("第一行第 5 列", "1 5\n"),
        ("第一列第 5 行", "5 1\n"),
        ("真题 20 行 20 列", "20 20\n"),
        ("同一条斜线的两端 1 40", "1 40\n"),
        ("随机中等 123 200", "123 200\n"),
        ("最大 10^9 量级", "1000000000 999999999\n"),
    ]

    # ---------------------------------------------------------- p50 每日温度
    r50 = random.Random(SEED_MID + 2)
    t50_small = [r50.randint(-30, 45) for _ in range(18)]
    t50_big = [r50.randint(-30, 45) for _ in range(100000)]
    cs["p50_daily_temperatures"] = [
        ("样例 73 74 75 71", "4\n73 74 75 71\n"),
        ("最小 n=1", "1\n30\n"),
        ("一路降温 全都等不到", "5\n32 31 30 29 28\n"),
        ("一路升温", "5\n20 21 22 23 24\n"),
        ("全部相同 相等不算更高", "4\n25 25 25 25\n"),
        ("末尾窜出一个高温", "6\n10 10 10 10 10 40\n"),
        ("随机 n=18 可暴力核对", "18\n" + " ".join(map(str, t50_small)) + "\n"),
        ("大随机 n=100000", "100000\n" + " ".join(map(str, t50_big)) + "\n"),
    ]

    # ---------------------------------------------------------- p51 最长无重复子串
    r51 = random.Random(SEED_MID + 3)
    s51_mid = "".join(r51.choice(ALPHA) for _ in range(20000))
    s51_big = "".join(r51.choice(ALPHA) for _ in range(200000))
    cs["p51_longest_no_repeat"] = [
        ("样例 abcabcbb", "8\nabcabcbb\n"),
        ("最小 n=1", "1\na\n"),
        ("全部相同", "5\nbbbbb\n"),
        ("整串无重复 36 个字符", "36\n" + ALPHA + "\n"),
        ("两个字符来回倒", "12\nabababababab\n"),
        ("随机短串 四种字母", "14\nabcdbacdaabcdd\n"),
        ("随机 n=20000", "20000\n" + s51_mid + "\n"),
        ("最大 n=200000", "200000\n" + s51_big + "\n"),
    ]

    # ---------------------------------------------------------- p52 区间合并
    r52 = random.Random(SEED_MID + 4)

    def iv_text(pairs):
        return "{}\n".format(len(pairs)) + "".join("{} {}\n".format(a, b) for a, b in pairs)

    iv_mid = sorted([(min(x, y), max(x, y)) for x, y in
                    ((r52.randint(0, 5000), r52.randint(0, 5000)) for _ in range(3000))])
    iv_big = sorted([(min(x, y), max(x, y)) for x, y in
                     ((r52.randint(0, 10 ** 9), r52.randint(0, 10 ** 9)) for _ in range(30000))])
    cs["p52_interval_merge"] = [
        ("样例 四段并两段", "4\n1 3\n2 6\n8 10\n9 11\n"),
        ("最小 n=1", "1\n5 9\n"),
        ("单点区间 长度为 0", "1\n7 7\n"),
        ("全部是同一个区间", "5\n2 5\n2 5\n2 5\n2 5\n2 5\n"),
        ("三段互不重叠", "3\n0 1\n5 6\n10 20\n"),
        ("端点相接要并成一段", "3\n1 3\n3 5\n7 9\n"),
        ("随机 n=3000 小坐标", iv_text(iv_mid)),
        ("随机 n=30000 大坐标", iv_text(iv_big)),
    ]

    # ---------------------------------------------------------- p53 区间和查询
    r53 = random.Random(SEED_MID + 5)
    a53 = [r53.randint(-10 ** 9, 10 ** 9) for _ in range(40000)]
    q53a = [(min(x, y), max(x, y)) for x, y in
            ((r53.randint(1, 12), r53.randint(1, 12)) for _ in range(5))]
    q53b = [(min(x, y), max(x, y)) for x, y in
            ((r53.randint(1, 1000), r53.randint(1, 1000)) for _ in range(200))]
    q53c = [(min(x, y), max(x, y)) for x, y in
            ((r53.randint(1, 40000), r53.randint(1, 40000)) for _ in range(15000))]
    cs["p53_range_sum_query"] = [
        ("样例 1..5 三问", "5 3\n1 2 3 4 5\n1 5\n2 4\n5 5\n"),
        ("最小 n=1 负数", "1 1\n-7\n1 1\n"),
        ("全 0 数组", "4 3\n0 0 0 0\n1 4\n2 2\n1 3\n"),
        ("每问都是单点", "3 3\n4 -5 6\n1 1\n2 2\n3 3\n"),
        ("含负数小随机 逐段核对", "12 5\n" +
         " ".join(str(r53.randint(-100, 100)) for _ in range(12)) + "\n" +
         "".join("{} {}\n".format(a, b) for a, b in q53a)),
        ("随机 n=1000 q=200", "1000 200\n" +
         " ".join(str(r53.randint(-10 ** 6, 10 ** 6)) for _ in range(1000)) + "\n" +
         "".join("{} {}\n".format(a, b) for a, b in q53b)),
        ("最大随机 n=40000 q=15000", "40000 15000\n" +
         " ".join(map(str, a53)) + "\n" +
         "".join("{} {}\n".format(a, b) for a, b in q53c)),
    ]

    # ---------------------------------------------------------- p54 差分区间加
    r54 = random.Random(SEED_MID + 6)

    def ops_text(ops):
        return "".join("{} {} {}\n".format(min(x, y), max(x, y), v) for x, y, v in ops)

    a54 = [r54.randint(-10 ** 5, 10 ** 5) for _ in range(20000)]
    ops54_big = [(r54.randint(1, 20000), r54.randint(1, 20000), r54.randint(-10 ** 5, 10 ** 5))
                 for _ in range(20000)]
    ops54_mid = [(r54.randint(1, 3000), r54.randint(1, 3000), r54.randint(-10 ** 4, 10 ** 4))
                 for _ in range(3000)]
    ops54_small = [(r54.randint(1, 60), r54.randint(1, 60), r54.randint(-100, 100))
                   for _ in range(60)]
    cs["p54_diff_range_add"] = [
        ("样例 三次区间加", "5 3\n1 1 1 1 1\n1 3 2\n2 5 3\n4 4 -5\n"),
        ("q=0 一次也不改", "3 0\n7 -2 5\n"),
        ("最小 n=1 反复改同一格", "1 2\n0\n1 1 5\n1 1 -3\n"),
        ("整段同加同减", "5 2\n1 2 3 4 5\n1 5 10\n1 5 -1\n"),
        ("初始值全相同", "6 3\n4 4 4 4 4 4\n2 3 1\n4 6 -4\n1 6 2\n"),
        ("小随机 n=60 q=60 朴素核对", "60 60\n" +
         " ".join(str(r54.randint(-50, 50)) for _ in range(60)) + "\n" + ops_text(ops54_small)),
        ("随机 n=3000 q=3000", "3000 3000\n" +
         " ".join(str(r54.randint(-10 ** 4, 10 ** 4)) for _ in range(3000)) + "\n" +
         ops_text(ops54_mid)),
        ("最大随机 n=20000 q=20000", "20000 20000\n" +
         " ".join(map(str, a54)) + "\n" + ops_text(ops54_big)),
    ]

    # ---------------------------------------------------------- p55 二维前缀和
    r55 = random.Random(SEED_MID + 7)

    def mat_text(rows):
        return "{} {}\n".format(len(rows), len(rows[0])) + "".join(
            " ".join(map(str, row)) + "\n" for row in rows)

    def qs_text(n, m, q):
        lines = [str(q)]
        for _ in range(q):
            r1, r2 = sorted((r55.randint(1, n), r55.randint(1, n)))
            c1, c2 = sorted((r55.randint(1, m), r55.randint(1, m)))
            lines.append("{} {} {} {}".format(r1, c1, r2, c2))
        return "\n".join(lines) + "\n"

    rows7 = [[r55.randint(0, 1000) for _ in range(9)] for _ in range(7)]
    rows120 = [[r55.randint(0, 1000) for _ in range(120)] for _ in range(120)]
    rows300 = [[r55.randint(0, 1000) for _ in range(300)] for _ in range(300)]
    cs["p55_prefix_sum_2d"] = [
        ("样例 3x4 两问", "3 4\n1 2 3 4\n5 6 7 8\n9 10 11 12\n2\n1 1 2 2\n2 3 3 4\n"),
        ("最小 1x1", "1 1\n7\n1\n1 1 1 1\n"),
        ("问整张表", "3 3\n1 2 3\n4 5 6\n7 8 9\n1\n1 1 3 3\n"),
        ("单行退化成一维前缀和", "1 5\n3 1 4 1 5\n3\n1 1 1 3\n1 2 1 5\n1 5 1 5\n"),
        ("全 0 矩阵", "2 2\n0 0\n0 0\n1\n1 1 2 2\n"),
        ("随机 7x9 直接加核对", mat_text(rows7) + "3\n1 1 7 9\n2 3 5 8\n4 4 4 4\n"),
        ("随机 120x120 q=3000", mat_text(rows120) + qs_text(120, 120, 3000)),
        ("最大 300x300 q=10000", mat_text(rows300) + qs_text(300, 300, 10000)),
    ]

    # ---------------------------------------------------------- p56 朋友圈
    r56 = random.Random(SEED_MID + 8)
    e60 = [(r56.randint(1, 60), r56.randint(1, 60)) for _ in range(80)]
    e_big = [(r56.randint(1, 30000), r56.randint(1, 30000)) for _ in range(50000)]
    cs["p56_friend_circles"] = [
        ("样例 5 人 3 条关系", "5 3\n1 2\n2 3\n4 5\n"),
        ("最小 n=1 无关系", "1 0\n"),
        ("谁都不认识谁", "3 0\n"),
        ("四人首尾连成一个圈", "4 4\n1 2\n2 3\n3 4\n4 1\n"),
        ("重边与自环", "3 4\n1 1\n1 2\n1 2\n2 3\n"),
        ("一条链 200 人", "200 199\n" +
         "".join("{} {}\n".format(i, i + 1) for i in range(1, 200))),
        ("随机 60 人 有意留孤立点", "60 {}\n".format(len(e60)) +
         "".join("{} {}\n".format(a, b) for a, b in e60)),
        ("大随机 30000 人 50000 条关系", "30000 50000\n" +
         "".join("{} {}\n".format(a, b) for a, b in e_big)),
    ]

    # ---------------------------------------------------------- p57 单源最短路
    r57 = random.Random(SEED_MID + 9)

    def gen_graph(n, extra, rnd):
        """先挂一棵 1 号点为根的有向树（每个点都能被走到），再补随机边。"""
        edges = []
        for i in range(2, n + 1):
            edges.append((rnd.randint(1, i - 1), i, rnd.randint(0, 10 ** 4)))
        for _ in range(extra):
            u, v = rnd.randint(1, n), rnd.randint(1, n)
            if u != v:
                edges.append((u, v, rnd.randint(0, 10 ** 4)))
        return edges

    def graph_text(n, edges):
        return "{} {} 1\n".format(n, len(edges)) + "".join(
            "{} {} {}\n".format(u, v, w) for u, v, w in edges)

    e40 = gen_graph(40, 60, r57)
    e3000 = gen_graph(3000, 9000, r57)
    e20000 = gen_graph(20000, 25000, r57)
    cs["p57_dijkstra_shortest"] = [
        ("样例 4 点 5 边", "4 5 1\n1 2 3\n1 3 1\n3 2 2\n2 4 2\n3 4 5\n"),
        ("最小 n=1 只有一条自环", "1 1 1\n1 1 0\n"),
        ("走不到的点输出 -1", "3 1 1\n1 2 5\n"),
        ("零权边与重边", "5 6 1\n1 2 7\n1 2 3\n2 3 0\n3 4 0\n1 5 10\n4 5 1\n"),
        ("起点在一个环上", "3 3 2\n1 2 4\n2 3 5\n3 1 6\n"),
        ("随机 n=40 朴素核对", graph_text(40, e40)),
        ("随机 n=3000 一万多条边", graph_text(3000, e3000)),
        ("大随机 n=20000 四万条边", graph_text(20000, e20000)),
    ]

    # ---------------------------------------------------------- p58 跳石头
    r58 = random.Random(SEED_MID + 10)
    rocks10 = sorted(r58.sample(range(1, 1000), 10))
    rocks20000 = sorted(r58.sample(range(1, 10 ** 6), 20000))
    rocks50000 = sorted(r58.sample(range(1, 10 ** 9), 50000))
    cs["p58_jump_stones"] = [
        ("样例 河宽 25 搬 2 块", "25 5 2\n2 11 14 17 21\n"),
        ("最小 L=1 没有岩石", "1 0 0\n"),
        ("一块也不能搬", "10 3 0\n4 6 7\n"),
        ("允许搬光所有岩石", "10 3 3\n2 5 8\n"),
        ("岩石紧挨着终点", "7 2 1\n6 3\n"),
        ("随机 n=10 枚举核对", "1000 10 3\n" + " ".join(map(str, rocks10)) + "\n"),
        ("随机 L=1e6 n=20000", "1000000 20000 8000\n" + " ".join(map(str, rocks20000)) + "\n"),
        ("最大 L=1e9 n=50000", "1000000000 50000 25000\n" +
         " ".join(map(str, rocks50000)) + "\n"),
    ]

    # ---------------------------------------------------------- p59 凑数方案数
    r59 = random.Random(SEED_MID + 11)
    n13 = [r59.randint(1, 40) for _ in range(13)]
    n60 = [r59.randint(1, 200) for _ in range(60)]
    n100 = [r59.randint(1, 500) for _ in range(100)]
    cs["p59_subset_sum_count"] = [
        ("样例 凑 8", "6 8\n1 2 3 4 5 6\n"),
        ("s=0 只有空取法", "3 0\n1 2 3\n"),
        ("谁都凑不出来", "3 100\n1 2 3\n"),
        ("全相同 选一半", "8 4\n1 1 1 1 1 1 1 1\n"),
        ("只能全部拿走", "4 10\n1 2 3 4\n"),
        ("随机 n=13 全枚举核对", "13 150\n" + " ".join(map(str, n13)) + "\n"),
        ("随机 n=60 s=1500", "60 1500\n" + " ".join(map(str, n60)) + "\n"),
        ("最大 n=100 s=5000", "100 5000\n" + " ".join(map(str, n100)) + "\n"),
    ]

    # ---------------------------------------------------------- p60 零钱兑换
    r60 = random.Random(SEED_MID + 12)
    coins50 = sorted(r60.sample(range(1, 5001), 50))
    coins12 = [r60.randint(1, 300) for _ in range(12)]
    cs["p60_coin_change_min"] = [
        ("样例 1 2 5 凑 11", "3 11\n1 2 5\n"),
        ("金额 0 不用硬币", "3 0\n1 2 5\n"),
        ("凑不出来输出 -1", "2 3\n2 4\n"),
        ("面额都比金额大", "2 5\n7 9\n"),
        ("贪心会出错的 1 3 4 凑 6", "3 6\n1 3 4\n"),
        ("只有一种面额刚好整除", "1 49\n7\n"),
        ("随机 k=12 s=1500 BFS 核对", "12 1500\n" + " ".join(map(str, coins12)) + "\n"),
        ("最大 k=50 s=20000", "50 20000\n" + " ".join(map(str, coins50)) + "\n"),
    ]

    # ---------------------------------------------------------- p61 最长公共子序列
    r61 = random.Random(SEED_MID + 13)
    a300 = "".join(r61.choice("abcde") for _ in range(300))
    b300 = "".join(r61.choice("abcde") for _ in range(300))
    a1200 = "".join(r61.choice("abcdefgh") for _ in range(1200))
    b1200 = "".join(r61.choice("abcdefig") for _ in range(1200))
    cs["p61_lcs_length"] = [
        ("样例 abcbdab 与 bdcaba", "7 6\nabcbdab\nbdcaba\n"),
        ("最小 1x1 相同", "1 1\na\na\n"),
        ("最小 1x1 不同", "1 1\na\nb\n"),
        ("两个串一模一样", "6 6\nabcdef\nabcdef\n"),
        ("字母完全不重叠 答案 0", "5 5\naaaaa\nbbbbb\n"),
        ("一个是另一个的子序列", "5 9\nabcde\nazbzzczdz\n"),
        ("随机 300 x 300", "300 300\n" + a300 + "\n" + b300 + "\n"),
        ("最大 1200 x 1200", "1200 1200\n" + a1200 + "\n" + b1200 + "\n"),
    ]

    # ---------------------------------------------------------- p62 组合数取模
    r62 = random.Random(SEED_MID + 14)
    q40 = [(r62.randint(0, 900), r62.randint(0, 900)) for _ in range(40)]
    q200 = [(r62.randint(0, 100000), r62.randint(0, 100000)) for _ in range(200)]
    cs["p62_comb_mod_query"] = [
        ("样例 三问", "3\n5 2\n10 3\n100000 0\n"),
        ("k 大于 n 输出 0", "1\n5 6\n"),
        ("n=0 与 k=0 的边界", "3\n0 0\n0 1\n7 0\n"),
        ("k=1 与 k=n-1", "2\n100000 1\n100000 99999\n"),
        ("正中间那一档", "1\n100000 50000\n"),
        ("大 n 小 k 连乘核对", "2\n100000 3\n99999 2\n"),
        ("随机 40 组 n 不超过 900", "40\n" + "".join("{} {}\n".format(a, b) for a, b in q40)),
        ("最大 200 组 n 到 1e5", "200\n" + "".join("{} {}\n".format(a, b) for a, b in q200)),
    ]
    return cs
