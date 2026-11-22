import os

from flask import Flask, render_template

from app.controllers.auth_controller import auth_bp
from app.controllers.health_controller import health_bp
from app.controllers.perfil_controller import perfil_bp
from app.controllers.personalizacao_controller import personalizacao_bp
from app.utils.auth_middleware import registrar_middlewares



def create_app():
    app = Flask(
        __name__,
        template_folder="views",
        static_folder="static"
    )

    app.secret_key = os.environ.get(
        "SECRET_KEY",
        "chave-desenvolvimento-altere-em-producao"
    )

    app.register_blueprint(auth_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(perfil_bp)
    app.register_blueprint(personalizacao_bp)

    registrar_middlewares(app)

    @app.errorhandler(404)
    def not_found(error):
        app.logger.warning("Página 404: %s", error)
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error("Erro interno: %s", error)
        return "Erro interno do servidor.", 500

    return app