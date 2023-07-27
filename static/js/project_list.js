document.addEventListener('DOMContentLoaded', 
  function() {
      const joinProjectButton = document.querySelector('.join-project-button');
      joinProjectButton.addEventListener('click', function() {
      const modal = new bootstrap.Modal(document.getElementById('projectSearchModal'));
      modal.show();
    });
});


const searchForm = document.querySelector('.form-size');
searchForm.addEventListener('submit', function(event) {
  event.preventDefault();
  const searchQuery = document.querySelector('input[name="search"]').value;
  window.location.href = `/app/projects/list/?search=${searchQuery}`;  
});


function toggleFavorite(projectId) {
  console.log(`Toggling favorite for project id: ${projectId}`);
  fetch(`/app/toggle_favorite/${projectId}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
    },
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      location.reload();
    } else {
      alert(data.message);
    }
  });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}


