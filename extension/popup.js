    'use strict'

    function initializeChromeStorageState() {
        chrome.storage.sync.get('enabledStatus', function(obj) {
            if (obj.enabledStatus == null) {
                chrome.storage.sync.set({ 'enabledStatus': true }, function() {});
            }
        })
    }

    initializeChromeStorageState();

    function updateButtonText() {
        chrome.storage.sync.get("enabledStatus", function(obj) {
            if (obj.enabledStatus == true) {
                $("#commandBtn").attr("value", "disable");
            } else {
                $("#commandBtn").attr("value", "enable");
            }
        });
    }

    updateButtonText();

    function changeChromeStorageState() {
        var state = chrome.storage.sync.get('enabledStatus', function(obj) {
            chrome.storage.sync.set({ 'enabledStatus': !obj.enabledStatus }, function() {
                updateButtonText();
                // broadCastToBackgroundScript();
                broadcastAllTabs();
            });
        });
    }

    var popup_to_background_port = chrome.extension.connect({
        name: "popup_background"
    });

    // port.postMessage("disable");

    // port.onMessage.addListener(function(msg) {
    //     console.log("message recieved" + msg);
    // });


    function broadcastAllTabs() {
        chrome.tabs.query({}, function(tabs) {
            var message = { action: "stop" };

            for (var i = 0; i < tabs.length; ++i) {
                chrome.tabs.sendMessage(tabs[i].id, message);
            }
        });
    }

    function broadCastToBackgroundScript() {
        // var port = chrome.extension.connect({
        //     name: "popup_background"
        // });

        popup_to_background_port.postMessage();

        // port.onMessage.addListener(function(msg) {
        //     console.log("message recieved" + msg);
        // });
    }

    // chrome.extension.onConnect.addListener(function(port) {
    //     console.log("Connected .....");
    //     if (port == "background_to_popup") {
    //         port.onMessage.addListener(function(msg) {
    //             console.log("message recieved" + msg);
    //             port.postMessage("Hi Popup.js");
    //         });
    //     } else if (port == "")

    // });


    window.onload = function() {
        document.getElementById('commandBtn').onclick = function() {

            changeChromeStorageState();

            // alert("button 2 was clicked");

        };
    }
