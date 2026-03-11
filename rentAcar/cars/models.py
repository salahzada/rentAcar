from django.db import models
from datetime import datetime


def year_choices():
    return [(year, year) for year in range(1918, datetime.now().year + 1)]

class DeletedCar(models.Model):
    # Original car data snapshot
    original_car_id = models.IntegerField()
    carBrand = models.CharField(max_length=100)
    carModel = models.CharField(max_length=100)
    carCategory = models.CharField(max_length=100)
    carYear = models.IntegerField()
    carKM = models.DecimalField(max_digits=10, decimal_places=2)
    carFuelType = models.CharField(max_length=50, null=True, blank=True)
    bensinType = models.CharField(max_length=50, null=True, blank=True)
    carType = models.CharField(max_length=50)
    karopkaType = models.CharField(max_length=50)
    dailyRentPrice = models.DecimalField(max_digits=10, decimal_places=0)
    carLocation = models.CharField(max_length=255, null=True, blank=True)
    carIdNumber = models.CharField(max_length=100)
    carRegistrationNumber = models.CharField(max_length=100)
    carColor = models.CharField(max_length=100)
    carMotor = models.DecimalField(max_digits=5, decimal_places=1)
    carSits = models.IntegerField()
    isPersonal = models.CharField(max_length=10)

    # Who owned it
    owner_username = models.CharField(max_length=150)
    owner_full_name = models.CharField(max_length=300, null=True, blank=True)

    # When it was deleted and by whom
    deleted_at = models.DateTimeField(auto_now_add=True)
    deleted_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deleted_cars'
    )

    def __str__(self):
        return f"[DELETED] {self.carBrand} {self.carModel} ({self.carYear}) — {self.deleted_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        db_table = "deleted_cars"
        ordering = ["-deleted_at"]
        verbose_name = "Deleted Car"
        verbose_name_plural = "Deleted Cars"

class Car(models.Model):

    BRAND_CHOICES = [
        ('mercedes', 'Mercedes-Benz'),
        ('bmw', 'BMW'),
        ('audi', 'Audi'),
        ('toyota', 'Toyota'),
        ('honda', 'Honda'),
        ('volkswagen', 'Volkswagen'),
        ('ford', 'Ford'),
        ('chevrolet', 'Chevrolet'),
        ('nissan', 'Nissan'),
        ('hyundai', 'Hyundai'),
        ('kia', 'Kia'),
        ('lexus', 'Lexus'),
        ('porsche', 'Porsche'),
        ('ferrari', 'Ferrari'),
        ('lamborghini', 'Lamborghini'),
        ('maserati', 'Maserati'),
        ('jaguar', 'Jaguar'),
        ('land_rover', 'Land Rover'),
        ('volvo', 'Volvo'),
        ('subaru', 'Subaru'),
        ('mazda', 'Mazda'),
        ('mitsubishi', 'Mitsubishi'),
        ('peugeot', 'Peugeot'),
        ('renault', 'Renault'),
        ('fiat', 'Fiat'),
        ('alfa_romeo', 'Alfa Romeo'),
        ('seat', 'SEAT'),
        ('skoda', 'Skoda'),
        ('tesla', 'Tesla'),
        ('jeep', 'Jeep'),
        ('dodge', 'Dodge'),
        ('chrysler', 'Chrysler'),
        ('cadillac', 'Cadillac'),
        ('buick', 'Buick'),
        ('infiniti', 'Infiniti'),
        ('acura', 'Acura'),
        ('genesis', 'Genesis'),
        ('bentley', 'Bentley'),
        ('rolls_royce', 'Rolls-Royce'),
        ('aston_martin', 'Aston Martin'),
        ('mclaren', 'McLaren'),
        ('bugatti', 'Bugatti'),
        ('lada', 'Lada'),
        ('opel', 'Opel'),
    ]

    MODEL_CHOICES = [
        # Mercedes
        ('c180', 'C180'), ('c200', 'C200'), ('c250', 'C250'), ('c300', 'C300'),
        ('e200', 'E200'), ('e250', 'E250'), ('e300', 'E300'), ('e350', 'E350'),
        ('s350', 'S350'), ('s450', 'S450'), ('s500', 'S500'), ('s600', 'S600'),
        ('gle300', 'GLE 300'), ('gle350', 'GLE 350'), ('gle450', 'GLE 450'),
        ('glc200', 'GLC 200'), ('glc300', 'GLC 300'),
        ('cla180', 'CLA 180'), ('cla200', 'CLA 200'), ('cla250', 'CLA 250'),
        ('a180', 'A180'), ('a200', 'A200'), ('a250', 'A250'),
        # BMW
        ('bmw_118i', '118i'), ('bmw_120i', '120i'),
        ('bmw_320i', '320i'), ('bmw_330i', '330i'), ('bmw_340i', '340i'),
        ('bmw_520i', '520i'), ('bmw_530i', '530i'), ('bmw_540i', '540i'), ('bmw_550i', '550i'),
        ('bmw_730i', '730i'), ('bmw_740i', '740i'), ('bmw_750i', '750i'),
        ('bmw_x3', 'X3'), ('bmw_x5', 'X5'), ('bmw_x6', 'X6'), ('bmw_x7', 'X7'),
        ('bmw_m3', 'M3'), ('bmw_m5', 'M5'),
        # Audi
        ('a3', 'A3'), ('a4', 'A4'), ('a5', 'A5'), ('a6', 'A6'), ('a7', 'A7'), ('a8', 'A8'),
        ('q3', 'Q3'), ('q5', 'Q5'), ('q7', 'Q7'), ('q8', 'Q8'),
        ('rs3', 'RS3'), ('rs6', 'RS6'), ('tt', 'TT'), ('r8', 'R8'),
        # Toyota
        ('camry', 'Camry'), ('corolla', 'Corolla'), ('yaris', 'Yaris'),
        ('rav4', 'RAV4'), ('land_cruiser', 'Land Cruiser'), ('prado', 'Land Cruiser Prado'),
        ('highlander', 'Highlander'), ('fortuner', 'Fortuner'),
        ('prius', 'Prius'), ('avalon', 'Avalon'),
        # Honda
        ('civic', 'Civic'), ('accord', 'Accord'), ('hrv', 'HR-V'),
        ('crv', 'CR-V'), ('pilot', 'Pilot'), ('jazz', 'Jazz'),
        # Volkswagen
        ('golf', 'Golf'), ('passat', 'Passat'), ('jetta', 'Jetta'),
        ('tiguan', 'Tiguan'), ('touareg', 'Touareg'), ('polo', 'Polo'),
        # Ford
        ('focus', 'Focus'), ('fusion', 'Fusion'), ('mustang', 'Mustang'),
        ('explorer', 'Explorer'), ('escape', 'Escape'), ('f150', 'F-150'),
        # Hyundai
        ('elantra', 'Elantra'), ('sonata', 'Sonata'), ('tucson', 'Tucson'),
        ('santafe', 'Santa Fe'), ('i30', 'i30'), ('i10', 'i10'),
        # Kia
        ('sportage', 'Sportage'), ('sorento', 'Sorento'), ('cerato', 'Cerato'),
        ('optima', 'Optima'), ('stinger', 'Stinger'), ('telluride', 'Telluride'),
        # Lexus
        ('lexus_es300', 'ES300'), ('lexus_es350', 'ES350'),
        ('lexus_rx300', 'RX300'), ('lexus_rx350', 'RX350'), ('lexus_rx450', 'RX450h'),
        ('lexus_ls460', 'LS460'), ('lexus_lx570', 'LX570'),
        # Porsche
        ('cayenne', 'Cayenne'), ('macan', 'Macan'), ('panamera', 'Panamera'),
        ('911', '911'), ('taycan', 'Taycan'),
        # Tesla
        ('model_s', 'Model S'), ('model_3', 'Model 3'),
        ('model_x', 'Model X'), ('model_y', 'Model Y'),
        # Nissan
        ('qashqai', 'Qashqai'), ('xtrail', 'X-Trail'), ('altima', 'Altima'),
        ('maxima', 'Maxima'), ('pathfinder', 'Pathfinder'), ('patrol', 'Patrol'),
        # Lada
        ('lada_vesta', 'Vesta'), ('lada_granta', 'Granta'), ('lada_niva', 'Niva'),
        # Opel
        ('astra', 'Astra'), ('insignia', 'Insignia'), ('mokka', 'Mokka'),
    ]

    CATEGORY_CHOICES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('crossover', 'Crossover'),
        ('offroad', 'Off-Road'),
        ('hatchback', 'Hatchback'),
        ('coupe', 'Coupe'),
        ('convertible', 'Convertible'),
        ('wagon', 'Station Wagon'),
        ('minivan', 'Minivan'),
        ('pickup', 'Pickup Truck'),
        ('van', 'Van'),
        ('sports', 'Sports Car'),
        ('luxury', 'Luxury'),
        ('electric', 'Electric'),
    ]

    FUEL_TYPE_CHOICES = [
        ('benzin', 'Benzin'),
        ('diesel', 'Diesel'),
        ('gas', 'Gas'),
    ]

    BENZIN_TYPE_CHOICES = [
        ('92', 'Benzin 92'),
        ('95', 'Benzin 95'),
        ('98', 'Benzin 98'),
    ]

    CAR_TYPE_CHOICES = [
        ('none', 'None'),
        ('hibrid', 'Hibrid'),
        ('plugin_hibrid', 'Plugin Hibrid'),
        ('elektrik', 'Elektrik'),
    ]

    KAROPKA_TYPE_CHOICES = [
        ('avtomat', 'Avtomat'),
        ('mexaniki', 'Mexaniki'),
    ]

    COLOR_CHOICES = [
        ('white', 'White'),
        ('black', 'Black'),
        ('silver', 'Silver'),
        ('gray', 'Gray'),
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('orange', 'Orange'),
        ('brown', 'Brown'),
        ('beige', 'Beige'),
        ('gold', 'Gold'),
        ('purple', 'Purple'),
        ('pink', 'Pink'),
        ('other', 'Other'),
    ]

    IS_PERSONAL_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    carBrand = models.CharField(max_length=100, choices=BRAND_CHOICES)
    carModel = models.CharField(max_length=100, choices=MODEL_CHOICES)
    carCategory = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    carYear = models.IntegerField(choices=year_choices())
    carKM = models.DecimalField(max_digits=10, decimal_places=2)
    carFuelType = models.CharField(max_length=50, choices=FUEL_TYPE_CHOICES, null=True, blank=True)
    bensinType = models.CharField(max_length=50, choices=BENZIN_TYPE_CHOICES, null=True, blank=True)
    carType = models.CharField(max_length=50, choices=CAR_TYPE_CHOICES, default='none')
    karopkaType = models.CharField(max_length=50, choices=KAROPKA_TYPE_CHOICES)
    dailyRentPrice = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    carLocation = models.CharField(max_length=255, null=True, blank=True)
    carIdNumber = models.CharField(max_length=100,default=None)
    carRegistrationNumber = models.CharField(max_length=100,default=None)
    carColor = models.CharField(max_length=100, choices=COLOR_CHOICES,default=None)
    carMotor = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    carSits = models.IntegerField(default=5)
    isPersonal = models.CharField(max_length=10, choices=IS_PERSONAL_CHOICES, default='no')
    profile = models.ForeignKey('profiles.Profile', on_delete=models.SET_NULL, null=True, blank=True, related_name='cars')

    def __str__(self):
        return f"{self.carBrand} {self.carModel} ({self.carYear})"

    class Meta:
        db_table = "cars"
        ordering = ["-carYear"]