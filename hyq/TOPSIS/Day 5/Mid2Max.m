function [posit_x] = Mid2Max(x,best)
% 函数功能：将中间型指标向量x正向化为极大型指标向量posit_x
% 输入：
%   x - 原始中间型指标列向量
%   best - 中间型指标的最优值（越接近此值越优）
% 输出：posit_x - 正向化后的极大型指标列向量
M = max(abs(x - best));  % 计算原始数据与最优值绝对差的最大值，用于归一化
posit_x = 1 - abs(x - best) / M;  % 通过公式将中间型转极大型，值越接近best，posit_x越接近1 
end