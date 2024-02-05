document.querySelectorAll(".book").forEach(bookElement => {
    const bookColor = bookElement.getAttribute("data-color");

    if (bookColor !== null && bookColor !== undefined) {
        bookElement.style.backgroundColor = bookColor;
    } else {
        bookElement.style.backgroundColor = "white";
    }

    const bookPages = bookElement.getAttribute("data-pages");
    let pages = parseInt(bookPages);

    let book_width = pages / 55;
    bookElement.style.width = book_width + "%";

    const siblingElement = bookElement.nextElementSibling;

    if (siblingElement) {
        siblingElement.style.backgroundColor = bookColor;
        siblingElement.style.width = book_width + "%";
    }
});