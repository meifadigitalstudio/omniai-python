from app.database import SessionLocal

from app.database.seed import SEEDERS


def main():

    db = SessionLocal()

    try:

        for Seeder in SEEDERS:
            print("=" * 50)
            print(f"Running {Seeder.__name__}")

            Seeder(db).seed()

        print("=" * 50)
        print("All seeds completed successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    main()
