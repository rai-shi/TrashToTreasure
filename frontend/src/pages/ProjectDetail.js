import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Badge, Alert, Nav, Tab } from 'react-bootstrap';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import ProjectRoadmap from '../components/project/ProjectRoadmap';
import projectService from '../services/projectService';

const ProjectDetail = () => {
  const { id } = useParams();
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('steps');

  useEffect(() => {
    const fetchProject = async () => {
      try {
        // Try to get project from our API
        const token = localStorage.getItem('token');
        if (!token) {
          throw new Error('Authentication required');
        }

        const response = await axios.get(`http://localhost:8002/projects/${id}`, {
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
    return `http://localhost:8002/${project.image}`;
  };

  // Generate steps list from roadmap
  const getStepsList = () => {
    if (!project || !project.roadmap || !project.roadmap.length) {
      return project?.steps || [];
    }
    
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
                <h1>{project.name}</h1>
                <div>
                  <Button variant="outline-secondary" as={Link} to="/explore" className="me-2">
                    <i className="fas fa-arrow-left me-2"></i>Geri
                  </Button>
                </div>
              </div>
              <p className="text-muted">
                <i className="fas fa-user me-2"></i>
                {project.user && project.user.username ? project.user.username : 'Kullanıcı'}
              </p>
            </Col>
          </Row>

          <Row className="mb-5">
            <Col lg={8}>
              <img 
                src={getImageUrl()} 
                alt={project.name} 
                className="img-fluid rounded shadow mb-4 w-100"
                style={{ maxHeight: '400px', objectFit: 'cover' }}
              />
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
                    <i className="fas fa-star-half-alt me-2 text-warning"></i>
                    <strong>Zorluk:</strong> {project.difficulty || 'Orta'}
                  </p>
                  <p>
                    <i className="fas fa-clock me-2 text-info"></i>
                    <strong>Tahmini Süre:</strong> {project.estimated_time || '2 saat'}
                  </p>
                  <div className="d-grid">
                    <Button variant="success">
                      <i className="fas fa-heart me-2"></i>Favorilere Ekle
                    </Button>
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
                  <Nav variant="tabs" className="border-bottom-0" activeKey={activeTab} onSelect={setActiveTab}>
                    <Nav.Item>
                      <Nav.Link eventKey="steps">
                        <i className="fas fa-list-ol me-2"></i>Adımlar
                      </Nav.Link>
                    </Nav.Item>
                    <Nav.Item>
                      <Nav.Link eventKey="roadmap">
                        <i className="fas fa-project-diagram me-2"></i>Yol Haritası
                      </Nav.Link>
                    </Nav.Item>
                  </Nav>
                </Card.Header>
                <Card.Body>
                  <Tab.Content>
                    <Tab.Pane eventKey="steps">
                      <h4 className="mb-4">Yapım Adımları</h4>
                      <div className="timeline">
                        {getStepsList().map((step, index) => (
                          <div key={index} className="timeline-item mb-4">
                            <div className="d-flex">
                              <div className="me-3">
                                <Badge bg="success" className="p-2 rounded-circle">{index + 1}</Badge>
                              </div>
                              <div>
                                <p className="mb-0">{step}</p>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </Tab.Pane>
                    <Tab.Pane eventKey="roadmap">
                      <h4 className="mb-4">Proje Yol Haritası</h4>
                      <div className="roadmap-container">
                        <ProjectRoadmap projectId={project.id} />
                      </div>
                    </Tab.Pane>
                  </Tab.Content>
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