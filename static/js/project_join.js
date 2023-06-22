document.getElementById('search-btn').addEventListener('click', function() {
    var invitationId = document.getElementById('invitation-id').value;
    fetch(`/app/projects/join/?invitation_id=${invitationId}`)
      .then(response => response.json())
      .then(data => {
        var searchResults = document.getElementById('search-results');
        searchResults.innerHTML = '';
        if (data.project) {
          var tile = document.createElement('div');
          tile.innerHTML = `<h3>${data.project.name}</h3>
                            <p>${data.project.responsible}</p>
                            <button onclick="location.href='/app/projects/join/?invitation_id=${data.project.id}'">参加する</button>`;
          searchResults.appendChild(tile);
        } else {
          searchResults.innerText = 'プロジェクトが見つかりませんでした';
        }
      });
  });
