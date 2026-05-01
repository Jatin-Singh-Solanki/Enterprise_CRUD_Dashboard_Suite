from app.data.seed import seed_database

if __name__ == "__main__":
    seed_database(force=True)
    print("AtlasNexus ProSuite database reset successfully")
