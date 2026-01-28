from backend.db.schema import init_db

if __name__ == "__main__":
    init_db("data/app.db")
    print("DB initialized at data/app.db", flush=True)

