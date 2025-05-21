import React, { useState } from "react";
import ReactDOM from "react-dom/client";

function App() {
  const [imageFile, setImageFile] = useState(null); // Lưu trữ file ảnh
  const [imagePreviewUrl, setImagePreviewUrl] = useState(null); // URL để xem trước ảnh
  const [recommendationResult, setRecommendationResult] = useState(null); // Lưu toàn bộ kết quả từ API
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImageFile(file);
      setImagePreviewUrl(URL.createObjectURL(file)); // Tạo URL xem trước tạm thời
      setRecommendationResult(null); // Xóa kết quả cũ khi chọn ảnh mới
      setError(null); // Xóa lỗi cũ
    }
  };

  const handleSubmit = async () => {
    if (!imageFile) {
      setError("Vui lòng chọn một hình ảnh để tải lên.");
      return;
    }

    setLoading(true);
    setRecommendationResult(null);
    setError(null);

    const formData = new FormData();
    formData.append("image", imageFile); // Gửi file ảnh

    try {
      // Thay thế URL nếu backend của bạn chạy trên một địa chỉ khác
      const response = await fetch("http://127.0.0.1:5000/api/predict", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        // Cố gắng đọc lỗi từ JSON nếu có
        let errorData = { message: `Lỗi từ server: ${response.status} ${response.statusText}` };
        try {
            const errJson = await response.json();
            errorData.message = errJson.error || errorData.message;
        } catch (e) {
            // Không thể parse JSON lỗi, giữ lỗi gốc
        }
        throw new Error(errorData.message);
      }

      const result = await response.json();
      setRecommendationResult(result);

    } catch (err) {
      console.error("Lỗi khi gửi yêu cầu dự đoán:", err);
      setError(err.message || "Đã xảy ra lỗi không xác định khi thực hiện dự đoán. Vui lòng thử lại.");
    }
    setLoading(false);
  };

  // --- CSS Styles (có thể tách ra file .css riêng) ---
  const styles = {
    container: {
      maxWidth: "900px",
      margin: "2rem auto",
      padding: "25px",
      fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
      textAlign: "center",
      backgroundColor: "#f9f9f9",
      borderRadius: "12px",
      boxShadow: "0 4px 15px rgba(0, 0, 0, 0.1)",
    },
    title: {
      color: "#2c3e50",
      marginBottom: "25px",
      fontSize: "2em",
    },
    input: {
      display: "block",
      margin: "25px auto",
      padding: "12px 15px",
      border: "2px dashed #bdc3c7",
      borderRadius: "8px",
      cursor: "pointer",
      backgroundColor: "#fff",
    },
    button: {
      padding: "12px 25px",
      fontSize: "1.1em",
      color: "white",
      backgroundColor: "#3498db",
      border: "none",
      borderRadius: "8px",
      cursor: "pointer",
      transition: "background-color 0.3s ease",
      boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
    },
    buttonDisabled: {
      backgroundColor: "#bdc3c7",
      cursor: "not-allowed",
    },
    imagePreviewContainer: {
      margin: "25px 0",
      padding: "15px",
      border: "1px solid #ecf0f1",
      borderRadius: "8px",
      backgroundColor: "#fff",
    },
    imagePreview: {
      maxWidth: "250px",
      maxHeight: "250px",
      margin: "10px auto",
      borderRadius: "4px",
      border: "1px solid #ddd",
      objectFit: "contain",
    },
    resultsContainer: {
      marginTop: "35px",
      textAlign: "left",
      borderTop: "2px solid #ecf0f1",
      paddingTop: "25px",
    },
    resultsTitle: {
      textAlign: "center",
      color: "#2c3e50",
      marginBottom: "20px",
    },
    categoryText: {
      fontSize: "1.1em",
      color: "#34495e",
      marginBottom: "8px",
    },
    suggestionText: {
      fontSize: "1em",
      color: "#7f8c8d",
      fontStyle: "italic",
      marginBottom: "20px",
    },
    outfitGrid: {
      display: "flex",
      flexWrap: "wrap",
      justifyContent: "center",
      gap: "20px",
      marginTop: "15px",
    },
    outfitItemCard: {
      border: "1px solid #ecf0f1",
      padding: "15px",
      borderRadius: "8px",
      textAlign: "center",
      width: "180px", // Độ rộng cho mỗi item trong bộ đồ
      backgroundColor: "#fff",
      boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
      transition: "transform 0.2s ease-in-out",
    },
    outfitItemImage: {
      width: "100%",
      height: "200px", // Chiều cao cố định cho ảnh item
      objectFit: "cover", // Cắt ảnh cho vừa, không làm méo
      marginBottom: "10px",
      borderRadius: "4px",
    },
    outfitItemName: {
      fontSize: "0.95em",
      color: "#34495e",
      fontWeight: "bold",
      minHeight: "40px", // Để các thẻ có chiều cao đồng đều hơn
    },
    outfitItemCategory: {
      fontSize: "0.8em",
      color: "#95a5a6",
    },
    errorText: {
      color: "#e74c3c",
      marginTop: "20px",
      fontWeight: "bold",
    },
    loadingText: {
        fontSize: "1.1em",
        color: "#3498db",
    }
  };
  // Hover effect for outfit item card
  const handleMouseOver = (e) => { e.currentTarget.style.transform = 'scale(1.03)'; };
  const handleMouseOut = (e) => { e.currentTarget.style.transform = 'scale(1)'; };


  return (
    <div style={styles.container}>
      <h1 style={styles.title}>AI Fashion Stylist</h1>
      <p style={{color: "#7f8c8d", marginBottom: "20px"}}>Tải lên một ảnh trang phục, chúng tôi sẽ gợi ý cách phối đồ cho bạn!</p>

      <input
        type="file"
        accept="image/*"
        onChange={handleImageUpload}
        style={styles.input}
      />

      {imagePreviewUrl && (
        <div style={styles.imagePreviewContainer}>
          <h3 style={{color: "#34495e"}}>Ảnh bạn đã chọn:</h3>
          <img src={imagePreviewUrl} alt="Xem trước ảnh tải lên" style={styles.imagePreview} />
        </div>
      )}

      <button
        onClick={handleSubmit}
        disabled={loading || !imageFile}
        style={{...styles.button, ...( (loading || !imageFile) && styles.buttonDisabled) }}
      >
        {loading ? "Đang xử lý..." : "Nhận Gợi Ý Phong Cách"}
      </button>

      {loading && <p style={styles.loadingText}>Model AI đang phân tích và phối đồ, vui lòng chờ...</p>}
      {error && <p style={styles.errorText}><strong>Lỗi:</strong> {error}</p>}

      {recommendationResult && (
        <div style={styles.resultsContainer}>
          <h2 style={styles.resultsTitle}>Đây là gợi ý dành cho bạn:</h2>
          <p style={styles.categoryText}>
            <strong>Item chính trong ảnh của bạn thuộc danh mục:</strong> {recommendationResult.input_item_category}
          </p>
          <p style={styles.suggestionText}>
            "{recommendationResult.suggestion_text}"
          </p>

          <h3 style={{ marginTop: "25px", color: "#34495e", textAlign: "center" }}>Bộ trang phục đề xuất:</h3>
          <div style={styles.outfitGrid}>
            {recommendationResult.suggested_outfit && recommendationResult.suggested_outfit.map((item, index) => (
              <div 
                key={index} 
                style={styles.outfitItemCard}
                onMouseOver={handleMouseOver}
                onMouseOut={handleMouseOut}
              >
                <img
                    src={item.image_url}
                    alt={item.name}
                    style={styles.outfitItemImage}
                    onError={(e) => { e.target.onerror = null; e.target.src="https://placehold.co/200x300/CCCCCC/FFFFFF?text=Image+Error"; }} // Fallback image
                />
                <p style={styles.outfitItemName}>{item.name}</p>
                <p style={styles.outfitItemCategory}>({item.category})</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);