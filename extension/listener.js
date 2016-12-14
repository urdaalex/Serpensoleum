function callPythonScript(url, query, element) {
    if ($('#Z1Z1Z1Z1').get(0) == undefined) {
        return;
    }

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:3000/check_valid",
        data: JSON.stringify({ url: url, query: query })
    }).done(function(response) {
        if ($('#Z1Z1Z1Z1').get(0) == undefined) {
            return;
        }

        response = JSON.parse(response);
        var img = document.createElement("img");

        if (response.error != null) {
            img.setAttribute('src', 'https://static1.squarespace.com/static/556f3f09e4b0c47e24124c57/556f47ede4b0762173f1c6e9/556f4a1ee4b0762173f21cab/1433359635368/404-error.jpg?format=750w');
        } else if (response.relevant != null) {
            if (response.relevant == true) {
                img.setAttribute('src', 'http://www.clker.com/cliparts/e/2/a/d/1206574733930851359Ryan_Taylor_Green_Tick.svg.med.png');
            } else {
                img.setAttribute('src', 'http://static.artuk.org/w944h944/CSF/CSF_FIFE_KIRMG_452_1.jpg');
            }
        } else if (response.validity != null) {
            if (response.validity == true) {
                img.setAttribute('src', 'http://www.clker.com/cliparts/e/2/a/d/1206574733930851359Ryan_Taylor_Green_Tick.svg.med.png');
            } else if (response.validity == false) {
                img.setAttribute('src', 'http://www.clipartbest.com/cliparts/jix/EyA/jixEyAb5T.png');
            } else {
                img.setAttribute('src', 'http://static.artuk.org/w944h944/CSF/CSF_FIFE_KIRMG_452_1.jpg');
            }
        }

        img.setAttribute('class', 'bs111check111bs')
        img.style.cssFloat = 'right';
        img.style.height = '20px';

        var header = $(element).find('h3.r')
        header.append(img);
    });
}

var currentPage = window.location.href;
var justLoaded = true;

var timer = setInterval(function() {
    if ($('#Z1Z1Z1Z1').get(0) == undefined) {
        clearInterval(timer);
        return;
    }

    if (justLoaded == true) {
        if (!window.location.href.startsWith('https://www.google') ){//|| window.location.href.indexOf('search?') < 0) {

        } else {
            setTimeout(function() { deferResultIteration(iterateOverPageResults, 100); }, 200);
        }

        justLoaded = false;
    } else if (currentPage !== window.location.href) {
        if (!window.location.href.startsWith('https://www.google')) {

        } else {
            setTimeout(function() { deferResultIteration(iterateOverPageResults, 100); }, 300);
        }

        console.log("currentPage: " + currentPage);
        console.log("window.location.href: " + window.location.href);
        currentPage = window.location.href;
    }
}, 100);

function iterateOverPageResults() {
    if (window.location.href.startsWith('https://www.google')) {
        $('div[class="g"]').each(function(i, obj) {
            var currentGoogleURL = window.location.href;
            console.log(currentGoogleURL);
            var query = googleURLToQuery(currentGoogleURL);
            // var url = $(this).find('cite').html();
            var url = $(this).find('h3.r a').data('href');

            if (url == null) {
                url = $(this).find('h3.r a').attr('href');
            }

            if (url != null) {
                callPythonScript(url, query, obj);
            } else {
                console.log($(this));
            }
        });
    }
}

function googleURLToQuery(url) {
    var patt = new RegExp("#.*");
    var res = patt.exec(url);

    if (res == null) {
        res = url.split("q=")[1];
        res = res.split("&")[0];
    } else {
        res = res[0].indexOf("&") > -1 ? res[0].split("&")[0] : res[0];

        res = res.split("#q=")[1];
    }

    return res;
}

var stillTryingToIterate = true;
var topElement = null;

function deferQuery(method, time) {
    if (window.jQuery) {
        method(iterateOverPageResults, 100);
    } else {
        setTimeout(function() { deferQuery(method, time) }, time);
    }
}

function deferResultIteration(method, time) {
    var currentQuery = googleURLToQuery(window.location.href);
    currentQuery = currentQuery.replace(/\+/g, " ")
    currentQuery = decodeURI(currentQuery);
    var iresDiv = $("#ires");
    var iresQuery = "";

    if (iresDiv != null) {
        if (iresDiv.attr('data-async-context') != null) {
            iresQuery = iresDiv.attr('data-async-context').split("query:")[1];    
            iresQuery = decodeURI(iresQuery);
        }
    }

    if ((iresQuery == currentQuery && $('#flyr[class="flyr-o"]').get(0) == null) || ($('#flyr[class="flyr-c"]').get(0) != null && $('#flyr').get(0) == null)) { //|| $('#flyr[class="flyr-c"]').get(0) != null) $('#flyr').get(0) == null && $('div[class="g"]').get(0) != null && {
        method();
        stillTryingToIterate = false;
    } else {
        stillTryingToIterate = true;
        setTimeout(function() { deferResultIteration(method, time) }, time);
    }
}
