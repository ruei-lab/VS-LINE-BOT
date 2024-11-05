import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.rcParams['axes.unicode_minus'] = False    # 解決負號顯示問題


def read_csv(csv_file_path):
      # 讀取 CSV 文件
    df=pd.read_csv(csv_file_path)

    # 將 rating 分組並計算每個分數的數量
    rating_counts = df.groupby('rating')['id'].count()

    # 將結果轉為列表，準備繪製圓餅圖
    sizes = []
    for i in range(1, 6):
      size = rating_counts.get(i, 0)
      sizes.append(size)  # 統計1~5星的數量

    # 設置圓餅圖的標籤
    labels = ['one', 'two', 'three', 'four', 'five']

    # 繪製圓餅圖
    plt.pie(sizes, labels=labels, autopct='%2.1f%%', startangle=90,shadow=True,pctdistance=0.6)

    # 設置圓餅圖為等比
    plt.axis('equal')

    plt.legend()

    # 計算總數
    total = sum(sizes)

    # 添加圖例，並在圖例中顯示總數
    plt.legend(title=f'total: {total}', loc='upper left',bbox_to_anchor=(0.9, 1),borderaxespad=0.)

    # 顯示圖表
    plt.show()

# 使用 CSV 檔案路徑呼叫 read_csv 函數
read_csv('D:\\datacenterprj\\datacenter\\user_rating.csv')




