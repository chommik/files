from flask import Flask

from controllers.index import index_page

app = Flask(__name__,
            static_folder="public",
            template_folder="templates")

app.register_blueprint(index_page)
app.debug = True

if __name__ == '__main__':
    app.run()
