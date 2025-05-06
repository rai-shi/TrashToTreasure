import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Navbar, Nav, Container } from 'react-bootstrap';

const AppNavbar = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    setIsAuthenticated(!!token);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    setIsAuthenticated(false);
    navigate('/');
  };

  return (
    <Navbar bg="light" expand="lg" className="shadow-sm mb-4">
      <Container>
        <Navbar.Brand as={Link} to="/">
          ♻️ TrashToTreasure
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto">
            <Nav.Link as={Link} to="/">Ana Sayfa</Nav.Link>
            <Nav.Link as={Link} to="/explore">Keşfet</Nav.Link>

            {isAuthenticated ? (
              <>
                <Nav.Link as={Link} to="/profile">Profil</Nav.Link>
                <Nav.Link as="button" onClick={handleLogout}>Çıkış Yap</Nav.Link>
              </>
            ) : (
              <>
                <Nav.Link as={Link} to="/login">Giriş Yap</Nav.Link>
                <Nav.Link as={Link} to="/register">Kayıt Ol</Nav.Link>
              </>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default AppNavbar;
