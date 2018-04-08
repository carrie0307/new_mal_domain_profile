/**
 * Created by wxb on 18-2-1.
 */
function showData(url,option,parameter,funcs){

  $.ajax({
      url:url,
      data:option,
      type:'get',
      timeout:10000,
      success: function (data) {  //成功后的处理  将从服务器传回的数据写到页面上
          //使用 JSON.parse 将 JSON 字符串转换成对象
         var data = JSON.parse(data);
         for(j = 0; j < funcs.length; j++) {
            funcs[j](data, parameter);
         }
      },
      error: function (xhr) {
          if (xhr.status == "0") {
              alert("超时，稍后重试");
          } else {
              alert("错误提示：" + xhr.status + " " + xhr.statusText);
          }
      } // 出错后的处理
  });
}

function showData_bysyn(url,option){
    var result = null;
    $.ajax({
      url:url,
      data:option,
      type:'get',
      timeout:10000,
      async: false,
      success: function (data) {  //成功后的处理  将从服务器传回的数据写到页面上
          //使用 JSON.parse 将 JSON 字符串转换成对象
         result = JSON.parse(data);
      },
      error: function (xhr) {
          if (xhr.status == "0") {
              alert("超时，稍后重试");
          } else {
              alert("错误提示：" + xhr.status + " " + xhr.statusText);
          }
      } // 出错后的处理
    });
    return result
}