from _typeshed import Self


class InfoMessage:
    def __init__(self,training_type,duration,distance,speed,calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
    """Информационное сообщение о тренировке."""
    def show_training_info(self):
        return ( f' Тип тренировки: {self.training_type};' 
                 f'Длительность: {duration} ч.; Дистанция: {distance} км;'               
                 f'Ср. скорость: {speed} км/ч; Потрачено ккал: {calories}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * Training.LEN_STEP / Training.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed


    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(self.duration(),
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""
    cf_calorie1 = 18
    cf_calorie2 = 20
    def get_spent_calories(self) -> float:
        calories = (cf_calorie1 * self.get_mean_speed() - cf_calorie2)  * self.weight / Training.M_IN_KM * self.duration
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    cf_calorie3 = 0.035
    cf_calorie4 = 2
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super.__init__(action,duration,weight)         
        self.height = height

    def get_spent_calories(self) -> float:  
        calories = (cf_calorie3 * self.weight + ( self.speed ** cf_calorie4 // self.height ) * self.duration)

class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    cf_calorie5 = 1.1
    cf_calorie6 = 2
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 lenght_pool,
                 count_pool,
                 ) -> None:
     super.__init__(action,duration,weight)
     self.lenght_pool = lenght_pool
     self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        speed = self.lenght_pool * self.count_pool / Training.M_IN_KM / self.duration
        return speed

    def get_spent_calories(self) -> float:
        calories = (self.speed + cf_calorie5) * cf_calorie6 * self.weight
        return calories

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * Swimming.LEN_STEP / Training.M_IN_KM
        return distance   



def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    Reader: dict = {'SWM':Swimming,
                    'RUN':Running,
                    'WLK':SportsWalking}
    NewTraining = Reader[workout_type](data[0],data[1],data[2],data[3],data[4])
    


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    info.get_message()


if __name__ == "__main__":
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

