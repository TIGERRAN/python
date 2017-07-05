$.ajaxSetup({
    timeout: 10000,
    error: function (xhr, status, e) {
        if (xhr.status == 401) {
            window.location.href = "/";
        } else {
            alert('error invoke! status:' + status);
        }
    },
    complete: function (xhr, status) {
    },
})

$(function () {
    var nav = "<nav class='navbar navbar-default' role='navigation'><div class='container-fluid'><div class='navbar-header'><a class='navbar-brand' href='/wk/home/'>Process</a></div><div id='nav_detail'><ul class='nav navbar-nav'>" +
        "<li class='active'><a href='/wk/home/'>上线申请</a></li>" +
        "<li><a href='/grp/group_manager/'>用户组</a></li>" +
        "<li><a href='/db/database_manager/'>DB</a></li>" +
        "<li><a href='/sys/list/'>系统</a></li>" +
        "<li><a href='/sys/pj_list/'>工程</a></li>" +
        "<li><a href='/db_backup/db_backup_view/'>数据库备份</a></li>" +
        "</ul></div><div style='float: right;margin-top: 15px'><span id='sessionUserNameShow'></span><a href='/login/logout'>注销</a></div></div></nav>";
    $("body").prepend(nav);
    $("#nav_detail li").removeClass("active");
    var cur = window.location.href;
    $("#nav_detail li a").each(function () {
        if (cur.indexOf($(this).attr("href")) > -1) {
            $(this).parent().addClass("active");
        }
    });

    var sessionUserName = $("#sessionUserName").val();
    if (sessionUserName) {
        $("#sessionUserNameShow").html("欢迎，" + sessionUserName+" &nbsp;&nbsp;");
    }
})

var CMN = {
    getUrlVar: function (name) {
        var vars = [], hash;
        var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
        for (var i = 0; i < hashes.length; i++) {
            hash = hashes[i].split('=');
            vars.push(hash[0]);
            vars[hash[0]] = hash[1];
        }
        return name ? vars[name] : vars;
    }
};
// 对Date的扩展，将 Date 转化为指定格式的String
// 月(M)、日(d)、小时(h)、分(m)、秒(s)、季度(q) 可以用 1-2 个占位符，
// 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字)
// 例子：
// (new Date()).Format("yyyy-MM-dd hh:mm:ss.S") ==> 2006-07-02 08:09:04.423
// (new Date()).Format("yyyy-M-d h:m:s.S")      ==> 2006-7-2 8:9:4.18
Date.prototype.Format = function (fmt) { //author: meizz
    var o = {
        "M+": this.getMonth() + 1,                 //月份
        "d+": this.getDate(),                    //日
        "h+": this.getHours(),                   //小时
        "m+": this.getMinutes(),                 //分
        "s+": this.getSeconds(),                 //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds()             //毫秒
    };
    if (/(y+)/.test(fmt))
        fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt))
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}