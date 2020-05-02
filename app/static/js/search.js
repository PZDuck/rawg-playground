$(document).ready(function() {
  const baseURL = "https://api.rawg.io/api/games"
  let nextURL = ``
  let previousURL = ``
  let currentPage = 1

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
            <h4 class="card-title">${game.name}</h5>
            <p class="card-text">${game.tags.map(x => `<span class="badge badge-pill badge-info" style="margin: 0 5px;">${x['name']}</span>`).join('')}</p>
            <a href="./game/${game.id}" class="btn btn-primary more">More</a>
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
    $('.next-prev').empty()
    currentPage = 1
    previousURL = ''
    nextURL = ''
    sessionStorage.clear()
    

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

    let p = new URLSearchParams("");
    
    for (key of Object.keys(params)) {
      p.set(key, params[key])
    }

    p.set('page', currentPage)

    window.history.replaceState({}, '', `${location.pathname}?${p}`)
    sessionStorage.setItem('search', p)

    populateURLs(games)
    createCards($gamesContainer, games)
    createButtons()

  })

  // Functionality for NEXT and PREVIOUS buttons, assigning corresponing links  to next and previous URLs
  // This is awful and needs to be rewritten
  $('.next-prev').on('click', 'button', async function(event) {
    event.stopImmediatePropagation()
    event.preventDefault()

    let $gamesContainer = $('.games')
    $gamesContainer.empty()

    let $buttonContainer = $('.next-prev')
    $buttonContainer.empty()

    if (event.target.id === 'next') {
      let games = await axios.post("/get-games", { data: {
        'url': nextURL,
        'params': ''
      }})

      currentPage++
      sessionStorage.setItem('search', nextURL.split("?")[1])
      window.history.replaceState({}, '', `${location.pathname}?${sessionStorage['search']}`)

      populateURLs(games)
      createCards($gamesContainer, games)

    }

    else if (event.target.id === 'previous') {
      let games = await axios.post("/get-games", { data: {
        'url': previousURL,
        'params': ''
      }})

      currentPage--
      sessionStorage.setItem('search', previousURL.split("?")[1])
      window.history.replaceState({}, '', `${location.pathname}?${sessionStorage['search']}`)

      populateURLs(games)
      createCards($gamesContainer, games)
    
    }    
    
    createButtons()

  })

  // If user left the Search Page during browsing, render the same page he left at
  if (window.location.pathname === '/search' && sessionStorage['search']) {
    (async () => {
      let $gamesContainer = $('.games')
      $gamesContainer.empty()
    
      let games = await axios.post(`/get-games`, { data: {
        'url': `${baseURL}?${sessionStorage['search']}`,
        'params': ''       
      }})

      window.history.replaceState({}, '', `${location.pathname}?${sessionStorage['search']}`)

      createCards($gamesContainer, games)
      populateURLs(games)
      createButtons()

    })()
  }

  // Prevent the dropdown form from closing on click
  $(document).on('click', '.dropdown .dropdown-menu', function(event) {
    event.stopPropagation()
  })

  $('#index-search-form').on('submit', async function(event) {

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

    console.log(jQuery.param(params))
    sessionStorage.setItem('search', jQuery.param(params))
  })

})