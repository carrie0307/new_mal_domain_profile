function showmap(data,paras){
//显示地图
    var result;
    var idx_name = "map_data_idx";
    if (paras.hasOwnProperty(idx_name)){
        var idx = paras[idx_name];
        result = data[idx];
    }else{
        result = data;
    }
    var max = result[1];
    var map_data = result[0];
    var chart = echarts.init(document.getElementById(paras.map_id));
    option = {
        tooltip: {
            trigger: 'item'
        },
        visualMap: {
            min: 0,
            max: max,
            left: 'left',
            top: 'bottom',
            text: ['高','低'],           // 文本，默认为数值文本
            calculable: true,
            inRange: {
                color: ['#d19392', '#d1524c','#d10e11']
            }
        },
        toolbox: {
            show: true,
            orient: 'vertical',
            left: 'right',
            top: 'center',
            feature: {
                dataView: {readOnly: false},
                restore: {},
                saveAsImage: {}
            }
        },
        series: [
            {
                name: '地区域名数量',
                type: 'map',
                mapType: 'china',
                roam: true,
                label: {
                    normal: {
                        show: true,
                        color: '#5e5f74'
                    },
                    emphasis: {
                        show: true,
                        textStyle: {
                            fontFamily: name
                        }
                    }
                },
                data:map_data
            }
        ]
    };
    chart.on('georoam', function (params) {
        console.log(params);
    });//实现地图的缩放
    chart.setOption(option);
}