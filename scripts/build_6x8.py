import bpy

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
for c in list(bpy.data.collections): bpy.data.collections.remove(c)
for m in list(bpy.data.materials): bpy.data.materials.remove(m)
for m in list(bpy.data.meshes): bpy.data.meshes.remove(m)

H = 3.2; WT = 0.15; WI = 0.10; DH = 2.2; WH = 0.8; WHT = 2.5
W = 6.0; D = 8.0; BW = 4.5; BD = 1.5
SX = W/2; SY = D/2
def cx(x): return x - SX
def cy(y): return y - SY

XL, XR = cx(0), cx(W); YB, YT = cy(0), cy(D)
XRb = cx(W + BD)

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

c_build = new_col("建築"); c_dw = new_col("門窗")

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
# 6x8m 建築 — 2房1廳1衛1陽台
# ============================================================
print("=== 6x8m 2房1廳1衛1陽台 ===")

# --- 底牆 (Y=-4~-3.85) 大門 X=0.5~1.9 ---
bx("底牆左", XL, YB, cx(3.5), YB+WT, 0, H, M["wall"], c_build)
bx("底牆門上", cx(3.5), YB, cx(4.9), YB+WT, DH, H, M["wall"], c_build)
bx("底牆右", cx(4.9), YB, XR, YB+WT, 0, H, M["wall"], c_build)

# --- 頂牆 (Y=3.85~4) 衛浴窗 X=0.5~2.0 ---
bx("頂牆左", XL, YT-WT, cx(3.5), YT, 0, H, M["wall"], c_build)
bx("頂牆窗下", cx(3.5), YT-WT, cx(5.0), YT, 0, WH, M["wall"], c_build)
bx("頂牆窗上", cx(3.5), YT-WT, cx(5.0), YT, WHT, H, M["wall"], c_build)
bx("頂牆右", cx(5.0), YT-WT, XR, YT, 0, H, M["wall"], c_build)

# --- 左牆 (X=-3~-2.85) BR1窗 Y=-3~-1.5, BR2窗 Y=0.5~2.0 ---
bx("左1", XL, YB, XL+WT, cy(1), 0, H, M["wall"], c_build)
bx("左2a", XL, cy(1), XL+WT, cy(2.5), 0, WH, M["wall"], c_build)
bx("左2b", XL, cy(1), XL+WT, cy(2.5), WHT, H, M["wall"], c_build)
bx("左3", XL, cy(2.5), XL+WT, cy(4.5), 0, H, M["wall"], c_build)
bx("左4a", XL, cy(4.5), XL+WT, cy(6.0), 0, WH, M["wall"], c_build)
bx("左4b", XL, cy(4.5), XL+WT, cy(6.0), WHT, H, M["wall"], c_build)
bx("左5", XL, cy(6.0), XL+WT, YT, 0, H, M["wall"], c_build)

# --- 右牆 (X=2.85~3) 陽台門 Y=-2.2~-1.3 + 廚房窗 Y=1.0~2.3 ---
bx("右1", XR-WT, YB, XR, cy(1.8), 0, H, M["wall"], c_build)
bx("右門上", XR-WT, cy(1.8), XR, cy(2.7), DH, H, M["wall"], c_build)
bx("右2", XR-WT, cy(2.7), XR, cy(5.0), 0, H, M["wall"], c_build)
bx("右3a", XR-WT, cy(5.0), XR, cy(6.3), 0, WH, M["wall"], c_build)
bx("右3b", XR-WT, cy(5.0), XR, cy(6.3), WHT, H, M["wall"], c_build)
bx("右4", XR-WT, cy(6.3), XR, YT, 0, H, M["wall"], c_build)

# --- 內牆 V1: X=cx(3)=0±0.05 ---
xv1l, xv1r = cx(3)-WI/2, cx(3)+WI/2
bx("V1a", xv1l, YB, xv1r, cy(1.5), 0, H, M["wall"], c_build)
bx("V1b", xv1l, cy(1.5), xv1r, cy(2.1), DH, H, M["wall"], c_build)
bx("V1c", xv1l, cy(2.1), xv1r, cy(5.5), 0, H, M["wall"], c_build)
bx("V1d", xv1l, cy(5.5), xv1r, cy(6.1), DH, H, M["wall"], c_build)
bx("V1e", xv1l, cy(6.1), xv1r, YT, 0, H, M["wall"], c_build)

# --- 內牆 H1: Y=cy(4.5)=0.5±0.05, X=0~3 ---
yh1l, yh1r = cy(4.5)-WI/2, cy(4.5)+WI/2
bx("H1a", cx(3), yh1l, cx(4.0), yh1r, 0, H, M["wall"], c_build)
bx("H1b", cx(4.0), yh1l, cx(4.6), yh1r, DH, H, M["wall"], c_build)
bx("H1c", cx(4.6), yh1l, XR, yh1r, 0, H, M["wall"], c_build)

# --- 內牆 H2: Y=cy(6.5)=2.5±0.05, X=0~3 ---
yh2l, yh2r = cy(6.5)-WI/2, cy(6.5)+WI/2
bx("H2a", cx(3), yh2l, cx(4.0), yh2r, 0, H, M["wall"], c_build)
bx("H2b", cx(4.0), yh2l, cx(4.6), yh2r, DH, H, M["wall"], c_build)
bx("H2c", cx(4.6), yh2l, XR, yh2r, 0, H, M["wall"], c_build)

# --- 陽台（右側）---
bx("B地", XR, YB, XRb, cy(4.5), 0, 0.05, M["floor"], c_build)
bx("B外牆", XRb-WT, YB, XRb, cy(4.5), 0, 1.1, M["wall"], c_build)
bx("B底牆", XR, YB, XRb, YB+WT, 0, 1.1, M["wall"], c_build)
bx("B頂牆", XR, cy(4.5)-WT, XRb, cy(4.5), 0, 1.1, M["wall"], c_build)

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
# 門窗
# ============================================================
print("=== 門窗 ===")

def make_door(name, ox1, oy1, ox2, oy2):
    parts = []; ft = 0.05; mt = 0.01
    def b(n,x1,y1,x2,y2,z1,z2,mat):
        return bx(n, x1, y1, x2, y2, z1, z2, mat, c_dw)
    parts.append(b(f"{name}_框L", ox1, oy1, ox1+ft, oy2, ft, DH-ft, M["door"]))
    parts.append(b(f"{name}_框R", ox2-ft, oy1, ox2, oy2, ft, DH-ft, M["door"]))
    parts.append(b(f"{name}_框T", ox1+ft, oy1, ox2-ft, oy2, DH-ft, DH, M["door"]))
    parts.append(b(f"{name}_框B", ox1+ft, oy1, ox2-ft, oy2, 0, ft, M["door"]))
    parts.append(b(f"{name}_板", ox1+ft+mt, oy1+mt, ox2-ft-mt, oy2-mt, ft+mt, DH-ft-mt, M["door"]))
    return join_objs(parts, name, c_dw)

def make_vwindow(name, ox1, oy1, ox2, oy2):
    ww = oy2 - oy1; wd = ox2 - ox1; wh = WHT - WH
    ft = 0.04; mt = 0.03; cx0 = (ox1+ox2)/2; cy0 = (oy1+oy2)/2
    parts = []
    def b(n,x1,y1,x2,y2,z1,z2,mat):
        return bx(n, x1, y1, x2, y2, z1, z2, mat, None)
    parts.append(b(f"{name}_框L", -ww/2, -wd/2, -ww/2+ft, wd/2, 0, wh, M["window_frame"]))
    parts.append(b(f"{name}_框R", ww/2-ft, -wd/2, ww/2, wd/2, 0, wh, M["window_frame"]))
    parts.append(b(f"{name}_框T", -ww/2+ft, -wd/2, ww/2-ft, wd/2, wh-ft, wh, M["window_frame"]))
    parts.append(b(f"{name}_框B", -ww/2+ft, -wd/2, ww/2-ft, wd/2, 0, ft, M["window_frame"]))
    parts.append(b(f"{name}_中柱", -mt/2, -wd/2, mt/2, wd/2, ft, wh-ft, M["window_frame"]))
    parts.append(b(f"{name}_玻璃L", -ww/2+ft, -wd*0.3, -mt/2, wd*0.3, ft, wh-ft, M["glass"]))
    parts.append(b(f"{name}_玻璃R", mt/2, -wd*0.3, ww/2-ft, wd*0.3, ft, wh-ft, M["glass"]))
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
make_door("大門", cx(3.5), YB, cx(4.9), YB+WT)

# 陽台門
make_door("陽台門", XR-WT, cy(1.8), XR, cy(2.7))

# 內門
xvl, xvr = cx(3)-WI/2, cx(3)+WI/2
make_door("BR1門", xvl, cy(1.5), xvr, cy(2.1))
make_door("BR2門", xvl, cy(5.5), xvr, cy(6.1))
make_door("廚房門", cx(4.0), yh1l, cx(4.6), yh1r)
make_door("衛浴門", cx(4.0), yh2l, cx(4.6), yh2r)
print("門完成")

# 左牆窗
make_vwindow("BR1窗", XL, cy(1), XL+WT, cy(2.5))
make_vwindow("BR2窗", XL, cy(4.5), XL+WT, cy(6.0))
print("左窗完成")

# 右牆窗
make_vwindow("廚房窗", XR-WT, cy(5.0), XR, cy(6.3))
print("右窗完成")

# 頂牆窗
make_vwindow("衛浴窗", cx(3.5), YT-WT, cx(5.0), YT)
print("頂窗完成")

for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'MATERIAL'

print("\n=== 建築模型完成（無家具）===")
print("6x8m 2房1廳1衛1陽台")
print("請確認建築模型無誤後，再選擇要生成的家具")
