// Fade header image on scroll
const checkpoint = 300;
var element = document.getElementById("main-body");
var banner = document.getElementById("banner");
window.addEventListener("scroll", () => {
  const currentScroll = window.pageYOffset;
  if (currentScroll <= checkpoint) {
    opacity = 1 - currentScroll / checkpoint;
    element.classList.remove("move-up");
  } else {
    opacity = 0;
    element.classList.add("move-up");
    banner.classList.add("hide");
  }
  document.querySelector(".header-image .img").style.opacity = opacity;
});
