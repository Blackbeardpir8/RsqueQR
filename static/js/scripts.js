function deleteUser(userId) {
    if (confirm("Are you sure you want to delete this user?")) {
        fetch(`/users/${userId}/delete/`, {
            method: "DELETE",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                alert("User deleted successfully!");
                window.location.reload();
            } else {
                alert("Error: " + data.message);
            }
        })
        .catch(error => console.error("Error:", error));
    }
}

function getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}
