function save_options() {
    var setting=1;
    var radio1 = document.getElementById("1")
    if (radio1.checked==true){
        setting=0;
    }
    var id=-1;
    if(document.getElementById("usrID").value){
        id=document.getElementById("usrID").value;
    }
    
    chrome.storage.local.set({
        setting: setting,
        id:id
    }, function() {
        // Update status to let user know options were saved.
        var status = document.getElementById('status');
        status.textContent = 'Options saved.';
        setTimeout(function() {
            status.textContent = '';
        }, 750);
    });
}

// Restores select box and checkbox state using the preferences
// stored in chrome.storage.
function restore_options() {
    chrome.storage.local.get({
        setting: 1,
        id:-1
    }, function(items) {
        document.getElementById('1').checked = !items.setting;
        document.getElementById('2').checked = items.setting;
        if(items.id==-1){
            document.getElementById('4').checked = 1;
        }
        else{
            document.getElementById('3').checked = 1;
            document.getElementById('usrID').value= items.id;
        }
    });
}
document.addEventListener('DOMContentLoaded', restore_options);
document.getElementById('save').addEventListener('click',
    save_options);