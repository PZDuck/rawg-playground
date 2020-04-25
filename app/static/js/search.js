$(document).ready(function() {
    
  const baseURL = "https://api.rawg.io/api/games"
  let nextURL = ``
  let previousURL = ``

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

    nextURL = games.data.next
    previousURL = games.data.previous

    for (i=0;i<games.data.results.length;i++) {
      let gameCard = createGameCard(games.data.results[i])
      $gamesContainer.append(gameCard)
    }

    let btnNext = document.createElement('button')
    btnNext.classList.add('btn', 'btn-success')
    btnNext.setAttribute('id', 'next')
    btnNext.innerHTML = 'Next'
    let btnPrevious = document.createElement('button')
    btnPrevious.classList.add('btn', 'btn-success')
    btnPrevious.setAttribute('id', 'previous')
    btnPrevious.innerHTML = 'Previous'

    if (previousURL) {
      $gamesContainer.append(btnPrevious)
    }
    if (nextURL) {
      $gamesContainer.append(btnNext)
    }

  })

  // Functionality for NEXT and PREVIOUS buttons, assigning corresponing links to next and previous URLs
  // This is awful and needs to be rewritten
  $('.games').on('click', 'button', async function(event) {
    event.stopImmediatePropagation()
    event.preventDefault()
    let $gamesContainer = $('.games')
    $gamesContainer.empty()

    if (event.target.id === 'next') {
      let games = await axios.get(nextURL)

      sessionStorage.setItem('currentPage', nextURL)

      nextURL = games.data.next
      previousURL = games.data.previous
            
      for (i=0;i<games.data.results.length;i++) {
        let gameCard = createGameCard(games.data.results[i])
        $gamesContainer.append(gameCard)
      }
    }

    else if (event.target.id === 'previous') {
      let games = await axios.get(previousURL)
      sessionStorage.setItem('currentPage', previousURL)
      nextURL = games.data.next
      previousURL = games.data.previous
        
      for (i=0;i<games.data.results.length;i++) {
        let gameCard = createGameCard(games.data.results[i])
        $gamesContainer.append(gameCard)
      }
    }    
    
    let btnNext = document.createElement('button')
    btnNext.classList.add('btn', 'btn-success')
    btnNext.setAttribute('id', 'next')
    btnNext.innerHTML = 'Next'
    let btnPrevious = document.createElement('button')
    btnPrevious.classList.add('btn', 'btn-success')
    btnPrevious.setAttribute('id', 'previous')
    btnPrevious.innerHTML = 'Previous'

    if (previousURL) {
      $gamesContainer.append(btnPrevious)
    }
    if (nextURL) {
      $gamesContainer.append(btnNext)
    }
  })

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

  // If user left the Search Page during browsing, render the same page he left at
  if (sessionStorage['currentPage']) {
    (async () => {
      let $gamesContainer = $('.games')
      $gamesContainer.empty()
    
      let games = await axios.get(sessionStorage['currentPage'])
        for (i=0;i<games.data.results.length;i++) {
          let gameCard = createGameCard(games.data.results[i])
          $gamesContainer.append(gameCard)
        }

      nextURL = games.data.next
      previousURL = games.data.previous
            
      let btnNext = document.createElement('button')
      btnNext.classList.add('btn', 'btn-success')
      btnNext.setAttribute('id', 'next')
      btnNext.innerHTML = 'Next'
      let btnPrevious = document.createElement('button')
      btnPrevious.classList.add('btn', 'btn-success')
      btnPrevious.setAttribute('id', 'previous')
      btnPrevious.innerHTML = 'Previous'
            
      if (previousURL) {
        $gamesContainer.append(btnPrevious)
      }
      if (nextURL) {
        $gamesContainer.append(btnNext)
      }
    })()
  }
})