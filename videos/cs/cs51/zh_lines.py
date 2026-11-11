"""Chinese narration for cs51: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第51部分：光与像素"

CHAPTERS = {
    "Hook": "一幅图像是光的样本",
    "Transforms": "1. 变换与旋转",
    "Projection": "2. 透视投影",
    "Raster": "3. 光栅化与 z 缓冲区",
    "Shading": "4. 着色",
    "Textures": "5. 纹理与采样",
    "Gpu": "6. GPU 流水线",
    "Rays": "7. 光线追踪",
    "Bvh": "8. 加速结构",
    "Radiometry": "9. 辐射度量学与 BRDF",
    "Equation": "10. 渲染方程",
    "Pathtrace": "11. 路径追踪",
    "Ours": "12. 我们的路径追踪器，以及去噪",
    "Curves": "13. 曲线、曲面与字体",
    "Frontier": "14. 前沿：实时渲染与神经渲染",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ s01_hook
    "This picture was made by the program we build in this part.":
        "这幅图是由我们在这一部分构建的程序生成的。<bookmark mark='a'/>每个像素只有一条光路时，它几乎全是噪声。每个像素的颜色，是对有多少光到达它的一次随机估计，"
        "这些光在一个盒子里四处反弹：盒子有一面红墙、一面绿墙、一个镜面球，天花板上还有一盏灯。<bookmark mark='b'/>有4条光路时，形状出现了；16条时，"
        "颜色出现了；<bookmark mark='c'/>256条时，它几乎干净了，而那些柔和的阴影，以及洒到白球上的红光，都不是画上去的：它们来自物理。<bookmark mark='d'/>"
        "误差按光路数的平方根分之一下降，这是第20部分的蒙特卡洛收敛速度，所以工作量变成4倍，噪声就减半。",
    'f"There are two ways to turn a scene into pixels,':
        "把一个场景变成像素有两种方法，这一部分两种都会构建。<bookmark mark='a'/>光栅化取出每个三角形，用线性代数加一次除法把它的角投影到屏幕上，再填满它覆盖的像素，"
        "这里是在一个三角形上混合三种颜色。游戏和用户界面就是这样工作的，每秒60次甚至更多。<bookmark mark='b'/>光线追踪反过来工作：从眼睛出发，穿过每个像素，"
        "进入场景，在镜子上反弹，穿过玻璃。这幅小图用了{w['counts']['total']:,}条光线。<bookmark mark='c'/>1963年，Ivan Sutherland 的 Sketchpad 在屏幕上画"
        "出了线条。1980年，Turner Whitted 追踪了递归的光线。这两者之间的数学，就是这一部分的主题。",
    "This is Part 51 of Computer Science, Built, and the first":
        "这是计算机科学，从零搭建，第51部分，也是第十幕“视野与信任”的第一部分。<bookmark mark='a'/>我们将变换并投影几何体；用深度缓冲区和透视校正插值把它光栅化；"
        "给它着色、贴上纹理，而且不产生混叠；让光线穿过包围体层次结构；推导渲染方程，并用路径追踪求解它；最后讲那些曲线，它们画出了你在这个系列里读到的每一个字母。",
    # ------------------------------------------------------------------ s02_transforms
    "Chapter one. Transforms and rotations.":
        "第一章：变换与旋转。",
    "A scene is made of points, and a renderer's first job is to":
        "一个场景由点组成，渲染器的第一项工作就是移动它们：把每个物体放进世界，再把世界摆到相机前面。<bookmark mark='a'/>一个矩阵一次移动所有的点。它的列说明两个坐标轴箭头落在哪里，"
        "而因为这个映射是线性的，其他一切都随之确定。<bookmark mark='b'/>旋转、缩放和剪切都是这样工作的，而一个接一个地做，就是单独一个矩阵，也就是它们的乘积。"
        "<bookmark mark='c'/>但线性映射从不移动原点，所以最简单的运动，也就是向旁边滑动，不是这种大小的矩阵能做到的。",
    "The fix is to add one coordinate. <bookmark mark='a'/> A":
        "办法是增加一个坐标。<bookmark mark='a'/>一般的运动是矩阵乘以点，再加上一个常数。<bookmark mark='b'/>给每个点一个额外的坐标 w，"
        "令它等于1，并把这个常数放进新的最后一列：矩阵乘以那个1，就替我们加上了平移。<bookmark mark='c'/>这是降一维之后的图景。点都住在 w 等于1的那条直线上。"
        "平面的一个剪切保持原点不动，线性映射必须如此，但它让这条直线沿着自身滑动：这就是一次平移。<bookmark mark='d'/>这就是 August Möbius 在1827年提出的齐次坐标。"
        "方向的 w 等于零，所以它们会转动，却从不移动。",
    "Now a chain of motions multiplies into one matrix. But":
        "现在，一串运动相乘就成了一个矩阵。但矩阵乘法不满足交换律，而且它们从右往左作用。<bookmark mark='a'/>左边，单位正方形先旋转四分之一圈，再向右移动两个单位。"
        "<bookmark mark='b'/>右边，同样两个矩阵换个次序：先移动，再绕原点甩过去。<bookmark mark='c'/>由我们的变换模块算出的角点，"
        "落在了不同的地方。<bookmark mark='d'/>渲染器要乘三个这样的矩阵：模型矩阵把物体放进世界，视图矩阵把世界摆到相机前面，而投影矩阵，也就是下一章的内容，"
        "为透视做准备。",
    "Rotations in three dimensions are usually described by three":
        "三维空间里的旋转通常用三个角来描述：偏航、俯仰和滚转。<bookmark mark='a'/>看着俯仰角增大时的滚转轴。到90度时，它与偏航轴重合：偏航和滚转现在绕同一条线旋转，"
        "一种转动方式消失了。这就是万向节锁。<bookmark mark='b'/>我们的变换模块测量了它：从角度变化率到转动的映射，其奇异值是1，以及1加、1减俯仰角正弦的平方根。"
        "<bookmark mark='c'/>在89度时，最小的那个约为百分之一；在90度时为零，秩降到了2。",
    "The cure is older than computers. <bookmark mark='a'/> In":
        "解药比计算机还要古老。<bookmark mark='a'/>1843年，威廉·罗文·哈密顿找到了一种数，它有三个虚数单位，平方都等于负1。<bookmark mark='b'/>"
        "绕一根轴转过角 θ，就是由半角的余弦和正弦构成的单位四元数。<bookmark mark='c'/>要旋转一个向量，就在一侧乘以 q，在另一侧乘以它的共轭。<bookmark mark='d'/>"
        "欧拉角紧凑，却有奇点。一个矩阵有九个数，第4部分讲的舍入会慢慢把它推离旋转。四元数只有四个数，从不锁死，而且只要除以它的长度就能修复。",
    "Quaternions also answer the animator's question: how do you":
        "四元数还回答了动画师的问题：怎样在两个朝向之间平滑地转动？<bookmark mark='a'/>朴素的做法让三个欧拉角沿直线滑动，于是鼻尖沿着这条红色路径游移。"
        "<bookmark mark='b'/>Ken Shoemake 在1985年提出的 slerp，也就是球面线性插值，沿着两个四元数之间的大圆走，用的是这些正弦权重。"
        "<bookmark mark='c'/>绿色路径每一步转过相同的角度，总量恰好是两端之间那单独一次旋转，大约139度。<bookmark mark='d'/>欧拉角路径大约转了237度，"
        "而且不均匀。这就是游戏引擎用四元数来插值旋转的原因。",
    # ------------------------------------------------------------------ s03_projection
    "Chapter two. Perspective projection.":
        "第二章：透视投影。",
    "Why do far things look small? Leon Battista Alberti wrote":
        "为什么远处的东西看起来小？1435年，Leon Battista Alberti 写下了画家的答案，那就是相似三角形。<bookmark mark='a'/>把眼睛放在原点，"
        "把一块屏幕放在距离 n 处。一个高度为 y、距离为 d 的点，是沿着这条线被看到的，这条线在高度 y 撇处穿过屏幕。<bookmark mark='b'/>小三角形和大三角形的角相同，"
        "所以 y 撇比 n 等于 y 比 d。<bookmark mark='c'/>两边同乘：y 撇等于 n 乘 y 除以 d。<bookmark mark='d'/>"
        "远一倍，矮一半。每个坐标都要除以深度，而除法不是线性的，所以没有哪个矩阵能单独做到这一点。",
    "The fourth coordinate rescues us. <bookmark mark='a'/> The":
        "第四个坐标救了我们。<bookmark mark='a'/>投影矩阵用焦距因子缩放 x 和 y，它的最后一行把距离复制进 w。这时还什么都没有除：这些是裁剪坐标。"
        "<bookmark mark='b'/>然后硬件除以 w，每个顶点一次，而这一次除法就是透视的全部。<bookmark mark='c'/>第三行必须为深度缓冲区保留深度。"
        "除法之后，它是负 A 加上 B 除以 d。<bookmark mark='d'/>要求近平面落在负1，远平面落在正1，<bookmark mark='e'/>然后求解。"
        "<bookmark mark='f'/>存下来的深度是距离倒数的仿射函数，而不是距离的仿射函数，这会让我们付出精度的代价。",
    "<bookmark mark='a'/> Here is what the matrix and the":
        "<bookmark mark='a'/>这就是矩阵和除法对空间做的事。这是视锥体，也就是相机在近平面和远平面之间看到的那个截头棱锥，里面有三个等间距的切片。<bookmark mark='b'/>"
        "把这个映射一点一点地施加上去。远端的面缩小，近端的面增大，直到视锥体变成一个在每个坐标上都从负1到1的立方体。<bookmark mark='c'/>直线自始至终保持笔直。"
        "<bookmark mark='d'/>但看看这些切片：在世界里它们等间距，现在却挤向远端的面。<bookmark mark='e'/>三角形在除法之前被裁剪，"
        "那时一切仍是线性的，最后这个立方体被拉伸到像素上。",
    "How much does that crowding matter? <bookmark mark='a'/>":
        "这种拥挤有多要紧？<bookmark mark='a'/>画出存储的深度随距离变化的曲线，近平面在0.1个单位，远平面在1000。<bookmark mark='b'/>"
        "整个范围的一半，在距离达到近平面距离的两倍之前就用掉了，百分之90在距离1之前就用掉了。<bookmark mark='c'/>深度缓冲区存储的是整数。设想一个只有4位的缓冲区："
        "它的16个值位于16除以16减 k 处。其中一半落在距离2之前。<bookmark mark='d'/>而单单一级就覆盖了场景的整个后半部分，从8到16。",
    "How close can two surfaces be before the buffer cannot tell":
        "两个表面要靠得多近，缓冲区才分不清它们？<bookmark mark='a'/>我们的变换模块用二分法找出24位缓冲区能分辨的最小间隙，并用一个闭式公式来核对。"
        "<bookmark mark='b'/>近平面在0.01个单位时，距离1000处的两个表面必须相隔大约6个单位。近平面在1时，0.06个单位就够了。<bookmark mark='c'/>"
        "闭式公式说明了原因：间隙随距离的平方增长，并与近平面距离成反比地缩小，而远平面几乎无关紧要。所以最便宜的修复不是更多的位，而是把近平面往外推。",
    "When two surfaces are closer than that gap, their depths":
        "当两个表面比这个间隙更近时，它们的深度会舍入到同一个整数，于是由绘制顺序决定哪一个露出来。<bookmark mark='a'/>我们的模块在距离50处画两个相隔0.01个单位的平面。"
        "<bookmark mark='b'/>用16位缓冲区，近平面在0.01时，百分之99的像素显示了错误的平面。24位把它降到大约三分之一。<bookmark mark='c'/>"
        "单把近平面移到1，帮助要小一些，降到大约百分之70；两者一起，每个像素都正确。<bookmark mark='d'/>现代引擎还把深度反过来存储，并且用浮点数，"
        "这样第4部分讲的、在零附近密集的浮点数，就落在了需要它们的远处几何体上。",
    # ------------------------------------------------------------------ s04_raster
    "Chapter three. Rasterization and the z-buffer.":
        "第三章：光栅化与 z 缓冲区。",
    "Which pixels does a triangle cover? <bookmark mark='a'/> For":
        "一个三角形覆盖哪些像素？<bookmark mark='a'/>对一条从 a 到 b 的边，取这条边与指向点 p 的向量的叉积：它是三角形 a、b、p 有向面积的两倍，"
        "也就是第22部分的方向测试，告诉我们 p 在边的哪一侧。<bookmark mark='b'/>把每个像素中心依次对三条边做测试。一个中心只要在任何一条边的错误一侧，"
        "就在外面；其余的在里面，而一条打破平局的规则，把恰好落在公共边上的中心只分给一个三角形。<bookmark mark='c'/>每个边函数都是仿射的，所以向右移一个像素就是加一个常数，"
        "硬件一次测试整块像素。<bookmark mark='d'/>包围盒里大约一半在内部。",
    "Once a pixel is inside, we need its colour, its depth, its":
        "一旦某个像素在内部，我们就需要它的颜色、它的深度、它的纹理位置：这些值只在三个角上给出。<bookmark mark='a'/>一个点 p 把三角形分成三个更小的三角形。"
        "每个角对面那一块所占的面积份额，就是这个角的权重 λ，三个权重加起来等于1。<bookmark mark='b'/>移动 p 看看：靠近一个角时，那个角的权重趋近于1。"
        "这就是重心坐标，同样来自1827年的 August Möbius，而且它们可以从我们已经算出的边函数里免费得到。<bookmark mark='c'/>角上的任何值，"
        "都用同样的权重来混合。<bookmark mark='d'/>给三个角纯红、纯绿和纯蓝，我们的光栅化器画出的就是这些权重本身。",
    "There is a catch, and it is perspective. <bookmark":
        "这里有个陷阱，那就是透视。<bookmark mark='a'/>在屏幕上走相等的步长，并不是在一块向远处延伸的地板上走相等的步长。屏幕上两个顶点之间的中点，比地板上沿途的中点近得多。"
        "<bookmark mark='b'/>所以按屏幕上的比例来混合纹理坐标是错的。<bookmark mark='c'/>什么才是对的？在一个平的三角形上，深度的倒数是屏幕位置的仿射函数："
        "把平面方程除以深度就能看出来。任何属性除以深度也是如此。<bookmark mark='d'/>所以对 u 除以 w 和1除以 w 都做线性插值，<bookmark mark='e'/>"
        "并在每个像素上用其中一个除以另一个。这次除法就是透视校正插值。",
    "Here is the difference, from our own rasterizer. <bookmark":
        "这是两者的区别，来自我们自己的光栅化器。<bookmark mark='a'/>一块由两个三角形组成的棋盘格地板，纹理坐标用仿射方式插值：方格沿着两个三角形相接的对角线弯折，"
        "地板上将近一半的像素得到了错误的颜色。<bookmark mark='b'/>用上1除以 w，每个像素都正确。<bookmark mark='c'/>而与对真实地板做的光线投射相比，"
        "纹理坐标在舍入误差之内一致。<bookmark mark='d'/>1994年最初的 PlayStation 省掉了这次除法，它的纹理以晃动而出名。",
    "Now visibility: which of two overlapping triangles do we":
        "现在是可见性：两个相互重叠的三角形，我们看到的是哪一个？<bookmark mark='a'/>这两个彼此穿插，所以在重叠区域里，各自有一部分在前面。<bookmark mark='b'/>"
        "画家算法把整个三角形从后到前排序。蓝色的那个平均更远，所以它先被画，然后处处被盖住：472个像素是错的。整个三角形无论按什么顺序画，都不可能对。<bookmark mark='c'/>"
        "Ed Catmull 在1974年的答案，是给每个像素一个深度：一个片元只有比那里已有的更近时，才会被写入。<bookmark mark='d'/>无论绘制顺序如何，"
        "结果都是对的，代价是每个像素一个数，这在1974年很昂贵，在今天则微不足道。",
    "Put together, this is our rasterizer. <bookmark mark='a'/>":
        "把这些放在一起，就是我们的光栅化器。<bookmark mark='a'/>顶点以裁剪坐标到达。三角形在仍是齐次的时候就对近平面做裁剪，所以眼睛后面的任何东西，"
        "都永远不会被一个负的 w 除。然后是除法、视口、边函数、深度测试，以及透视校正的混合。<bookmark mark='b'/>有一个细节比看上去更重要：顶点被对齐到256分之一像素，"
        "就像 GPU 做的那样，所以边测试是精确的，两个共享一条边的三角形之间永远不会留下裂缝。<bookmark mark='c'/>这一章以及接下来两章里的每一幅图，"
        "都出自这条流水线。",
    # ------------------------------------------------------------------ s05_shading
    "Chapter four. Shading.":
        "第四章：着色。",
    "Now that we know which triangle a pixel sees, how bright":
        "既然我们知道一个像素看到的是哪个三角形，它该有多亮？<bookmark mark='a'/>从一束光垂直照到一个哑光表面上开始。<bookmark mark='b'/>"
        "把光倾斜。同一束光现在铺开在更长的一段表面上，长度是原来的余弦分之一，所以每一小块表面接收到的光更少，与余弦成正比。Johann Heinrich Lambert 在1760年写下了这一点。"
        "<bookmark mark='c'/>单位面积上的功率，是功率除以面积，而面积按余弦分之一增长。<bookmark mark='d'/>所以亮度随余弦变化，也就是单位法线与指向光源的单位向量的点积。"
        "<bookmark mark='e'/>哑光表面把这些光均匀地散射到所有方向，所以从哪里看都一样：这是只有漫反射光的我们的球。",
    "Shiny surfaces add a highlight, and in 1975 Bui Tuong Phong,":
        "有光泽的表面会多出一个高光，1975年，犹他大学的 Bui Tuong Phong 给出了至今仍最先讲授的模型。<bookmark mark='a'/>把光的方向关于法线做反射。"
        "它在法线上的投影是 N 点乘 L 再乘 N；走到那里两次，再退回一个 L，就得到镜面方向 R。<bookmark mark='b'/>当眼睛正对着 R 看下去时，"
        "高光最亮，并随着 R 与视线方向夹角的余弦衰减，这个余弦要取 s 次幂。<bookmark mark='c'/>幂越大，波瓣越窄，高光越小越锐利，材质也就越有光泽。"
        "<bookmark mark='d'/>加上一个代表来自其他各处的光的环境常数，再加上漫反射项和高光，这就是我们光栅化器画出的球，幂取32。",
    "In 1977 Jim Blinn proposed a cheaper highlight. <bookmark":
        "1977年，Jim Blinn 提出了一种更便宜的高光。<bookmark mark='a'/>不去反射光，而是取光和眼睛正中间的那个向量，也就是半程向量 H，"
        "测量法线离它有多近。当法线恰好等于 H 时，眼睛就位于镜面方向上。<bookmark mark='b'/>同样的幂下，两种高光的宽度并不相同。在峰值附近，Phong 的余弦的 s 次幂，"
        "表现得像关于角 α 的一个高斯函数。<bookmark mark='c'/>到 H 的夹角大约是 α 的一半，<bookmark mark='d'/>所以 Blinn 的幂必须大4倍才能匹配。"
        "<bookmark mark='e'/>当光源和观察者都在远处时，H 在每个像素上都相同，这让它成了 OpenGL 和 Direct3D 的固定功能光照。",
    "Where should the lighting be computed? <bookmark mark='a'/>":
        "光照应该在哪里计算？<bookmark mark='a'/>1971年，Henri Gouraud 在每个顶点上算一次，再让光栅化器混合颜色，这很便宜。Phong 1975年的论文也提出了另一种做法："
        "混合法线，重新归一化，再对每个像素计算光照。<bookmark mark='b'/>在一个由360个三角形组成的球上，差别出现在高光里。<bookmark mark='c'/>"
        "放大。Gouraud 的高光是一颗由直边混合构成的星，因为顶点之间的峰值，不可能靠混合顶点上的值得到。Phong 的则是圆的。<bookmark mark='d'/>"
        "我们的光栅化器测量了它：与精确的球相比，Gouraud 的误差大5倍。漫反射光变化缓慢，经得起逐顶点光照；高光则不行，这就是每个现代渲染器都逐像素计算光照的原因。",
    "One last trap, back in chapter one's matrices. <bookmark":
        "最后一个陷阱，回到第一章的矩阵。<bookmark mark='a'/>法线是方向，所以它们不做平移。但把一个圆压扁成椭圆，并用同一个矩阵移动它的法线，它们就会倾斜："
        "不再垂直于表面，光照也就错了。<bookmark mark='b'/>为什么？法线的定义，就是垂直于每一条切线。<bookmark mark='c'/>在它们之间塞进单位矩阵，"
        "也就是 M 的逆乘以 M。<bookmark mark='d'/>切线按 M 移动，所以要让乘积保持为零，法线必须按逆转置移动。<bookmark mark='e'/>"
        "对旋转来说，这两个是同一个矩阵，这就是为什么这个错误会一直藏着，直到某个物体被拉伸，也是为什么引擎要另外交给着色器一个法线矩阵。",
    # ------------------------------------------------------------------ s06_textures
    "Chapter five. Textures and sampling.":
        "第五章：纹理与采样。",
    "A texture is a picture glued onto a surface, Ed Catmull's":
        "纹理是一幅粘到表面上的图片，这是 Ed Catmull 在1974年的想法。查找纹理就是采样，而采样有个陷阱。<bookmark mark='a'/>一个9个周期的波，"
        "采样10次。<bookmark mark='b'/>把样本连起来，它们描出的是一个只有1个周期、方向还反了的波：一个混叠。<bookmark mark='c'/>"
        "一个频率 f，以速率 f s 采样，与 f 减去 f s 的任意倍数无法区分。<bookmark mark='d'/>为了安全，每个周期要取两个以上的样本，这是第36部分的 Nyquist 准则。"
        "<bookmark mark='e'/>我们的光栅化器在每个像素中心查找一个纹素。靠近地平线时，每个像素横跨许多个方格，远远超出了 Nyquist 极限，样本画出了并不存在的曲线："
        "摩尔纹。",
    "Two cures: filter the texture before sampling, or take more":
        "两种解药：在采样之前对纹理做滤波，或者取更多的样本。这是用四种方式画出的地板，来自我们的渲染器。<bookmark mark='a'/>点采样：摩尔纹。<bookmark mark='b'/>"
        "参考图：每个像素256个抖动样本，取平均。<bookmark mark='c'/>与它相比，点采样的偏差大约是满亮度的五分之一。<bookmark mark='d'/>"
        "三线性 mipmap 每个像素读取8个纹素，把这个误差降到三分之一。<bookmark mark='e'/>每个像素16个样本的效果稍好一点，但读取次数是两倍，"
        "而且远处的几行仍在闪烁。便宜的赢家是预先滤波的纹理。",
    "In 1983 Lance Williams proposed filtering the texture in":
        "1983年，Lance Williams 提出预先对纹理做滤波，而且在每一个尺度上都做。<bookmark mark='a'/>第0级就是纹理本身。下一级对上一级的每个2乘2块取平均："
        "宽度减半，高度减半。<bookmark mark='b'/>到第5级，每个纹素均等地覆盖一个亮方格和一个暗方格，图案变成了它的平均灰色。Williams 把它叫作 mip map，"
        "取自拉丁语 multum in parvo，意思是小地方里的许多东西。<bookmark mark='c'/>代价呢？每一级的纹素是上一级的四分之一。<bookmark mark='d'/>"
        "额外的内存是一个几何级数，<bookmark mark='e'/>三分之一。<bookmark mark='f'/>我们的1万6千个纹素变成了2万2千个。",
    "Which level should a pixel read? The one whose texels match":
        "一个像素该读哪一级？纹素与像素覆盖区域相匹配的那一级。<bookmark mark='a'/>向右走一个像素，或者向下走一个，测量纹理坐标移动了多远，以纹素为单位；"
        "把较大的那个叫作 ρ。<bookmark mark='b'/>如果一步跨过4个纹素，那么往下两级，一个纹素就宽4倍：级别就是 ρ 以2为底的对数。<bookmark mark='c'/>"
        "λ 很少是整数，所以三线性滤波读取最近的两级，各读4个纹素，再把它们混合：这就是那8次读取。<bookmark mark='d'/>这是我们的渲染器在每个像素上选的级别："
        "靠近相机处为0，到地平线升到7，也就是那唯一一个灰色纹素。<bookmark mark='e'/>在真实硬件上，导数来自相邻的像素，下一章会讲到。",
    "The mipmap has one flaw, and our floor shows it. <bookmark":
        "mipmap 有一个缺陷，我们的地板就暴露了它。<bookmark mark='a'/>在掠射角下，一个方形像素落在纹理上，是一块又长又窄的覆盖区域。<bookmark mark='b'/>"
        "三线性滤波只用一个数，也就是较大的那个导数，所以它滤波的是一个和长轴一样宽的圆盘。<bookmark mark='c'/>比较我们的三线性图像顶部和参考图：越往地平线，"
        "方格越模糊成一片灰色。<bookmark mark='d'/>各向异性滤波沿着长轴取若干个探针，每个按短轴定大小，再取平均。<bookmark mark='e'/>"
        "探针的个数是两轴之比，有上限，而每个探针读取更精细的一级。",
    "Mipmaps fix the inside of a triangle, but edges alias too,":
        "mipmap 修好了三角形的内部，但边缘也会混叠，变成阶梯。<bookmark mark='a'/>蛮力的解药是超采样：每个像素16个样本，每个都着色，再取平均，"
        "代价是16倍。<bookmark mark='b'/>多重采样抗锯齿，MSAA，看出阶梯是一个覆盖问题。它在每个像素的4个点上测试覆盖和深度，<bookmark mark='c'/>"
        "但对每个像素、每个三角形只运行一次着色器，再把颜色复制到被覆盖的样本上。<bookmark mark='d'/>对样本取平均，边缘就变柔和了。<bookmark mark='e'/>"
        "在三角形内部，四个样本都一致，所以纹理仍然需要 mipmap。<bookmark mark='f'/>在我们的地板上，16个样本只比 mipmap 稍好一点，工作量却是16倍。"
        "好的采样，比更多的采样更便宜。",
    # ------------------------------------------------------------------ s07_gpu
    "Chapter six. The GPU pipeline.":
        "第六章：GPU 流水线。",
    "Everything so far is what a graphics processor does in":
        "到目前为止的一切，都是图形处理器在硬件里做的事，组织成一条流水线。<bookmark mark='a'/>顶点从内存中取出，交给一个小程序，也就是顶点着色器，它施加第一章和第二章的矩阵，"
        "把每个顶点以裁剪坐标输出。<bookmark mark='b'/>固定功能的硬件做裁剪、除以 w，并映射到屏幕上，<bookmark mark='c'/>然后用第三章的边函数做光栅化，"
        "产生片元：携带着插值结果的候选像素。<bookmark mark='d'/>第二个程序，片元着色器，计算每个片元的颜色：这是第四章和第五章的内容。<bookmark mark='e'/>"
        "最后，深度测试和混合写入帧缓冲区。<bookmark mark='f'/>绿色的阶段是你写的程序；橙色的阶段是硅片。OpenGL、Direct3D、Vulkan、"
        "Metal 和 WebGPU 都暴露出同样的形状。",
    "Here are the two programs, in the style of OpenGL's shading":
        "这是那两个程序，写成 OpenGL 着色语言的风格。<bookmark mark='a'/>顶点着色器对每个顶点运行一次。它把位置乘以一个合并了模型、视图和投影的矩阵，"
        "再用法线矩阵，也就是第四章的逆转置，来移动法线。<bookmark mark='b'/>无论它输出什么，这里是法线和纹理坐标，光栅化器都会在三角形上做插值，而且是透视校正的，"
        "用的是第三章的1除以 w。<bookmark mark='c'/>片元着色器对每个片元运行一次：把法线重新归一化，取 Lambert 的余弦，<bookmark mark='d'/>"
        "再乘以一次纹理查找。这一个调用，就是第五章的三线性滤波，在专用硬件里完成。<bookmark mark='e'/>两个程序都看不到任何别的顶点或片元，正是这种独立性，"
        "让 GPU 能同时运行数以百万计的它们。",
    "How many runs is that? A screen of nineteen twenty by ten":
        "那是多少次运行？一块1920乘1080的屏幕大约有200万个像素，每个都需要自己的一次片元着色器运行，每秒60次。<bookmark mark='a'/>因为每次运行都是独立的，"
        "GPU 把片元按2乘2的块打包，这种块叫作 quad，<bookmark mark='b'/>再编进共享一条指令流的组里：在 NVIDIA 的硬件上，就是一个有32条通道的线程束，"
        "也就是第10部分和《人工智能，从零搭建》第17部分的单指令多线程模型。<bookmark mark='c'/>代价是分支。如果一个线程束里有些片元走 if 的一边，"
        "其余的走另一边，<bookmark mark='d'/>这个线程束就两边都要执行，一边接一边，每次都关掉一部分通道。一个逐像素分支的着色器，可能只以一半的速度运行，"
        "甚至更糟。",
    "Quads are how a GPU gets derivatives. <bookmark mark='a'/>":
        "quad 是 GPU 获得导数的方式。<bookmark mark='a'/>在一个2乘2的块里，右边像素的值减去左边像素的值，就是沿屏幕横向的导数，纵向也一样。"
        "这就是第五章的 ρ，因此也就得到了 mip 级别，只要一次减法。<bookmark mark='b'/>但沿着三角形的边，一个 quad 可能只覆盖一个、两个或三个像素。"
        "其余的照样运行，作为辅助通道，只是为了提供差值，它们的颜色会被丢掉。<bookmark mark='c'/>对第三章的那个三角形，我们的光栅化器的覆盖触及1236个 quad："
        "196条辅助通道，多出百分之4。<bookmark mark='d'/>一个只覆盖单个像素的三角形，四条通道里浪费三条，这就是为什么非常小的三角形在 GPU 上很昂贵。",
    "Last, where the depth test sits. <bookmark mark='a'/>":
        "最后，深度测试放在哪里。<bookmark mark='a'/>第三章那两个交叉的三角形产生6576个片元。如果每个片元都先着色、再做深度测试，那它们每一个都要为片元着色器付出代价。"
        "<bookmark mark='b'/>只要着色器不能改变结果，GPU 就在着色之前测试深度。在我们这次运行中，693个片元没有通过测试，从未被着色。<bookmark mark='c'/>"
        "但只有5412个像素是可见的：有471个片元通过了测试、被着色，然后又被后来画的一个更近的片元盖住。<bookmark mark='d'/>所以引擎从前到后绘制不透明物体，"
        "或者先用一遍只写下深度，然后让每个可见像素恰好着色一次。",
    # ------------------------------------------------------------------ s08_rays
    "Chapter seven. Ray tracing.":
        "第七章：光线追踪。",
    "Rasterization starts from the triangles; ray tracing starts":
        "光栅化从三角形出发；光线追踪从眼睛出发。<bookmark mark='a'/>对每个像素，穿过像素中心射出一条光线：一个点 o 加上 t 乘以方向 d。<bookmark mark='b'/>"
        "求它与每个物体的交点，保留 t 为正的最近交点：这就是这个像素看到的东西。Arthur Appel 在1968年这样做过，用来处理隐藏面和阴影。<bookmark mark='c'/>"
        "它就是倒过来的 z 缓冲区：不是每个三角形问自己覆盖哪些像素，而是每个像素问自己最先遇到哪个物体。<bookmark mark='d'/>我们的追踪器为一幅小图射出19200条这样的光线，"
        "然后，沿着 Turner Whitted 的做法，继续往前走。",
    "The simplest object is a sphere. <bookmark mark='a'/> A":
        "最简单的物体是球。<bookmark mark='a'/>光线上的一个点，当它到球心的距离等于半径时，就在球面上。<bookmark mark='b'/>把长度的平方展开成点积，"
        "它就是一个关于 t 的二次方程。<bookmark mark='c'/>把系数叫作 A、B 和 C，<bookmark mark='d'/>根就随之而来。判别式决定一切。"
        "<bookmark mark='e'/>滑动这条光线：为正，两个交点，一进一出；为零，光线擦过球面；为负，它没有击中。较小的那个正根就是我们看到的交点。<bookmark mark='f'/>"
        "还有第4部分的教训：教科书公式可能会让两个几乎相等的数相减，所以我们的代码安全地算出一个根，再从两根之积求出另一个。",
    "Most scenes are triangles. In 1997 Tomas Möller and Ben":
        "大多数场景由三角形组成。1997年，Tomas Möller 和 Ben Trumbore 发表了至今大多数光线追踪器仍在使用的测试。<bookmark mark='a'/>"
        "三角形上的一点，是它的角按重心权重的混合，又是第三章的那一套；当这两个点重合时，光线就击中了它。<bookmark mark='b'/>一切都从第一个角量起，沿着两条边。"
        "<bookmark mark='c'/>这是一个关于 t、u 和 v 的三乘三线性方程组。<bookmark mark='d'/>用克莱姆法则求解：每个行列式都是一个三重积，"
        "而它们共用两个叉积，p 和 q。<bookmark mark='e'/>当 u 和 v 非负、它们的和至多为1、并且 t 为正时，就是一次击中；而且 u 和 v 免费得到，"
        "随时可以用来贴纹理。",
    "Turner Whitted's paper of 1980 asked what happens after the":
        "Turner Whitted 1980年的论文追问了第一次击中之后会发生什么。<bookmark mark='a'/>在哑光表面上，朝光源投出一条阴影光线；如果有东西挡在中间，"
        "这个点就在阴影里。<bookmark mark='b'/>在镜子上，用同样的过程追踪反射光线。这里它找到了红球，落在一个被镜子本身挡住了光源的点上。<bookmark mark='c'/>"
        "在玻璃上，追踪两条：一条反射光线，以及一条弯折进球里、再穿出来的折射光线。每个像素长出一棵树。<bookmark mark='d'/>我们的追踪器数了数：19200条主光线，"
        "1万3千5百条阴影光线，反射和折射光线各4千多条：大约每个像素两条。",
    "Glass bends light. <bookmark mark='a'/> Snell's law: the":
        "玻璃会让光弯折。<bookmark mark='a'/>Snell 定律：折射率乘以角的正弦，在两侧相同。<bookmark mark='b'/>光线追踪器想要它的向量形式："
        "弯折后的方向是入射方向和法线的混合，不需要任何角度。<bookmark mark='c'/>从玻璃进入空气时，平方根可能失败。<bookmark mark='d'/>"
        "在玻璃内部倾斜光线：超过大约42度时，就没有折射光线了，所有的光都被反射。<bookmark mark='e'/>在一个球里，这永远不会发生：到入射点和出射点的两条半径构成一个等腰三角形，"
        "所以光线以它进入时的角度离开。我们的追踪器数到的是零。",
    "How much light reflects, and how much goes through?":
        "有多少光被反射，又有多少穿过去？<bookmark mark='a'/>Fresnel 方程给出了精确的答案：正对着时，玻璃反射百分之4，到掠射角时上升到全部。"
        "<bookmark mark='b'/>1994年，Christophe Schlick 用一个五次幂拟合了它，<bookmark mark='c'/>锚定在正对时的值上，"
        "对玻璃是0.04。<bookmark mark='d'/>我们的追踪器给玻璃上的每次击中一条按 R 加权的反射光线，和一条按1减 R 加权的折射光线，并丢掉权重可以忽略的分支。"
        "所以我们的玻璃球的边缘映出了地板和天空，而它的中间显示出背后的场景，被折射弯折了。",
    # ------------------------------------------------------------------ s09_bvh
    "Chapter eight. Acceleration structures.":
        "第八章：加速结构。",
    "A ray tracer spends nearly all its time on one question:":
        "光线追踪器几乎把全部时间都花在一个问题上：这条光线最先击中哪个三角形？<bookmark mark='a'/>显而易见的答案是测试每一个三角形，保留最近的那个。"
        "<bookmark mark='b'/>40个三角形，40次测试，换来一次击中。<bookmark mark='c'/>我们那幅 Whitted 图用了4万1千5百条光线。"
        "面对一个有10万个三角形的网格，也就是我们下面测试的最大的那个，一幅小小的图就要超过40亿次求交测试。<bookmark mark='d'/>而其中几乎全部都是浪费："
        "每条光线只保留一个答案。<bookmark mark='e'/>解药来自1980年的 Steven Rubin 和 Turner Whitted，和图书馆的做法一样："
        "把东西装进盒子，再把盒子装进更大的盒子。一条没有击中某个盒子的光线，可以跳过盒子里的一切。",
    "Here is the idea built on our forty triangles. <bookmark":
        "这是在我们那40个三角形上搭起来的这个想法。<bookmark mark='a'/>在所有东西外面套一个盒子：根。<bookmark mark='b'/>沿盒子较宽的一边给三角形排序，"
        "在中位数处把它们分开，给每一半各套一个盒子。<bookmark mark='c'/>在每一半里重复，<bookmark mark='d'/>再重复，直到一个盒子至多装三个三角形。"
        "每个盒子是一棵二叉树的一个节点，叶子装着三角形。<bookmark mark='e'/>两个孩子的盒子可能重叠。包围体层次结构划分的是物体，而不是空间，所以每个三角形恰好住在一个叶子里，"
        "而当盒子里的三角形移动时，盒子可以便宜地重新拟合。<bookmark mark='f'/>每一层都减半，深度就像三角形数目的对数那样增长。",
    "Now trace a ray through the tree. <bookmark mark='a'/>":
        "现在让一条光线穿过这棵树。<bookmark mark='a'/>测试一个盒子很便宜：这是 Kay 和 Kajiya 的平板测试。对每根轴，找出光线进入和离开盒子两个平面之间那块平板的位置。"
        "<bookmark mark='b'/>光线在最晚的进入和最早的离开之间位于盒子内部，所以当这个区间非空时，它就击中了盒子。<bookmark mark='c'/>"
        "从根开始。在它进入的每个盒子处，先访问较近的孩子；跳过它没有击中的盒子，或者起点比目前找到的最佳交点还远的盒子。<bookmark mark='d'/>在它到达的叶子里，"
        "测试三角形。<bookmark mark='e'/>这条光线只需要几个盒子和几个三角形，而不是全部40个，并且找到了同一个最近的交点。",
    "The median split ignores where the triangles are. Here, nine":
        "中位数划分不管三角形在哪里。这里，有9个挤在左边，3个散在右边。盒子该在哪里切开？<bookmark mark='a'/>按一次划分的期望代价给它定价：一次盒子测试，"
        "加上每个孩子的三角形，按一条进入父盒子的光线也进入那个孩子的概率加权。<bookmark mark='b'/>对随机光线，这个概率是孩子的表面积除以父盒子的表面积，"
        "这是积分几何的一个经典结果。<bookmark mark='c'/>两个单位代价都取1，就像我们的构建器那样，这就是 MacDonald 和 Booth 在1990年提出的表面积启发式。"
        "<bookmark mark='d'/>让一个候选平面扫过去，就像第22部分扫过直线那样，在每个位置上计算代价。<bookmark mark='e'/>中位数切穿了那一簇，"
        "留下一个装着6个三角形的宽盒子。最便宜的平面把整簇放进一个紧凑的盒子，把三个掉队的放进另一个。<bookmark mark='f'/>而如果没有哪种划分比测试每个三角形更好，"
        "就做成一个叶子。",
    "Now our real BVH, in three dimensions, built over random":
        "现在是我们真正的 BVH，在三维空间里，建在从100到10万个三角形的随机地形网格上，并用排成网格的相机光线来追踪。<bookmark mark='a'/>蛮力法测试每一个三角形，"
        "在这张对数图上是一条直线。<bookmark mark='b'/>用中位数划分，每条光线大约7到10次三角形测试，不论规模多大。<bookmark mark='c'/>"
        "用表面积启发式，2到3次。<bookmark mark='d'/>工作转移到了盒子上。以三角形数目的对数为横轴，每条光线访问的盒子数沿一条几乎笔直的线上升：规模每增加10倍，"
        "大约多9个。这就是每条光线一个对数。<bookmark mark='e'/>在10万个三角形时，每条光线做2.5次三角形测试，访问39个盒子，而不是10万次测试；"
        "而且在我们检查过的每一条光线上，它都和蛮力法找到同一个最近的交点。",
    # ------------------------------------------------------------------ s10_radiometry
    "Chapter nine. Radiometry and BRDFs.":
        "第九章：辐射度量学与 BRDF。",
    "First, directions. <bookmark mark='a'/> An angle in the":
        "首先，方向。<bookmark mark='a'/>平面上的一个角，是弧长除以半径，单位是弧度。<bookmark mark='b'/>立体角是同一个想法升高一维："
        "一个形状在球面上覆盖的面积，除以半径的平方，单位是球面度。<bookmark mark='c'/>在单位球面上，一小块经纬网格的面积是 sin θ dθ dφ。"
        "<bookmark mark='d'/>在半角为 α 的球冠上积分：2π 乘以1减 cos α。<bookmark mark='e'/>把球冠张开到90度，它就覆盖了表面上方的每一个方向："
        "2π 球面度，是整个球面4π 的一半。",
    "Now the quantities. <bookmark mark='a'/> Radiant flux,":
        "现在是各个量。<bookmark mark='a'/>辐射通量，大写的 Φ，是每秒的能量，单位是瓦特。<bookmark mark='b'/>辐照度是单位面积上到达的通量："
        "一个表面被照得有多亮。<bookmark mark='c'/>辐亮度再除一次：垂直于光束的单位面积、单位立体角上的通量。余弦之所以在那里，是因为一块斜着看的面片，"
        "只呈现出它面积的 cos θ 倍。<bookmark mark='d'/>辐亮度就是相机像素测量的东西：一小块面积，沿着一个窄锥看出去。<bookmark mark='e'/>"
        "把辐亮度带着余弦在半球上汇总起来，就得回辐照度：这就是第四章的 Lambert 定律。",
    "Radiance has one property that makes ray tracing possible.":
        "辐亮度有一个性质，让光线追踪成为可能。<bookmark mark='a'/>一个像素沿着一个窄锥看出去。把墙移远，锥里那一块墙随距离的平方增大，<bookmark mark='b'/>"
        "而每一小块的光进入像素的份额，按距离平方的倒数减小。<bookmark mark='c'/>两者抵消：在空的空间里，辐亮度沿着光线不变。这就是为什么你从一面墙走开时，"
        "它不会变暗。<bookmark mark='d'/>这也是为什么光线追踪器可以携带一个数，也就是辐亮度，从它击中的表面直接带回眼睛。",
    "How a material reflects is a function of two directions.":
        "一种材料怎样反射，是两个方向的函数。<bookmark mark='a'/>BRDF，也就是双向反射分布函数，由 Fred Nicodemus 等人在1977年命名，"
        "它是沿一个方向射出的辐亮度，除以从另一个方向到达的辐照度。<bookmark mark='b'/>把每一个入射方向加起来，我们就得到了反射方程。<bookmark mark='c'/>"
        "哑光表面向各处均匀散射，所以它的 BRDF 是一个常数，ρ 除以 π。<bookmark mark='d'/>为什么是 π？余弦在半球上的积分是2π 乘以二分之一："
        "π。<bookmark mark='e'/>所以在辐亮度为1的均匀光照下，哑光表面恰好返回它的反照率。<bookmark mark='f'/>而有光泽的表面，则把它的光聚拢成镜面方向周围的一个波瓣。",
    "Glossy surfaces are rough at a scale far below a pixel.":
        "有光泽的表面，在远小于一个像素的尺度上是粗糙的。<bookmark mark='a'/>1982年，Robert Cook 和 Kenneth Torrance 把它们建模为随机倾斜的微小镜面，"
        "也就是微表面。<bookmark mark='b'/>一个小面只有当它的法线是两个方向之间的半程向量时，才会把光从一个方向送到另一个方向。<bookmark mark='c'/>"
        "所以 BRDF 是 D，朝向半程向量的小面的密度；乘以 G，没有被邻居遮挡或遮蔽的比例；乘以 F，第七章的 Fresnel 反射率；再除以变量替换带来的4乘两个余弦。"
        "<bookmark mark='d'/>GGX 分布由 Bruce Walter 等人在2007年引入图形学，它只有一个参数，粗糙度 α。<bookmark mark='e'/>"
        "把它调大，小面就散开：高光变宽、变暗。",
    "Every physical BRDF obeys two rules, and our instruments":
        "每一个符合物理的 BRDF 都遵守两条规则，我们的仪器两条都检查。<bookmark mark='a'/>互易性：交换两个方向，值不变。在1万对随机方向上，我们的四个模型在舍入误差内一致。"
        "<bookmark mark='b'/>能量守恒：在一个白炉里，也就是从每个方向均匀照亮时，一个表面返回的至多是1。<bookmark mark='c'/>Lambert 恰好返回1。"
        "归一化的 Phong 在正对时返回1，在掠射角下返回得更少，因为那里它的波瓣沉到了地平线以下。<bookmark mark='d'/>通常的 Blinn-Phong 归一化只是近似的："
        "在指数为10时，它凭空产生了能量，1.075。<bookmark mark='e'/>GGX 在光滑时几乎保住了一切，但在粗糙度为1时，正对着会损失三分之二以上，"
        "因为这个模型漏掉了在小面之间反弹不止一次的光。",
    # ------------------------------------------------------------------ s11_equation
    "Chapter ten. The rendering equation.":
        "第十章：渲染方程。",
    "Chapter nine's reflection equation needs the light arriving":
        "第九章的反射方程，需要知道到达一个点的光。<bookmark mark='a'/>在后墙上取一个点。光从它前方的每个方向到达。<bookmark mark='b'/>"
        "但每一份到达的光，都是离开另外某个表面的光：天花板、灯、两个球，或者穿过敞开的正面，什么都没有。<bookmark mark='c'/>而离开那个表面的东西，又取决于到达那里的一切。"
        "<bookmark mark='d'/>把它写下来。离开一个点的光，是它发出的光，加上它反射的光。<bookmark mark='e'/>从一个方向到达的光，就是离开光线沿那个方向遇到的第一个表面的光，"
        "这是第七章和第八章的工作。<bookmark mark='f'/>代入，未知的辐亮度就出现在两边。这就是渲染方程，由 James Kajiya 在1986年发表："
        "在每一个点、每一个方向上的能量平衡。",
    "Name the integral as an operator. <bookmark mark='a'/> T":
        "把这个积分命名为一个算子。<bookmark mark='a'/>T 接受一个辐亮度场，返回反射一次的光：投出一条光线，查出那里的辐亮度，用 BRDF 和余弦加权，"
        "再积分。方程变成了 L 等于 L e 加 T L。<bookmark mark='b'/>把 T L 移到另一边，然后求逆。<bookmark mark='c'/>"
        "再展开成几何级数，正如1除以1减 x 等于1加 x 加 x 的平方。<bookmark mark='d'/>当 T 让每个场都缩小时，这个 Neumann 级数收敛，"
        "而第九章的白炉保证了这一点：每次反射至多保留它的反照率。<bookmark mark='e'/>在一个墙壁反照率为0.73的封闭房间里，也就是我们的白墙，每次反弹保留百分之73，"
        "所有反弹加起来是发出的光的3.7倍。",
    "Each term of the series has a picture. <bookmark mark='a'/>":
        "级数的每一项都有一幅图。<bookmark mark='a'/>单独的 L e，是从灯直接进入眼睛的光。<bookmark mark='b'/>T L e 是在到达我们之前反射了一次的光："
        "从地板上，或者从镜面球上。这就是直接光照。<bookmark mark='c'/>T 的平方乘 L e，是反弹了两次的光，从后墙到地板，再到眼睛。<bookmark mark='d'/>"
        "每一项都是对具有那么多次反射的所有路径的积分，而图像是对所有长度求和。Eric Veach 1997年的博士论文，把整个方程写成了对路径的单个积分，下一章采样的正是这种形式。",
    "Our path tracer records each path's light by the number of":
        "我们的路径追踪器按每条路径经历的反射次数记录它的光，所以我们能在自己的场景里，看着这个级数一项一项地加起来。<bookmark mark='a'/>第0次反弹："
        "只有灯。<bookmark mark='b'/>加上第1次反弹，也就是直接光照。地板和墙被照亮，球投下阴影，镜子映出墙；但天花板是黑的，因为没有光直接到达它。<bookmark mark='c'/>"
        "加上第2次反弹。天花板出现了，阴影变柔和，红光和绿光洒到白色的表面上。<bookmark mark='d'/>第3、4、5次以及更多：每一次加得更少，图像逐渐稳定成收敛的图像。"
        "<bookmark mark='e'/>这里没有任何东西是画上去的。柔和的阴影和颜色渗透，不过是级数里靠后的那些项。",
    "How fast do the terms shrink? <bookmark mark='a'/> On a":
        "这些项缩小得有多快？<bookmark mark='a'/>在对数刻度上，每次反弹图像的平均亮度落在一条几乎笔直的线上。<bookmark mark='b'/>"
        "从第1次反弹起，每一项是前一项的0.38到0.53倍：一个几何级数，正如算子观点所预言的。每次反弹损失的光，被有颜色的墙吸收了，或者从敞开的正面逃走了。<bookmark mark='c'/>"
        "这8幅图加起来，恰好就是收敛的图像。<bookmark mark='d'/>而靠后的项很重要：在从表面到达眼睛的光中，百分之43经历了两次或更多次反弹。一个止步于直接光照的渲染器会把它全部丢掉；"
        "1984年的辐射度方法为哑光表面算出了它，而路径追踪为一切算出了它。",
    # ------------------------------------------------------------------ s12_pathtrace
    "Chapter eleven. Path tracing.":
        "第十一章：路径追踪。",
    "The rendering equation is an integral inside an integral,":
        "渲染方程是积分里套着积分，没有尽头，而蒙特卡洛能处理它。<bookmark mark='a'/>要估计一个积分，就从任意一个密度 p 中抽取方向，对被积函数除以 p 取平均："
        "这是第20部分的方法。<bookmark mark='b'/>它是无偏的：在 p 之下，g 除以 p 的期望值恰好就是这个积分。<bookmark mark='c'/>"
        "现在在每次反弹时只取一个样本。从眼睛出发，光线遇到后墙；随机选一个方向，它遇到天花板；再选一次，遇到哑光球；再选一次，它到达了灯。这就是一条路径。<bookmark mark='d'/>"
        "一个累乘的权重，也就是吞吐量，在每次反弹时乘以 f 乘 cos θ 除以 p，<bookmark mark='e'/>而路径找到的光乘以它的吞吐量，就是对这个像素的一次估计。"
        "这就是路径追踪，Kajiya 自己的算法。",
    "Which density should we sample? Any works, but the noise":
        "我们应该按哪个密度采样？哪个都行，但噪声取决于这个选择。<bookmark mark='a'/>被积函数里含有一个余弦，所以要在余弦大的地方，也就是法线附近，更频繁地采样。"
        "<bookmark mark='b'/>Malley 的方法不用任何三角函数就做到了这一点。在一个圆盘上均匀地取点，<bookmark mark='c'/>再把每个点竖直向上抬到它上方的半球上。"
        "它们挤向顶部。<bookmark mark='d'/>圆盘就是从上方看到的半球，一小块方向 dω 投在它上面的面积是 cos θ dω。所以抬起来的方向的密度是 cos θ 除以 π。"
        "<bookmark mark='e'/>对哑光表面，f 乘 cos θ 除以 p 于是就是反照率。每次反弹都把吞吐量乘以同一个数，而余弦完全不带来任何噪声。",
    "When should a path stop? Cutting every path at a fixed":
        "一条路径应该在什么时候停下？在一个固定长度处截断每条路径，会丢掉级数里靠后的项：这是一种偏差。<bookmark mark='a'/>一条路径的吞吐量在每次反弹时都会缩小，"
        "所以它靠后的项越来越不重要。<bookmark mark='b'/>俄罗斯轮盘赌由 James Arvo 和 David Kirk 在1990年引入图形学，它改为随机地停止路径："
        "以概率 q 保留这条路径，如果它活下来，就把它的权重除以 q。<bookmark mark='c'/>证明只要一行。期望贡献是 q 乘以 X 除以 q，加上1减 q 乘以零："
        "X。<bookmark mark='d'/>代价是一些额外的方差，q 越小，它越大。<bookmark mark='e'/>我们的追踪器从第三次反弹开始玩这个游戏，"
        "q 等于吞吐量，上限为0.95：暗淡的路径通常会死去，而幸存者回到完整的权重。",
    'f"Our light is small, a sixteenth of the ceiling.':
        "我们的光源很小，只占天花板的十六分之一。<bookmark mark='a'/>一条从地板沿随机方向出发的路径很少击中它：这里，九条中有{n_word}条。确实找到它的路径稀少而明亮："
        "这就是噪声。<bookmark mark='b'/>下一事件估计直接瞄准光源。在每个哑光顶点上，在灯上取一个点，朝它发出一条阴影光线。<bookmark mark='c'/>"
        "把光源上的面积换算成这个点处的立体角，得到两个余弦除以距离的平方。<bookmark mark='d'/>如果阴影光线畅通无阻，就加上直接光。<bookmark mark='e'/>"
        "然后，为了不重复计数，后来某次反弹碰巧到达的光会被忽略，只有在镜子之后例外，因为阴影光线无法穿过镜子去瞄准。",
    "Light sampling is not always best. <bookmark mark='a'/> With":
        "光源采样并不总是最好的。<bookmark mark='a'/>光源小、波瓣宽时，它很理想：每个样本都落在被积函数所在的地方。<bookmark mark='b'/>"
        "但光源大、而波瓣又窄又有光泽时，大多数光源样本落在 BRDF 几乎为零的地方，这时对 BRDF 采样要好得多。<bookmark mark='c'/>Eric Veach 和 Leonidas Guibas 在1995年"
        "展示了怎样两者兼用：从每种策略中抽取样本，并给每个样本加权。<bookmark mark='d'/>只要在每个方向上权重之和都是1，这个组合就是无偏的，不管权重是什么。"
        "<bookmark mark='e'/>平衡启发式给一个样本的权重，是它自己那种策略的密度除以所有策略密度之和，所以每个区域主要由最擅长对它采样的策略来处理，而 Veach 证明了，"
        "它永远不会比最好的单一策略差太多。",
    # ------------------------------------------------------------------ s13_ours
    "Chapter twelve. Our path tracer, and denoising.":
        "第十二章：我们的路径追踪器，以及去噪。",
    "Here is one corner of our render, enlarged: the white ball,":
        "这是我们渲染图的一个角落，放大了：白球、蓝球和绿墙。<bookmark mark='a'/>每个像素一条路径，是一片斑点。<bookmark mark='b'/>"
        "每一步把路径数乘以4，时间也跟着增长，从不到0.03秒到6秒多。<bookmark mark='c'/>每条路径都是一个独立的随机估计，而像素是它们的平均值。<bookmark mark='d'/>"
        "N 个独立项的平均值，其方差是 σ 的平方除以 N，<bookmark mark='e'/>所以误差按 N 的平方根分之一下降：工作量变成4倍，噪声就减半。",
    "Now the whole image, against a reference of two thousand and":
        "现在是整幅图像，对照一张每像素2048条路径的参考图。<bookmark mark='a'/>在对数坐标轴上，误差落在一条直线上。<bookmark mark='b'/>"
        "它的斜率是负0.46，接近蒙特卡洛的负二分之一。<bookmark mark='c'/>最后一个点稍高一些，因为参考图本身也有噪声。<bookmark mark='d'/>"
        "时间随路径数增长，所以误差每减半一次，就要花4倍的时间。<bookmark mark='e'/>收敛速度是固定的；这一章余下的部分，攻击的是那个常数 σ。",
    "Our instrument renders the same image four ways, at sixteen":
        "我们的仪器用四种方式渲染同一幅图，每像素16条路径，并按效率给每种方式打分：效率是误差的平方乘以时间的倒数。<bookmark mark='a'/>带下一事件估计的余弦采样是我们的默认做法。"
        "<bookmark mark='b'/>均匀半球采样的效率大约是它的百分之70。<bookmark mark='c'/>没有下一事件估计，那个小光源就只能碰巧被找到，"
        "效率骤降到大约九分之一。<bookmark mark='d'/>瞄准光源值9倍的工作量；对余弦采样，大约值1.5倍。",
    "The last chapter proved Russian roulette unbiased; now we":
        "上一章证明了俄罗斯轮盘赌是无偏的；现在我们来检验它。<bookmark mark='a'/>12次用轮盘赌的渲染，12次不用，两者都以32次反弹为上限。<bookmark mark='b'/>"
        "平均亮度在一个标准误差之内一致。<bookmark mark='c'/>逐像素地看，差异的大小正是单靠噪声就会产生的：它们的 z 分数的均方根是1.04。<bookmark mark='d'/>"
        "而轮盘赌让路径早早结束：每条路径3.16条光线，而不是将近7条，少了百分之55，用时大约一半。",
    "Our box is all matte, so we test multiple importance":
        "我们的盒子全是哑光的，所以我们在多重重要性采样真正要紧的地方检验它：一个圆形光源下的一个有光泽的点，32个样本，重复4000次。<bookmark mark='a'/>"
        "沿网格往下，有光泽的波瓣变窄；往右，光源变大。<bookmark mark='b'/>光源采样在左上角获胜，误差不到百分之0.2，但在右下角误差达到百分之93。"
        "<bookmark mark='c'/>BRDF 采样正好相反：在最小的光源下误差达到百分之460。<bookmark mark='d'/>幂启发式从来不是单独最好的那个，"
        "但它最坏的情况是百分之8。",
    "The other way to fight noise is to borrow from the":
        "另一种对抗噪声的办法，是向邻居借，用的是 Holger Dammertz 等人2010年提出的边缘避让 à-trous 滤波器。<bookmark mark='a'/>"
        "一遍滤波，在一个小而平滑的核下，把每个像素和25个邻居混合。<bookmark mark='b'/>每一遍都把采样点之间的距离拉开一倍，中间留下空洞：à trous 就是“带孔”的意思。"
        "<bookmark mark='c'/>三遍，一共75个采样点，覆盖一个29像素宽的正方形。<bookmark mark='d'/>为了保留边缘，每个采样点还要按两个像素有多相似来加权，"
        "比较的是颜色、法线、反照率和位置。<bookmark mark='e'/>而且只模糊光照：除以反照率，滤波，再乘回去，这样墙的颜色保持清晰。",
    "Here is the filter on sixteen paths per pixel. <bookmark":
        "这是作用在每像素16条路径上的滤波器。<bookmark mark='a'/>球周围的斑点消失了，而边缘和柔和的阴影保留了下来：表面上的误差小了4倍。<bookmark mark='b'/>"
        "在只被间接照亮的天花板上，噪声变成了一块块斑痕，这是低频的误差，任何滤波器都无法把它和真实的光区分开。<bookmark mark='c'/>在全部像素上，误差下降得少得多，"
        "因为光源自身边缘上的噪声没有被处理。<bookmark mark='d'/>这个滤波器花三分之一秒，比渲染少。但它是有偏的：它用噪声换来了模糊。",
    # ------------------------------------------------------------------ s14_curves
    "Chapter thirteen. Curves, surfaces and fonts.":
        "第十三章：曲线、曲面与字体。",
    "Smooth shapes need curves, and the standard one was found":
        "光滑的形状需要曲线，而标准的那种曲线被发现了两次，在两家汽车制造商：1959年在雪铁龙的 Paul de Casteljau，以及在雷诺的 Pierre Bézier，"
        "他在1960年代发表了它。<bookmark mark='a'/>从四个控制点开始。<bookmark mark='b'/>选一个比例 t。沿控制多边形的每一条边走这个比例，"
        "把新得到的点连起来。重复，直到只剩一个点：那就是曲线在 t 处的点。<bookmark mark='c'/>让 t 从0扫到1，这个点就画出整条曲线。在二分之一处，"
        "我们的仪器给出的点是（2，1.6）。<bookmark mark='d'/>这个构造给出的还不止这些。冻结在二分之一处，每一层的第一个点，就是曲线左半段的控制点，"
        "而每一层的最后一个点，就是右半段的控制点。<bookmark mark='e'/>一直分割，直到每一段都几乎是直的，然后画直线：渲染器就是这样画曲线的。",
    "What polynomial is the construction computing? <bookmark":
        "这个构造在计算的是什么多项式？<bookmark mark='a'/>一层是两点之间的一次线性插值。<bookmark mark='b'/>两层把它们嵌套起来，"
        "是线性插值的线性插值。<bookmark mark='c'/>乘开，二次的权重是1减 t 之差的平方、2t 乘以1减 t，以及 t 的平方。<bookmark mark='d'/>"
        "三层给出三次曲线，它的四个权重就是 Bernstein 多项式。<bookmark mark='e'/>它们从不为负，而且总和总是1。所以曲线始终在它控制点的凸包之内；"
        "它在端点处开始和结束，并与第一条和最后一条边相切；而用一个矩阵移动这四个点，就移动了整条曲线，所以第一章的变换只需作用在控制点上。",
    "Long curves are made of many pieces, and joining Bézier":
        "长曲线由许多段组成，而要让贝塞尔曲线段光滑地相接，每个接点都得小心处理。B 样条把光滑性内建其中。<bookmark mark='a'/>三次 B 样条的每一段由四个相邻的控制点构成，"
        "权重来自 Maurice Cox 和 Carl de Boor 在1972年发表的递推。这里，七个点构成四段。<bookmark mark='b'/>我们的仪器测量了这些接点。"
        "在每个节点处，位置、斜率和曲率都在舍入误差之内一致，大约10的负10次方；只有三阶导数会跳变。这条曲线是 C2 的。<bookmark mark='c'/>而且控制是局部的："
        "移动一个点，只有用到它的那些段会改变。<bookmark mark='d'/>加上权重和不均匀的节点，它们就成了 NURBS，计算机辅助设计里的曲线。",
    "Surfaces follow the same idea. In 1978 Edwin Catmull and Jim":
        "曲面遵循同样的想法。1978年，Edwin Catmull 和 Jim Clark 给出了一套规则，可以细化任何多边形网格。<bookmark mark='a'/>"
        "每个面在中心得到一个点；每条边得到一个点，由它的两个端点和两个相邻面平均而来；<bookmark mark='b'/>每个旧顶点移向它邻居的一个加权平均。每个面都变成四边形。"
        "<bookmark mark='c'/>作用在一个立方体上，每一步把面数乘以4，而顶点数减边数加面数始终是2：这个曲面保持着球面的拓扑。<bookmark mark='d'/>"
        "角往里收，从1.73向0.866靠拢，这正是一个精确公式预言的极限。<bookmark mark='e'/>极限曲面几乎处处光滑，而 Pixar 第一次用这样的曲面制作角色动画，"
        "是在它1997年的短片《棋逢敌手》（Geri's Game）里。",
    'f"And curves are in front of you now. <bookmark':
        "而曲线此刻就在你眼前。<bookmark mark='a'/>这个系列里的每一个字母，都是由贝塞尔曲线构成的轮廓。这是单词 Light，由 Manim 用 TeX 的字体画出来。"
        "<bookmark mark='b'/>圆点是曲线相接处的锚点，方块是控制柄；一笔直线，不过是控制柄落在这条线上的曲线。<bookmark mark='c'/>"
        "这个单词由{spoken(n_word)}条三次曲线构成，它上方的标题则是{spoken(n_head)}条。<bookmark mark='d'/>PostScript 以及 TeX 用的字体，"
        "存储的是三次曲线；TrueType 存储的是二次曲线。<bookmark mark='e'/>要画一个字母，光栅化器按环绕数填充轮廓，并在每个像素内对覆盖率取平均："
        "这是第五章的抗锯齿，让曲线在由样本组成的网格上看起来也是光滑的。",
    # ------------------------------------------------------------------ s15_frontier
    "Chapter fourteen, the frontier. Can a path tracer run at":
        "第十四章：前沿。路径追踪器能以每秒60帧运行吗？",
    'f"A film frame can take hours. A game has sixteen':
        "一帧电影画面可以花上几个小时。一个游戏只有16毫秒。<bookmark mark='a'/>弥合这个差距的第一步，是只取极少的样本：这里是我们自己那幅每像素16条路径的图，"
        "仍然有噪声。<bookmark mark='b'/>然后是一个去噪器，也就是第十二章那个感知边缘的滤波器，它在每个像素的法线和颜色引导下把噪声抹平，误差从{d['rmse_surfaces_before']:.3f}降到{d['rmse_surfaces_after']:.3f}，"
        "比256条路径的还低。<bookmark mark='c'/>实时渲染器还加上了另外三个想法：自2018年起，用硅片遍历包围体层次结构的硬件；像2020年的 ReSTIR 那样的算法，"
        "在相邻像素和相邻帧之间复用好的光源样本；以及训练来去噪和放大分辨率的神经网络。",
    "The newest idea turns rendering around. <bookmark mark='a'/>":
        "最新的想法把渲染倒了过来。<bookmark mark='a'/>2020年，Ben Mildenhall 等人训练了一个小网络，把一个点和一个观察方向映射成一种颜色和一个密度，"
        "再沿每条光线积分来渲染它，这个网络是根据一个真实场景的几十张照片拟合出来的。<bookmark mark='b'/>2023年，Bernhard Kerbl 等人用数以百万计的小三维高斯函数取代了这个网络，"
        "它们由光栅化器投影并混合，能实时运行。<bookmark mark='c'/>失去的是物理：没有显式的材质或光源，所以这些场景很难编辑或重新打光。<bookmark mark='d'/>"
        "两者都把这一部分倒着运行：给定图片，求出场景，这就是《人工智能，从零搭建》第22部分的反问题。",
    "Open problems. <bookmark mark='a'/> Caustics: light focused":
        "未解的问题。<bookmark mark='a'/>焦散：光穿过玻璃聚焦到地板上，再在镜子里被看到，对每一种已知的无偏方法来说，它收敛起来仍然很慢。<bookmark mark='b'/>"
        "对自己引入的偏差有保证的去噪器。<bookmark mark='c'/>能恢复材质和光源、而不只是外观的逆向渲染。<bookmark mark='d'/>还有一种与人们实际看到的相吻合的图像误差度量。"
        "<bookmark mark='e'/>这一部分的研究题，要求为那些焦散路径构造一个无偏估计量，并证明它的方差在最优可能值的常数倍之内。",
    # ------------------------------------------------------------------ s16_outro
    "What we built in this part. Transforms as matrices, with":
        "我们在这一部分构建了什么。作为矩阵的变换，以及用来平滑旋转的四元数；作为线性代数再加一次除法的透视，以及被那次除法扭曲的深度缓冲区。一个光栅化器，带着边函数和透视校正插值、"
        "着色，以及没有混叠地采样的纹理。一个光线追踪器，用包围体层次结构加速到每条光线一个对数。辐射度量学与渲染方程，由一个路径追踪器求解，它的噪声按样本数的平方根分之一下降，"
        "并靠重要性采样和去噪变得实用。还有画出屏幕上每一个字母的贝塞尔曲线。一个思想贯穿其中：一幅图像是一个积分，而每一种技术都是估计它的一种方法。",
    "Where this comes back. Part 52 treats integration and linear":
        "这些内容会在哪里再出现。第52部分以舍入所要求的那种细心，处理积分和线性方程组求解器。第54部分证明程序是正确的，图形驱动程序也在其中。第57部分追问从图像中学习什么时候能够泛化。"
        "第60部分为单一的一种工作专门构建硬件，而 GPU 是第一个、也是最成功的例子。而第61部分会把这一部分的未解问题当作研究重新拾起。",
    "In practice. Game engines rasterize, and add ray-traced":
        "实践中。游戏引擎做光栅化，并在硬件允许的地方加上光线追踪的阴影和反射。Vulkan、Metal 和 WebGPU 这样的图形编程接口，暴露出着色器和命令缓冲区。"
        "电影由带去噪器的产品级路径追踪器在渲染农场上渲染。字体、矢量图形和合成器，画出你用的每一个界面。而当一个渲染器出错时，看看每像素一个样本的图：噪声会告诉你光在哪里丢失了。",
    "Six problems, with full solutions in the part's notes. Pause":
        "六道习题，完整解答在这一部分的笔记里。可以在任何一道上暂停。第五道是构建题：给我们的路径追踪器加上第二个光源，并对两个光源都采样，然后测量噪声。最后一道标有星号，"
        "是研究题：为焦散构造一个估计量，并证明它的方差接近最优可能值。",
    "Next time, Part 52: computing with real numbers. With":
        "下一次，第52部分：用实数计算。每一次运算都有舍入，哪些答案可以信任？答案把一个问题有多难，和一个算法有多好区分开来，并引出那些驱动整个科学计算的算法。",
    "The books and papers this part follows are on screen and in":
        "这一部分所依据的书和论文都在屏幕上和笔记里。感谢观看。",
}

PHRASES = {"one": "一", "two": "两", "three": "三", "four": "四", "five": "五", "six": "六", "seven": "七",
           "eight": "八", "nine": "九", "ten": "十"}
PHRASES.update({"none": "零"})
