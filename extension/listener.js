function callPythonScript(url, query, element) {
    if ( $('#Z1Z1Z1Z1').get(0) == undefined) {
        return;
    }

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:3000/check_valid",
        data: JSON.stringify({ url: url , query: query})
    }).done(function(response) {
        if ( $('#Z1Z1Z1Z1').get(0) == undefined)  {
            return;
        }

        console.log(response);
        response = JSON.parse(response);
        var img = document.createElement("img");

        if (response.validity == true) {
            img.setAttribute('src', 'http://www.clker.com/cliparts/e/2/a/d/1206574733930851359Ryan_Taylor_Green_Tick.svg.med.png');            
        } else {
            img.setAttribute('src', 'http://www.clipartbest.com/cliparts/jix/EyA/jixEyAb5T.png');
        }

        img.setAttribute('class', 'bs111check111bs')
        img.style.cssFloat = 'right';
        img.style.height = '25px';

        var header = $(element).find('h3.r')
        header.append(img);
    });
}

var currentPage = window.location.href;

var timer = setInterval(function()
{
    if ( $('#Z1Z1Z1Z1').get(0) == undefined) {
        clearInterval(timer);
        return;
    }

    if (currentPage !== window.location.href)
    {
        if (!window.location.href.startsWith('https://www.google')) {

        } else {
            setTimeout(iterateOverPageResults, 1000);
        }
        // alert(window.location.href);
        // page has changed, set new page as 'current'

        currentPage = window.location.href;

    }
}, 100);


// document.getElementsByTagName("body")[0].onhashchange = function() { iterateOverPageResults() };

function iterateOverPageResults() {
    if (window.location.href.startsWith('https://www.google')) {
        $('div.g').each(function(i, obj) {
            var currentGoogleURL = window.location.href;
            var query = googleURLToQuery(currentGoogleURL);
            // var url = $(this).find('cite').html();
            var url = $(this).find('h3.r a').data('href');

            if (url == null) {
                url = $(this).find('h3.r a').attr('href');
            }

            callPythonScript(url, query, obj);
        });
    }
}

function googleURLToQuery(url) {
    var patt = new RegExp("#.*");
    var res = patt.exec(url);

    res = url.indexOf("&") > -1 ? url.split("&")[0] : url;

    return res;
}


function defer(method) {
    if (window.jQuery) {
        method();
    }
    else {
        setTimeout(function() { defer(method) }, 50);
    }
}

defer(iterateOverPageResults);