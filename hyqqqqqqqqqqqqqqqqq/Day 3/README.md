# 割平面法

## 一、核心思想
通过逐步添加**切割平面约束**，将线性松弛问题的非整数解逐次切除，最终得到整数最优解：

```math
\begin{aligned}
&\text{原整数规划问题} \quad (P) \\
&\text{线性松弛问题} \quad (P_0)
\end{aligned}
```

## 二、算法步骤

### 1. 求解初始松弛问题
先求解线性松弛问题$(P_0)$：
```math
\min \ \boldsymbol{c}^T\boldsymbol{x} \quad \text{s.t.} \ \boldsymbol{Ax} \leq \boldsymbol{b}, \ \boldsymbol{x} \geq \boldsymbol{0}
```

### 2. 整数性检验
- ✅ 若$(P_0)$无可行解 → $(P)$无解  
- ✅ 若解$\boldsymbol{x}^*$全为整数 → 即为最优解  
- ❌ 若含非整数分量 → 进入切割步骤

### 3. 生成割平面
对非整数基变量$x_j$对应的约束方程：
```math
x_j + \sum_{k \in N} a_{jk}x_k = b_j
```
进行系数拆分：
```math
\begin{cases}
a_{jk} = \lfloor a_{jk} \rfloor + f_{jk} \\
b_j = \lfloor b_j \rfloor + f_j
\end{cases}
\quad (0 \leq f_{jk}, f_j < 1)
```
得到Gomory割平面：
```math
\sum_{k \in N} f_{jk}x_k \geq f_j
```

### 4. 迭代求解
将割平面加入$(P_0)$形成$(P_1)$，用**对偶单纯形法**求解，重复直到获得整数解

## 三、算法流程图
```mermaid
flowchart TD
    A[开始] --> B[求解LP松弛问题(P₀)]
    B --> C{是否有解?}
    C -->|无解| D[问题无可行解]
    C -->|有解| E{是否全整数?}
    E -->|是| F[输出最优解]
    E -->|否| G[生成割平面约束]
    G --> H[添加约束得新问题(P₁)]
    H --> I[用对偶单纯形法求解]
    I --> E
```

## 四、关键特性
| 性质 | 说明 |
|------|------|
| 收敛性 | 有限步收敛（有理数数据） |
| 切割类型 | 分数割、混合整数割 |
| 计算效率 | 依赖切割平面质量 |

> **注**：实际应用中常与分支定界法结合为**分支切割法**。
