from app.data.seed import seed_database
from app.services.analytics import dashboard


def test_dashboard_has_demo_data():
    seed_database(force=True)
    data = dashboard()
    assert data["summary"]["projects"] >= 1
    assert data["summary"]["customers"] >= 1
    assert data["summary"]["forecast"] >= 50
