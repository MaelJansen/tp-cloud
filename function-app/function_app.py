import azure.functions as func

from shared.api import games_bp, users_bp
from shared.functions import import_rawg_data

app = func.FunctionApp()

for bp in [users_bp, games_bp]:
    app.register_blueprint(bp)


# @app.function_name(name="data-collector")
# @app.schedule(schedule="0 0 * * 1", arg_name="timer", run_on_startup=False)
# def rawg_automatic_data_collector(timer: func.TimerRequest) -> None:
    import_rawg_data()


# Décommentez ce bloc si jamais vous souhaitez exécuter du code de manière indépendante de la Function App,
# directement dans votre interpréteur Python.
# if __name__ == '__main__':
#     from shared.utils import load_settings_file
#     from shared.context import Context
#
#     load_settings_file()
#     Context.initialize()
#
#     # Faites vos appels de fonctions ici
#     import_rawg_data()
