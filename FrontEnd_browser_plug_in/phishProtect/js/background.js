

var tabIdMap = {};
var tabIgnored = {};
var tabMalicious = {};

chrome.storage.local.get({
    setting: 1,
}, function (items) {
    addListener(items.setting);
});

function addListener(setting) {
    chrome.tabs.onUpdated.addListener(function mylistener(tabId, changedProps, tab) {
        chrome.storage.local.get({
            setting: 1,
            id:-1
        }, function (items) {
            setting = items.setting;
            id=items.id;
        });

        if (changedProps.status != "complete") { //未加载完成
            return;
        }
        //alert("bg setting:"+setting);
        var prev_url = "";
        if (tabId in tabIdMap) { //如果该tab之前被访问过
            prev_url = tabIdMap[tabId]; //拿到之前该tab的url
        }
        tabIdMap[tabId] = tab.url;//把当前的tab访问的url也加入二维数组中。一对一
        var domain = extractHostname(tab.url);

        if (isPageBlockedUrl(prev_url)) { //如果之前的url被判定为恶意
            if (tabId in tabIgnored) {//如果tab在tabIngnored数组中，一对多
                tabIgnored[tabId].push(domain);//在tabIgnored中当前tabId加入对应的domin
            } else {
                tabIgnored[tabId] = [domain];//创建，加入
            }
            return;
        }

        if ((tabId in tabIgnored) && (tabIgnored[tabId].indexOf(domain) > -1)) { //如果当前tab在tabIgnored数组中存在当前domin，不拦截
            return;
        }
        //IDN国际编码拦截
        if (isDomainIDN(domain)) {
            chrome.tabs.update(tabId, { url: "page_blocked.html" });
            return;
        }
        //浏览器扩展管理界面打开或者是内网打开，放行
        if (isSystemUrl(tab.url) || isPrivateIp(domain)) {
            return;
        }

        var xhr = new XMLHttpRequest();
        //使用HTTP POST请求与服务器交互数据
        xhr.open("POST", "http://127.0.0.1:8000/api/", true);
        //设置发送数据的请求格式
        xhr.withCredentials = true
        xhr.setRequestHeader("Content-type", "application/json");
        xhr.onreadystatechange = () =>{
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                res = JSON.parse(xhr.responseText);
                if (res['result'] == '0') {
                    tabMalicious[tabId] = { zero_day: true, targeted_brand: domain };
                    chrome.tabs.update(tabId, { url: "page_blocked.html" });
                }
            } else {
                console.log(xhr.responseText)
            }
        }
        var sendData = {'url':tab.url,'setting':setting,'id':id};
        //将用户输入值序列化成字符串
        xhr.send(JSON.stringify(sendData));
    });
};









