var request_selected = true;
var request = document.getElementById('gql-query');
var response = document.getElementById('response');
var request_api = document.getElementById('request-api');

request.classList.add("bg-light-bunting");
request.classList.add("text-white");
request.classList.add("mr-2");
request.classList.remove("text-light-haiti"); 
request_api.innerHTML = 'curl -X GET http://cysuite.appspot.com/api/subdomain/markgacoka.com'

request.addEventListener('click', requestHandler);
response.addEventListener('click', responseHandler);

function requestHandler(){
    request.classList.add("bg-light-bunting");
    request.classList.add("text-white");
    request.classList.add("mr-2");
    request.classList.remove("text-light-haiti");

    response.classList.remove("bg-light-bunting");
    response.classList.remove("text-white");
    response.classList.remove("mr-2");
    response.classList.add("text-light-haiti");
    request_api.innerHTML = 'curl -X GET http://cysuite.appspot.com/api/subdomain/markgacoka.com'
}

function responseHandler(){
    response.classList.add("bg-light-bunting");
    response.classList.add("text-white");
    response.classList.add("mr-2");
    response.classList.remove("text-light-haiti");

    request.classList.remove("bg-light-bunting");
    request.classList.remove("text-white");
    request.classList.remove("mr-2");
    request.classList.add("text-light-haiti");
    request_api.innerHTML = 
`{
    "_dc-mx.e4730ef3a4d3.markgacoka.com": {
        "headers": "{
            'Connection': 'Keep-Alive', 
            'Content-Type': 'text/html', 
            'Last-Modified': 'Wed, 17 Jun 2020 20:01:33 GMT', 
            'Accept-Ranges': 'bytes', 
            'Content-Length': '163', 
            'Date': 
            'Fri, 26 Nov 2021 03:35:34 GMT'
        }",
        "status": 200,
        "total_time": 0.076472
    },
    "cpanel.markgacoka.com": {
        "headers": "{
            'Connection': 'Keep-Alive', 
            'Content-Type': 'text/html', 
            'Last-Modified': 'Wed, 17 Jun 2020 20:01:33 GMT', 
            'Accept-Ranges': 'bytes', 
            'Content-Length': '163', 
            'Date': 
            'Fri, 26 Nov 2021 03:35:34 GMT'
        }",
        "status": 200,
        "total_time": 0.076472
    },
    "mail.markgacoka.com": {
        "headers": "{
            'Connection': 'Keep-Alive', 
            'Content-Type': 'text/html', 
            'Last-Modified': 'Wed, 17 Jun 2020 20:01:33 GMT', 
            'Accept-Ranges': 'bytes', 
            'Content-Length': '163', 
            'Date': 
            'Fri, 26 Nov 2021 03:35:34 GMT'
        }",
        "status": 200,
        "total_time": 0.076472
    },
    "markgacoka.com": {
        "headers": "{
            'Connection': 'Keep-Alive', 
            'Content-Type': 'text/html', 
            'Last-Modified': 'Wed, 17 Jun 2020 20:01:33 GMT', 
            'Accept-Ranges': 'bytes', 
            'Content-Length': '163', 
            'Date': 
            'Fri, 26 Nov 2021 03:35:34 GMT'
        }",
        "status": 200,
        "total_time": 0.076472
    },
    "webdisk.markgacoka.com": {
        "headers": "{
            'Connection': 'Keep-Alive', 
            'Content-Type': 'text/html', 
            'Last-Modified': 'Wed, 17 Jun 2020 20:01:33 GMT', 
            'Accept-Ranges': 'bytes', 
            'Content-Length': '163', 
            'Date': 
            'Fri, 26 Nov 2021 03:35:34 GMT'
        }",
        "status": 200,
        "total_time": 0.076472
    },
    "webmail.markgacoka.com": {
        "headers": "{
            'Connection': 'Keep-Alive', 
            'Content-Type': 'text/html', 
            'Last-Modified': 'Wed, 17 Jun 2020 20:01:33 GMT', 
            'Accept-Ranges': 'bytes', 
            'Content-Length': '163', 
            'Date': 
            'Fri, 26 Nov 2021 03:35:34 GMT'
        }",
        "status": 200,
        "total_time": 0.076472
    },
    "www.markgacoka.com": {
        "headers": "{
            'Connection': 'Keep-Alive', 
            'Content-Type': 'text/html', 
            'Last-Modified': 'Wed, 17 Jun 2020 20:01:33 GMT', 
            'Accept-Ranges': 'bytes', 
            'Content-Length': '163', 
            'Date': 
            'Fri, 26 Nov 2021 03:35:34 GMT'
        }",
        "status": 200,
        "total_time": 0.076472
    }
}`
}

window.onscroll = function() {
    scrollFunction();
};

function scrollFunction() {
    if (
        document.body.scrollTop > 50 ||
        document.documentElement.scrollTop > 50
    ) {
        $(".site-header--sticky").addClass("scrolling");
    } else {
        $(".site-header--sticky").removeClass("scrolling");
    }
    if (
        document.body.scrollTop > 700 ||
        document.documentElement.scrollTop > 700
    ) {
        $(".site-header--sticky.scrolling").addClass("reveal-header");
    } else {
        $(".site-header--sticky.scrolling").removeClass("reveal-header");
    }
}