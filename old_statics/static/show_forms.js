document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".show_edit_shelf").forEach(button => {
        button.addEventListener("click", function(event) {
            let shelfID = this.parentElement.getAttribute("data-id");
            document.querySelector(`.shelf[data-id="${shelfID}"] .edit_shelf`).style.display = "inline-block";
        });
    });

    document.querySelectorAll(".hide_edit_shelf").forEach(button => {
        button.addEventListener("click", function(event) {
            this.parentElement.style.display = "none";
        });
    });

    document.querySelectorAll(".show_edit_book").forEach(button => {
        button.addEventListener("click", function(event) {
            let bookID = this.parentElement.getAttribute("data-id");
            document.querySelector(`.shelf[data-id="${bookID}"] .edit_book`).style.display = "inline-block";
        });
    });

    document.querySelectorAll(".hide_edit_book").forEach(button => {
        button.addEventListener("click", function(event) {
            this.parentElement.style.display = "none";
        });
    });

    document.querySelectorAll(".show_add_book").forEach(button => {
        button.addEventListener("click", function(event) {
            let shelfID = this.parentElement.getAttribute("data-id");
            document.querySelector(`.shelf[data-id="${shelfID}"] .add_book`).style.display = "inline-block";
        });
    });

    document.querySelectorAll(".hide_add_book").forEach(button => {
        button.addEventListener("click", function(event) {
            this.parentElement.style.display = "none";
        });
    });

    document.querySelectorAll(".show_add_shelf").forEach(button => {
        button.addEventListener("click", function(event) {
            document.querySelector(`.add_shelf`).style.display = "inline-block";
        });
    });

    document.querySelectorAll(".hide_add_shelf").forEach(button => {
        button.addEventListener("click", function(event) {
            document.querySelector(`.add_shelf`).style.display = "none";
        });
    });
});