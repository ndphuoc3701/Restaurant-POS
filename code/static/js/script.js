//Rating Events

$(".rating")
  .on("mouseleave", function() {
    ratingUpdate($(this));
});

$(".rating")
  .children()
  .on("mouseenter", function() {
    starHover($(this));
})
  .on("click", function() {
    applyValue($(this));
    ratingUpdate($(this).parent());
});








//Rating functions

function ratingUpdate(obj) {
  clear(obj);

  var evaluation = $(obj).data("evaluation");
  var loopNext = $(obj).children(":first");

  for (i = 0; i < evaluation; i++) {
    $(loopNext).addClass("icon-selected");
    loopNext = $(loopNext).next();
  }
}


function starHover(obj) {
  clear($(obj).parent());

  //Apply hover effect
  $(obj).addClass("icon-hover");

  //Apply backward trail
  var loopPrev = $(obj).prev();
  while (loopPrev.length) {
    $(loopPrev).addClass("icon-active");
    loopPrev = $(loopPrev).prev();
  }
}




function checkHover(obj) {
  clear($(obj).parent());
  
  var evaluation = $(obj)
    .parent()
    .data("evaluation");
  
  if (evaluation == 0) {
    $(obj)
      .addClass("icon-hover")
      .text(''); //add icon;
  } else if (evaluation == 1) {
    $(obj)
      .addClass("icon-hover")
      .text(''); //remove icon;
  }

  
  //Apply hover effect
  $(obj).addClass("icon-hover");
}



function checkApplyValue(obj) {
  var value = $(obj).data("value");
  var evaluation = $(obj)
    .parent()
    .data("evaluation");

  if (value == evaluation) {
    value = 0; //Reset
    $(obj).text(''); //add icon;
    clear($(obj).parent());
  } else {
    $(obj)
      .removeClass("icon-hover")
      .addClass("icon-active")
      .text(''); //check icon
    burst(obj); //Burst!
  }
  
  //Apply new value
  $(obj)
      .parent()
      .data("evaluation", value);
}




//Function Utils

function clear(obj) {
  //Remove all overrided classes
  $(obj)
    .children()
    .removeClass("icon-hover")
    .removeClass("icon-active")
    .removeClass("icon-selected");
}



function applyValue(obj) {
  var value = $(obj).data("value");
  var evaluation = $(obj)
    .parent()
    .data("evaluation");

  if (value == evaluation) {
    value = 0; //Reset
    clear($(obj).parent());
  } else {
    burst(obj); //Burst!
    $(obj)
      .removeClass("icon-hover")
      .addClass("icon-active");
  }
  
  //Apply new value
  $(obj)
      .parent()
      .data("evaluation", value);
}



function burst(obj) {
$('<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADoAAAA6CAYAAAGWvHq+AAAAAXNSR0IArs4c6QAABGlJREFUaAXtWslPE1EYn4WWlulQQDbRBuouxMSIF+OFk5p4lcSLiTFGbyYuCbTF+IwKGtQDITH8C5w0XryReHRJvIgxBNpSpFgU2VrKFOY5HzpN25mB2ToWnB46733v+37fMm/53ptHEDv6hzEmrXAQVYWr5PRQQHSRPJZrNEgb7sR0tysSAhhUl/AYhNMrHnJHb+TKDrV/cEA9WBHZnUu3voxawi6J1v6GGUZC/CcExCQarVU83DlMW6tR1BZgw0fE8sCBsXKxnPdECG+Mlzxi0SoDB7C8GWZqzLoEg1U38PO9Mbdu4dIQvMvEjomW3Nz+7oiuFPWJan5WKg4WszSPdOAyVDNWuRlewB05tVm7qjbETteqYlRgEtcVheYSIXczE2fMMCXoCiOjETPDjnwMmM5QZawmO63lNxuuQUdEQoc0DGQqQJCZPGsGYA8zeaaHiZ0zA6t4GNDruqrHvaIGxE4dEsuFT6XebnruZySP151T3PdHip8hFIb0/6gbTQF0vVPvHK42El5dSlvP+74bUapKNsiEN52hgq7IFVVAf5lUeYp5ctOdlDBm84YPLOCoYrJJiyFEgJ3aZWS10TVxgBBiwhbvzjTFZbsyw0FJaFdsj1H777qjp4W09JZqHGGIHFfNbDPmRAC2rrnzdXZygHfZ540amlNz9OQVR99HHI50UpoJgjVGJoQ8LdumIiRUJ4ppbPadikoCnrE6J1MxLdb1PmF7GXSHu/TK23LmRmBjaStYhAPu6AUlLT3sxOHCNsjuUdtnZyEd6pKOBESSJPG9pC8OZfjBFq+MJMJ/atJ/PkNfLKT2plriRLxReqBbyFjy9SAz0aDXSNnwqgFbqXYsquGzeewIFCkClnyIA9vh3JRIJz2Ef+kH+tzGFckfRVjdg1QRUaFh2ZFZV2iyyWZGwLSui5qmK7g57jZF0+8fJn1vtBqJquItXDp9maCJl71J/ycleVieV6NOb3kzt6BlCJjmKBgGX9jmElMMWvTNKRlqhP6kdpZdSa2wy6xz4en3xqQWLE2OdgubHFeGdC9T3Fr/0v5ZyGe0KLN57QiYFwFNXdc8tcaQYMu+9mz6IF7LtDrKvSNovnp+K0Tp5l9GIlTzzcenMpdIAjtpinr9INX8UYbNMpJ78AczT6Rxb9e+VyQiecsU24pKKALbcowqxQ95ZuoJnvszHJ3rKTTvz45diaND7dgR/xKrE8F2H03MXv94MiPW7acdgdKIgKTrypnV453cz6/ywnEUduAyarhvuXlUjs8qGpy3L3L8dYqgxjG7/rY3sa/4nxetck5ODxYSB10f8eTAbNpOjwDkmYj9WrtxBvSPnIUlEHWMqEpfRRNVTUYi88YVqXexeqKMTN9b2PtLbj8ackWv8Zin+1b9L0Q5NU/hqsBVniRcj1daBrfivyPcpfYscV6O4PGjZPOMnB1bYRhuh2jrBSmdy+B6PciRg092cDkvh2RJUVM/N8MiEtNUcn1N/31qM4ywMXZABH4Dr7RaLmkYve8AAAAASUVORK5CYII=">')
      .appendTo($(obj))
      .addClass("icon-burst")
      .animate(
        { height: '70px', width: '70px', left: '-75%', top: '-60%', opacity: 0 },
        200,
        "swing",
        function() {
          //...then remove from DOM
          $(this).remove();
        }
      );
}