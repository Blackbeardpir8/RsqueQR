document.addEventListener("DOMContentLoaded", function () {
    fetchUsers();
});

// Fetch Users
function fetchUsers() {
    fetch("http://127.0.0.1:8000/api/users/")
        .then(response => response.json())
        .then(data => {
            let table = document.getElementById("user-table");
            table.innerHTML = "";
            data.data.forEach(user => {
                let row = `
                    <tr>
                        <td>${user.first_name} ${user.last_name}</td>
                        <td>${user.phone_number}</td>
                        <td>
                            <a href="user_detail.html?id=${user.id}">View</a>
                            <button onclick="deleteUser(${user.id})">Delete</button>
                        </td>
                    </tr>`;
                table.innerHTML += row;
            });
        })
        .catch(error => console.log("Error fetching users:", error));
}

// Delete User
function deleteUser(userId) {
    fetch(`http://127.0.0.1:8000/api/users/${userId}/`, {
        method: "DELETE",
    })
    .then(response => {
        if (response.status === 204) {
            alert("User deleted successfully");
            fetchUsers(); // Refresh user list
        } else {
            alert("Error deleting user");
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("user-form");

    if (form) {
        form.addEventListener("submit", function (event) {
            event.preventDefault();
            createUser();
        });
    }
});

// Create User Function
function createUser() {
    const first_name = document.getElementById("first_name").value;
    const last_name = document.getElementById("last_name").value;
    const phone_number = document.getElementById("phone_number").value;
    const email = document.getElementById("email").value;

    fetch("http://127.0.0.1:8000/api/users/create/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            first_name: first_name,
            last_name: last_name,
            phone_number: phone_number,
            email: email
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            document.getElementById("message").innerText = "User created successfully!";
            document.getElementById("user-form").reset();
        } else {
            document.getElementById("message").innerText = "Error: " + JSON.stringify(data.error);
        }
    })
    .catch(error => console.log("Error:", error));
}
