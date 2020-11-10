from .fhir_server import create_app
from .config import ProductionConfig

if __name__=="__main__":
    create_app().run(debug=True)
