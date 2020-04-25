$(document).ready(function() {

  // Save selected game to user's personal list
  $('.details').on('click', async function(event) {
    let gameBtn = $('#btn-game')[0]
    if (event.target.dataset.action === 'add') {
      let resp = await axios.post('/save-game', { data: {
        'id': event.target.dataset.gameid,
        'status': $('#status :selected').val()
        }
      })

      toggleButtonToRemove()
      $('#add-game-modal').modal('hide')


    } else if (event.target.dataset.action === 'remove') {
      let resp = await axios.post('/save-game', { data: {
        'id': event.target.dataset.gameid
        }
      })

      toggleButtonToAdd()
    }
  })

  // Add selected game to user's collection of their choice
  $('.add-to-collection').on('click', async function(event) {
    await axios.post('/add-to-collection', { data: {
      'game_id': event.target.dataset.gameid,
      'collection_name': $('#collection-name')[0].value
      }
    })

    $('#add-to-collection-modal').modal('hide')
  })

  // Util funcs
  function toggleButtonToAdd() {
    let gameBtn = $('#btn-game')[0]
    gameBtn.classList.remove('btn-danger')  
    gameBtn.classList.add('btn-primary')
    gameBtn.innerHTML = "Add to My Games"      
    gameBtn.setAttribute('data-action', 'add')
    gameBtn.setAttribute('data-toggle', 'modal')
    gameBtn.setAttribute('data-target', '#add-game-modal')
  }

  function toggleButtonToRemove() {
    let gameBtn = $('#btn-game')[0]
    gameBtn.classList.remove('btn-primary')
    gameBtn.classList.add('btn-danger')
    gameBtn.innerHTML = "Remove from games"
    gameBtn.setAttribute('data-action', 'remove')
    gameBtn.removeAttribute('data-toggle')
  }

})