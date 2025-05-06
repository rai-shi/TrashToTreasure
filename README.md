# ♻️ Trash To Treasure

Kullanıcıların kullanmadıkları eşyaları dönüştürerek tekrar kullanabilmelerine imkan sağlayan sürdürülebilirlik odaklı bir web uygulamasıdır. Kullanıcılar sadece kullanmadıklarını ürünlerinin fotoğrafını sisteme yükler, sistem bu ürünü analiz ederek kullanıcının ne gibi yaratıcı geri dönüşüm projeleri üretilebileceğini önerir. Dahası kullanıcıya geri dönüşüm projelerinde gerekli olabilecek materyalleri ve proje adımlarını da sunar. 

Bu proje sayesinde daha sürdürülebilir bir yaşam tarzı teşvik edilirken, bireylerin atıklarını azaltmaları, yapay zekanın yaratıcılık gücünü kullanarak çevreye duyarlı çözümler üretmeleri ve toplumsal farkındalık kazanmaları sağlanır.

## 🧩 Proje Senaryosu

1. Kullanıcı sisteme giriş yapar.
2. Elinde geri dönüştürmek istediği bir ürünün fotoğrafını yükler.
3. AI, görsel tanıma yoluyla ürünü analiz eder.
4. Sistem, kullanıcıya 3 geri dönüşüm fikri sunar (örneğin: eski tişört ➝ çanta, minder kılıfı, ip).
5. Kullanıcı AI fikirlerini (açıklama, gerekli materyaller, geri dönüşüm fikri yol haritası) inceleyerek bir geri dönüşüm fikri seçer.
6. Seçili ürün fikri veri tabanımıza kayıt edilir.
7. Kullanıcı geri dönüşüm fikirlerini profil sayfasında görüntüleyebilir.
8. Kullanıcı ürünün geri dönüşüm fikrini uyguladığında geri dönüştürülmüş ürün görüntüsünü yükleyip projeyi public'e çekebilir. Böylece kullanıcılar uygulama içinde yaptıkları projeleri paylaşabilir, diğer kullanıcıların projelerine göz atabilir.


## ⚙️ Teknik Mimari
* Backend için FastAPI tercih edilmiştir.
* Veri tabanı olarak SQLite kullanılmıştır.
* Görüntü işleme ve proje fikirleri üretimi için Google Gemini modeli (gemini-2.0-flash) kullanılmıştır.
* Arayüz React Framework ile geliştirilmiştir.


## 🛠️ MVP Özellikleri

* Kullanıcı kayıt ve giriş sistemi
* Geri dönüşüm ürün fotoğrafı yükleme arayüzü
* AI tabanlı görsel analiz ve geri dönüşüm fikri üretimi
* Geri dönüşüm fikirleri için materyal ve adım adım yol haritası 
* Geri dönüştürülmüş ürün fotoğrafının projeye eklenebilmesi


## ✨ Gelecek Geliştirmeler (Post-MVP)

- MVP Ver-1 aşamasında kullanıcı geri dönüşüm fikrini uygulayıp projeyi gerçekleştirdiğinde geri dönüştürülmüş ürün fotoğrafını sisteme yükleyebilmektedir. Buna ek olarak gelecek versiyonda projeyi public hale getirip ana sayfada görüntülenebilmesi ve kullanıcının kendi projesine yorum ekleyebilmesi sağlanacaktır. Böylece kullanıcılar başka projelerden de ilham alabilir.
- Public projeleri favorilere ekleme özelliği eklenecektir. 
- Yapay zeka eklentisi geliştirilerek yapay zekanın yalnızca metin değil görüntü de üretmesi sağlanarak proje adımları görselleştirilecektir.
- Arayüz iyileştirmeleri yapılacaktır.


## 🔧 Projeyi Çalıştırma Adımları (Kurulum ve Geliştirme Ortamı)
1. Proje içinde Python venv ile ya da conda ile virtual environment oluşturmanız önerilir. (python==3.12)
2. env aktive edildikten sonra `pip install -r requirements.txt`
3. Kendi .env dosyanızı oluşturun içinde şu bilgiler bulunmalı
```
JWT_SECRET_KEY=your-jwt-key
JWT_ALGORITHM=HS256
SQLALCHAMY_DATABASE_URL=sqlite:///./your_db_name.db
GEMINI_API_KEY=your-key
```
4. TrashToTreasure/backend altında `uvicorn main:app --reload`
5. TrashToTreasure/frontend altında `npm start`
6. localhost:3000 altında arayüz açılacaktır.


## Bizimle İletişime Geçin

Proje hakkında sorularınız, önerileriniz ya da katkılarınız olursa bize GitHub üzerinden ulaşabilir ya da pull request açabilirsiniz. Her türlü geri bildirime açığız! 
- [Ayşenur Tak](https://github.com/aysenurtak) – Proje sahibi ve geliştirici  
- [](https://github.com/arkadas1) – Arayüz geliştirme  
- [](https://github.com/arkadas2) – AI entegrasyonu  
.


