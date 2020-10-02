from fitbit.api import Fitbit


class CustomFitbit(Fitbit):
    def get_activity_summary(self, user_id: str, date: str):
        url = "{0}/{1}/user/{2}/activities/date/{3}.json".format(
            *self._get_common_args(user_id), date)
        return self.make_request(url)

    def get_food_summary(self, user_id: str, date: str):
        url = "{0}/{1}/user/{2}/foods/log/date/{3}.json".format(
            *self._get_common_args(user_id), date)
        return self.make_request(url)

    def get_water_summary(self, user_id: str, date: str):
        url = "{0}/{1}/user/{2}/foods/log/water/date/{3}.json".format(
            *self._get_common_args(user_id), date)
        return self.make_request(url)

    def get_body_fat_logs(self, user_id: str, date: str):
        url = "{0}/{1}/user/{2}/body/log/fat/date/{3}.json".format(
            *self._get_common_args(user_id), date)
        return self.make_request(url)

    def get_body_weight_logs(self, user_id: str, date: str):
        url = "{0}/{1}/user/{2}/body/log/weight/date/{3}.json".format(
            *self._get_common_args(user_id), date)
        return self.make_request(url)
