$(document).ready(function() {

  // Get data from form and create a new collection
  $(".create-collection").on('click', async function(event) {
    event.preventDefault()

    collectionName = $('#name')[0].value
    collectionDescription = $('#description')[0].value
    collectionImg = $('#image')[0].value
    date_created = $('#date_created')[0].value

    await axios.post('/create-collection', { data: {
      'collection_name': collectionName,
      'collection_description': collectionDescription,
      'collection_image': collectionImg,
      'date_created': date_created
      }
    })  
  })
})