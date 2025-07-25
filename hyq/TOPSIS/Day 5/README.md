# TOPSIS | 基本原理

## 模型原理

TOPSIS法是一种理想目标相似性的顺序选优技术，在多目标决策分析中是一种非常有效的方法。它通过归一化后（去量纲化）的数据规范化矩阵，找出多个目标中最优目标和最劣目标（分别用理想归一解化和反理想解表示），分别计算各评价目标与理想解和反理想解的距离，获得各目标与理想解的贴近度，按理想解贴近度的大小排序，以此作为评价目标优劣的依据。贴近度取值在0～1之间，该值愈接近1，表示相应的评价目标越接近最优水平；反之，该值愈接近0，表示评价目标越接近最劣水平。

## 基本步骤

- 将原始矩阵正向化  
  将原始矩阵正向化，就是要将所有的指标类型统一转化为极大型指标。

- 正向矩阵标准化  
  标准化的方法有很多种，其主要目的就是去除量纲的影响，保证不同评价指标在同一数量级，且数据大小排序不变。

- 计算得分并归一化   
  ```math
  S_i = \frac{D_i^+}{D_i^+ + D_i^-} 
  ```
  其中：
 - $S_i$ 为得分
 - $D_i^+$ 为评价对象与理想解（最大值）的距离
 - $D_i^-$ 为评价对象与负理想解（最小值）的距离

 ### 原始矩阵正向化

| 指标名称 | 指标特点 | 例子 |
|---------|---------|------|
| 极大型（效益型）指标 | 越大（多）越好 | 颜值、成绩、GDP增速 |
| 极小型（成本型）指标 | 越小（少）越好 | 脾气、费用、坏品率、污染程度 |
| 中间型指标 | 越接近某个值越好 | 身高、水质量评估时的PH值 |
| 区间型指标 | 落在某个区间最好 | 体重、体温 |



- 将原始矩阵正向化，就是要将所有的指标类型统一转化为极大型指标。



| 指标类型 | 正向化公式 | 说明 |
|---------|------------|------|
| **极大型（效益型）指标** | 无需转换 | 本身已是越大越好 |
| **极小型（成本型）指标** | $\hat{x} = max - x$ | $max$为指标最大值，$x$为原始值 |
| **中间型指标** | $M = \max\|x_i - x_{best}\|$<br>$\hat{x}_i = 1 - \frac{\|x_i - x_{best}\|}{M}$ | $x_{best}$为最优值 |
| **区间型指标** | $M = \max\{a-\min x_i, \max x_i-b\}$<br>$\hat{x}_i = \begin{cases}1-\frac{a-x_i}{M}, & x_i<a \\ 1, & a\leq x_i\leq b \\ 1-\frac{x_i-b}{M}, & x_i>b\end{cases}$ | $[a,b]$为最佳区间 |

#### 公式说明：
1. 极小型→极大型：取差值
2. 中间型：基于最优值的距离归一化
3. 区间型：分段线性转换

### 正向化矩阵标准化

- 标准化的目的是消除不同指标量纲的影响。

假设有 $n$ 个要评价的对象，$m$ 个评价指标（已正向化）构成的正向化矩阵如下：

```math
X = 
\begin{bmatrix}
x_{11} & \cdots & x_{1m} \\
\vdots & \ddots & \vdots \\
x_{n1} & \cdots & x_{nm}
\end{bmatrix}
```

### 计算得分并归一化

- 上一步得到标准化矩阵 $Z$

```math
Z = \begin{bmatrix}
z_{11} & z_{12} & z_{13} \\
\vdots & \vdots & \vdots \\
z_{n1} & z_{n2} & z_{n3}
\end{bmatrix}
```
#### 定义极值解
理想解（最大值）：:
```math
Z^+ = (Z_1^+, Z_2^+, ..., Z_m^+) = (\max\{z_{11}, z_{21},...,z_{n1}\}, \max\{z_{12}, z_{22},...,z_{n2}\}, ..., \max\{z_{1m}, z_{2m},...,z_{nm}\})
```
负理想解（最小值）：
```math
Z^- = (Z_1^-, Z_2^-, ..., Z_m^-) = (\min\{z_{11}, z_{21},...,z_{n1}\}, \min\{z_{12}, z_{22},...,z_{n2}\}, ..., \min\{z_{1m}, z_{2m},...,z_{nm}\})
```
#### 距离计算
与理想解的距离：
```math
D_i^+ = \sqrt{\sum_{j=1}^m (Z_j^+ - z_{ij})^2}
```
与负理想解的距离：
```math
D_i^- = \sqrt{\sum_{j=1}^m (Z_j^- - z_{ij})^2}
```
#### 得分计算
未归一化得分：
```math
S_i = \frac{D_i^-}{D_i^+ + D_i^-} \quad (0 \leq S_i \leq 1)
```
百分制归一化：
```math
\overline{S_i} = \frac{S_i}{\sum_{i=1}^n S_i} \times 100
```