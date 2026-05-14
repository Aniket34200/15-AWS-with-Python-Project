function showMessage() {
    alert("Hello! You clicked the button.");
}

function greetUser() {
    let name = document.getElementById("name").value;
    document.getElementById("output").innerText = "Hello " + name + "!";
}