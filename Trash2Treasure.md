görsel algılama + bilgi filtreleme + yaratıcı fikir üretimi + görselleştirme + rehber üretimi

* image detection
  * BLIP-2, CLIP    
  * Google Gemini Pro Vision
* bilgi filtreleme
  * RAG + LLM (gpt, gemini)
* Roadmap üretimi ?
  * LLM çıktısı customize edilebilir. Çıktıyı biz görselleştirebiliriz. örneğin <stop> gibi keywordler olur ki oradan parse ederiz. daha sonra adım adım oklarla görselleştirme yapılır.
* görselleştirme ?? sonraki bir ekleme olabilir
  * google imagen





# ♻️ Trash2Treasure

**Trash2Treasure**, kullanıcıların kullanmadıkları eşyaları dönüştürerek tekrar kullanabilmelerine imkân sağlayan sürdürülebilirlik odaklı bir web uygulamasıdır. Kullanıcılar ürünlerinin fotoğraflarını sisteme yükler, sistem bu ürünü analiz ederek eldeki materyallerle ne gibi yaratıcı geri dönüşüm projeleri üretilebileceğini önerir.

---

## 🧩 Proje Senaryosu

1. Kullanıcı sisteme giriş yapar.
2. Elinde geri dönüştürmek istediği bir ürünün fotoğrafını yükler.
3. AI, görsel tanıma yoluyla ürünün materyalini ve kullanım durumunu analiz eder.
4. Sistem, kullanıcıya birkaç geri dönüşüm fikri sunar (örneğin: eski tişört ➝ çanta, minder kılıfı, ip).
5. Ardından, "Elinizde hangi materyaller var?" gibi bir form sunulur (checkbox/keyword input).
6. Kullanıcı elindeki araç ve malzemeleri seçer (örneğin: makas, boya, iplik).
7. AI, bu girdilere göre uygulanabilir projeleri tekrar filtreleyerek sunar.
8. Seçilen proje için bir yol haritası (roadmap) oluşturulur: adım adım rehber, gerekirse 3D model/diffusion görseli ile.
9. Kullanıcılar uygulama içinde yaptıkları projeleri paylaşabilir, diğer kullanıcıların projelerine göz atabilir.


?? ürün işlenir, rag araması geri dönüşüm ürünü-fikir eşleşmelerinden materyaller çıkarılır, onlar arasından inceleme ile tekrar bir filtreleme yapılır, uygun eşleşmelerden geri dönüşüm fikirleri sunulur. seçili üründen roadmap çıkarılır.


---

## ⚙️ Teknik Mimari

### Backend
- **FastAPI**: RESTful API ve AI entegrasyonu
- **PostgreSQL**: Kullanıcılar, projeler, geri dönüşüm fikirleri gibi veri yapıları için
- **Qdrant**: Görsel + metin tabanlı benzerlik karşılaştırmaları için vektör veritabanı
- **Python AI Components**:
  - **CLIP / BLIP / GPT-4-V**: Görsel analiz ve açıklama üretimi
  - **GPT-4 / RAG Pipeline**: Geri dönüşüm fikirleri ve adım adım yol haritası üretimi
  - **Diffusion Model**: Ürün fikirlerinin AI tabanlı görselleştirilmesi (isteğe bağlı)

### Frontend
- **Bootstrap + Vanilla JS / HTMX**: Hızlı prototipleme için yeterli
- **Jinja Templating**: FastAPI ile entegre frontend
- **Drag-and-drop görsel yükleme**, **interaktif form alanları**, **Pinterest-style grid**

### Ek Teknolojiler
- **RAG (Retrieval-Augmented Generation)**: Hazır veri setlerinden örnekler ile AI çıktılarının zenginleştirilmesi
- **Auth system**: FastAPI ile kullanıcı girişi (JWT veya session tabanlı)
- **File Storage**: Local veya cloud (örn. S3, Cloudinary opsiyonel)

---

## 🧪 MVP Özellikleri

1. ✅ Kullanıcı girişi ve kayıt sistemi
2. ✅ Ürün fotoğrafı yükleme arayüzü
3. ✅ AI tabanlı görsel analiz ve açıklama üretimi (CLIP veya benzeri)
4. ✅ Kullanıcıdan materyal girişi alınması (checkbox veya keyword)
5. ✅ AI tarafından eldeki ürün + materyallere göre yaratıcı upcycling fikirleri sunulması
6. ✅ Seçilen fikir için adım adım yol haritası (GPT destekli)
7. ✅ Paylaşım sayfası: kullanıcılar tamamlanan projelerini sistemde paylaşabilir
8. ✅ Basit bir “Explore” sayfası: diğer kullanıcı projelerine göz atma (Pinterest benzeri grid)

---

## 🛠 3 Günlük Geliştirme Yol Haritası

### 🟢 **Gün 1 – Temel Sistem Yapısı ve AI Entegrasyonu**

- [ ] Proje yapısını oluştur (`backend`, `frontend`, `static`, `templates`, `models`, `utils`)
- [ ] PostgreSQL + FastAPI entegrasyonunu yap
- [ ] Kullanıcı modelini ve Auth sistemini kur
- [ ] Görsel yükleme endpoint'ini hazırla (`/upload`)
- [ ] CLIP / BLIP ile yüklenen görsellerin otomatik açıklamasını üret
- [ ] Örnek 2–3 ürün için statik bir geri dönüşüm öneri listesi oluştur (dummy response)

**Teslim:** Kullanıcı fotoğraf yükler → görsel analizi yapılır → basit öneriler döner.

---

### 🟡 **Gün 2 – Materyal Seçimi, GPT & RAG, Yol Haritası Üretimi**

- [ ] Görsel analizden sonra “elinizde ne var?” formunu oluştur (checkbox input / text tags)
- [ ] Kullanıcının materyal seçimiyle birlikte, AI'a input gönder
- [ ] GPT ile materyal + ürün açıklaması üzerinden geri dönüşüm önerileri üret
- [ ] Seçilen fikir için adım adım bir yol haritası oluştur (GPT veya OpenRouter API)
- [ ] Basit bir diffusion API ile örnek proje görseli üret (isteğe bağlı, dummy de olabilir)
- [ ] RAG pipeline'ı (örneğin HuggingFace + Qdrant) entegre et ve örnek bir sorgu sonucu getir

**Teslim:** Kullanıcı fikir seçer → roadmap ve görsel çıktısı döner.

---

### 🟣 **Gün 3 – Sosyal Modül, Explore Sayfası ve UI İyileştirmeleri**

- [ ] Kullanıcılar tamamlanan projeleri “Benim Projelerim” kısmına ekleyebilmeli
- [ ] Tüm projeler için “Explore” / “Community” sayfası (Pinterest-style grid)
- [ ] Like sistemi (opsiyonel)
- [ ] UI/UX revizyonu: mobile responsive, sade ve akıcı arayüz
- [ ] Proje sonunda minik bir “Projenizi PDF olarak indir” butonu
- [ ] README, API docs ve demo içeriği hazırlanması

**Teslim:** Kullanıcı deneyimi akıcı, paylaşım yapılabilen ve minimum viable şekilde çalışan demo app.

---

## 📦 Gelecek Geliştirmeler (Post-MVP)

- Diffusion model ile görsel üretimin iyileştirilmesi
- Yerel servislerle eşleştirme (harita entegrasyonu)
- Kendi fikirlerini tasarlayıp paylaşabilme (3D veya Canva tarzı arayüz)
- Gamification (rozetler, sıralama sistemi)
- Erişilebilirlik (WCAG) standartları

---

## ✨ Vizyon

> “Çöp değil, potansiyel!”  
Trash2Treasure, tüketim toplumunun israf kültürüne yaratıcı ve sürdürülebilir bir alternatif sunar. Yapay zekâ ile bireyleri dönüşüm sürecine dahil eder, döngüsel ekonomiye katkı sağlar.

