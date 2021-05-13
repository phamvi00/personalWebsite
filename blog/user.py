from flask import(
    Blueprint, render_template, url_for, request, current_app, redirect, g
)
from .db import get_db
from .auth import require_login
import uuid #create a unique string depending on time
import os

bp = Blueprint('user', __name__)

@bp.route('/<int:user_id>/profile', methods= ('GET','POST'))
def profile(user_id):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id={}'.format(user_id)).fetchone()
    return render_template('user/profile.html', user=user)

@bp.route('/upload', methods= ('GET', 'POST'))
@require_login
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = str(uuid.uuid4()) + '.' + f.filename.split('.')[-1]
        savepath = os.path.join(current_app.static_folder, 'uploads', filename)
        f.save(savepath)
        db = get_db()
        db.execute("UPDATE users SET avatar='{}' WHERE id={}".format(url_for('static', filename= os.path.join('uploads/'+filename)), g.user['id']))
        db.commit()
        return redirect(url_for('user.profile', user_id=g.user['id']))
