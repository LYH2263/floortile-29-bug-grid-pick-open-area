"""钉选一致性：写入回包、历史列表摘要、按编号打开的详情必须是同一套结果，
且不随后续系统默认择大开关的变化而漂移。"""

import pytest

from app import seed
from app.repositories import history, settings_repo
from app.services import estimate_service


@pytest.fixture
def temp_db(monkeypatch, tmp_path):
    monkeypatch.setattr("app.db.DB_PATH", tmp_path / "test.db")
    seed.init_db()


def _run(take_max):
    # 客餐厅 6.0x4.5 + 600x600：面积法 75 片，网格 80 块，损耗 8%
    return estimate_service.run_estimate(
        room_id=1, tile_id=1, waste_pct=8.0, save=True, note="t", take_max=take_max
    )


def test_take_max_detail_matches_list_and_response(temp_db):
    resp = _run(take_max=True)
    run_id = resp["run_id"]

    detail = history.get_run(run_id)
    listed = next(r for r in history.list_runs() if r["id"] == run_id)

    assert resp["take_max"] is True
    assert resp["raw_count"] == 75
    assert resp["base_count"] == 80
    assert resp["order_count"] == 87

    # 详情保持写入时钉选：不得退回只按面积法 raw 套损耗（81）
    assert detail["result"]["take_max"] is True
    assert detail["result"]["base_count"] == 80
    assert detail["result"]["order_count"] == 87
    assert "pick_mode" not in detail["result"]

    # 三处口径完全一致
    assert detail["result"] == listed["result"]
    assert detail["result"]["order_count"] == resp["order_count"]
    assert detail["result"]["base_count"] == resp["base_count"]


def test_detail_pinned_after_live_default_flips(temp_db):
    resp = _run(take_max=True)
    # 写入后改掉系统默认择大开关，旧记录详情仍钉在写入时的结果
    settings_repo.set_values({"take_max": "0"})

    detail = history.get_run(resp["run_id"])
    assert detail["result"]["take_max"] is True
    assert detail["result"]["base_count"] == 80
    assert detail["result"]["order_count"] == 87


def test_take_max_off_detail_matches_area_method(temp_db):
    resp = _run(take_max=False)
    detail = history.get_run(resp["run_id"])
    listed = next(r for r in history.list_runs() if r["id"] == resp["run_id"])

    assert resp["base_count"] == 75
    assert resp["order_count"] == 81
    assert detail["result"]["take_max"] is False
    assert detail["result"] == listed["result"]
    assert detail["result"]["order_count"] == resp["order_count"]
