import pandas as pd
import datetime
from pyecharts import options as opts
from pyecharts.charts import Line, Timeline,Bar,Grid
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Kline
data = pd.read_csv(r"D:/Python数据分析/可视化项目/pyecharts绘制B站从上市至今股价变迁/BILI历史数据.csv")
data.columns = (['date','close','open','high','low','volume','percentage'])
data['date'] = pd.to_datetime(data.date,format="%Y年%m月%d日")
data = data.sort_values(by='date',ascending=True)

symbols = {'TV':"path://M830.577778 227.555556H657.066667l74.903703-70.162963c11.377778-11.377778 11.377778-29.392593 0-39.822223-5.688889-5.688889-13.274074-8.533333-21.807407-8.533333-7.585185 0-15.17037 2.844444-21.807407 8.533333L570.785185 227.555556H456.059259L338.488889 117.57037c-5.688889-5.688889-13.274074-8.533333-21.807408-8.533333-7.585185 0-15.17037 2.844444-21.807407 8.533333-11.377778 11.377778-11.377778 29.392593 0 39.822223L369.777778 227.555556H193.422222C117.57037 227.555556 56.888889 295.822222 56.888889 381.155556v332.8c0 85.333333 60.681481 153.6 136.533333 153.6h42.666667c0 25.6 22.755556 47.407407 50.251852 47.407407s50.251852-20.859259 50.251852-47.407407h353.659259c0 25.6 22.755556 47.407407 50.251852 47.407407s50.251852-20.859259 50.251852-47.407407h38.874074c75.851852 0 136.533333-69.214815 136.533333-153.6V381.155556c0.948148-85.333333-59.733333-153.6-135.585185-153.6zM698.785185 574.577778L425.718519 733.866667c-22.755556 13.274074-41.718519 2.844444-41.718519-24.651852V389.688889c0-26.548148 18.962963-37.925926 41.718519-24.651852l273.066666 160.237037c22.755556 14.222222 22.755556 35.081481 0 49.303704z"}
color0 = ['#FF76A2','#24ACE6']
color_js0 = """new echarts.graphic.LinearGradient(0, 1, 0, 0,
    [{offset: 0, color: '#FFC0CB'}, {offset: 1, color: '#ed1941'}], false)"""
color_js1 = """new echarts.graphic.LinearGradient(0, 1, 0, 0,
    [{offset: 0, color: '#FFFFFF'}, {offset: 1, color: '#009ad6'}], false)"""

tl = Timeline()
for i in range(0,len(data)):
    coordy_high = list(data['high'])[i]
    coordx = list(data['date'])[i]
    coordy_low = list(data['low'])[i]
    x_max = list(data['date'])[i]+datetime.timedelta(days=70)
    y_max = int(max(list(data['high'])[0:i+1]))+3
    title_date = list(data['date'])[i].strftime('%Y-%m-%d')
    c = (
        Line(
            init_opts=opts.InitOpts(
            theme='dark',
            #设置动画
            animation_opts=opts.AnimationOpts(animation_delay_update=800),#(animation_delay=1000, animation_easing="elasticOut"),
            #设置宽度、高度
            width='1500px',
            height='900px', )
        )
        .add_xaxis(list(data['date'])[0:i])
        .add_yaxis(
            series_name="",
            y_axis=list(data['high'])[0:i], is_smooth=True,is_symbol_show=False,
            linestyle_opts={
                   'normal': {
                       'width': 3,
                       'shadowColor': 'rgba(0, 0, 0, 0.5)',
                       'shadowBlur': 5,
                       'shadowOffsetY': 10,
                       'shadowOffsetX': 10,
                       'curve': 0.5,
                       'color': JsCode(color_js0)
                   }
               },
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
                "barBorderRadius": [45, 45, 45, 45],
                "shadowColor": "rgb(0, 160, 221)",
            }
        },
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(name="high_price",value=coordy_high,coord=[coordx,coordy_high],symbol=symbols['TV'],symbol_size=35,#symbol=symbols['circle'],symbol_size=20,
                                       itemstyle_opts=opts.ItemStyleOpts(color=color0[0])),#,border_color="red"
                ],
                label_opts=opts.LabelOpts(font_size=18,color=color0[0],font_weight="bold",position="right")
            )

        )
        .add_yaxis(
            series_name="",
            y_axis=list(data['low'])[0:i], is_smooth=True,is_symbol_show=False,
#             linestyle_opts=opts.LineStyleOpts(color=color0[1],width=3),
            itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_js1)),
            linestyle_opts={
                   'normal': {
                       'width': 3,
                       'shadowColor': 'rgba(0, 0, 0, 0.5)',
                       'shadowBlur': 5,
                       'shadowOffsetY': 10,
                       'shadowOffsetX': 10,
                       'curve': 0.5,
                       'color': JsCode(color_js1)
                   }
               },
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(name="low_price",value=coordy_low,coord=[coordx,coordy_low],symbol=symbols['TV'],symbol_size=35,#symbol=symbols['circle'],symbol_size=20,
                                       itemstyle_opts=opts.ItemStyleOpts(color=color0[1])),#,border_color="red"
                ],
                label_opts=opts.LabelOpts(font_size=18,color=color0[0],font_weight="bold",position="right")
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts("bilibili上市以来每日最高和最低\n\n            {}".format(title_date),pos_left=330,padding=[30,20]),
            xaxis_opts=opts.AxisOpts(type_="time",max_=x_max),#, interval=10,min_=i-5,split_number=20,axistick_opts=opts.AxisTickOpts(length=2500),axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="grey"))
            yaxis_opts=opts.AxisOpts(min_=9,max_=y_max),#坐标轴颜色,axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="grey"))
        )
    )
    tl.add(c, "{}".format(list(data['date'])[i]))
    tl.add_schema(
        axis_type='time',
        play_interval=30,  # 表示播放的速度
        pos_bottom="-29px",
        is_loop_play=False, # 是否循环播放
        width="780px",
        pos_left='30px',
        is_auto_play=True,  # 是否自动播放。
        is_timeline_show=False)
print(tl.render())