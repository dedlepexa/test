import streamlit as st
import numpy as np
import json
import random

# ============================================================
# ПАРАМЕТРЫ СЕТИ
# ============================================================
input_size = 100
hidden_size = 100
output_size = 14

# ============================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ РИСОВАНИЯ
# ============================================================
def create_blank():
    return np.zeros((10, 10))

def draw_line(img, x1, y1, x2, y2, thickness=1):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    while True:
        for tx in range(-thickness//2, thickness//2+1):
            for ty in range(-thickness//2, thickness//2+1):
                if 0 <= x1+tx < 10 and 0 <= y1+ty < 10:
                    img[y1+ty, x1+tx] = 1
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

def draw_rect(img, x1, y1, x2, y2, thickness=1):
    draw_line(img, x1, y1, x2, y1, thickness)
    draw_line(img, x2, y1, x2, y2, thickness)
    draw_line(img, x2, y2, x1, y2, thickness)
    draw_line(img, x1, y2, x1, y1, thickness)

def draw_filled_rect(img, x1, y1, x2, y2):
    for y in range(y1, y2+1):
        for x in range(x1, x2+1):
            if 0 <= x < 10 and 0 <= y < 10:
                img[y, x] = 1

def draw_circle(img, cx, cy, r, thickness=1):
    for y in range(cy-r, cy+r+1):
        for x in range(cx-r, cx+r+1):
            if 0 <= x < 10 and 0 <= y < 10:
                dist = np.sqrt((x-cx)**2 + (y-cy)**2)
                if abs(dist - r) <= thickness/2:
                    img[y, x] = 1

# ============================================================
# ШАБЛОНЫ ЦИФР 0-9
# ============================================================
def digit_template(digit):
    img = create_blank()
    if digit == 0:
        draw_rect(img, 1, 1, 8, 8, 2)
    elif digit == 1:
        draw_line(img, 5, 1, 5, 8, 2)
        draw_line(img, 4, 3, 5, 2, 1)
    elif digit == 2:
        draw_line(img, 1, 1, 8, 1, 2)
        draw_line(img, 8, 1, 8, 4, 2)
        draw_line(img, 8, 4, 1, 4, 2)
        draw_line(img, 1, 4, 1, 8, 2)
        draw_line(img, 1, 8, 8, 8, 2)
    elif digit == 3:
        draw_line(img, 1, 1, 8, 1, 2)
        draw_line(img, 8, 1, 8, 8, 2)
        draw_line(img, 1, 4, 8, 4, 2)
        draw_line(img, 8, 8, 1, 8, 2)
    elif digit == 4:
        draw_line(img, 1, 1, 1, 5, 2)
        draw_line(img, 1, 5, 8, 5, 2)
        draw_line(img, 8, 1, 8, 8, 2)
    elif digit == 5:
        draw_line(img, 1, 1, 8, 1, 2)
        draw_line(img, 1, 1, 1, 4, 2)
        draw_line(img, 1, 4, 8, 4, 2)
        draw_line(img, 8, 4, 8, 8, 2)
        draw_line(img, 8, 8, 1, 8, 2)
    elif digit == 6:
        draw_line(img, 1, 1, 8, 1, 2)
        draw_line(img, 1, 1, 1, 8, 2)
        draw_line(img, 1, 4, 8, 4, 2)
        draw_line(img, 8, 4, 8, 8, 2)
        draw_line(img, 8, 8, 1, 8, 2)
    elif digit == 7:
        draw_line(img, 1, 1, 8, 1, 2)
        draw_line(img, 8, 1, 8, 8, 2)
    elif digit == 8:
        draw_rect(img, 1, 1, 8, 8, 2)
        draw_line(img, 1, 4, 8, 4, 2)
    elif digit == 9:
        draw_line(img, 1, 1, 8, 1, 2)
        draw_line(img, 8, 1, 8, 8, 2)
        draw_line(img, 1, 4, 8, 4, 2)
        draw_line(img, 1, 1, 1, 4, 2)
    return img

# ============================================================
# ШАБЛОНЫ ФИГУР
# ============================================================
def snowman_template():
    img = create_blank()
    draw_circle(img, 5, 2, 1, 2)
    draw_circle(img, 5, 5, 2, 2)
    draw_circle(img, 5, 8, 3, 2)
    return img

def carrot_template():
    img = create_blank()
    draw_line(img, 5, 8, 2, 2, 2)
    draw_line(img, 5, 8, 8, 2, 2)
    draw_line(img, 2, 2, 8, 2, 1)
    draw_line(img, 3, 2, 3, 0, 1)
    draw_line(img, 5, 2, 5, 0, 1)
    draw_line(img, 7, 2, 7, 0, 1)
    return img

def hat_template():
    img = create_blank()
    draw_line(img, 2, 2, 7, 2, 2)
    draw_rect(img, 3, 3, 6, 8, 2)
    return img

def tree_template():
    img = create_blank()
    draw_line(img, 5, 0, 1, 4, 2)
    draw_line(img, 5, 0, 9, 4, 2)
    draw_line(img, 1, 4, 9, 4, 2)
    draw_line(img, 5, 2, 2, 6, 2)
    draw_line(img, 5, 2, 8, 6, 2)
    draw_line(img, 2, 6, 8, 6, 2)
    draw_line(img, 5, 4, 3, 8, 2)
    draw_line(img, 5, 4, 7, 8, 2)
    draw_line(img, 3, 8, 7, 8, 2)
    draw_filled_rect(img, 4, 8, 5, 9)
    return img

# ============================================================
# АУГМЕНТАЦИЯ
# ============================================================
def augment(img):
    img = img.copy()
    mask = np.random.rand(*img.shape) < 0.10
    img[mask] = 1 - img[mask]
    dx = random.randint(-3, 3)
    dy = random.randint(-3, 3)
    shifted = np.zeros_like(img)
    for y in range(10):
        for x in range(10):
            if 0 <= x+dx < 10 and 0 <= y+dy < 10:
                shifted[y+dy, x+dx] = img[y, x]
    img = shifted
    if random.random() < 0.6:
        angle = random.uniform(-15, 15) * np.pi / 180
        rotated = np.zeros_like(img)
        for y in range(10):
            for x in range(10):
                cx, cy = 4.5, 4.5
                new_x = int(round(np.cos(angle)*(x-cx) - np.sin(angle)*(y-cy) + cx))
                new_y = int(round(np.sin(angle)*(x-cx) + np.cos(angle)*(y-cy) + cy))
                if 0 <= new_x < 10 and 0 <= new_y < 10:
                    rotated[new_y, new_x] = img[y, x]
        img = rotated
    if random.random() < 0.5:
        remove_mask = np.random.rand(*img.shape) < 0.15
        img[remove_mask] = 0
    if random.random() < 0.4:
        add_mask = np.random.rand(*img.shape) < 0.1
        img[add_mask] = 1
    return img

# ============================================================
# ОБУЧЕНИЕ (кэшируется — выполняется один раз)
# ============================================================
@st.cache_resource(show_spinner=False)
def train_and_split():
    X = []
    y = []
    for class_id in range(10):
        base = digit_template(class_id)
        for _ in range(300):
            X.append(augment(base).flatten())
            y.append(class_id)
    figures = [snowman_template(), carrot_template(), hat_template(), tree_template()]
    for idx, fig in enumerate(figures):
        class_id = 10 + idx
        for _ in range(300):
            X.append(augment(fig).flatten())
            y.append(class_id)

    X = np.array(X)
    y_onehot = np.eye(output_size)[y]

    np.random.seed(42)
    W1 = np.random.randn(input_size, hidden_size) * 0.1
    b1 = np.zeros((1, hidden_size))
    W2 = np.random.randn(hidden_size, output_size) * 0.1
    b2 = np.zeros((1, output_size))

    def sigmoid(x):
        return 1 / (1 + np.exp(-x))
    def sigmoid_deriv(x):
        return x * (1 - x)

    lr = 0.5
    epochs = 10000
    for epoch in range(epochs):
        hidden_input = np.dot(X, W1) + b1
        hidden_output = sigmoid(hidden_input)
        final_input = np.dot(hidden_output, W2) + b2
        final_output = sigmoid(final_input)
        error = y_onehot - final_output

        d_final = error * sigmoid_deriv(final_output)
        d_hidden = d_final.dot(W2.T) * sigmoid_deriv(hidden_output)
        W2 += hidden_output.T.dot(d_final) * lr
        b2 += np.sum(d_final, axis=0, keepdims=True) * lr
        W1 += X.T.dot(d_hidden) * lr
        b1 += np.sum(d_hidden, axis=0, keepdims=True) * lr

    weights_parts = {}
    W1_list = W1.tolist()
    rows_per_part_w1 = 7
    num_parts_w1 = (100 + rows_per_part_w1 - 1) // rows_per_part_w1
    for part in range(num_parts_w1):
        start = part * rows_per_part_w1
        end = min(start + rows_per_part_w1, 100)
        weights_parts[f"w1_{part+1}"] = {"W1": W1_list[start:end]}

    W2_list = W2.tolist()
    rows_per_part_w2 = 20
    num_parts_w2 = (100 + rows_per_part_w2 - 1) // rows_per_part_w2
    for part in range(num_parts_w2):
        start = part * rows_per_part_w2
        end = min(start + rows_per_part_w2, 100)
        weights_parts[f"w2_{part+1}"] = {"W2": W2_list[start:end]}

    weights_parts["biases"] = {"b1": b1[0].tolist(), "b2": b2[0].tolist()}
    return weights_parts

# ============================================================
# STREAMLIT UI
# ============================================================
st.set_page_config(page_title="Нейросеть 10x10", page_icon="🧠")
st.title("🧠 Нейросеть для распознавания цифр и фигур 10x10")
st.write("Обучение происходит на CPU и кэшируется — запускается один раз.")

if st.button("🚀 Train (обучить сеть)"):
    with st.spinner("Обучение... Это может занять несколько минут."):
        train_and_split()
    st.success("✅ Обучение завершено. Веса готовы.")

st.divider()
st.subheader("Получить веса по частям")

part_input = st.text_input(
    "Название части",
    placeholder="например: w1_1, w2_3, biases",
)

if st.button("📤 Получить часть"):
    parts = train_and_split()
    key = part_input.strip().lower()
    if key in parts:
        st.code(json.dumps(parts[key]), language="json")
    else:
        st.error(f"Часть '{key}' не найдена. Доступные: {', '.join(parts.keys())}")
