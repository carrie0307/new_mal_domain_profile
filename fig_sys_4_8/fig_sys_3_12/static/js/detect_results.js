function set_detect_results(detect_results){
    for(var key in detect_results){
        var class_type;
        if (detect_results[key]['detect_type']=="危险"){
            class_type = "result_danger"
        }else if (detect_results[key]['detect_type']=="安全"){
            class_type = "result_safety"
        }else{
            class_type="result_unknown";
        }
        $('#'+key+'-res').text(detect_results[key]['detect_result']);
        $('#'+key+'-time').text(detect_results[key]['detect_time']);
        document.getElementById(key+"-img").setAttribute("class",class_type);
    }
}
