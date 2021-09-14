import jieba
import pandas as pd
from pyecharts.charts import Bar
from pyecharts.commons.utils import JsCode
from stylecloud import stylecloud
from pyecharts import options as opts

from 可视化项目.Python中秋月饼销量分析.月饼销量分析 import df

stop_words = [line.strip('\n') for line in
              open('D:/Python数据分析/可视化项目/Python中秋月饼销量分析/stop_words.txt', 'r', encoding='utf-8').readlines()]
stop_words.extend(['logo', '10', '100', '200g', '100g', '140g', '130g', '月饼', '礼盒','礼盒装'])
contents = df['商品名称'].apply(lambda x : ([i for i in jieba.cut(x,cut_all=False) if i not in stop_words]))
content_list = []
tmp = [content_list.extend(i) for i in contents.values.tolist()]

roles=["冰皮","冰淇","蛋黄莲蓉","豆沙","黑芝麻","火腿","椒盐","榴莲","玫瑰","流心","奶酪","牛肉","水果","酥皮","五仁","椰蓉","枣蓉","桃仁"]
content=''.join([str(i) for i in list(df['商品名称'])])
roles_num=[]
for role in roles:
    count=content.count(role)
    roles_num.append((role,count))
roles_num=pd.DataFrame(roles_num)
roles_num.columns=['口味','商家']
#print(roles_num)
# 线性渐变
color_js = """new echarts.graphic.LinearGradient(0, 1, 0, 0,
    [{offset: 0, color: '#FFFFFF'}, {offset: 1, color: '#ed1941'}], false)"""

roles_num=roles_num.sort_values(by='商家',ascending=False)
roles_num=roles_num.reset_index(drop=True)
bar4 = (
        Bar()
        .add_xaxis(list(roles_num['口味']))
        .add_yaxis('频次', list(roles_num['商家']),itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_js)))
        .set_global_opts(
            title_opts=dict(
                text='口味分布',
                left='center',
                top='5%',
                textStyle=dict(color='#DC143C')
            ),
            legend_opts=opts.LegendOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
            yaxis_opts=opts.AxisOpts(name="频次",name_location='middle',name_gap=50,name_textstyle_opts=opts.TextStyleOpts(font_size=16)))

    )
#print(bar4.render())

stylecloud.gen_stylecloud(
    text=' '.join(content_list),
    font_path=r'/home/mw/input/202109144150/STXINWEI.TTF',
    # palette='cartocolors.qualitative.Bold_5',# 设置配色方案
    # icon_name='fas fa-gift', # 设置蒙版方案
    output_name='中秋.png',
    )


from PIL import Image
Image.open("D:/Python数据分析/可视化项目/Python中秋月饼销量分析/中秋.png")


