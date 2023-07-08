window.addEventListener('DOMContentLoaded', (event) => {
  const params = new URLSearchParams(window.location.search);
  const projectId = params.get('joined_id');

  if (projectId) {
      fetch(`/app/projects/join/?joined_id=${projectId}`)
      .then(response => response.json())
      .then(data => {
          if (data.project) {
              document.getElementById('project-name').textContent = data.project.name;
              document.getElementById('project-description').textContent = data.project.description;

              const joinBtn = document.getElementById('join-btn');
              joinBtn.onclick = function () {
                  window.location.href = `/app/projects/join/?joined_id=${data.project.id}`;
              }
          } else {
              alert('プロジェクトが見つかりませんでした');
          }
      });
  } else {
      alert('プロジェクトIDが指定されていません');
  }
});

