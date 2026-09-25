from app.engines.tile_math import layout_preview, tile_count


def test_guest_room_600_waste8():
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0)
    assert r["area_m2"] == 27.0
    assert r["raw_count"] == 75
    assert r["base_count"] == 75
    assert r["order_count"] == 81
    assert r["layout"]["cols"] == 10
    assert r["layout"]["rows"] == 8
    assert r["layout"]["grid_count"] == 80


def test_layout_preview_small_room():
    lp = layout_preview(2.5, 2.0, 0.6, 0.6)
    assert lp["cols"] == 5
    assert lp["rows"] == 4
    assert lp["grid_count"] == 20


def test_zero_waste():
    r = tile_count(3.0, 3.0, 1.0, 1.0, 0.0)
    assert r["raw_count"] == 9
    assert r["order_count"] == 9


def test_take_max_picks_grid_when_larger():
    # 客餐厅：面积法 75 片，网格 80 块，择大后基数 80，订货 ceil(80*1.08)=87
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0, take_max=True)
    assert r["take_max"] is True
    assert r["raw_count"] == 75
    assert r["layout"]["grid_count"] == 80
    assert r["base_count"] == 80
    assert r["order_count"] == 87


def test_take_max_off_keeps_area_method():
    # 关闭择大：口径与改造前一致，基数即 raw
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0, take_max=False)
    assert r["take_max"] is False
    assert r["base_count"] == 75
    assert r["order_count"] == 81


def test_take_max_corridor():
    # 狭长走廊：面积法 15 片，网格 10x2=20 块，择大订货 ceil(20*1.08)=22
    r = tile_count(8.0, 1.2, 0.8, 0.8, 8.0, take_max=True)
    assert r["raw_count"] == 15
    assert r["layout"]["grid_count"] == 20
    assert r["base_count"] == 20
    assert r["order_count"] == 22


def test_take_max_equal_counts():
    # raw 与 grid 相等时择大不放大
    r = tile_count(3.0, 3.0, 1.0, 1.0, 0.0, take_max=True)
    assert r["base_count"] == 9
    assert r["order_count"] == 9
