# 数学建模学习日志（2025年6月30日）

## 今日学习目标

- 了解线性规划的基本原理及其在实际问题中的应用
- 掌握MATLAB中使用 `linprog` 函数进行求解的方法
- 学习案例：最优资源分配问题
- 阅读文献：交通流建模基础

---

## 一、线性规划基础回顾

### 线性规划定义

线性规划（Linear Programming，LP）是指在约束条件为线性不等式的情况下，求解线性目标函数最大值或最小值的问题。

标准形式如下：

$$
\text{Maximize } \mathbf{c}^T \mathbf{x} \\
\text{Subject to } A \mathbf{x} \leq \mathbf{b}, \quad \mathbf{x} \geq 0
$$

- $\mathbf{c}$ 是目标系数向量
- $\mathbf{x}$ 是决策变量向量
- $A$ 是约束系数矩阵
- $\mathbf{b}$ 是资源约束向量

---

## 二、MATLAB中使用`linprog`函数

今天学习了使用 MATLAB 中的 `linprog` 函数解决线性规划问题。基本语法如下：

```matlab
[x, fval] = linprog(f, A, b, Aeq, beq, lb, ub);
