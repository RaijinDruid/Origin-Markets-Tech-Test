from project.app import create_app

config = {
    "SQLALCHEMY_DATABASE_URL": "sqlite:///./sqlite.db",
    "ENV": "development",
    "DEBUG": True,
    "SECRET_KEY": "would-get-from-env-file"
}

app = create_app(config)
app.run(debug=True)
