"""2D 光照：法线、衰减与遮挡：待实现的核心模块。"""


def decode_normal(r, g):
    """解码 2D 法线贴图。"""
    raise NotImplementedError

def falloff(distance, radius, exponent):
    """距离衰减。"""
    raise NotImplementedError

def cone_mask(angle, inner, outer):
    """聚光内外角软过渡。"""
    raise NotImplementedError

def blend_light(base, light, intensity):
    """光照按强度叠加。"""
    raise NotImplementedError

def ray_segment_intersect(origin, direction, a, b):
    """射线与线段求交。"""
    raise NotImplementedError

def cull_lights(position, radius, lights):
    """按影响半径裁剪灯光。"""
    raise NotImplementedError

def batch_count(count, max_batch):
    """灯光批次拆分。"""
    raise NotImplementedError

def normal_strength(normal, strength):
    """法线强度缩放。"""
    raise NotImplementedError

def attenuate_color(color, distance, radius):
    """颜色按距离衰减。"""
    raise NotImplementedError

def commit_lights(statuses):
    """批量灯光全部成功才提交。"""
    raise NotImplementedError
