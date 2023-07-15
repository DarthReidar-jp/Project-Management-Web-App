document.addEventListener('DOMContentLoaded', function() {
    const searchProjectButton = document.querySelector('.search-project-button');
    searchProjectButton.addEventListener('click', function(event) {
      event.preventDefault(); // Prevent form submission
      const joinedId = document.querySelector('input[name="joined_id"]').value;
      window.location.href = `/app/projects/search/?joined_id=${joinedId}`;
    });
   
    const joinProjectButton = document.querySelector('.join-project-button');
    if (joinProjectButton) { // Check if the button exists
      joinProjectButton.addEventListener('click', function() {
        const projectId = joinProjectButton.getAttribute('data-project-id');
        window.location.href = `/app/projects/join/${projectId}/`;
      });
    }
  });
  