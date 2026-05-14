let students = JSON.parse(localStorage.getItem("students")) || [];

function saveData() {
    localStorage.setItem("students", JSON.stringify(students));
}

function addStudent() {
    const nameInput = document.getElementById("studentName");
    const name = nameInput.value.trim();

    if (name === "") {
        alert("Enter student name");
        return;
    }

    students.push({ name: name, present: false });
    nameInput.value = "";
    saveData();
    displayStudents();
}

function toggleAttendance(index) {
    students[index].present = !students[index].present;
    saveData();
    displayStudents();
}

function deleteStudent(index) {
    students.splice(index, 1);
    saveData();
    displayStudents();
}

function displayStudents() {
    const list = document.getElementById("attendanceList");
    list.innerHTML = "";

    students.forEach((student, index) => {
        const row = `
            <tr>
                <td>${student.name}</td>
                <td class="${student.present ? 'present' : 'absent'}">
                    ${student.present ? 'Present' : 'Absent'}
                </td>
                <td>
                    <button onclick="toggleAttendance(${index})">
                        Mark ${student.present ? 'Absent' : 'Present'}
                    </button>
                    <button onclick="deleteStudent(${index})" style="background:red;">
                        Delete
                    </button>
                </td>
            </tr>
        `;
        list.innerHTML += row;
    });
}

// Load data on page load
displayStudents();