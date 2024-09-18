import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import yfinance as yf

def calculate_and_plot_ahr999(symbol, start_date, title):
    # 下载历史数据
    data = yf.download(symbol, start=start_date, end=datetime.now().strftime('%Y-%m-%d'))

    # 计算200日移动平均线
    data['MA200'] = data['Close'].rolling(window=200).mean()

    # 计算ahr999指标
    data['AHR999'] = (data['Close'] - data['MA200']) / data['MA200']

    # 创建带有双Y轴的交互式图表
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # 添加AHR999指标线
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['AHR999'],
            mode='lines',
            name='AHR999',
            hovertemplate='日期: %{x|%Y-%m-%d}<br>AHR999: %{y:.4f}<extra></extra>'
        ),
        secondary_y=False
    )

    # 添加价格线
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['Close'],
            mode='lines',
            name=f'{title}价格',
            hovertemplate='日期: %{x|%Y-%m-%d}<br>价格: $%{y:,.2f}<extra></extra>'
        ),
        secondary_y=True
    )

    # 添加0线
    fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="0 线", secondary_y=False)

    # 更新布局
    fig.update_layout(
        title=f'{title} AHR999 指标和价格',
        xaxis_title='日期',
        hovermode="x unified",
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1月", step="month", stepmode="backward"),
                    dict(count=6, label="6月", step="month", stepmode="backward"),
                    dict(count=1, label="1年", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )

    # 更新Y轴标题
    fig.update_yaxes(title_text="AHR999 值", secondary_y=False)
    fig.update_yaxes(title_text=f"{title}价格 (USD)", secondary_y=True)

    fig.show()

    # 打印最新的AHR999值、价格和当前日期
    print(f"当前日期: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"最新的{title} AHR999值: {data['AHR999'].iloc[-1]:.4f}")
    print(f"最新的{title}价格: ${data['Close'].iloc[-1]:,.2f}")

# 使用示例：
# 计算并绘制比特币的AHR999指标和价格
calculate_and_plot_ahr999('BTC-USD', '2010-01-01', '比特币')

# 计算并绘制以太坊的AHR999指标和价格
calculate_and_plot_ahr999('ETH-USD', '2015-08-07', '以太坊')
