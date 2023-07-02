document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("addTask").addEventListener("click", function() {
        var taskTableBody = document.getElementById("taskTableBody");
        var rowCount = taskTableBody.rows.length + 1;
        var newRow = taskTableBody.insertRow(-1);
        var cell1 = newRow.insertCell(0);
        var cell2 = newRow.insertCell(1);
        var cell3 = newRow.insertCell(2);
        cell1.innerHTML = '<input type="text" name="task_name_' + rowCount + '">';
        cell2.innerHTML = '<textarea name="task_description_' + rowCount + '" rows="2"></textarea>';
        cell3.innerHTML = '<input type="date" name="task_deadline_' + rowCount + '">';
    });
});