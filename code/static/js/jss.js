
let b = [1, 1, 1];
let prices = [12, 8, 9];
totl = 0;
for (let i = 0; i < 3; i++) {
  totl = b[i] * prices[i] + totl;
}
function myFunction(a, c, i) {
  b[i] = b[i] + a;
  if (b[i] < 1) { b[i] = 1; }
  else {
    document.getElementById(c).innerHTML = b[i];
    totl = totl + prices[i] * a;
    document.getElementById(4).innerHTML = "$" + totl;
  }
}
document.getElementById(4).innerHTML = "$" + totl;
document.getElementById(100).style.display = 'block';
function my(i) {
  document.getElementById(30000).style.display = 'none';
  document.getElementById("ordercheckout").style.display = 'none';
  document.getElementById("info").style.display = 'none';
  document.getElementById("40000").style.display = 'block';
  for (el = 100; el < 107; el++) {
    if (el != i) {
      document.getElementById(el).style.display = 'none';
    }
    else {
      document.getElementById(el).style.display = 'block';
    }
  }
}

function ord(el, ee) {
  for (i = 301; i < 303; i++) {
    if (i == el) {
      document.getElementById(30000).style.display = 'block';
      document.getElementById(i).style.display = 'block';
    }
    else {
      document.getElementById(i).style.display = 'none';
    }
  }
}

function or() {
  document.getElementById(30000).style.display = 'none';
  for (i = 301; i < 303; i++) {
    document.getElementById(i).style.display = 'none';
  }
}

function menucate(el) {
  for (i = 1001; i < 1004; i++) {
    if (i == el) {
      document.getElementById(i).style.display = 'block';
    }
    else {
      document.getElementById(i).style.display = 'none';
    }
  }
}

function printt() {
  location.assign("./PrintInvoice/print.html");
}

function feedback() {
  document.getElementById("succes").style.display = 'none';
  document.getElementById("107").style.display = 'block';
}

function gohome() {
  document.getElementById("succes").style.display = 'none';
  document.getElementById("successfeedbacks").style.display = 'none';
  document.getElementById(100).style.display = 'block';
}

function success() {
  var url = '/product/pay/confirm/';
  fetch(url).then(() => {
    var result = confirm("                                          Payment success! \n                                      Do you want feedback?");
    if (result == true) {
      location.assign("./feedback/");

    } else {
      location.assign("../home");
    }
    // window.location.href = "{% url 'product:place-list' %}";
  });

}

function menu() {
  document.getElementById("100").style.display = 'none';
  document.getElementById("101").style.display = 'block';
}

function successfeedback() {
  var c = document.getElementById("sta").children;
  var eva = 0;
  for (let i = c.length - 1; i >= 0; i--) {
    if (c[i].classList.contains('icon-selected')) {
      eva = i + 1;
      break;
    }
  }
  var csrftoken = getCookie('csrftoken');
  var url = '/product/pay/feedback/confirm/';
  fetch(url, {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({ eval: eva, comt: document.getElementById('comment').value })
  }).then(() => {
    alert("Feedback success");
    location.assign("../../home");
  });

}


function typelistr(q) {
  if (q == 1) {
    var add = "typelist";
  }
  else {
    var add = "typelist2";
  }
  if (document.getElementById(add).value == 20001) {
    document.getElementById("20001").style.display = 'block';
    document.getElementById("20002").style.display = 'none';
  }
  else {
    document.getElementById("20002").style.display = 'block';
    document.getElementById("20001").style.display = 'none';
  }

}


function infcustomer() {

}


function creditpay() {
  document.getElementById("creditcard").style.display = 'block';
  document.getElementById("momo").style.display = 'none';
}
function momopay() {
  document.getElementById("creditcard").style.display = 'none';
  document.getElementById("momo").style.display = 'block';
}
function cash() {
  document.getElementById("creditcard").style.display = 'none';
  document.getElementById("momo").style.display = 'none';
}

function reserva(i) {
  document.getElementById("reserve").style.display = 'block';
}

function noreserva() {

  document.getElementById("reserve").style.display = 'none';
  alert("Successful reservation")
}

function ordercheckouton() {
  document.getElementById("ordercheckout").style.display = 'block';
  document.getElementById("info").style.display = 'block';
}


function addneworder() {
  alert("Successfully added order");
}
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}