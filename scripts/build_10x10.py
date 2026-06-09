import bpy

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
for c in list(bpy.data.collections): bpy.data.collections.remove(c)
for m in list(bpy.data.materials): bpy.data.materials.remove(m)
for m in list(bpy.data.meshes): bpy.data.meshes.remove(m)

H = 3.2
WT = 0.15
WI = 0.10
DH = 2.2
WH = 0.8
WHT = 2.5

W = 10.0; D = 10.0
BW1 = 3.2; BD1 = 1.5
BW2 = 2.0; BD2 = 1.5

SX = W / 2; SY = D / 2
def cx(x): return x - SX
def cy(y): return y - SY

XL, XR = cx(0), cx(W)
YB, YT = cy(0), cy(D)
YTb1 = cy(D + BD1)
XRb2 = cx(W + BD2)

def new_mat(name, r, g, b, a=1.0):
    m = bpy.data.materials.new(name=name)
    m.use_nodes = True
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (r, g, b, a)
    return m

M = {}
M["wall"] = new_mat("牆壁", 0.90, 0.88, 0.85)
M["floor"] = new_mat("地板", 0.82, 0.73, 0.62)
M["door"] = new_mat("門板", 0.72, 0.38, 0.15)
M["window_frame"] = new_mat("窗框", 0.08, 0.08, 0.08)
M["glass"] = new_mat("玻璃", 0.65, 0.88, 0.98, 0.40)
M["glass"].blend_method = 'BLEND'

def new_col(name):
    c = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(c); return c

c_build = new_col("建築")
c_dw = new_col("門窗")

def bx(name, x1, y1, x2, y2, z1, z2, mat, coll):
    mesh = bpy.data.meshes.new(name + "_m")
    vs = [(-0.5,-0.5,-0.5),(0.5,-0.5,-0.5),(0.5,0.5,-0.5),(-0.5,0.5,-0.5),
          (-0.5,-0.5,0.5),(0.5,-0.5,0.5),(0.5,0.5,0.5),(-0.5,0.5,0.5)]
    fs = [(0,1,2,3),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    mesh.from_pydata(vs, [], fs); mesh.update()
    o = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(o)
    o.location = ((x1+x2)*0.5, (y1+y2)*0.5, (z1+z2)*0.5)
    o.scale = (x2-x1, y2-y1, z2-z1)
    if mat:
        o.data.materials.append(mat)
        o.color = mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value[:3] + (1.0,)
    if coll:
        for c in list(o.users_collection): c.objects.unlink(o); coll.objects.link(o)
    return o

def join_objs(objs, name, coll):
    if not objs: return None
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    r = bpy.context.active_object; r.name = name
    for c in list(r.users_collection): c.objects.unlink(r); coll.objects.link(r)
    return r

# ============================================================
# 10x10m 建築 — 三房二廳2衛2陽台
# 分段牆體，無Boolean，每段明確
# 不生成任何家具
# ============================================================
print("=== 10x10m 三房二廳2衛2陽台 ===")

# --- 底牆 (Y=-5.0~-4.85) 大門 X=2.0~3.4 ---
bx("底牆左", XL, YB, cx(7.0), YB+WT, 0, H, M["wall"], c_build)
bx("底牆門上", cx(7.0), YB, cx(8.4), YB+WT, DH, H, M["wall"], c_build)
bx("底牆右", cx(8.4), YB, XR, YB+WT, 0, H, M["wall"], c_build)

# --- 頂牆 (Y=4.85~5.0) 陽台1門 X=-0.45~0.45（0.9m寬，置中於陽台）---
bx("頂牆左", XL, YT-WT, cx(3.4), YT, 0, H, M["wall"], c_build)
bx("頂牆門左", cx(3.4), YT-WT, cx(4.55), YT, 0, H, M["wall"], c_build)
bx("頂牆門上", cx(4.55), YT-WT, cx(5.45), YT, DH, H, M["wall"], c_build)
bx("頂牆門右", cx(5.45), YT-WT, cx(6.6), YT, 0, H, M["wall"], c_build)
bx("頂牆右", cx(6.6), YT-WT, XR, YT, 0, H, M["wall"], c_build)

# --- 左牆 (X=-5.0~-4.85) 三扇窗 ---
# Y=-5.0~-4.0 (BR1窗下)
bx("左1", XL, YB, XL+WT, cy(1.0), 0, H, M["wall"], c_build)
# BR1窗區 Y=-4.0~-2.5: 窗台下+窗頂上
bx("左2a", XL, cy(1.0), XL+WT, cy(2.5), 0, WH, M["wall"], c_build)
bx("左2b", XL, cy(1.0), XL+WT, cy(2.5), WHT, H, M["wall"], c_build)
# Y=-2.5~-1.0 (BR1~BR2間)
bx("左3", XL, cy(2.5), XL+WT, cy(4.0), 0, H, M["wall"], c_build)
# BR2窗區 Y=-1.0~0.5
bx("左4a", XL, cy(4.0), XL+WT, cy(5.5), 0, WH, M["wall"], c_build)
bx("左4b", XL, cy(4.0), XL+WT, cy(5.5), WHT, H, M["wall"], c_build)
# Y=0.5~2.5 (BR2~BR3間)
bx("左5", XL, cy(5.5), XL+WT, cy(7.5), 0, H, M["wall"], c_build)
# BR3窗區 Y=2.5~4.0
bx("左6a", XL, cy(7.5), XL+WT, cy(9.0), 0, WH, M["wall"], c_build)
bx("左6b", XL, cy(7.5), XL+WT, cy(9.0), WHT, H, M["wall"], c_build)
# Y=4.0~5.0 (BR3窗上)
bx("左7", XL, cy(9.0), XL+WT, YT, 0, H, M["wall"], c_build)

# --- 右牆 (X=4.85~5.0) 陽台2門 Y=-4.45~-3.55（0.9m）+ 2窗 ---
bx("右1", XR-WT, YB, XR, cy(0.55), 0, H, M["wall"], c_build)
bx("右門上", XR-WT, cy(0.55), XR, cy(1.45), DH, H, M["wall"], c_build)
bx("右門右", XR-WT, cy(1.45), XR, cy(2.0), 0, H, M["wall"], c_build)
# Y=-3.0~-1.0 (門~窗間)
bx("右3", XR-WT, cy(2.0), XR, cy(4.0), 0, H, M["wall"], c_build)
# 客廳窗區 Y=-1.0~0.5
bx("右4a", XR-WT, cy(4.0), XR, cy(5.5), 0, WH, M["wall"], c_build)
bx("右4b", XR-WT, cy(4.0), XR, cy(5.5), WHT, H, M["wall"], c_build)
# Y=0.5~2.5 (窗間)
bx("右5", XR-WT, cy(5.5), XR, cy(7.5), 0, H, M["wall"], c_build)
# 廚房窗區 Y=2.5~4.0
bx("右6a", XR-WT, cy(7.5), XR, cy(9.0), 0, WH, M["wall"], c_build)
bx("右6b", XR-WT, cy(7.5), XR, cy(9.0), WHT, H, M["wall"], c_build)
# Y=4.0~5.0
bx("右7", XR-WT, cy(9.0), XR, YT, 0, H, M["wall"], c_build)

# --- 陽台1（頂部）---
b1l, b1r = cx((W-BW1)/2), cx((W+BW1)/2)
bx("B1地", b1l, YT, b1r, YTb1, 0, 0.05, M["floor"], c_build)
bx("B1左牆", b1l, YT, b1l+WT, YTb1, 0, 1.1, M["wall"], c_build)
bx("B1右牆", b1r-WT, YT, b1r, YTb1, 0, 1.1, M["wall"], c_build)
bx("B1頂牆", b1l, YTb1-WT, b1r, YTb1, 0, 1.1, M["wall"], c_build)

# --- 陽台2（右側底部）---
b2b, b2t = YB, cy(BW2)
bx("B2地", XR, b2b, XRb2, b2t, 0, 0.05, M["floor"], c_build)
bx("B2前", XR, b2t-WT, XRb2, b2t, 0, 1.1, M["wall"], c_build)
bx("B2右", XRb2-WT, b2b, XRb2, b2t, 0, 1.1, M["wall"], c_build)

# --- 內牆 V1: X=cx(3.5)±WI/2 = -1.55~-1.45 ---
xv1l, xv1r = cx(3.5)-WI/2, cx(3.5)+WI/2
bx("V1a", xv1l, YB, xv1r, cy(0.5), 0, H, M["wall"], c_build)
bx("V1b", xv1l, cy(0.5), xv1r, cy(1.1), DH, H, M["wall"], c_build)
bx("V1c", xv1l, cy(1.1), xv1r, cy(4.0), 0, H, M["wall"], c_build)
bx("V1d", xv1l, cy(4.0), xv1r, cy(4.6), DH, H, M["wall"], c_build)
bx("V1e", xv1l, cy(4.6), xv1r, cy(7.5), 0, H, M["wall"], c_build)
bx("V1f", xv1l, cy(7.5), xv1r, cy(8.1), DH, H, M["wall"], c_build)
bx("V1g", xv1l, cy(8.1), xv1r, YT, 0, H, M["wall"], c_build)

# --- 內牆 V2: X=0.45~0.55, Y=-5.0~-1.5 ---
xv2l, xv2r = cx(5.5)-WI/2, cx(5.5)+WI/2
bx("V2a", xv2l, YB, xv2r, cy(0.5), 0, H, M["wall"], c_build)
bx("V2b", xv2l, cy(0.5), xv2r, cy(1.1), DH, H, M["wall"], c_build)
bx("V2c", xv2l, cy(1.1), xv2r, cy(3.5), 0, H, M["wall"], c_build)

# --- 內牆 V3: X=0.45~0.55, Y=2.0~5.0 ---
bx("V3a", xv2l, cy(7.0), xv2r, cy(7.5), 0, H, M["wall"], c_build)
bx("V3b", xv2l, cy(7.5), xv2r, cy(8.1), DH, H, M["wall"], c_build)
bx("V3c", xv2l, cy(8.1), xv2r, YT, 0, H, M["wall"], c_build)

# --- 內牆 H1: Y=-1.55~-1.45, X=-1.5~5.0 ---
yh1l, yh1r = cy(3.5)-WI/2, cy(3.5)+WI/2
bx("H1a", cx(3.5), yh1l, cx(7.0), yh1r, 0, H, M["wall"], c_build)
bx("H1b", cx(7.0), yh1l, cx(7.6), yh1r, DH, H, M["wall"], c_build)
bx("H1c", cx(7.6), yh1l, XR, yh1r, 0, H, M["wall"], c_build)

# --- 內牆 H2: Y=2.0~2.1, X=-5.0~5.0 ---
yh2l, yh2r = cy(7.0)-WI/2, cy(7.0)+WI/2
bx("H2a", XL, yh2l, cx(0.5), yh2r, 0, H, M["wall"], c_build)
bx("H2b", cx(0.5), yh2l, cx(1.1), yh2r, DH, H, M["wall"], c_build)
bx("H2c", cx(1.1), yh2l, cx(6.5), yh2r, 0, H, M["wall"], c_build)
bx("H2d", cx(6.5), yh2l, cx(7.1), yh2r, DH, H, M["wall"], c_build)
bx("H2e", cx(7.1), yh2l, XR, yh2r, 0, H, M["wall"], c_build)

# --- 地板 ---
bx("地板", XL, YB, XR, YT, 0, 0.05, M["floor"], c_build)

# --- 合併建築 ---
objs = list(c_build.objects)
bpy.ops.object.select_all(action='DESELECT')
for o in objs: o.select_set(True)
bpy.context.view_layer.objects.active = objs[0]
bpy.ops.object.join()
bpy.context.active_object.name = "建築物"
print("建築物完成")

# ============================================================
# 門窗 — 簡潔模型
# ============================================================
print("=== 門窗 ===")

def make_door(name, ox1, oy1, ox2, oy2):
    """在開口位置建立門（門框+門板），直接以開口尺寸填滿"""
    parts = []
    ft = 0.05; mt = 0.01
    def b(n,x1,y1,x2,y2,z1,z2,mat):
        return bx(n, x1, y1, x2, y2, z1, z2, mat, c_dw)
    parts.append(b(f"{name}_框L", ox1, oy1, ox1+ft, oy2, ft, DH-ft, M["door"]))
    parts.append(b(f"{name}_框R", ox2-ft, oy1, ox2, oy2, ft, DH-ft, M["door"]))
    parts.append(b(f"{name}_框T", ox1+ft, oy1, ox2-ft, oy2, DH-ft, DH, M["door"]))
    parts.append(b(f"{name}_框B", ox1+ft, oy1, ox2-ft, oy2, 0, ft, M["door"]))
    parts.append(b(f"{name}_板", ox1+ft+mt, oy1+mt, ox2-ft-mt, oy2-mt, ft+mt, DH-ft-mt, M["door"]))
    return join_objs(parts, name, c_dw)

def make_vwindow(name, ox1, oy1, ox2, oy2):
    """在垂直牆開口建立窗（黑框+淺藍玻璃）"""
    ww = oy2 - oy1
    wd = ox2 - ox1
    wh = WHT - WH
    ft = 0.04; mt = 0.03
    cx0 = (ox1+ox2)/2; cy0 = (oy1+oy2)/2
    # 全部在局部座標以水平方向建立
    parts = []
    def b(n,x1,y1,x2,y2,z1,z2,mat):
        return bx(n, x1, y1, x2, y2, z1, z2, mat, None)
    # 左框、右框：全高
    parts.append(b(f"{name}_框L", -ww/2, -wd/2, -ww/2+ft, wd/2, 0, wh, M["window_frame"]))
    parts.append(b(f"{name}_框R", ww/2-ft, -wd/2, ww/2, wd/2, 0, wh, M["window_frame"]))
    # 上框、下框：僅邊條
    parts.append(b(f"{name}_框T", -ww/2+ft, -wd/2, ww/2-ft, wd/2, wh-ft, wh, M["window_frame"]))
    parts.append(b(f"{name}_框B", -ww/2+ft, -wd/2, ww/2-ft, wd/2, 0, ft, M["window_frame"]))
    # 中柱
    parts.append(b(f"{name}_中柱", -mt/2, -wd/2, mt/2, wd/2, ft, wh-ft, M["window_frame"]))
    # 玻璃
    parts.append(b(f"{name}_玻璃L", -ww/2+ft, -wd*0.3, -mt/2, wd*0.3, ft, wh-ft, M["glass"]))
    parts.append(b(f"{name}_玻璃R", mt/2, -wd*0.3, ww/2-ft, wd*0.3, ft, wh-ft, M["glass"]))
    # 合併後搬入門窗收集
    for p in parts:
        for c in list(p.users_collection): c.objects.unlink(p)
        c_dw.objects.link(p)
    obj = join_objs(parts, name, c_dw)
    bpy.context.view_layer.objects.active = obj; obj.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    obj.rotation_euler = (0, 0, -1.5708 if ox1 < 0 else 1.5708)
    obj.location = (cx0, cy0, (WH+WHT)/2)
    return obj

# 大門
make_door("大門", cx(7.0), YB, cx(8.4), YB+WT)
# 陽台1門
make_door("陽台1門", cx(4.55), YT-WT, cx(5.45), YT)
# 陽台2門
make_door("陽台2門", XR-WT, cy(0.55), XR, cy(1.45))
print("外門完成")

# 內門
xil, xir = cx(3.5)-WI/2, cx(3.5)+WI/2
make_door("BR1門", xil, cy(0.5), xir, cy(1.1))
make_door("BR2門", xil, cy(4.0), xir, cy(4.6))
make_door("BR3門", xil, cy(7.5), xir, cy(8.1))
make_door("Bath1門", xv2l, cy(0.5), xv2r, cy(1.1))
make_door("Bath2門", xv2l, cy(7.5), xv2r, cy(8.1))
make_door("LR門", cx(7.0), yh1l, cx(7.6), yh1r)
make_door("BR2BR3門", cx(0.5), yh2l, cx(1.1), yh2r)
make_door("Kitchen門", cx(6.5), yh2l, cx(7.1), yh2r)
print("內門完成")

# 左牆窗
make_vwindow("BR1窗", XL, cy(1.0), XL+WT, cy(2.5))
make_vwindow("BR2窗", XL, cy(4.0), XL+WT, cy(5.5))
make_vwindow("BR3窗", XL, cy(7.5), XL+WT, cy(9.0))
print("左窗完成")

# 右牆窗
make_vwindow("客廳窗", XR-WT, cy(4.0), XR, cy(5.5))
make_vwindow("廚房窗", XR-WT, cy(7.5), XR, cy(9.0))
print("右窗完成")

for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'MATERIAL'

print("\n=== 建築模型完成（無家具）===")
print("10x10m 三房二廳2衛2陽台")
print("請確認建築模型無誤後，再選擇要生成的家具")
