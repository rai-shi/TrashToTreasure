import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Form, InputGroup } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const Explore = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    // Örnek proje verileri - gerçek uygulamada API'den gelecek
    const dummyProjects = [
      {
        id: 1,
        name: 'Şişe Lamba',
        description: 'Eski cam şişeleri dekoratif lambalara dönüştürün.',
        image: 'https://placehold.co/300x200/28a745/white?text=Sise+Lamba',
        user: {
          username: 'recycle_master'
        }
      },
      {
        id: 2,
        name: 'Palet Sehpa',
        description: 'Atık ahşap paletlerden şık bir sehpa yapımı.',
        image: 'https://placehold.co/300x200/28a745/white?text=Palet+Sehpa',
        user: {
          username: 'wood_crafter'
        }
      },
      {
        id: 3,
        name: 'T-Shirt Çanta',
        description: 'Eski tişörtlerinizden dikişsiz alışveriş çantası yapın.',
        image: 'https://placehold.co/300x200/28a745/white?text=Tisort+Canta',
        user: {
          username: 'eco_designer'
        }
      },
      {
        id: 4,
        name: 'Kavanoz Mumluk',
        description: 'Kullanılmış cam kavanozları şık mumlara dönüştürün.',
        image: 'https://placehold.co/300x200/28a745/white?text=Kavanoz+Mumluk',
        user: {
          username: 'candle_maker'
        }
      },
      {
        id: 5,
        name: 'Kitap Rafı',
        description: 'Eski tahtalardan minimalist kitaplık yapımı.',
        image: 'https://placehold.co/300x200/28a745/white?text=Kitap+Rafi',
        user: {
          username: 'bookworm'
        }
      },
      {
        id: 6,
        name: 'Dergi Sepeti',
        description: 'Eski dergilerden örülmüş saklama sepeti.',
        image: 'https://placehold.co/300x200/28a745/white?text=Dergi+Sepeti',
        user: {
          username: 'paper_artist'
        }
      }
    ];

    setProjects(dummyProjects);
    setLoading(false);
  }, []);

  // Arama fonksiyonu
  const filteredProjects = projects.filter(project =>
    project.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    project.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <Container className="py-5">
      <h1 className="text-center mb-5">Projeleri Keşfet</h1>

      {/* Arama ve Filtreleme */}
      <Row className="mb-4">
        <Col md={8} className="mx-auto">
          <InputGroup>
            <Form.Control
              placeholder="Proje ara..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <Button variant="success">
              <i className="fas fa-search"></i>
            </Button>
          </InputGroup>
        </Col>
      </Row>

      {/* Projeler Listesi */}
      {loading ? (
        <div className="text-center py-5">
          <div className="spinner-border text-success" role="status">
            <span className="visually-hidden">Yükleniyor...</span>
          </div>
        </div>
      ) : (
        <>
          {filteredProjects.length === 0 ? (
            <div className="text-center py-5">
              <i className="fas fa-search fa-3x text-muted mb-3"></i>
              <p className="text-muted">"{searchTerm}" ile ilgili proje bulunamadı.</p>
            </div>
          ) : (
            <Row>
              {filteredProjects.map(project => (
                <Col md={4} className="mb-4" key={project.id}>
                  <Card className="h-100 project-card shadow-sm">
                    <Card.Img variant="top" src={project.image} alt={project.name} />
                    <Card.Body>
                      <Card.Title>{project.name}</Card.Title>
                      <Card.Text>{project.description}</Card.Text>
                      <p className="text-muted small mb-0">
                        <i className="fas fa-user me-1"></i> {project.user.username}
                      </p>
                    </Card.Body>
                    <Card.Footer className="bg-white border-0">
                      <Button
                        as={Link}
                        to={`/project/${project.id}`}
                        variant="outline-success"
                        className="w-100"
                      >
                        <i className="fas fa-eye me-2"></i>Detayları Gör
                      </Button>
                    </Card.Footer>
                  </Card>
                </Col>
              ))}
            </Row>
          )}
        </>
      )}
    </Container>
  );
};

export default Explore; 