from flaskr import app
from .config import ProductionConfig

app.config.from_object(ProductionConfig)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
