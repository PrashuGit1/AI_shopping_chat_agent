import sqlite3

conn = sqlite3.connect("phones.db")
cursor = conn.cursor()


phones = [
    ('Pixel 8a','Google',29999,50,4500,6.1,8,128,'Tensor G2','Strong camera software; clean Android'),
    ('OnePlus Nord CE 4','OnePlus',24999,64,5000,6.6,8,128,'Snapdragon 7 Gen 3','Good value'),
    ('Samsung A55','Samsung',27999,64,5000,6.6,8,128,'Exynos 1380','Great display'),
    ('Xiaomi Redmi Note 13','Xiaomi',15999,108,6000,6.67,8,256,'Dimensity 7020','Excellent battery'),
    ('iPhone SE (2022)','Apple',30999,12,2018,4.7,4,64,'A15 Bionic','Compact form factor'),
    ('Realme 12 Pro','Realme',19999,50,5000,6.72,8,128,'Helio G99','Balanced performer')
]


cursor.executemany("""
INSERT INTO phones (model, brand, price, camera_mp, battery_mah, display_inch, ram_gb, storage_gb, soc, notes)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", phones)


conn.commit()
conn.close()

print("✅ Sample phone data inserted successfully!")
