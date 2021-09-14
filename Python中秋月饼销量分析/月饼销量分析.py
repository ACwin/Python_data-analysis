import re
import numpy as np
import pandas as pd
from collections import Counter
from pyecharts.charts import Bar
from pyecharts.charts import Map
from pyecharts.charts import Pie
from pyecharts.charts import Grid
from pyecharts.charts import Page
from pyecharts.components import Image
from pyecharts.charts import WordCloud
from pyecharts import options as opts
from pyecharts.globals import SymbolType
from pyecharts.commons.utils import JsCode


#Pandas数据处理

df = pd.read_excel("D:/Python数据分析/可视化项目/Python中秋月饼销量分析/月饼.xlsx")
df.head(10)
#print(df)

#print(df)
#去重

df.drop_duplicates(inplace=True)
#print(df.shape)

#理付款情况字段 付款人数超过10000后会直接用"万"替代，这里我们需要将其恢复
#df[df['付款情况'].str.contains("万")]

# 提取数值
df['num'] = [re.findall(r'(\d+\.{0,1}\d*)', i)[0] for i in df['付款情况']]
df['num'] = df['num'].astype('float')

# 提取单位（万）
df['unit'] = [''.join(re.findall(r'(万)', i)) for i in df['付款情况']]
df['unit'] = df['unit'].apply(lambda x: 10000 if x == '万' else 1)

# 计算销量
df['销量'] = df['num'] * df['unit']
df = df[df['地址'].notna()]
df['省份'] = df['地址'].str.split(' ').apply(lambda x: x[0])

# 删除多余的列
df.drop(['付款情况', 'num', 'unit'], axis=1, inplace=True)

# 重置索引
df = df.reset_index(drop=True)
# 按售价排序
df1 = df.sort_values(by="售价", axis=0, ascending=False)

shop_top10 = df.groupby('商品名称')['销量'].sum().sort_values(ascending=False).head(10)

#基本图表
bar0 = (
    Bar()
        .add_xaxis(shop_top10.index.tolist()[::-1])
        .add_yaxis('sales_num', shop_top10.values.tolist()[::-1])
        .reversal_axis()
        .set_global_opts(title_opts=opts.TitleOpts(title='月饼商品销量Top10'),
                         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)))
        .set_series_opts(label_opts=opts.LabelOpts(position='right'))
)
#print(bar0.render())

# 线性渐变
color_js = """new echarts.graphic.LinearGradient(0, 0, 1, 0,
    [{offset: 0, color: '#008B8B'}, {offset: 1, color: '#FF6347'}], false)"""
color_js = """new echarts.graphic.LinearGradient(0, 0, 1, 0,
    [{offset: 0, color: '#009ad6'}, {offset: 1, color: '#ed1941'}], false)"""

bar1 = (
    Bar()
        .add_xaxis(shop_top10.index.tolist()[::-1])
        .add_yaxis('sales_num', shop_top10.values.tolist()[::-1],
                   itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_js)))
        .reversal_axis()
        .set_global_opts(title_opts=opts.TitleOpts(title='月饼商品销量Top10'),
                         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
                         )
        .set_series_opts(label_opts=opts.LabelOpts(position='right'))
)
# 将图形整体右移
grid = (
    Grid()
        .add(bar1, grid_opts=opts.GridOpts(pos_left='45%', pos_right='10%'))
)
#print(grid.render())

bar2 = (
    Bar(init_opts=opts.InitOpts(
        width='800px', height='600px', ))
        .add_xaxis(shop_top10.index.tolist()[::-1])
        .add_yaxis('', shop_top10.values.tolist()[::-1],
                   category_gap='30%',
                   itemstyle_opts={
                       'normal': {
                           'shadowColor': 'rgba(0, 0, 0, .5)',  # 阴影颜色
                           'shadowBlur': 5,  # 阴影大小
                           'shadowOffsetY': 2,  # Y轴方向阴影偏移
                           'shadowOffsetX': 2,  # x轴方向阴影偏移
                           'borderColor': '#fff'
                       }
                   }
                   )
        .reversal_axis()
        .set_global_opts(
        xaxis_opts=opts.AxisOpts(is_show=False),
        yaxis_opts=opts.AxisOpts(is_show=False,
                                 axisline_opts=opts.AxisLineOpts(is_show=False),
                                 axistick_opts=opts.AxisTickOpts(is_show=False)
                                 ),
        title_opts=opts.TitleOpts(
            title='月饼销量排名TOP10商品',
            pos_left='center',
            pos_top='4%',
            title_textstyle_opts=opts.TextStyleOpts(
                color='#ed1941', font_size=16)
        ),
        visualmap_opts=opts.VisualMapOpts(
            is_show=False,
            max_=10,
            #             range_color=['#FFCC99', '#F08080', '#990000']
            range_color=["#CCD3D9", "#E6B6C2", "#D4587A", "#DC364C"]
        ),
    )
        .set_series_opts(
        itemstyle_opts={
            "normal": {
                "color": JsCode(
                    """new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                offset: 0,
                color: '#ed1941'
            }, {
                offset: 1,
                color: '#009ad6'
            }], false)"""
                ),
                "barBorderRadius": [30, 30, 30, 30],
                "shadowColor": "rgb(0, 160, 221)",
            }
        },
        label_opts=opts.LabelOpts(position="insideLeft",
                                  font_size=12,
                                  vertical_align='middle',
                                  horizontal_align='left',
                                  font_weight='bold',
                                  formatter='{b}: {c}'))
)

#print(bar2.render())

shop_top10 = df.groupby('店铺名称')['销量'].sum().sort_values(ascending=False).head(10)
bar3 = (
    Bar(init_opts=opts.InitOpts(
        width='800px', height='600px', ))
        .add_xaxis(shop_top10.index.tolist())
        .add_yaxis('', shop_top10.values.tolist(),
                   category_gap='30%',
                   )

        .set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
        title_opts=opts.TitleOpts(
            title='月饼销量排名TOP10店铺',
            pos_left='center',
            pos_top='4%',
            title_textstyle_opts=opts.TextStyleOpts(
                color='#ed1941', font_size=16)
        ),
        visualmap_opts=opts.VisualMapOpts(
            is_show=False,
            max_=600000,
            range_color=["#CCD3D9", "#E6B6C2", "#D4587A", "#FF69B4", "#DC364C"]
        ),
    )
)
#print(bar3.render())

# 线性渐变
color_js = """new echarts.graphic.LinearGradient(0, 0, 1, 0,
    [{offset: 0, color: '#009ad6'}, {offset: 1, color: '#ed1941'}], false)"""
province_num = df.groupby('省份')['销量'].sum().sort_values(ascending=False)
map_chart = Map(init_opts=opts.InitOpts(theme='light',
                                        width='800px',
                                        height='600px'))
map_chart.add('',
              [list(z) for z in zip(province_num.index.tolist(), province_num.values.tolist())],
              maptype='china',
              is_map_symbol_show=False,
              itemstyle_opts={
                  'normal': {
                      'shadowColor': 'rgba(0, 0, 0, .5)',  # 阴影颜色
                      'shadowBlur': 5,  # 阴影大小
                      'shadowOffsetY': 0,  # Y轴方向阴影偏移
                      'shadowOffsetX': 0,  # x轴方向阴影偏移
                      'borderColor': '#fff'
                  }
              }
              )
map_chart.set_global_opts(
    visualmap_opts=opts.VisualMapOpts(
        is_show=True,
        is_piecewise=True,
        min_ = 0,
        max_ = 1,
        split_number = 5,
        series_index=0,
        pos_top='70%',
        pos_left='10%',
        range_text=['销量(份)：', ''],
        pieces=[
            {'max':2000000, 'min':200000, 'label':'> 200000', 'color': '#990000'},
            {'max':200000, 'min':100000, 'label':'100000-200000', 'color': '#CD5C5C'},
            {'max':100000, 'min':50000, 'label':'50000-100000', 'color': '#F08080'},
            {'max':50000, 'min':10000, 'label':'10000-50000', 'color': '#FFCC99'},
            {'max':10000, 'min':0, 'label':'0-10000', 'color': '#FFE4E1'},
           ],
    ),
    legend_opts=opts.LegendOpts(is_show=False),
    tooltip_opts=opts.TooltipOpts(
        is_show=True,
        trigger='item',
        formatter='{b}:{c}'
    ),
    title_opts=dict(
        text='全国各地区月饼销量',
        left='center',
        top='5%',
        textStyle=dict(
            color='#DC143C'))
)
#print(map_chart.render())

def price_range(price):
    if price <= 50:
        return '50元以下'
    elif price <= 100:
        return '50-100元'
    elif price <= 500:
        return '100-300元'
    else:
        return '300元以上'


df['price_range'] = df['售价'].apply(lambda x: price_range(x))
price_cut_num = df.groupby('price_range')['销量'].sum()
data_pair = [list(z) for z in zip(price_cut_num.index, price_cut_num.values)]

# 饼图
pie1 = (
    Pie(init_opts=opts.InitOpts(width='750px', height='350px'))
        .add(
        series_name="销量",
        radius=["35%", "50%"],
        data_pair=data_pair,
        label_opts=opts.LabelOpts(formatter='{b}\n占比{d}%'),
    )
        .set_global_opts(
        title_opts=dict(
            text='不同价格区间的月饼销量占比',
            left='center',
            top='5%',
            textStyle=dict(color='#DC143C')),
        legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", pos_top="50%", orient="vertical")
    )
        .set_colors(["#F08080", "#FFCC99", "#DC143C", "#990000"])
)

print(pie1.render())



