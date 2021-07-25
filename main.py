from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float(), nullable=False)


@app.route('/')
def home():
    books = Book.query.all()
    if len(books) == 0:
        empty = True
    else:
        empty = False
    return render_template("index.html", books=books, empty=empty)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        rating = request.form['rating']

        book = Book(title=title, author=author, rating=rating)
        db.session.add(book)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template("add.html")


@app.route("/edit/<int:book_id>", methods=["GET", "POST"])
def edit(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if request.method == "POST":
        new_rating = request.form['rating']
        book.rating = new_rating
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", book=book)


@app.route("/delete/<int:book_id>")
def delete(book_id):
    book = Book.query.filter_by(id=book_id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
