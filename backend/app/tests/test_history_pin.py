"""写入时钉选一致性：保存回包、列表摘要、详情打开必须是同一套口径，
且不随后续系统默认择大开关变化。"""

import pytest

from app import seed
from app.repositories import history, settings_repo
from app.services import estimate_service


@pytest.fixture
def isolated_db(monkeypatch, tmp_path):
    db_path = tmp_path / "test_pin.db"
    monkeypatch.setattr("app.db.DB_PATH", db_path)
    seed.init_db()
    return db_path


def _key_parts(result: dict) -> dict:
    return {
        "raw_count": result["raw_count"],
        "base_count": result["base_count"],
        "order_count": result["order_count"],
        "take_max": result["take_max"],
        "waste_pct": result["waste_pct"],
    }


def test_saved_take_max_run_stays_pinned_in_detail_and_list(isolated_db):
    # 客餐厅 6x4.5 + 600x600 + 8% 损耗：面积法 75 片，网格 80 块，择大订货 87 片
    settings_repo.set_values({"take_max": "1"})
    saved = estimate_service.run_estimate(1, 1, 8.0, True, "钉选", take_max=True)
    assert saved["run_id"] is not None
    pinned = _key_parts(saved)
    assert pinned == {
        "raw_count": 75,
        "base_count": 80,
        "order_count": 87,
        "take_max": True,
        "waste_pct": 8.0,
    }

    # 事后把系统默认择大关掉，旧记录详情不得跟着现行默认变
    settings_repo.set_values({"take_max": "0"})

    detail = history.get_run(saved["run_id"])["result"]
    assert _key_parts(detail) == pinned
    assert "pick_mode" not in detail or detail.get("pick_mode") != "area"

    listed = next(r for r in history.list_runs() if r["id"] == saved["run_id"])
    assert _key_parts(listed["result"]) == pinned

    # 详情与列表摘要、写入回包三者同值
    assert detail["order_count"] == listed["result"]["order_count"] == saved["order_count"]
    assert detail["base_count"] == listed["result"]["base_count"] == saved["base_count"]
    assert detail["take_max"] is listed["result"]["take_max"] is saved["take_max"] is True


def test_saved_area_method_run_stays_area_after_default_flips_on(isolated_db):
    settings_repo.set_values({"take_max": "0"})
    saved = estimate_service.run_estimate(1, 1, 8.0, True, "面积法", take_max=False)
    pinned = _key_parts(saved)
    assert pinned["base_count"] == 75
    assert pinned["order_count"] == 81
    assert pinned["take_max"] is False

    settings_repo.set_values({"take_max": "1"})
    detail = history.get_run(saved["run_id"])["result"]
    assert _key_parts(detail) == pinned
    listed = next(r for r in history.list_runs() if r["id"] == saved["run_id"])
    assert _key_parts(listed["result"]) == pinned


def test_fresh_estimate_follows_live_default(isolated_db):
    # 未显式传 take_max 时，当场新测跟随现行默认
    settings_repo.set_values({"take_max": "1"})
    on = estimate_service.run_estimate(1, 1, 8.0, False, "", take_max=None)
    assert on["take_max"] is True
    assert on["order_count"] == 87

    settings_repo.set_values({"take_max": "0"})
    off = estimate_service.run_estimate(1, 1, 8.0, False, "", take_max=None)
    assert off["take_max"] is False
    assert off["order_count"] == 81
