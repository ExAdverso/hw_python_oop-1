class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = (duration)
        self.distance = (distance)
        self.speed = (speed)
        self.calories = (calories)

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * Training.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.__class__.__name__, 
                              self.duration,
                              self.get_distance(), 
                              self.get_mean_speed(),
                              self.get_spent_calories())
        return message


class Running(Training):
    """Тренировка: бег."""
    COEF_CALORIE_RUN: int = 18
    COEF_CALORIE_RUN1: int = 20
    MIN: int = 60

    def get_spent_calories(self) -> float:
        return ((self.COEF_CALORIE_RUN * self.get_mean_speed()
                - self.COEF_CALORIE_RUN1) * self.weight / self.M_IN_KM
                * (self.duration * Running.MIN))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEF_CALORIE_W: float = 0.035 
    COEF_CALORIE_W1: float = 0.029
    MIN: int = 60
    
    def __init__(self, action: int, duration: float, weight: float, height: float) -> None:    
        super().__init__(action, duration, weight)
        self.height = height
    
    def get_spent_calories(self) -> float:
        return (self.COEF_CALORIE_W* self.weight
                + (self.get_mean_speed()**2 // self.height) 
                * self.COEF_CALORIE_W1 * self.weight) * (self.duration * Running.MIN)
                                                                         
                                                         
class Swimming(Training):
    """Тренировка: плавание."""
    COEF_CALORIE_SW: float = 1.1
    COEF_CALORIE_SW1: float = 2.0
    LEN_STEP: float = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return (self.action * Swimming.LEN_STEP) / Training.M_IN_KM
    
    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / Training.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEF_CALORIE_SW)
                * self.COEF_CALORIE_SW1 * self.weight)
    

def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    read: dict[str, Training] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }
    if read.get(workout_type) is None:
        return None
    readdat = read.get(workout_type)(*data)
    return readdat


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

