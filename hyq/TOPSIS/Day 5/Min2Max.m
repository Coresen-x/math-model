function [posit_x] = Min2Max(x)
% 函数功能：将极小型指标向量x正向化为极大型指标向量posit_x
% 输入：x - 原始极小型指标列向量
% 输出：posit_x - 正向化后的极大型指标列向量
posit_x = max(x) - x;  % 方法1：用最大值差运算正向化（通用，无需x全正）
% posit_x = 1 ./ x;    % 方法2：若x全>0，可用倒数正向化（被注释，按需启用）
end