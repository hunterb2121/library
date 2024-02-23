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
    
    const bookTitle = bookElement.querySelector(".book_title");
    if (bookTitle) {
        if (book_width < 3) {
            bookTitle.style.fontSize = "0.8rem";
        } else {
            bookTitle.style.fontSize = "1.2rem";
        }
    }

    if (book_width < 4) {
        bookElement.style.gridTemplateRows = "0.1fr 0.1fr 1fr";
        bookElement.style.gridTemplateAreas = '"delete delete ." "edit edit ." ". title ."';
    }

    const siblingElement = bookElement.nextElementSibling;

    if (siblingElement) {
        siblingElement.style.backgroundColor = bookColor;
        if (book_width < (600 / 55)) {
            siblingElement.style.width = 600 / 55 + "%";
        } else {
            siblingElement.style.width = book_width + "%";
        }
    }
});