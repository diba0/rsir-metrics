import os
import pandas as pd
import numpy as np

def process_performance_csv_files(performance_dir):
    filename_list = []
    for filename in os.listdir(performance_dir):
        if filename.endswith('.csv'):
            filepath = os.path.join(performance_dir, filename)
            df = pd.read_csv(filepath)
            # 检查倒数第三列是否存在
            if len(df.columns) >= 3:
                third_last_col = df.columns[-3]
                # 检查倒数第三列中是否有值大于1000
                if (df[third_last_col] > 1000).any():
                    filename_list.append(filename)
            # 可以在这里添加更多处理逻辑

    return filename_list

def extract_number_from_filename(filename):
    """从文件名中提取下划线前的数字用于排序"""
    try:
        # 提取下划线前的数字部分
        number_str = filename.split('_')[0]
        return int(number_str)
    except (ValueError, IndexError):
        # 如果无法提取数字，返回一个很大的数，使其排在后面
        return float('inf')

def group_files_by_number_gap(files, max_gap=1):
    """将文件按照数字间隔分组，间隔不超过max_gap的文件归为一组"""
    if not files:
        return []
    
    groups = []
    current_group = [files[0]]
    
    for i in range(1, len(files)):
        current_num = extract_number_from_filename(files[i])
        prev_num = extract_number_from_filename(files[i-1])
        
        # 如果当前文件和前一个文件的数字差超过max_gap，开始新的分组
        if current_num - prev_num > max_gap:
            groups.append(current_group)
            current_group = [files[i]]
        else:
            current_group.append(files[i])
    
    # 添加最后一组
    if current_group:
        groups.append(current_group)
    
    return groups

def calculate_group_averages(performance_dir, group, start_num, end_num):
    """计算指定范围内所有文件的最后三列的平均值"""
    all_last_three_cols = []
    
    # 遍历范围内的所有数字
    for num in range(start_num, end_num + 1):
        filename = f"{num}_performance.csv"
        filepath = os.path.join(performance_dir, filename)
        
        # 检查文件是否存在
        if os.path.exists(filepath):
            try:
                df = pd.read_csv(filepath)
                # 获取最后三列的数据
                if len(df.columns) >= 3:
                    last_three_cols = df.iloc[:, -3:].values
                    all_last_three_cols.extend(last_three_cols)
            except Exception as e:
                print(f"  警告：无法读取文件 {filename}: {e}")
    
    # 计算平均值
    if all_last_three_cols:
        all_last_three_cols = pd.DataFrame(all_last_three_cols)
        averages = all_last_three_cols.mean()
        return averages.tolist()
    else:
        return [0, 0, 0]

def get_group_averages(performance_folder):
        """
        输入 performance 文件夹路径，输出各组的最后三列平均值列表
        """
        if not os.path.exists(performance_folder):
            print(f"performance 文件夹不存在: {performance_folder}")
            return []

        valid_files = process_performance_csv_files(performance_folder)
        valid_files.sort(key=extract_number_from_filename)
        file_groups = group_files_by_number_gap(valid_files, max_gap=1)
        # print(file_groups)

        group_averages = []
        for group in file_groups:
            first_file = group[0]
            last_file = group[-1]
            first_num = extract_number_from_filename(first_file)
            last_num = extract_number_from_filename(last_file)
            
            if last_num - first_num < 3:
                # print(f"  跳过组 {group}，因为范围小于3")
                continue
            # print(f"  处理组 {group}，范围: {first_num} 到 {last_num}")
            averages = calculate_group_averages(performance_folder, group, first_num + 1, last_num - 1)
            averages[0] *= 2 / 1000 * 100
            group_averages.append(averages)
        return group_averages


if __name__ == "__main__":
    hops_performance_folder = os.path.join(os.path.dirname(__file__), 'hops/performance')
    loss_performance_folder = os.path.join(os.path.dirname(__file__), 'loss/performance')
    delay_performance_folder = os.path.join(os.path.dirname(__file__), 'delay/performance')
    bandwidtha_performance_folder = os.path.join(os.path.dirname(__file__), 'bandwidtha/performance')
    ql_performance_folder = os.path.join(os.path.dirname(__file__), 'q-learning/performance')
    qlwf_performance_folder = os.path.join(os.path.dirname(__file__), 'q-learning-with-flow/performance')

    hops_group_averages = get_group_averages(hops_performance_folder)
    loss_group_averages = get_group_averages(loss_performance_folder)
    delay_group_averages = get_group_averages(delay_performance_folder)
    bandwidtha_group_averages = get_group_averages(bandwidtha_performance_folder)
    ql_group_averages = get_group_averages(ql_performance_folder)
    qlwf_group_averages = get_group_averages(qlwf_performance_folder)

    print(f"\n len(hops_group_averages): {len(hops_group_averages)}")
    print("\nhops所有组的平均值:")
    for avg in hops_group_averages:
        print(f"  {avg[0]:.6f}, {avg[1]:.6f}, {avg[2]:.6f}")

    print(f"\n len(loss_group_averages): {len(loss_group_averages)}")
    print("\nloss所有组的平均值:")
    for avg in loss_group_averages:
        print(f"  {avg[0]:.6f}, {avg[1]:.6f}, {avg[2]:.6f}")

    print(f"\n len(delay_group_averages): {len(delay_group_averages)}")
    print("\ndelay所有组的平均值:") 
    for avg in delay_group_averages:
        print(f"  {avg[0]:.6f}, {avg[1]:.6f}, {avg[2]:.6f}")
    
    print(f"\n len(bandwidtha_group_averages): {len(bandwidtha_group_averages)}")
    print("\nbandwidtha所有组的平均值:")
    for avg in bandwidtha_group_averages:
        print(f"  {avg[0]:.6f}, {avg[1]:.6f}, {avg[2]:.6f}")
    
    print(f"\n len(ql_group_averages): {len(ql_group_averages)}")
    print("\nql所有组的平均值:")
    for avg in ql_group_averages:
        print(f"  {avg[0]:.6f}, {avg[1]:.6f}, {avg[2]:.6f}")

    print(f"\n len(qlwf_group_averages): {len(qlwf_group_averages)}")
    print("\nqlwf所有组的平均值:")
    for avg in qlwf_group_averages:
        print(f"  {avg[0]:.6f}, {avg[1]:.6f}, {avg[2]:.6f}")
    
    # 绘制三个柱形图，每个组的每一个平均值作为一个图，第一个图绘制三组的第一个平均值，依次类推
    import matplotlib.pyplot as plt

    # 准备数据
    group_labels = ['0:00', '1:00', '3:00', '5:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '15:00', '17:00', '19:00', '21:00', '23:00']

    # 填充数据，确保长度一致
    def pad_list(lst, length):
        return lst + [[0,0,0]] * (length - len(lst))

    max_len = max(len(hops_group_averages), len(loss_group_averages), len(delay_group_averages), len(bandwidtha_group_averages), len(ql_group_averages))
    hops_group_averages = pad_list(hops_group_averages, max_len)
    loss_group_averages = pad_list(loss_group_averages, max_len)
    delay_group_averages = pad_list(delay_group_averages, max_len)
    bandwidtha_group_averages = pad_list(bandwidtha_group_averages, max_len)
    ql_group_averages = pad_list(ql_group_averages, max_len)
    qlwf_group_averages = pad_list(qlwf_group_averages, max_len)

    # 转置数据，方便绘图
    hops_vals = np.array(hops_group_averages).T
    loss_vals = np.array(loss_group_averages).T
    delay_vals = np.array(delay_group_averages).T
    bandwidtha_vals = np.array(bandwidtha_group_averages).T
    ql_vals = np.array(ql_group_averages).T
    qlwf_vals = np.array(qlwf_group_averages).T

    performance_names = ['Average of mean link throughput(Mbps)', 'Delay(ms)', 'loss(%)']
    all_vals = [hops_vals, loss_vals, delay_vals, bandwidtha_vals, ql_vals, qlwf_vals]
    titles = ['hops', 'loss', 'delay', 'bandwidth', 'ql', 'qlwf']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#0ab1cc', '#9467bd', "#d7ee0592"]

    # 设置每个图的ylabel为对应的performance_names
    for i in range(3):
        plt.figure(figsize=(10, 5))
        x = np.arange(max_len)
        width = 0.1
        plt.bar(x - 2 * width, hops_vals[i], width, label='hops', color=colors[0])
        plt.bar(x - width, loss_vals[i], width, label='loss', color=colors[1])
        plt.bar(x, delay_vals[i], width, label='delay', color=colors[2])
        plt.bar(x + width, bandwidtha_vals[i], width, label='bandwidtha', color=colors[3])
        plt.bar(x + 2 * width, ql_vals[i], width, label='ql', color=colors[4])
        plt.bar(x + 3 * width, qlwf_vals[i], width, label='qlwf', color=colors[5])
        plt.xlabel('Hour')
        plt.ylabel(f'{performance_names[i]}')
        plt.xticks(x, group_labels)
        plt.legend()
        plt.tight_layout()
        plt.show()


    