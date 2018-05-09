/**
 * Created by wxb on 18-2-1.
 */

function showtable_pos(data,paras){
    var result;
    var idx_name = "table_data_idx";
    if (paras.hasOwnProperty(idx_name)){
        var idx = paras[idx_name];
        result = data[idx];
    }else{
        result = data;
    }
    var table_tip= document.getElementById(paras.table_id);
    if ( $.fn.dataTable.isDataTable( table_tip) ) {
      var table = $(table_tip).DataTable();
      table.clear().draw();
      table.rows.add(result).draw();
    }else {
      table = $(table_tip).DataTable({
          data: result,
          columns:paras.cols,
          aoColumnDefs :  [{
                "aTargets" :　[1],
                "mRender" : function(data){
                    return "<a href='/keyinfo_query?source=pos&value="+data+"'>"+data+"</a>";
                }
          }],
          retrieve:true,
          destroy:true,
          bAutoWidth: false,
          bDeferRender:true,
          bLengthChange:false,
          bFilter:false,
          info:false
      });
      if (paras.hasOwnProperty('rows')){
          table.page.len(paras.rows).draw();
      }else{
          table.page.len(20).draw();
      }
    }
}

function show_general_table(data,paras){
    var table_tip= document.getElementById(paras.table_id);
    if ( $.fn.dataTable.isDataTable( table_tip) ) {
        var table = $(table_tip).DataTable();
        table.drop();
    }
    var cols;
    if (paras.source == "ip"){
        $('.source_title').text("服务IP");
        cols = [
            {
                "data": "seq_num",
                "title": "序号"
            },
            {
                "data": "IP",
                "title": "服务IP"
            },
            {
                "data": 'num',
                "title": "服务域名数量"
            },
            {
                "data": "country",
                "title": "国家"
            },
            {
                "data": "city",
                "title": "地址"
            },
            {
                "data": "operater",
                "title": "运营商"
            },
            {
                "data": "ASN",
                "title": "ASN"
            },
            {
                "data": "AS_OWNER",
                "title": "AS_OWNER"
            }
        ];
    }else if (paras.source == "reg_name"){
        $('.source_title').text("注册者");
        cols = [
            {
                "data": "seq_num",
                "title": "序号"
            },
            {
                "data": "reg_name",
                "title": "注册人姓名"
            },
            {
                "data": "domain_count",
                "title": "非法域名总量"
            },
            {
                "data": "gamble_count",
                "title": "赌博类"
            },
            {
                "data": "porno_count",
                "title": "色情类"
            }
        ];
    }else if (paras.source == "reg_phone"){
        $('.source_title').text("注册电话");
        cols = [
            {
                "data": "seq_num",
                "title": "序号"
            },
            {
                "data": "reg_phone",
                "title": "注册人电话"
            },
            {
                "data": "domain_count",
                "title": "非法域名总量"
            },
            {
                "data": "gamble_count",
                "title": "赌博类"
            },
            {
                "data": "porno_count",
                "title": "色情类"
            }
        ];
    }else if (paras.source == "reg_email"){
        $('.source_title').text("注册邮箱");
        cols = [
            {
                "data": "seq_num",
                "title": "序号"
            },
            {
                "data": "reg_email",
                "title": "注册人邮箱"
            },
            {
                "data": "domain_count",
                "title": "非法域名总量"
            },
            {
                "data": "gamble_count",
                "title": "赌博类"
            },
            {
                "data": "porno_count",
                "title": "色情类"
            }
        ];
    }else if (paras.source == "registrar"){
        $('.source_title').text("注册商");
        cols = [
            {
                "data": "seq_num",
                "title": "序号"
            },
            {
                "data": 'sponsoring_registrar',
                "title": "注册商"
            },
            {
                "data": "domain_count",
                "title": "非法域名总量"
            },
            {
                "data": "gamble_count",
                "title": "赌博类"
            },
            {
                "data": "porno_count",
                "title": "色情类"
            }
        ];
    }else{
        alert("类型错误!");
        return
    }
    if (paras.source=="registrar"){
        paras['source']="sponsoring_registrar"
    }
    table = $(table_tip).DataTable({
        data: data,
        columns:cols,
        retrieve:true,
        aoColumnDefs :  [{
                "aTargets" :　[1],
                "mRender" : function(data){
                    return "<a href='/keyinfo_query?source="+paras.source+"&value="+data.replace(/\+/g,"%2B")+"'>"+data+"</a>";
                }
          }],
        destroy:true,
        bAutoWidth: false,
        bDeferRender:true,
        bLengthChange:false,
        bFilter:false,
        info:false
    });
    if (paras.hasOwnProperty('rows')){
        table.page.len(paras.rows).draw();
    }else{
        table.page.len(20).draw();
    }
}

function show_overview_tables(data,paras){
    for(j=0; j < 6; j++){
        parameters = {
            table_id : paras.table_ids[j],
            cols : paras.table_cols[j],
            rows:paras.rows[j],
            aoColumnDefs:paras.aoColumnDefs
        };
        result = data[j];
        showtable(result,parameters);
    }
}

function showtable(data,paras){
    var result;
    var idx_name = "table_data_idx";
    if (paras.hasOwnProperty(idx_name)){
        var idx = paras[idx_name];
        result = data[idx];
    }else{
        result = data;
    }
    var table_tip= document.getElementById(paras.table_id);
    var def;
    if (paras.hasOwnProperty('aoColumnDefs')){
        def = paras.aoColumnDefs;
    }else{
        def = [];
    }
    if ( $.fn.dataTable.isDataTable( table_tip) ) {
      var table = $(table_tip).DataTable();
      table.clear().draw();
      table.rows.add(result).draw();
    }else {
      table = $(table_tip).DataTable({
          data: result,
          columns:paras.cols,
          aoColumnDefs : def,
          retrieve:true,
          destroy:true,
          bAutoWidth: false,
          bDeferRender:true,
          bLengthChange:false,
          bFilter:false,
          info:false
      });
      if (paras.hasOwnProperty('rows')){
          table.page.len(paras.rows).draw();
      }else{
          table.page.len(20).draw();
      }
    }
}
