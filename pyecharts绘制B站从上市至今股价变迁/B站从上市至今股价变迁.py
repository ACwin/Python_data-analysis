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
color0 = ['#FF76A2']
color_js0 = """new echarts.graphic.LinearGradient(0, 1, 0, 0,
    [{offset: 0, color: '#FFFFFF'}, {offset: 1, color: '#ed1941'}], false)"""

tl = Timeline()
for i in range(0, len(data)):
    x_max = list(data['date'])[i] + datetime.timedelta(days=70)
    y_max = int(max(list(data['close'])[0:i + 1])) + 3
    title_date = list(data['date'])[i].strftime('%Y-%m-%d')
    c = (
        Line(
            init_opts=opts.InitOpts(
                theme='dark',
                width='1500px',
                height='900px', )
        )
            .add_xaxis(list(data['date'])[0:i])
            .add_yaxis(
            series_name="",
            y_axis=list(data['close'])[0:i], is_smooth=True, is_symbol_show=False,
            #             linestyle_opts=opts.LineStyleOpts(color=color0[0],width=3),
            linestyle_opts={
                'normal': {
                    'width': 3,
                    'shadowColor': 'rgba(0, 0, 0, 0.5)',
                    'shadowBlur': 5,
                    'shadowOffsetY': 10,
                    'shadowOffsetX': 10,
                    'curve': 0.5,
                    'color': 'red'
                }
            },
            itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_js0)),
        )

            .set_global_opts(
            title_opts=opts.TitleOpts("bilibili上市以来每日收盘价\n\n        {}".format(title_date), pos_left=350,
                                      padding=[30, 20]),
            xaxis_opts=opts.AxisOpts(type_="time", max_=x_max),
            # , interval=10,min_=i-5,split_number=20,axistick_opts=opts.AxisTickOpts(length=2500),axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="grey"))
            yaxis_opts=opts.AxisOpts(min_=9, max_=y_max),
            # 坐标轴颜色,axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="grey"))
        )
    )
    tl.add(c, "{}".format(list(data['date'])[i]))
    tl.add_schema(
        axis_type='time',
        play_interval=30,  # 表示播放的速度
        pos_bottom="-29px",
        is_loop_play=True,  # 是否循环播放
        width="780px",
        pos_left='30px',
        is_auto_play=True,  # 是否自动播放。
        is_timeline_show=False
    )

print(tl.render())