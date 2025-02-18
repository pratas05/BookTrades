/*=============== SEARCH ===============*/
const searchButton = document.getElementById('search-button')
      searchClose = document.getElementById('search-close'),
      searchContent = document.getElementById('search-content')

/* ======= SEARCH SHOW ======== */
/* Validate if constant exists */
if(searchButton){
  searchButton.addEventListener('click', () =>{
    searchContent.classList.add('show-search')
  })
}

/* ======= SEARCH HIDDEN ======== */
/* Validate if constant exists */
if(searchClose){
  searchClose.addEventListener('click', () =>{
    searchContent.classList.remove('show-search')
  })
}

/*=============== LOGIN ===============*/
const loginButton = document.getElementById('login-button')
      loginClose = document.getElementById('login-close')
      loginContent = document.getElementById('login-content')
      loginSignUp = document.getElementById('login__signup')

/* ======= LOGIN SHOW ======== */
/* Validate if constant exists */
if(loginButton){
  loginButton.addEventListener('click', () =>{
    loginContent.classList.add('show-login')
  })
}

/* ======= LOGIN HIDDEN ======== */
/* Validate if constant exists */
if(loginClose){
  loginClose.addEventListener('click', () =>{
    loginContent.classList.remove('show-login')
  })
}

if(loginSignUp){
  loginSignUp.addEventListener('click', () =>{
    loginContent.classList.remove('show-login')
  })
}

/*=============== ADD SHADOW HEADER ===============*/
const shadowHeader = () =>{
  const header = document.getElementById('header')
  // When the scroll is greater than 50 viewport height, add the 
  this.scrollY >= 50 ? header.classList.add('shadow-header')
                     : header.classList.remove('shadow-header')
  window.addEventListener('scroll', shadowHeader)                     
}

/*=============== HOME SWIPER ===============*/
let swiperHome = new Swiper('.home__swiper', {
  loop: true,
  spaceBetween: -24,
  grabCursor: true,
  slidesPerView: 'auto',
  centeredSlides: 'auto',

  autoplay: {
    delay: 3000,
    disableOnInteraction: false,
  },

  breakpoints: {
    1220: {
      spaceBetween: -32,
    }
  }


})

/*=============== FEATURED SWIPER ===============*/
let swiperFeatured = new Swiper('.featured__swiper', {
  loop: true,
  spaceBetween: 16,
  grabCursor: true,
  slidesPerView: 'auto',
  centeredSlides: 'auto',


  breakpoints: {
    1150: {
      slidesPerView: 4,
      centeredSlides: false,
    }
  }
})



/*=============== SHOW SCROLL UP ===============*/ 
const scrollUp = () => {
  const scrollToTop = document.getElementById('scroll-up')

  this.scrollY >= 350 ? scrollUp.classList.add('show-scroll')
                      : scrollUp.classList.remove('show-scroll')
}
window.addEventListener('scroll', scrollUp)



/*=============== DARK LIGHT THEME ===============*/ 
const themeButton = document.getElementById('theme-button')
const darkTheme = 'dark-theme'
const iconTheme = 'ri-sun-line'

const selectedTheme = localStorage.getItem('selected-theme')
const selectedIcon = localStorage.getItem('selected-icon')

const getCurrentTheme = () => document.body.classList.contains(darkTheme) ? 'dark' : 'light'
const getCurrentIcon = () => themeButton.classList.contains(iconTheme) ? 'ri-moon-line' : 'ri-sun-line'

if(selectedTheme){
  document.body.classList[selectedTheme === 'dark' ? 'add' : 'remove'](darkTheme)
  themeButton.classList[selectedIcon === 'ri-moon-line'? 'add' :'remove'](iconTheme)
}

themeButton.addEventListener('click', () => {
  document.body.classList.toggle(darkTheme)
  themeButton.classList.toggle(iconTheme)
  localStorage.setItem('selected-theme', getCurrentTheme())
  localStorage.setItem('selected-icon', getCurrentIcon())
})



/*=============== SCROLL REVEAL ANIMATION ===============*/





// Codigo dos generos

// Array de gêneros disponíveis
const genres = [
  "History", "Philosophy", "Science", "Fiction", "Fantasy", "Mystery", "Romance", 
  "Biography", "Self-Help", "Horror", "Thriller", "Adventure", "Science Fiction", 
  "Non-Fiction", "Poetry", "Art", "Children", "Cookbooks", "Graphic Novels"
];

// Referência ao contêiner onde os checkboxes serão inseridos
const genresContainer = document.getElementById('genres-container');

// Função para gerar dinamicamente os checkboxes
function generateGenres() {
  genres.forEach(genre => {
     const genreDiv = document.createElement('div');
     genreDiv.innerHTML = `
        <label>
           <input type="checkbox" name="genre" value="${genre.toLowerCase()}"> ${genre}
        </label>
     `;
     genresContainer.appendChild(genreDiv);
  });
}

// Chama a função para gerar os checkboxes quando a página carregar
generateGenres();
