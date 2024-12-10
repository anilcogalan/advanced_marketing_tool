# Marketing Analytics Toolkit

![PyPI version](https://img.shields.io/pypi/v/marketing-analytics-toolkit.svg)
![Python versions](https://img.shields.io/pypi/pyversions/marketing-analytics-toolkit.svg)
![License](https://img.shields.io/github/license/yourusername/marketing-analytics-toolkit.svg)

Marketing Analytics Toolkit, pazarlama profesyonelleri ve veri bilimciler için geliştirilmiş kapsamlı bir Python kütüphanesidir. Bu toolkit, müşteri segmentasyonu, pazarlama karması optimizasyonu ve müşteri yaşam döngüsü analizi gibi ileri düzey pazarlama analitik araçları sunar.

## 🚀 Özellikler

### 🎯 Müşteri Segmentasyonu
- RFM (Recency, Frequency, Monetary) analizi
- Davranışsal segmentasyon
- Demografik segmentasyon
- K-means ve hierarchical clustering algoritmaları
- Özel segment skorlama sistemleri

### 📊 Pazarlama Karması Optimizasyonu
- 4P analizi (Price, Product, Place, Promotion)
- Kanal performans analizi
- Bütçe optimizasyonu
- ROI hesaplamaları
- A/B test analizi

### 🔄 Müşteri Yaşam Döngüsü Analizi
- Churn tahminleme
- Müşteri değer hesaplaması (CLV)
- Satın alma olasılığı modellemesi
- Müşteri yolculuğu analizi
- Cohort analizi

### 📈 Kanal Atribüsyon Modellemesi
- First-touch attribution
- Last-touch attribution
- Multi-touch attribution
- Markov Chain modelleri
- Custom attribution modelleri

## 🛠️ Kurulum

pip ile kurulum:
```bash
pip install marketing-analytics-toolkit
```

Geliştirici kurulumu:
```bash
git clone https://github.com/yourusername/marketing-analytics-toolkit.git
cd marketing-analytics-toolkit
pip install -e .
```

## 📖 Hızlı Başlangıç

### Müşteri Segmentasyonu Örneği
```python
from marketing_analytics.models import AdvancedSegmentationModel
from marketing_analytics.utils import prepare_data

# Veri hazırlığı
data = prepare_data(your_data)

# Model başlatma
model = AdvancedSegmentationModel(
    n_segments=3,
    method='kmeans',
    random_state=42
)

# Model eğitimi ve tahmin
segments = model.fit_predict(data)

# Segment önerileri alma
recommendations = model.get_segment_recommendations(
    segment_id=0,
    data=data
)
```

### RFM Analizi Örneği
```python
from marketing_analytics.analysis import RFMAnalysis

# RFM analizi başlatma
rfm = RFMAnalysis(
    date_column='purchase_date',
    customer_id_column='customer_id',
    revenue_column='amount'
)

# RFM skorlarını hesaplama
rfm_scores = rfm.calculate_scores(transaction_data)

# Segment özetlerini görüntüleme
segment_summary = rfm.get_segment_summary()
```

## 📊 Görselleştirme Araçları

Kütüphane, çeşitli görselleştirme araçları sunar:

```python
from marketing_analytics.visualization import (
    plot_customer_segments,
    plot_channel_performance,
    plot_customer_journey
)

# Müşteri segmentlerini görselleştirme
plot_customer_segments(segments_data)

# Kanal performansını görselleştirme
plot_channel_performance(channel_data)
```

## 📚 Detaylı Dokümantasyon

Daha detaylı bilgi için [dokümantasyonumuzu]("") ziyaret edin.

## 🤝 Katkıda Bulunma

Projeye katkıda bulunmak için:

1. Bu repository'yi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Bir Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 📫 İletişim

- Proje Sahibi: [Your Name](mailto:your.email@example.com)
- Twitter: [@yourusername](https://twitter.com/yourusername)
- LinkedIn: [Your Name](https://linkedin.com/in/yourusername)

## 🙏 Teşekkürler

Bu projeye katkıda bulunan herkese teşekkür ederiz. Katkıda bulunanların tam listesi için [CONTRIBUTORS.md](CONTRIBUTORS.md) dosyasına bakın.

## 📌 Alıntılama

Bu projeyi akademik çalışmalarınızda kullanıyorsanız, lütfen aşağıdaki gibi alıntılayın:

```bibtex
@software{marketing_analytics_toolkit,
  author = {Your Name},
  title = {Marketing Analytics Toolkit},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/yourusername/marketing-analytics-toolkit}
}
```

