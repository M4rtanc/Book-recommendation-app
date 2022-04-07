import pandas as pd


def dfcell_to_str(df: pd.DataFrame, index, column: str) -> pd.DataFrame:
    """"Converts DataFrame cell value to plain text."""
    return str(df[column].values[index])[2:-2]


def get_all_publications(df: pd.DataFrame, isbn: str) -> pd.DataFrame:
    """Returns same books with different ISBN."""
    index = df[df['ISBN'] == isbn].index
    name = dfcell_to_str(df, index, 'Book-Title')
    author = dfcell_to_str(df, index, 'Book-Author')
    result = df[(df['Book-Title'] == name) & (df['Book-Author'] == author)]
    return result


def get_readers(books: pd.DataFrame, ratings: pd.DataFrame) -> list[str]:
    """Returns IDs of users who have read and liked the books."""
    isbns = books['ISBN'].tolist()
    result = ratings[(ratings['ISBN'].isin(isbns)) & (ratings['Book-Rating'] >= 5)]
    return result['User-ID'].tolist()


def get_similar_books(readers: list[str], books: pd.DataFrame, orig_publications: pd.DataFrame,
                      ratings: pd.DataFrame) -> pd.DataFrame:
    """Returns sorted ISBNs by average rating and frequency."""
    candidate_isbn = set(ratings[(ratings['User-ID'].isin(readers)) &
                                 (ratings['Book-Rating'] >= 5)]['ISBN'].tolist())
    candidate_isbn = candidate_isbn.intersection(set(books['ISBN'].tolist()))  # not all ISBNs in ratings are also in books
    candidate_isbn = candidate_isbn.difference(set(orig_publications['ISBN'].tolist()))  # filter out books which are same as pattern book

    similar_books = ratings[ratings['ISBN'].isin(candidate_isbn)]
    mean = similar_books.groupby('ISBN').mean().sort_values(by='ISBN')['Book-Rating']
    count = similar_books.groupby('ISBN').count().sort_values(by='ISBN')['Book-Rating']
    dir = {'mean': mean, 'count': count}
    result = pd.DataFrame(dir)
    result.reset_index(inplace=True)
    return result.sort_values(by=['mean', 'count'], ascending=[False, False])


def write_book(books: pd.DataFrame, index) -> str:
    if index.empty:
        return ""
    return "<b>Title: </b>" + dfcell_to_str(books, index, 'Book-Title') + ", <b>Author:</b> " + dfcell_to_str(books, index, 'Book-Author') + ", <b>ISBN:</b> " + dfcell_to_str(books, index, 'ISBN')


def write_output(similar_books: pd.DataFrame, books: pd.DataFrame) -> str:
    if similar_books.shape[0] == 0:
        return "Entered book has no readers."
    result = "<br><b><u>Recommended books</u>:</b><br><br>"
    counter = 0
    for isbn in similar_books["ISBN"]:
        counter += 1
        i = books[books['ISBN'] == isbn].index
        result += "<b>" + str(counter) + ")</b> " + write_book(books, i) + "<br><br>"
        if counter == 15:  # 15 similar books is enough
            break
    return result


def get_isbn_list() -> str:
    f = open('isbn_list.txt', 'r')
    lines = f.read()
    f.close()
    return lines
