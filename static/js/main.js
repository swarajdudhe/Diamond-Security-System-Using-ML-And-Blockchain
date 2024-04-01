const arrows = document.querySelectorAll(".arrow");
const movieLists = document.querySelectorAll(".movie-list");

arrows.forEach((arrow, i) => {
  const itemNumber = movieLists[i].querySelectorAll("img").length;
  let clickCounter = 0;
  arrow.addEventListener("click", () => {
    const ratio = Math.floor(window.innerWidth / 270);
    clickCounter++;
    if (itemNumber - (4 + clickCounter) + (4 - ratio) >= 0) {
      movieLists[i].style.transform = `translateX(${
        movieLists[i].computedStyleMap().get("transform")[0].x.value - 300
      }px)`;
    } else {
      movieLists[i].style.transform = "translateX(0)";
      clickCounter = 0;
    }
  });

  console.log(Math.floor(window.innerWidth / 270));
});

//TOGGLE

const ball = document.querySelector(".toggle-ball");
const items = document.querySelectorAll(
  ".container,.movie-list-title,.navbar-container,.sidebar,.left-menu-icon,.toggle, .box, .footer,.menu-list-item,.profile-text"
);

ball.addEventListener("click", () => {
  items.forEach((item) => {
    item.classList.toggle("active");

  });
  ball.classList.toggle("active");
});


// FAQS
const toggles = document.querySelectorAll('.faq-toggle')

toggles.forEach(toggle => {
    toggle.addEventListener('click', () => {
        toggle.parentNode.classList.toggle('active')
    })
})

// login
const labels = document.querySelectorAll('.form-control label')

labels.forEach(label => {
    label.innerHTML = label.innerText
        .split('')
        .map((letter, idx) => `<span style="transition-delay:${idx * 50}ms">${letter}</span>`)
        .join('')
})


// search button

document.getElementById('searchButton').addEventListener('click', redirectToGoogle);
    document.getElementById('searchInput').addEventListener('keypress', function(event) {
        // Check if Enter key is pressed (keyCode 13)
        if (event.keyCode === 13) {
            redirectToGoogle();
        }
    });

    function redirectToGoogle() {
        // Get the search query from the input field
        var searchQuery = document.getElementById('searchInput').value.trim();

        // Check if search query is not empty
        if (searchQuery !== '') {
            // Construct Google search URL with the search query
            var googleSearchURL = 'https://www.google.com/search?q=' + encodeURIComponent(searchQuery);

            // Redirect user to Google search
            window.location.href = googleSearchURL;
        }
    }


    // buttton click
    function alertt(){
        alert("Please Login for more information")
    }

    // buttton click
    function SocialMedia(){
        alert("Social media link is not available right now")
    }