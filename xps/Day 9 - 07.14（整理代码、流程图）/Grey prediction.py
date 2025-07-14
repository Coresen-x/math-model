import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.font_manager as fm

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows系统
plt.rcParams['axes.unicode_minus'] = False
plt.ion()  # 交互模式

# 数据准备
data = np.array([174, 179, 183, 189, 207, 234, 220.5, 256, 270, 285])
years = np.arange(1995, 2005)


# 1. 数据预处理
def preprocess_data(data):
    """处理缺失值和异常值"""
    # 用前后均值填充缺失值
    mask = np.isnan(data)
    for i in np.where(mask)[0]:
        prev = data[i - 1] if i > 0 else np.nanmean(data)
        next_val = data[i + 1] if i < len(data) - 1 else np.nanmean(data)
        data[i] = np.nanmean([prev, next_val])

    # 异常值处理（3σ原则）
    mean, std = np.nanmean(data), np.nanstd(data)
    upper = mean + 3 * std
    lower = mean - 3 * std
    data = np.clip(data, lower, upper)
    return data


# 2. 准指数规律检验
def exponential_law_test(data, show_plot=True):
    """准指数规律检验"""
    x1 = np.cumsum(data)
    rho = data[1:] / x1[:-1]  # 光滑比

    n = len(data)
    valid_ratio = np.sum(rho < 0.5) / (n - 1)
    later_valid = np.sum(rho[2:] < 0.5) / max(n - 3, 1)

    print(f"光滑比<0.5的比例: {valid_ratio:.1%} (应>60%)")
    print(f"后{n - 3}期光滑比<0.5的比例: {later_valid:.1%} (应>90%)")

    if show_plot:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        ax1.plot(years, data, 'bo-')
        ax1.set_title('原始数据序列')

        ax2.plot(years[1:], rho, 'rs--')
        ax2.axhline(0.5, color='k', linestyle='--')
        ax2.set_title('光滑比检验')
        plt.tight_layout()
        plt.show(block=False)

    return valid_ratio > 0.6 and later_valid > 0.9


# 3. GM模型实现
class GreyModels:
    @staticmethod
    def traditional_gm11(data, predict_n):
        n = len(data)
        x1 = np.cumsum(data)
        z1 = 0.5 * (x1[1:] + x1[:-1])  # 背景值

        B = np.vstack([-z1, np.ones(n - 1)]).T
        Y = data[1:].reshape(-1, 1)

        # 带正则化的最小二乘
        params = np.linalg.pinv(B.T @ B + 1e-5 * np.eye(2)) @ B.T @ Y
        a, b = params.flatten()

        # 时间响应函数
        x1_hat = (data[0] - b / a) * np.exp(-a * np.arange(n + predict_n)) + b / a
        x0_hat = np.diff(x1_hat, prepend=0)
        x0_hat[0] = data[0]

        return x0_hat[:n], x0_hat[n:]  # 拟合值, 预测值

    @staticmethod
    def new_info_gm11(data, predict_n, alpha=0.3):
        weights = np.linspace(1 - alpha, 1 + alpha, len(data))
        weighted_data = data * weights
        return GreyModels.traditional_gm11(weighted_data, predict_n)

    @staticmethod
    def metabolism_gm11(data, predict_n, decay=0.95):
        history = data.copy()
        predictions = []

        # 先获取完整拟合值
        fitted, _ = GreyModels.traditional_gm11(data, 0)

        # 预测未来值
        for _ in range(predict_n):
            _, pred = GreyModels.traditional_gm11(history, 1)
            predictions.append(pred[-1])
            history = np.append(history[1:], pred[-1]) * np.array(
                [decay ** i for i in range(len(history))][::-1])

        return fitted, np.array(predictions)


# 4. 模型评估
def evaluate_model(actual, predicted):
    """模型精度评估"""
    residuals = actual - predicted
    SSE = np.sum(residuals ** 2)
    MAPE = np.mean(np.abs(residuals / actual)) * 100

    # 后验差检验
    S1 = np.std(actual)
    S2 = np.std(residuals)
    C = S2 / S1  # 后验差比

    P = np.sum(np.abs(residuals - residuals.mean()) < 0.6745 * S1) / len(actual)

    # 精度等级
    grade = "优" if (C < 0.35 and P > 0.95) else \
        "良" if (C < 0.5 and P > 0.8) else \
            "合格" if (C < 0.65 and P > 0.7) else "不合格"

    print(f"  SSE: {SSE:.2f}  MAPE: {MAPE:.2f}%")
    print(f"  后验差比C: {C:.3f}  小误差概率P: {P:.3f} → 精度等级: {grade}")
    return {'SSE': SSE, 'MAPE': MAPE, 'C': C, 'P': P, 'grade': grade}


# 主程序
def main():
    print("=== 长江水质排污量预测 ===")

    # 1. 数据预处理
    clean_data = preprocess_data(data.copy())
    print("\n[1] 数据预处理完成")

    # 2. 准指数规律检验
    print("\n[2] 准指数规律检验:")
    if not exponential_law_test(clean_data):
        print("警告：数据不满足准指数规律，进行对数变换")
        trans_data = np.log(clean_data)
        need_inverse = True
    else:
        trans_data = clean_data
        need_inverse = False

    # 3. 划分训练集(前7年)和测试集(后3年)
    train_size = 7
    train_data, test_data = trans_data[:train_size], trans_data[train_size:]
    print(f"\n[3] 数据划分: 训练集{len(train_data)}年, 测试集{len(test_data)}年")

    # 4. 多模型建模与评估
    models = {
        '传统GM': GreyModels.traditional_gm11,
        '新信息GM': GreyModels.new_info_gm11,
        '新陈代谢GM': GreyModels.metabolism_gm11
    }

    results = {}
    print("\n[4] 模型训练与评估:")
    for name, model in models.items():
        print(f"\n{name}模型:")
        try:
            # 训练阶段
            fitted, _ = model(train_data, len(test_data))

            # 测试阶段（用训练集+1年预测剩余年份）
            _, test_pred = model(trans_data[:train_size + 1], len(test_data) - 1)

            # 结果逆变换
            if need_inverse:
                fitted = np.exp(fitted)
                test_pred = np.exp(test_pred)
                full_pred = np.concatenate([fitted, test_pred])
            else:
                full_pred = np.concatenate([fitted, test_pred])

            # 评估测试集预测效果
            actual_test = clean_data[train_size:]
            results[name] = evaluate_model(actual_test[1:], test_pred)

            # 可视化
            plt.figure()
            plt.plot(years[:train_size], clean_data[:train_size], 'bo-', label='训练数据')
            plt.plot(years[train_size:], clean_data[train_size:], 'go-', label='测试数据')
            plt.plot(years[1:train_size + 1], full_pred[:train_size], 'r--', label='拟合值')
            plt.plot(years[train_size + 1:], test_pred, 'rs--', label='预测值')
            plt.title(f'{name}模型效果')
            plt.legend()
            plt.grid(True)
            plt.show(block=False)

        except Exception as e:
            print(f"  {name}模型出错: {str(e)}")
            results[name] = None

    # 5. 模型优选
    valid_results = {k: v for k, v in results.items() if v is not None}
    if not valid_results:
        raise ValueError("所有模型均失败，请检查数据或模型实现")

    best_model = min(valid_results.items(), key=lambda x: x[1]['SSE'])
    print(f"\n[5] 最优模型: {best_model[0]} (SSE: {best_model[1]['SSE']:.2f})")

    # 6. 最终预测
    final_model = models[best_model[0]]
    _, final_pred = final_model(trans_data, 3)  # 预测未来3年
    if need_inverse:
        final_pred = np.exp(final_pred)

    # 7. 结果输出
    print("\n[6] 最终预测结果:")
    for year, val in zip(range(2005, 2008), final_pred):
        print(f"  {year}年预测排污量: {val:.2f}亿吨")

    print("\n[7] 模型验证报告:")
    print(f"  精度等级: {best_model[1]['grade']}级")
    print("  结论: ", end='')
    if best_model[1]['grade'] in ['优', '良']:
        print("预测结果可靠，可用于决策参考")
    else:
        print("预测结果仅供参考，建议结合其他方法验证")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"程序运行出错: {str(e)}")
    finally:
        plt.ioff()
        plt.show()