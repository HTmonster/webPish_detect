window.onload = function() {
    document.getElementById("btn_safety").addEventListener("click", btn_safety);
    document.getElementById("btn_continue").addEventListener("click", btn_continue);
}

function getJsonFromUrl() {
    var query = location.search.substr(1);
    var result = {};
    query.split("&").forEach(function(part) {
        var item = part.split("=");
        result[item[0]] = decodeURIComponent(item[1]);
    });
    return result;
}

function btn_safety() {
    if(window.history.go(-2))
        ;
    else
        window.location.href="http://www.baidu.com";

}

function btn_continue() {
    window.history.go(-1);
    return false;
}