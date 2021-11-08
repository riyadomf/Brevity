from flask import Flask, render_template, url_for

app = Flask(__name__)


posts = [
    {
        'author': 'Riyad', 
        'title': 'Blog post 1',
        'content': 'First post content',
        'date_posted': 'November 1, 2021'
    },
    {
        'author': 'Nowshad', 
        'title': 'Blog post 2',
        'content': 'Second post content',
        'date_posted': 'November 1, 2021'
    }
]

@app.route("/")
@app.route("/home")
def hello():
    return render_template('home.html', posts = posts)

@app.route("/about")
def about():
    return render_template('about.html', title = 'About')

if __name__ == '__main__':
    app.run(debug=True)