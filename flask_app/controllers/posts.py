from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.post import Post


@app.route('/posts/create', methods=['POST'])
def createPost():
    if not Post.validate_post(request.form):
        return redirect("/dashboard")
    data = {
        'content' : request.form['content'],
        'user_id' : session['id']
    }
    id = Post.save(data)
    session['user_id']= id
    return redirect('/dashboard')

@app.route('/posts_show/<int:id>')
def show(id):
    data ={
        "id": id
    }
    return render_template('dashboard.html', all_posts = Post.get_by_post_id(data))

@app.route('/destroy/posts/<int:id>')
def destroy_post(id):

    Post.destroy(id)

    return redirect('/dashboard')



