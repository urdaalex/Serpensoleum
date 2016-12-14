'use strict'

var cs_to_background_port = chrome.extension.connect({
    name: "cs_to_background"
});

var background_to_cs = chrome.extension.connect({
    name: "background_to_cs"
});


chrome.extension.onConnect.addListener(function(port) {
    console.log("Connected .....");
    if (port.name == "background_to_cs") {
        port.onMessage.addListener(function(msg) {
            console.log("message recieved" + msg);

            if (msg.state == false) {
                removeAllScripts();
            } else if (msg.state == true) {
                if (window.location.href.indexOf('google') > -1) {
                    injectAllScripts();
                }
            }
        });
    }
});

function messageListener(request, sender, sendResponse) {
    handleStateModification();

    sendResponse({});

    // sendResponse({ state: chrome.storage.sync.get('enabledStatus') });
}

chrome.runtime.onMessage.addListener(messageListener);

// function manageResponse(msg) {
//     console.log("message recieved" + msg);

//     if (msg.state == false) {
//         removeAllScripts();
//     } else if (msg.state == true) {
//         injectAllScripts();
//     }
// }

function requestExtensionState() {
    // cs_to_background_port.postMessage("get state");
    // chrome.runtime.sendMessage("get state", manageResponse)

    handleStateModification();
}

requestExtensionState();

function handleStateModification() {
    chrome.storage.sync.get('enabledStatus', function(obj) {
        if (obj.enabledStatus == null) {
            obj.enabledStatus = true;
        }

        if (obj.enabledStatus == true) {
            if (window.location.href.indexOf('google') > -1) { 
                injectAllScripts();
            }
        } else {
            removeAllScripts();
        }
    });
}

function injectScript(file, node, id) {
    var th = document.getElementsByTagName(node)[0];
    var s = document.createElement('script');
    s.setAttribute('id', id);
    s.setAttribute('type', 'text/javascript');
    s.setAttribute('src', file);
    th.appendChild(s);
}

function removeAllScripts() {
    $('#Z1Z1Z1Z1').remove();
    $('#X1X1X1X1').remove();
    $('.bs111check111bs').remove();
}

function injectAllScripts() {
    // var iresDiv = $("#ires");
    // iresDiv.attr('data-async-context', '');


    injectScript(chrome.extension.getURL('jquery.js'), 'head', 'Z1Z1Z1Z1');
    injectScript(chrome.extension.getURL('listener.js'), 'head', 'X1X1X1X1');
}


// var script = document.createElement('script');
// script.textContent = actualCode;
// (document.head||document.documentElement).appendChild(script);
// script.parentNode.removeChild(script);
