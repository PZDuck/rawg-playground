$(document).ready(function() {

  // Get data from form and create a new collection
  $('.create-collection').on('click', async function(event) {
    event.preventDefault()
    await axios.post('/create-collection', { data: {
      'collection_name': $('#collection_name')[0].value,
      'collection_description': $('#description')[0].value,
      'collection_image': $('#image')[0].value,
      'date_created': $('#date_created')[0].value
      }
    })  
    $('#createCollectionModal').modal('hide')

    location.reload()
  })

  $('.collections button').on('click', async function(event) {
    event.preventDefault()

    if (event.target.id === 'delete-collection') {
      await axios.post('/delete-collection', { data: { 
        'collection': $(this)[0].dataset.collection
        }
      })
      event.target.closest('a').remove()    
    } 
    else {
      await axios.post('/toggle-private', { data: { 
          'collection_name': $(this)[0].dataset.collection
        }
      })

      if (event.target.id === 'toggle-private') {
        console.log($(this).siblings('span'))

        $(this).siblings('span')[0].classList.remove('badge-secondary')
        $(this).siblings('span')[0].classList.add('badge-primary')
        $(this).siblings('span')[0].innerHTML = "Private"

        event.target.id = 'toggle-public'
        event.target.innerHTML = 'Unmark private'
        event.target.classList.remove('btn-outline-info')
        event.target.classList.add('btn-outline-warning')
      } else {

        $(this).siblings('span')[0].classList.remove('badge-primary')
        $(this).siblings('span')[0].classList.add('badge-secondary')
        $(this).siblings('span')[0].innerHTML = "Public"

        event.target.id = 'toggle-private'
        event.target.innerHTML = 'Mark private'
        event.target.classList.remove('btn-outline-warning')
        event.target.classList.add('btn-outline-info')
      }
    }
  })
})