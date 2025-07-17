function [posit_x] = Inter2Max(x,a,b)
% 函数功能：将区间型指标向量x正向化为极大型指标向量posit_x
% 输入：
%   x - 原始区间型指标列向量
%   a - 区间型指标的最优区间下界
%   b - 区间型指标的最优区间上界
% 输出：posit_x - 正向化后的极大型指标列向量
r_x = size(x,1);  % 获取x的行数（即指标数据个数）
M = max([a - min(x), max(x) - b]);  % 计算用于归一化的基准值M
posit_x = zeros(r_x,1);  % 初始化正向化结果向量，全0填充
for i = 1:r_x  % 遍历每个指标数据
    if x(i) < a  % 数据小于区间下界，按公式1 - (a - x(i))/M正向化
        posit_x(i) = 1 - (a - x(i))/M;
    elseif x(i) > b  % 数据大于区间上界，按公式1 - (x(i) - b)/M正向化
        posit_x(i) = 1 - (x(i) - b)/M;
    else  % 数据在最优区间内，正向化结果为1
        posit_x(i) = 1;
    end
end
end