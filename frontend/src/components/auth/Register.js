import React, { useState } from 'react';
import { Container, Row, Col, Card, Form, Button, Alert } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

// Axios için backend URL'ini ayarla
axios.defaults.baseURL = 'http://localhost:8002';

const Register = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const { username, email, first_name, last_name, password, confirmPassword } = formData;

  const onChange = e => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const onSubmit = async e => {
    e.preventDefault();
    setError('');
    setLoading(true);
    
    console.log('Form gönderiliyor:', formData);

    // Validation
    if (!username || !email || !first_name || !last_name || !password || !confirmPassword) {
      setError('Lütfen tüm alanları doldurunuz');
      setLoading(false);
      return;
    }

    if (password !== confirmPassword) {
      setError('Şifreler eşleşmiyor');
      setLoading(false);
      return;
    }

    if (password.length < 8) {
      setError('Şifre en az 8 karakter olmalıdır');
      setLoading(false);
      return;
    }

    try {
      // API isteği
      console.log('Axios isteği gönderiliyor...');
      const res = await axios.post('/auth/register', {
        username,
        email,
        first_name,
        last_name,
        password
      });

      console.log('Yanıt alındı:', res);

      // Başarılı kayıt
      if (res.data && res.data.id) {
        console.log('Kayıt başarılı, giriş sayfasına yönlendiriliyor');
        navigate('/login');
      } else {
        console.warn('Sunucudan beklenen yanıt alınamadı:', res.data);
        setError('Beklenmeyen bir hata oluştu. Lütfen daha sonra tekrar deneyin.');
      }
    } catch (err) {
      console.error("Kayıt hatası - tam hata:", err);
      console.error("Hata konfigürasyonu:", err.config);
      console.error("Hata yanıtı:", err.response);
      
      // Error handling düzeltildi
      if (err.response && err.response.data && err.response.data.detail) {
        // String olarak hata mesajı al
        setError(typeof err.response.data.detail === 'string' 
          ? err.response.data.detail 
          : 'Formatta hata var. Lütfen girdiğiniz bilgileri kontrol edin.');
      } else {
        setError('Sunucu bağlantısında bir sorun oluştu. Lütfen daha sonra tekrar deneyin.');
      }
    } finally {
      console.log('İşlem tamamlandı, loading durumu kapatılıyor');
      setLoading(false);
    }
  };

  return (
    <Container className="py-5">
      <Row className="justify-content-center">
        <Col md={8}>
          <Card className="shadow border-0">
            <Card.Header className="bg-white border-0 text-center py-3">
              <h3 className="mb-0">Hesap Oluştur</h3>
            </Card.Header>
            <Card.Body className="px-4 py-4">
              {error && <Alert variant="danger">{error}</Alert>}
              
              <Form onSubmit={onSubmit}>
                <Row>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>Ad</Form.Label>
                      <Form.Control
                        type="text"
                        placeholder="Adınızı giriniz"
                        name="first_name"
                        value={first_name}
                        onChange={onChange}
                        required
                      />
                    </Form.Group>
                  </Col>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>Soyad</Form.Label>
                      <Form.Control
                        type="text"
                        placeholder="Soyadınızı giriniz"
                        name="last_name"
                        value={last_name}
                        onChange={onChange}
                        required
                      />
                    </Form.Group>
                  </Col>
                </Row>

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

                <Form.Group className="mb-3">
                  <Form.Label>Email</Form.Label>
                  <Form.Control
                    type="email"
                    placeholder="Email adresinizi giriniz"
                    name="email"
                    value={email}
                    onChange={onChange}
                    required
                  />
                </Form.Group>

                <Row>
                  <Col md={6}>
                    <Form.Group className="mb-4">
                      <Form.Label>Şifre</Form.Label>
                      <Form.Control
                        type="password"
                        placeholder="Şifre giriniz"
                        name="password"
                        value={password}
                        onChange={onChange}
                        required
                      />
                      <Form.Text className="text-muted">
                        En az 8 karakter olmalıdır.
                      </Form.Text>
                    </Form.Group>
                  </Col>
                  <Col md={6}>
                    <Form.Group className="mb-4">
                      <Form.Label>Şifre Tekrarı</Form.Label>
                      <Form.Control
                        type="password"
                        placeholder="Şifreyi tekrar giriniz"
                        name="confirmPassword"
                        value={confirmPassword}
                        onChange={onChange}
                        required
                      />
                    </Form.Group>
                  </Col>
                </Row>

                <div className="d-grid">
                  <Button 
                    variant="success" 
                    type="submit"
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                        Kayıt yapılıyor...
                      </>
                    ) : (
                      'Kayıt Ol'
                    )}
                  </Button>
                </div>
              </Form>
            </Card.Body>
            <Card.Footer className="bg-white border-0 text-center py-3">
              <p className="mb-0">
                Zaten hesabınız var mı? <Link to="/login" className="text-success">Giriş yapın</Link>
              </p>
            </Card.Footer>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Register; 