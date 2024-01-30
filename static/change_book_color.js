document.querySelectorAll(".book").forEach(bookElement => {
    const bookColor = bookElement.getAttribute("data-color");

    if (bookColor !== null && bookColor !== undefined) {
        bookElement.style.backgroundColor = bookColor;
    } else {
        bookElement.style.backgroundColor = "white";
    }
});