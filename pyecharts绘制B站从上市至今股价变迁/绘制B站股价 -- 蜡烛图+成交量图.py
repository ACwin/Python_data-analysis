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





data['date'] = data['date'].astype("str")
xaxis_data=list(data.date)


def get_duration(x):
    if 'M' in x:
        x = float(x.split('M')[0]) * 1000000
        return int(x)
    elif 'K' in x:
        x = float(x.split('K')[0]) * 1000
        return int(x)


data['volume'] = data['volume'].apply(lambda x: get_duration(x))

kline = (
    Kline(init_opts=opts.InitOpts(width="1000px", height="800px"))
        .add_xaxis(xaxis_data=list(data.date))
        .add_yaxis(
        series_name="klines",
        y_axis=data[["open", "close", "low", "high"]].values.tolist(),
        itemstyle_opts=opts.ItemStyleOpts(color="#ec0000", color0="#00da3c"),
    )
        .set_global_opts(legend_opts=opts.LegendOpts(is_show=True, pos_bottom=10, pos_left="center"),
                         datazoom_opts=[
                             opts.DataZoomOpts(
                                 is_show=False,
                                 type_="inside",
                                 xaxis_index=[0, 1],  # 这里需要修改可缩放的x轴坐标编号
                                 range_start=98,
                                 range_end=100,
                             ),
                             opts.DataZoomOpts(
                                 is_show=True,
                                 xaxis_index=[0, 1],  # 这里需要修改可缩放的x轴坐标编号
                                 type_="slider",
                                 pos_top="85%",
                                 range_start=98,
                                 range_end=100,
                             ),
                         ],
                         yaxis_opts=opts.AxisOpts(
                             is_scale=True,
                             splitarea_opts=opts.SplitAreaOpts(
                                 is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                             ),
                         ),
                         tooltip_opts=opts.TooltipOpts(
                             trigger="axis",
                             axis_pointer_type="cross",
                             background_color="rgba(245, 245, 245, 0.8)",
                             border_width=1,
                             border_color="#ccc",
                             textstyle_opts=opts.TextStyleOpts(color="#000"),
                         ),
                         visualmap_opts=opts.VisualMapOpts(
                             is_show=False,
                             dimension=2,
                             series_index=5,
                             is_piecewise=True,
                             pieces=[
                                 {"value": 1, "color": "#00da3c"},
                                 {"value": -1, "color": "#ec0000"},
                             ],
                         ),
                         axispointer_opts=opts.AxisPointerOpts(
                             is_show=True,
                             link=[{"xAxisIndex": "all"}],
                             label=opts.LabelOpts(background_color="#777"),
                         ),
                         brush_opts=opts.BrushOpts(
                             x_axis_index="all",
                             brush_link="all",
                             out_of_brush={"colorAlpha": 0.1},
                             brush_type="lineX",
                         ),
                         )
)

bar = (
    Bar()
        .add_xaxis(xaxis_data=list(data.date))
        .add_yaxis(
        series_name="volume",
        y_axis=data["volume"].tolist(),
        xaxis_index=1,
        yaxis_index=1,
        label_opts=opts.LabelOpts(is_show=False),
        itemstyle_opts=opts.ItemStyleOpts(
            color=JsCode(
                """
            function(params) {
                var colorList;
                if (barData[params.dataIndex][1] > barData[params.dataIndex][0]) {
                    colorList = '#ef232a';
                } else {
                    colorList = '#14b143';
                }
                return colorList;
            }
            """
            )
        ),
    )
        .set_global_opts(
        xaxis_opts=opts.AxisOpts(
            type_="category",
            grid_index=1,
            axislabel_opts=opts.LabelOpts(is_show=False),
        ),
        legend_opts=opts.LegendOpts(is_show=False),
    )
)

grid_chart = Grid(
    init_opts=opts.InitOpts(
        width="1000px",
        height="800px",
        animation_opts=opts.AnimationOpts(animation=False),
    )
)

grid_chart.add_js_funcs(
    "var barData={}".format(data[["open", "close"]].values.tolist()))  # 导入open、close数据到barData改变交易量每个bar的颜色
grid_chart.add(
    # overlap_kline_line,
    kline,
    grid_opts=opts.GridOpts(pos_left="10%", pos_right="8%", height="40%"),
)
grid_chart.add(
    bar,
    grid_opts=opts.GridOpts(
        pos_left="10%", pos_right="8%", pos_top="60%", height="20%"
    ),
)
print(grid_chart.render())