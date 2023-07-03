//削除ボタンの設定
document.addEventListener('DOMContentLoaded', 
  function() {
      const joinProjectButton = document.querySelector('.join-project-button');
      joinProjectButton.addEventListener('click', function() {
      const modal = new bootstrap.Modal(document.getElementById('projectSearchModal'));
      modal.show();
    });

    const deleteButtons = document.querySelectorAll('.delete-button');

  deleteButtons.forEach(button => {
    button.addEventListener('click', 
    function() {
      const projectId = button.getAttribute('data-project-id');
      showDeleteConfirmationModal(projectId);
    });
  });

  const confirmDeleteButton = document.querySelector('.confirm-delete-button');
  confirmDeleteButton.addEventListener('click', function() {
    const projectId = confirmDeleteButton.getAttribute('data-project-id');
    deleteProject(projectId);
  });
});

//プロジェクト削除の確認モーダルを表示するための関数を呼び出しています。
function showDeleteConfirmationModal(projectId) {
  const modal = new bootstrap.Modal(document.getElementById('deleteProjectModal'));
  const confirmDeleteButton = document.querySelector('.confirm-delete-button');
  confirmDeleteButton.setAttribute('data-project-id', projectId);
  modal.show();
}

//プロジェクトを削除するための関数を呼び出す。
function deleteProject(projectId) {
  const url = `/app/projects/${projectId}/delete/`;
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
  })
    .then(response => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error('削除リクエストが失敗しました。');
      }
    })
    .then(data => {
      if (data.success) {
        location.reload();
      } else {
        throw new Error(data.message);
      }
    })
    .catch(error => {
      console.error(error);
    });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

searchInput.addEventListener('input', function() {
  const searchQuery = searchInput.value;
  window.location.href = `/app/projects/list/?search=${searchQuery}`;  // "app"を追加
});

