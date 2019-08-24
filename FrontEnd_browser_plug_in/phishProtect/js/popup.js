function restore_popup() {
    chrome.storage.local.get({
        setting:1
    }, function(items) {
       
        var bg = chrome.extension.getBackgroundPage();
        var query = {active: true, currentWindow: true};
        chrome.tabs.query(query, function callback(tabs) {
           
            var currentTab = tabs[0];//当前的tab
            if (currentTab.id in bg.tabMalicious) {
                var container = document.getElementById('container');
                var container_img = document.getElementById('container-img');
                var container_text = document.getElementById('container-text');
                container.style.background="red";//将背景颜色改为红色
                container_img.src = "img/icon-illegal.png"; //图片
                container_text.innerHTML = "此网站是恶意网站";//改变文字
                
            }
        });
    });
};

document.addEventListener('DOMContentLoaded', restore_popup);
