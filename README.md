# Scoutium Makine Ogrenmesi ile Yetenek Avciligi Siniflandirma

## İş Problemi:

Scoutlar tarafından izlenen futbolcuların özelliklerine verilen puanlara göre, oyuncuların hangi sınıf (average, highlighted) oyuncu olduğunu tahminleme.

## Veriseti Hikayesi:

* Veri seti Scoutium’dan maçlarda gözlemlenen futbolcuların özelliklerine göre, scoutların değerlendirdikleri futbolcuların, maç içerisinde puanlanan özellikleri ve puanlarını içeren bilgilerden oluşmaktadır.

* attributes: Oyuncuları değerlendiren kullanıcıların bir maçta izleyip değerlendirdikleri her oyuncunun özelliklerine verdikleri puanları içeriyor. (bağımsız değişkenler)

* potential_labels: Oyuncuları değerlendiren kullanıcıların her bir maçta oyuncularla ilgili nihai görüşlerini içeren potansiyel etiketlerini içeriyor. (hedef değişken)

## Veriseti Hakkında:

9 Değişken, 10730 Gözlem, 0.65 mb

### Değişkenler:

* task_response_id: Bir scoutun bir maçta bir takımın kadrosundaki tüm oyunculara dair değerlendirmelerinin kümesi.

* match_id: İlgili maçın id'si.

* evaluator_id: Değerlendiricinin(scout'un) id'si.

* player_id: İlgili oyuncunun id'si.

*  position_id: İlgili oyuncunun o maçta oynadığı pozisyonun id'si.
  1.  Kaleci
  2.  Stoper
  3.  Sağ bek
  4.  Sol bek
  5.  Defansif orta saha
  6.  Merkez orta saha
  7.  Sağ kanat
  8.  Sol kanat
  9.  Ofansif orta saha
  10.  Forvet

* analysis_id: Bir scoutun bir maçta bir oyuncuya dair özellik değerlendirmelerini içeren küme.
* attribute_id: Oyuncuların değerlendirildiği her bir özelliğin id'si.
* attribute_value: Bir scoutun bir oyuncunun bir özelliğine verilen değer(puan).
* potential_label: Bir scoutun bir maçta bir oyuncuyla ilgili nihai kararını belirten etiket. (hedef değişken)

## Proje Aşamaları:

### Görev 1: scoutium_attributes.csv ve scoutium_potential_labels.csv dosyalarını okutunuz.
### Görev 2: Okutmuş olduğumuz CSV dosyalarını merge fonksiyonunu kullanarak birleştirelim.  ("task_response_id", 'match_id', 'evaluator_id' "player_id"  4 adet değişken üzerinden birleştirme işlemini gerçekleştiriniz.)
### Görev 3: position_id içerisindeki Kaleci (1) sınıfını verisetinden kaldırınız.
### Görev 4: potential_label içerisindeki below_average sınıfını verisetinden kaldırınız.( below_average sınıfı  tüm verisetinin %1'ini oluşturur)
### Görev 5: Oluşturduğunuz verisetinden “pivot_table” fonksiyonunu kullanarak bir tablo oluşturunuz. Bu pivot table'da her satır bir oyuncu olacak şekilde manipülasyon yapınız.
1. Her sütunda oyuncunun “position_id”, “potential_label” ve her oyuncunun sırayla bütün “attribute_idleri” içerecek şekilde işlem yapınız.
2. “reset_index” fonksiyonunu kullanarak index hatasından kurtulunuz ve “attribute_id” sütunlarının isimlerini stringe çeviriniz. (df.columns.map(str))

### Görev 6:  Label Encoder fonksiyonunu kullanarak “potential_label” kategorilerini (average, highlighted) sayısal olarak ifade ediniz.
### Görev 7: Sayısal değişken kolonlarını “num_cols” adıyla bir listeye kaydediniz.
### Görev 8: Kaydettiğiniz bütün “num_cols” değişkenlerindeki veriyi ölçeklendirmek için standardScaler uygulayınız.
### Görev 9: Elimizdeki veri seti üzerinden minimum hata ile futbolcuların potansiyel etiketlerini tahmin eden bir makine öğrenmesi modeli geliştiriniz.
### Görev 10: Değişkenlerin önem düzeyini belirten feature_importance fonksiyonunu kullanarak özelliklerin sıralamasını çizdiriniz.
