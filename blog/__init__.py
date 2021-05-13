from flask import Flask
from .db import init_app


def create_app():
  app = Flask(__name__)
  app.config["SECRET_KEY"] = "12345"
  app.config['UPLOAD_FOLDER'] = 'static/uploads'#for user photo


  # . is package blog
  from . import auth
  app.register_blueprint(auth.bp, url_prefix = "/auth")

  from . import blog
  app.register_blueprint(blog.bp)
  #direct to the homepage with the link

  from . import user
  app.register_blueprint(user.bp)


  init_app(app)
  #calling to db.py


  return app
