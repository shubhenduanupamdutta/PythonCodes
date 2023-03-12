from flask import Flask, render_template, request
from post import *
from datetime import datetime
from send_mail import *


app = Flask(__name__)
all_blog_post = Post().get_data()
# print(all_blog_post)
# Create a dictionary with id as keys to refer in get_individual_post
all_blogs = { post["id"]: post for post in all_blog_post}
current_year = datetime.now().year


@app.route('/')
@app.route('/index.html')
@app.route('/index')
@app.route('/home')
def main_page():  # put application's code here
    return render_template("index.html", all_post=all_blog_post, year=current_year)


@app.route('/about')
def about_page():
    return render_template("about.html", year=current_year)


@app.route('/contact', methods=["GET", "POST"])
def contact_page():
    if request.method == "POST":
        msg = "Subject: New Message from my blog. \n\n"
        msg += f"Name: {request.form['name']} \n"
        msg += f"Email ID: {request.form['email']} \n"
        msg += f"Phone Number: {request.form['phone_number']} \n"
        msg += f"Message: {request.form['message']}"
        send_me_mail(msg)
        return render_template("contact.html", year=current_year, success_msg=True)

    return render_template("contact.html", year=current_year, success_msg=False)

@app.route("/post/<int:blog_id>")
def individual_post(blog_id):
    return render_template("post.html", blog_post=all_blogs[blog_id], year=current_year)


if __name__ == '__main__':
    app.run(debug=True)
