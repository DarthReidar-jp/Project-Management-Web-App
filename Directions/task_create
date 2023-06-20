私の指示に従い、djangoのコードを実装又は修正してください。
[概要]
プロジェクト管理アプリのタスク作成画面です。

[指示]
・必須入力は、名前のみです。
・開始日が何も入力されていなければ作成日を自動入力
・締切日が何も入力されていなければユニットの締め切り日を自動入力
・タスクアサインメンバーが空欄であれば作成者のみを追加してください
・unit_list画面へ戻るボタンを実装してください
・日程入力のカレンダーをもっと大きくして入力しやすくしてください

[提出物]
あなたは、実装又は修正したhtml,css,javascript,views.py全文を提出してください。

[情報源]
html
{% extends 'app_base.html' %}
{% block title %}タスク作成{% endblock %}
{% block styles %}
{% load static %}
<link rel="stylesheet" type="text/css" href="{% static 'css/task_create.css' %}">
{% endblock %}

{% block content %}
<div class="task-create">
  <h2>タスク作成</h2>
  <form method="post" action="{% url 'task_create' project_id=project_id phase_id=phase_id unit_id=unit_id %}">
    {% csrf_token %}
    <div class="form-group">
      <label for="task-name">タスク名</label>
      <input type="text" id="task-name" name="task_name" required>
    </div>
    <div class="form-group">
      <label for="task-description">タスクの説明</label>
      <textarea id="task-description" name="task_description" rows="4"></textarea>
    </div>
    <div class="form-group">
      <label for="task-deadline">タスク期限</label>
      <input type="date" id="task-deadline" name="task_deadline" required>
    </div>
    <div class="form-group">
      <label for="task-member">タスク割り当てメンバー</label>
      <select id="task-member" name="task_member">
        <option value="">選択してください</option>
        {% for member in project_members %}
          <option value="{{ member.id }}">{{ member.name }}</option>
        {% endfor %}
      </select>
    </div>
    <button type="submit" class="btn-create">作成する</button>
  </form>
</div>
{% endblock %}
    
css
/* task_create.css */
.task-create {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
  }
  
  h2 {
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  label {
    display: block;
    font-weight: bold;
  }
  
  input[type="text"],
  textarea,
  select {
    width: 100%;
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #ccc;
  }
  
  button[type="submit"] {
    padding: 8px 16px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button[type="submit"]:hover {
    background-color: #45a049;
  }
  
  .btn-create {
    background-color: #4CAF50;
  }
  
  .btn-create:hover {
    background-color: #45a049;
  }
  

views
def task_create(request, project_id, phase_id, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)
    project_members = ProjectMember.objects.filter(project_id=project_id)

    if request.method == 'POST':
        task_name = request.POST['task_name']
        task_description = request.POST['task_description']
        task_deadline = request.POST['task_deadline']
        task_member_id = request.POST['task_member']

        task = Task.obAjects.create(
            task_name=task_name,
            task_description=task_description,
            unit=unit,
            start_day=date.today(),
            dead_line=task_deadline
        )

        task_assignment = TaskAssignment.objects.create(
            task=task,
            project_member_id=task_member_id
        )

        return redirect('task_detail', project_id=project_id, phase_id=phase_id, unit_id=unit_id, task_id=task.id)