from app.extensions import db  

class City(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __repr__(self):
        return f"<City {self.name} ({self.latitude}, {self.longitude})>"
    
def init_cities():
    # Initialize the cities table with some data
    db.create_all()
    if not City.query.first():

        cities = [
            City(name="Amsterdam", latitude=52.3676, longitude=4.9041),
            City(name="Athens", latitude=37.9838, longitude=23.7275),
            City(name="Belgrade", latitude=44.7866, longitude=20.4489),
            City(name="Berlin", latitude=52.52, longitude=13.405),
            City(name="Bila Tserkva", latitude=49.7950, longitude=30.1000),
            City(name="Bratislava", latitude=48.1482, longitude=17.1067),
            City(name="Brussels", latitude=50.8503, longitude=4.3517),
            City(name="Bucharest", latitude=44.4268, longitude=26.1025),
            City(name="Budapest", latitude=47.4979, longitude=19.0402),
            City(name="Cherkasy", latitude=49.4444, longitude=32.0592),
            City(name="Chernihiv", latitude=51.5055, longitude=31.2890),
            City(name="Chernivtsi", latitude=48.2915, longitude=25.9350),
            City(name="Copenhagen", latitude=55.6761, longitude=12.5683),
            City(name="Dnipro", latitude=48.4647, longitude=35.0462),
            City(name="Donetsk", latitude=48.0159, longitude=37.8029),
            City(name="Dublin", latitude=53.3498, longitude=-6.2603),
            City(name="Gdansk", latitude=54.3520, longitude=18.6466),
            City(name="Helsinki", latitude=60.1695, longitude=24.9354),
            City(name="Istanbul", latitude=41.0082, longitude=28.9784),
            City(name="Ivano-Frankivsk", latitude=48.9220, longitude=24.7111),
            City(name="Kharkiv", latitude=49.9935, longitude=36.2304),
            City(name="Kherson", latitude=46.6354, longitude=32.6160),
            City(name="Khmelnytskyi", latitude=49.4214, longitude=27.0089),
            City(name="Krakow", latitude=50.0647, longitude=19.9450),
            City(name="Kropyvnytskyi", latitude=48.5044, longitude=32.2622),
            City(name="Kyiv", latitude=50.4501, longitude=30.5234),
            City(name="Lisbon", latitude=38.7223, longitude=-9.1393),
            City(name="Ljubljana", latitude=46.0569, longitude=14.5051),
            City(name="London", latitude=51.5074, longitude=-0.1278),
            City(name="Luhansk", latitude=48.5740, longitude=39.3072),
            City(name="Lutsk", latitude=50.7479, longitude=25.3252),
            City(name="Lviv", latitude=49.8397, longitude=24.0297),
            City(name="Madrid", latitude=40.4168, longitude=-3.7038),
            City(name="Mukachevo", latitude=48.4444, longitude=22.7181),
            City(name="Mykolaiv", latitude=46.9750, longitude=31.9946),
            City(name="Odesa", latitude=46.4825, longitude=30.7233),
            City(name="Oslo", latitude=59.9139, longitude=10.7522),
            City(name="Paris", latitude=48.8566, longitude=2.3522),
            City(name="Podgorica", latitude=42.4411, longitude=19.2636),
            City(name="Poltava", latitude=49.5883, longitude=34.5514),
            City(name="Poznan", latitude=52.4084, longitude=16.9342),
            City(name="Prague", latitude=50.0755, longitude=14.4378),
            City(name="Pristina", latitude=42.6629, longitude=21.1655),
            City(name="Riga", latitude=56.9496, longitude=24.1052),
            City(name="Rivne", latitude=50.6192, longitude=26.2516),
            City(name="Rome", latitude=41.9028, longitude=12.4964),
            City(name="Sarajevo", latitude=43.8486, longitude=18.3564),
            City(name="Skopje", latitude=41.9973, longitude=21.4280),
            City(name="Sofia", latitude=42.6977, longitude=23.3219),
            City(name="Stockholm", latitude=59.3293, longitude=18.0686),
            City(name="Sumy", latitude=50.9070, longitude=34.7982),
            City(name="Tallinn", latitude=59.4372, longitude=24.7536),
            City(name="Ternopil", latitude=49.5535, longitude=25.5942),
            City(name="Tirana", latitude=41.3275, longitude=19.8189),
            City(name="Uzhhorod", latitude=48.6202, longitude=22.2870),
            City(name="Vienna", latitude=48.2082, longitude=16.3738),
            City(name="Vilnius", latitude=54.6872, longitude=25.2797),
            City(name="Vinnytsia", latitude=49.2328, longitude=28.4682),
            City(name="Warsaw", latitude=52.2297, longitude=21.0122),
            City(name="Wroclaw", latitude=51.1079, longitude=17.0385),
            City(name="Zagreb", latitude=45.8150, longitude=15.9819),
            City(name="Zaporizhzhia", latitude=47.8388, longitude=35.1390),
            City(name="Zhytomyr", latitude=50.2620, longitude=28.6582),
            City(name="Zurich", latitude=47.3769, longitude=8.5417)
        ]

        db.session.bulk_save_objects(cities)
        db.session.commit()