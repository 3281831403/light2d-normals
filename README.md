# 2D 光照：法线、衰减与遮挡

2D 场景里的灯光边缘发灰、遮挡穿帮：法线贴图没有解码，衰减指数固定，聚光边缘没有软过渡，光照叠加没有按强度，射线与线段求交漏掉共线，灯光裁剪用错半径，批次没拆分，法线强度没缩放，颜色没按距离衰减，批量灯光只提交一半。

## 目录结构

```
README.md
conftest.py
.gitignore
render/__init__.py
render/light2d.py
tests/test_light2d.py
```

## 当前状态

`render/light2d.py` 中所有函数只保留签名与文档字符串，函数体统一
`raise NotImplementedError`。`tests/test_light2d.py` 有 15 个参数化用例，
初始全部失败。

## 需要修复的 10 个问题

1. 法线贴图解码到单位向量
2. 距离衰减按指数
3. 聚光内外角软过渡
4. 光照按强度叠加
5. 射线与线段求交
6. 灯光按影响半径裁剪
7. 灯光批次拆分
8. 法线强度缩放
9. 颜色按距离衰减
10. 批量灯光统一提交

## 验收

```bash
python -m pytest -q
```

初始应得到 `15 failed`，且没有 collection error。实现 `render/light2d.py`
后 15 条用例应全部通过。
