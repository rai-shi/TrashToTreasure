import React, { useState } from 'react';
import { Container, Row, Col, Card, Form, Button, ListGroup, Spinner, Alert } from 'react-bootstrap';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const ProjectIdeaSelector = ({ token }) => {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [ideas, setIdeas] = useState([]);
  const [selectedIdea, setSelectedIdea] = useState(null);
  const [imagePath, setImagePath] = useState(null);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    setFile(selected);
    setPreviewUrl(URL.createObjectURL(selected));
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("image", file);

      const response = await axios.post("/project/create-ideas", formData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setIdeas(response.data.ideas);
      setImagePath(response.data.image);
    } catch (err) {
      setError("Bir hata oluştu. Lütfen tekrar deneyin.");
    } finally {
      setLoading(false);
    }
  };

  const handleSelectIdea = async () => {
    if (!selectedIdea) return;
    setSaving(true);
    setError(null);

    try {
      await axios.post(
        "/project/save-idea",
        {
          title: selectedIdea.title,
          description: selectedIdea.description,
          image_path: imagePath,
          materials: selectedIdea.materials,
          roadmap: selectedIdea.roadmap,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      navigate("/project/my-ideas");
    } catch (err) {
      setError("Proje kaydedilemedi.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <Container className="py-5">
      <h2 className="text-center mb-4">Fikir Oluştur</h2>

      {!ideas.length ? (
        <Card className="mx-auto p-4" style={{ maxWidth: 500 }}>
          <Form.Group>
            <Form.Label>Bir görsel yükleyin</Form.Label>
            <Form.Control type="file" accept="image/*" onChange={handleFileChange} />
          </Form.Group>

          {previewUrl && (
            <img
              src={previewUrl}
              alt="Önizleme"
              className="img-fluid img-thumbnail mt-3"
              style={{ maxHeight: 200 }}
            />
          )}

          <div className="d-grid mt-4">
            <Button variant="primary" onClick={handleUpload} disabled={loading || !file}>
              {loading ? <Spinner animation="border" size="sm" /> : "Fikirleri Oluştur"}
            </Button>
          </div>

          {error && <Alert variant="danger" className="mt-3">{error}</Alert>}
        </Card>
      ) : (
        <>
          <Row className="g-4 mt-4">
            {ideas.map((idea, index) => (
              <Col md={4} key={index}>
                <Card
                  className={`h-100 ${selectedIdea?.title === idea.title ? 'border-success shadow' : ''}`}
                  onClick={() => setSelectedIdea(idea)}
                  style={{ cursor: 'pointer' }}
                >
                  <Card.Body>
                    <Card.Title>{idea.title}</Card.Title>
                    <Card.Text>{idea.description}</Card.Text>
                    <h6>Gerekli Malzemeler:</h6>
                    <ul>
                      {idea.materials.map((m, i) => <li key={i}>{m}</li>)}
                    </ul>
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>

          {selectedIdea && (
            <Card className="mt-5">
              <Card.Header>
                <h5>Seçilen Fikir: {selectedIdea.title}</h5>
              </Card.Header>
              <Card.Body>
                <h6>Yol Haritası:</h6>
                <ListGroup variant="flush">
                  {selectedIdea.roadmap.map((step, i) => (
                    <ListGroup.Item key={i}>{i + 1}. {step}</ListGroup.Item>
                  ))}
                </ListGroup>

                <div className="d-grid mt-4">
                  <Button
                    variant="success"
                    onClick={handleSelectIdea}
                    disabled={saving}
                  >
                    {saving ? <Spinner animation="border" size="sm" /> : "Bu Projeyi Seç"}
                  </Button>
                </div>

                {error && <Alert variant="danger" className="mt-3">{error}</Alert>}
              </Card.Body>
            </Card>
          )}
        </>
      )}
    </Container>
  );
};

export default ProjectIdeaSelector;
