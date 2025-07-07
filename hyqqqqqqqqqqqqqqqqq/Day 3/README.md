## 割平面算法

### 基本思想
- 如果松弛问题$(P_0)$无解，则$(P)$无解；  
- 如果$(P_0)$的最优解为整数向量，则也是$(P)$的最优解；  
- 如果$(P_0)$的解含有非整数分量，则对$(P_0)$增加割平面条件：即对$(P_0)$增加一个线性约束，将$(P_0)$的可行区域割掉一块，使得非整数解恰好在割掉的一块中，但又没有割掉原问题$(P)$的可行解，得到问题$(P_1)$，重复上述的过程。

### 步骤详解

#### 1. 基本可行解与非整数分量
假设 $(P_0)$ 的最优解为 $x^*$，若存在非整数分量 $x_j^* \notin \mathbb{Z}$，则对应约束方程可表示为：
$$
x_j + \sum_{k \in N} a_{jk} x_k = b_j
$$
其中：
- $N$ 为非基变量索引集
- $a_{jk}$ 为约束系数
- $b_j$ 为约束常数项

#### 2. 系数拆分与小数部分
将系数 $a_{jk}$ 和常数项 $b_j$ 拆分为整数部分和小数部分：
$$
\begin{aligned}
a_{jk} &= \lfloor a_{jk} \rfloor + f_{jk}, \quad 0 \leq f_{jk} < 1 \\
b_j &= \lfloor b_j \rfloor + f_j, \quad 0 \leq f_j < 1
\end{aligned}
$$
其中 $\lfloor \cdot \rfloor$ 表示下取整函数。

#### 3. 割平面约束推导
代入拆分结果得：
$$
x_j + \sum_{k \in N} \lfloor a_{jk} \rfloor x_k + \sum_{k \in N} f_{jk} x_k = \lfloor b_j \rfloor + f_j
$$
移项整理为：
$$
x_j + \sum_{k \in N} \lfloor a_{jk} \rfloor x_k - \lfloor b_j \rfloor = f_j - \sum_{k \in N} f_{jk} x_k
$$

#### 4. 割平面条件分析
由于左侧为整数，右侧必须满足：
$$
f_j - \sum_{k \in N} f_{jk} x_k \in \mathbb{Z}
$$
结合非负约束 $x_k \geq 0$，得到割平面约束：
$$
\sum_{k \in N} f_{jk} x_k \geq f_j
$$

#### 5. 加入割平面后的新问题
将割平面约束加入原问题 $(P_0)$ 得到 $(P_1)$：
$$
\begin{aligned}
\min \ & c^T x \\
\text{s.t.} \ & Ax = b \\
& \sum_{k \in N} f_{jk} x_k \geq f_j \\
& x \geq 0
\end{aligned}
$$

flowchart TD
    A[开始] --> B[初始化并赋值]
    B --> C{初始解是否为最优解}
    C -->|否| D[用单纯形法求最优解]
    D --> E{是否找到最优解}
    E -->|否| F[输出“找不到最优解”]
    E -->|是| G{是否为整数解}
    C -->|是| G
    G -->|是| H[输出最优整数解]
    G -->|否| I[构建切割方程并形成新的约束矩阵]
    I --> J[用对偶单纯形法求出最优解]
    J --> G
    F --> K[程序结束]
    H --> K

    