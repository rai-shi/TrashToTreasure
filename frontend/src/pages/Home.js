import React from 'react';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const Home = () => {
  // Örnek öne çıkan projeler
  const featuredProjects = [
    {
      id: 1,
      title: 'Şişe Lamba',
      description: 'Eski cam şişeleri dekoratif lambalara dönüştürün.',
      image: 'https://placehold.co/300x200/28a745/white?text=Sise+Lamba'
    },
    {
      id: 2,
      title: 'Palet Sehpa',
      description: 'Atık ahşap paletlerden şık bir sehpa yapımı.',
      image: 'https://placehold.co/300x200/28a745/white?text=Palet+Sehpa'
    },
    {
      id: 3,
      title: 'T-Shirt Çanta',
      description: 'Eski tişörtlerinizden dikişsiz alışveriş çantası yapın.',
      image: 'https://placehold.co/300x200/28a745/white?text=Tisort+Canta'
    }
  ];

  return (
    <>
      {/* Hero Section */}
      <div className="hero-section">
        <Container className="text-center py-5">
          <h1 className="display-4 fw-bold">♻️ Trash to Treasure</h1>
          <p className="lead">Kullanmadığınız eşyalarınızı yaratıcı ve sürdürülebilir projelere dönüştürün</p>
          <div className="mt-4">
            <Button
              as={Link}
              to="/project/new"
              variant="success"
              size="lg"
              className="me-2"
            >
              <i className="fas fa-recycle me-2"></i>Dönüştürmeye Başla
            </Button>
            <Button
              as={Link}
              to="/explore"
              variant="outline-dark"
              size="lg"
            >
              <i className="fas fa-search me-2"></i>Projeleri Keşfet
            </Button>
          </div>
        </Container>
      </div>

      {/* Nasıl Çalışır */}
      <Container className="py-5">
        <h2 className="text-center mb-5">Nasıl Çalışır?</h2>
        
        <Row>
          <Col md={4} className="mb-4">
            <Card className="h-100 text-center border-0 shadow-sm">
              <Card.Body>
                <div className="text-success mb-3">
                  <i className="fas fa-upload fa-3x"></i>
                </div>
                <Card.Title>Yükle</Card.Title>
                <Card.Text>
                  Dönüştürmek istediğiniz eşyanın fotoğrafını çekip platformumuza yükleyin.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
          
          <Col md={4} className="mb-4">
            <Card className="h-100 text-center border-0 shadow-sm">
              <Card.Body>
                <div className="text-success mb-3">
                  <i className="fas fa-lightbulb fa-3x"></i>
                </div>
                <Card.Title>Fikir Al</Card.Title>
                <Card.Text>
                  Yapay zeka eşyanızı analiz ederek yaratıcı dönüşüm fikirleri sunar.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
          
          <Col md={4} className="mb-4">
            <Card className="h-100 text-center border-0 shadow-sm">
              <Card.Body>
                <div className="text-success mb-3">
                  <i className="fas fa-hands fa-3x"></i>
                </div>
                <Card.Title>Oluştur</Card.Title>
                <Card.Text>
                  Adım adım rehberimizi takip ederek güzel ve kullanışlı bir şey yaratın.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>

      {/* Öne Çıkan Projeler */}
      <Container className="py-5">
        <h2 className="text-center mb-4">Öne Çıkan Projeler</h2>
        <Row>
          {featuredProjects.map(project => (
            <Col md={4} className="mb-4" key={project.id}>
              <Card className="project-card h-100 shadow-sm">
                <Card.Img variant="top" src={project.image} alt={project.title} />
                <Card.Body>
                  <Card.Title>{project.title}</Card.Title>
                  <Card.Text>{project.description}</Card.Text>
                </Card.Body>
                <Card.Footer className="bg-white border-0">
                  <Button variant="outline-success" as={Link} to={`/project/${project.id}`}>
                    Detayları Gör
                  </Button>
                </Card.Footer>
              </Card>
            </Col>
          ))}
        </Row>
        <div className="text-center mt-4">
          <Button variant="success" as={Link} to="/explore">
            Tüm Projeleri Keşfet
          </Button>
        </div>
      </Container>

      {/* Sürdürülebilirlik Hakkında */}
      <div className="bg-light py-5 mt-5">
        <Container>
          <Row className="align-items-center">
            <Col md={6} className="mb-4 mb-md-0">
              <h2>Sürdürülebilir Yaşam için Atıkları Dönüştür</h2>
              <p className="lead">
                Her yıl milyonlarca ton atık çöp sahalarında son buluyor. TrashToTreasure ile bu atıkları değerli eşyalara dönüştürerek çevreye katkıda bulunabilirsiniz.
              </p>
              <p>
                Platformumuz, sürdürülebilir yaşam pratiklerini teşvik ederek tüketim kültürüne alternatif sunar. Atık malzemeleri yeniden kullanarak hem doğal kaynakları korur hem de yaratıcılığınızı geliştirebilirsiniz.
              </p>
            </Col>
            <Col md={6} className="text-center">
              <img 
                src="https://placehold.co/600x400/28a745/white?text=Surdurulebilirlik" 
                alt="Sürdürülebilirlik" 
                className="img-fluid rounded shadow"
              />
            </Col>
          </Row>
        </Container>
      </div>
    </>
  );
};

export default Home; 