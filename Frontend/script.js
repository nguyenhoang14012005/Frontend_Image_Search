//index
let slideIndex = 1;
let intervalId;
const intervalTime = 3000;

function showSlides(n) {
    let slides = document.getElementsByClassName("slides");
    let dots = document.getElementsByClassName("dot");

    if (n > slides.length) slideIndex = 1;
    if (n < 1) slideIndex = slides.length;

    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (let i = 0; i < dots.length; i++) {
        dots[i].classList.remove("active");
      }

    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].classList.add("active");
}

function plusSlides(n) {
    showSlides(slideIndex += n);
    resetInterval();
}

function currentSlide(n) {
    showSlides(slideIndex = n);
    resetInterval();
}

function startInterval() {
    intervalId = setInterval(() => plusSlides(1), intervalTime);
}

function resetInterval() {
    clearInterval(intervalId);
    startInterval();
}

document.addEventListener("DOMContentLoaded", () => {
    showSlides(slideIndex);
    startInterval();
});