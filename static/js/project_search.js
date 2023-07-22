document.addEventListener('DOMContentLoaded', function() {
  const searchProjectButton = document.querySelector('.search-project-button');
  searchProjectButton.addEventListener('click', function(event) {
    event.preventDefault(); // Prevent form submission
    const joinedId = document.querySelector('input[name="joined_id"]').value;
    window.location.href = `/app/projects/search/?joined_id=${joinedId}`;
  });

  const joinProjectButton = document.getElementById('join-project-button');
  if (joinProjectButton) { // Check if the button exists
    console.log("Join project button found."); // Debug log
    joinProjectButton.addEventListener('click', function() {
      const projectId = joinProjectButton.getAttribute('data-project-id');
      console.log(`Project ID: ${projectId}`); // Debug log
      if (projectId) {
          window.location.href = `/app/projects/join/${projectId}/`;
      } else {
          console.log('Failed to get project ID.'); // Debug log
      }
    });
  } else {
    console.log("Join project button not found."); // Debug log
  }
});
