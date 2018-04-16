/**
 * Created by wxb on 18-2-3.
 */



function add_table_rows(data,paras){
    var tab = document.getElementById(paras.table_id);
    for (var j=0;j<data.length;j++){
        tr = document.createElement("tr");
        tab.tBodies[0].appendChild(tr);
        for (var i=0;i<data[j].length;i++){
            td = document.createElement("td");
            td.innerHTML = data[j][i];
            tr.appendChild(td);
        }
    }
}
function add_whois_analyse(data,paras){
    var tag_info = data['tag'];
    $('#reg_name_num').text(tag_info['reg_name_num']);
    $('#reg_email_num').text(tag_info['reg_email_num']);
    $('#reg_phone_num').text(tag_info['reg_phone_num']);
    $('#live_period').text(tag_info['live_period']);
    data['table_content'][13][1] = "<a href='/whois_history?domain=" + paras['domain'] + " '>点击查看</a>";
    add_table_rows(data['table_content'],paras);
}

function add_pos_analyse(data,paras){
    var map_data = data[0];
    var table1_data = data[1];
    $('#pos_level').text(data[2]);
    var table2_data = data[3];
    var table3_data = data[4];
    showmap(map_data,paras);
    add_table_rows(table1_data,paras);
    paras['table_id'] = 'icp_pos_table';
    $("#icp_pos_table tbody").html("");
    add_table_rows(table2_data,paras);
    paras['table_id'] = 'ip_pos_table';
    $("#ip_pos_table tbody").html("");
    add_table_rows(table3_data,paras);
}


function add_links_analyse(data,paras){
    var table_data = data[0];
    var chart_data = data[1];
    add_table_rows(table_data,paras);
    showbar(chart_data,paras);
}

function add_content_analyse(data,paras){
    var table_data = data[0];
    var shot_path = data[1];
    var shot_id=paras.shot_id;
    add_table_rows(table_data,paras);
    $("#"+shot_id).attr('src','/static/images/'+shot_path);
}

function add_ip_analyse(data,paras){
    $('#ip_num').text(data['ip_num']);
    $('#ip_change_freq').text(data['change_frequency']);
    showtable(data['table_info'],paras);

//    CNAME记录
    if(data['other_dns_rr']['cname'].length == 0){
        $("#dns_cname tbody").html("<tr><td>CNAME记录</td><td>无数据</td></tr>");
    }
    else{
        var dns_paras = {};
        dns_paras['table_id'] = 'dns_cname';
        $("#dns_cname tbody").html("");
        add_table_rows(data['other_dns_rr']['cname'],dns_paras);
    };

//    NS记录
    if(data['other_dns_rr']['ns'].length == 0){
        $("#dns_ns tbody").html("<tr><td>NS记录</td><td>无数据</td></tr>");
    }
    else{
        var dns_paras = {};
        dns_paras['table_id'] = 'dns_ns';
        $("#dns_ns tbody").html("");
        add_table_rows(data['other_dns_rr']['ns'],dns_paras);
    };

//    TXT记录
    if(data['other_dns_rr']['txt'].length == 0){
        $("#dns_txt tbody").html("<tr><td>TXT记录</td><td>无数据</td></tr>");
    }
    else{
        var dns_paras = {};
        dns_paras['table_id'] = 'dns_txt';
        $("#dns_txt tbody").html("");
        add_table_rows(data['other_dns_rr']['txt'],dns_paras);
    };


    var res_mx = data['other_dns_rr']['mx'];
    if(res_mx.length ==0){
        $("#dns_mx tbody").html("<tr><td>无数据</td><td>无数据</td></tr>");
    }
    else{
        var dns_paras = {};
        dns_paras['table_id'] = 'dns_mx';
        $("#dns_mx tbody").html("");
        add_table_rows(data['other_dns_rr']['mx'],dns_paras);
    };

    var res_soa = data['other_dns_rr']['soa'];
    if(res_soa.length ==0){
        $("#dns_soa tbody").html("<tr><td>无数据</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>");
    }
    else{
        var dns_paras = {};
        dns_paras['table_id'] = 'dns_soa';
        $("#dns_soa tbody").html("");
        add_table_rows(data['other_dns_rr']['soa'],dns_paras);
    };


}

function add_all_analyse(data,paras){

    $('#baseinfo_1').text(data['baseinfo'][0]);
    $('#baseinfo_2').text(data['baseinfo'][1]);
    $('#baseinfo_3').text(data['baseinfo'][2]);
    $('#baseinfo_4').text(data['baseinfo'][3]);
    set_detect_results(data['detect_results']);
    add_ip_analyse(data['analyse_results'],paras)
}

function deal_ip_history(data,paras){
    if(data==""){
        var html_none = '<li><div class="block_list"><h2 class="ip_total">无数据</h2><span class="circle"></span><span class="square"></span></div></li>';
        $("#timeline").html(html_none);
    }
    else{
        var data_len = data.length;
        var html_total = "";
        for (var i=0; i < data_len; i++){
            var ip_time = data[i]['insert_time'];
            var add_list = data[i]['add_ip'];
            var reduce_list = data[i]['reduce_ip'];
            var ip_list = data[i]['ips']


            var ip_total_html = '';
            if(ip_list.length != ""){
                ip_total_html = '<h3 class="ip_total">IP集合</h3><p>';
                for(var j=0; j < ip_list.length; j++){
                    var htmls ='<span class="IP-style">'
                                + ip_list[j]['ip'] + '&nbsp &nbsp &nbsp' + ip_list[j]['status']
                                + '</span>';
                    ip_total_html = ip_total_html + htmls;
                }
                ip_total_html = ip_total_html + '</p>';
            }
            else{
                ip_total_html = '<h3 class="ip_total">IP集合</h3><p><span class="IP-style">无数据</span></p>';
            };

            var add_ip_html = '';
            if(add_list != ""){
                add_ip_html = '<h3 class="ip_add">增加的IP</h3><p>';
                for(var j=0; j < add_list.length; j++){
                    var htmls ='<span class="IP-style">'+ add_list[j] + '</span>';
                    add_ip_html = add_ip_html + htmls;
                }
                add_ip_html = add_ip_html + '</p>';
            };

            var reduce_ip_html = '';
            if(reduce_list != ""){
                reduce_ip_html = '<h3 class="ip_add">减少的IP</h3><p>';
                for(var j=0; j < reduce_list.length; j++){
                    var htmls ='<span class="IP-style">'+ reduce_list[j]+ '</span>';
                    reduce_ip_html = reduce_ip_html + htmls;
                }
                reduce_ip_html = reduce_ip_html + '</p>';
            };

            var html_1 = '<li><div class="block_list">'
                    + ip_total_html + add_ip_html + reduce_ip_html
                    + '<span class="date">'+ ip_time +'</span>'
                    + '<span class="circle"></span><span class="square"></span></div></li>';
            html_total = html_total + html_1;
        }
        $("#timeline").html(html_total);
    }
}
