from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import random # Sẽ dùng để giả lập nếu logic model chưa có

app = Flask(__name__)
CORS(app)

# --- Tải Model Phân Loại Item Chính ---
# Model này sẽ phân loại item chính trong ảnh người dùng tải lên.
MODEL_CLASSIFICATION = None
MODEL_PATH = "outfit_recommender_v2.h5" # Đảm bảo file này tồn tại

try:
    MODEL_CLASSIFICATION = tf.keras.models.load_model(MODEL_PATH)
    print(f"Đã tải model phân loại '{MODEL_PATH}' thành công!")
except Exception as e:
    print(f"LỖI NGHIÊM TRỌNG: Không thể tải model phân loại '{MODEL_PATH}'. Lỗi: {e}")
    print("Ứng dụng có thể không hoạt động đúng nếu không có model này.")
    # Trong trường hợp này, có thể bạn muốn ứng dụng không khởi động
    # hoặc có một cơ chế fallback rất rõ ràng.
    # For now, we'll let it run and it will likely fail at predict or use mock data.

CLASSES = [ # Danh sách các lớp mà MODEL_CLASSIFICATION có thể dự đoán
    "Jackets & Vests", "Shirts & Polos", "Suiting", "Blouses & Shirts",
    "Cardigans", "Dresses", "Graphic Tees", "Jackets & Coats", "Leggings",
    "Rompers & Jumpsuits", "Skirts", "Denim", "Pants", "Shorts",
    "Sweaters", "Sweatshirts & Hoodies", "Tees & Tanks"
]

# --- Hàm Tiền Xử Lý Ảnh cho Model Phân Loại ---
def preprocess_image_for_classification(image_bytes, target_size=(224, 224)):
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image.resize(target_size)
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        return image_array
    except Exception as e:
        print(f"Lỗi khi tiền xử lý ảnh: {e}")
        return None

# --- LOGIC CỐT LÕI: Sinh Gợi Ý Bộ Trang Phục ---
# Đây là phần bạn cần HOÀN THIỆN dựa trên model/hệ thống của bạn.
# Hàm này nhận vào danh mục của item chính (và có thể là các đặc trưng khác từ model)
# và trả về một danh sách các item cho bộ đồ gợi ý.
def generate_full_outfit_suggestion(classified_item_category, input_image_features=None):
    """
    Hàm này cần được BẠN HOÀN THIỆN.
    Nó sẽ sử dụng model `outfit_recommender_v2.h5` của bạn (hoặc một model/logic khác)
    để tạo ra một bộ trang phục hoàn chỉnh.

    Input:
        classified_item_category (str): Danh mục của item chính đã được phân loại.
        input_image_features (any): Có thể là các đặc trưng trích xuất từ ảnh đầu vào
                                     mà model gợi ý bộ trang phục của bạn cần.

    Output:
        suggested_outfit (list of dict): Danh sách các item, mỗi item là một dict
                                         ví dụ: {"name": "Tên Item", "category": "Loại", "image_url": "url_anh.jpg"}
        suggestion_text (str): Một đoạn văn bản mô tả gợi ý.
    """

    # ---- BẮT ĐẦU PHẦN BẠN CẦN THAY THẾ BẰNG LOGIC MODEL CỦA BẠN ----
    # Logic giả lập hiện tại:
    print(f"Đang tạo gợi ý giả lập cho item đầu vào thuộc danh mục: {classified_item_category}")
    suggestion_text = f"Với một item '{classified_item_category}', đây là một gợi ý phối đồ thú vị dành cho bạn:"
    outfit_items = []

    # Thêm item "gốc" (dựa trên phân loại) - bạn có thể không cần bước này nếu model của bạn sinh cả bộ
    # Chúng ta không có ảnh của item gốc, nên sẽ dùng placeholder hoặc chỉ tên
    # outfit_items.append({
    #     "name": f"Item bạn chọn ({classified_item_category})",
    #     "category": classified_item_category,
    #     "image_url": "https://placehold.co/200x300/EEEEEE/AAAAAA?text=Input+Item"
    # })

    # Logic giả lập để chọn các item khác
    mock_db = {
        "Tops": {"name": "Áo Thun Basic Fit", "image_url": "https://placehold.co/200x300/E2E8F0/AAAAAA?text=Áo+Thun+Fit"},
        "Bottoms": {"name": "Quần Jeans Ống Đứng", "image_url": "https://placehold.co/200x300/A0AEC0/FFFFFF?text=Quần+Jean+Ống+Đứng"},
        "Shoes": {"name": "Giày Sneaker Cổ Điển", "image_url": "https://placehold.co/200x300/CBD5E0/FFFFFF?text=Sneaker+Cổ+Điển"},
        "Outerwear": {"name": "Áo Khoác Bomber Kaki", "image_url": "https://placehold.co/200x300/718096/FFFFFF?text=Áo+Khoác+Kaki"},
        "Accessories": {"name": "Mũ Lưỡi Trai Năng Động", "image_url": "https://placehold.co/200x300/4A5568/FFFFFF?text=Mũ+Lưỡi+Trai"}
    }

    if classified_item_category in ["Tees & Tanks", "Graphic Tees", "Shirts & Polos", "Blouses & Shirts"]:
        # Item đầu vào là áo
        outfit_items.append({"category": "Bottoms", **mock_db["Bottoms"]})
        outfit_items.append({"category": "Shoes", **mock_db["Shoes"]})
        if random.random() > 0.5: outfit_items.append({"category": "Outerwear", **mock_db["Outerwear"]})
    elif classified_item_category in ["Dresses", "Rompers & Jumpsuits"]:
        # Item đầu vào là váy/đầm liền
        outfit_items.append({"category": "Shoes", **mock_db["Shoes"]})
        outfit_items.append({"category": "Accessories", **mock_db["Accessories"]})
    elif classified_item_category in ["Skirts", "Denim", "Pants", "Shorts", "Leggings"]:
        # Item đầu vào là quần/váy
        outfit_items.append({"category": "Tops", **mock_db["Tops"]})
        outfit_items.append({"category": "Shoes", **mock_db["Shoes"]})
    else: # Các trường hợp khác (áo khoác, suit, etc.)
        outfit_items.append({"category": "Tops", **mock_db["Tops"]})
        outfit_items.append({"category": "Bottoms", **mock_db["Bottoms"]})
        outfit_items.append({"category": "Shoes", **mock_db["Shoes"]})

    # Đảm bảo không có item nào trùng với category của item đầu vào (trừ khi đó là ý đồ)
    # Ví dụ: nếu input là "Tops", thì trong các item gợi ý không nên có "Tops" nữa.
    # Logic giả lập trên có thể tạo ra điều này, bạn cần kiểm soát.
    # ---- KẾT THÚC PHẦN BẠN CẦN THAY THẾ ----

    return suggestion_text, outfit_items[:3] # Giới hạn 3 item gợi ý thêm (cho demo)

@app.route("/api/predict", methods=["POST"])
def predict_api_route():
    if "image" not in request.files:
        return jsonify({"error": "Không tìm thấy file ảnh tải lên."}), 400

    image_file = request.files["image"]

    try:
        image_bytes = image_file.read()
        processed_image_for_classification = preprocess_image_for_classification(image_bytes)
        if processed_image_for_classification is None:
            return jsonify({"error": "Không thể xử lý ảnh đầu vào."}), 400
    except Exception as e:
        return jsonify({"error": f"Lỗi khi đọc hoặc xử lý file ảnh: {str(e)}"}), 400

    # 1. Phân loại item chính trong ảnh
    classified_category = "Không xác định"
    input_image_features_for_outfit_model = None # Khởi tạo

    if MODEL_CLASSIFICATION is not None:
        try:
            prediction_scores = MODEL_CLASSIFICATION.predict(processed_image_for_classification)
            predicted_class_index = np.argmax(prediction_scores[0])

            if 0 <= predicted_class_index < len(CLASSES):
                classified_category = CLASSES[predicted_class_index]
                # --- TRÍCH XUẤT ĐẶC TRƯNG (NẾU CẦN) ---
                # Nếu model gợi ý bộ trang phục của bạn cần đặc trưng từ ảnh gốc (không chỉ danh mục),
                # bạn có thể cần trích xuất chúng ở đây từ MODEL_CLASSIFICATION hoặc một model khác.
                # Ví dụ:
                # layer_name = 'name_of_a_feature_layer_in_MODEL_CLASSIFICATION'
                # feature_extractor_model = tf.keras.Model(inputs=MODEL_CLASSIFICATION.input,
                #                                        outputs=MODEL_CLASSIFICATION.get_layer(layer_name).output)
                # input_image_features_for_outfit_model = feature_extractor_model.predict(processed_image_for_classification)
                # ---------------------------------------
            else:
                print(f"CẢNH BÁO: predicted_class_index ({predicted_class_index}) nằm ngoài phạm vi của CLASSES.")
                classified_category = "Danh mục không xác định (lỗi index)"
        except Exception as e:
            print(f"Lỗi khi thực hiện dự đoán bằng model phân loại: {str(e)}")
            # Fallback nếu model phân loại lỗi
            classified_category = random.choice(CLASSES) if CLASSES else "Fallback Category"
    else:
        print("CẢNH BÁO: Model phân loại không được tải. Sử dụng category ngẫu nhiên cho đầu vào.")
        classified_category = random.choice(CLASSES) if CLASSES else "Fallback Category"


    # 2. Sinh gợi ý bộ trang phục dựa trên item đã phân loại (và có thể là đặc trưng)
    # Gọi hàm mà BẠN SẼ HOÀN THIỆN với logic model của mình
    suggestion_text, suggested_outfit_items = generate_full_outfit_suggestion(
        classified_category,
        input_image_features_for_outfit_model # Truyền đặc trưng nếu model của bạn cần
    )

    return jsonify({
        "input_item_category": classified_category,
        "suggestion_text": suggestion_text,
        "suggested_outfit": suggested_outfit_items
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)