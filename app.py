import pandas as pd
from flask import Flask, request
import util_functions as util


# loading data
books = pd.read_csv("./BX-Books-cleaned.csv", encoding='utf_8', sep=';', on_bad_lines='skip', low_memory=False, encoding_errors='replace')
ratings = pd.read_csv('./BX-Book-Ratings-cleaned.csv', encoding='utf_8', sep=';', on_bad_lines='skip', low_memory=False, encoding_errors='replace')
users = pd.read_csv('./BX-Users-cleaned.csv', encoding='utf_8', sep=';', on_bad_lines='skip', low_memory=False, encoding_errors='replace')


app = Flask(__name__)
app.logger.debug("I've just initialized the Flask app")


@app.route("/")
def index():
    isbn = request.args.get("isbn", "")
    if isbn and isbn not in books['ISBN'].tolist():
        return (
            """<form action="" method="get">
                            <b>Book ISBN:</b> <input type="text" name="isbn">
                            <input type="submit" value="Recommend similar">
                            </form>"""
            + "<br>"
            + "<b><u>Entered ISBN</u>:</b> " + isbn + " (Not found)"
            + "<br><br>"
            + util.get_isbn_list()
        )
    if isbn:
        all_publications = util.get_all_publications(books, isbn)
        readers = util.get_readers(all_publications, ratings)
        similar_books = util.get_similar_books(readers, books, all_publications, ratings)
        result = util.write_output(similar_books, books)
    else:
        result = ""
    i = books[books['ISBN'] == isbn].index
    return (
        """<form action="" method="get">
                        <b>Book ISBN:</b> <input type="text" name="isbn">
                        <input type="submit" value="Recommend similar">
                        </form>"""
        + "<br>"
        + "<b><u>Entered book</u>:</b> " + util.write_book(books, i)
        + "<br><br>"
        + result
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
