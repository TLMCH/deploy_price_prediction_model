
"""Класс FastApiHandler, который обрабатывает запросы API."""

import pandas as pd
import joblib
import logging


class FastApiHandler:
    """Класс FastApiHandler, который обрабатывает запрос и возвращает предсказание."""

    def __init__(self):
        """Инициализация переменных класса."""

        # типы параметров запроса для проверки
        self.param_types = {
            "flat_id": str,
            "model_params": dict
        }

        # загрузка модели
        self.model_path = "models/model.pkl"
        self.load_model(model_path=self.model_path)

        # загрузка column_transformer
        self.column_transformer_path = "models/column_transformer.pkl"
        self.load_column_transformer(column_transformer_path=self.column_transformer_path)

        # загрузка auto_feat_regressor
        self.auto_feat_regressor_path = "models/auto_feat_regressor.pkl"
        self.load_auto_feat_regressor(auto_feat_regressor_path=self.auto_feat_regressor_path)
        
        # необходимые параметры для предсказаний модели оттока
        self.required_model_params = [
                'id', 'flat_id', 'building_id', 'floor', 'kitchen_area', 'living_area', 'rooms', 
                'is_apartment', 'studio', 'total_area', 'build_year', 
                'building_type_int', 'latitude', 'longitude', 'ceiling_height', 'flats_count', 'floors_total', 'has_elevator'
            ]
        
        self.logger = logging.getLogger('fast_api_handler')
        self.logger.setLevel(logging.INFO)
        logger_handler = logging.FileHandler('ml_service/fast_api_handler_log.log')
        logger_handler.setLevel(logging.INFO)
        logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger_handler.setFormatter(logger_formatter)
        self.logger.addHandler(logger_handler)


    def load_model(self, model_path: str):
        """Загружаем обученную модель предсказания цены.
        Args:
            model_path (str): Путь до модели.
        """
        try:
            with open(model_path, 'rb') as fd:
                self.model = joblib.load(fd) 
        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")


    def load_column_transformer(self, column_transformer_path: str):
        """Загружаем обученный column_transformer.
        Args:
            column_transformer_path (str): Путь до column_transformer.
        """
        try:
            with open(column_transformer_path, 'rb') as fd:
                self.column_transformer = joblib.load(fd) 
        except Exception as e:
            self.logger.error(f"Failed to load column_transformer: {e}")

    
    def load_auto_feat_regressor(self, auto_feat_regressor_path: str):
        """Загружаем обученный auto_feat_regressor.
        Args:
            auto_feat_regressor_path (str): Путь до cauto_feat_regressor.
        """
        try:
            with open(auto_feat_regressor_path, 'rb') as fd:
                self.auto_feat_regressor = joblib.load(fd) 
        except Exception as e:
            self.logger.error(f"Failed to load auto_feat_regressor: {e}")


    def floor_type(self, row):
            if row['floor'] == 1:
                return 0
            elif row['floor'] == row['floors_total']:
                return 2
            else:
                return 1


    def d_f_c_long(self, x):
            return abs(x - 37.6)
    

    def d_f_c_lat(self, x):
            return abs(x - 55.74)
    

    def transform_data(self, original_model_params: dict) -> pd.DataFrame:
        """Трансформируем входные данные, для обработки моделью.
        Args:
            original_model_params (dict): Необработанные параметры для модели.
        Returns:
            pd.DataFrame: pandas DataFrame с обработанными данными.
        """
        data = pd.DataFrame(original_model_params, index=[0])

        data['floor_type'] = data.apply(self.floor_type, axis=1)
        data['distance_from_center_longitude'] = data['longitude'].apply(self.d_f_c_long)
        data['distance_from_center_latitude'] = data['latitude'].apply(self.d_f_c_lat)

        num_features = [
            'total_area',
            'build_year',
            'distance_from_center_latitude',
            'distance_from_center_longitude',
            'flats_count'
        ]

        encoded_data = self.column_transformer.transform(data)

        transformed_data = pd.DataFrame(
            encoded_data, 
            columns=self.column_transformer.get_feature_names_out()
        )

        afr_data = self.auto_feat_regressor.transform(data[num_features])

        concat_data = pd.concat([afr_data, transformed_data], axis=1)
        concat_data.drop(columns=num_features, inplace=True)
        top_features = ['1/distance_from_center_longitude', 'num__scaler__build_year', 'num__pol__distance_from_center_latitude', 
                        'num__pol__distance_from_center_longitude', 'num__pol__total_area^2', 'num__pol__total_area build_year flats_count', 
                        'num__pol__distance_from_center_longitude^3', 'cat__building_type_int_2', 'cat__building_type_int_4', 'cat__floor_type_0']

        return concat_data[top_features]
    

    def check_required_query_params(self, query_params: dict) -> bool:
        """Проверяем параметры запроса на наличие обязательного набора.
        
        Args:
            query_params (dict): Параметры запроса.
        
        Returns:
                bool: True — если есть нужные параметры, False — иначе
        """
        if "flat_id" not in query_params or "model_params" not in query_params:
            return False
        
        if not isinstance(query_params["flat_id"], self.param_types["flat_id"]):
            return False
                
        if not isinstance(query_params["model_params"], self.param_types["model_params"]):
            return False
        return True
    

    def check_required_model_params(self, model_params: dict) -> bool:
        """Проверяем параметры квартиры на наличие обязательного набора.
    
        Args:
            model_params (dict): Параметры квартиры для предсказания.
    
        Returns:
            bool: True — если есть нужные параметры, False — иначе
        """
        if set(model_params.keys()).issubset(self.required_model_params):
            return True
        return False
    

    def validate_params(self, params: dict) -> bool:
        """Разбираем запрос и проверяем его корректность.
    
        Args:
            params (dict): Словарь параметров запроса.
    
        Returns:
            - **dict**: Cловарь со всеми параметрами запроса.
        """
        if self.check_required_query_params(params):
            self.logger.info("All query params exist")
        else:
            self.logger.info("Not all query params exist")
            return False
        
        if self.check_required_model_params(params["model_params"]):
            self.logger.info("All model params exist")
        else:
            self.logger.info("Not all model params exist")
            return False
        return True
        

    def handle(self, params):
        """Функция для обработки входящих запросов по API. Запрос состоит из параметров.
    
        Args:
            params (dict): Словарь параметров запроса.
    
        Returns:
            - **dict**: Словарь, содержащий результат выполнения запроса.
        """
        try:
            # валидируем запрос к API
            if not self.validate_params(params):
                self.logger.error("Error while handling request")
                response = {"Error": "Problem with parameters"}
            else:
                model_params = self.transform_data(params["model_params"])
                flat_id = params["flat_id"]
                self.logger.info(f"Predicting for flat_id: {flat_id} and model_params:\n{model_params.to_dict('list')}")
                # получаем предсказания модели
                prediction = self.model.predict(model_params.iloc[0, :])
                response = {
                        "flat_id": flat_id, 
                        "prediction": prediction.round()
                    }
        except Exception as e:
            self.logger.error(f"Error while handling request: {e}")
            return {"Error": "Problem with request"}
        else:
            self.logger.info(response)
            return response
        

if __name__ == "__main__":

    # создаём тестовый запрос
    test_params = {
        "flat_id": "123",
        "model_params": {
            'id': 1, 
            'flat_id': 0, 
            'building_id': 6220, 
            'floor': 9, 
            'kitchen_area': 9.90, 
            'living_area': 19.900000, 
            'rooms': 1, 
            'is_apartment': False, 
            'studio': False, 
            'total_area': 35.099998, 
            'build_year': 1965, 
            'building_type_int': 6, 
            'latitude': 55.717113, 
            'longitude': 37.781120	, 
            'ceiling_height': 2.64, 
            'flats_count': 84, 
            'floors_total': 12, 
            'has_elevator': True
        }
    }

    # создаём обработчик запросов для API
    handler = FastApiHandler()

    # делаем тестовый запрос
    response = handler.handle(test_params)
    print(f"Response: {response}")