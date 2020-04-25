$(document).ready(function() {

  // Get data from form and create a new collection
  $(".create-collection").on('click', async function(event) {
    event.preventDefault()

    await axios.post('/create-collection', { data: {
      'collection_name': $('#name')[0].value,
      'collection_description': $('#description')[0].value,
      'collection_image': $('#image')[0].value,
      'date_created': $('#date_created')[0].value
      }
    })  
  })
})