import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Alert } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import projectService from '../services/projectService';

// Backend base URL
const API_URL = "http://127.0.0.1:8000";

const Profile = () => {
  const navigate = useNavigate();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [projects, setProjects] = useState([]);

  const handleDelete = async (itemId) => {
    if (!window.confirm("Bu projeyi silmek istediğinize emin misiniz?")) return;
  
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        alert("Giriş yapmanız gerekiyor.");
        return;
      }
  
      const response = await axios.delete(`${API_URL}/project/my-ideas/${itemId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
  
      if (response.status === 204) {
        alert("Proje başarıyla silindi.");
        // Silinen projeyi listeden çıkar
        setProjects(prevProjects => prevProjects.filter(p => p.id !== itemId));
      } else {
        alert("Proje silinemedi.");
      }
    } catch (error) {
      console.error("Silme hatası:", error);
      alert("Bir hata oluştu, lütfen tekrar deneyin.");
    }
  };
  

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        // Check if token exists
        const token = localStorage.getItem('access_token');
        if (!token) {
          navigate('/login');
          return;
        }

        // Fetch user profile
        const profileRes = await axios.get(`${API_URL}/user/profile`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        if (profileRes.data && profileRes.data.user) {
          setProfile(profileRes.data.user);
          
          // Fetch user projects
          try {
            const projects = await projectService.getUserProjects();
            setProjects(projects);
          } catch (err) {
            console.log('Projeler yüklenemedi, örnek veriler gösteriliyor.');
            // Example projects (for when API fails)
            setProjects([
              {
                id: 1,
                name: 'Cam Şişe Lamba',
                description: 'Eski şişelerden dekoratif bir lamba projesi',
                image: 'https://placehold.co/300x200/28a745/white?text=Sise+Lamba'
              }
            ]);
          }
        }
      } catch (err) {
        console.error('Profile fetch error:', err);
        
        // Check if it's an authentication error
        if (err.response && (err.response.status === 401 || err.response.status === 403)) {
          // Clear token and redirect to login
          localStorage.removeItem('access_token');
          navigate('/login');
          return;
        }
        
        setError('Profil bilgileri yüklenemedi. Lütfen tekrar deneyin.');
        
        // Use placeholder profile data for development
        setProfile({
          first_name: 'Test',
          last_name: 'User',
          username: 'testuser',
          email: 'test@example.com'
        });
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [navigate]);

  // Get image URL
  const getImageUrl = (imagePath) => {
    if (!imagePath) return 'https://placehold.co/300x200/28a745/white?text=No+Image';
    
    // If image is a full URL, use it directly
    if (imagePath.startsWith('http')) {
      return imagePath;
    }
    console.log('Image path:', imagePath);
    // Otherwise, assume it's a path on the server
    return `${API_URL}/${imagePath}`;
  };

  if (loading) {
    return (
      <Container className="py-5 text-center">
        <div className="spinner-border text-success" role="status">
          <span className="visually-hidden">Yükleniyor...</span>
        </div>
        <p className="mt-2">Profil yükleniyor...</p>
      </Container>
    );
  }

  return (
    <Container className="py-5">
      {error && <Alert variant="danger">{error}</Alert>}
      
      <Row>
        {/* Profil Bilgileri */}
        <Col lg={4} className="mb-4">
          <Card className="shadow border-0">
            <Card.Header className="bg-white text-center py-4 border-0">
              <div className="mb-3">
                <i className="fas fa-user-circle fa-5x text-secondary"></i>
              </div>
              {profile && (
                <>
                  <h3>{profile.first_name} {profile.last_name}</h3>
                  <p className="text-muted mb-0">@{profile.username}</p>
                </>
              )}
            </Card.Header>
            <Card.Body>
              {profile && (
                <>
                  <p className="mb-2">
                    <i className="fas fa-envelope me-2 text-success"></i>
                    {profile.email}
                  </p>
                  <p className="mb-0">
                    <i className="fas fa-recycle me-2 text-success"></i>
                    {projects.length} Proje
                  </p>
                </>
              )}
            </Card.Body>
            <Card.Footer className="bg-white border-0 py-3">
              <Button variant="outline-secondary" size="sm" className="w-100">
                <i className="fas fa-cog me-2"></i>Profil Düzenle
              </Button>
            </Card.Footer>
          </Card>
        </Col>
        
        {/* Projeler */}
        <Col lg={8}>
          <Card className="shadow border-0">
            <Card.Header className="bg-white py-3 d-flex justify-content-between align-items-center">
              <h4 className="mb-0">Projelerim</h4>
              <Button
                as={Link}
                to="/project/new"
                variant="success"
                size="sm"
              >
                <i className="fas fa-plus me-2"></i>Yeni Proje
              </Button>
            </Card.Header>
            <Card.Body>
              {projects.length === 0 ? (
                <div className="text-center py-5">
                  <i className="fas fa-seedling fa-3x text-muted mb-3"></i>
                  <p className="text-muted">Henüz hiç projeniz yok. Yeni bir proje oluşturarak başlayabilirsiniz.</p>
                  <Button
                    as={Link}
                    to="/project/new"
                    variant="success"
                  >
                    <i className="fas fa-plus me-2"></i>İlk Projeyi Oluştur
                  </Button>
                </div>
              ) : (
                <Row>
                  {projects.map(project => (
                    <Col md={6} className="mb-4" key={project.id}>
                      <Card className="h-100 project-card shadow-sm">
                        <Card.Img variant="top" src={getImageUrl(project.image)} alt={project.name} />
                        <Card.Body>
                          <Card.Title>{project.name}</Card.Title>
                          <Card.Text>{project.description}</Card.Text>
                        </Card.Body>
                        <Card.Footer className="bg-white border-0">
                          <div className="d-flex justify-content-between">
                            <Button
                              as={Link}
                              to={`/project/${project.id}`}
                              variant="outline-success"
                              size="sm"
                            >
                              <i className="fas fa-eye me-2"></i>Görüntüle
                            </Button>
                            <Button
                              variant="outline-danger"
                              size="sm"
                              onClick={() => handleDelete(project.id)} // itemId, silmek istediğin projenin id'si olmalı
                            >
                              <i className="fas fa-trash-alt me-2"></i>Sil
                            </Button>
                          </div>
                        </Card.Footer>
                      </Card>
                    </Col>
                  ))}
                </Row>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Profile; 