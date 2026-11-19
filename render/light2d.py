"""2D 光照：法线、衰减与遮挡：核心实现。"""

import math


def decode_normal(r, g):
    """解码 2D 法线贴图。

    r/g 是 [0, 1] 的贴图采样值，先映射到 [-1, 1]，z 分量由
    ``sqrt(max(0, 1 - x^2 - y^2))`` 还原，得到单位向量。
    """
    x = float(r) * 2.0 - 1.0
    y = float(g) * 2.0 - 1.0
    z_sq = 1.0 - x * x - y * y
    z = math.sqrt(z_sq) if z_sq > 0.0 else 0.0
    return [x, y, z]


def falloff(distance, radius, exponent):
    """距离衰减。

    在光源处为 1，随距离按 ``(1 - d / radius) ** exponent`` 平滑降到 0，
    超出半径（或半径为 0）时为 0。
    """
    if radius <= 0.0:
        return 0.0
    if distance <= 0.0:
        return 1.0
    if distance >= radius:
        return 0.0
    return (1.0 - float(distance) / float(radius)) ** float(exponent)


def cone_mask(angle, inner, outer):
    """聚光内外角软过渡。

    角度取绝对值：不大于 inner 时完全照亮（1.0），不小于 outer 时完全
    为 0，中间用平滑插值过渡，避免硬边。
    """
    a = abs(float(angle))
    inner = float(inner)
    outer = float(outer)
    if a <= inner:
        return 1.0
    if a >= outer:
        return 0.0
    if outer <= inner:
        return 0.0
    t = (a - inner) / (outer - inner)
    return 1.0 - t * t * (3.0 - 2.0 * t)


def blend_light(base, light, intensity):
    """光照按强度叠加。

    叠加量按 intensity 缩放后加到基色上，而不是无条件加满。
    """
    return float(base) + float(light) * float(intensity)


def ray_segment_intersect(origin, direction, a, b):
    """射线与线段求交。

    求 ``origin + t * direction`` 与线段 ``a-b`` 的交点参数 t。
    线段参数 u 落在 [0, 1]（含端点）且 t >= 0 时返回 t；
    平行但共线时返回最近的 t；其余情况返回 -1.0 表示未命中。
    """
    ox, oy = float(origin[0]), float(origin[1])
    dx, dy = float(direction[0]), float(direction[1])
    ax, ay = float(a[0]), float(a[1])
    bx, by = float(b[0]), float(b[1])

    # 线段方向
    sx, sy = bx - ax, by - ay
    # 原点指向线段起点的向量
    qx, qy = ax - ox, ay - oy

    denom = dx * sy - dy * sx
    if denom == 0.0:
        # 平行：共线时退化为线段在射线上的投影区间求最近命中点。
        if dx * qy - dy * qx != 0.0:
            return -1.0
        dir_len_sq = dx * dx + dy * dy
        if dir_len_sq == 0.0:
            return -1.0
        ta = (qx * dx + qy * dy) / dir_len_sq
        tb = ((bx - ox) * dx + (by - oy) * dy) / dir_len_sq
        lo, hi = (ta, tb) if ta <= tb else (tb, ta)
        if hi < 0.0:
            return -1.0
        return lo if lo >= 0.0 else 0.0

    t = (qx * sy - qy * sx) / denom
    u = (qx * dy - qy * dx) / denom

    if t < 0.0 or u < 0.0 or u > 1.0:
        return -1.0
    return t


def _light_position(light):
    """取出灯光的位置，兼容点、字典与带 position 属性的对象。"""
    if isinstance(light, dict):
        return light.get("position", light)
    position = getattr(light, "position", None)
    if position is not None:
        return position
    return light


def cull_lights(position, radius, lights):
    """按影响半径裁剪灯光。

    返回影响范围与查询圆相交的灯光下标（升序）。距离等于半径视为命中。
    """
    px, py = float(position[0]), float(position[1])
    radius = float(radius)
    hits = []
    for i, light in enumerate(lights):
        lp = _light_position(light)
        lx, ly = float(lp[0]), float(lp[1])
        d = math.hypot(lx - px, ly - py)
        if d <= radius:
            hits.append(i)
    return hits


def batch_count(count, max_batch):
    """灯光批次拆分。

    每个批次至多 max_batch 盏灯，向上取整得到批次数。
    """
    count = int(count)
    max_batch = int(max_batch)
    if count <= 0:
        return 0
    if max_batch <= 0:
        raise ValueError("max_batch must be positive")
    return (count + max_batch - 1) // max_batch


def normal_strength(normal, strength):
    """法线强度缩放。

    只缩放切线方向（x/y）分量，保留 z 分量不变。
    """
    s = float(strength)
    return [float(normal[0]) * s, float(normal[1]) * s, float(normal[2])]


def attenuate_color(color, distance, radius):
    """颜色按距离衰减。

    与距离衰减一致：在光源处保持原色，到影响半径处线性衰减到 0。
    """
    if radius <= 0.0:
        factor = 0.0
    elif distance <= 0.0:
        factor = 1.0
    elif distance >= radius:
        factor = 0.0
    else:
        factor = 1.0 - float(distance) / float(radius)
    return [float(c) * factor for c in color]


def _iter_statuses(statuses):
    """递归展开批次，产出单个状态值。"""
    for item in statuses:
        if isinstance(item, (list, tuple, set)):
            yield from _iter_statuses(item)
        else:
            yield item


def commit_lights(statuses):
    """批量灯光全部成功才提交。

    只有所有批次、所有灯光都成功时才返回 True。
    """
    return all(bool(s) for s in _iter_statuses(statuses))
