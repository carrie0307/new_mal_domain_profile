/**
 * Created by wxb on 18-2-4.
 */
function showbar(data,paras){
//正常显示柱状图
    var dom=document.getElementById(paras.fig_id);
    var myChart = echarts.init(dom);
    var option={
    tooltip : {
        trigger: 'axis'
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {show: true, type: ['bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            name : '链接关系',
            type : 'category',
            data : data['xdata'],
            position:'bottom',
            offset:1
        }
    ],
    yAxis : [
        {
            name : '数量比值(个)',
            type : 'value',
            axisLabel : {
                formatter: '{value}'
            }
        }
    ],
    series : [
        {
            name:'比值',
            type:'bar',
            data:data['ydata'],
            barWidth:50,
            markPoint : {
                data : [
                    {type : 'max', name: '最大值'},
                    {type : 'min', name: '最小值'}
                ]
            }
        }
    ]
};
myChart.setOption(option)
}