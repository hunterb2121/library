document.querySelectorAll(".hidden_button").forEach(button => {
    button.addEventListener("click", function() {
        if (this.nextElementSibling.style.display == "none" || this.nextElementSibling.style.display == "") {
            this.nextElementSibling.style.display = "block";
        } else {
            this.nextElementSibling.style.display = "none";
        }
    });
});
