var request_selected = true;
var request = document.getElementById('gql-query');
var response = document.getElementById('response');
var request_api = document.getElementById('request-api');

request.classList.add("bg-light-bunting");
request.classList.add("text-white");
request.classList.add("mr-2");
request.classList.remove("text-light-haiti"); 
request_api.innerHTML = 'curl https://cysuite.io/'

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
    request_api.innerHTML = ' curl -X GET http://cysuite.herokuapp.com/api/users/'
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
`[
    {
        "user_id": "fe0f8512-93d4-4ff0-8664-25b14f1c9de6",
        "username": "admin",
        "email": "admin@cysuite.io",
        "first_name": "Admin",
        "last_name": "Account",
        "date_joined": "2021-11-14T04:17:21.900904Z",
        "last_login": "2021-11-14T04:47:38.779401Z",
        "is_admin": true,
        "is_premium": true,
        "hide_email": true,
        "feedback": ""
    }
]`
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