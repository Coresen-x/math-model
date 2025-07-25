# 时间序列分析指南

## 目录
1. [基本概念](#基本概念)
2. [预处理方法](#预处理方法)
3. [常用模型](#常用模型)
4. [Python代码示例](#python代码示例)
5. [评估指标](#评估指标)
6. [参考资料](#参考资料)

## 基本概念
<a name="基本概念"></a>

时间序列是按时间顺序排列的一组观测值，通常具有以下特性：
- **趋势性**：长期变化的趋势
- **季节性**：固定周期内的重复模式
- **周期性**：非固定周期的波动
- **随机性**：不可预测的噪声

## 预处理方法
<a name="预处理方法"></a>

### 1. 平稳性处理
- **差分法**：消除趋势和季节性
  ```python
  # 一阶差分
  diff = ts.diff().dropna()