import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Badge, Alert, Nav, Tab } from 'react-bootstrap';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import ProjectRoadmap from '../components/project/ProjectRoadmap';
import ShareModal from '../components/project/EditModal'; // doğru yoldan import et
import projectService from '../services/projectService';
import { Carousel } from 'react-bootstrap';

const ProjectDetail = () => {
  const { id } = useParams();
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('steps');
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    const fetchProject = async () => {
      try {
        // Try to get project from our API
        const token = localStorage.getItem('access_token');
        if (!token) {
          throw new Error('Authentication required');
        }

        const response = await axios.get(`http://127.0.0.1:8000/project/my-ideas/${id}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        setProject(response.data);
      } catch (err) {
        console.error('Project fetch error:', err);
        setError('Proje bilgileri yüklenemedi. Lütfen tekrar deneyin.');
        
        // Geliştirme aşaması için örnek proje verileri
        setProject({
          id: parseInt(id),
          name: 'Örnek Proje',
          description: 'Bu bir örnek projedir. Gerçek proje verileri API\'den gelecektir.',
          image: 'https://placehold.co/800x400/28a745/white?text=Ornek+Proje',
          user_id: 1,
          materials: [
            'Cam şişe veya kavanoz',
            'LED ışık dizisi',
            'Yapıştırıcı',
            'Dekoratif malzemeler'
          ],
          steps: [
            'Şişeyi iyice temizleyin ve kurulayın',
            'LED ışıkları şişenin içine yerleştirin',
            'Dekoratif malzemelerle şişeyi süsleyin',
            'Şişeyi uygun bir yerde sergileyin'
          ],
          difficulty: 'Orta',
          estimated_time: '2 saat',
          user: {
            username: 'ornek_kullanici'
          }
        });
      } finally {
        setLoading(false);
      }
    };

    fetchProject();
  }, [id]);

  // Extract materials list from roadmap steps
  const getMaterialsList = () => {
    if (!project || !project.roadmap) return [];
    
    // Collect all unique materials from roadmap steps
    const materialsSet = new Set();
    project.roadmap.forEach(step => {
      if (step.materials_needed && Array.isArray(step.materials_needed)) {
        step.materials_needed.forEach(material => materialsSet.add(material));
      }
    });
    
    return Array.from(materialsSet);
  };

  if (loading) {
    return (
      <Container className="py-5 text-center">
        <div className="spinner-border text-success" role="status">
          <span className="visually-hidden">Yükleniyor...</span>
        </div>
        <p className="mt-2">Proje detayları yükleniyor...</p>
      </Container>
    );
  }

  // Get image URL
  const getImageUrl = () => {
    if (!project || !project.image) return 'https://placehold.co/800x400/28a745/white?text=No+Image';
    
    // If image is a full URL, use it directly
    if (project.image.startsWith('http')) {
      return project.image;
    }
    
    // Otherwise, assume it's a path on the server
    return `http://127.0.0.1:8000/${project.image}`;
  };

  // Generate steps list from roadmap
  const getStepsList = () => {
    if (!project || !project.roadmap || !project.roadmap.length) {
      return project?.steps || [];
    }
    // console.log("roadmap: ",project.roadmap);
    
    return project.roadmap.map(step => step.description);
  };

  return (
    <Container className="py-5">
      {error && <Alert variant="danger">{error}</Alert>}
      
      {project && (
        <>
          <Row className="mb-4">
            <Col>
              <div className="d-flex justify-content-between align-items-center mb-3">
                <h1>{project.title}</h1>
                <div>
                  <Button variant="outline-secondary" as={Link} to="/explore" className="me-2">
                    <i className="fas fa-arrow-left me-2"></i>Geri
                  </Button>
                </div>
              </div>
              <p className="text-muted">
                <i className="fas fa-user me-2"></i>
                {project.user ? project.user : 'Kullanıcı'}
                {console.log("project.user: ", project.user)}
              </p>
            </Col>
          </Row>

          <Row className="mb-5">
            <Col lg={8}>
              
              {/* <img 
                src={getImageUrl()} 
                alt={project.name} 
                className="img-fluid rounded shadow mb-4"
                style={{ 
                  width: '100%',
                  height: '400px',           // Sabit yükseklik
                  objectFit: 'contain',      // Resim taşmadan içeri sığar
                  objectPosition: 'center',  // Ortalanır
                  backgroundColor: '#f8f9fa' // Boşluklar görünürse hoş dursun
                }}
              /> */}
              {project.recycled_image
              ? (
                <Carousel className="mb-4 shadow rounded" style={{ backgroundColor: '#f8f9fa' }}>
                  {/* Ana proje görseli */}
                  <Carousel.Item>
                    <img
                      className="d-block w-100"
                      src={project.image.startsWith('http') ? project.image : `http://127.0.0.1:8000/${project.image}`}
                      alt={project.name}
                      style={{
                        height: '400px',
                        objectFit: 'contain',
                        objectPosition: 'center'
                      }}
                    />
                  </Carousel.Item>

                  {/* Geri dönüştürülmüş görsel(ler) */}
                  {(Array.isArray(project.recycled_image) ? project.recycled_image : [project.recycled_image]).map((img, index) => (
                    <Carousel.Item key={index}>
                      <img
                        className="d-block w-100"
                        src={img.startsWith('http') ? img : `http://127.0.0.1:8000/${img}`}
                        alt={`Recycled ${index + 1}`}
                        style={{
                          height: '400px',
                          objectFit: 'contain',
                          objectPosition: 'center'
                        }}
                      />
                    </Carousel.Item>
                  ))}
                </Carousel>
              ) : (
                // Sadece ana görseli göster
                <img 
                  src={project.image.startsWith('http') ? project.image : `http://127.0.0.1:8000/${project.image}`} 
                  alt={project.name} 
                  className="img-fluid rounded shadow mb-4"
                  style={{ 
                    width: '100%',
                    height: '400px',
                    objectFit: 'contain',
                    objectPosition: 'center',
                    backgroundColor: '#f8f9fa'
                  }}
                />
              )
            }

              <Card className="shadow-sm border-0 mb-4">
                <Card.Body>
                  <h4>Proje Açıklaması</h4>
                  <p>{project.description}</p>
                </Card.Body>
              </Card>
            </Col>
            
            <Col lg={4}>
              <Card className="shadow-sm border-0 mb-4">
                  <Card.Body>
                    <h4 className="mb-3">Proje Detayları</h4>
                    <p>
                      <i className="fas fa-globe me-2 text-primary"></i>
                      <strong>Görünürlük:</strong> {project.is_public ? 'Herkese Açık' : 'Gizli'}
                    </p>
                    <div className="d-grid">
                    <Button variant="warning" onClick={() => setShowModal(true)}>
                        <i className="fas fa-edit me-2"></i>Projeyi Güncelle
                      </Button>

                      <ShareModal 
                        show={showModal} 
                        onHide={() => setShowModal(false)} 
                        projectId={project.id}
                      />
                    </div>
                  </Card.Body>
              </Card>
              
              <Card className="shadow-sm border-0 mb-4">
                <Card.Body>
                  <h4 className="mb-3">Gerekli Malzemeler</h4>
                  <ul className="list-group list-group-flush">
                    {(project.materials || getMaterialsList()).map((material, index) => (
                      <li key={index} className="list-group-item d-flex align-items-center border-0 px-0">
                        <i className="fas fa-check-circle text-success me-2"></i>
                        {material}
                      </li>
                    ))}
                  </ul>
                </Card.Body>
              </Card>
            </Col>
          </Row>
          
          <Row>
            <Col>
              <Card className="shadow-sm border-0">
              <Card.Header className="bg-white border-bottom pt-3">
                <h4 className="mb-0">
                  <i className="fas fa-project-diagram me-2"></i>Proje Yol Haritası
                </h4>
              </Card.Header>

                <Card.Body>
                  <h4 className="mb-4">Proje Yol Haritası</h4>
                  <ProjectRoadmap roadmap={project.roadmap} />
                </Card.Body>

              </Card>
            </Col>
          </Row>
        </>
      )}
    </Container>
  );
};

export default ProjectDetail; 

