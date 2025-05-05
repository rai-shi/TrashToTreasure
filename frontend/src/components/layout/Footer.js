import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

const Footer = () => {
  return (
    <footer className="footer py-4 mt-auto">
      <Container>
        <Row className="text-center text-white">
          <Col>
            <h5>♻️ TrashToTreasure</h5>
            <p className="mb-0">Atıklarınızı değerli hazinelere dönüştürün</p>
            <p className="small mt-3">&copy; {new Date().getFullYear()} TrashToTreasure | Sürdürülebilir Yaşam</p>
          </Col>
        </Row>
        <Row className="mt-3">
          <Col md={4} className="text-center text-md-start">
            <h6 className="text-white">Hakkımızda</h6>
            <p className="text-white-50 small">
              TrashToTreasure, sürdürülebilir yaşamı destekleyen ve atıkları değerli ürünlere dönüştürmenize yardımcı olan bir platformdur.
            </p>
          </Col>
          <Col md={4} className="text-center">
            <h6 className="text-white">Sosyal Medya</h6>
            <div className="d-flex justify-content-center gap-3 mt-2">
              <a href="#" className="text-white"><i className="fab fa-facebook-f"></i></a>
              <a href="#" className="text-white"><i className="fab fa-twitter"></i></a>
              <a href="#" className="text-white"><i className="fab fa-instagram"></i></a>
              <a href="#" className="text-white"><i className="fab fa-youtube"></i></a>
            </div>
          </Col>
          <Col md={4} className="text-center text-md-end mt-3 mt-md-0">
            <h6 className="text-white">İletişim</h6>
            <p className="text-white-50 small mb-0">
              <i className="fas fa-envelope me-2"></i>info@trashtotreasure.com
            </p>
            <p className="text-white-50 small">
              <i className="fas fa-phone me-2"></i>+90 (212) 345 67 89
            </p>
          </Col>
        </Row>
      </Container>
    </footer>
  );
};

export default Footer; 