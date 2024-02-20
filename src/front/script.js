document.getElementById("registration-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const requestData = Object.fromEntries(formData.entries());
    try {
        const response = await fetch("http://localhost:8000/api/auth/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(requestData)
        });
        if (response.ok) {
            alert("Registration successful!");
            // Redirect to another page or perform other actions
        } else {
            const errorData = await response.json();
            alert(`Registration failed: ${errorData.detail}`);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred. Please try again later.");
    }
});
