import streamlit as st
import datetime
import sqlite3

# Veritabanı bağlantısını açıyoruz.
conn = sqlite3.connect('ideas.db')
c = conn.cursor()

# İdealar tablosunu oluşturuyoruz.
c.execute('CREATE TABLE IF NOT EXISTS ideas (idea TEXT, name TEXT, timestamp TEXT)')

# Streamlit uygulamasını başlatıyoruz.
st.title("Öneri Kaydedici")

# İlk textbox kullanıcının fikrini yazacağı yer.
idea = st.text_input("Fikrinizi buraya yazın:")

# İkinci textbox kullanıcının adını yazacağı yer.
name = st.text_input("Adınızı buraya yazın:")

# Eğer kullanıcı hem fikrini hem de adını girdiyse, kayıt işlemi yapılır.
if st.button("Kaydet"):
    if idea and name:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Veritabanına kaydediyoruz.
        c.execute('INSERT INTO ideas (idea, name, timestamp) VALUES (?, ?, ?)', (idea, name, timestamp))
        conn.commit()
        st.success("Fikir başarıyla kaydedildi!")
    else:
        st.warning("Lütfen fikir ve ad alanlarını doldurun.")

# Şimdi, kaydedilmiş fikirleri ekrana yazdırıyoruz.
st.write("\n\n")
st.header("Kaydedilmiş Fikirler")
c.execute('SELECT * FROM ideas')
ideas = c.fetchall()
if not ideas:
    st.write("Henüz kaydedilmiş bir fikir yok.")
else:
    for i, (idea, name, timestamp) in enumerate(ideas):
        st.write(f"{i+1}. **{idea}** - {name} ({timestamp})")

# Veritabanı bağlantısını kapatıyoruz.
c.close()
conn.close()
