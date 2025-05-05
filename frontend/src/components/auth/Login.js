import React, { useState } from 'react';
import { Container, Row, Col, Card, Form, Button, Alert } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

// Axios için backend URL'ini ayarla
axios.defaults.baseURL = 'http://localhost:8002';

const Login = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const { username, password } = formData;

  const onChange = e => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const onSubmit = async e => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Validation
    if (!username || !password) {
      setError('Tüm alanları doldurunuz');
      setLoading(false);
      return;
    }

    try {
      // API isteği
      const res = await axios.post('/auth/login', {
        username,
        password
      });

      // Başarılı login
      if (res.data && res.data.access_token) {
        localStorage.setItem('token', res.data.access_token);
        navigate('/profile');
      } else {
        setError('Beklenmeyen bir hata oluştu.');
      }
    } catch (err) {
      console.error("Login hatası:", err);
      
      // Error handling düzeltildi
      if (err.response && err.response.data && err.response.data.detail) {
        // String olarak hata mesajı al
        setError(typeof err.response.data.detail === 'string' 
          ? err.response.data.detail 
          : 'Formatta hata var. Lütfen girdiğiniz bilgileri kontrol edin.');
      } else {
        setError('Sunucu bağlantısında bir sorun oluştu.');
      }
    }

    setLoading(false);
  };

  return (
    <Container className="py-5">
      <Row className="justify-content-center">
        <Col md={6}>
          <Card className="shadow border-0">
            <Card.Header className="bg-white border-0 text-center py-3">
              <h3 className="mb-0">Giriş Yap</h3>
            </Card.Header>
            <Card.Body className="px-4 py-4">
              {error && <Alert variant="danger">{error}</Alert>}
              
              <Form onSubmit={onSubmit}>
                <Form.Group className="mb-3">
                  <Form.Label>Kullanıcı Adı</Form.Label>
                  <Form.Control
                    type="text"
                    placeholder="Kullanıcı adınızı giriniz"
                    name="username"
                    value={username}
                    onChange={onChange}
                    required
                  />
                </Form.Group>

                <Form.Group className="mb-4">
                  <Form.Label>Şifre</Form.Label>
                  <Form.Control
                    type="password"
                    placeholder="Şifrenizi giriniz"
                    name="password"
                    value={password}
                    onChange={onChange}
                    required
                  />
                </Form.Group>

                <div className="d-grid">
                  <Button 
                    variant="success" 
                    type="submit"
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                        Giriş yapılıyor...
                      </>
                    ) : (
                      'Giriş Yap'
                    )}
                  </Button>
                </div>
              </Form>
            </Card.Body>
            <Card.Footer className="bg-white border-0 text-center py-3">
              <p className="mb-0">
                Hesabınız yok mu? <Link to="/register" className="text-success">Kayıt olun</Link>
              </p>
            </Card.Footer>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Login; 