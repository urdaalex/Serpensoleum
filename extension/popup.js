'use strict'

function initializeChromeStorageState() {
    // By default the extension will be enabled when first importing it into chrome
    chrome.storage.sync.get('enabledStatus', function(obj) {
        if (obj.enabledStatus == null) {
            chrome.storage.sync.set({ 'enabledStatus': true }, function() {
                updateButtonText();
            });
        }
    })
}

initializeChromeStorageState();

function updateButtonText() {
    chrome.storage.sync.get("enabledStatus", function(obj) {
        if (obj.enabledStatus == true) {
            $("#commandBtn").attr("value", "Disable");
            $("#commandBtn").removeClass();
            $("#commandBtn").addClass("disable");
        } else {
            $("#commandBtn").attr("value", "Enable");
            $("#commandBtn").removeClass();
            $("#commandBtn").addClass("enable");
        }
    });
}

updateButtonText();

function changeChromeStorageState() {
    var state = chrome.storage.sync.get('enabledStatus', function(obj) {
        chrome.storage.sync.set({ 'enabledStatus': !obj.enabledStatus }, function() {
            updateButtonText();
            broadcastAllTabs();
        });
    });
}

var popup_to_background_port = chrome.extension.connect({
    name: "popup_background"
});

function broadcastAllTabs() {
    chrome.tabs.query({}, function(tabs) {
        var message = { action: "stop" };

        for (var i = 0; i < tabs.length; ++i) {
            chrome.tabs.sendMessage(tabs[i].id, message);
        }
    });
}

function broadCastToBackgroundScript() {
    popup_to_background_port.postMessage();
}

window.onload = function() {
    document.getElementById('commandBtn').onclick = function() {
        changeChromeStorageState();
    };
}
