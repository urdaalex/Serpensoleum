 'use strict'
 chrome.extension.onConnect.addListener(function(port) {
     console.log("Connected .....");
     if (port.name == "popup_background") {
         port.onMessage.addListener(function(msg) {
             console.log("message recieved" + msg);

             // background_to_cs_port.postMessage({ state: state });
             broadcastAllTabs();

             // port.postMessage("Hi Popup.js");
         });
     } else if (port.name == "cs_to_background") {
         chrome.storage.sync.get('enabledStatus', function(obj) {
             if (obj.enabledStatus == null) {
                 obj["enabledStatus"] = true;
             }

             port.postMessage({ state: obj.enabledStatus });
         });
     }
 });


 // function messageListener(request, sender, sendResponse) {
 //     chrome.storage.sync.get('enabledStatus', function(obj) {
 //         if (obj.enabledStatus == null) {
 //             obj["enabledStatus"] = true;
 //         }

 //         sendResponse({ state: obj.enabledStatus });
 //     });

 //     return true;
 //     // sendResponse({ state: chrome.storage.sync.get('enabledStatus') });
 // }

 // chrome.runtime.onMessage.addListener(messageListener);


 function broadcastAllTabs() {
     chrome.tabs.query({}, function(tabs) {
         var message = { action: "stop" };

         for (var i = 0; i < tabs.length; ++i) {
             var port = chrome.tabs.connect(tabs[i].id, { name: "background_to_cs" });

             try {
                 chrome.storage.sync.get('enabledStatus', function(obj) {
                     if (obj.enabledStatus == null) {
                         obj["enabledStatus"] = true;
                     }

                     port.postMessage({ state: obj.enabledStatus });
                 });

                 // port.postMessage({ state: chrome.storage.sync.get('enabledStatus') });
             } catch (err) {
                 // console.log(tabs[i].name);
             }
         }
     });
 }
