$(document).ready(function() {
    
  const baseURL = "https://api.rawg.io/api/games"
  let nextURL = ``
  let previousURL = ``

  function createButtons() {
    let btnNext = document.createElement('button')
    btnNext.classList.add('btn', 'btn-lg', 'btn-info')
    btnNext.setAttribute('id', 'next')
    btnNext.innerHTML = 'Next'
    let btnPrevious = document.createElement('button')
    btnPrevious.classList.add('btn', 'btn-lg', 'btn-info')
    btnPrevious.setAttribute('id', 'previous')
    btnPrevious.innerHTML = 'Previous'

    if (previousURL) {
      $(".next-prev").append(btnPrevious)
    }
    if (nextURL) {
      $(".next-prev").append(btnNext)
    }
  }

  function populateURLs(response) {
    nextURL = response.data.next
    previousURL = response.data.previous
  }

  function createCards(container, response) {
    for (i=0;i<response.data.results.length;i++) {
      let gameCard = createGameCard(response.data.results[i])
      container.append(gameCard)
    }
  }

  // Generate card HTML
  function createGameCard(game) {
    let gameCard = `
      <div class="card text-center owl-item">
        <img class="card-img-top" width="500px" height="auto" src=${game.background_image} alt="Card image cap">
          <div class="card-body">
            <h5 class="card-title">${game.name}</h5>
            <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
            <a href="./game/${game.id}" class="btn btn-primary">More</a>
          </div>
      </div>
      `
    return gameCard
  }


  // Display search results by sending the form data to Flask and rendering received response on page
  // after the search button has been pressed
  $('#search-form').submit(async function(event) {
    event.stopImmediatePropagation()
    event.preventDefault()

    let $gamesContainer = $('.games')
    $gamesContainer.empty()

    let params = {}
    params['search'] = $('#search')[0].value

    // plain terrible, but it works
    if ($('#publishers')[0].value) {
      params['publishers'] = $('#publishers')[0].value
    }
    if ($('#genres')[0].value) {
      params['genres'] = $('#genres')[0].value   
    }
    if ($('#order_by')[0].value) {
      params['ordering'] = $('#order_by')[0].value
    }
    
    let games = await axios.post("/get-games", { data: {
      'url': baseURL,
       params
    }})

    sessionStorage.setItem('currentPage', baseURL + '?search=' + $('#search')[0].value)

    populateURLs(games)
    createCards($gamesContainer, games)
    createButtons()

  })

  // Functionality for NEXT and PREVIOUS buttons, assigning corresponing links to next and previous URLs
  // This is awful and needs to be rewritten
  $('.next-prev').on('click', 'button', async function(event) {
    event.stopImmediatePropagation()
    event.preventDefault()

    let $gamesContainer = $('.games')
    $gamesContainer.empty()

    let $buttonContainer = $('.next-prev')
    $buttonContainer.empty()

    if (event.target.id === 'next') {
      let games = await axios.get(nextURL)

      sessionStorage.setItem('currentPage', nextURL)

      populateURLs(games)
      createCards($gamesContainer, games)

    }

    else if (event.target.id === 'previous') {
      let games = await axios.get(previousURL)
      sessionStorage.setItem('currentPage', previousURL)

      populateURLs(games)
      createCards($gamesContainer, games)
    
    }    
    
    createButtons()

  })

  // If user left the Search Page during browsing, render the same page he left at
  if (sessionStorage['currentPage']) {
    (async () => {
      let $gamesContainer = $('.games')
      $gamesContainer.empty()
    
      let games = await axios.get(sessionStorage['currentPage'])
        
      createCards($gamesContainer, games)
      populateURLs(games)
      createButtons()

    })()
  }

  // Prevent the dropdown form from closing on click
  $(document).on('click', '.dropdown .dropdown-menu', function(event) {
    event.stopPropagation()
  })

})