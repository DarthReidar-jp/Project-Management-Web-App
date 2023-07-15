document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("addTask").addEventListener("click", async function() {
        var taskTableBody = document.getElementById("taskTableBody");
        var rowCount = taskTableBody.rows.length + 1;
        var newRow = taskTableBody.insertRow(-1);
        var cell1 = newRow.insertCell(0);
        var cell2 = newRow.insertCell(1);
        var cell3 = newRow.insertCell(2);
        var cell4 = newRow.insertCell(3);
        cell1.innerHTML = '<input type="text" name="task_name_' + rowCount + '">';
        cell2.innerHTML = '<textarea name="task_description_' + rowCount + '" rows="2"></textarea>';
        cell3.innerHTML = '<input type="date" name="task_deadline_' + rowCount + '">';

        // Fetch project members asynchronously
        var formElement = document.getElementById('unitForm');
        var projectId = formElement.dataset.projectId;
        var members = await fetchProjectMembers(projectId);

        // Create a select element
        var select = document.createElement('select');
        select.name = "task_member_" + rowCount;

        // Create an option element for each project member
        members.forEach(function(member) {
            var option = document.createElement('option');
            option.value = member.id;
            option.text = member.name;
            select.appendChild(option);
        });

        // Add the select element to the new cell
        cell4.appendChild(select);
    });
});

async function fetchProjectMembers(projectId) {
    let response = await fetch(`/app/api/project-members/${projectId}`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    } else {
        let data = await response.json();
        return data;
    }
}

