// JavaScriptで削除ボタンのクリックイベントを処理する
document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.delete-button');

    deleteButtons.forEach(button => {
      button.addEventListener('click', function() {
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

  // 削除確認アラートモーダルを表示する関数
  function showDeleteConfirmationModal(projectId) {
    const modal = new bootstrap.Modal(document.getElementById('deleteProjectModal'));
    const confirmDeleteButton = document.querySelector('.confirm-delete-button');
    confirmDeleteButton.setAttribute('data-project-id', projectId);
    modal.show();
  }

  // プロジェクトを削除する関数
  function deleteProject(projectId) {
    // Ajaxを使用してプロジェクトを削除するリクエストを送信する
    const url = `/projects/${projectId}/delete/`;
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': '{{ csrf_token }}',  // DjangoのCSRFトークンを取得してヘッダーに追加
      },
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          // プロジェクトの削除に成功した場合、project_listにリダイレクトする
          window.location.href = '/project_list/';
        } else {
          // エラーメッセージを表示するなどの処理
          console.error(data.message);
        }
      })
      .catch(error => {
        console.error(error);
      });
  }