import bpy

# 建立家具收集
c_fur = None
for c in bpy.data.collections:
    if c.name == "家具":
        c_fur = c; break
if not c_fur:
    c_fur = bpy.data.collections.new("家具")
    bpy.context.scene.collection.children.link(c_fur)

def new_mat(name, r, g, b, a=1.0):
    m = bpy.data.materials.new(name=name)
    m.use_nodes = True
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (r, g, b, a)
    return m

M_fur = {}
M_fur["bed"] = new_mat("床", 0.90, 0.88, 0.85)
M_fur["mattress"] = new_mat("床墊", 0.55, 0.70, 0.60)
M_fur["wardrobe"] = new_mat("衣櫃", 0.70, 0.50, 0.30)
M_fur["sofa"] = new_mat("沙發", 0.35, 0.55, 0.45)
M_fur["tv_cabinet"] = new_mat("電視櫃", 0.65, 0.42, 0.28)
M_fur["tv"] = new_mat("電視", 0.10, 0.10, 0.12)
M_fur["fridge"] = new_mat("冰箱", 0.85, 0.88, 0.92)
M_fur["table"] = new_mat("餐桌", 0.72, 0.60, 0.40)
M_fur["chair"] = new_mat("椅子", 0.50, 0.45, 0.40)

def box(name, x1, y1, x2, y2, z1, z2, mat):
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
    c_fur.objects.link(o)
    for c in list(o.users_collection):
        if c != c_fur: c.objects.unlink(o)
    return o

# ====== BR1（底部左側：X=-3~0, Y=-4~0）======
# 床：靠左牆，1.8x2.0x0.3 + 床墊
box("BR1_床板", -2.9, -2.0, -1.1, 0, 0, 0.3, M_fur["bed"])
box("BR1_床墊", -2.85, -1.95, -1.15, -0.05, 0.3, 0.4, M_fur["mattress"])
# 衣櫃：靠左牆下方，1.2x0.6x2.0
box("BR1_衣櫃", -2.9, -3.9, -1.7, -3.3, 0, 2.0, M_fur["wardrobe"])

# ====== BR2（頂部左側：X=-3~0, Y=0~4）======
# 床：靠左牆
box("BR2_床板", -2.9, 0.5, -1.1, 2.5, 0, 0.3, M_fur["bed"])
box("BR2_床墊", -2.85, 0.55, -1.15, 2.45, 0.3, 0.4, M_fur["mattress"])
# 衣櫃：靠左牆下方
box("BR2_衣櫃", -2.9, 2.6, -1.7, 3.2, 0, 2.0, M_fur["wardrobe"])

# ====== 客廳（X=0~3, Y=-4~0.5）======
# L型沙發：靠底牆（Y=-4）+ 左牆（X=0）
box("沙發_長", 0.1, -3.9, 2.5, -2.3, 0, 0.6, M_fur["sofa"])
box("沙發_短", 0.1, -3.9, 0.7, -1.5, 0, 0.6, M_fur["sofa"])
# 電視櫃：靠右牆（X=3）
box("電視櫃", 2.5, -1.5, 3.0, -0.5, 0, 0.6, M_fur["tv_cabinet"])
box("電視", 2.55, -1.4, 2.95, -0.6, 0.6, 1.2, M_fur["tv"])
# 餐桌：中間偏上
box("餐桌", 1.2, -1.5, 2.0, -0.7, 0, 0.7, M_fur["table"])
box("餐椅1", 1.0, -1.7, 1.2, -1.5, 0, 0.45, M_fur["chair"])
box("餐椅2", 2.0, -0.7, 2.2, -0.5, 0, 0.45, M_fur["chair"])

# ====== 廚房（X=0~3, Y=0.5~2.5）======
# 冰箱：靠右牆
box("冰箱", 2.4, 1.5, 3.0, 2.2, 0, 1.8, M_fur["fridge"])

# ====== 衛浴（X=0~3, Y=2.5~4）======
# 馬桶
box("馬桶", 0.5, 2.7, 1.1, 3.3, 0, 0.5, M_fur["chair"])

for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'MATERIAL'

print("家具完成")
