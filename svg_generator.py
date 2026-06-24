import random
import math

def wrap_svg(content, width=200, height=200):
    return f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">{content}</svg>'

def get_polygon_svg(sides, cx, cy, r, rotation=0, fill="none", stroke="black", stroke_width=2):
    pts = []
    for i in range(sides):
        angle = math.radians(rotation + i * 360 / sides)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        pts.append(f"{x},{y}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'

def generate_series(packet_seed):
    random.seed(packet_seed)
    start_sides = random.randint(3, 5)
    # Question SVG
    q_svg = wrap_svg(f"""
        {get_polygon_svg(start_sides, 40, 100, 30)}
        {get_polygon_svg(start_sides+1, 100, 100, 30)}
        {get_polygon_svg(start_sides+2, 160, 100, 30)}
        <text x="220" y="105" font-size="24" font-family="Arial">?</text>
    """, width=260, height=200)
    
    correct_sides = start_sides + 3
    options = []
    for s in [correct_sides, correct_sides+1, correct_sides+2, correct_sides-1, 10]:
        if s == 10:
            options.append(wrap_svg('<circle cx="100" cy="100" r="30" fill="none" stroke="black" stroke-width="2"/>'))
        else:
            options.append(wrap_svg(get_polygon_svg(s, 100, 100, 30)))
    
    return {
        "text": f"<p>Pilihlah gambar yang tepat untuk melanjutkan seri di bawah ini:</p><br/>{q_svg}",
        "options": options,
        "correctIndex": 0,
        "explanation": f"Pola deret adalah penambahan sisi bangun datar (+1 sisi). Sisi terakhir adalah {start_sides+2}, sehingga selanjutnya adalah {correct_sides} sisi."
    }

def get_f_shape(cx, cy, scale, rot=0, flip=False):
    # Base F shape centered at 0,0
    # Let's draw an L with an extra line
    pts = [(-20, -30), (20, -30), (20, -10), (-4, -10), (-4, -4), (12, -4), (12, 16), (-4, 16), (-4, 30), (-20, 30)]
    if flip:
        pts = [(-x, y) for x, y in pts]
    
    rot_rad = math.radians(rot)
    trans_pts = []
    for x, y in pts:
        x *= scale
        y *= scale
        rx = x * math.cos(rot_rad) - y * math.sin(rot_rad)
        ry = x * math.sin(rot_rad) + y * math.cos(rot_rad)
        trans_pts.append(f"{rx+cx},{ry+cy}")
    
    return f'<polygon points="{" ".join(trans_pts)}" fill="black"/>'

def generate_rotation(packet_seed):
    random.seed(packet_seed)
    base_rot = random.randint(0, 360)
    q_svg = wrap_svg(get_f_shape(100, 100, 1.5, base_rot, False))
    
    options = []
    correct_rot = (base_rot + random.choice([90, 180, 270])) % 360
    options.append(wrap_svg(get_f_shape(100, 100, 1.5, correct_rot, False)))
    
    for i in range(4):
        flip_rot = random.randint(0, 360)
        options.append(wrap_svg(get_f_shape(100, 100, 1.5, flip_rot, True)))
        
    return {
        "text": f"<p>Manakah dari pilihan berikut yang merupakan hasil rotasi (perputaran) dari gambar di bawah ini, tanpa dicerminkan?</p><br/>{q_svg}",
        "options": options,
        "correctIndex": 0,
        "explanation": "Pilihan yang benar adalah hasil perputaran gambar asli. Pilihan lainnya adalah hasil pencerminan (mirror) yang tidak dapat diperoleh hanya dengan diputar."
    }

def generate_matrix(packet_seed):
    random.seed(packet_seed)
    dot_start = random.randint(1, 2)
    # 3x3 grid
    content = '<rect x="10" y="10" width="180" height="180" fill="none" stroke="black" stroke-width="2"/>'
    content += '<line x1="70" y1="10" x2="70" y2="190" stroke="black" stroke-width="2"/>'
    content += '<line x1="130" y1="10" x2="130" y2="190" stroke="black" stroke-width="2"/>'
    content += '<line x1="10" y1="70" x2="190" y2="70" stroke="black" stroke-width="2"/>'
    content += '<line x1="10" y1="130" x2="190" y2="130" stroke="black" stroke-width="2"/>'
    
    def draw_dots(cx, cy, count):
        dots = ""
        positions = [(0,0), (-10,-10), (10,10), (-10,10), (10,-10), (0,-15), (0,15)]
        for i in range(count):
            if i < len(positions):
                dx, dy = positions[i]
                dots += f'<circle cx="{cx+dx}" cy="{cy+dy}" r="4" fill="black"/>'
        return dots

    correct_count = 0
    for row in range(3):
        for col in range(3):
            cx = 40 + col * 60
            cy = 40 + row * 60
            if row == 2 and col == 2:
                content += f'<text x="{cx-5}" y="{cy+8}" font-size="20">?</text>'
            else:
                count = dot_start + row + col
                content += draw_dots(cx, cy, count)
                if row == 2 and col == 1:
                    correct_count = count + 1

    q_svg = wrap_svg(content)
    options = []
    opts_counts = [correct_count, correct_count+1, correct_count-1, correct_count+2, correct_count-2]
    for c in opts_counts:
        options.append(wrap_svg(draw_dots(100, 100, max(1, c))))

    return {
        "text": f"<p>Perhatikan pola pada matriks 3x3 berikut. Gambar apa yang tepat untuk mengisi kotak bertanda tanya?</p><br/>{q_svg}",
        "options": options,
        "correctIndex": 0,
        "explanation": "Pola matriks: jumlah titik bertambah 1 setiap bergeser ke kanan dan bertambah 1 setiap turun ke bawah."
    }

def generate_superposition(packet_seed):
    random.seed(packet_seed)
    
    # Base: circle
    base = '<circle cx="100" cy="100" r="50" fill="none" stroke="black" stroke-width="2"/>'
    
    # Feature 1
    f1 = random.choice([
        '<line x1="50" y1="100" x2="150" y2="100" stroke="black" stroke-width="2"/>',
        '<line x1="100" y1="50" x2="100" y2="150" stroke="black" stroke-width="2"/>'
    ])
    
    # Feature 2
    f2 = random.choice([
        '<rect x="80" y="80" width="40" height="40" fill="none" stroke="black" stroke-width="2"/>',
        '<circle cx="100" cy="100" r="20" fill="none" stroke="black" stroke-width="2"/>'
    ])

    q_svg = wrap_svg(f"""
        <g transform="translate(-100, 0)">
            {base}
            {f1}
        </g>
        <text x="70" y="105" font-size="24">+</text>
        <g transform="translate(0, 0)">
            {base}
            {f2}
        </g>
        <text x="170" y="105" font-size="24">=</text>
        <text x="210" y="105" font-size="24">?</text>
    """, width=240, height=200)

    options = []
    # Correct: base + f1 + f2
    options.append(wrap_svg(f'{base}{f1}{f2}'))
    # Wrong 1: base + f1 only
    options.append(wrap_svg(f'{base}{f1}'))
    # Wrong 2: base + f2 only
    options.append(wrap_svg(f'{base}{f2}'))
    # Wrong 3: base + f1 + wrong f2
    wrong_f2 = '<line x1="50" y1="50" x2="150" y2="150" stroke="black" stroke-width="2"/>'
    options.append(wrap_svg(f'{base}{f1}{wrong_f2}'))
    # Wrong 4: just base
    options.append(wrap_svg(f'{base}'))

    return {
        "text": f"<p>Jika gambar pertama digabungkan (ditumpuk) dengan gambar kedua, maka akan menghasilkan gambar...</p><br/>{q_svg}",
        "options": options,
        "correctIndex": 0,
        "explanation": "Penumpukan (superposisi) gambar akan menggabungkan semua garis dari gambar pertama dan kedua dalam satu bingkai."
    }

def generate_odd_one_out(packet_seed):
    random.seed(packet_seed)
    
    def make_shape(rot, is_odd):
        content = '<rect x="60" y="60" width="80" height="80" fill="none" stroke="black" stroke-width="2"/>'
        # Dot in corner
        if is_odd:
            content += '<circle cx="120" cy="80" r="10" fill="black"/>' # Top right
        else:
            content += '<circle cx="80" cy="80" r="10" fill="black"/>' # Top left
            
        content += '<line x1="100" y1="60" x2="100" y2="100" stroke="black" stroke-width="2"/>'
        
        return f'<g transform="rotate({rot} 100 100)">{content}</g>'

    rots = [0, 90, 180, 270, 45]
    random.shuffle(rots)
    
    options = []
    correct_idx = random.randint(0, 4)
    
    for i in range(5):
        options.append(wrap_svg(make_shape(rots[i], i == correct_idx)))
        
    return {
        "text": f"<p>Manakah dari 5 gambar di bawah ini yang paling BERBEDA (tidak mengikuti pola yang sama dengan yang lain)?</p>",
        "options": options,
        "correctIndex": correct_idx,
        "explanation": "Semua gambar, jika diputar ke posisi tegak, memiliki titik hitam di sebelah KIRI atas. Namun ada satu gambar yang titik hitamnya berada di sebelah KANAN atas (merupakan hasil cermin)."
    }

def generate_mirror(packet_seed):
    random.seed(packet_seed)
    
    # Asymmetric shape
    def make_base():
        return f"""
        <rect x="50" y="50" width="100" height="100" fill="none" stroke="black" stroke-width="2"/>
        <polygon points="50,50 100,100 50,150" fill="gray"/>
        <circle cx="120" cy="70" r="15" fill="black"/>
        <line x1="100" y1="100" x2="150" y2="150" stroke="black" stroke-width="4"/>
        """
        
    q_svg = wrap_svg(make_base())
    
    def make_mirrored(flip_h, flip_v, rot=0):
        scale_x = -1 if flip_h else 1
        scale_y = -1 if flip_v else 1
        trans_x = 200 if flip_h else 0
        trans_y = 200 if flip_v else 0
        return wrap_svg(f'<g transform="translate({trans_x}, {trans_y}) scale({scale_x}, {scale_y}) rotate({rot} 100 100)">{make_base()}</g>')

    options = []
    options.append(make_mirrored(True, False)) # Correct mirror horizontal
    options.append(make_mirrored(False, True)) # Mirror vertical
    options.append(make_mirrored(True, True)) # Mirror both (rotate 180)
    options.append(make_mirrored(False, False, 90)) # Rotate 90
    options.append(make_mirrored(True, False, 90)) # Mirror H + Rotate 90
    
    return {
        "text": f"<p>Carilah gambar yang merupakan hasil PENCERMINAN (mirror image) dari gambar di bawah ini:</p><br/>{q_svg}",
        "options": options,
        "correctIndex": 0,
        "explanation": "Pencerminan mengubah posisi kiri menjadi kanan dan sebaliknya, namun atas dan bawah tetap pada tempatnya."
    }

def get_spatial_questions(packet_id):
    # Returns 6 questions
    seed = packet_id * 100
    q1 = generate_series(seed + 1)
    q2 = generate_rotation(seed + 2)
    q3 = generate_matrix(seed + 3)
    q4 = generate_superposition(seed + 4)
    q5 = generate_odd_one_out(seed + 5)
    q6 = generate_mirror(seed + 6)
    
    # Shuffle options for each to make it more random
    questions = [q1, q2, q3, q4, q5, q6]
    for q in questions:
        c_idx = q["correctIndex"]
        opts = q["options"]
        correct_opt = opts[c_idx]
        
        # shuffle options
        shuffled_opts = list(opts)
        random.Random(seed).shuffle(shuffled_opts)
        
        new_c_idx = shuffled_opts.index(correct_opt)
        q["options"] = shuffled_opts
        q["correctIndex"] = new_c_idx
        seed += 1
        
    return questions
