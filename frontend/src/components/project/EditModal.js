import React, { useState } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';
import axios from 'axios';

const ShareModal = ({ show, onHide, projectId }) => {
  const [image, setImage] = useState(null);
  const [isPublic, setIsPublic] = useState(true);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!image) return;

    setLoading(true);

    try {
    //   const base64Image = await toBase64(image);
      const token = localStorage.getItem("access_token");

      const formData = new FormData();
        formData.append("recycled_image", image); // file: input.files[0]
        formData.append("is_public", true);

        await axios.put(`http://127.0.0.1:8000/project/my-ideas/${projectId}`, formData, {
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "multipart/form-data"
        }
        });

      alert("Paylaşım başarıyla güncellendi!");
      onHide(); // modalı kapat
    } catch (error) {
      console.error("Güncelleme hatası:", error);
      alert("Bir hata oluştu.");
    } finally {
      setLoading(false);
    }
  };

  const toBase64 = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
  });

  return (
    <Modal show={show} onHide={onHide} centered>
      <Modal.Header closeButton>
        <Modal.Title>Geri Dönüşüm Paylaşımı</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <p>Geri dönüştürdüğünüz ürünün resmini yükleyip paylaşmak ister misiniz?</p>
        <Form.Group>
          <Form.Label>Resim Yükle</Form.Label>
          <Form.Control type="file" accept="image/*" onChange={e => setImage(e.target.files[0])} />
        </Form.Group>
        <Form.Group className="mt-3">
          <Form.Check 
            type="checkbox"
            label="Herkese açık olarak paylaş"
            checked={isPublic}
            onChange={e => setIsPublic(e.target.checked)}
          />
        </Form.Group>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>İptal</Button>
        <Button variant="success" onClick={handleSubmit} disabled={loading}>
          {loading ? "Yükleniyor..." : "Paylaş"}
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ShareModal;
