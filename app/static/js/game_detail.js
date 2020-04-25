$(document).ready(function() {
  
  // Save selected game to user's personal list
  $('.btn-game').on('click', async function(event) {
    let resp = await axios.post('/save-game', { data: {
      'id': event.target.id
      }
    })
        
      event.target.innerHTML = "Done!"
      event.target.classList.remove('btn-primary')
      event.target.classList.add('btn-success')
  })

  // Add selected game to user's collection of their choice
  $('.add-to-collection').on('click', async function(event) {
    await axios.post('/add-to-collection', { data: {
      'game_id': event.target.id,
      'collection_name': $('#collection-name')[0].value
      }
    })
    $('#add-to-collection-modal').modal('hide')
  })
})