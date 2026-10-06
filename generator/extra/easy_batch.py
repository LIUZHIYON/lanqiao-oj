"""入门语法练习批：p28 ~ p47 共 20 道编程题（练 Python 语法用）。

约定（照 _TEMPLATE.py）：
  · 参考解在 generator/reference/<pid>.py，读 stdin、print 答案
  · prog_cases() 返回 {pid: [(测试点名字, 输入文本), ...]}，第一条必须是可见样例
  · 只手写输入数据，expected 一律由 build_problems.py 真实运行参考解得到

构建与自检：
    python generator/build_problems.py --only p28 p29 ... p47
    python generator/self_check.py    --only p28 p29 ... p47
"""
import datetime
import random

SEED = 20261007

PROG_META = [
    dict(pid="p28_arithmetic_bundle", title="四则运算套餐", difficulty="入门",
         tags=["运算符", "输入输出"], chapter="第 1 章 运算符 / 第 2 章 流程控制",
         source="蓝桥杯风格语法练习",
         reference="code/ch01-basics/04_floor_division.py",
         input_format="一行两个正整数 a、b（1 ≤ a、b ≤ 10^9），中间用一个空格分隔。",
         output_format="一行五个整数：和、差、积、整除的商、余数，用一个空格分隔。",
         statement="<p>读入两个正整数 <code>a</code> 和 <code>b</code>，把四则运算的结果一次算完。</p>"
                   "<p>Python 里整数相除要用 <code>//</code>（商向下取整），余数用 <code>%</code>。"
                   "只写一个斜杠 <code>/</code> 得到的是小数，不能当商用。</p>"
                   "<p>输出五个结果，顺序固定：和、差、积、整除的商、余数。</p>",
         idea="<p>先 <code>a, b = map(int, input().split())</code> 把两个数读进来，"
              "再一行 <code>print(a + b, a - b, a * b, a // b, a % b)</code>。"
              "<code>print</code> 用逗号分隔多个值时，会自动在中间打一个空格。</p>"
              "<p>差可能是负数（a 小于 b 的时候），乘积最大到 10 的 18 次方。"
              "Python 的整数不会溢出，放心直接乘。</p>"),

    dict(pid="p29_digit_sum", title="各位数字之和", difficulty="入门",
         tags=["拆位", "循环"], chapter="第 1 章 运算符 / 第 2 章 循环",
         source="蓝桥杯风格语法练习",
         reference="code/ch01-basics/22_ex_digit_sum.py",
         input_format="第一行一个整数 T（1 ≤ T ≤ 50000）；接下来 T 行，每行一个整数 n（-10^9 ≤ n ≤ 10^9）。",
         output_format="T 行，每行一个整数，是对应那个 n 的各位数字之和。",
         statement="<p>把一个整数的每一位数字加起来。</p>"
                   "<p>例如 123 的各位数字之和是 <code>1 + 2 + 3 = 6</code>；9999 是 36；0 是 0。</p>"
                   "<p>本题第一行先给组数 <code>T</code>，接下来 <code>T</code> 行每行一个整数，"
                   "每个数单独输出一行结果。</p>"
                   "<p>拆位的通用招法：一遍遍用 <code>n % 10</code> 拿到最低位，"
                   "再用 <code>n //= 10</code> 把最低位扔掉，直到 n 变成 0。"
                   "负号不参与求和，按绝对值拆。</p>",
         idea="<p>循环写法：<code>while n &gt; 0: total += n % 10; n //= 10</code>。"
              "n 本来是 0 时循环一次都不进，结果正好是 0，不用特判。</p>"
              "<p>另一条路是把数字当字符串：<code>sum(int(c) for c in str(abs(n)))</code>。"
              "两种都练一遍，考场上写顺手的那个。</p>"),

    dict(pid="p30_seconds_convert", title="秒数换算", difficulty="入门",
         tags=["整除取余"], chapter="第 1 章 运算符",
         source="蓝桥杯风格语法练习",
         reference="code/ch01-basics/24_ex_seconds.py",
         input_format="一行一个非负整数 s（0 ≤ s ≤ 10^9），表示总秒数。",
         output_format="一行四个整数：天 时 分 秒，用一个空格分隔，不补零。",
         statement="<p>一段时间用总秒数表示，把它拆成 <code>天 时 分 秒</code> 四个数。</p>"
                   "<p>进率：1 分 = 60 秒，1 时 = 3600 秒，1 天 = 86400 秒。</p>"
                   "<p>算法是大单位先算：先取天数，把剩下的秒数拿来算小时，再算分钟，"
                   "最后剩下的就是秒。整除 <code>//</code> 拿商，取余 <code>%</code> 留零头，一级一级往下剥。</p>",
         idea="<p><code>day = s // 86400</code>，<code>rest = s % 86400</code>；"
              "接着 <code>hour = rest // 3600</code>、<code>rest %= 3600</code>、"
              "<code>minute = rest // 60</code>、<code>second = rest % 60</code>。</p>"
              "<p>写完拿 59、60、3599、86399、86400 这几个数口算对一遍，一秒都不能差。</p>"),

    dict(pid="p31_bmi_level", title="BMI 判定", difficulty="入门",
         tags=["if-elif", "浮点数"], chapter="第 2 章 流程控制 / 第 1 章 浮点数",
         source="蓝桥杯风格语法练习",
         reference="code/ch02-control/01_if_elif_basics.py",
         input_format="一行两个数：身高（米，小数，1 ≤ 身高 ≤ 2.5）和体重（公斤，小数，1 ≤ 体重 ≤ 300），空格分隔。",
         output_format="一行一个等级，只能是 偏瘦、正常、偏胖、肥胖 四个词之一。",
         statement="<p>身体质量指数 <code>BMI = 体重（公斤）÷ 身高（米）÷ 身高（米）</code>。</p>"
                   "<p>按下面的标准输出等级，注意每一档左边界算进来、右边界不算：</p>"
                   "<ul><li>BMI 小于 18.5：偏瘦</li>"
                   "<li>18.5 到 24：正常（含 18.5，不含 24）</li>"
                   "<li>24 到 28：偏胖（含 24，不含 28）</li>"
                   "<li>28 及以上：肥胖（含 28）</li></ul>"
                   "<p>用 <code>if-elif-else</code> 从上往下判断，每个分支只写上界，"
                   "不要写成一串互相重叠的条件。</p>",
         idea="<p><code>bmi = weight / (height * height)</code>，然后一路 "
              "<code>if bmi &lt; 18.5 ... elif bmi &lt; 24 ... elif bmi &lt; 28 ... else ...</code>。</p>"
              "<p>边界最容易错：BMI 正好 18.5 属于正常，正好 24 属于偏胖，正好 28 属于肥胖。"
              "自测就挑整数关系的数据，比如身高 2.0 米、体重 74 公斤正好是 18.5。</p>"),

    dict(pid="p32_score_grades", title="成绩等级与平均分", difficulty="入门",
         tags=["多分支", "格式化输出"], chapter="第 2 章 流程控制 / 第 1 章 格式化输出",
         source="蓝桥杯风格语法练习",
         reference="code/ch01-basics/11_format_output.py",
         input_format="第一行一个整数 n（1 ≤ n ≤ 100000）；第二行 n 个整数成绩，空格分隔，每个成绩在 0 到 100 之间。",
         output_format="前 n 行每行一个字母 A、B、C 或 D，顺序与输入一致；第 n+1 行是平均分，保留两位小数。",
         statement="<p>读入 n 个成绩，逐个评级，每个等级单独一行：</p>"
                   "<ul><li>90 分及以上：A</li><li>80 到 89 分：B</li>"
                   "<li>60 到 79 分：C</li><li>60 分以下：D</li></ul>"
                   "<p>等级全部输出完之后，再单独一行输出平均分，保留两位小数，"
                   "形如 <code>76.40</code>——末尾的 0 也要写出来，不能只写 76.4。</p>",
         idea="<p>评级写成函数，从高分档一路 <code>if</code> 到低分档，最后 "
              "<code>return 'D'</code> 收尾，这样不会出现两个档同时命中。</p>"
              "<p>平均分用 <code>format(sum(scores) / n, '.2f')</code>，<code>.2f</code> 会自动补足两位。"
              "别用 <code>print(round(x, 2))</code>：76.4 会被打成 <code>76.4</code>，小数位少了一位。</p>"),

    dict(pid="p33_leap_weekday", title="闰年与星期", difficulty="入门",
         tags=["闰年判断", "日期处理"], chapter="第 1 章 运算符 / 第 3 章 列表与元组",
         source="蓝桥杯风格语法练习",
         reference="code/ch01-basics/25_ex_leap_year.py",
         input_format="一行三个整数 y、m、d（1900 ≤ y ≤ 2100，1 ≤ m ≤ 12，d 是该月合法日期），表示 y 年 m 月 d 日，空格分隔。",
         output_format="一行两个字段，空格分隔：第一个是 闰 或 平，第二个是 周一 到 周日。",
         statement="<p>给一个日期，输出两件事：这一年是闰年还是平年，以及这一天是星期几。</p>"
                   "<p>闰年规则：能被 4 整除且不能被 100 整除，或者能被 400 整除。"
                   "所以 1900 年是平年，2000 年是闰年。</p>"
                   "<p>星期几要输出成汉字：<code>周一</code>、<code>周二</code>、……、<code>周六</code>、<code>周日</code>。</p>",
         idea="<p>闰年一行表达式就能搞定：<code>(y % 4 == 0 and y % 100 != 0) or y % 400 == 0</code>。</p>"
              "<p>星期用标准库：<code>import datetime</code>，"
              "<code>datetime.date(y, m, d).weekday()</code> 返回 0 到 6，"
              "<strong>0 是周一，6 才是周日</strong>。拿一个七个元素的表按下标取名字，"
              "别把周日排到第一个位置。</p>"),

    dict(pid="p34_char_classify", title="字符分类统计", difficulty="入门",
         tags=["字符串方法", "条件计数"], chapter="第 3 章 字符串 / 第 2 章 循环",
         source="蓝桥杯风格语法练习",
         reference="code/ch03-data/17_str_toolbox.py",
         input_format="一行文本，长度 1 到 100000，可能含空格、标点、数字和汉字，行尾没有多余空格。",
         output_format="一行三个整数：字母数 数字数 其它字符数，用一个空格分隔。",
         statement="<p>数一行文本里的字符，分成三类：</p>"
                   "<ul><li>字母：只算 26 个英文字母，大小写都算</li>"
                   "<li>数字：只算 <code>0</code> 到 <code>9</code> 这十个字符</li>"
                   "<li>其它：空格、标点符号、汉字等统统算这一类</li></ul>"
                   "<p>行末那个换行符不算文本内容，不要统计它；行中间的空格要算。</p>"
                   "<p>这题的坑在于 <code>isalpha()</code> 对汉字也返回 True，"
                   "所以字母那一类必须再限定是 ASCII 字符，汉字得落到「其它」里。</p>",
         idea="<p>一个循环三种情况：<code>c.isdigit()</code> 记数字，"
              "<code>c.isascii() and c.isalpha()</code> 记字母，其余全记其它。</p>"
              "<p>读整行用 <code>input()</code>——它连着中间的空格一起读，只去掉行末换行。"
              "千万别 <code>input().split()</code>，那样空格会把文本切碎，空格就漏数了。</p>"),

    dict(pid="p35_reverse_words", title="单词倒序", difficulty="入门",
         tags=["split", "join"], chapter="第 3 章 字符串",
         source="蓝桥杯风格语法练习",
         reference="code/ch03-data/15_str_split_join.py",
         input_format="一行英文句子，至少含一个单词。单词由字母、数字和常见标点组成，单词之间用空格或制表符分隔（可能连续多个，行首行尾也可能有）。整行长度不超过 400000 个字符。",
         output_format="一行，单词顺序反转，单词之间恰好一个空格，行末没有空格。",
         statement="<p>一行英文句子里有很多单词，把单词的顺序整个反过来，单词内容不变，输出仍然是一行。</p>"
                   "<p>例如 <code>Hello world python</code> 反过来是 <code>python world Hello</code>。</p>"
                   "<p>单词之间可能有一个或多个空格，行首行尾也可能有空格，中间还可能夹着制表符。"
                   "这些空白都不算单词，输出时单词之间只用一个空格。</p>",
         idea="<p>口诀：<code>' '.join(reversed(s.split()))</code>。</p>"
              "<p>关键在 <code>split()</code> 不带参数：任意一段连续空白都当成一个分隔符，"
              "首尾空白也自动丢掉。要是写成 <code>split(' ')</code>，几个连续空格会切出一堆空字符串，"
              "倒过来一打印就满行都是多余的间隔。</p>"),

    dict(pid="p36_palindrome_check", title="回文判断", difficulty="入门",
         tags=["切片", "字符串"], chapter="第 3 章 切片 / 第 1 章 字符串",
         source="蓝桥杯风格语法练习",
         reference="code/ch03-data/04_slice_rules.py",
         input_format="一行字符串，长度 1 到 100000，由字母、数字、空格和常见标点组成，行尾没有多余空格。",
         output_format="一行，yes 或 no，全小写。",
         statement="<p>正着读和反着读一模一样的串叫回文，比如 <code>level</code>、<code>abCCba</code>。</p>"
                   "<p>本题<strong>忽略大小写</strong>：先把大写全转成小写，再判断是不是回文。"
                   "空格和标点照常参与比较，不要删掉。</p>"
                   "<p>是回文输出 <code>yes</code>，不是输出 <code>no</code>。</p>",
         idea="<p>两步走：<code>low = s.lower()</code>，然后比 <code>low == low[::-1]</code>。</p>"
              "<p><code>[::-1]</code> 是步长为 -1 的切片，等于整串反转。"
              "它会复制出一个新串，10 万长度也完全跑得动，不用纠结。</p>"),

    dict(pid="p37_max_min_range", title="最大最小与极差", difficulty="入门",
         tags=["打擂台", "循环"], chapter="第 2 章 累加与打擂台",
         source="蓝桥杯风格语法练习",
         reference="code/ch02-control/02_accumulate_templates.py",
         input_format="第一行一个整数 n（1 ≤ n ≤ 100000）；第二行 n 个整数，空格分隔，每个数在 -10^9 到 10^9 之间。",
         output_format="一行三个整数：最大值 最小值 极差，用一个空格分隔。",
         statement="<p>读入 n 个整数，输出其中的最大值、最小值，以及极差（最大值减最小值）。</p>"
                   "<p>找最大最小的通用做法是打擂台：先让第一个数当擂主，"
                   "后面的数挨个上台比一比，谁大谁就当新擂主。</p>",
         idea="<p><code>high = low = nums[0]</code>，一个循环里两次比较："
              "<code>if v &gt; high</code> 换最大值，<code>if v &lt; low</code> 换最小值。</p>"
              "<p>擂主一定要取输入的第一个数，不要从 0 起步：全是负数的时候，从 0 起步会把最大值错当成 0。"
              "极差一定非负，最大值减最小值不可能越界。</p>"),

    dict(pid="p38_count_filter", title="计数筛选", difficulty="入门",
         tags=["条件计数", "循环"], chapter="第 2 章 累加与打擂台",
         source="蓝桥杯风格语法练习",
         reference="code/ch02-control/02_accumulate_templates.py",
         input_format="第一行两个整数 n 和 x（1 ≤ n ≤ 100000，-10^9 ≤ x ≤ 10^9）；第二行 n 个整数，空格分隔，每个数在 -10^9 到 10^9 之间。",
         output_format="一行两个整数：个数 总和，用一个空格分隔。",
         statement="<p>读入 n 个整数和一个门槛值 <code>x</code>，把其中大于等于 x 的数挑出来，"
                   "输出两件事：挑出来的个数、这些数的总和。</p>"
                   "<p>一个都没挑到时，个数与和都输出 0。</p>"
                   "<p>注意门槛是「大于或等于」，正好等于 x 的那个数也要算进来。</p>",
         idea="<p>一次循环干两件事：<code>if v &gt;= x:</code> 里面同时 <code>cnt += 1</code> "
              "和 <code>total += v</code>，不用先把数存下来再遍历一遍。</p>"
              "<p>条件写成 <code>&gt;</code> 还是 <code>&gt;=</code> 是这题最常见的错，"
              "拿「x 刚好等于数组里某个数」的数据自测一次就能发现。</p>"),

    dict(pid="p39_mult_table", title="九九乘法表", difficulty="入门",
         tags=["嵌套循环", "格式输出"], chapter="第 2 章 嵌套循环",
         source="蓝桥杯风格语法练习",
         reference="code/ch02-control/04_enumerate_nested.py",
         input_format="一行一个整数 n（1 ≤ n ≤ 9）。",
         output_format="共 n 行。第 i 行有 i 个算式，形如 j*i=积，算式之间用一个空格分隔，行末没有空格。",
         statement="<p>输出前 n 行九九乘法表，形状是下三角。</p>"
                   "<p>第 <code>i</code> 行有 <code>i</code> 个算式，从左到右依次是 "
                   "<code>1*i=结果</code>、<code>2*i=结果</code>、……、<code>i*i=结果</code>。"
                   "比如第 4 行是 <code>1*4=4 2*4=8 3*4=12 4*4=16</code>。</p>"
                   "<p>算式之间恰好一个空格，行末不能有多余空格。</p>",
         idea="<p>外层 <code>for i in range(1, n + 1)</code>，内层 <code>for j in range(1, i + 1)</code>——"
              "内层的上界跟着外层走，这才印得出下三角。</p>"
              "<p>输出别用 <code>print(..., end=' ')</code> 一个一个打，很容易在行尾多留一个空格。"
              "把一行的算式先收进列表，再 <code>' '.join(行)</code>，整表拼好一次性输出。</p>"),

    dict(pid="p40_prime_check", title="素数判定", difficulty="入门",
         tags=["素数", "试除"], chapter="第 2 章 循环与 break",
         source="蓝桥杯风格语法练习",
         reference="code/ch02-control/16_ex1_prime.py",
         input_format="第一行一个整数 n（1 ≤ n ≤ 200）；第二行 n 个正整数，空格分隔，每个数在 1 到 2000000000 之间。",
         output_format="前 n 行每行一个 yes 或 no，顺序与输入一致；第 n+1 行一个整数，是素数的个数。",
         statement="<p>给 n 个正整数，逐个判断是不是素数：是输出 <code>yes</code>，不是输出 <code>no</code>，"
                   "最后再单独一行输出素数一共有几个。</p>"
                   "<p>素数是大于 1、只能被 1 和自己整除的整数。"
                   "<strong>1 不是素数，2 是最小的素数，也是唯一的偶素数。</strong></p>"
                   "<p>试除只要试到平方根就够：如果 <code>d * d</code> 已经超过 x 还没找到因子，"
                   "x 一定是素数。用 <code>math.isqrt(x)</code> 直接拿整数平方根。</p>",
         idea="<p>写一个 <code>is_prime(x)</code>：<code>x &lt; 2</code> 直接 False；"
              "<code>x == 2</code> 是 True；偶数直接 False；剩下的让因子 d 从 3 起每次加 2，"
              "试到 <code>isqrt(x)</code> 为止。</p>"
              "<p>试到平方根是这题的分水岭：20 亿开根约 44721，判一次最多两万多次数；"
              "要是傻试到 x 的一半，一次就是一亿次循环，直接超时。</p>"),

    dict(pid="p41_fib_list", title="斐波那契前 n 项", difficulty="入门",
         tags=["递推", "大整数"], chapter="第 2 章 循环 / 第 1 章 大整数",
         source="蓝桥杯省赛真题（题意整理）",
         reference="code/ch02-control/20_ex5_fib_nth.py",
         input_format="一行一个整数 n（1 ≤ n ≤ 90）。",
         output_format="一行 n 个整数，空格分隔，是数列的前 n 项。",
         statement="<p>数列规定第 1 项和第 2 项都是 1，从第 3 项起每一项等于前两项之和："
                   "<code>1 1 2 3 5 8 13 21 ……</code></p>"
                   "<p>读入 n，输出前 n 项，用一个空格分隔。</p>"
                   "<p>官方练习系统里这道题要求每一项对 10007 取模；本题 n 不超过 90，"
                   "第 90 项约是 2.88 × 10^18，Python 的整数完全装得下，所以不取模。</p>",
         idea="<p>滚动两个变量：<code>a, b = b, a + b</code> 一行就完成一次递推，"
              "注意先把当前的 a 收进结果，再更新。</p>"
              "<p>递归 <code>fib(n) = fib(n-1) + fib(n-2)</code> 也能写对，"
              "但 n 到 35 左右就要几百万次调用，还会撞上递归深度限制，考场上老老实实写循环。</p>"),

    dict(pid="p42_bubble_sort", title="手写冒泡排序", difficulty="入门",
         tags=["排序", "嵌套循环"], chapter="第 3 章 列表与排序 / 第 2 章 嵌套循环",
         source="蓝桥杯风格语法练习",
         reference="code/ch03-data/03_list_sort_methods.py",
         input_format="第一行一个整数 n（1 ≤ n ≤ 1000）；第二行 n 个整数，空格分隔，每个数在 -10^9 到 10^9 之间。",
         output_format="一行 n 个整数，从小到大排列，空格分隔，行末没有空格。",
         statement="<p>把 n 个整数从小到大排好输出。</p>"
                   "<p>这道题要练的是排序基本功：<strong>自己写双重循环做冒泡</strong>。"
                   "相邻两个数比一比，前面比后面大就交换；走完一趟，最大的那个就冒到了末尾，"
                   "下一趟就可以少看最后一个位置。</p>"
                   "<p>冒泡是 O(n 的平方) 的算法，所以 n 只给到 1000。"
                   "判题只看最后结果，用 <code>sorted()</code> 也能过，但就练不到这一招了。</p>",
         idea="<p>外层 <code>for i in range(n - 1)</code>，内层 <code>for j in range(n - 1 - i)</code>："
              "已经冒到尾巴上的 i 个数不用再比。</p>"
              "<p>交换直接用 <code>a[j], a[j + 1] = a[j + 1], a[j]</code>。"
              "再加一个 <code>swapped</code> 标记，一整趟没发生交换说明已经有序，直接 <code>break</code>，"
              "最好的情况能降到 O(n)。</p>"),

    dict(pid="p43_dedupe_order", title="去重保序", difficulty="入门",
         tags=["集合", "列表"], chapter="第 3 章 集合 / 第 3 章 列表",
         source="蓝桥杯风格语法练习",
         reference="code/ch03-data/21_ex_dedupe_order.py",
         input_format="第一行一个整数 n（1 ≤ n ≤ 100000）；第二行 n 个整数，空格分隔，每个数在 -10^9 到 10^9 之间。",
         output_format="一行，去重后的整数，按第一次出现的先后顺序排列，空格分隔，行末没有空格。",
         statement="<p>n 个整数里有些会重复出现。把它们按<strong>第一次出现的先后顺序</strong>输出，"
                   "重复的丢掉，同一个数只保留它第一次出现的那个位置。</p>"
                   "<p>例如 <code>1 3 2 3 1 5 2 7</code> 去重后是 <code>1 3 2 5 7</code>。</p>"
                   "<p>坑在于 <code>set</code> 能判重，但集合自己不讲顺序，"
                   "所以要一边扫一边把新数字收进一个列表里。</p>",
         idea="<p>套路是两份数据各司其职：<code>seen = set()</code> 负责问「见过没有」，"
              "<code>out = []</code> 负责记住先后顺序。没见过的数同时进两处。</p>"
              "<p><code>v not in seen</code> 是 O(1)，整体 O(n)。"
              "要是写成 <code>v not in out</code>（在列表里逐个找），最坏每次都要扫全表，"
              "10 万个数直接超时。</p>"),

    dict(pid="p44_char_topk", title="出现次数最多的 k 个字符", difficulty="入门",
         tags=["计数", "多条件排序"], chapter="第 3 章 字典与排序",
         source="蓝桥杯风格语法练习",
         reference="code/ch03-data/11_dict_count_sort.py",
         input_format="第一行一个字符串 s（长度 1 到 100000，只含小写字母 a-z 和数字 0-9，不含空格）；第二行一个整数 k（1 ≤ k ≤ s 中不同字符的个数）。",
         output_format="一行 k 个 字符:次数，用一个空格分隔，行末没有空格。",
         statement="<p>一行由小写字母和数字组成的串，统计每个字符出现了几次，输出次数最多的 k 个字符。</p>"
                   "<p>排序规则有两条，按先后依次生效：</p>"
                   "<ul><li>出现次数多的排在前面</li>"
                   "<li>次数一样时，字符本身小的排在前面（按 <code>0-9</code>、<code>a-z</code> 的顺序）</li></ul>"
                   "<p>每个字符写成 <code>字符:次数</code> 的形式，彼此用一个空格分隔。"
                   "题目保证 k 不超过出现过的字符种类数。</p>",
         idea="<p>先计数：<code>cnt[c] = cnt.get(c, 0) + 1</code>，或者 "
              "<code>Counter(s)</code>。</p>"
              "<p>排序一行解决：<code>sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))</code>。"
              "次数前面加负号，「从大到小」就变成了「取负之后的从小到大」，"
              "字符不加符号仍是从小到大——多条件排序就用这招一次排完。</p>"),

    dict(pid="p45_base_convert", title="任意进制转换", difficulty="入门",
         tags=["进制", "字符串"], chapter="第 1 章 进制与 ASCII",
         source="蓝桥杯省赛真题（题意整理）",
         reference="code/ch01-basics/26_ex_base_convert.py",
         input_format="一行两个整数 n 和 b（-10^15 ≤ n ≤ 10^15，2 ≤ b ≤ 16），空格分隔。",
         output_format="一行，n 的 b 进制表示，数字 10 以上用大写字母 A 到 F，负数最前面带一个负号。",
         statement="<p>把一个十进制整数 n 转成 b 进制（b 在 2 到 16 之间）。</p>"
                   "<p>约定：数字 10 到 15 依次用大写字母 <code>A</code> 到 <code>F</code> 表示；"
                   "负数在最前面输出一个负号，其余部分按绝对值转；0 就输出 <code>0</code>。</p>"
                   "<p>短除法：反复 <code>n % b</code> 拿到当前最低位，<code>n //= b</code> 去掉这一位，"
                   "把拿到的字符一个个攒起来，最后反过来拼就是答案——先拿到的是低位。</p>",
         idea="<p>先记下 <code>neg = n &lt; 0</code>，再 <code>n = abs(n)</code>，"
              "全程只处理非负数，最后按需要在结果最前面挂个负号，省去一堆分支。"
              "<code>n == 0</code> 时循环一次都不进，要特判。</p>"
              "<p>写完可以交叉验证：<code>bin</code>、<code>oct</code>、<code>hex</code> 的结果"
              "去掉前缀 <code>0b</code>、<code>0o</code>、<code>0x</code>，应该和自己转 2、8、16 进制一致。</p>"),

    dict(pid="p46_narcissistic", title="区间内的水仙花数", difficulty="入门",
         tags=["枚举", "拆位"], chapter="第 2 章 枚举与循环",
         source="蓝桥杯省赛真题（题意整理）",
         reference="code/ch02-control/17_ex2_narcissistic.py",
         input_format="一行两个整数 lo 和 hi（1 ≤ lo ≤ hi ≤ 999），空格分隔，表示闭区间。",
         output_format="一行，区间内所有三位水仙花数用英文逗号分隔（逗号后不加空格），从小到大排列；一个都没有时输出 none。",
         statement="<p>三位数里，各位数字的立方和等于自身的数叫水仙花数，"
                   "例如 <code>153 = 1 的立方 + 5 的立方 + 3 的立方</code>。</p>"
                   "<p>给一个闭区间 <code>[lo, hi]</code>，把落在区间里的三位水仙花数从小到大输出，"
                   "用英文逗号分隔；一个都没有就输出 <code>none</code>。</p>"
                   "<p>区间可能探到三位数外面去（比如 1 到 99），但一位数和两位数都不算水仙花数，"
                   "所以实际枚举的范围要跟 100 和 999 取个交集。</p>",
         idea="<p>拆三位：<code>a = n // 100</code>、<code>b = n // 10 % 10</code>、"
              "<code>c = n % 10</code>，再判 <code>a*a*a + b*b*b + c*c*c == n</code>。</p>"
              "<p>枚举下界取 <code>max(lo, 100)</code>、上界取 <code>min(hi, 999)</code>，别越界。"
              "三位水仙花数只有 153、370、371、407 四个，先拿这四个数把自己写的程序对一遍。</p>"),

    dict(pid="p47_triangle_area", title="三角形判定与面积", difficulty="入门",
         tags=["条件判断", "math.sqrt"], chapter="第 2 章 流程控制 / 第 1 章 浮点数",
         source="蓝桥杯风格语法练习",
         reference="code/ch01-basics/27_ex_circle.py",
         input_format="一行三个正数（可以是小数），空格分隔，是三条边的长度，每个都在 1 到 1000 之间。",
         output_format="能构成三角形时，一行两个字段：yes 和面积，面积保留两位小数，空格分隔；否则只输出一行 no。",
         statement="<p>给三条边长，先判断能不能拼成一个三角形："
                   "任意两边之和都要<strong>严格大于</strong>第三边。"
                   "三边排好序之后，只要检查最短两条之和是不是大于最长边。</p>"
                   "<p>能拼的话输出 <code>yes</code> 和面积，中间一个空格，面积保留两位小数；"
                   "拼不成只输出 <code>no</code>。</p>"
                   "<p>面积用海伦公式：<code>s = (a + b + c) / 2</code>，"
                   "<code>area = sqrt(s * (s - a) * (s - b) * (s - c))</code>。</p>"
                   "<p>像 <code>1 2 3</code> 这种两边之和刚好等于第三边的是退化情况，拼不成，要输出 <code>no</code>。</p>",
         idea="<p>先把三边 <code>sorted</code> 一下，只比一次 <code>a + b &gt; c</code> 就够了，"
              "比写三个 <code>and</code> 省心事少。判的是严格大于，写成 <code>&gt;=</code> "
              "就会把 <code>1 2 3</code> 误判成能拼。</p>"
              "<p>开平方用 <code>math.sqrt</code>，输出用 <code>format(area, '.2f')</code>。"
              "小数会有丁点误差，公式里再套一层 <code>max(0.0, ...)</code> 兜底，"
              "免得根号下出现极小的负数报错。</p>"),
]

FILL_META = []

# ---------------------------------------------------------------- 输入数据
_POOL_34 = ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "0123456789 .,!?;:()-_+*/=#%&")
_POOL_36 = ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
_POOL_44 = "abcdefghijklmnopqrstuvwxyz0123456789"


def _r(n):
    """固定种子的随机源：每次构建出来的输入完全一致。"""
    return random.Random(SEED + 977 * n)


def _words(rnd, count, lo=1, hi=6):
    return " ".join("".join(rnd.choice(_POOL_36[:26]) for _ in range(rnd.randint(lo, hi)))
                    for _ in range(count))


def _rand_text(rnd, length, pool=_POOL_34):
    """随机一行文本，保证行尾不是空格（输入格式里写了行尾没有多余空格）。"""
    s = "".join(rnd.choice(pool) for _ in range(length))
    while s and s[-1] == " ":
        s = s[:-1] + rnd.choice(_POOL_36)
    return s


def prog_cases():
    cs = {}

    # p28 四则运算套餐
    r = _r(1)
    x1, y1 = r.randint(10 ** 8, 10 ** 9), r.randint(1, 10 ** 9)
    cs["p28_arithmetic_bundle"] = [
        ("样例 17 和 5", "17 5\n"),
        ("最小 1 和 1", "1 1\n"),
        ("a 小于 b，商是 0", "3 10\n"),
        ("正好整除，余数是 0", "8 8\n"),
        ("差是负数", "12 45\n"),
        ("上界 10^9 相乘", "1000000000 1000000000\n"),
        ("随机大数", "{} {}\n".format(x1, y1)),
    ]

    # p29 各位数字之和
    r = _r(2)
    mid29 = "\n".join(["20"] + [str(r.randint(-10 ** 9, 10 ** 9)) for _ in range(20)]) + "\n"
    r = _r(3)
    t29 = 50000
    big29 = "\n".join([str(t29)] + [str(r.randint(-10 ** 9, 10 ** 9)) for _ in range(t29)]) + "\n"
    cs["p29_digit_sum"] = [
        ("样例 四组", "4\n123\n9999\n0\n-321\n"),
        ("最小 T=1", "1\n7\n"),
        ("只有 0", "1\n0\n"),
        ("负数边界", "3\n-1000000000\n-999999999\n-1\n"),
        ("正数上界", "3\n1000000000\n999999999\n1\n"),
        ("随机 20 组", mid29),
        ("较大规模 T=50000", big29),
    ]

    # p30 秒数换算
    r = _r(4)
    cs["p30_seconds_convert"] = [
        ("样例 100000 秒", "100000\n"),
        ("最小 0 秒", "0\n"),
        ("不足一分钟", "59\n"),
        ("正好一分钟", "60\n"),
        ("差一秒到整点", "3599\n"),
        ("差一秒到整天", "86399\n"),
        ("正好一整天", "86400\n"),
        ("随机中间值", "{}\n".format(r.randint(0, 999999999))),
        ("上界 10^9 秒", "1000000000\n"),
    ]

    # p31 BMI 判定
    r = _r(5)
    h31 = "{:.2f}".format(r.uniform(1.40, 2.00))
    w31 = "{:.1f}".format(r.uniform(35, 140))
    cs["p31_bmi_level"] = [
        ("样例 1.75 米 70 公斤", "1.75 70\n"),
        ("BMI 正好 18.5", "2.0 74\n"),
        ("刚低于 18.5", "2.0 73.9\n"),
        ("BMI 正好 24", "1.0 24\n"),
        ("刚低于 24", "1.0 23.9\n"),
        ("BMI 正好 28", "1.0 28\n"),
        ("大体重一定肥胖", "1.6 200\n"),
        ("随机身高体重", "{} {}\n".format(h31, w31)),
    ]

    # p32 成绩等级与平均分
    r = _r(6)
    mid32 = "1000\n" + " ".join(str(r.randint(0, 100)) for _ in range(1000)) + "\n"
    r = _r(7)
    n32 = 100000
    big32 = "{}\n".format(n32) + " ".join(str(r.randint(0, 100)) for _ in range(n32)) + "\n"
    cs["p32_score_grades"] = [
        ("样例 5 人", "5\n95 82 60 55 90\n"),
        ("最小 n=1 满分", "1\n100\n"),
        ("最小 n=1 零分", "1\n0\n"),
        ("四档边界", "8\n0 59 60 79 80 89 90 91\n"),
        ("全是不及格", "3\n12 45 59\n"),
        ("平均分要补零", "2\n77 80\n"),
        ("随机 1000 人", mid32),
        ("较大规模 n=100000", big32),
    ]

    # p33 闰年与星期
    r = _r(8)
    base33 = datetime.date(1900, 1, 1)
    span33 = (datetime.date(2100, 12, 31) - base33).days
    d33 = base33 + datetime.timedelta(days=r.randint(0, span33))
    cs["p33_leap_weekday"] = [
        ("样例 2026-10-01", "2026 10 1\n"),
        ("年初边界 1900-01-01", "1900 1 1\n"),
        ("百年不闰 1900-03-01", "1900 3 1\n"),
        ("四百年才闰 2000-01-01", "2000 1 1\n"),
        ("闰年 2 月 29 日", "2024 2 29\n"),
        ("平年 2 月 28 日", "2023 2 28\n"),
        ("年末边界 2100-12-31", "2100 12 31\n"),
        ("随机日期", "{} {} {}\n".format(d33.year, d33.month, d33.day)),
    ]

    # p34 字符分类统计
    r = _r(9)
    cs["p34_char_classify"] = [
        ("样例 中英数混合", "Hello World 123!\n"),
        ("单个字母", "a\n"),
        ("单个数字", "0\n"),
        ("单个空格", " \n"),
        ("只有空格和标点", "  !!!\n"),
        ("含汉字算其它", "你好 abc 12\n"),
        ("随机 200 字符", _rand_text(r, 200) + "\n"),
        ("较大规模 100000 字符", _rand_text(r, 100000) + "\n"),
    ]

    # p35 单词倒序
    r = _r(10)
    cs["p35_reverse_words"] = [
        ("样例 三个单词", "Hello world python\n"),
        ("只有一个单词", "abc\n"),
        ("连续多个空格与首尾空格", "  a  b   c \n"),
        ("含标点", "python is great!\n"),
        ("制表符也算分隔", "a\tb c\n"),
        ("随机 100 个单词", _words(r, 100) + "\n"),
        ("随机 1000 个单词", _words(r, 1000) + "\n"),
        ("较大规模 50000 个单词", _words(r, 50000, 1, 5) + "\n"),
    ]

    # p36 回文判断
    r = _r(11)
    half36 = _rand_text(r, 50000, _POOL_36)
    palin36 = half36 + half36[::-1]
    noise36 = list(_rand_text(r, 100000, _POOL_36))
    noise36[10], noise36[-11] = "a", "b"       # 对称位置放不同字符，保证不是回文
    cs["p36_palindrome_check"] = [
        ("样例 Level", "Level\n"),
        ("最小 单字符", "x\n"),
        ("偶数长度回文", "abCCba\n"),
        ("忽略大小写", "AbBa\n"),
        ("差一点就不是", "abc\n"),
        ("空格也参与比较", "a b a\n"),
        ("较大规模 100000 长回文", palin36 + "\n"),
        ("较大规模 100000 长非回文", "".join(noise36) + "\n"),
    ]

    # p37 最大最小与极差
    r = _r(12)
    mid37 = "1000\n" + " ".join(str(r.randint(-99999, 99999)) for _ in range(1000)) + "\n"
    r = _r(13)
    n37 = 100000
    big37 = "{}\n".format(n37) + " ".join(str(r.randint(-99999, 99999)) for _ in range(n37)) + "\n"
    cs["p37_max_min_range"] = [
        ("样例 5 个数", "5\n3 -1 7 7 2\n"),
        ("最小 n=1 负数", "1\n-5\n"),
        ("最小 n=1 是 0", "1\n0\n"),
        ("全部相同", "4\n0 0 0 0\n"),
        ("只有两个数 前大后小", "2\n10 -10\n"),
        ("极值边界", "3\n-1000000000 123 1000000000\n"),
        ("随机 1000 个", mid37),
        ("较大规模 n=100000", big37),
    ]

    # p38 计数筛选
    r = _r(14)
    mid38 = "1000 7\n" + " ".join(str(r.randint(-99999, 99999)) for _ in range(1000)) + "\n"
    r = _r(15)
    n38 = 100000
    big38 = "{} {}\n".format(n38, r.randint(-50000, 50000)) + \
            " ".join(str(r.randint(-99999, 99999)) for _ in range(n38)) + "\n"
    cs["p38_count_filter"] = [
        ("样例 x=10", "6 10\n3 12 10 8 25 -1\n"),
        ("最小 n=1 命中", "1 5\n5\n"),
        ("最小 n=1 不命中", "1 5\n4\n"),
        ("一个都不命中", "3 100\n1 2 3\n"),
        ("全部命中", "4 0\n1 2 3 4\n"),
        ("门槛是负数 且有 0", "5 -3\n-5 -3 -1 0 3\n"),
        ("随机 1000 个", mid38),
        ("较大规模 n=100000", big38),
    ]

    # p39 九九乘法表
    cs["p39_mult_table"] = [
        ("样例 n=2", "2\n"),
        ("最小 n=1", "1\n"),
        ("n=3", "3\n"),
        ("n=4", "4\n"),
        ("n=6", "6\n"),
        ("n=8", "8\n"),
        ("最大 n=9", "9\n"),
    ]

    # p40 素数判定
    r = _r(16)
    mid40 = "20\n" + " ".join(str(r.randint(1, 10 ** 6)) for _ in range(20)) + "\n"
    r = _r(17)
    big40 = "200\n" + " ".join(str(r.randint(10 ** 8, 2 * 10 ** 9)) for _ in range(200)) + "\n"
    cs["p40_prime_check"] = [
        ("样例 2 3 4 1", "4\n2 3 4 1\n"),
        ("最小 n=1 值是 1", "1\n1\n"),
        ("最小素数 2", "1\n2\n"),
        ("1 到 8 挨个判", "8\n1 2 3 4 5 6 7 8\n"),
        ("平方数与大合数", "4\n121 169 1000000000 999999937\n"),
        ("大素数与上界", "3\n1000000007 999999929 2000000000\n"),
        ("随机 20 个", mid40),
        ("较大规模 n=200 大数", big40),
    ]

    # p41 斐波那契前 n 项
    cs["p41_fib_list"] = [
        ("样例 n=6", "6\n"),
        ("最小 n=1", "1\n"),
        ("n=2 两项都是 1", "2\n"),
        ("n=3", "3\n"),
        ("n=10", "10\n"),
        ("n=30", "30\n"),
        ("n=60", "60\n"),
        ("最大 n=90", "90\n"),
    ]

    # p42 手写冒泡排序
    r = _r(18)
    mid42 = "500\n" + " ".join(str(r.randint(-99999, 99999)) for _ in range(500)) + "\n"
    worst42 = "1000\n" + " ".join(str(v) for v in range(1000, 0, -1)) + "\n"
    cs["p42_bubble_sort"] = [
        ("样例 6 个数", "6\n5 2 9 1 5 6\n"),
        ("最小 n=1", "1\n7\n"),
        ("n=2 已经有序", "2\n1 2\n"),
        ("n=2 需要交换", "2\n2 1\n"),
        ("全部相同", "4\n2 2 2 2\n"),
        ("含 0 和负数", "7\n0 -3 5 -1 0 8 -100\n"),
        ("随机 500 个", mid42),
        ("较大规模 n=1000 完全逆序", worst42),
    ]

    # p43 去重保序
    r = _r(19)
    mid43 = "1000\n" + " ".join(str(r.randint(-50, 50)) for _ in range(1000)) + "\n"
    perm43 = list(range(100000))
    r.shuffle(perm43)
    big43 = "100000\n" + " ".join(map(str, perm43)) + "\n"
    cs["p43_dedupe_order"] = [
        ("样例 8 个数", "8\n1 3 2 3 1 5 2 7\n"),
        ("最小 n=1", "1\n42\n"),
        ("全部相同", "5\n7 7 7 7 7\n"),
        ("一个都不重复", "4\n3 1 2 5\n"),
        ("含 0 和负数", "6\n0 -1 0 -1 -2 3\n"),
        ("两种数来回出现", "20\n" + " ".join(str(1 if i % 2 == 0 else -1) for i in range(20)) + "\n"),
        ("随机 1000 个值域很小", mid43),
        ("较大规模 n=100000 全不重复", big43),
    ]

    # p44 出现次数最多的 k 个字符
    r = _r(20)
    mid44 = _rand_text(r, 1000, _POOL_44) + "\n5\n"
    big44 = _rand_text(r, 100000, _POOL_44) + "\n26\n"
    cs["p44_char_topk"] = [
        ("样例 banana", "banana\n3\n"),
        ("最小 长度 1", "a\n1\n"),
        ("只有一种字符", "aaaa\n1\n"),
        ("k 等于种类数", "abcabc\n3\n"),
        ("次数并列按字符排", "ccbbaa\n2\n"),
        ("数字也算字符", "a1a11\n2\n"),
        ("随机 1000 长 取 5 个", mid44),
        ("较大规模 100000 长 取 26 个", big44),
    ]

    # p45 任意进制转换
    r = _r(21)
    n45, b45 = r.randint(-10 ** 15, 10 ** 15), r.randint(2, 16)
    cs["p45_base_convert"] = [
        ("样例 2026 转 16 进制", "2026 16\n"),
        ("0 转任何进制都是 0", "0 8\n"),
        ("1 转 2 进制", "1 2\n"),
        ("正好是基数幂", "4096 16\n"),
        ("负数 16 进制", "-255 16\n"),
        ("负数 2 进制全是 1", "-1023 2\n"),
        ("随机大数与随机基数", "{} {}\n".format(n45, b45)),
        ("上界 10^15 转 2 进制", "1000000000000000 2\n"),
    ]

    # p46 区间内的水仙花数
    cs["p46_narcissistic"] = [
        ("样例整个三位数范围", "100 999\n"),
        ("最小 区间在三位数之前", "1 99\n"),
        ("单点命中 lo=hi=153", "153 153\n"),
        ("单点不命中", "152 152\n"),
        ("刚好差一个到 153", "100 152\n"),
        ("含头一个水仙花数", "100 153\n"),
        ("中段三个", "370 407\n"),
        ("末尾一个都没有", "408 999\n"),
    ]

    # p47 三角形判定与面积
    r = _r(23)
    e47 = (r.randint(1, 1000), r.randint(1, 1000), r.randint(1, 1000))
    cs["p47_triangle_area"] = [
        ("样例 直角三角形", "3 4 5\n"),
        ("退化 两边和等于第三边", "1 2 3\n"),
        ("最小 等边", "1 1 1\n"),
        ("拼不成 有一条太长", "1 2 10\n"),
        ("细长但能拼", "1 100 100\n"),
        ("小数边", "1.5 2.5 3.5\n"),
        ("上界等边 1000", "1000 1000 1000\n"),
        ("随机三边", "{} {} {}\n".format(*e47)),
    ]

    return cs
