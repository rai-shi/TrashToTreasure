import React, { useState } from 'react';
import { Container, Row, Col, Card, Form, Button, Alert } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import projectService from '../services/projectService';

const NewProject = () => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    image: null
  });
  const [previewUrl, setPreviewUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [step, setStep] = useState(1);
  const [projectId, setProjectId] = useState(null);
  const navigate = useNavigate();

  const { name, description } = formData;

  // Form değişikliğini izleme
  const onChange = e => {
    if (e.target.name === 'image') {
      // Görsel yükleme işlemi
      const file = e.target.files[0];
      setFormData({ ...formData, image: file });
      
      // Görsel önizleme
      if (file) {
        const reader = new FileReader();
        reader.onloadend = () => {
          setPreviewUrl(reader.result);
        };
        reader.readAsDataURL(file);
      } else {
        setPreviewUrl('');
      }
    } else {
      setFormData({ ...formData, [e.target.name]: e.target.value });
    }
  };

  // Form gönderme
  const onSubmit = async e => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Form doğrulama
    if (!name || !description || !formData.image) {
      setError('Lütfen tüm alanları doldurun ve bir görsel yükleyin.');
      setLoading(false);
      return;
    }

    try {
      // Project service kullanarak API'ye gönder
      const result = await projectService.createProject(
        { name, description },
        formData.image
      );
      
      console.log('Project created:', result);
      setProjectId(result.project_id);
      setLoading(false);
      setStep(2); // Başarılı olduğunda sonraki adıma geç
      
    } catch (err) {
      console.error('Error creating project:', err);
      // Handle different error formats safely
      let errorMessage = 'Proje oluşturulurken bir hata oluştu.';
      
      if (err.response && err.response.data) {
        if (typeof err.response.data.detail === 'string') {
          errorMessage = err.response.data.detail;
        } else if (err.response.data.detail && err.response.data.detail.msg) {
          errorMessage = err.response.data.detail.msg;
        }
      }
      
      setError(errorMessage);
      setLoading(false);
    }
  };

  // Roadmap gösterme ve projeye git
  const viewRoadmap = () => {
    if (projectId) {
      navigate(`/project/${projectId}`);
    } else {
      // Test için geçici yönlendirme
      navigate('/profile');
    }
  };

  return (
    <Container className="py-5">
      <Row className="justify-content-center">
        <Col lg={8}>
          <Card className="shadow border-0">
            <Card.Header className="bg-white border-0 text-center py-3">
              <h3 className="mb-0">
                {step === 1 ? 'Yeni Proje Oluştur' : 'Proje Oluşturuldu!'}
              </h3>
            </Card.Header>
            
            {/* Adım 1: Proje Bilgisi ve Görsel Yükleme */}
            {step === 1 && (
              <Card.Body className="px-4 py-4">
                {error && <Alert variant="danger">{error}</Alert>}
                
                <Form onSubmit={onSubmit}>
                  <Form.Group className="mb-3">
                    <Form.Label>Proje Adı</Form.Label>
                    <Form.Control
                      type="text"
                      placeholder="Projeniz için bir isim girin"
                      name="name"
                      value={name}
                      onChange={onChange}
                    />
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label>Açıklama</Form.Label>
                    <Form.Control
                      as="textarea"
                      rows={3}
                      placeholder="Dönüştürmek istediğiniz eşyayı tanımlayın"
                      name="description"
                      value={description}
                      onChange={onChange}
                    />
                    <Form.Text className="text-muted">
                      Bu eşyayı nasıl dönüştürmek istediğinizi detaylı olarak anlatın.
                    </Form.Text>
                  </Form.Group>

                  <Form.Group className="mb-4">
                    <Form.Label>Eşya Görseli</Form.Label>
                    <Form.Control
                      type="file"
                      accept="image/*"
                      name="image"
                      onChange={onChange}
                    />
                    <Form.Text className="text-muted">
                      Dönüştürmek istediğiniz eşyanın fotoğrafını yükleyin.
                    </Form.Text>
                  </Form.Group>

                  {previewUrl && (
                    <div className="text-center mb-4">
                      <img 
                        src={previewUrl} 
                        alt="Önizleme" 
                        style={{ maxHeight: '200px' }} 
                        className="img-thumbnail"
                      />
                    </div>
                  )}

                  <div className="d-grid">
                    <Button 
                      variant="success" 
                      type="submit"
                      disabled={loading}
                    >
                      {loading ? (
                        <>
                          <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                          İşleniyor...
                        </>
                      ) : (
                        'Projeyi Oluştur'
                      )}
                    </Button>
                  </div>
                </Form>
              </Card.Body>
            )}
            
            {/* Adım 2: Başarılı Oluşturma */}
            {step === 2 && (
              <Card.Body className="px-4 py-5 text-center">
                <div className="mb-4">
                  <div className="bg-success text-white rounded-circle d-inline-flex justify-content-center align-items-center" style={{width: '80px', height: '80px'}}>
                    <i className="fas fa-check fa-3x"></i>
                  </div>
                </div>
                
                <h4 className="mb-3">Projeniz Başarıyla Oluşturuldu!</h4>
                <p className="text-muted mb-4">
                  Yüklediğiniz fotoğraf ve açıklamaya göre dönüşüm yol haritası hazırlanmıştır.
                </p>
                
                <div className="d-grid">
                  <Button 
                    variant="success" 
                    size="lg"
                    onClick={viewRoadmap}
                  >
                    <i className="fas fa-map-signs me-2"></i>
                    Yol Haritasını Görüntüle
                  </Button>
                </div>
              </Card.Body>
            )}
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default NewProject; 