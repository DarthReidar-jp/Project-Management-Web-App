document.addEventListener("DOMContentLoaded", function() { 
    document.getElementById("addTask").addEventListener("click", function() {
        var taskTableBody = document.getElementById("taskTableBody");
        var rowCount = taskTableBody.rows.length + 1;
        var newRow = taskTableBody.insertRow(-1);
        var cell1 = newRow.insertCell(0);
        var cell2 = newRow.insertCell(1);
        var cell3 = newRow.insertCell(2);
        var cell4 = newRow.insertCell(3); // 追加
        cell1.innerHTML = '<input type="text" name="task_name_' + rowCount + '">';
        cell2.innerHTML = '<textarea name="task_description_' + rowCount + '" rows="2"></textarea>';
        cell3.innerHTML = '<input type="date" name="task_deadline_' + rowCount + '">';

        // メンバーの一覧をプルダウンメニューに表示
        var select = document.createElement('select');
        select.name = 'task_member_' + rowCount;
        members.forEach(function(member) {
            var option = document.createElement('option');
            option.value = member.id;
            option.text = member.name;
            select.appendChild(option);
        });
        cell4.appendChild(select); // 追加
    });
});
