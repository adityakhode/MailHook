function nameValidation(){
    // Clear previous error messages
    document.getElementById("nameError").textContent = "";
    const name = document.getElementById("name").value;

    let isValid = true;

    // Name validation
    const nameRegex = /^[A-Za-z\s]+$/;
    if (!nameRegex.test(name)) {
        document.getElementById("nameError").textContent = "Name must contain only letters and spaces.";
        isValid = false;
    }
    return isValid; 
}

function emailValidation(){
    document.getElementById("emailError").textContent = "";
    const email = document.getElementById("email").value;

    let isValid = true;
    // Email validation
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailRegex.test(email)) {
        document.getElementById("emailError").textContent = "Please enter a valid email address (e.g., asdfgh@fghj.com).";
        isValid = false;
    }
    return isValid; 
}

function validateForm() {
    const isNameValid = nameValidation();
    const isEmailValid = emailValidation();
    const submitButton = document.getElementById('submitButton');
    // Enable or disable the submit button based on validation
    if (isNameValid && isEmailValid) {
        submitButton.disabled = false;
    } else {
        submitButton.disabled = true;
    }
}