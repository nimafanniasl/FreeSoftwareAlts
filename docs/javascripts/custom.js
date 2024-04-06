document.addEventListener("DOMContentLoaded", function() {
  externalLinks();
  var lazyLoadInstance = new LazyLoad({
  });
});


function externalLinks() {
    for(var c = document.getElementsByTagName("a"), a = 0;a < c.length;a++) {
      var b = c[a];
      b.getAttribute("href") && b.hostname !== location.hostname && (b.target = "_blank")
    }
}